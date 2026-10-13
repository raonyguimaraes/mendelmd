"""Pynnotator 3 output loads into the variants table and the filters find it."""
import os
import shutil
import tempfile
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from individuals.models import Individual
from individuals.populate import parse_line, populate_variants, split_score, max_float
from variants.models import Variant

CSQ = ("Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|"
       "cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|"
       "FLAGS|SYMBOL_SOURCE|HGNC_ID|CANONICAL|SOURCE|SIFT|PolyPhen|gnomADe_AF|gnomADg_AF|"
       "clinvar|clinvar_CLNSIG|clinvar_CLNREVSTAT|clinvar_CLNDN")

HEADER = (
    "##fileformat=VCFv4.2\n"
    "##INFO=<ID=CSQ,Number=.,Type=String,Description=\"Consequence annotations from Ensembl VEP. Format: %s\">\n"
    "##INFO=<ID=VARTYPE,Number=1,Type=String,Description=\"Variant type\">\n"
    "##INFO=<ID=HET,Number=0,Type=Flag,Description=\"Heterozygous\">\n"
    "##INFO=<ID=HOM,Number=0,Type=Flag,Description=\"Homozygous\">\n"
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n" % CSQ
)


def csq(*values):
    fields = dict.fromkeys(CSQ.split("|"), "")
    fields.update(values[0])
    return "|".join(fields[k] for k in CSQ.split("|"))


# Missense, HIGH impact stop-gain, and a common synonymous variant.
LINES = [
    "chr1\t1000\t.\tA\tG\t50\tPASS\tCSQ=%s;VARTYPE=SNP;HET\tGT:DP\t0/1:31\n" % csq({
        "Allele": "G", "Consequence": "missense_variant&splice_region_variant", "IMPACT": "MODERATE",
        "SYMBOL": "GENEA", "Feature": "ENST1", "SIFT": "deleterious(0.01)",
        "PolyPhen": "probably_damaging(0.998)", "gnomADe_AF": "0.0001", "gnomADg_AF": "",
        "Existing_variation": "rs123&COSV9"}),
    "chr2\t2000\trs555\tC\tT\t60\tPASS\tCSQ=%s;VARTYPE=SNP;HOM\tGT:DP\t1|1:12\n" % csq({
        "Allele": "T", "Consequence": "stop_gained", "IMPACT": "HIGH", "SYMBOL": "GENEB",
        "clinvar_CLNSIG": "Pathogenic"}),
    "chr3\t3000\t.\tG\tA\t.\tLowQual\tCSQ=%s;VARTYPE=SNP;HET\tGT:DP\t0/1:8\n" % csq({
        "Allele": "A", "Consequence": "synonymous_variant", "IMPACT": "LOW", "SYMBOL": "GENEC",
        "gnomADe_AF": "0.3&0.1", "gnomADg_AF": "0.25"}),
]


class ParseLineTests(TestCase):
    def setUp(self):
        self.fields = CSQ.split("|")

    def test_missense_maps_to_legacy_columns(self):
        v = parse_line(LINES[0], self.fields)
        self.assertEqual((v["chr"], v["pos"], v["gene"]), ("1", 1000, "GENEA"))
        self.assertEqual(v["snpeff_effect"], "NON_SYNONYMOUS_CODING")
        self.assertEqual(v["snpeff_func_class"], "MISSENSE")
        self.assertEqual(v["snpeff_impact"], "MODERATE")
        self.assertEqual((v["sift"], v["sift_pred"]), (0.01, "deleterious"))
        self.assertEqual(v["polyphen2"], 0.998)
        self.assertEqual(v["esp_maf"], 0.0001)
        self.assertIsNone(v["genomes1k_maf"])
        self.assertEqual(v["dbsnp_maf"], 0.0001)
        self.assertEqual(v["variant_id"], "rs123")
        self.assertEqual((v["genotype"], v["mutation_type"], v["read_depth"]), ("0/1", "HET", 31))
        self.assertEqual(v["index"], "1-1000-A-G")
        self.assertEqual(v["pos_index"], "1-1000")

    def test_phased_hom_and_clinvar(self):
        v = parse_line(LINES[1], self.fields)
        self.assertEqual(v["genotype"], "1/1")
        self.assertEqual(v["mutation_type"], "HOM")
        self.assertEqual(v["snpeff_effect"], "STOP_GAINED")
        self.assertEqual(v["snpeff_func_class"], "NONSENSE")
        self.assertEqual(v["clinvar_clnsig"], "Pathogenic")
        self.assertEqual(v["variant_id"], "rs555")
        self.assertEqual(v["index"], "2-2000-T-T")

    def test_missing_qual_and_multi_value_frequency(self):
        v = parse_line(LINES[2], self.fields)
        self.assertIsNone(v["qual"])
        self.assertEqual(v["esp_maf"], 0.3)
        self.assertEqual(v["dbsnp_maf"], 0.3)

    def test_genotype_beats_info_flags(self):
        line = LINES[0].replace("\t0/1:31", "\t1/1:31")  # INFO still says HET
        self.assertEqual(parse_line(line, self.fields)["mutation_type"], "HOM")
        line = LINES[0].replace("\t0/1:31", "\t0/0:31")
        self.assertIsNone(parse_line(line, self.fields)["mutation_type"])
        line = LINES[0].replace("\t0/1:31", "\t./.:31")
        self.assertEqual(parse_line(line, self.fields)["mutation_type"], "HET")

    def test_hom_ref_and_no_call_rows_are_skipped(self):
        from individuals.populate import carries_alt_allele
        self.assertTrue(carries_alt_allele(LINES[0]))
        self.assertFalse(carries_alt_allele(LINES[0].replace("\t0/1:31", "\t0/0:31")))
        self.assertFalse(carries_alt_allele(LINES[0].replace("\t0/1:31", "\t./.:31")))
        self.assertTrue(carries_alt_allele(LINES[0].replace("\t0/1:31", "\t./1:31")))
        self.assertTrue(carries_alt_allele("1\t5\t.\tA\tG\t.\tPASS\t.\n"))  # sites-only

    def test_array_genotype_has_no_depth(self):
        v = parse_line("1\t5\trs1\tA\tG\t.\tPASS\t.\tGT\t1/1\n", self.fields)
        self.assertIsNone(v["read_depth"])
        self.assertIsNone(v["qual"])
        self.assertEqual(v["mutation_type"], "HOM")

    def test_helpers(self):
        self.assertEqual(split_score(""), (None, None))
        self.assertEqual(split_score("benign(0.1)"), ("benign", 0.1))
        self.assertIsNone(max_float("&"))


