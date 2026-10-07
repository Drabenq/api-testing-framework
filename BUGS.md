# Bug report – Restful-Booker API

Defects found while building this suite. Each one is covered by a test.

| ID | Severity | Endpoint | Expected | Actual | Test |
|----|----------|----------|----------|--------|------|
| BUG-01 | Low | `GET /ping` | `200 OK` | `201 Created` | `test_smoke.py::test_health_check` |
| BUG-02 | Low | `DELETE /booking/{id}` | `200 OK` or `204 No Content` | `201 Created` | `test_booking_crud.py::test_delete_booking` |
| BUG-03 | Medium | `POST /auth` with wrong password | `401 Unauthorized` | `200 OK` with `{"reason": "Bad credentials"}` | `test_known_bugs.py::test_bad_credentials_return_401` |
| BUG-04 | High | `POST /booking` without `firstname` | `400 Bad Request` with validation message | `500 Internal Server Error` | `test_known_bugs.py::test_create_booking_without_required_fields_returns_400` |
| BUG-05 | High | `POST /booking` with checkout before checkin | `400 Bad Request` | Booking is created | `test_known_bugs.py::test_checkout_before_checkin_is_rejected` |

## Steps to reproduce BUG-04

1. Send `POST /booking` with header `Content-Type: application/json`.
2. Body: a valid booking without the `firstname` field.
3. Observe `500 Internal Server Error`.

**Impact:** clients receive a server error instead of a validation message, so they cannot tell the user what is wrong. A 500 also triggers alerts as if the server were broken.
