import random
import time

import pytest

from pageObjects.AffiliatesPage import AffiliatesPage


@pytest.fixture
def affiliates_setup(logged_in_driver):
    ap = AffiliatesPage(logged_in_driver)
    ap.navigate_to_affiliates()
    return ap


@pytest.mark.order(4)
class Test_AffiliatesPage:

    # 1. Mandatory field validation check
    @pytest.mark.xfail(reason="Known defect: Affiliate form saves successfully even with mandatory fields left blank")
    def test_020_add_affiliate_without_mandatory_fields(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_add_new()
        self.ap.fill_affiliate_form()
        self.ap.save_affiliate()

        error_shown = self.ap.is_validation_error_displayed()
        assert error_shown, "Defect: affiliate saved despite missing mandatory fields"



    # 2. Add new affiliate and verify entered details persist
    def test_021_add_new_affiliate_and_verify_details(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_add_new()

        unique = random.randint(1000, 9999)
        first_name = f"Test{unique}"
        last_name = "Affiliate"
        email = f"test{unique}@example.com"
        city = "Toronto"
        address1 = "123 Test Street"
        zip_code = "M5H 2N2"
        phone = "4165551234"

        self.ap.fill_affiliate_form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            city=city,
            address1=address1,
            zip_code=zip_code,
            phone=phone,
        )
        self.ap.save_and_continue()  # stays on the edit page so we can verify field values

        actual_first_name = self.ap.get_field_value(self.ap.first_name)
        actual_email = self.ap.get_field_value(self.ap.email)

        if actual_first_name == first_name and actual_email == email:
            print("Test_021 Passed - Affiliate details saved and verified correctly")
            assert True
        else:
            print("Test_021 Failed - Saved details do not match entered details")
            assert False

    # 3. "Back to affiliate list" link
    def test_022_back_to_affiliate_list(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_add_new()
        self.ap.click_back_to_list()

        actual_title = self.ap.driver.title
        if actual_title == "Affiliates / nopCommerce administration":
            print("Test_022 Passed - Navigated back to affiliate list")
            assert True
        else:
            print("Test_022 Failed - Wrong page after clicking back link:", actual_title)
            assert False

    # 4. "Affiliate info" expandable panel
    def test_023_affiliate_info_expand_collapse(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_add_new()

        was_expanded_before = self.ap.is_affiliate_info_expanded()
        self.ap.toggle_affiliate_info()
        expanded_after_first_click = self.ap.is_affiliate_info_expanded()
        self.ap.toggle_affiliate_info()
        expanded_after_second_click = self.ap.is_affiliate_info_expanded()

        if expanded_after_first_click != was_expanded_before and expanded_after_second_click == was_expanded_before:
            print("Test_023 Passed - Affiliate info panel expands and collapses correctly")
            assert True
        else:
            print("Test_023 Failed - Panel did not toggle as expected")
            assert False

    # 5. Help (?) icon tooltip
    def test_024_help_icon_tooltip(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_add_new()

        tooltip_text = self.ap.hover_help_icon()
        print("Tooltip text is:", tooltip_text)
        if tooltip_text:
            print("Test_024 Passed - Tooltip text displayed on hover")
            assert True
        else:
            print("Test_024 Failed - No tooltip text found")
            assert False

    # 6. Page size = 7 vs Next button behaviour
    def test_025_pagination_next_button(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.select_page_size(7)
        total_entries = self.ap.get_total_entries()
        print(f"Total entries: {total_entries}")

        is_enabled = self.ap.is_next_button_enabled()
        if total_entries > 7:
            assert is_enabled, "Next button should be enabled when entries > page size"
            self.ap.click_next_page()
            print("Test_025 Passed - Next button enabled and clickable when entries > page size")
        else:
            assert not is_enabled, "Next button should be disabled when entries <= page size"
            print("Test_025 Passed - Next button correctly disabled when entries <= page size")

    # 7. Edit affiliate and verify changes reflected
    def test_026_edit_affiliate_reflects_changes(self, affiliates_setup):
        self.ap = affiliates_setup
        self.ap.click_first_edit()

        unique = random.randint(1000, 9999)
        new_comment = f"Updated comment {unique}"

        comment_field = self.ap.driver.find_element(*self.ap.admin_comment)
        comment_field.clear()
        comment_field.send_keys(new_comment)
        self.ap.save_and_continue()

        actual_comment = self.ap.get_field_value(self.ap.admin_comment)
        if actual_comment == new_comment:
            print("Test_026 Passed - Edited details reflected after save")
            assert True
        else:
            print("Test_026 Failed - Edited details not reflected:", actual_comment)
            assert False

    # 8. "Learn more about affiliates" doc link
    def test_027_learn_more_link_opens_new_page(self, affiliates_setup):
        self.ap = affiliates_setup
        original_handles = self.ap.driver.window_handles

        self.ap.click_learn_more()
        time.sleep(2)
        new_handles = self.ap.driver.window_handles

        if len(new_handles) > len(original_handles):
            self.ap.driver.switch_to.window(new_handles[-1])
            print("New tab URL:", self.ap.driver.current_url)
            if "docs.nopcommerce.com" in self.ap.driver.current_url:
                print("Test_027 Passed - Learn more link opened documentation in a new tab")
                assert True
            else:
                print("Test_027 Failed - New tab did not open the documentation page")
                assert False
            self.ap.driver.close()
            self.ap.driver.switch_to.window(original_handles[0])
        else:
            print("Test_027 Failed - No new tab/window was opened")
            assert False
