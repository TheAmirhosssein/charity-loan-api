from rest_framework import response
from rest_framework.pagination import PageNumberPagination


class SimpleListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "item"

    def get_paginated_response(self, data):
        return response.Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
