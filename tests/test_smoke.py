import pytest

from config import PASSWORD, USERNAME
from schemas.booking import BOOKING_IDS, TOKEN


@pytest.mark.smoke
def test_health_check(client):
    # Restful-Booker answers its health check with 201 instead of 200 (see BUGS.md, BUG-01).
    assert client.ping().status_code == 201


@pytest.mark.smoke
def test_auth_returns_token(client, assert_schema):
    response = client.create_token(USERNAME, PASSWORD)

    assert response.status_code == 200
    assert_schema(response.json(), TOKEN)


@pytest.mark.smoke
def test_list_bookings(client, assert_schema):
    response = client.get_booking_ids()

    assert response.status_code == 200
    assert_schema(response.json(), BOOKING_IDS)
