from django.test import TestCase
from django.http import HttpRequest
from filter_analysis.filter_options import filter_individuals_variants


class FilterIndividualsVariantsTest(TestCase):

    def test_no_individuals_selected_returns_empty_lists(self):
        request = HttpRequest()
        request.GET = request.GET.copy()
        request.GET.setlist('individuals', [])
        request.GET.setlist('groups', [])
        request.GET.setlist('exclude_individuals', [])
        request.GET.setlist('exclude_groups', [])
        query = {}
        args = []
        exclude = {}
        filter_individuals_variants(request, query, args, exclude)
        self.assertNotIn('individual__id__in', query)
        self.assertNotIn('index__in', exclude)
