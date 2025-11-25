import pytest
import undetected_chromedriver as uc
import selenium
from selenium import webdriver

from pageObjects.Login_Page import LoginPage


@pytest.fixture
def setup():
    driver = uc.Chrome()
    driver.get("https://admin-demo.nopcommerce.com/login?returnUrl=%2Fadmin%2F")
    driver.maximize_window()

    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def login_setup(setup):
    driver=setup
    driver.implicitly_wait(5)
    lp=LoginPage(driver)
    return lp
