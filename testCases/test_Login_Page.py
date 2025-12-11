import selenium
from selenium import webdriver
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pageObjects.Login_Page import LoginPage
import time
from selenium.webdriver.common.by import By

@pytest.mark.order(1)
@pytest.mark.usefixtures("setup")
class Test_loginPage:

    #baseurl="https://admin-demo.nopcommerce.com/login?returnUrl=%2Fadmin%2F"

    #Test case to check the Title of the page
    def test_001_titleCheck(self,setup):
        print("Test case to check the Title of the page")
        self.driver=setup
        #self.driver.get(self.baseurl)
        actual_title =self.driver.title
        if actual_title == "nopCommerce demo store. Login":
            print("Test_001_titleCheck Passed")
            assert True
            self.driver.save_screenshot(".\\Screenshots\\"+"titlecheck.png")

        else:
            print("Test_001_titleCheck Failed")
            assert False

    #Testcase to check login with valid credentials :valid username, invalid password
    def test_002_invalid_loginCheck(self,login_setup):
        print("#Testcase to check login with invalid credentials :valid username, invalid password")
        username = "admin@yourstore.com"
        password = "ad"
        self.lp=login_setup
        self.lp.username_fn(username)
        self.lp.password_fn(password)
        self.lp.login_fn()
        #waiting for error to appear
        time.sleep(5)
        error=self.lp.falied_login()
        if error:
            print("Test_003_invalid_loginCheck Passed - Error msg is displayed")
            assert True
        else:
            print("Test_003_invalid_loginCheck Failed - No error")
            assert False

    def test_003_invalid_loginCheck(self,login_setup):
        print("#Testcase to check login with invalid credentials :invalid username, valid password")
        username = "jisha"
        password = "ad"
        self.lp=login_setup
        self.lp.username_fn(username)
        self.lp.password_fn(password)
        self.lp.login_fn()
        error_msg = self.lp.driver.find_element(By.ID, "Email-error")
        if error_msg.text == "Please enter a valid email address.":
            print("Test004 passed")
            assert True
        else:
            print("Test004 failed, accepting invalid email")
            assert False
    def test_004_invalid_loginCheck(self,login_setup):
        print("Testcase to check login with blank username and password")
        username = ""
        password = ""
        self.lp = login_setup
        self.lp.username_fn(username)
        self.lp.password_fn(password)
        self.lp.login_fn()
        error_msg = self.lp.driver.find_element(By.ID, "Email-error")
        if error_msg.text == "Please enter your email":
            print("Test005 passed")
            assert True
        else:
            print("Test004 failed, accepting invalid email")
            assert False

    #Testcase to check login with valid credentials
    def test_005_valid_loginCheck(self,login_setup):
        print("#Testcase to check login with valid credentials")
        username = "admin@yourstore.com"
        password = "admin"
        self.lp=login_setup
        #self.driver.get(self.baseurl)
        #self.lp=LoginPage(self.driver)
        self.lp.username_fn(username)
        self.lp.password_fn(password)
        self.lp.login_fn()
        self.lp.alert_check()
        print("Test_002_valid_loginCheck Passed")
        assert True

    def test_006_logout(self,login_setup):
        username = "admin@yourstore.com"
        password = "admin"
        self.lp = login_setup
        # self.driver.get(self.baseurl)
        # self.lp=LoginPage(self.driver)
        self.lp.username_fn(username)
        self.lp.password_fn(password)
        self.lp.login_fn()
        self.lp.alert_check()
        self.lp.driver.find_element(By.XPATH,"//a[normalize-space()='Logout']").click()
        actual_title = self.lp.driver.title
        if actual_title == "nopCommerce demo store. Login":
            print("Test_006_Logout Passed")
            assert True
        else:
            print("Test_006_Logout Failed")
            assert False























