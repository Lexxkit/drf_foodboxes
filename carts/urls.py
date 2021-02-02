from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CartView, CartItemsViewSet

carts_router = DefaultRouter()
carts_router.register(r'carts/items', CartItemsViewSet, basename='cartitem')
urlpatterns = carts_router.urls

urlpatterns += [
    path('carts/', CartView.as_view())
]
