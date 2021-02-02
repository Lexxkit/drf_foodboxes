from decimal import Decimal

from rest_framework import serializers

from .models import Cart, CartItem
from items.models import Item
from items.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'item', 'price', 'total_price']
        extra_kwargs = {
            'item_id': {'required': True},
            'quantity': {'required': True},
        }
        depth = 1

    def get_total_price(self, obj):
        total_price = Decimal(obj.price * obj.quantity).quantize(Decimal('1.00'))
        return str(total_price)

    def create(self, validated_data):
        user_cart = Cart.objects.get(user=self.context['request'].user)
        cart_item = CartItem(
            item=validated_data['item'],
            quantity=validated_data['quantity'],
            price=validated_data['item'].price,
            cart=user_cart
        )
        cart_item.save()
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    items = CartItemSerializer(source='cart_items', many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cost']
        read_only_fields = ['id']

    def get_total_cost(self, obj):
        cart_items = obj.cart_items.all()
        total_cost = 0
        for item in cart_items:
            print(item)
            total_cost += (item.price * item.quantity)

        return str(Decimal(total_cost).quantize(Decimal('1.00')))
