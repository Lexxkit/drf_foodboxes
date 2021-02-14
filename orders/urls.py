from rest_framework.routers import DefaultRouter

from .views import CreateListRetrieveUpdateOrderViewSet

orders_router = DefaultRouter()
orders_router.register(r'', CreateListRetrieveUpdateOrderViewSet, basename='orders')

urlpatterns = orders_router.urls
