from datetime import datetime

import allure

from infra.playwright_driver import PlaywrightDriver
from page.home_page.page import HomePage
from page.login_page.page import LoginPage
from page.signup_page.page import SignupPage


class TestCase:

    def setup_method(self):
        self.driver = PlaywrightDriver(headless=True)
        self.home = HomePage(driver=self.driver)
        self.login = LoginPage(driver=self.driver)
        self.signup = SignupPage(driver=self.driver)

    def teardown_method(self):
        self.driver.close_driver()

    @allure.story('New Register User')
    def test_new_register_user(self):
        current_time = datetime.now()
        for_loop_max = 180
        expected_homepage_title = 'Automation Exercise'
        expected_sign_up_form_text = 'New User Signup!'
        name = f'automation_{current_time.strftime("%Y%m%d%H%M%S")}'
        sign_up_email = f'{current_time.strftime("%Y%m%d%H%M%S")}@automation.com'
        expected_enter_account_info_text = 'ENTER ACCOUNT INFORMATION'
        password = '1234567890'
        address = '24th Floor, Dr. S.P.M. Civic Centre, Minto Road, New Delhi, India.'
        state = 'Minto Road'
        city = 'New Delhi'
        zipcode = '100002'
        mobile_number = '155305'
        expected_account_created_text = 'ACCOUNT CREATED!'

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

        # region __Step5. Enter name and email address
        self.login.fill_sign_up_name(value=name)
        self.login.fill_sign_up_email(value=sign_up_email)
        # endregion __Step5. Enter name and email address

        # region __Step6. Click 'Signup' button
        self.login.click_sign_up_btn()
        # endregion __Step6. Click 'Signup' button

        # region __Step7. Verify that 'ENTER ACCOUNT INFORMATION' is visible
        actual_enter_account_info = self.signup.inner_text_enter_account_info()
        assert actual_enter_account_info == expected_enter_account_info_text
        # endregion __Step7. Verify that 'ENTER ACCOUNT INFORMATION' is visible

        # region __Step8. Fill details: Title, Name, Email, Password, Date of birth
        self.signup.click_title_gender_radio()
        # endregion __Step8. Fill details: Title, Name, Email, Password, Date of birth
