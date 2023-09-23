from http import HTTPStatus

import pytest
import requests


@pytest.mark.slow()
def test_get_json_from_api() -> None:
    """Test data retrieval from external API."""
    response = requests.get('http://localhost:6262/posts/', timeout=(2, 5))

    assert response.status_code == HTTPStatus.OK
