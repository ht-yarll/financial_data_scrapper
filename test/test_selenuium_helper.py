import pytest

from financial_data_scraper.utils.selenium_helper import SeleniumHelper
from financial_data_scraper.utils.config import load_config

from selenium.webdriver.remote.webdriver import WebDriver

def test_selenium_helper_succesufully_connects():
    config = load_config()
    s = SeleniumHelper(config)
    con = s._init_session()

    assert isinstance(con, WebDriver)

def test_selenium_helper_returns_list_of_tuples():
    config = load_config()
    s = SeleniumHelper(config)
    elements = s.get_monthly_elements()
    limited_elements = elements[:3]

    assert isinstance(limited_elements, list)
    assert all(isinstance(item, tuple) for item in limited_elements)