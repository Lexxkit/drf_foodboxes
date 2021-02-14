from rest_framework.routers import DefaultRouter

from .views import CreateListReviewViewSet

reviews_router = DefaultRouter()
reviews_router.register(r'', CreateListReviewViewSet, basename='review')

urlpatterns = reviews_router.urls
