from django.contrib.auth import get_user_model
from django.db import models

from carts.models import Cart


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('delivered', 'Delivered'),
        ('processed', 'Processed'),
        ('cancelled', 'Cancelled'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    delivery_at = models.DateTimeField(default=None)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=256)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='created')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.address
