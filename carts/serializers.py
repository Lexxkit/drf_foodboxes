from rest_framework import serializers

from .models import Cart, CartItem
from items.models import Item
from items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, source='get_total_price', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'item', 'price', 'total_price']
        extra_kwargs = {
            'item_id': {'required': True},
            'quantity': {'required': True},
            'total_price': {'read_only': True},
        }
        depth = 1

    def create(self, validated_data):
        current_user = self.context['request'].user
        user_cart = Cart.objects.filter(user=current_user).exclude(orders__recipient=current_user).first()
        # check if item is already in the users cart
        if user_cart.items.filter(title=validated_data['item']):
            # if YES, then only increase QUANTITY in users cart
            cart_item = user_cart.cart_items.filter(item=validated_data['item']).first()
            cart_item.quantity += validated_data['quantity']
        # if NO - add item to the users cart
        else:
            cart_item = CartItem(
                item=validated_data['item'],
                quantity=validated_data['quantity'],
                price=validated_data['item'].price,
                cart=user_cart
            )

        cart_item.save()
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(max_digits=8, decimal_places=2, source='get_total_cost', read_only=True)
    items = CartItemSerializer(source='cart_items', many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
        read_only_fields = ['id', 'total_cost']
