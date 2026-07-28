"""Driver factory — abstracts local vs BrowserStack, web vs mobile."""
import os
import json
from playwright.sync_api import sync_playwright


def _browserstack_url(caps: dict) -> str:
    user = os.getenv("BROWSERSTACK_USERNAME")
    key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    caps_json = json.dumps(caps)
    return (
        f"wss://cdp.browserstack.com/playwright?"
        f"caps={caps_json}&user={user}&key={key}"
    )


def launch_local(playwright, browser_name: str = "chromium",
                 headless: bool = True):
    """Launch a local browser (chromium/firefox/webkit)."""
    browser_type = getattr(playwright, browser_name)
    return browser_type.launch(headless=headless)


def connect_browserstack(playwright, caps: dict):
    """Connect to a BrowserStack session (web or mobile) via CDP."""
    return playwright.chromium.connect(_browserstack_url(caps))


def get_context(use_browserstack: bool = False, caps: dict | None = None,
                browser_name: str = "chromium", headless: bool = True,
                viewport: dict | None = None):
    """
    Returns (playwright, browser, context). Caller is responsible for
    closing them (or use within a fixture with guaranteed teardown).
    """
    playwright = sync_playwright().start()
    if use_browserstack:
        browser = connect_browserstack(playwright, caps or {})
    else:
        browser = launch_local(playwright, browser_name, headless)
    context = browser.new_context(
        viewport=viewport or {"width": 1280, "height": 800}
    )
    return playwright, browser, context