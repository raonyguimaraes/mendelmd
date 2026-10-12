"""Sign-up form with lightweight bot protection (no external service needed).

* ``website`` is a honeypot: hidden off-screen, real users leave it empty.
* ``started`` is a signed timestamp set when the form is rendered; a form
  posted back within MIN_SECONDS, or with a missing/forged/expired stamp, is
  rejected. Bots usually submit instantly or replay a stale form.
"""
import time

from allauth.account.forms import SignupForm
from django import forms
from django.core import signing

MIN_SECONDS = 3
MAX_AGE = 60 * 60 * 24
_SALT = "mendelmd.signup.started"
REJECT = "Sign-up could not be completed. Please reload the page and try again."


class ProtectedSignupForm(SignupForm):
    website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )
    started = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["started"] = signing.dumps(time.time(), salt=_SALT)

    def clean(self):
        cleaned = super().clean()
        if self.data.get("website"):
            raise forms.ValidationError(REJECT)
        try:
            started = signing.loads(self.data.get("started", ""), salt=_SALT, max_age=MAX_AGE)
        except signing.BadSignature:
            raise forms.ValidationError(REJECT)
        if time.time() - float(started) < MIN_SECONDS:
            raise forms.ValidationError(REJECT)
        return cleaned
