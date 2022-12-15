class GGbanError(Exception):
    pass


class Error(GGbanError):
    def __init__(self, name: str, message: str, code: int):
        self.name = name
        self.message = message
        self.code = code
        Exception.__init__(
            self, f"code: {self.code} name: '{self.name}' message: {self.message}"
        )


class UnauthorizedError(GGbanError):
    pass


class NotFoundError(GGbanError):
    pass


class Forbidden(GGbanError):
    def __init__(self, token: str) -> None:
        Exception.__init__(
            self, f"Your token: `{token}` does not have the necessary permissions."
        )


class TooManyRequests(GGbanError):
    method: str
    message: str

    def __init__(self, method: str, message: str) -> None:
        self.method = method
        self.message = message
        Exception.__init__(
            self, f"Too Many Requests for method '{method}'. Message: {message}."
        )
