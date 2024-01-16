import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
# Paypal
from paypalcheckoutsdk.orders import OrdersGetRequest

from cart.cart import Cart
from .forms import AddressForm
from .models import DeliveryOptions, Order, OrderItem, Address
from .paypal import PayPalClient


@login_required
def checkout_view(request):
    """Handles the address form:
    - create address
    - update address    
    """
    deliveries = DeliveryOptions.objects.filter(is_active=True)
    cart = Cart(request)

    # Try to get the default address, or create a new one if it doesn't exist
    address, created = Address.objects.get_or_create(
        user=request.user,
        default=True,
        defaults={'user': request.user, 'default': True}
    )

    address_form = AddressForm(instance=address)

    if request.method == 'POST':
        address_form = AddressForm(data=request.POST, instance=address)
        if address_form.is_valid():
            # If the form is valid, save the address and proceed to the payment selection            
            address_form.save()
            return redirect(reverse('checkout:payment-selection'))

        # If the form is not valid, display an error message
        messages.error(request,
                       'Required address fields and delivery option have to '
                       'be selected. Please check your input.')

    context = {
        'cart': cart,
        'deliveries': deliveries,
        'address_form': address_form,
        'title': 'Checkout',
    }
    return render(request, 'checkout/checkout.html', context)


def cart_update_delivery(request):
    """
    Updates delivery price dynamically though 
    ajax and adds purchase ket to the Session
    """
    cart = Cart(request)
    if request.POST.get('action') == 'POST':
        # Get the selected delivery option ID from the POST data
        delivery_option = int(request.POST.get('delivery_option'))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)

        # Update the total price in the cart by adding the delivery cost
        updated_total_price = cart.cart_update_delivery(
            delivery_type.delivery_price)

        # Access the session to store or update the purchase information
        session = request.session
        if 'purchase' not in request.session:
            # If 'purchase' key doesn't exist in the session, create it
            session['purchase'] = {
                'delivery_id': delivery_type.id,
            }
        else:
            # If 'purchase' key exists, update the delivery_id and mark the session as modified
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        # Prepare a JSON response with the updated total price and delivery price            
        response = JsonResponse({'total': updated_total_price,
                                 'delivery_price': delivery_type.delivery_price})
        return response


@login_required
def payment_selection(request):
    session = request.session

    if 'purchase' not in session:
        messages.warning(request,
                         'Please select both address and delivery option!')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    # Create an order for pay on receive
    cart = Cart(request)
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price(),
        delivery=DeliveryOptions.objects.get(pk=cart.get_delivery_option_id()),
        transaction_id='',
        payment_option='on_receive',
        billing_status=False,
        order_status='pending',
        shipping_address=Address.objects.filter(user=request.user,
                                                default=True).first()
    )

    # Create order items based on the cart
    for item in cart:
        OrderItem.objects.create(
            order=order,
            book=item['book'],
            quantity=item['quantity'],
            language=item['language_id'],
            book_type=item['book_type_id'],
            price=item['price'],
            subtotal_price=item['total_price'],
        )

    return render(request, 'checkout/payment_selection.html',
                  {'title': 'Payment Selection'})


###########################################################################
#  PayPay

@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body['orderID']

    # Fetch details about the PayPal payment
    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)

    # Update an order in your system based on PayPal response   
    try:
        order = Order.objects.get(transaction_id=data)
        order.total_price = response.result.purchase_units[0].amount.value
        order.transaction_id = data
        order.billing_status = True
        order.save()
        return JsonResponse('Payment completed!', safe=False)
    except Exception:
        return redirect('checkout:payment-failed', status=500)


@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'checkout/payment_successful.html',
                  {'title': 'Successful Payment'})


@login_required
def payment_failed(request):
    return render(request, 'checkout/payment_failed.html',
                  {'title': 'Payment Failed'})
