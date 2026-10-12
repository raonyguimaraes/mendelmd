from django.test import TestCase
from variants.models import Variant


class VariantModelTest(TestCase):

    def test_get_fields_returns_list_of_tuples(self):
        fields = Variant.get_fields(Variant)
        self.assertIsInstance(fields, list)
        self.assertTrue(all(isinstance(f, tuple) for f in fields))
        self.assertTrue(all(len(f) == 2 for f in fields))

    def test_get_fields_contains_expected_fields(self):
        fields = dict(Variant.get_fields(Variant))
        self.assertIn('chr', fields)
        self.assertIn('pos', fields)
        self.assertIn('gene', fields)
        self.assertIn('qual', fields)

    def test_get_fields_returns_titlecase_verbose_names(self):
        fields = dict(Variant.get_fields(Variant))
        self.assertEqual(fields['genomes1k_maf'], '1000 Genomes Frequency')

