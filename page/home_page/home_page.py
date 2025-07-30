from page.home_page.locator import Locator
from infra.playwright_driver import PlaywrightDriver


class HomePage:

    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver

    def click_signup_login_href(self):
        self.driver.goto(url=self.locator.ENTER_HOMPAGE_URL)
        self.driver.click(selector=self.locator.SIGN_IN_OR_SIGN_UP_HYPERLINK)
