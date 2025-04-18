import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.config import TestData

@pytest.mark.usefixtures("init_driver")
class TestGuvi:
    def test_valid_url(self):
        self.driver.get(TestData.BASE_URL)
        assert self.driver.current_url == TestData.BASE_URL

    def test_page_title(self):
        home_page = HomePage(self.driver)
        assert home_page.get_page_title() == TestData.EXPECTED_TITLE

    def test_login_button(self):
        home_page = HomePage(self.driver)
        assert home_page.is_login_button_visible()

    def test_valid_login_logout(self):
        self.driver.get(TestData.SIGNIN_URL)
        login_page = LoginPage(self.driver)
        login_page.login(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
        assert login_page.logout()

    def test_invalid_login(self):
        self.driver.get(TestData.SIGNIN_URL)
        login_page = LoginPage(self.driver)
        login_page.login(TestData.INVALID_EMAIL, TestData.INVALID_PASSWORD)
        assert login_page.get_error_message() is not None

    def test_signup_button(self):
        self.driver.get(TestData.BASE_URL)  # Return to main page
        home_page = HomePage(self.driver)
        assert home_page.is_signup_button_visible()

    def test_signup_page(self):
        home_page = HomePage(self.driver)
        home_page.click_signup_button()
        assert self.driver.current_url == TestData.SIGNUP_URL