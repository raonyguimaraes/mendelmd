"""Bot protection on the open sign-up form."""
import time

from django.contrib.auth import get_user_model
from django.core import signing
from django.core.cache import cache
from django.test import TestCase, override_settings

from mendelmd.signup_form import _SALT


def stamp(age):
    return signing.dumps(time.time() - age, salt=_SALT)


@override_settings(SIGNUP_OPEN=True)
class SignupProtectionTests(TestCase):
    def setUp(self):
        cache.clear()
        self.n = 0

    def post(self, ip="203.0.113.7", **extra):
        self.client.logout()
        self.n += 1
        data = {
            "email": "user%s@example.com" % self.n, "username": "user%s" % self.n,
            "password1": "Long-enough-pass-123", "password2": "Long-enough-pass-123",
            "website": "", "started": stamp(10),
        }
        data.update(extra)
        return self.client.post("/accounts/signup/", data, HTTP_X_REAL_IP=ip)

    def users(self):
        return get_user_model().objects.count()

    def test_form_renders_hidden_honeypot_and_stamp(self):
        html = self.client.get("/accounts/signup/").content.decode()
        self.assertIn('id="div_id_website"', html)
        self.assertIn('name="started"', html)

    def test_human_signup_succeeds(self):
        self.post()
        self.assertEqual(self.users(), 1)

    def test_honeypot_blocks(self):
        self.post(website="http://spam.example")
        self.assertEqual(self.users(), 0)

    def test_too_fast_or_forged_stamp_blocks(self):
        self.post(started=stamp(0))
        self.post(started="forged")
        self.post(started="")
        self.assertEqual(self.users(), 0)

    def test_rate_limit_per_client_ip(self):
        for _ in range(5):
            self.post(ip="198.51.100.1")
        self.assertEqual(self.users(), 5)
        blocked = self.post(ip="198.51.100.1")
        self.assertEqual(blocked.status_code, 429)
        self.assertEqual(self.users(), 5)
        self.post(ip="198.51.100.2")  # a different client is unaffected
        self.assertEqual(self.users(), 6)
