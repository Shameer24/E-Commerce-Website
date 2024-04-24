from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from cart.models import Cart

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, related_name='order')
    total_price = models.FloatField(default=0.0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
