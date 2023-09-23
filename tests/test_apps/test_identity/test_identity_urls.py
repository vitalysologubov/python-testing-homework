from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_login_page(client: Client) -> None:
    """Test ensures that login page is accessible."""
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK


def test_logout_page(client: Client) -> None:
    """Test ensures that logout page is accessible and redirects to index."""
    response = client.get(reverse('identity:logout'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('index')


def test_registration_page(client: Client) -> None:
    """The test ensures that registration page is accessible."""
    response = client.get(reverse('identity:registration'))

    assert response.status_code == HTTPStatus.OK


def test_update_user_details_page_for_admin(admin_client: Client) -> None:
    """Test ensures that update user page is accessible for admin."""
    response = admin_client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK


def test_update_user_details_page_for_client(client: Client) -> None:
    """Test ensures that update user page is not accessible for client."""
    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.FOUND
