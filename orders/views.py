from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from .models import Order
from .paginators import OrderLimitOffsetPagination
from .serializers import OrderSerializer


class CreateListRetrieveUpdateOrderViewSet(mixins.CreateModelMixin,
                                           mixins.ListModelMixin,
                                           mixins.RetrieveModelMixin,
                                           mixins.UpdateModelMixin,
                                           viewsets.GenericViewSet):

    authentication_classes = [TokenAuthentication]
    pagination_class = OrderLimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(recipient=self.request.user)
        return queryset
