"""
Part 1 — Corrected login tests.
Fixes: auto-waiting, regex URL match, optional 2FA, guaranteed cleanup,
fixed viewport, externalized config, and the multi-tenant false-positive.
"""
import os
import pytest

from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.utils.config_loader import load_environment


@pytest.mark.smoke
@pytest.mark.ui
def test_user_login(page):
    env = load_environment("company1")
    login = LoginPage(page, env["base_url"])
    dashboard = DashboardPage(page, env["base_url"])

    login.login_default("admin@company1.com", env["tenant_id"])

    # expect() auto-waits — no sleep, tolerant URL match
    dashboard.assert_loaded()


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.security
def test_multi_tenant_access(page):
    env = load_environment("company2")
    login = LoginPage(page, env["base_url"])
    dashboard = DashboardPage(page, env["base_url"])

    login.login_default("user@company2.com", env["tenant_id"])

    # Fixes false positive: waits for cards + asserts list is non-empty
    dashboard.assert_all_cards_belong_to(env["tenant_marker"])