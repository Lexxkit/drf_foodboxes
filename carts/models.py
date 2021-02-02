from django.contrib.auth import get_user_model
from django.db import models

from items.models import Item


class CartItem(models.Model):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(to='Cart', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Cart(models.Model):
    items = models.ManyToManyField(to=Item, through=CartItem)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='carts')
