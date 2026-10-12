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
