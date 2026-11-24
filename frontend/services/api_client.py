import logging
from typing import Any

import requests

from frontend.config import API_BASE_URL, API_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class APIClientError(Exception):
    """Raised when communication with the backend fails."""


class APIClient:
    """HTTP client used by the Streamlit frontend."""

    def __init__(
        self,
        base_url: str = API_BASE_URL,
        timeout: float = API_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Send an HTTP request and return a JSON object."""

        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise APIClientError("Backend returned an unexpected response format.")

            return data

        except requests.exceptions.Timeout as exc:
            logger.warning("Backend request timed out: %s", endpoint)
            raise APIClientError("The backend took too long to respond.") from exc

        except requests.exceptions.ConnectionError as exc:
            logger.warning("Backend connection failed: %s", endpoint)
            raise APIClientError(
                "Cannot connect to the backend. Check whether FastAPI is running."
            ) from exc

        except requests.exceptions.HTTPError as exc:
            status_code = (
                exc.response.status_code if exc.response is not None else "unknown"
            )
            logger.warning(
                "Backend returned HTTP error %s for %s",
                status_code,
                endpoint,
            )
            raise APIClientError(
                f"Backend returned HTTP error: {status_code}."
            ) from exc

        except requests.exceptions.RequestException as exc:
            logger.exception("Unexpected HTTP client error")
            raise APIClientError("An unexpected network error occurred.") from exc

        except ValueError as exc:
            logger.error("Backend returned invalid JSON: %s", endpoint)
            raise APIClientError("Backend returned invalid JSON.") from exc

    def health_check(self) -> dict[str, Any]:
        """Check whether the backend is responding."""
        return self._request("GET", "/health")

    def ask_question(
        self,
        question: str,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        """Send an employee question to the backend."""

        if not question.strip():
            raise APIClientError("Question cannot be empty.")

        payload: dict[str, Any] = {"question": question.strip()}

        if conversation_id:
            payload["conversation_id"] = conversation_id

        return self._request(
            "POST",
            "/api/v1/chat",
            json=payload,
        )

    def upload_document(
        self,
        filename: str,
        file_content: bytes,
    ) -> dict[str, Any]:
        """Upload a document to the backend."""

        if not filename:
            raise APIClientError("Filename cannot be empty.")

        if not file_content:
            raise APIClientError("Uploaded file is empty.")

        files = {
            "file": (
                filename,
                file_content,
                "application/octet-stream",
            )
        }

        return self._request(
            "POST",
            "/api/v1/documents",
            files=files,
        )
