from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Cart, CartItem
from .paginators import CartItemLimitOffsetPagination
from .serializers import CartSerializer, CartItemSerializer


class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: CartSerializer(many=True)})
    def get(self, request):
        user = request.user
        user_cart, _ = Cart.objects.get_or_create(
            user=user,
            defaults=None
        )
        serializer = CartSerializer(user_cart)
        return Response(serializer.data)


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
