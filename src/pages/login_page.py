"""Login Page Object — handles authentication incl. optional 2FA."""
import os
from playwright.sync_api import expect, TimeoutError as PWTimeout

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = "#email"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-btn"
    OTP_FIELD = "#otp-code"
    VERIFY_BTN = "#verify-btn"

    def login(self, email: str, password: str, otp: str | None = None):
        """Perform login, handling dynamic loading and optional 2FA."""
        self.open("login")

        expect(self.page.locator(self.EMAIL)).to_be_visible()
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

        # Optional 2FA — some users have it, some don't
        otp_field = self.page.locator(self.OTP_FIELD)
        try:
            otp_field.wait_for(state="visible", timeout=3000)
            if otp:
                otp_field.fill(otp)
                self.click(self.VERIFY_BTN)
        except PWTimeout:
            pass  # No 2FA for this user — continue

    def login_default(self, email: str, tenant_id: str):
        """Convenience login using env-provided password/OTP."""
        password = os.getenv("TEST_PASSWORD", "password123")
        otp = os.getenv(f"OTP_{tenant_id}")
        self.login(email, password, otp)