from rest_framework_json_api.pagination import JsonApiLimitOffsetPagination


class LimitOffsetPagination(JsonApiLimitOffsetPagination):
    offset_query_param = "page[offset]"
    limit_query_param = "page[limit]"
    default_limit = 10
    max_limit = 25
