from rest_framework.pagination import LimitOffsetPagination


class OrderLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 3
