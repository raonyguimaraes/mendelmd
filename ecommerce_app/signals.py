from django.shortcuts import get_object_or_404
from .models import Order
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    print('recebido!!!!!!!!!!1')
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED and ipn.invoice:
        # payment was successful
        order = get_object_or_404(Order, id=ipn.invoice)

        if order.total_cost() == ipn.mc_gross:
            # mark the order as paid
            order.paid = True
            order.save()
