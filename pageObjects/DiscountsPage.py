import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DiscountsPage:

    # Navigation — using direct URL is more reliable
    discounts_url = "https://admin-demo.nopcommerce.com/Admin/Discount/List"

    # Search Locators
    search_discount_name = (By.ID, "SearchDiscountName")
    search_discount_type = (By.ID, "SearchDiscountTypeId")
    search_button = (By.ID, "search-discounts")

    # Results Table
    no_data_message = (By.XPATH, "//*[contains(text(), 'No data available in table')]")
    data_rows = (By.XPATH, "//table[@id='discounts-grid']//tbody/tr[count(td) > 1]")
    edit_buttons = (By.XPATH, "//table[@id='discounts-grid']//tbody//a[contains(text(),'Edit')]")

    # Add New Discount
    add_new_button = (By.XPATH, "//a[contains(@href,'/Admin/Discount/Create')]")

    # Discount Form Fields
    discount_name = (By.ID, "Name")
    discount_type = (By.ID, "DiscountTypeId")
    use_percentage = (By.ID, "UsePercentage")
    discount_percentage = (By.ID, "DiscountPercentage")
    discount_amount = (By.ID, "DiscountAmount")
    use_coupon_code = (By.ID, "RequiresCouponCode")
    coupon_code = (By.ID, "CouponCode")
    save_button = (By.NAME, "save")

    # Success/Error Messages
    success_message = (By.XPATH, "//div[contains(@class,'alert-success')]")
    error_message = (By.XPATH, "//div[contains(@class,'alert-danger')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_discounts(self):
        """Navigate directly to Discounts page via URL"""
        self.driver.get(self.discounts_url)
        # Wait until search field is visible before proceeding
        self.wait.until(
            EC.presence_of_element_located(self.search_discount_name)
        )
        time.sleep(1)

    def search_by_name(self, name):
        """Search discount by name"""
        search_input = self.wait.until(
            EC.presence_of_element_located(self.search_discount_name)
        )
        search_input.clear()
        search_input.send_keys(name)
        self.driver.find_element(*self.search_button).click()
        time.sleep(2)

    def search_by_type(self, discount_type):
        """Search discount by type"""
        dropdown = Select(
            self.wait.until(
                EC.presence_of_element_located(self.search_discount_type)
            )
        )
        dropdown.select_by_visible_text(discount_type)
        self.driver.find_element(*self.search_button).click()
        time.sleep(2)

    def get_result_count(self):
        """Get number of results in table"""
        try:
            rows = self.driver.find_elements(*self.data_rows)
            return len(rows)
        except:
            return 0

    def has_no_data(self):
        """Check if table shows no data message"""
        try:
            elements = self.driver.find_elements(*self.no_data_message)
            for elem in elements:
                if elem.is_displayed():
                    return True
            return False
        except:
            return False

    def add_new_discount(self, name, disc_type="Assigned to order total",
                         percentage=True, amount=10,
                         use_coupon=True, coupon="SAVE10"):
        """Add a new discount"""
        self.wait.until(
            EC.element_to_be_clickable(self.add_new_button)
        ).click()
        time.sleep(1)

        # Enter name
        name_field = self.wait.until(
            EC.presence_of_element_located(self.discount_name)
        )
        name_field.clear()
        name_field.send_keys(name)

        # Select discount type
        type_dropdown = Select(
            self.driver.find_element(*self.discount_type)
        )
        type_dropdown.select_by_visible_text(disc_type)
        time.sleep(1)

        # Set percentage or amount
        if percentage:
            use_pct = self.driver.find_element(*self.use_percentage)
            if not use_pct.is_selected():
                use_pct.click()
            time.sleep(0.5)
            pct_field = self.driver.find_element(*self.discount_percentage)
            pct_field.clear()
            pct_field.send_keys(str(amount))
        else:
            amt_field = self.driver.find_element(*self.discount_amount)
            amt_field.clear()
            amt_field.send_keys(str(amount))

        # Set coupon code
        if use_coupon:
            coupon_checkbox = self.driver.find_element(*self.use_coupon_code)
            if not coupon_checkbox.is_selected():
                coupon_checkbox.click()
            time.sleep(0.5)
            coupon_field = self.driver.find_element(*self.coupon_code)
            coupon_field.clear()
            coupon_field.send_keys(coupon)

        # Save
        self.driver.find_element(*self.save_button).click()
        time.sleep(2)

    def is_success_message_displayed(self):
        """Check if success message is shown"""
        try:
            msg = self.wait.until(
                EC.presence_of_element_located(self.success_message)
            )
            return msg.is_displayed()
        except:
            return False