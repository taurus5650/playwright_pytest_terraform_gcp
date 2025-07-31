import allure

from infra.playwright_driver import PlaywrightDriver
from page.home_page.home_page import HomePage


class TestCase:

    def setup_method(self):
        self.driver = PlaywrightDriver(headless=True)
        self.home = HomePage(driver=self.driver)

    def teardown_method(self):
        self.driver.close_driver()

    @allure.story('New Register User')
    def test_new_register_user(self):
        for_loop_max = 180
        expected_homepage_title = "Automation Exercise"

        # region __Step1. Navigate to url
        actual_homepage_title = self.home.go_to_hompage()
        # endregion __Step1. Navigate to url

        assert expected_homepage_title in actual_homepage_title.title()

        # region __Step2. Click on 'Signup / Login' button
        self.home.click_signup_login_href()
        # region __Step2. Click on 'Signup / Login' button


