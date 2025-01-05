import ninja

from nekosapi.images.api import router as images_router


api = ninja.NinjaAPI(title="Nekos API", version="4.0.0")


@api.get("/")
def index(request):
    return {
        "message": "Welcome to Nekos API!",
        "version": "4.0.0",
        "endpoints": [
            "/v4/images",
            "/v4/images/random",
            "/v4/images/random/file",
            "/v4/images/{image_id}",
            "/v4/images/{image_id}/file",
        ],
    }


@api.get("/v3/{path}")
def v3_discontinued(request, path: str):
    return {
        "message": "This version has been discontinued. Use v4 instead.",
    }


@api.get("/v2/{path}")
def v2_discontinued(request, path: str):
    return {
        "message": "This version has been discontinued. Use v4 instead.",
    }


@api.get("/v1/{path}")
def v1_discontinued(request, path: str):
    return {
        "message": "This version has been discontinued. Use v4 instead.",
    }


@api.get("/v0/{path}")
def v0_discontinued(request, path: str):
    return {
        "message": "This version has been discontinued. Use v4 instead.",
    }


api.add_router("/v4/", images_router)
