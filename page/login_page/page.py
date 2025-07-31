from page.login_page.locator import Locator
from infra.playwright_driver import PlaywrightDriver


class LoginPage:

    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver
        self.locator = Locator()

    def inner_text_signin_or_signup_h2(self) -> str:
        return self.driver.inner_text(self.locator.SIGN_IN_OR_SIGN_UP_PAGE_H2)