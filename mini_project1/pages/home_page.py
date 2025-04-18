from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class HomePage(BasePage):
    # Locators
    LOGIN_BUTTON = (By.ID, "login-btn")
    SIGNUP_BUTTON = (By.XPATH, "//a[contains(@class, 'bg-green-500') and contains(@href, '/register/')]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_button(self):
        time.sleep(2)  # Wait before clicking
        result = self.click_element(self.LOGIN_BUTTON)
        time.sleep(1)  # Wait after click
        return result

    def click_signup_button(self):
        time.sleep(2)  # Increased wait before clicking
        result = self.click_element(self.SIGNUP_BUTTON)
        time.sleep(2)  # Wait after click for page load
        return result

    def is_login_button_visible(self):
        time.sleep(1)
        return self.is_visible(self.LOGIN_BUTTON)

    def is_signup_button_visible(self):
        time.sleep(1)
        return self.is_visible(self.SIGNUP_BUTTON)

    def get_page_title(self):
        time.sleep(1)  # Wait for title to load
        return self.driver.title

    def navigate_to_signup(self):
        self.click_signup_button()
        time.sleep(2)  # Wait for navigation
        return self.driver.current_url