from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.conf import settings as django_settings

import stripe
import djstripe.models

from .models import S3Credential, Provider, Profile
from .forms import S3CredentialForm

stripe.api_key = django_settings.STRIPE_TEST_SECRET_KEY


@login_required
def index(request):
    if request.user.is_staff:
        s3_settings = S3Credential.objects.all()
    else:
        s3_settings = S3Credential.objects.filter(user=request.user)
    context = {'s3_settings': s3_settings}
    return render(request, 'settings/index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)


@login_required
def mysubscription(request):
    current_price_ids = set()
    customer = djstripe.models.Customer.objects.filter(subscriber=request.user).first()
    if customer:
        for sub in customer.subscriptions.filter(status__in=['active', 'trialing']):
            for item in sub.items.all():
                current_price_ids.add(item.price.id)

    products_with_prices = []
    for product in djstripe.models.Product.objects.filter(active=True).order_by('name'):
        prices = list(product.prices.filter(active=True).order_by('unit_amount'))
        if prices:
            products_with_prices.append({'product': product, 'prices': prices})

    context = {
        'products_with_prices': products_with_prices,
        'current_price_ids': current_price_ids,
    }
    return render(request, 'account/my_subscription.html', context)


@login_required
@require_POST
def create_checkout_session(request):
    price_id = request.POST.get('price_id')
    if not price_id:
        return redirect('settings-mysubscription')

    success_url = (
        request.build_absolute_uri(reverse('subscription-success'))
        + '?session_id={CHECKOUT_SESSION_ID}'
    )
    cancel_url = request.build_absolute_uri(reverse('subscription-cancel'))

    session_kwargs = dict(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{'price': price_id, 'quantity': 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )

    customer = djstripe.models.Customer.objects.filter(subscriber=request.user).first()
    if customer:
        session_kwargs['customer'] = customer.id
    else:
        session_kwargs['customer_email'] = request.user.email

    session = stripe.checkout.Session.create(**session_kwargs)
    return redirect(session.url, code=303)


@login_required
def subscription_success(request):
    return render(request, 'account/subscription_success.html', {})


@login_required
def subscription_cancel(request):
    return render(request, 'account/subscription_cancel.html', {})


@login_required
def billing(request):
    subscription = None
    customer = djstripe.models.Customer.objects.filter(subscriber=request.user).first()
    if customer:
        subscription = customer.subscriptions.filter(
            status__in=['active', 'trialing']
        ).first()

    context = {'subscription': subscription}
    return render(request, 'account/billing.html', context)


@login_required
@require_POST
def create_portal_session(request):
    customer = djstripe.models.Customer.objects.filter(subscriber=request.user).first()
    if not customer:
        return redirect('settings-mysubscription')

    portal_session = stripe.billing_portal.Session.create(
        customer=customer.id,
        return_url=request.build_absolute_uri(reverse('settings-billing')),
    )
    return redirect(portal_session.url, code=303)


@login_required
def create_s3_credential(request):
    form = S3CredentialForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            s3credential = S3Credential(user=request.user)
            s3credential.name = form.cleaned_data['name']
            s3credential.access_key = form.cleaned_data['access_key']
            s3credential.secret_key = form.cleaned_data['secret_key']
            s3credential.buckets = form.cleaned_data['buckets']
            s3credential.exclude_paths = form.cleaned_data['exclude_paths']
            s3credential.exclude_files = form.cleaned_data['exclude_files']
            s3credential.save()
            return redirect('settings-index')
    context = {'form': form}
    return render(request, 'settings/create-s3-credential.html', context)


class S3CredentialUpdate(LoginRequiredMixin, UpdateView):
    model = S3Credential
    fields = ['name', 'access_key', 'secret_key', 'buckets', 'exclude_paths', 'exclude_files']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects


@method_decorator(login_required, name='dispatch')
class S3CredentialDetailView(DetailView):
    model = S3Credential

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects


@method_decorator(login_required, name='dispatch')
class S3CredentialDelete(DeleteView):
    model = S3Credential
    success_url = reverse_lazy('settings-index')

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.model.objects.filter(user=self.request.user)
        return self.model.objects


class ProviderCreate(CreateView):
    model = Provider
    fields = ['name']
