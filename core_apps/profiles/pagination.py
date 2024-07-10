from rest_framework.pagination import PageNumberPagination


class ProfilePagination(PageNumberPagination):
    """Profile Pagination Class."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20
