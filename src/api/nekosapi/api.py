from django.http import Http404

from ninja import NinjaAPI

from nekosapi.errors import HttpError
from nekosapi.parsers import ORJSONParser
from nekosapi.renderers import ORJSONRenderer
from nekosapi.images.api import router as images_router
from nekosapi.artists.api import router as artists_router
from nekosapi.characters.api import router as characters_router


api = NinjaAPI(
    title="Nekos API",
    version="3",
    description="An open source anime art API.",
    servers=[
        {
            "url": "https://api.nekosapi.com",
            "description": "Production API",
        },
    ],
    parser=ORJSONParser(),
    renderer=ORJSONRenderer(),
)


@api.get(
    "",
    summary="Get a summary of the API.",
    description="Returns a bunch of data about the API, like endpoints, versions, and more. This is not really intended to be used by programs, but rather for users (devs) to see when they first use the API.",
)
async def index(request):
    return {
        "endpoints": [
            "/",
            "/images",
            "/images/{id:int}",
            "/images/{id:int}/tags",
            "/images/{id:int}/report",
            "/images/{id:int}/artist",
            "/images/{id:int}/characters",
            "/images/random",
            "/images/random/file",
            "/images/tags",
            "/images/tags/{id:int}",
            "/images/tags/{id:int}/images",
            "/artists",
            "/artists/{id:int}",
            "/artists/{id:int}/images",
            "/characters",
            "/characters/{id:int}",
            "/characters/{id:int}/images",
            "/openapi.json",
        ],
        "versions": {
            "v3": {"url": "https://api.nekosapi.com/v3", "status": "stable"},
            "v2": {"url": "https://api.nekosapi.com/v2", "status": "down"},
            "v1": {"url": "https://api.nekosapi.com/v1", "status": "deprecated"},
            "v0": {"url": "https://api.nekosapi.com/v0", "status": "deprecated"},
        },
        "github": "https://github.com/Nekos-API/Nekos-API",
        "discord": "https://discord.gg/PgQnuM3YnM",
        "openapi": "/v3/openapi.json",
        "documentation": "https://nekosapi.com/docs",
        "openapi_documentation": "https://api.nekosapi.com/v3/docs"
    }


@api.exception_handler(HttpError)
def http_error(request, exc: HttpError):
    return api.create_response(request, {"detail": exc.errors}, status=exc.status_code)


@api.exception_handler(Http404)
def http_404(request, exc: Http404):
    return api.create_response(
        request,
        {
            "detail": [
                {
                    "loc": [],
                    "msg": f"Could nto find this resource.",
                    "type": "not_found",
                    "ctx": {},
                }
            ]
        },
        status=404,
    )


api.add_router("/images", images_router)
api.add_router("/artists", artists_router)
api.add_router("/characters", characters_router)
