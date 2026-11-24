from unittest.mock import Mock, patch

import pytest
import requests

from frontend.services.api_client import APIClient, APIClientError


def test_health_check_returns_backend_response() -> None:
    """Verify that a successful health check returns JSON."""

    expected_response = {"status": "healthy"}

    mock_response = Mock()
    mock_response.json.return_value = expected_response

    with patch(
        "frontend.services.api_client.requests.request",
        return_value=mock_response,
    ) as mock_request:

        client = APIClient(base_url="http://localhost:8000")

        result = client.health_check()

        assert result == expected_response

        mock_request.assert_called_once()


def test_empty_question_is_rejected() -> None:
    """Verify that an empty question is not sent to the backend."""

    client = APIClient()

    with pytest.raises(APIClientError):
        client.ask_question("   ")


def test_connection_error_is_handled() -> None:
    """Verify that backend connection errors become readable errors."""

    with patch(
        "frontend.services.api_client.requests.request",
        side_effect=requests.exceptions.ConnectionError,
    ):

        client = APIClient(base_url="http://localhost:8000")

        with pytest.raises(APIClientError) as error:
            client.health_check()

        assert "Cannot connect to the backend" in str(error.value)
