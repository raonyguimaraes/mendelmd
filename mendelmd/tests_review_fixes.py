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

    def test_upload_creates_sample_and_queues_checks(self):
        import shutil, tempfile
        from unittest import mock
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        media = tempfile.mkdtemp()
        try:
            self.client.force_login(self.alice)
            upload = SimpleUploadedFile("My Exome.vcf", b"##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            with override_settings(MEDIA_ROOT=media), mock.patch("individuals.views.VerifyVCF.delay") as verify:
                r = self.client.post("/individuals/create/", {"file": upload, "vcf_file": "/etc/passwd"}, HTTP_ACCEPT="application/json")
            self.assertEqual(r.status_code, 200)
            ind = Individual.objects.filter(user=self.alice).exclude(pk=self.ind.pk).get()
            self.assertTrue(ind.vcf_file.name.startswith("genomes/ra/%s/" % ind.id))
            verify.assert_called_once_with(ind.id)
        finally:
            shutil.rmtree(media, ignore_errors=True)

    def test_tar_upload_cannot_write_outside_sample_folder(self):
        import io, os, tarfile, tempfile, shutil
        from individuals.tasks import _copy_first_vcf_from_tar
        work = tempfile.mkdtemp()
        try:
            sample_dir = os.path.join(work, "genomes", "ra", "1")
            os.makedirs(sample_dir)
            archive = os.path.join(sample_dir, "x.tar.gz")
            with tarfile.open(archive, "w:gz") as tar:
                def add(name, data, **kw):
                    info = tarfile.TarInfo(name); info.size = len(data)
                    for k, v in kw.items(): setattr(info, k, v)
                    tar.addfile(info, io.BytesIO(data))
                add("../../../escape.vcf", b"evil")
                add("/tmp/abs-escape-mendelmd.vcf", b"evil")
                link = tarfile.TarInfo("link.vcf"); link.type = tarfile.SYMTYPE; link.linkname = "/etc/passwd"
                tar.addfile(link)
                add("real.vcf", b"##fileformat=VCFv4.2\n")
            target = os.path.join(sample_dir, "sample.vcf")
            self.assertTrue(_copy_first_vcf_from_tar(archive, target))
            self.assertFalse(os.path.exists(os.path.join(work, "escape.vcf")))
            self.assertFalse(os.path.exists("/tmp/abs-escape-mendelmd.vcf"))
            self.assertFalse(os.path.islink(target))
            # The first regular member wins; its bytes land only in sample.vcf.
            with open(target, "rb") as fh:
                self.assertEqual(fh.read(), b"evil")
            self.assertEqual(sorted(os.listdir(sample_dir)), ["sample.vcf", "x.tar.gz"])
        finally:
            shutil.rmtree(work, ignore_errors=True)

    def test_normalize_vcf_header_fixes_integer_gt(self):
        import os, tempfile
        from individuals.tasks import normalize_vcf_header
        fd, path = tempfile.mkstemp(suffix=".vcf"); os.close(fd)
        body = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n1\t5\trs1\tA\tG\t.\t.\t.\tGT\t0/1\n"
        try:
            with open(path, "w") as fh:
                fh.write('##fileformat=VCFv4.0\n##FORMAT=<ID=GT,Number=.,Type=Integer,Description="Genotype">\n' + body)
            self.assertTrue(normalize_vcf_header(path))
            with open(path) as fh:
                text = fh.read()
            self.assertIn('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n', text)
            self.assertTrue(text.endswith(body))
            self.assertFalse(normalize_vcf_header(path))  # already standard: untouched
        finally:
            os.remove(path)

    def test_annotation_failure_marks_sample_failed(self):
        import os, shutil, tempfile
        from unittest import mock
        from django.test import override_settings
        from individuals.tasks import AnnotateVariants
        base = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            folder = os.path.join(base, "genomes", "ra", str(self.ind.id))
            os.makedirs(folder)
            with open(os.path.join(folder, "a.vcf"), "w") as fh:
                fh.write("##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            self.ind.vcf_file.name = "genomes/ra/%s/a.vcf" % self.ind.id
            self.ind.save()
            boom = mock.Mock(side_effect=RuntimeError("htslib parse error"))
            with override_settings(BASE_DIR=base), \
                    mock.patch("pynnotator.annotator.Annotator", return_value=mock.Mock(run=boom)), \
                    mock.patch("individuals.tasks.PopulateVariants.delay") as populate:
                AnnotateVariants(self.ind.id)
            self.ind.refresh_from_db()
            self.assertEqual(self.ind.status, "failed")
            populate.assert_not_called()
            self.assertEqual(os.path.realpath(os.getcwd()), os.path.realpath(base))
        finally:
            os.chdir(cwd)
            shutil.rmtree(base, ignore_errors=True)
