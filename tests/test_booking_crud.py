import pytest

from data.factories import booking_payload
from schemas.booking import BOOKING, CREATED_BOOKING


@pytest.mark.regression
def test_create_booking(client, token, assert_schema):
    payload = booking_payload()

    response = client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    assert_schema(body, CREATED_BOOKING)
    assert body["booking"] == payload
    client.delete_booking(body["bookingid"], token=token)


@pytest.mark.regression
def test_get_booking_returns_saved_data(client, booking, assert_schema):
    response = client.get_booking(booking["id"])

    assert response.status_code == 200
    assert_schema(response.json(), BOOKING)
    assert response.json() == booking["payload"]


@pytest.mark.regression
def test_full_update_booking(client, token, booking):
    new_data = booking_payload(additionalneeds="Dinner")

    response = client.update_booking(booking["id"], new_data, token=token)

    assert response.status_code == 200
    assert response.json() == new_data
    assert client.get_booking(booking["id"]).json() == new_data


@pytest.mark.regression
def test_partial_update_only_changes_sent_fields(client, token, booking):
    response = client.partial_update_booking(booking["id"], {"totalprice": 1}, token=token)

    assert response.status_code == 200
    expected = {**booking["payload"], "totalprice": 1}
    assert response.json() == expected


@pytest.mark.regression
def test_delete_booking(client, token):
    created = client.create_booking(booking_payload()).json()

    delete = client.delete_booking(created["bookingid"], token=token)

    # Deletion answers 201 Created instead of 200/204 (see BUGS.md, BUG-02).
    assert delete.status_code == 201
    assert client.get_booking(created["bookingid"]).status_code == 404


@pytest.mark.regression
def test_get_unknown_booking_returns_404(client):
    assert client.get_booking(999_999_999).status_code == 404


@pytest.mark.regression
def test_filter_by_name_finds_booking(client, booking):
    payload = booking["payload"]

    response = client.get_booking_ids(firstname=payload["firstname"], lastname=payload["lastname"])

    ids = [item["bookingid"] for item in response.json()]
    assert booking["id"] in ids
