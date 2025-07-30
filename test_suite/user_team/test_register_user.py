import time
from datetime import datetime

import allure


from page.home_page.home_page import HomePage
from infra.playwright_driver import PlaywrightDriver
from utils import logger


class TestCase:

    def setup_method(self):
        self.driver = PlaywrightDriver(headless=False)
        self.home = HomePage(driver=self.driver)

    def teardown_method(self):
        self.driver.close_driver()

    @allure.story('New Register User')
    def test_new_register_user(self):
        self.home.click_signup_login_href()
