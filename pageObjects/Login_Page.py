import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginPage:

    #Locators:
    username_locator = (By.ID,"Email")
    password_locator = (By.ID,"Password")
    login_locator = (By.XPATH,"//button[@type='submit']")
    failed_login_locator = (By.XPATH,"//div[@class='message-error validation-summary-errors']")

    def __init__(self,driver):
        self.driver=driver

    def username_fn(self,username):
        self.driver.find_element(*self.username_locator).clear()
        self.driver.find_element(*self.username_locator).send_keys(username)
    def password_fn(self,password):
        self.driver.find_element(*self.password_locator).clear()
        self.driver.find_element(*self.password_locator).send_keys(password)
    def login_fn(self):
        self.driver.find_element(*self.login_locator).click()
    def alert_check(self):
        try:
            alert=self.driver.switch_to.alert
            alert_text=alert.text
            alert.accept()
            print("Alert accepted successfully")
        except Exception as e:
            print("No alert appeared",e)
    def falied_login(self):
        error_element=self.driver.find_element(*self.failed_login_locator)
        return error_element.is_displayed()

