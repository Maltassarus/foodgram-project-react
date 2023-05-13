from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginator(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.page.next_page_number,
                'previous': self.page.previous_page_number,
            },
            'count': self.page.paginator.count,
            'response': data,
        })
