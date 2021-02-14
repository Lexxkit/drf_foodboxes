from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import ItemFilter
from .models import Item
from .paginators import ItemPageNumberPagination
from .serializers import ItemSerializer

USER_CACHE_KEY = 'user_cache_{}'
USER_CACHE_TTL = 300    # 5 min


class ItemReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering_fields = ['price']
    pagination_class = ItemPageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        key = USER_CACHE_KEY.format('items')
        cached_queryset = cache.get(key)
        if cached_queryset:
            return cached_queryset
        else:
            queryset = Item.objects.all()
            cache.set(key, queryset, USER_CACHE_TTL)
            return queryset
