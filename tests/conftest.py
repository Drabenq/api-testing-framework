import pytest
from jsonschema import FormatChecker, validate

from api.client import BookerClient
from data.factories import booking_payload

from config import BASE_URL, PASSWORD, USERNAME


@pytest.fixture(scope="session")
def client() -> BookerClient:
    return BookerClient(BASE_URL)


@pytest.fixture(scope="session")
def token(client) -> str:
    response = client.create_token(USERNAME, PASSWORD)
    assert response.status_code == 200, response.text
    return response.json()["token"]


@pytest.fixture()
def booking(client, token):
    """Creates a booking for the test and deletes it afterwards."""
    payload = booking_payload()
    response = client.create_booking(payload)
    assert response.status_code == 200, response.text
    created = response.json()
    yield {"id": created["bookingid"], "payload": payload}
    client.delete_booking(created["bookingid"], token=token)


@pytest.fixture()
def assert_schema():
    def _assert(instance, schema):
        validate(instance=instance, schema=schema, format_checker=FormatChecker())

    return _assert