class PopulateAndFilterTests(TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        User = get_user_model()
        self.owner = User.objects.create_user("fo", "fo@example.com", "pw-fo-123")
        self.other = User.objects.create_user("fx", "fx@example.com", "pw-fx-123")
        self.ind = Individual.objects.create(name="trio-child", user=self.owner, status="annotated")
        folder = os.path.join(self.base, "genomes", "fo", str(self.ind.id), "ann_sample")
        os.makedirs(folder)
        with open(os.path.join(folder, "annotation.final.vcf"), "w") as fh:
            fh.write(HEADER + "".join(LINES))

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _populate(self):
        from individuals.tasks import PopulateVariants
        with override_settings(BASE_DIR=self.base):
            return PopulateVariants(self.ind.id)

    def test_task_loads_rows_and_marks_populated(self):
        self.assertEqual(self._populate(), 3)
        self.ind.refresh_from_db()
        self.assertEqual(self.ind.status, "populated")
        self.assertEqual(self.ind.n_lines, 3)
        # Re-running replaces rather than duplicates.
        self._populate()
        self.assertEqual(Variant.objects.filter(individual=self.ind).count(), 3)

    def test_missing_file_is_skipped(self):
        other = Individual.objects.create(name="no-file", user=self.owner, status="annotated")
        from individuals.tasks import PopulateVariants
        with override_settings(BASE_DIR=self.base):
            self.assertEqual(PopulateVariants(other.id), 0)

    def test_failed_insert_does_not_stay_annotated(self):
        # A sample whose variants never loaded must not keep reading as finished.
        # PopulateVariants imports populate_variants inside the function body,
        # so the patch has to land on the module it is imported from.
        from individuals.tasks import PopulateVariants
        with override_settings(BASE_DIR=self.base):
            with mock.patch('individuals.populate.populate_variants',
                            side_effect=RuntimeError('index row size')):
                with self.assertRaises(RuntimeError):
                    PopulateVariants(self.ind.id)
        self.ind.refresh_from_db()
        self.assertEqual(self.ind.status, "failed")

    def _filter(self, **params):
        self.client.force_login(self.owner)
        params.setdefault("individuals", str(self.ind.id))
        response = self.client.get("/filter_analysis/", params)
        self.assertEqual(response.status_code, 200)
        return sorted(v.gene for v in response.context["variants"])

    def test_filter_page_finds_loaded_variants(self):
        self._populate()
        self.assertEqual(self._filter(), ["GENEA", "GENEB", "GENEC"])
        self.assertEqual(self._filter(impact="HIGH"), ["GENEB"])
        self.assertEqual(self._filter(effect="NON_SYNONYMOUS_CODING"), ["GENEA"])
        self.assertEqual(self._filter(genomes1000="0.01"), ["GENEA", "GENEB"])
        self.assertEqual(self._filter(esp_frequency="0.01"), ["GENEA", "GENEB"])
        self.assertEqual(self._filter(mutation_type="homozygous"), ["GENEB"])
        self.assertEqual(self._filter(filter="PASS"), ["GENEA", "GENEB"])

    def test_other_user_sees_nothing(self):
        self._populate()
        self.client.force_login(self.other)
        response = self.client.get("/filter_analysis/", {"individuals": str(self.ind.id)})
        self.assertEqual(len(list(response.context["variants"] or [])), 0)

    def test_family_analysis_and_gene_pages_render(self):
        from genes.models import Gene
        Gene.objects.create(symbol="GENEB")
        self._populate()
        intergenic = Variant.objects.filter(individual=self.ind).first()
        intergenic.pk, intergenic.gene, intergenic.pos = None, None, 99999
        intergenic.save()  # no gene symbol must not break the gene summaries
        self.client.force_login(self.owner)
        response = self.client.get("/filter_analysis/family_analysis/", {"individuals": str(self.ind.id)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/genes/GENEB/").status_code, 200)
        self.assertEqual(self.client.get("/genes/NOSUCHGENE/").status_code, 404)
        self.assertEqual(self.client.get("/genes/geneset/add/").status_code, 200)

    def test_family_analysis_with_parent_and_export(self):
        self._populate()
        father = Individual.objects.create(name="father", user=self.owner)
        Variant.objects.create(**{**{f.name: getattr(Variant.objects.filter(individual=self.ind, gene="GENEA").first(), f.name)
                                  for f in Variant._meta.concrete_fields if not f.primary_key},
                                  "individual": father, "genotype": "0/1"})
        self.client.force_login(self.owner)
        params = {"individuals": str(self.ind.id), "children": str(self.ind.id), "father": str(father.id)}
        page = self.client.get("/filter_analysis/family_analysis/", params)
        self.assertEqual(page.status_code, 200)
        rows = {v.gene: v.father for v in page.context["variants"]}
        self.assertEqual(rows.get("GENEA"), "HET")
        export = self.client.get("/filter_analysis/family_analysis/", dict(params, export="csv"))
        self.assertEqual(export.status_code, 200)
        body = b"".join(export.streaming_content).decode()
        self.assertIn("GENEA", body)
        self.assertIn("HET", body)  # father's genotype column is filled per row

    def test_filter_page_streams_exports(self):
        self._populate()
        self.client.force_login(self.owner)
        for fmt, sep in (("csv", ","), ("txt", "\t")):
            r = self.client.get("/filter_analysis/", {"individuals": str(self.ind.id), "export": fmt})
            lines = b"".join(r.streaming_content).decode().strip().splitlines()
            self.assertEqual(len(lines), 4)  # header + 3 variants
            self.assertTrue(lines[0].startswith("Individual" + sep))

    def test_depth_and_qual_filters_keep_array_samples(self):
        """Genotype-only samples (no DP/QUAL) are not wiped out by depth filters."""
        array = Individual.objects.create(name="array-sample", user=self.owner, status="annotated")
        folder = os.path.join(self.base, "genomes", "fo", str(array.id), "ann_sample")
        os.makedirs(folder)
        gt_only = [l.split("\t") for l in LINES[:2]]
        rows = ["\t".join(c[:5] + [".", "PASS", c[7], "GT", c[9].split(":")[0] + "\n"]) for c in gt_only]
        with open(os.path.join(folder, "annotation.final.vcf"), "w") as fh:
            fh.write(HEADER + "".join(rows))
        from individuals.tasks import PopulateVariants
        with override_settings(BASE_DIR=self.base):
            self.assertEqual(PopulateVariants(array.id), 2)
        self._populate()
        both = "%s" % array.id
        self.assertEqual(self._filter(individuals=both, read_depth_option=">", read_depth="10"), ["GENEA", "GENEB"])
        self.assertEqual(self._filter(individuals=both, read_depth_option=">", read_depth="10",
                                      impact=["HIGH", "MODERATE"], mutation_type="homozygous",
                                      genes_in_common="on", genomes1000="0 - 0.01",
                                      dbsnp_frequency="0 - 0.01", esp_frequency="0 - 0.01",
                                      dbsnp_option=">", dbsnp_build="130"), ["GENEB"])
        self.assertEqual(self._filter(individuals=both, qual_option=">", qual="30"), ["GENEA", "GENEB"])
        page = self.client.get("/filter_analysis/", {"individuals": both, "read_depth_option": ">", "read_depth": "10"})
        self.assertContains(page, "No read depth or QUAL in array-sample")
        # Sequenced samples are still filtered by depth, and get no note.
        self.assertEqual(self._filter(read_depth_option=">", read_depth="20"), ["GENEA"])
        page = self.client.get("/filter_analysis/", {"individuals": str(self.ind.id), "read_depth_option": ">", "read_depth": "20"})
        self.assertNotContains(page, "No read depth or QUAL")
