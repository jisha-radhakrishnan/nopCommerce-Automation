import time
from telnetlib import EC

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class HomePage:
    order=(By.XPATH,"//a[@href='/Admin/Order/List'][normalize-space()='More info']")
    start_date=(By.ID,"StartDate")
    end_date=(By.ID,"EndDate")
    search=(By.ID,"search-orders")
    Order_statuses=(By.ID,"OrderStatusIds")


    def __init__(self,driver):
        self.driver=driver

    def order_details_fn(self):
        self.driver.find_element(*self.order).click()
    def order_search_fn(self):

            self.driver.execute_script(
                "document.getElementById('StartDate').value = '2019-02-03';")
            self.driver.execute_script(
                "document.getElementById('EndDate').value = '2025-12-27';")
            # Trigger change events to ensure the calendar widget recognizes the change
            self.driver.execute_script(
                "document.getElementById('StartDate').dispatchEvent(new Event('change'));")
            self.driver.execute_script(
                "document.getElementById('EndDate').dispatchEvent(new Event('change'));")
            # Small delay to ensure values are set
            dropdown=Select(self.driver.find_element(*self.Order_statuses))
            dropdown.select_by_visible_text("Cancelled")
            time.sleep(1)
            self.driver.find_element(*self.search).click()
            time.sleep(2)

