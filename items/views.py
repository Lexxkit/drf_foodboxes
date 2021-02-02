from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import ItemFilter
from .models import Item
from .paginators import ItemPageNumberPagination
from .serializers import ItemSerializer


class ItemReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering_fields = ['price']
    pagination_class = ItemPageNumberPagination
    permission_classes = [permissions.AllowAny]
