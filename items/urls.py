from rest_framework.routers import DefaultRouter

from .views import ItemReadOnlyViewSet

items_router = DefaultRouter()
items_router.register(r'items', ItemReadOnlyViewSet, basename='item')
urlpatterns = items_router.urls
