from fastapi.responses import ORJSONResponse

from nekos_api.api.schemas import ErrorSchema


class BaseError(Exception):
    status_code: int = 500
    title: str = "Error"
    message: str = "An error occurred."

    def __init__(
        self,
        *,
        title: str = ...,
        message: str = ...,
        status_code: int = ...,
    ):
        if title is not ...:
            self.title = title

        if message is not ...:
            self.message = message

        if status_code is not ...:
            self.status_code = status_code

    @classmethod
    async def handler(cls, _request, exc: "BaseError"):
        """Handles the exception and returns a standardized error response."""

        return ORJSONResponse(
            status_code=exc.status_code if hasattr(exc, "status_code") else cls.status_code,
            content=ErrorSchema(
                title=exc.title if hasattr(exc, "title") else cls.title,
                message=exc.message if hasattr(exc, "message") else cls.message,
            ).model_dump(mode="json"),
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, message={self.message!r}, status_code={self.status_code!r})"


class ErrorInitMixin:
    def __init__(self, message: str = ..., *, title: str = ...):
        if title is not ...:
            self.title = title

        if message is not ...:
            self.message = message


class InternalServerError(ErrorInitMixin, BaseError):
    title: str = "Internal Server Error"
    message: str = "An unexpected error occurred on the server."
    status_code: int = 500


class FailedDependencyError(ErrorInitMixin, BaseError):
    title: str = "Failed Dependency"
    message: str = "The request failed due to a failed dependency."
    status_code: int = 424


class ValidationError(ErrorInitMixin, BaseError):
    title: str = "Validation Error"
    message: str = "One or more validation errors occurred."
    status_code: int = 422


class ConflictError(ErrorInitMixin, BaseError):
    title: str = "Conflict"
    message: str = "The request could not be completed due to a conflict with the current state of the resource."
    status_code: int = 409


class NotFoundError(BaseError):
    title: str = "Not Found"
    message: str = "The requested resource was not found."
    status_code: int = 404

    def __init__(self, resource: str = "resource"):
        self.message = f"The requested {resource} was not found."


class ForbiddenError(ErrorInitMixin, BaseError):
    title: str = "Forbidden"
    message: str = "You do not have permission to access this resource."
    status_code: int = 403


class PaymentRequiredError(ErrorInitMixin, BaseError):
    title: str = "Payment Required"
    message: str = "Payment is required to access this resource."
    status_code: int = 402


class UnauthorizedError(ErrorInitMixin, BaseError):
    title: str = "Unauthorized"
    message: str = "You must be authenticated to access this resource."
    status_code: int = 401
