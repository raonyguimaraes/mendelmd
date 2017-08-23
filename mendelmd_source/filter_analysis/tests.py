"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from individuals.models import Individual

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    def test_individuals_filter(self):
        """
        Tests get individuals variants
        """
        # individuals_list = ['Exome_4_ELS.var.annotated', 'Exome_3_EDS.var.annotated'],
        # print 'hello world'
        # individuals = Individual.objects.all()
        # print individuals
        # for individual in individuals:
        #     print individual.name
        # print individual
        self.assertEqual(1 + 1, 2)
