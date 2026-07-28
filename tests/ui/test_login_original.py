"""
REFERENCE ONLY — the intern's original flaky test.
Kept for comparison against test_login_fixed.py. Do NOT run in CI.
See docs/PART1_FLAKY_ANALYSIS.md for the full breakdown of what's wrong.
"""
import pytest
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.skip(reason="Flaky reference implementation")


def test_user_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://app.workflowpro.com/login")
        page.fill("#email", "admin@company1.com")
        page.fill("#password", "password123")
        page.click("#login-btn")
        # ISSUE: no wait, strict URL equality, is_visible() as assertion
        assert page.url == "https://app.workflowpro.com/dashboard"
        assert page.locator(".welcome-message").is_visible()
        browser.close()


def test_multi_tenant_access():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://app.workflowpro.com/login")
        page.fill("#email", "user@company2.com")
        page.fill("#password", "password123")
        page.click("#login-btn")
        # ISSUE: cards captured too early -> empty list -> FALSE POSITIVE
        projects = page.locator(".project-card").all()
        for project in projects:
            assert "Company2" in project.text_content()
        browser.close()