from ninja.parser import Parser

import orjson


class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)
