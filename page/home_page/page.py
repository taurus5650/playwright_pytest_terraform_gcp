from infra.config import get_env_config
from infra.playwright_driver import PlaywrightDriver
from page.home_page.locator import Locator


class HomePage:

    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver
        self.locator = Locator()
        self.base_url = get_env_config().get_single_key('HOMEPAGE', 'WEB_BASE_URL')

    def go_to_hompage(self):
        return self.driver.goto(url=self.base_url)

    def click_signup_login_href(self):
        return self.driver.click(selector=self.locator.SIGN_IN_OR_SIGN_UP_HYPERLINK)
