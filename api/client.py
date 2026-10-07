"""Thin wrapper around the Restful-Booker API.

Tests talk to this client instead of calling `requests` directly, so URLs,
headers and auth live in one place.
"""
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)


class BookerClient:
    def __init__(self, base_url: str, timeout: float = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        # The demo API is hosted on a free tier and sometimes answers 502/503 while waking up.
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504], allowed_methods=None)
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def _request(self, method: str, path: str, token: str | None = None, **kwargs) -> requests.Response:
        headers = kwargs.pop("headers", {})
        if token:
            headers["Cookie"] = f"token={token}"
        response = self.session.request(
            method, f"{self.base_url}{path}", headers=headers, timeout=self.timeout, **kwargs
        )
        log.info("%s %s -> %s (%.0f ms)", method, path, response.status_code,
                 response.elapsed.total_seconds() * 1000)
        return response

    # --- endpoints -------------------------------------------------------
    def ping(self):
        return self._request("GET", "/ping")

    def create_token(self, username: str, password: str):
        return self._request("POST", "/auth", json={"username": username, "password": password})

    def get_booking_ids(self, **filters):
        return self._request("GET", "/booking", params=filters)

    def get_booking(self, booking_id: int):
        return self._request("GET", f"/booking/{booking_id}")

    def create_booking(self, payload: dict):
        return self._request("POST", "/booking", json=payload)

    def update_booking(self, booking_id: int, payload: dict, token: str | None = None):
        return self._request("PUT", f"/booking/{booking_id}", token=token, json=payload)

    def partial_update_booking(self, booking_id: int, payload: dict, token: str | None = None):
        return self._request("PATCH", f"/booking/{booking_id}", token=token, json=payload)

    def delete_booking(self, booking_id: int, token: str | None = None):
        return self._request("DELETE", f"/booking/{booking_id}", token=token)
