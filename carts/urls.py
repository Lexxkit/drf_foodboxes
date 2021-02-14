from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CartView, CartItemsViewSet

carts_router = DefaultRouter()
carts_router.register(r'items', CartItemsViewSet, basename='cartitems')

urlpatterns = [
    path('', CartView.as_view(), name='cart')
]

urlpatterns += carts_router.urls
