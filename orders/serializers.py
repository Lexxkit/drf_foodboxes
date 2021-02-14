from rest_framework import serializers

from carts.models import Cart
from.models import Order


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        default=serializers.CreateOnlyDefault('created'),
        choices=['created', 'cancelled']
    )

    class Meta:
        model = Order
        fields = ['id', 'cart', 'status', 'total_cost', 'address', 'delivery_at', 'created_at']
        read_only_fields = ['id', 'cart', 'total_cost', 'created_at']

    def create(self, validated_data):
        current_user = self.context['request'].user
        user_cart = Cart.objects.filter(user=current_user).exclude(orders__recipient=current_user).first()
        if user_cart.items.exists():
            order = Order(**validated_data)
            order.recipient = current_user
            order.cart = user_cart
            order.total_cost = user_cart.get_total_cost
            order.save()
            return order
        else:
            raise serializers.ValidationError('Empty cart cannot be ordered.')

    def update(self, instance, validated_data):
        if instance.status == 'created':
            instance = super().update(instance, validated_data)
            instance.save()
            return instance
        elif instance.status == 'delivered':
            raise serializers.ValidationError('Delivered order cannot be modified.')
        else:
            raise serializers.ValidationError('Order cannot be modified.')
