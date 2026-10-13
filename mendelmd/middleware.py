"""Access control for the whole site.

Every page requires a logged-in user unless its path is listed as public below.
Infrastructure pages (servers, workers, API keys) additionally require staff status.
New views are therefore private by default; to make one public, add its prefix here.
Works on Django 4.2 and later (does not rely on Django 5.1's LoginRequiredMiddleware).
"""
from django.contrib.auth.views import redirect_to_login
import re

from django.http import Http404

PUBLIC_EXACT = {"/"}
PUBLIC_PREFIXES = (
    "/demo/",       # read-only page for a genome explicitly flagged is_public
    "/accounts/",   # allauth login, signup, password reset
    "/admin/",      # Django admin enforces its own staff login
    "/stripe/",     # dj-stripe webhooks, verified by signature
    "/static/",
    "/media/",
    "/docs/",
    "/favicon.ico",
)
STAFF_PREFIXES = ("/servers/", "/workers/", "/keys/", "/statistics/", "/databases/")
# Admin jobs (bulk database loads, app catalogue changes) anywhere in the URL space.
STAFF_PATTERNS = re.compile(r"^/(genes|diseases|pathway_analysis)/.*populate|^/apps/(import|[^/]+/move_app/)")


class SiteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        if path in PUBLIC_EXACT or path.startswith(PUBLIC_PREFIXES):
            return None
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if (path.startswith(STAFF_PREFIXES) or STAFF_PATTERNS.search(path)) and not request.user.is_staff:
            raise Http404
        return None
