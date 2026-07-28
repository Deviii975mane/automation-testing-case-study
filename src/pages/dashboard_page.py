"""Dashboard Page Object — post-login verification & project cards."""
import re
from playwright.sync_api import expect

from src.pages.base_page import BasePage


class DashboardPage(BasePage):
    WELCOME = ".welcome-message"
    PROJECT_CARD = ".project-card"

    def assert_loaded(self):
        """Verify we're on the dashboard and it has rendered."""
        expect(self.page).to_have_url(re.compile(r".*/dashboard"))
        expect(self.page.locator(self.WELCOME)).to_be_visible()

    def project_cards(self):
        return self.page.locator(self.PROJECT_CARD)

    def assert_project_visible(self, project_name: str):
        card = self.page.locator(self.PROJECT_CARD, has_text=project_name)
        expect(card).to_be_visible()

    def assert_project_not_visible(self, project_name: str):
        """Tenant isolation: project must NOT appear for another tenant."""
        card = self.page.locator(self.PROJECT_CARD, has_text=project_name)
        expect(card).to_have_count(0)

    def assert_all_cards_belong_to(self, tenant_marker: str):
        """Every rendered card must belong to the expected tenant."""
        cards = self.project_cards()
        expect(cards.first).to_be_visible()  # avoid vacuous pass
        count = cards.count()
        assert count > 0, "Expected at least one project card"
        for i in range(count):
            text = cards.nth(i).text_content() or ""
            assert tenant_marker in text, (
                f"Cross-tenant leak in card {i}: {text!r}"
            )