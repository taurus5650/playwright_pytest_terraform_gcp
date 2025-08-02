from page.home_page.locator import Locator
from infra.playwright_driver import PlaywrightDriver


class HomePage:

    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver
        self.locator = Locator()

    def go_to_hompage(self, url: str):
        return self.driver.goto(url=url)

    def click_signup_login_href(self):
        return self.driver.click(selector=self.locator.SIGN_IN_OR_SIGN_UP_HYPERLINK)
