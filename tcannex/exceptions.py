class TCAnnexError(Exception):
    """Base exception for all TCAnnex driver errors."""


class AuthenticationError(TCAnnexError):
    """Raised when the API key is missing or invalid."""


class APIError(TCAnnexError):
    """Raised on non-2xx API responses."""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"API request failed with status {status_code}: {body}")
