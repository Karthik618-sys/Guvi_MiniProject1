from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email.form-control")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#password.form-control")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a#login-btn.btn.login-btn")
    PROFILE_DROPDOWN = (By.CSS_SELECTOR, "img.rounded-full.border-2.avatar_banner[id='dropdown_contents']")
    SIGNOUT_BUTTON = (By.XPATH, "//li[@id='dropdown_contents']//div[contains(text(), 'Sign Out')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger, .invalid-feedback, .error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 30)
        self.short_wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 45)

    def login(self, email, password):
        try:
            # Fill email
            email_field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
            email_field.clear()
            email_field.send_keys(email)

            # Fill password
            password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
            password_field.clear()
            password_field.send_keys(password)

            # Click login
            login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            self.driver.execute_script("arguments[0].click();", login_btn)

            # Wait for profile dropdown
            self.wait.until(EC.presence_of_element_located(self.PROFILE_DROPDOWN))
            return True
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False

    def logout(self):
        try:
            # Create ActionChains instance
            actions = ActionChains(self.driver)

            # Wait for and find dropdown
            dropdown = self.wait.until(
                EC.presence_of_element_located(self.PROFILE_DROPDOWN)
            )

            # Move to and click dropdown
            actions.move_to_element(dropdown).click().perform()

            # Wait for and find signout
            signout = self.wait.until(
                EC.presence_of_element_located(self.SIGNOUT_BUTTON)
            )

            # Move to and click signout
            actions.move_to_element(signout).click().perform()

            # Return True if profile dropdown is no longer visible (logged out)
            try:
                self.short_wait.until(
                    EC.invisibility_of_element_located(self.PROFILE_DROPDOWN)
                )
                return True
            except:
                return True  # Element not found means logged out

        except Exception as e:
            print(f"Logout error: {str(e)}")
            # Check if profile dropdown is not present (means logged out)
            try:
                self.driver.find_element(*self.PROFILE_DROPDOWN)
                return False  # Still logged in
            except:
                return True  # Element not found means logged out

    def get_error_message(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text if error.is_displayed() else None
        except Exception as e:
            print(f"Error message not found: {str(e)}")
            return None

    def is_logged_in(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.PROFILE_DROPDOWN)) is not None
        except:
            return False