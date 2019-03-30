# Generated by Django 2.0.1 on 2018-02-12 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('individuals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.TextField(db_index=True)),
                ('pos_index', models.TextField(db_index=True)),
                ('chr', models.TextField(db_index=True, verbose_name='Chr')),
                ('pos', models.IntegerField(db_index=True)),
                ('variant_id', models.TextField(db_index=True, verbose_name='ID')),
                ('ref', models.TextField(blank=True, db_index=True, null=True)),
                ('alt', models.TextField(blank=True, db_index=True, null=True)),
                ('qual', models.FloatField(db_index=True)),
                ('filter', models.TextField(db_index=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('format', models.TextField(blank=True, db_index=True, null=True)),
                ('genotype_col', models.TextField(blank=True, db_index=True, null=True)),
                ('genotype', models.TextField(db_index=True)),
                ('read_depth', models.IntegerField()),
                ('gene', models.TextField(blank=True, db_index=True, null=True)),
                ('mutation_type', models.TextField(db_index=True, null=True)),
                ('vartype', models.TextField(db_index=True, null=True)),
                ('genomes1k_maf', models.FloatField(blank=True, db_index=True, null=True, verbose_name='1000 Genomes Frequency')),
                ('dbsnp_maf', models.FloatField(blank=True, db_index=True, null=True, verbose_name='dbSNP Frequency')),
                ('esp_maf', models.FloatField(blank=True, db_index=True, null=True, verbose_name='ESP6500 Frequency')),
                ('dbsnp_build', models.IntegerField(db_index=True, null=True)),
                ('sift', models.FloatField(blank=True, db_index=True, null=True)),
                ('sift_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('polyphen2', models.FloatField(blank=True, db_index=True, null=True)),
                ('polyphen2_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('condel', models.FloatField(blank=True, db_index=True, null=True)),
                ('condel_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('dann', models.FloatField(blank=True, db_index=True, null=True)),
                ('cadd', models.FloatField(blank=True, db_index=True, null=True)),
                ('hi_index_str', models.TextField(blank=True, db_index=True, null=True)),
                ('hi_index', models.FloatField(blank=True, db_index=True, null=True)),
                ('hi_index_perc', models.FloatField(blank=True, db_index=True, null=True)),
                ('is_at_omim', models.BooleanField(db_index=True, default=False)),
                ('is_at_hgmd', models.BooleanField(db_index=True, default=False)),
                ('hgmd_entries', models.TextField(blank=True, db_index=True, null=True)),
                ('snpeff_effect', models.TextField(blank=True, db_index=True, null=True)),
                ('snpeff_impact', models.TextField(blank=True, db_index=True, null=True)),
                ('snpeff_gene_name', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_allele', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_gene', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_feature', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_feature_type', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_consequence', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_cdna_position', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_cds_position', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_protein_position', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_amino_acids', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_codons', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_existing_variation', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_distance', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_strand', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_symbol', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_symbol_source', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_sift', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_polyphen', models.TextField(blank=True, db_index=True, null=True)),
                ('vep_condel', models.TextField(blank=True, db_index=True, null=True)),
                ('ensembl_clin_HGMD', models.BooleanField(db_index=True, default=False)),
                ('clinvar_CLNSRC', models.TextField(blank=True, db_index=True, null=True)),
                ('SIFT_score', models.TextField(blank=True, db_index=True, null=True)),
                ('SIFT_converted_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('Uniprot_acc_Polyphen2', models.TextField(blank=True, db_index=True, null=True)),
                ('Uniprot_id_Polyphen2', models.TextField(blank=True, db_index=True, null=True)),
                ('Uniprot_aapos_Polyphen2', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HDIV_score', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HDIV_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HDIV_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HVAR_score', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HVAR_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('Polyphen2_HVAR_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('LRT_score', models.TextField(blank=True, db_index=True, null=True)),
                ('LRT_converted_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('LRT_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('LRT_Omega', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationTaster_score', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationTaster_converted_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationTaster_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationTaster_model', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationTaster_AAE', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationAssessor_UniprotID', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationAssessor_variant', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationAssessor_score', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationAssessor_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('MutationAssessor_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('FATHMM_score', models.TextField(blank=True, db_index=True, null=True)),
                ('FATHMM_converted_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('FATHMM_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('PROVEAN_score', models.TextField(blank=True, db_index=True, null=True)),
                ('PROVEAN_converted_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('PROVEAN_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('Transcript_id_VEST3', models.TextField(blank=True, db_index=True, null=True)),
                ('Transcript_var_VEST3', models.TextField(blank=True, db_index=True, null=True)),
                ('VEST3_score', models.TextField(blank=True, db_index=True, null=True)),
                ('VEST3_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaSVM_score', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaSVM_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaSVM_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaLR_score', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaLR_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('MetaLR_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('Reliability_index', models.TextField(blank=True, db_index=True, null=True)),
                ('CADD_raw', models.TextField(blank=True, db_index=True, null=True)),
                ('CADD_raw_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('CADD_phred', models.TextField(blank=True, db_index=True, null=True)),
                ('DANN_score', models.TextField(blank=True, db_index=True, null=True)),
                ('DANN_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('fathmm_MKL_coding_score', models.TextField(blank=True, db_index=True, null=True)),
                ('fathmm_MKL_coding_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('fathmm_MKL_coding_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('fathmm_MKL_coding_group', models.TextField(blank=True, db_index=True, null=True)),
                ('Eigen_raw', models.TextField(blank=True, db_index=True, null=True)),
                ('Eigen_phred', models.TextField(blank=True, db_index=True, null=True)),
                ('Eigen_raw_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('Eigen_PC_raw', models.TextField(blank=True, db_index=True, null=True)),
                ('Eigen_PC_raw_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('GenoCanyon_score', models.TextField(blank=True, db_index=True, null=True)),
                ('GenoCanyon_score_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('integrated_fitCons_score', models.TextField(blank=True, db_index=True, null=True)),
                ('integrated_fitCons_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('integrated_confidence_value', models.TextField(blank=True, db_index=True, null=True)),
                ('GM12878_fitCons_score', models.TextField(blank=True, db_index=True, null=True)),
                ('GM12878_fitCons_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('GM12878_confidence_value', models.TextField(blank=True, db_index=True, null=True)),
                ('H1_hESC_fitCons_score', models.TextField(blank=True, db_index=True, null=True)),
                ('H1_hESC_fitCons_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('H1_hESC_confidence_value', models.TextField(blank=True, db_index=True, null=True)),
                ('HUVEC_fitCons_score', models.TextField(blank=True, db_index=True, null=True)),
                ('HUVEC_fitCons_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('HUVEC_confidence_value', models.TextField(blank=True, db_index=True, null=True)),
                ('GERP_NR', models.TextField(blank=True, db_index=True, null=True)),
                ('GERP_RS', models.TextField(blank=True, db_index=True, null=True)),
                ('GERP_RS_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('phyloP100way_vertebrate', models.TextField(blank=True, db_index=True, null=True)),
                ('phyloP100way_vertebrate_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('phyloP20way_mammalian', models.TextField(blank=True, db_index=True, null=True)),
                ('phyloP20way_mammalian_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('phastCons100way_vertebrate', models.TextField(blank=True, db_index=True, null=True)),
                ('phastCons100way_vertebrate_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('phastCons20way_mammalian', models.TextField(blank=True, db_index=True, null=True)),
                ('phastCons20way_mammalian_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('SiPhy_29way_pi', models.TextField(blank=True, db_index=True, null=True)),
                ('SiPhy_29way_logOdds', models.TextField(blank=True, db_index=True, null=True)),
                ('SiPhy_29way_logOdds_rankscore', models.TextField(blank=True, db_index=True, null=True)),
                ('clinvar_rs', models.TextField(blank=True, db_index=True, null=True)),
                ('clinvar_clnsig', models.TextField(blank=True, db_index=True, null=True)),
                ('clinvar_trait', models.TextField(blank=True, db_index=True, null=True)),
                ('clinvar_golden_stars', models.TextField(blank=True, db_index=True, null=True)),
                ('mcap_score', models.FloatField(blank=True, db_index=True, null=True)),
                ('mcap_rankscore', models.FloatField(blank=True, db_index=True, null=True)),
                ('mcap_pred', models.TextField(blank=True, db_index=True, null=True)),
                ('revel_score', models.TextField(blank=True, db_index=True, null=True)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='individuals.Individual')),
            ],
        ),
    ]
