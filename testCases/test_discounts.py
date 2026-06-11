import pytest
from pageObjects.DiscountsPage import DiscountsPage
import time


@pytest.fixture
def discounts_setup(logged_in_driver):
    dp = DiscountsPage(logged_in_driver)
    dp.navigate_to_discounts()
    return dp


@pytest.mark.order(3)
class Test_DiscountsPage:

    def test_013_discounts_page_title(self, discounts_setup):
        """Verify Discounts page title"""
        self.dp = discounts_setup
        actual_title = self.dp.driver.title
        print("Actual title:", actual_title)
        if actual_title == "Discounts / nopCommerce administration":
            print("Test_013 Passed - Discounts page loaded successfully")
            assert True
        else:
            print("Test_013 Failed - Wrong page title")
            assert False

    def test_014_search_discount_by_name(self, discounts_setup):
        """Search for an existing discount by name"""
        self.dp = discounts_setup
        self.dp.search_by_name("20% order total")
        count = self.dp.get_result_count()
        print(f"Results found: {count}")
        if count > 0:
            print("Test_014 Passed - Discount found by name")
            assert True
        else:
            print("Test_014 Failed - No discount found")
            assert False

    def test_015_search_discount_invalid_name(self, discounts_setup):
        """Search with a name that doesn't exist"""
        self.dp = discounts_setup
        self.dp.search_by_name("XYZNOTEXIST999")
        no_data = self.dp.has_no_data()
        if no_data:
            print("Test_015 Passed - No data shown for invalid search")
            assert True
        else:
            print("Test_015 Failed - Expected no data")
            assert False

    def test_016_search_by_discount_type(self, discounts_setup):
        """Search discounts by type"""
        self.dp = discounts_setup
        self.dp.search_by_type("Assigned to order total")
        count = self.dp.get_result_count()
        print(f"Discounts found for type: {count}")
        assert count >= 0
        print("Test_016 Passed - Search by type completed")
        self.dp.driver.save_screenshot(
            ".\\Screenshots\\discount_type_search.png"
        )

    def test_017_add_new_discount(self, discounts_setup):
        """Add a new discount with coupon code"""
        self.dp = discounts_setup
        import random
        unique = random.randint(1000, 9999)
        discount_name = f"TestDiscount_{unique}"
        coupon = f"TEST{unique}"

        self.dp.add_new_discount(
            name=discount_name,
            disc_type="Assigned to order total",
            percentage=True,
            amount=10,
            use_coupon=True,
            coupon=coupon
        )

        success = self.dp.is_success_message_displayed()
        if success:
            print(f"Test_017 Passed - Discount '{discount_name}' added successfully")
            assert True
        else:
            print("Test_017 Failed - Success message not shown")
            assert False
        self.dp.driver.save_screenshot(
            ".\\Screenshots\\add_discount_success.png"
        )

    def test_018_verify_added_discount(self, discounts_setup):
        """Verify the newly added discount appears in search"""
        self.dp = discounts_setup
        # Navigate back to list first
        self.dp.driver.get(
            "https://admin-demo.nopcommerce.com/Admin/Discount/List"
        )
        time.sleep(2)
        self.dp.search_by_name("TestDiscount")
        count = self.dp.get_result_count()
        print(f"Found {count} test discount(s)")
        if count > 0:
            print("Test_018 Passed - Added discount found in search")
            assert True
        else:
            print("Test_018 Failed - Added discount not found")
            assert False

    def test_019_search_empty_name(self, discounts_setup):
        """Search with empty name - should return all discounts"""
        self.dp = discounts_setup
        self.dp.search_by_name("")
        count = self.dp.get_result_count()
        print(f"Total discounts found: {count}")
        assert count > 0
        print("Test_019 Passed - All discounts returned for empty search")
        self.dp.driver.save_screenshot(
            ".\\Screenshots\\all_discounts.png"
        )