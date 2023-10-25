class HttpError(Exception):
    def __init__(self, status_code: int = 500, errors: list = []) -> None:
        self.errors = errors
        self.status_code = status_code
        super().__init__()
