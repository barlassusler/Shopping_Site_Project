from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse



def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping':shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except:
            return render(request,'payment/checkout.html')
    else:
        return render(request, 'payment/checkout.html')



def payment_success(request):

    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 +  "\n" +  address2 + "\n" +
                            city + "\n" + state + "\n" + zipcode
                            )


        cart = Cart(request)
        total_cost = cart.get_total()



        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user =request.user)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity= item['qty'], price=item['price'], user=request.user)


        else:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                             amount_paid=total_cost)
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                             price=item['price'])


        order_success = True
        response = JsonResponse({'success': order_success})
        return response