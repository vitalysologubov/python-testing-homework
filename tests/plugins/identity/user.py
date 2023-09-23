import datetime
from typing import Callable, Protocol, TypedDict, final

import pytest

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """Represents user data."""

    email: str
    first_name: str
    last_name: str
    date_of_birth: datetime.datetime
    address: str
    job_title: str
    phone: str


@final
class RegistrationData(UserData, total=False):
    """Represents registratin data."""

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    """User data protocol."""

    def __call__(self, **fields) -> RegistrationData:
        """Returns user data."""


@pytest.fixture()
def expected_user_data(registration_data: RegistrationData) -> UserData:
    """Data modifier."""
    return {
        key_name: value_part
        for key_name, value_part in registration_data().items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def assert_correct_user() -> Callable[[str, UserData], None]:
    """Helper for data validation."""

    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active

        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory
