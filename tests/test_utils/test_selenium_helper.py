import pytest

from app.utils.selenium_helper import SeleniumHelper
from app.utils.config import load_config

from selenium.webdriver.remote.webdriver import WebDriver

def test_selenium_remote_connection():
    config = load_config()
    helper = SeleniumHelper(config['urls']['usd_currency'])  # Passe uma URL real de teste
    driver = helper.driver

    assert isinstance(driver, WebDriver)

    driver.get("https://www.google.com")
    assert "Google" in driver.title

    search_box = driver.find_element("name", "q")
    assert search_box is not None

    driver.quit()