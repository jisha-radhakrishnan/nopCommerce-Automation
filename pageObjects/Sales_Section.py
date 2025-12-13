import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SalesSection:
    # Navigation and Search Locators
    order=(By.XPATH,"//a[@href='/Admin/Order/List'][normalize-space()='More info']")
    start_date=(By.ID,"StartDate")
    end_date=(By.ID,"EndDate")
    search=(By.ID,"search-orders")
    Order_statuses=(By.ID,"OrderStatusIds")

    # Table Data Verification Locators
    checkbox_rows=(By.XPATH,"//table//tbody/tr/td/input[@type='checkbox']")
    no_data_message=(By.XPATH,"//*[contains(text(), 'No data available in table')]")
    no_records_message=(By.XPATH,"//*[contains(text(), 'No records')]")
    data_rows=(By.XPATH,"//table//tbody/tr[count(td) > 1 and not(contains(., 'No data available'))]")
    view_buttons=(By.XPATH,"//table//tbody//button[contains(text(), 'View')] | //table//tbody//a[contains(text(), 'View')]")

    # Export Locators
    first_order_checkbox = (By.XPATH, "//table//tbody/tr[1]/td/input[@type='checkbox']")
    export_button = (By.XPATH, "//button[@class='btn btn-success dropdown-toggle dropdown-icon']")
    export_to_excel=(By.XPATH, "//button[@id='exportexcel-selected']")

    element_locator= (By.XPATH,"//div[@class='ico-help']")

    def __init__(self,driver):
        self.driver=driver

    def order_details_fn(self):
        self.driver.find_element(*self.order).click()


    def order_search_fn(self, start_date="2019-02-03", end_date="2025-12-27", order_status="Processing"):

        try:
            # Set start date
            self.driver.execute_script(
                f"document.getElementById('StartDate').value = '{start_date}';")
            self.driver.execute_script(
                "document.getElementById('StartDate').dispatchEvent(new Event('change'));")

            # Set end date
            self.driver.execute_script(
                f"document.getElementById('EndDate').value = '{end_date}';")
            self.driver.execute_script(
                "document.getElementById('EndDate').dispatchEvent(new Event('change'));")

            # Select order status from dropdown
            dropdown = Select(self.driver.find_element(*self.Order_statuses))
            dropdown.select_by_visible_text(order_status)
            time.sleep(1)

            # Click search button
            self.driver.find_element(*self.search).click()
            time.sleep(2)

            # Get the actual selected status from dropdown
            selected_status = dropdown.first_selected_option.text

            # Check if data is available in the table
            has_data = self.check_table_data()
            order_count = 0

            if has_data:
                order_count = self.get_order_count()
                print(f"✓ Search Results: Data found for status '{selected_status}' - {order_count} order(s)")
            else:
                print(f"✗ Search Results: No data available for status '{selected_status}'")

            return {
                'has_data': has_data,
                'status_searched': selected_status,
                'order_count': order_count
            }

        except Exception as e:
            print(f"Error during order search: {str(e)}")
            return {
                'has_data': False,
                'status_searched': order_status,
                'order_count': 0,
                'error': str(e)
            }

    def check_table_data(self):
        """
        Check if the orders table contains data or shows "No data available"

        Returns:
            bool: True if table has data, False if empty
        """
        try:
            time.sleep(1)

            # Method 1: Check for "No data available in table" message
            try:
                no_data_elements = self.driver.find_elements(*self.no_data_message)
                if len(no_data_elements) > 0:
                    for elem in no_data_elements:
                        if elem.is_displayed():
                            print("  → Found 'No data available in table' message")
                            return False
            except Exception as e:
                print(f"  → Method 1 check failed: {e}")

            # Method 2: Check for "No records" message
            try:
                no_records_elements = self.driver.find_elements(*self.no_records_message)
                if len(no_records_elements) > 0:
                    for elem in no_records_elements:
                        if elem.is_displayed():
                            print("  → Found 'No records' message")
                            return False
            except Exception as e:
                print(f"  → Method 2 check failed: {e}")

            # Method 3: Check for checkbox rows (indicates data)
            try:
                checkbox_rows = self.driver.find_elements(*self.checkbox_rows)
                if len(checkbox_rows) > 0:
                    print(f"  → Found {len(checkbox_rows)} order row(s) with checkboxes")
                    return True
            except Exception as e:
                print(f"  → Method 3 check failed: {e}")

            # Method 4: Check for "View" buttons
            try:
                view_buttons = self.driver.find_elements(*self.view_buttons)
                if len(view_buttons) > 0:
                    print(f"  → Found {len(view_buttons)} 'View' button(s)")
                    return True
            except Exception as e:
                print(f"  → Method 4 check failed: {e}")

            # If no data found
            print("  → No data detected by any method")
            return False

        except Exception as e:
            print(f"Error checking table data: {str(e)}")
            return False

    def get_order_count(self):
        """
        Get the count of orders in the search results

        Returns:
            int: Number of orders found
        """
        try:
            # Count checkbox rows (most reliable)
            checkbox_rows = self.driver.find_elements(*self.checkbox_rows)
            if len(checkbox_rows) > 0:
                return len(checkbox_rows)

            # Fallback: Count data rows
            data_rows = self.driver.find_elements(*self.data_rows)
            return len(data_rows)

        except Exception as e:
            print(f"Error getting order count: {str(e)}")
            return 0

    def select_first_order(self):
        """Select the first order checkbox"""
        self.driver.find_element(*self.first_order_checkbox).click()
        time.sleep(0.5)

    def export_selected_to_excel(self):
        """Click export to Excel button"""
        self.driver.find_element(*self.export_button).click()
        self.driver.find_element(*self.export_to_excel).click()
        time.sleep(2)
    def text_hover_check(self):
        """Using ActionChains to hover over element"""
        element = self.driver.find_element(*self.element_locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        hover_text=element.get_attribute("data-original-title")
        return hover_text
