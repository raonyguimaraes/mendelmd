"""Load Pynnotator 3 (VEP-only) annotations into the variants table.

The filter, family and pathway analyses query ``variants.Variant``. Pynnotator 3
replaced the SnpEff/dbNSFP pipeline with a single VEP pass (``--pick``, one
consequence per variant), so this module maps VEP output onto the existing
Variant columns instead of the old ``parse_vcf`` layout:

* VEP Consequence -> ``snpeff_effect`` (SnpEff-style names used by the effect
  filter); VEP IMPACT -> ``snpeff_impact`` (same HIGH/MODERATE/LOW/MODIFIER
  vocabulary); ``snpeff_func_class`` derived from the consequence.
* Population frequencies reuse the legacy columns, relabelled in the UI:
  gnomAD genomes AF -> ``genomes1k_maf``, gnomAD exomes AF -> ``esp_maf``,
  the larger of the two -> ``dbsnp_maf``.
* SIFT/PolyPhen "label(score)" strings are split into score and prediction.
"""
import gzip
import json
import re

from django.db import transaction

from variants.models import Variant

BATCH_SIZE = 5000

# VEP sequence-ontology terms -> SnpEff effect names offered by the filter form.
CONSEQUENCE_TO_EFFECT = {
    "transcript_ablation": "EXON_DELETED",
    "splice_acceptor_variant": "SPLICE_SITE_ACCEPTOR",
    "splice_donor_variant": "SPLICE_SITE_DONOR",
    "stop_gained": "STOP_GAINED",
    "frameshift_variant": "FRAME_SHIFT",
    "stop_lost": "STOP_LOST",
    "start_lost": "START_LOST",
    "inframe_insertion": "CODON_INSERTION",
    "inframe_deletion": "CODON_DELETION",
    "missense_variant": "NON_SYNONYMOUS_CODING",
    "protein_altering_variant": "CODON_CHANGE",
    "splice_donor_5th_base_variant": "SPLICE_SITE_REGION",
    "splice_region_variant": "SPLICE_SITE_REGION",
    "splice_donor_region_variant": "SPLICE_SITE_REGION",
    "splice_polypyrimidine_tract_variant": "SPLICE_SITE_REGION",
    "incomplete_terminal_codon_variant": "CDS",
    "start_retained_variant": "SYNONYMOUS_START",
    "stop_retained_variant": "SYNONYMOUS_STOP",
    "synonymous_variant": "SYNONYMOUS_CODING",
    "coding_sequence_variant": "CDS",
    "mature_miRNA_variant": "MICRO_RNA",
    "5_prime_UTR_variant": "UTR_5_PRIME",
    "3_prime_UTR_variant": "UTR_3_PRIME",
    "non_coding_transcript_exon_variant": "EXON",
    "intron_variant": "INTRON",
    "NMD_transcript_variant": "TRANSCRIPT",
    "non_coding_transcript_variant": "TRANSCRIPT",
    "coding_transcript_variant": "TRANSCRIPT",
    "upstream_gene_variant": "UPSTREAM",
    "downstream_gene_variant": "DOWNSTREAM",
    "TFBS_ablation": "REGULATION",
    "TFBS_amplification": "REGULATION",
    "TF_binding_site_variant": "REGULATION",
    "regulatory_region_ablation": "REGULATION",
    "regulatory_region_amplification": "REGULATION",
    "regulatory_region_variant": "REGULATION",
    "intergenic_variant": "INTERGENIC",
}

FUNC_CLASS = {
    "missense_variant": "MISSENSE",
    "stop_gained": "NONSENSE",
    "synonymous_variant": "SILENT",
    "stop_retained_variant": "SILENT",
    "start_retained_variant": "SILENT",
}

_SCORE_RE = re.compile(r"^([^()]+)\(([-0-9.eE]+)\)$")


