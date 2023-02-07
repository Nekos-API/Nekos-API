import json

from django.http import HttpResponse


class JSONAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ["HEAD", "OPTIONS"]:
            if request.path.startswith("/v2/") and not request.path.startswith("/v2/auth/"):
                if request.META.get("HTTP_ACCEPT") != "application/vnd.api+json":
                    return HttpResponse(status=415)

        response = self.get_response(request)
        return response
