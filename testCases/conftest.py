import pytest
import undetected_chromedriver as uc
import selenium
from selenium import webdriver

from pageObjects.Sales_Section import HomePage
from pageObjects.Login_Page import LoginPage


@pytest.fixture
def setup():
    driver=uc.Chrome()
    driver.get("https://admin-demo.nopcommerce.com/login?returnUrl=%2Fadmin%2F")
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(setup):
    driver = setup
    lp = LoginPage(driver)
    lp.username_fn("admin@yourstore.com")
    lp.password_fn("admin")
    lp.login_fn()
    return driver

@pytest.fixture
def login_setup(setup):
    driver=setup
    driver.implicitly_wait(5)
    lp=LoginPage(driver)
    return lp

@pytest.fixture
def homepage_setup(logged_in_driver):
    hp=HomePage(logged_in_driver)
    return hp