import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
# Public demo credentials documented by Restful-Booker itself.
USERNAME = os.getenv("BOOKER_USER", "admin")
PASSWORD = os.getenv("BOOKER_PASSWORD", "password123")
