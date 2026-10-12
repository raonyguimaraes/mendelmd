"""Regression tests for issues found in the independent review (2026-10-12)."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from individuals.models import Group, Individual


class ReviewFixTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user("ra", "ra@example.com", "pw-ra-123")
        self.bob = User.objects.create_user("rb", "rb@example.com", "pw-rb-123")
        self.ind = Individual.objects.create(name="a-sample", user=self.alice,
                                             vcf_file="genomes/ra/1/a.vcf.gz")

    def test_edit_form_cannot_change_vcf_path(self):
        self.client.force_login(self.alice)
        self.client.post("/individuals/edit/%s/" % self.ind.id,
                         {"name": "renamed", "vcf_file": "/etc/passwd;id"})
        self.ind.refresh_from_db()
        self.assertEqual(self.ind.name, "renamed")
        self.assertEqual(self.ind.vcf_file.name, "genomes/ra/1/a.vcf.gz")

    def test_project_bulk_action_cannot_delete_other_users_file(self):
        from files.models import File
        from projects.models import Project
        victim_file = File.objects.create(name="b.vcf", user=self.bob)
        project = Project.objects.create(name="mine", user=self.alice)
        self.client.force_login(self.alice)
        r = self.client.post("/projects/project_bulk_action/%s/" % project.id,
                             {"model": "files", "action": "delete", "files": [victim_file.id]})
        self.assertEqual(r.status_code, 404)
        self.assertTrue(File.objects.filter(pk=victim_file.pk).exists())

    def test_run_analysis_requires_owner(self):
        from analyses.models import Analysis
        analysis = Analysis.objects.create(name="b-analysis", user=self.bob)
        self.client.force_login(self.alice)
        self.assertEqual(self.client.get("/analyses/run/%s/" % analysis.id).status_code, 404)

    def test_empty_group_not_reachable_by_other_users(self):
        empty = Group.objects.create(name="empty")
        self.client.force_login(self.alice)
        self.assertEqual(self.client.post("/individuals/delete_group/%s" % empty.id).status_code, 404)
        self.assertTrue(Group.objects.filter(pk=empty.pk).exists())

    def test_gene_list_filter_rejects_other_users_list(self):
        from genes.models import GeneList
        private = GeneList.objects.create(name="secret-genes", user=self.bob, genes="BRCA1")
        self.client.force_login(self.alice)
        r = self.client.get("/filter_analysis/", {"individuals": self.ind.id, "genelists": private.id})
        self.assertEqual(r.status_code, 404)

    def test_safe_stem_strips_paths_and_shell_characters(self):
        from individuals.tasks import _safe_stem
        self.assertEqual(_safe_stem("../../etc/x;rm -rf"), "_.._etc_x_rm_-rf")
        self.assertEqual(_safe_stem("NA12878"), "NA12878")
