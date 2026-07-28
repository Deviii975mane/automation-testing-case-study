"""Shared pytest fixtures for the WorkFlow Pro automation suite."""
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.utils.config_loader import load_environment, load_browsers

load_dotenv()

DEFAULT_TIMEOUT = int(os.getenv("PW_TIMEOUT", "15000"))
HEADLESS = os.getenv("CI", "false").lower() == "true"


@pytest.fixture(scope="session")
def env():
    """Loads the active tenant environment config (default: company1)."""
    return load_environment(os.getenv("ENV", "company1"))


@pytest.fixture(scope="session")
def browsers_config():
    return load_browsers()


@pytest.fixture
def page():
    """Isolated Playwright page with guaranteed cleanup on failure."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        context.set_default_timeout(DEFAULT_TIMEOUT)
        pg = context.new_page()
        try:
            yield pg
        finally:
            context.close()
            browser.close()


@pytest.fixture
def api_headers():
    """Factory returning auth headers for a given tenant."""
    def _headers(tenant_id):
        token = os.getenv(f"TOKEN_{tenant_id}", "fake-token")
        return {
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": tenant_id,
            "Content-Type": "application/json",
        }
    return _headers