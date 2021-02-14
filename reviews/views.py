from rest_framework import mixins, viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from .models import Review
from .paginators import ReviewLimitOffsetPagination
from .serializers import ReviewSerializer


class CreateListReviewViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = ReviewLimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(status='published')
        return queryset
