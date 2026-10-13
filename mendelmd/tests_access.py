from django.contrib.auth import get_user_model
from django.test import TestCase

from individuals.models import Individual


class SiteAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user("owner", "owner@example.com", "pw-owner-123")
        self.other = User.objects.create_user("other", "other@example.com", "pw-other-123")
        self.staff = User.objects.create_user("staff", "staff@example.com", "pw-staff-123", is_staff=True)
        self.ind = Individual.objects.create(name="sample-a", user=self.owner)
        self.orphan = Individual.objects.create(name="sample-orphan", user=None)

    def test_landing_is_public_and_shows_no_data(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Sign in")
        self.assertNotContains(r, "sample-orphan")
        self.assertNotContains(r, "Langdon")

    def test_anonymous_cannot_view_individual(self):
        r = self.client.get(f"/individuals/view/{self.orphan.id}/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_anonymous_cannot_reach_servers(self):
        for path in ["/servers/", "/servers/create/", "/servers/import_from_hetzner", "/servers/reboot"]:
            r = self.client.get(path)
            self.assertEqual(r.status_code, 302, path)

    def test_non_staff_gets_404_on_servers(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get("/servers/").status_code, 404)

    def test_staff_can_reach_servers(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get("/servers/").status_code, 200)

    def test_other_user_cannot_view_or_download_individual(self):
        self.client.force_login(self.other)
        for path in [f"/individuals/view/{self.ind.id}/", f"/individuals/download/{self.ind.id}/",
                     f"/individuals/download_annotated/{self.ind.id}/", f"/individuals/edit/{self.ind.id}/"]:
            self.assertEqual(self.client.get(path).status_code, 404, path)

    def test_owner_can_view_individual(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(f"/individuals/view/{self.ind.id}/").status_code, 200)

    def test_anonymous_can_read_a_public_demo_genome(self):
        demo = Individual.objects.create(name="GIAB demo", user=self.owner, is_public=True)
        r = self.client.get(f"/demo/{demo.id}/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Public demo genome")
        # The owner-only actions must not be offered to an anonymous reader.
        self.assertNotContains(r, f"/individuals/download/{demo.id}/")
        self.assertNotContains(r, f"/individuals/annotate/{demo.id}/")

    def test_demo_path_refuses_a_genome_not_flagged_public(self):
        for ind in (self.ind, self.orphan):
            self.assertEqual(self.client.get(f"/demo/{ind.id}/").status_code, 404, ind.name)

    def test_public_flag_does_not_open_the_private_individual_urls(self):
        demo = Individual.objects.create(name="GIAB demo", user=self.owner, is_public=True)
        # Flagging a genome public must not make the owner-only endpoints
        # reachable: anonymous still gets bounced to login.
        for path in [f"/individuals/view/{demo.id}/", f"/individuals/download/{demo.id}/",
                     f"/individuals/download_annotated/{demo.id}/", f"/individuals/edit/{demo.id}/",
                     f"/individuals/annotate/{demo.id}/"]:
            r = self.client.get(path)
            self.assertEqual(r.status_code, 302, path)
            self.assertIn("/accounts/login/", r["Location"], path)

    def test_other_user_cannot_reach_a_public_genome_through_private_urls(self):
        demo = Individual.objects.create(name="GIAB demo", user=self.owner, is_public=True)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f"/individuals/download/{demo.id}/").status_code, 404)

    def test_login_and_signup_pages_are_public(self):
        self.assertEqual(self.client.get("/accounts/login/").status_code, 200)
        self.assertEqual(self.client.get("/accounts/signup/").status_code, 200)

    def test_logged_in_dashboard_does_not_list_orphans(self):
        self.client.force_login(self.other)
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "sample-orphan")


class OrphanAndMonitorTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("u1", "u1@example.com", "pw-u1-123")
        self.orphan = Individual.objects.create(name="sample-orphan", user=None)

    def test_logged_in_user_cannot_open_orphan_sample(self):
        self.client.force_login(self.user)
        r = self.client.get(f"/individuals/view/{self.orphan.id}/")
        self.assertIn(r.status_code, (403, 404))

    def test_annotation_monitor_requires_login_and_ownership(self):
        r = self.client.get(f"/individuals/annotation/{self.orphan.id}/")
        self.assertEqual(r.status_code, 302)
        self.client.force_login(self.user)
        r = self.client.get(f"/individuals/annotation/{self.orphan.id}/")
        self.assertIn(r.status_code, (403, 404))

    def test_dashboard_does_not_list_orphans(self):
        self.client.force_login(self.user)
        self.assertNotContains(self.client.get("/dashboard/"), "sample-orphan")


