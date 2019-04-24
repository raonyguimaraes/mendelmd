from django.shortcuts import get_object_or_404
from .models import Order, OrderType, PaymentStatus
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver


def get_order(order_id):
    return get_object_or_404(Order, id=order_id)


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED and ipn.invoice:
        # payment was successful
        order = get_order(ipn.invoice)

        if not ipn.is_subscription():
            order.order_type = OrderType.PRODUCT.__str__()

        if order.total_cost() == ipn.mc_gross:
            # mark the order as paid
            order.paid = True
            order.payment_status = PaymentStatus.PAID.__str__()
            order.save()
    elif ipn.is_subscription_cancellation() and ipn.invoice:
        order = get_order(ipn.invoice)
        order.paid = False
        order.payment_status = PaymentStatus.CANCELED.__str__()
        order.save()
    elif ipn.is_subscription_failed() and ipn.invoice:
        order = get_order(ipn.invoice)
        order.paid = False
        order.payment_status = PaymentStatus.REFUSED.__str__()
        order.save()