def _open(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
    return open(path, "r", encoding="utf-8", errors="ignore")


def csq_format(header_lines):
    """Return the CSQ field names declared in the VCF header, or []."""
    for line in header_lines:
        if line.startswith("##INFO=<ID=CSQ"):
            m = re.search(r"Format: ([^\">]+)", line)
            if m:
                return m.group(1).strip().split("|")
    return []


def _float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def max_float(value):
    """Largest number in a VEP multi-value field like '0.01&0.2' (None if none)."""
    if value in (None, ""):
        return None
    numbers = [_float(v) for v in re.split(r"[&,|]", str(value))]
    numbers = [n for n in numbers if n is not None]
    return max(numbers) if numbers else None


def split_score(value):
    """'deleterious(0.01)' -> ('deleterious', 0.01); '' -> (None, None)."""
    if not value:
        return None, None
    m = _SCORE_RE.match(value.split("&")[0])
    if not m:
        return value, None
    return m.group(1), _float(m.group(2))


def _rsid(variant_id, existing):
    if variant_id and variant_id.startswith("rs"):
        return variant_id.split(";")[0]
    for item in (existing or "").split("&"):
        if item.startswith("rs"):
            return item
    return "."


def _index(chrom, pos, ref, alt, genotype):
    alleles = [ref] + alt.split(",")
    calls = re.split(r"[/|]", genotype) if genotype else []
    picked = []
    if len(calls) >= 2:
        for call, fallback in ((calls[0], 0), (calls[-1], 1)):
            if call.isdigit() and int(call) < len(alleles):
                picked.append(alleles[int(call)])
            else:
                picked.append(alleles[min(fallback, len(alleles) - 1)])
    else:
        picked.append(alleles[0])
    return "%s-%s-%s" % (chrom, pos, "-".join(sorted(picked)))


def parse_line(line, csq_fields):
    """Turn one annotated VCF data line into Variant field values (dict)."""
    cols = line.rstrip("\n").split("\t")
    chrom = cols[0][3:] if cols[0].startswith("chr") else cols[0]
    pos = int(cols[1])
    variant_id, ref, alt = cols[2], cols[3], cols[4]
    qual = _float(cols[5]) if cols[5] not in (".", "-1") else None
    filt = cols[6]

    info = {}
    for element in cols[7].split(";"):
        if not element or element == ".":
            continue
        key, _, value = element.partition("=")
        info[key] = value if _ else key

    fmt = cols[8].split(":") if len(cols) > 9 else []
    sample = cols[-1].split(":") if len(cols) > 9 else []
    genotype = sample[0].replace("|", "/") if sample else "./."
    read_depth = 0
    if "DP" in fmt and fmt.index("DP") < len(sample) and sample[fmt.index("DP")].isdigit():
        read_depth = int(sample[fmt.index("DP")])

    if "HOM" in info:
        mutation_type = "HOM"
    elif "HET" in info:
        mutation_type = "HET"
    else:
        calls = [c for c in genotype.split("/") if c not in (".", "")]
        if len(calls) == 2 and calls[0] != "0" and calls[0] == calls[1]:
            mutation_type = "HOM"
        elif len(set(calls)) == 2:
            mutation_type = "HET"
        else:
            mutation_type = None

    csq = {}
    if "CSQ" in info and csq_fields:
        first = info["CSQ"].split(",")[0].split("|")
        csq = dict(zip(csq_fields, first))

    def ann(key):
        return csq.get(key) or info.get(key) or ""

    consequences = [c for c in ann("Consequence").split("&") if c]
    top = consequences[0] if consequences else ""
    sift_pred, sift = split_score(ann("SIFT"))
    pp2_pred, pp2 = split_score(ann("PolyPhen"))
    gnomad_e = max_float(ann("gnomADe_AF"))
    gnomad_g = max_float(ann("gnomADg_AF"))
    pop = [x for x in (gnomad_e, gnomad_g) if x is not None]
    symbol = ann("SYMBOL") or None

    return dict(
        index=_index(chrom, pos, ref, alt, genotype),
        pos_index="%s-%s" % (chrom, pos),
        chr=chrom,
        pos=pos,
        variant_id=_rsid(variant_id, ann("Existing_variation")),
        ref=ref,
        alt=alt,
        qual=qual if qual is not None else 0.0,
        filter=filt,
        info=json.dumps(info),
        format=":".join(fmt),
        genotype_col=":".join(sample),
        genotype=genotype,
        read_depth=read_depth,
        gene=symbol,
        mutation_type=mutation_type,
        vartype=info.get("VARTYPE"),
        genomes1k_maf=gnomad_g,
        esp_maf=gnomad_e,
        dbsnp_maf=max(pop) if pop else None,
        sift=sift,
        sift_pred=sift_pred,
        polyphen2=pp2,
        polyphen2_pred=pp2_pred,
        clinvar_clnsig=ann("clinvar_CLNSIG") or None,
        clinvar_trait=ann("clinvar_CLNDN") or None,
        snpeff_effect=CONSEQUENCE_TO_EFFECT.get(top, top.upper() or None),
        snpeff_impact=ann("IMPACT") or None,
        snpeff_func_class=FUNC_CLASS.get(top, "NONE") if top else None,
        snpeff_gene_name=symbol,
        snpeff_aa_change=ann("HGVSp") or None,
        snpeff_codon_change=ann("Codons") or None,
        snpeff_transcript_id=ann("Feature") or None,
        snpeff_biotype=ann("BIOTYPE") or None,
        snpeff_exon_rank=ann("EXON") or None,
        vep_allele=ann("Allele") or None,
        vep_gene=ann("Gene") or None,
        vep_feature=ann("Feature") or None,
        vep_feature_type=ann("Feature_type") or None,
        vep_consequence=ann("Consequence") or None,
        vep_cdna_position=ann("cDNA_position") or None,
        vep_cds_position=ann("CDS_position") or None,
        vep_protein_position=ann("Protein_position") or None,
        vep_amino_acids=ann("Amino_acids") or None,
        vep_codons=ann("Codons") or None,
        vep_existing_variation=ann("Existing_variation") or None,
        vep_distance=ann("DISTANCE") or None,
        vep_strand=ann("STRAND") or None,
        vep_symbol=symbol,
        vep_symbol_source=ann("SYMBOL_SOURCE") or None,
        vep_sift=ann("SIFT") or None,
        vep_polyphen=ann("PolyPhen") or None,
    )


def populate_variants(individual, vcf_path):
    """Replace the individual's rows in the variants table with the file's contents.

    Returns the number of variants inserted.
    """
    header, total = [], 0
    with transaction.atomic():
        Variant.objects.filter(individual=individual).delete()
        batch, fields = [], None
        with _open(vcf_path) as handle:
            for line in handle:
                if line.startswith("#"):
                    header.append(line)
                    continue
                if fields is None:
                    fields = csq_format(header)
                if not line.strip():
                    continue
                batch.append(Variant(individual=individual, **parse_line(line, fields)))
                if len(batch) >= BATCH_SIZE:
                    Variant.objects.bulk_create(batch)
                    total += len(batch)
                    batch = []
        if batch:
            Variant.objects.bulk_create(batch)
            total += len(batch)
    return total
