import codecs, json

from rest_framework.exceptions import ParseError
from rest_framework_json_api.parsers import JSONParser


class FixedJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        try:
            return json.loads(stream.read())
        except ValueError as exc:
            raise ParseError("JSON parse error - %s" % str(exc))
