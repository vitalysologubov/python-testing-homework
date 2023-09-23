from http import HTTPStatus
from typing import Callable, TypeAlias

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.locales import Locale
from mimesis.random import global_seed
from mimesis.schema import Field, Schema

from tests.plugins.identity.user import (
    RegistrationData,
    RegistrationDataFactory,
    UserData,
)

CorrectUserData: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture()
def registration_data() -> RegistrationDataFactory:
    """Returns fake random registration data."""

    def factory(**fields) -> RegistrationData:
        field = Field(locale=Locale.RU, seed=global_seed)
        password = field('password')
        schema = Schema(schema=lambda: {
            'email': field('person.email'),
            'first_name': field('person.first_name'),
            'last_name': field('person.last_name'),
            'date_of_birth': field('datetime.date'),
            'address': field('address.city'),
            'job_title': field('person.occupation'),
            'phone': field('person.telephone'),
        })

        return {
            **schema.create()[0],
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@pytest.mark.django_db()
def test_registration_page(
    client: Client,
    registration_data: RegistrationData,
    expected_user_data: UserData,
    assert_correct_user: CorrectUserData,
) -> None:
    """The test ensures that registration is valid."""
    response = client.post(
        reverse('identity:registration'),
        data=registration_data(),
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(registration_data()['email'], expected_user_data)
