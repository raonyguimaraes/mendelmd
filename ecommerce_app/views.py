from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, LineItem
from .forms import CartForm, CheckoutForm
from . import cart

# Create your views here.


def index(request):
    all_products = Product.objects.all()
    return render(request, "ecommerce_app/index.html", {
                                    'all_products': all_products,
                                    })


def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
                                            'product': product,
                                            'form': form,
                                            })


def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
                                            'cart_items': cart_items,
                                            'cart_subtotal': cart_subtotal,
                                            })


def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                name=cleaned_data.get('name'),
                email=cleaned_data.get('email'),
                postal_code=cleaned_data.get('postal_code'),
                address=cleaned_data.get('address'),
            )
            o.save()

            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                li = LineItem(
                    product_id=cart_item.product_id,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    order_id=o.id
                )

                li.save()

            cart.clear(request)

            request.session['order_id'] = o.id

            return redirect('process_payment')
    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())


def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    line_items = order.lineitem_set.all()
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecommerce_app/process_payment.html', {'order': order,
                                                                  'line_itens': line_items,
                                                                  'form': form})


@login_required
def process_subscription(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not product.is_subscription:
        return redirect('index')
    user = request.user
    order = Order.objects.create(user=user)
    line_item = LineItem.objects.create(product_id=product.id,
                                        price=product.price,
                                        quantity=1,
                                        order_id=order.id)
    host = request.get_host()

    paypal_dict = {
        'cmd': '_xclick-subscriptions',
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'a3': '%.2f' % order.total_cost().quantize(
            Decimal('.01')),  # monthly price
        'p3': 1,  # duration of each unit (depends on unit)
        't3': "M",  # duration unit ("M for Month")
        'src': "1",  # make payments recur
        'sra': "1",  # reattempt payment on payment error
        'no_note': "1",  # remove extra notes (optional)
        'item_name': product.slug,
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")

    # Output the button.
    return render(request, 'ecommerce_app/process_subscription.html', {'order': order,
                                                                       'line_items': order.lineitem_set.all(),
                                                                       'user': request.user,
                                                                       'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'ecommerce_app/payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')
