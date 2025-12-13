import pytest


@pytest.mark.order(2)
class Test_HomePage:
    def test_007_order_titlecheck(self,homepage_setup):
        print("Testcase to order details")
        self.hp = homepage_setup
        self.hp.order_details_fn()
        self.hp.driver.implicitly_wait(3)
        actual_title = self.hp.driver.title
        print("Actual title is:", actual_title)

        if actual_title == "Orders / nopCommerce administration":
            print("Test_006_titleCheck Passed")
            assert True
            self.hp.driver.save_screenshot(".\\Screenshots\\" + "Order_deatils_titlecheck.png")
        else:
            print("Test_006_titleCheck Failed")
            assert False

    def test_008_search_order(self,homepage_setup):
            """Test order search with Processing status"""
            self.hp = homepage_setup
            self.hp.order_details_fn()  # Navigate to orders page
            self.hp.driver.implicitly_wait(2)

            # Search for Processing orders
            result = self.hp.order_search_fn(
                start_date="2019-02-03",
                end_date="2025-12-27",
                order_status="Processing"
            )
            assert result['has_data'] == True, "Expected to find Processing orders"
            assert result['order_count'] > 0, f"Expected orders > 0, got {result['order_count']}"
            print(f"✓ Test Passed: Found {result['order_count']} Processing orders")


    def test_009_search_cancelled_orders(self, homepage_setup):
        """Test order search with Cancelled status - expecting no data"""
        self.hp = homepage_setup
        self.hp.order_details_fn()  # Navigate to orders page
        self.hp.driver.implicitly_wait(2)

        # Search for Cancelled orders
        result = self.hp.order_search_fn(
            start_date="2019-02-03",
            end_date="2025-12-27",
            order_status="Cancelled"
        )

        # Verify results - expecting no data
        print(f"Cancelled orders search result: {result}")

        if not result['has_data']:
            print("✓ Test Passed: No Cancelled orders found (as expected)")
            assert result['order_count'] == 0, "Order count should be 0"
        else:
            print(f"⚠ Warning: Found {result['order_count']} Cancelled orders")

        # Take screenshot
        self.hp.driver.save_screenshot(".\\Screenshots\\" + "search_cancelled_orders.png")

    def test_010_search_multiple_statuses(self, homepage_setup):
        """Test searching for orders with different statuses"""
        self.hp = homepage_setup
        self.hp.order_details_fn()  # Navigate to orders page
        self.hp.driver.implicitly_wait(2)

        # Test different order statuses
        statuses_to_test = ["Processing", "Cancelled", "Complete", "Pending"]
        results = {}

        for status in statuses_to_test:
            print(f"\n{'=' * 60}")
            print(f"Searching for {status} orders...")
            print('=' * 60)

            result = self.hp.order_search_fn(
                start_date="2019-02-03",
                end_date="2025-12-27",
                order_status=status
            )

            results[status] = result

            # Take screenshot for each status
            self.hp.driver.save_screenshot(f".\\Screenshots\\search_{status.lower()}_orders.png")

        # Print summary
        print(f"\n{'=' * 60}")
        print("SEARCH RESULTS SUMMARY")
        print('=' * 60)
        for status, result in results.items():
            if result['has_data']:
                print(f"{status:15} : {result['order_count']} order(s) found")
            else:
                print(f"{status:15} : No data available")
        print('=' * 60)

    def test_011_export_pending_order(self, homepage_setup):
        """Export Pending order to Excel"""
        self.hp = homepage_setup
        self.hp.order_details_fn()
        result = self.hp.order_search_fn(start_date = "2019-02-03",end_date = "2025-12-27", order_status = "Processing")

        # Select first order and export
        assert result['has_data'] == True
        self.hp.select_first_order()
        self.hp.export_selected_to_excel()

    def test_012_text_hover(self, homepage_setup):
        self.hp = homepage_setup
        self.hp.order_details_fn()
        print("Hover Text is",self.hp.text_hover_check())

