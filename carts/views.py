from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from .models import Cart, CartItem
from .paginators import CartItemLimitOffsetPagination
from .serializers import CartSerializer, CartItemSerializer


class CartView(RetrieveAPIView):
    queryset = Cart.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        current_user = self.request.user
        # get the user's cart that hasn't been ordered yet
        cart_obj = Cart.objects.filter(user=current_user).exclude(orders__recipient=current_user).first()
        # if not such a cart, then it will be created
        if not cart_obj:
            cart_obj = Cart.objects.create(user=current_user)

        return cart_obj


class CartItemsViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = CartItemLimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        # get the user's cart that hasn't been ordered yet
        queryset = Cart.objects.filter(user=current_user).exclude(orders__recipient=current_user).first()
        return queryset.cart_items.all()

    def get_object(self):
        current_user = self.request.user
        # get the user's cart that hasn't been ordered yet
        queryset = Cart.objects.filter(user=current_user).exclude(orders__recipient=current_user).first()
        return get_object_or_404(queryset.cart_items, id=self.kwargs['pk'])
