"""Test data builders. Every call returns fresh, unique data."""
import random
import uuid
from datetime import date, timedelta

FIRST_NAMES = ["Lucia", "Mateo", "Sofia", "Benjamin", "Valentina", "Joaquin", "Martina", "Tomas"]
LAST_NAMES = ["Gomez", "Fernandez", "Lopez", "Diaz", "Martinez", "Perez", "Romero", "Sosa"]


def unique_suffix() -> str:
    return uuid.uuid4().hex[:6]


def booking_payload(**overrides) -> dict:
    checkin = date.today() + timedelta(days=random.randint(1, 30))
    checkout = checkin + timedelta(days=random.randint(1, 10))
    payload = {
        "firstname": f"{random.choice(FIRST_NAMES)}{unique_suffix()}",
        "lastname": random.choice(LAST_NAMES),
        "totalprice": random.randint(50, 900),
        "depositpaid": random.choice([True, False]),
        "bookingdates": {"checkin": checkin.isoformat(), "checkout": checkout.isoformat()},
        "additionalneeds": random.choice(["Breakfast", "Late checkout", "Parking"]),
    }
    payload.update(overrides)
    return payload
