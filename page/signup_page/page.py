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

    def fill_password(self, value: str):
        return self.driver.fill(selector=self.locator.PASSWORD, value=value)

    def select_date_of_birth_dropdown_list_date(self, value: str):
        return self.driver.select_option_with_value(selector=self.locator.DATE_OF_BIRTH_DROPDOWN_DAYS, value=value)

    def select_date_of_birth_dropdown_list_month(self, value: str):
        return self.driver.select_option_with_value(selector=self.locator.DATE_OF_BIRTH_DROPDOWN_MONTHS, value=value)

    def select_date_of_birth_dropdown_list_year(self, value: str):
        return self.driver.select_option_with_value(selector=self.locator.DATE_OF_BIRTH_DROPDOWN_YEARS, value=value)

