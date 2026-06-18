import pytest
import undetected_chromedriver as uc
import selenium
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.Sales_Section import SalesSection
from pageObjects.Login_Page import LoginPage


@pytest.fixture
def setup():
    #driver=uc.Chrome()
    driver = uc.Chrome(version_main=149)
    driver.get("https://admin-demo.nopcommerce.com/login?returnUrl=%2Fadmin%2F")
    #driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    try:
        driver.quit()
    except Exception as e:
        print(f"Warning: driver.quit() raised an exception during teardown: {e}")
    time.sleep(2)

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
    hp=SalesSection(logged_in_driver)
    return hp