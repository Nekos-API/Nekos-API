import os

from urllib import parse

from django import http


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method == "OPTIONS"
            and "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META
        ):
            response = http.HttpResponse()
            response["Content-Length"] = "0"
            response["Access-Control-Max-Age"] = 86400

        # Allow only domains and subdomains of the BASE_DOMAIN env var to send
        # credentials.
        response["Access-Control-Allow-Origin"] = (
            "*"
            if "Origin" not in request.headers
            else request.headers["Origin"]
            if "Origin" in request.headers
            and (
                parse.urlparse(request.headers["Origin"]).netloc.split(":")[0]
                == os.getenv("BASE_DOMAIN")
                or parse.urlparse(request.headers["Origin"])
                .netloc.split(":")[0]
                .endswith("." + os.getenv("BASE_DOMAIN", "nekosapi.com"))
            )
            else "*"
        )
        response["Access-Control-Allow-Credentials"] = (
            "false"
            if "Origin" not in request.headers
            else "true"
            if "Origin" in request.headers
            and (
                parse.urlparse(request.headers["Origin"]).netloc.split(":")[0]
                == os.getenv("BASE_DOMAIN")
                or parse.urlparse(request.headers["Origin"])
                .netloc.split(":")[0]
                .endswith("." + os.getenv("BASE_DOMAIN", "nekosapi.com"))
            )
            else "false"
        )
        response[
            "Access-Control-Allow-Methods"
        ] = "DELETE, GET, OPTIONS, PATCH, POST, PUT"
        response[
            "Access-Control-Allow-Headers"
        ] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        return response


class DisableCSRFMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response