import pytest

from data.factories import booking_payload


@pytest.mark.regression
@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "bad-token"])
def test_update_requires_valid_token(client, booking, token):
    response = client.update_booking(booking["id"], booking_payload(), token=token)
    assert response.status_code == 403


@pytest.mark.regression
@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "bad-token"])
def test_delete_requires_valid_token(client, booking, token):
    assert client.delete_booking(booking["id"], token=token).status_code == 403
    assert client.get_booking(booking["id"]).status_code == 200


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password",
    [("admin", "wrong"), ("nobody", "password123"), ("", "")],
    ids=["wrong-password", "unknown-user", "empty"],
)
def test_bad_credentials_do_not_return_token(client, username, password):
    response = client.create_token(username, password)
    assert "token" not in response.json()
