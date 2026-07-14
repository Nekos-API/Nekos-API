from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from nekos_api.lib import settings, project
from nekos_api.api import docs
from nekos_api.api.errors import BaseError, NotFoundError, ValidationError, InternalServerError
from nekos_api.api.lifespan import lifespan
from nekos_api.api.images.router import router as images_router


app = FastAPI(
    debug=settings.DEBUG,
    title="Nekos API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)


app.add_exception_handler(404, NotFoundError.handler)


app_v5 = FastAPI(
    debug=settings.DEBUG,
    title="Nekos API",
    description=docs.OPENAPI_DESCRIPTION,
    version=project.get_project_version(),
    docs_url=None,
    redoc_url="/docs",
    openapi_tags=docs.OPENAPI_TAGS,
    default_response_class=ORJSONResponse,
)


app_v5.include_router(images_router)

app_v5.add_exception_handler(BaseError, BaseError.handler)
app_v5.add_exception_handler(404, NotFoundError.handler)
app_v5.add_exception_handler(422, ValidationError.handler)
app_v5.add_exception_handler(Exception, InternalServerError.handler)


app.mount("/v5", app_v5)
