import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestLogin:
    
    @pytest.fixture
    def driver(self):
        """Set up Chrome driver with headless mode for CI/CD."""
        chrome_options = Options()
        
        # Check if running in GitHub Actions
        if os.getenv("CI") == "true":
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        yield driver
        driver.quit()
    
    def test_valid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        home_page = HomePage(driver)
        assert home_page.is_logged_in() == True
    
    def test_invalid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login("invalid_user", "wrong_password")
        error = login_page.get_error_message()
        assert "Username and password do not match" in error