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


def owned_individuals(user):
    from individuals.models import Individual
    qs = Individual.objects.all().order_by("id")
    if getattr(user, "is_staff", False):
        return qs
    if not getattr(user, "is_authenticated", False):
        return qs.none()
    return qs.filter(user=user)


def owned_groups(user):
    """Sample groups whose members all belong to the user (staff: all groups)."""
    from individuals.models import Group, Individual
    qs = Group.objects.all().order_by("id")
    if getattr(user, "is_staff", False):
        return qs
    if not getattr(user, "is_authenticated", False):
        return qs.none()
    # Groups have no owner column; a group belongs to you when it has members
    # and all of them are yours. Empty groups are reachable by staff only.
    return qs.filter(members__isnull=False).exclude(members__in=Individual.objects.exclude(user=user)).distinct()


def restrict_analysis_form(form, user):
    """Limit every sample, group and gene-list choice on an analysis form to what the user owns."""
    individuals = owned_individuals(user)
    groups = owned_groups(user)
    for name in ("individuals", "exclude_individuals", "mother", "father", "children", "parents"):
        if name in form.fields and hasattr(form.fields[name], "queryset"):
            form.fields[name].queryset = individuals
            widget = form.fields[name].widget
            if hasattr(widget, "queryset"):
                widget.queryset = individuals
    for name in ("groups", "exclude_groups"):
        if name in form.fields:
            form.fields[name].queryset = groups
    for name in ("genelists", "exclude_genelists"):
        if name in form.fields:
            from genes.models import GeneList
            gl = GeneList.objects.all().order_by("name")
            if not getattr(user, "is_staff", False):
                gl = gl.filter(user=user) if getattr(user, "is_authenticated", False) else gl.none()
            form.fields[name].queryset = gl


def owned_variants(request):
    from variants.models import Variant
    return owned_queryset(request, Variant.objects.all(), "individual__user")


def owned_sample_groups(user):
    """Sample groups whose members all belong to the user (staff: all)."""
    from samples.models import Sample, SampleGroup
    qs = SampleGroup.objects.all()
    if getattr(user, "is_staff", False):
        return qs
    if not getattr(user, "is_authenticated", False):
        return qs.none()
    return qs.filter(members__isnull=False).exclude(members__in=Sample.objects.exclude(user=user)).distinct()


class OwnedSampleGroupMixin:
    def get_queryset(self):
        return owned_sample_groups(self.request.user)
