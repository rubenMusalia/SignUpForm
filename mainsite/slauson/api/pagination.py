from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )


class ProfileLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class ProfileNumberPagination(PageNumberPagination):
    page_size = 5