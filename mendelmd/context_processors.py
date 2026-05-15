from django.conf import settings


def stripe(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY,
    }
