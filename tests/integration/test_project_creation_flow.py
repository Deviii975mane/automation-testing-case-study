"""
Part 3 — API + UI + Mobile integration test.

Strategy (test pyramid):
  1. Create project via API (fast, reliable setup).
  2. Verify it displays in the web UI for the owning tenant.
  3. Verify mobile accessibility via BrowserStack (mobile web).
  4. Verify tenant isolation at both UI and API layers (security).

Edge cases handled: network retries (API client), slow loading
(auto-waiting expect), mobile responsiveness (expand nav), and
test-data cleanup (fixture teardown with unique run-IDs).
"""
import os
import uuid
import pytest
from playwright.sync_api import sync_playwright, expect

from src.api.projects_client import ProjectsClient
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.utils.config_loader import load_environment
from src.utils.driver_factory import get_context

HEADLESS = os.getenv("CI", "false").lower() == "true"


@pytest.fixture
def projects_client():
    return ProjectsClient()


@pytest.fixture
def created_project(projects_client):
    """API-created project scoped to Company1, cleaned up after."""
    env = load_environment("company1")
    tenant_id = env["tenant_id"]
    name = f"Integration Project {uuid.uuid4().hex[:8]}"

    resp = projects_client.create_project(tenant_id, name, "integration test")
    assert resp.status_code in (200, 201), f"API create failed: {resp.text}"
    project = resp.json()
    project["tenant_id"] = tenant_id

    yield project

    projects_client.delete_project(tenant_id, project["id"])


def _verify_in_ui(env_name: str, project_name: str, should_be_visible: bool,
                  browser_name: str = "chromium"):
    """Reusable web UI check — reused for both owning and other tenant."""
    env = load_environment(env_name)
    playwright, browser, context = get_context(
        browser_name=browser_name, headless=HEADLESS
    )
    try:
        page = context.new_page()
        login = LoginPage(page, env["base_url"])
        dashboard = DashboardPage(page, env["base_url"])
        login.login_default(f"user@{env_name}.com", env["tenant_id"])
        dashboard.open("dashboard")
        if should_be_visible:
            dashboard.assert_project_visible(project_name)
        else:
            dashboard.assert_project_not_visible(project_name)
    finally:
        context.close()
        browser.close()
        playwright.stop()


def _verify_on_mobile(project_name: str):
    """
    Mobile web verification via BrowserStack.
    Edge case: on mobile the card may be behind a collapsed nav menu,
    so we expand it before asserting. Skipped if BrowserStack creds absent.
    """
    if not os.getenv("BROWSERSTACK_USERNAME"):
        pytest.skip("BrowserStack credentials not configured")

    caps = {"device": "iPhone 15", "os_version": "17", "real_mobile": True}
    playwright, browser, context = get_context(
        use_browserstack=True, caps=caps
    )
    try:
        env = load_environment("company1")
        page = context.new_page()
        login = LoginPage(page, env["base_url"])
        dashboard = DashboardPage(page, env["base_url"])
        login.login_default("user@company1.com", env["tenant_id"])
        dashboard.open("dashboard")

        # Expand mobile nav if present, then assert
        menu = page.locator(".mobile-menu-toggle")
        if menu.is_visible():
            menu.click()
        dashboard.assert_project_visible(project_name)
    finally:
        context.close()
        browser.close()
        playwright.stop()


@pytest.mark.integration
@pytest.mark.security
def test_project_creation_flow(created_project, projects_client):
    project = created_project
    name = project["name"]

    # 1. API creation validated in the fixture
    assert project["status"] == "active"

    # 2. Web UI: visible to the owning tenant (Company1)
    _verify_in_ui("company1", name, should_be_visible=True)

    # 3. Mobile: accessible on a real device (BrowserStack)
    _verify_on_mobile(name)

    # 4a. Security (UI): NOT visible to Company2
    _verify_in_ui("company2", name, should_be_visible=False)

    # 4b. Security (API): Company2 token cannot read the project
    other_tenant = load_environment("company2")["tenant_id"]
    resp = projects_client.get_project(other_tenant, project["id"])
    assert resp.status_code in (403, 404), "Tenant isolation breach!"


@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_project_visible_cross_browser(created_project, browser_name):
    """Cross-browser: project displays correctly on all supported browsers."""
    _verify_in_ui("company1", created_project["name"],
                  should_be_visible=True, browser_name=browser_name)