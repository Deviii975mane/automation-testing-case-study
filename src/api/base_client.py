"""Base API client — auth headers, retries, transient-failure handling."""
import os
import time
import requests


class BaseClient:
    def __init__(self, api_url: str | None = None):
        self.api_url = api_url or os.getenv(
            "API_URL", "https://app.workflowpro.com/api/v1"
        )

    def headers(self, tenant_id: str) -> dict:
        token = os.getenv(f"TOKEN_{tenant_id}", "fake-token")
        return {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": tenant_id,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, tenant_id: str,
                 retries: int = 3, **kwargs):
        """HTTP request with simple retry on transient network errors."""
        url = f"{self.api_url}/{path.lstrip('/')}"
        headers = self.headers(tenant_id)
        last_exc = None
        for attempt in range(retries):
            try:
                return requests.request(
                    method, url, headers=headers, timeout=10, **kwargs
                )
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                time.sleep(1 * (attempt + 1))  # linear backoff
        raise last_exc