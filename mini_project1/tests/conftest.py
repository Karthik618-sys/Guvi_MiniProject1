import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import TestData


@pytest.fixture(scope="class")
def init_driver(request):
    if TestData.BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    request.cls.driver = driver
    yield
    driver.quit()