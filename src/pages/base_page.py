"""Base Page Object — common actions shared by all pages."""
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self, path: str = ""):
        """Navigate to a path relative to the tenant base URL."""
        url = f"{self.base_url}/{path}".rstrip("/")
        self.page.goto(url, wait_until="domcontentloaded")

    def click(self, selector: str):
        """Click with Playwright's built-in auto-waiting."""
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Wait for visibility; returns bool without raising."""
        try:
            expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
            return True
        except AssertionError:
            return False

    def screenshot(self, name: str):
        """Capture a screenshot (attach to report on failure)."""
        self.page.screenshot(path=f"reports/{name}.png")