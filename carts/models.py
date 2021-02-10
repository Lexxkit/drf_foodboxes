from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item


class CartItem(models.Model):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def get_total_price(self):
        total_price = self.price * self.quantity
        return total_price


class Cart(models.Model):
    items = models.ManyToManyField(to=Item, through=CartItem)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='carts')

    @property
    def get_total_cost(self):
        cart_items = self.cart_items.all()
        total_cost = 0
        for item in cart_items:
            total_cost += (item.price * item.quantity)

        return total_cost
