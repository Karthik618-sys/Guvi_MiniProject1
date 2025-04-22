import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.config import TestData


@pytest.mark.usefixtures("init_driver")
class TestGuvi:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method that runs before each test"""
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.driver.get(TestData.BASE_URL)

    def test_01_verify_homepage_url(self):
        """Test if homepage URL is correct"""
        assert self.driver.current_url == TestData.BASE_URL, "Homepage URL mismatch"

    def test_02_verify_page_title(self):
        """Test if page title is correct"""
        assert self.home_page.get_page_title() == TestData.EXPECTED_TITLE, "Page title mismatch"

    def test_03_verify_login_button_visible(self):
        """Test if login button is visible on homepage"""
        assert self.home_page.is_login_button_visible(), "Login button not visible"

    def test_04_verify_signup_button_visible(self):
        """Test if signup button is visible on homepage"""
        assert self.home_page.is_signup_button_visible(), "Signup button not visible"

    def test_05_verify_signup_navigation(self):
        """Test if signup button navigates to correct page"""
        self.home_page.click_signup_button()
        assert self.driver.current_url == TestData.SIGNUP_URL, "Signup page navigation failed"

    def test_06_verify_valid_login_logout(self):
        """Test valid login and logout functionality"""
        # Navigate to login page
        self.driver.get(TestData.SIGNIN_URL)

        # Perform login
        assert self.login_page.login(
            TestData.VALID_EMAIL,
            TestData.VALID_PASSWORD
        ), "Login failed"

        # Verify login successful
        assert self.login_page.is_logged_in(), "Login verification failed"

        # Perform logout
        assert self.login_page.logout(), "Logout failed"

    def test_07_verify_invalid_login(self):
        """Test invalid login attempt"""
        # Navigate to login page
        self.driver.get(TestData.SIGNIN_URL)

        # Attempt invalid login
        self.login_page.login(
            TestData.INVALID_EMAIL,
            TestData.INVALID_PASSWORD
        )

        # Verify error message appears
        error_msg = self.login_page.get_error_message()
        assert error_msg is not None, "Error message not displayed for invalid login"