class SignupClosedTests(TestCase):
    def test_signup_is_closed_by_default(self):
        from django.contrib.auth import get_user_model
        before = get_user_model().objects.count()
        r = self.client.post("/accounts/signup/", {"email": "x@example.com", "username": "spam1",
                                                   "password1": "Very-strong-pw-123", "password2": "Very-strong-pw-123"})
        self.assertEqual(get_user_model().objects.count(), before)
        self.assertNotContains(self.client.get("/"), "Create an account")


class BulkActionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user("bo", "bo@example.com", "pw-bo-123")
        self.other = User.objects.create_user("bx", "bx@example.com", "pw-bx-123")
        self.ind = Individual.objects.create(name="keep-me", user=self.owner)

    def test_other_user_cannot_bulk_delete(self):
        self.client.force_login(self.other)
        self.client.post("/dashboard/bulk_action/", {"individuals": [self.ind.id], "selectionField": "Delete"})
        self.assertTrue(Individual.objects.filter(pk=self.ind.id).exists())


class OwnershipAcrossAppsTests(TestCase):
    """Another signed-in user must not see or act on the owner's data."""

    def setUp(self):
        from analyses.models import Analysis
        from files.models import File
        from genes.models import GeneList
        from individuals.models import Group
        from samples.models import Sample
        from variants.models import Variant

        User = get_user_model()
        self.owner = User.objects.create_user("own", "own@example.com", "pw-own-123")
        self.other = User.objects.create_user("oth", "oth@example.com", "pw-oth-123")
        self.ind = Individual.objects.create(name="private-ind", user=self.owner)
        required = {
            f.name: 0
            for f in Variant._meta.concrete_fields
            if not f.null and not f.has_default() and not f.primary_key
            and f.get_internal_type() not in ("CharField", "TextField", "ForeignKey")
        }
        required.update(individual=self.ind, chr="1", pos=12345)
        self.variant = Variant.objects.create(**required)
        self.sample = Sample.objects.create(name="private-sample", user=self.owner)
        self.file = File.objects.create(name="private.vcf", user=self.owner)
        self.analysis = Analysis.objects.create(name="private-analysis", user=self.owner)
        self.genelist = GeneList.objects.create(name="private-genes", user=self.owner)
        self.group = Group.objects.create(name="private-group")
        self.group.members.add(self.ind)

    def _as(self, user):
        self.client.force_login(user)

    def test_other_user_gets_404_on_owned_objects(self):
        self._as(self.other)
        urls = [
            f"/variants/view/{self.variant.id}/",
            f"/samples/{self.sample.id}/",
            f"/files/view/{self.file.id}/",
            f"/analyses/detail/{self.analysis.id}/",
            f"/genes/geneset/view/{self.genelist.id}",
            f"/individuals/view_group/{self.group.id}/",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_owned_variants_scoping(self):
        from mendelmd.access import owned_variants
        from django.test import RequestFactory

        req = RequestFactory().get("/")
        req.user = self.other
        self.assertFalse(owned_variants(req).exists())
        req.user = self.owner
        self.assertEqual(list(owned_variants(req)), [self.variant])

    def test_filter_form_only_offers_own_choices(self):
        from filter_analysis.forms import FilterAnalysisForm

        form = FilterAnalysisForm(self.other)
        self.assertFalse(form.fields["individuals"].queryset.filter(pk=self.ind.pk).exists())
        self.assertFalse(form.fields["genelists"].queryset.filter(pk=self.genelist.pk).exists())
        form = FilterAnalysisForm(self.owner)
        self.assertTrue(form.fields["individuals"].queryset.filter(pk=self.ind.pk).exists())

    def test_comparison_form_and_group_form_are_scoped(self):
        from individuals.forms import ComparisonForm, GroupForm

        self.assertFalse(ComparisonForm(self.other).fields["individual_one"].queryset.exists())
        self.assertFalse(GroupForm(user=self.other).fields["members"].queryset.exists())

    def test_non_staff_cannot_reach_populate_or_import(self):
        self._as(self.other)
        for url in ["/genes/populate/", "/diseases/populate/", "/apps/import"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)
