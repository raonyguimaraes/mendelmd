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


@override_settings(SIGNUP_OPEN=True, ACCOUNT_EMAIL_VERIFICATION="mandatory")
class EmailFlowTests(TestCase):
    """What happens once real email is configured (tests capture mail in memory)."""

    def setUp(self):
        cache.clear()

    def test_signup_sends_confirmation_and_blocks_login_until_confirmed(self):
        from django.core import mail
        self.client.post("/accounts/signup/", {
            "email": "new@example.com", "username": "newbie",
            "password1": "Long-enough-pass-123", "password2": "Long-enough-pass-123",
            "website": "", "started": stamp(10)}, HTTP_X_REAL_IP="192.0.2.5")
        self.assertEqual(get_user_model().objects.filter(username="newbie").count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("new@example.com", mail.outbox[0].to)
        self.client.logout()
        r = self.client.post("/accounts/login/", {"login": "newbie", "password": "Long-enough-pass-123"})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_password_reset_sends_email(self):
        from django.core import mail
        get_user_model().objects.create_user("resetme", "reset@example.com", "Old-pass-12345")
        self.client.post("/accounts/password/reset/", {"email": "reset@example.com"}, HTTP_X_REAL_IP="192.0.2.6")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset@example.com", mail.outbox[0].to)


class EmailSettingsTests(TestCase):
    def _settings(self, **env):
        import json, os, subprocess, sys
        code = ("import json, django; from django.conf import settings; django.setup(); "
                "print(json.dumps([settings.EMAIL_BACKEND, settings.ACCOUNT_EMAIL_VERIFICATION]))")
        full_env = {k: v for k, v in os.environ.items() if not k.startswith("EMAIL_")}
        full_env.update(env, DJANGO_SETTINGS_MODULE="mendelmd.settings")
        out = subprocess.run([sys.executable, "-c", code], env=full_env, capture_output=True, text=True, check=True)
        return json.loads(out.stdout.strip().splitlines()[-1])

    def test_console_without_host_and_smtp_with_host(self):
        self.assertEqual(self._settings(), ["django.core.mail.backends.console.EmailBackend", "optional"])
        self.assertEqual(self._settings(EMAIL_HOST="smtp.example.com"),
                         ["django.core.mail.backends.smtp.EmailBackend", "mandatory"])
