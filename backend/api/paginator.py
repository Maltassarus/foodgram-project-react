from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginator(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 6