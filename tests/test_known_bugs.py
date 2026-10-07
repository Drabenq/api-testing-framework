"""Tests describing the *expected* behaviour where the API currently fails.

They are marked xfail(strict=True): the suite stays green while the bug exists,
and turns red the day the bug is fixed, so the test gets updated.
Details in BUGS.md.
"""
import pytest

from data.factories import booking_payload


@pytest.mark.xfail(strict=True, reason="BUG-03: bad credentials return 200 instead of 401")
def test_bad_credentials_return_401(client):
    assert client.create_token("admin", "wrong").status_code == 401


@pytest.mark.xfail(strict=True, reason="BUG-04: missing required fields return 500 instead of 400")
def test_create_booking_without_required_fields_returns_400(client):
    payload = booking_payload()
    del payload["firstname"]
    assert client.create_booking(payload).status_code == 400


@pytest.mark.xfail(strict=True, reason="BUG-05: checkout before checkin is accepted")
def test_checkout_before_checkin_is_rejected(client, token):
    payload = booking_payload(bookingdates={"checkin": "2030-01-10", "checkout": "2030-01-01"})
    response = client.create_booking(payload)
    if response.status_code == 200:
        client.delete_booking(response.json()["bookingid"], token=token)
    assert response.status_code == 400
