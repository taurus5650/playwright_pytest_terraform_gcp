from page.signup_page.locator import Locator
from infra.playwright_driver import PlaywrightDriver


class SignupPage:

    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver
        self.locator = Locator()


    def inner_text_enter_account_info(self):
        return self.driver.inner_text(selector=self.locator.ENTER_ACCOUNT_INFO_TEXT)

    def click_title_gender_radio(self):
        return self.driver.checkbox_or_radio(selector=self.locator.ID_GENDER_1)