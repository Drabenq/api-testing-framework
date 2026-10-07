# API Testing Framework

![API tests](https://github.com/Drabenq/api-testing-framework/actions/workflows/api-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)

Automated test suite for the [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) API, a public API made for practicing testing. Built with **pytest** and **requests**, with **JSON Schema** contract validation, an HTML report and scheduled runs on **GitHub Actions**.

## What it covers

| Area | Examples |
|------|----------|
| Smoke | Health check, authentication, list bookings |
| CRUD | Create, read, full update, partial update, delete |
| Contract | Every response is validated against a JSON Schema |
| Security | Update and delete without token or with an invalid token |
| Negative | Bad credentials, missing fields, invalid dates |
| Filters | Search bookings by name |

## Bugs found

The suite found **5 defects** in the API, documented in [BUGS.md](BUGS.md) with severity and steps to reproduce. Tests for known bugs are marked `xfail(strict=True)`: the pipeline stays green while the bug exists and fails the day it is fixed, so nobody forgets to update the test.

## Design

```
api/client.py        # one method per endpoint; tests never build URLs
data/factories.py    # unique random test data for every test
schemas/booking.py   # JSON Schemas for contract testing
tests/conftest.py    # fixtures: client, token, booking with automatic cleanup
config.py            # base URL and credentials from environment variables
```

- **Independent tests**: every test creates its own data and the `booking` fixture deletes it afterwards.
- **Retries** for 502/503/504 because the demo API runs on a free host that sometimes sleeps.
- **Markers** to run only what you need: `pytest -m smoke`.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                 # full suite, report in reports/report.html
pytest -m smoke        # quick check
```

Point it at another environment with `BASE_URL=https://... pytest`.

## CI

Runs on every push and every weekday at 12:00 UTC to detect changes in the API. The HTML report is attached to each run as an artifact.
