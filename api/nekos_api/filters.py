import re
from rest_framework_json_api.filters import QueryParameterValidationFilter


class QueryParameterValidation(QueryParameterValidationFilter):
    query_regex = re.compile(
        r"^(sort|include|token)$|^(?P<type>filter|fields|page)(\[[\w\.\-]+\])?$"
    )
