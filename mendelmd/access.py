"""Shared per-user access rules.

Staff can see everything. Everyone else only sees records they own.
Records with no owner are staff-only.
"""
from django.http import Http404
from django.shortcuts import get_object_or_404


def owned_queryset(request, queryset, owner_field="user"):
    """Restrict a queryset to records the requesting user may see."""
    if request.user.is_staff:
        return queryset
    if not request.user.is_authenticated:
        return queryset.none()
    return queryset.filter(**{owner_field: request.user})


def owned_or_404(request, model_or_queryset, owner_field="user", **lookup):
    """get_object_or_404 that also 404s when the requesting user does not own the record."""
    queryset = model_or_queryset._default_manager.all() if hasattr(model_or_queryset, "_default_manager") else model_or_queryset
    return get_object_or_404(owned_queryset(request, queryset, owner_field), **lookup)


class OwnedQuerysetMixin:
    """For DetailView/UpdateView/DeleteView: only the owner's records are reachable."""
    owner_field = "user"

    def get_queryset(self):
        return owned_queryset(self.request, super().get_queryset(), self.owner_field)


def require_staff(request):
    if not request.user.is_staff:
        raise Http404
