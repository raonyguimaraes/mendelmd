"""Access control for the whole site.

Every page requires a logged-in user unless its path is listed in PUBLIC_PREFIXES.
Infrastructure pages (servers, workers, API keys) additionally require staff status.
New views are therefore private by default; to make one public, add its prefix here.
"""
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.http import Http404

# Paths reachable without logging in. "/" is matched exactly, the rest by prefix.
PUBLIC_EXACT = {"/"}
PUBLIC_PREFIXES = (
    "/accounts/",   # allauth login, signup, password reset
    "/admin/",      # Django admin enforces its own staff login
    "/stripe/",     # dj-stripe webhooks, verified by signature
    "/static/",
    "/media/",
    "/docs/",
    "/favicon.ico",
)
STAFF_PREFIXES = ("/servers/", "/workers/", "/keys/")


class SiteAccessMiddleware(LoginRequiredMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        if path in PUBLIC_EXACT or path.startswith(PUBLIC_PREFIXES):
            return None
        response = super().process_view(request, view_func, view_args, view_kwargs)
        if response is not None:
            return response
        if path.startswith(STAFF_PREFIXES) and not request.user.is_staff:
            raise Http404
        return None
