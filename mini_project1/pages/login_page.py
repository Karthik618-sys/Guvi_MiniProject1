from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
import time


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email.form-control")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password.form-control")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a#login-btn.btn.login-btn")
    PROFILE_IMG = (By.CSS_SELECTOR, "img.avatar_banner")
    SIGNOUT_BUTTON = (By.XPATH, "//div[@id='dropdown_contents' and text()='Sign Out']")
    ERROR_MESSAGE = (By.CLASS_NAME, "invalid-feedback")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 20)

    def login(self, email, password):
        try:
            time.sleep(2)
            # Fill email
            email_field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
            email_field.clear()
            time.sleep(1)
            email_field.send_keys(email)

            # Fill password
            password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(password)

            # Click login
            time.sleep(1)
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            self.driver.execute_script("arguments[0].click();", login_btn)
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False

    def logout(self):
        try:
            time.sleep(3)  # Wait for page load after login
            # Click profile image
            profile = self.wait.until(EC.presence_of_element_located(self.PROFILE_IMG))
            self.driver.execute_script("arguments[0].click();", profile)
            time.sleep(2)  # Wait for dropdown

            # Click sign out
            signout = self.wait.until(EC.presence_of_element_located(self.SIGNOUT_BUTTON))
            self.driver.execute_script("arguments[0].click();", signout)
            time.sleep(2)  # Wait for logout
            return True
        except Exception as e:
            print(f"Logout error: {str(e)}")
            return False

    def get_error_message(self):
        try:
            time.sleep(2)
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception as e:
            print(f"Error message not found: {str(e)}")
            return None

    def is_logged_in(self):
        try:
            return self.is_visible(self.PROFILE_IMG)
        except:
            return False

    def wait_for_login_form(self):
        try:
            return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.PASSWORD_INPUT)
        except:
            return False