from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem

# Create your views here.

@login_required(login_url="/login/")
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == "POST":
        order = Order.objects.create(user=request.user, cart=cart, total_price=0)
        total_price = 0
        for item in cart.items.all():
            price = item.total_price
            total_price += price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.productPrice
            )
        order.total_price = total_price
        order.save()
        cart.items.all().delete()
        cart.delete()
        Cart.objects.create(user=request.user)
        return redirect('order_details', order_id=order.id)
    return render(request, 'cart.html', {'cart': cart})

@login_required(login_url="/login/")
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()
    return render(request, 'thanks.html', {'order': order, 'order_items': order_items})

@login_required(login_url="/login/")
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'ordersList.html', {'orders': orders})
