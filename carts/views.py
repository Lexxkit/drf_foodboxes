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
        # create cart for pre-populated mock users or get an existing one
        obj, _ = Cart.objects.get_or_create(
            user=self.request.user,
            defaults=None
        )
        return obj


class CartItemsViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = CartItemLimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = get_object_or_404(Cart, user=self.request.user)
        return queryset.cart_items.all()

    def get_object(self):
        queryset = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(queryset.cart_items, id=self.kwargs['pk'])
