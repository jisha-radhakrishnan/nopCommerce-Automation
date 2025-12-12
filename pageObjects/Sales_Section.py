import time

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SalesSection:
    order=(By.XPATH,"//a[@href='/Admin/Order/List'][normalize-space()='More info']")
    start_date=(By.ID,"StartDate")
    end_date=(By.ID,"EndDate")
    search=(By.ID,"search-orders")
    Order_statuses=(By.ID,"OrderStatusIds")


    def __init__(self,driver):
        self.driver=driver

    def order_details_fn(self):
        self.driver.find_element(*self.order).click()


    '''def order_search_fn(self):

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
            dropdown.select_by_visible_text("Processing")
            time.sleep(1)
            self.driver.find_element(*self.search).click()
            time.sleep(2)'''

    def order_search_fn(self, start_date="2019-02-03", end_date="2025-12-27", order_status="Processing"):
        """
        Search for orders with specified date range and status.

        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            order_status: Order status to filter (e.g., 'Processing', 'Cancelled')

        Returns:
            dict: {'has_data': bool, 'status_searched': str, 'order_count': int}
        """
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

            # Get the actual selected status from dropdown (to verify)
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
                no_data_elements = self.driver.find_elements(By.XPATH,
                                                             "//*[contains(text(), 'No data available in table')]")
                if len(no_data_elements) > 0:
                    for elem in no_data_elements:
                        if elem.is_displayed():
                            print("  → Found 'No data available in table' message")
                            return False
            except Exception as e:
                print(f"  → Method 1 check failed: {e}")

            # Method 2: Check for "No records" message
            try:
                no_records_elements = self.driver.find_elements(By.XPATH,
                                                                "//*[contains(text(), 'No records')]")
                if len(no_records_elements) > 0:
                    for elem in no_records_elements:
                        if elem.is_displayed():
                            print("  → Found 'No records' message")
                            return False
            except Exception as e:
                print(f"  → Method 2 check failed: {e}")

            # Method 3: Check for checkbox rows (indicates data)
            try:
                checkbox_rows = self.driver.find_elements(By.XPATH,
                                                          "//table//tbody/tr/td/input[@type='checkbox']")
                if len(checkbox_rows) > 0:
                    print(f"  → Found {len(checkbox_rows)} order row(s) with checkboxes")
                    return True
            except Exception as e:
                print(f"  → Method 3 check failed: {e}")

            # Method 4: Check for "View" buttons
            try:
                view_buttons = self.driver.find_elements(By.XPATH,
                                                         "//table//tbody//button[contains(text(), 'View')] | //table//tbody//a[contains(text(), 'View')]")
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
            checkbox_rows = self.driver.find_elements(By.XPATH,
                                                      "//table//tbody/tr/td/input[@type='checkbox']")
            if len(checkbox_rows) > 0:
                return len(checkbox_rows)

            # Fallback: Count data rows
            data_rows = self.driver.find_elements(By.XPATH,
                                                  "//table//tbody/tr[count(td) > 1 and not(contains(., 'No data available'))]")
            return len(data_rows)

        except Exception as e:
            print(f"Error getting order count: {str(e)}")
            return 0