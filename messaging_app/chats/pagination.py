from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'  # Allows client to override page size
    max_page_size = 100  # Maximum limit for page size