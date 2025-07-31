import allure

from infra.playwright_driver import PlaywrightDriver
from page.home_page.page import HomePage
from page.login_page.page import LoginPage


class TestCase:

    def setup_method(self):
        self.driver = PlaywrightDriver(headless=True)
        self.home = HomePage(driver=self.driver)
        self.login = LoginPage(driver=self.driver)

    def teardown_method(self):
        self.driver.close_driver()

    @allure.story('New Register User')
    def test_new_register_user(self):
        for_loop_max = 180
        expected_homepage_title = "Automation Exercise"
        expected_sign_up_form_text = "New User Signup!"

        # region __Step1. Navigate to url
        actual_homepage_title = self.home.go_to_hompage()
        # endregion __Step1. Navigate to url

        # region __Step2. Verify that home page is visible successfully
        assert expected_homepage_title in actual_homepage_title.title()
        # endregion __Step2. Verify that home page is visible successfully

        # region __Step3. Click on 'Signup / Login' button
        self.home.click_signup_login_href()
        # region __Step3. Click on 'Signup / Login' button

        # region __Step4. Verify 'New User Signup!' is visible
        actual_sign_up_form_text = self.login.inner_text_signin_or_signup_h2()
        assert actual_sign_up_form_text == expected_sign_up_form_text
        # endregion __Step4. Verify 'New User Signup!' is visible
