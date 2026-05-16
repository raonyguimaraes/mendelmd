from django.test import TestCase
from individuals.tasks import treat_float_max, treat_float_min, parse_vcf


class TreatFloatMaxTest(TestCase):

    def test_returns_max_of_comma_separated_floats(self):
        self.assertEqual(treat_float_max('0.1,0.5,0.3'), 0.5)

    def test_skips_dot_values(self):
        self.assertEqual(treat_float_max('0.1,.,0.3'), 0.3)

    def test_returns_negative_default_for_all_dots(self):
        self.assertEqual(treat_float_max('.,.,.'), -100)

    def test_single_value(self):
        self.assertEqual(treat_float_max('0.42'), 0.42)


class TreatFloatMinTest(TestCase):

    def test_returns_min_of_comma_separated_floats(self):
        self.assertEqual(treat_float_min('0.5,0.1,0.3'), 0.1)

    def test_skips_dot_values(self):
        self.assertEqual(treat_float_min('0.3,.,0.1'), 0.1)

    def test_returns_1_default_for_all_dots(self):
        self.assertEqual(treat_float_min('.,.,.'), 1)

    def test_single_value(self):
        self.assertEqual(treat_float_min('0.99'), 0.99)


class ParseVcfTest(TestCase):

    def test_parses_basic_vcf_line(self):
        line = '1\t1000\trs123\tA\tG\t100.0\tPASS\t.\tGT:DP\t0/1:50\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['chr'], '1')
        self.assertEqual(variant['pos'], '1000')
        self.assertEqual(variant['variant_id'], 'rs123')
        self.assertEqual(variant['ref'], 'A')
        self.assertEqual(variant['alt'], 'G')
        self.assertEqual(variant['qual'], '100.0')
        self.assertEqual(variant['filter'], 'PASS')

    def test_strips_chr_prefix(self):
        line = 'chr1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['chr'], '1')

    def test_parses_genotype_and_read_depth(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT:DP\t0/1:30\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['genotype'], '0/1')
        self.assertEqual(variant['read_depth'], 30)

    def test_handles_hom_ref_genotype_without_dp(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/0\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['genotype'], '0/0')
        self.assertEqual(variant['read_depth'], 0)

    def test_handles_no_call_genotype(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT:DP\t./.:50\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['read_depth'], 0)

    def test_parses_qual_dot_as_zero(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['qual'], 0.0)

    def test_parses_qual_minus_one_as_zero(self):
        line = '1\t1000\t.\tA\tG\t-1\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['qual'], 0.0)

    def test_builds_correct_index(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['index'], '1-1000-A-G')

    def test_builds_correct_pos_index(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['pos_index'], '1-1000')

    def test_index_is_sorted_for_het_alleles(self):
        line = '1\t1000\t.\tA\tG,T\t.\tPASS\t.\tGT\t1/2\n'
        variant = parse_vcf(line)
        parts = variant['index'].split('-')
        self.assertEqual(parts[2:], sorted(parts[2:]))

    def test_parses_mutation_type_from_info(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\tHET;VARTYPE=SNP\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['mutation_type'], 'HET')

    def test_parses_vartype_from_info(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\tVARTYPE=SNP\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['vartype'], 'SNP')

    def test_returns_none_for_missing_mutation_type(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n'
        variant = parse_vcf(line)
        self.assertIsNone(variant['mutation_type'])

    def test_parses_hom_mutation_type(self):
        line = '1\t1000\t.\tA\tG\t.\tPASS\tHOM\tGT\t1/1\n'
        variant = parse_vcf(line)
        self.assertEqual(variant['mutation_type'], 'HOM')
