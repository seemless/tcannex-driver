from __future__ import annotations

import os

import httpx

from tcannex.exceptions import APIError, AuthenticationError
from tcannex.models import CPRTResponse


class TCAnnexClient:
    """Client for the TCAnnex CPRT API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.tcannex.com",
    ) -> None:
        resolved_key = api_key or os.environ.get("TCANNEX_API_KEY")
        if not resolved_key:
            raise AuthenticationError(
                "No API key provided. Set the TCANNEX_API_KEY environment variable "
                "or pass api_key to TCAnnexClient()."
            )
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {resolved_key}"},
        )

    def _request(self, method: str, path: str) -> CPRTResponse:
        response = self._client.request(method, path)
        if response.status_code < 200 or response.status_code >= 300:
            raise APIError(response.status_code, response.text)
        return CPRTResponse.model_validate(response.json())

    def get_root(self) -> CPRTResponse:
        """GET / — Read root."""
        return self._request("GET", "/")

    def get_documents(self) -> CPRTResponse:
        """GET /documents — List all documents."""
        return self._request("GET", "/documents")

    def get_document(self, document_identifier: str) -> CPRTResponse:
        """GET /documents/{document_identifier} — Get a document with relations."""
        return self._request("GET", f"/documents/{document_identifier}")

    def get_element(
        self, document_identifier: str, element_identifier: str
    ) -> CPRTResponse:
        """GET /elements/{document_identifier}/{element_identifier} — Get an element with relations."""
        return self._request(
            "GET", f"/elements/{document_identifier}/{element_identifier}"
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> TCAnnexClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
