import re
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AffiliatesPage:

    # Navigation
    affiliates_url = "https://admin-demo.nopcommerce.com/Admin/Affiliate/List"

    # List page locators
    add_new_button = (By.XPATH, "//a[contains(@href,'/Admin/Affiliate/Create')]")
    learn_more_link = (By.XPATH, "//a[contains(@href,'docs.nopcommerce.com') and contains(@href,'affiliates')]")
    first_edit_button = (By.XPATH, "//table[@id='affiliates-grid']//tbody/tr[1]//a[contains(text(),'Edit')]")

    # Create/Edit form locators
    # NOTE: nopCommerce's actual locale resource for this link is lower-case
    # ("back to affiliate list"), so the match below is case-insensitive to
    # avoid being broken by resource-text casing.
    back_to_list_link = (
        By.XPATH,
        "//a[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'back to affiliate list')]"
    )
    affiliate_info_header = (By.XPATH, "//div[contains(@class,'card-header')][contains(.,'Affiliate info')]")
    affiliate_info_body = (
        By.XPATH,
        "//div[contains(@class,'card-header')][contains(.,'Affiliate info')]"
        "/following-sibling::div[contains(@class,'card-body')][1]"
    )

    active_checkbox = (By.ID, "Active")
    first_name = (By.ID, "Address_FirstName")
    last_name = (By.ID, "Address_LastName")
    email = (By.ID, "Address_Email")
    company = (By.ID, "Address_Company")
    city = (By.ID, "Address_City")
    address1 = (By.ID, "Address_Address1")
    zip_code = (By.ID, "Address_ZipPostalCode")
    phone = (By.ID, "Address_PhoneNumber")
    admin_comment = (By.ID, "AdminComment")
    friendly_url_name = (By.ID, "FriendlyUrlName")

    save_button = (By.NAME, "save")
    save_continue_button = (By.NAME, "save-continue")

    # Validation
    validation_summary = (By.XPATH, "//div[contains(@class,'validation-summary-errors')]")
    field_validation_errors = (By.XPATH, "//span[contains(@class,'field-validation-error')]")

    # Generic tooltip/help icon (same pattern used elsewhere in this framework)
    help_icon = (By.XPATH, "//div[@class='ico-help']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- Navigation ----------
    def navigate_to_affiliates(self):
        self.driver.get(self.affiliates_url)
        self.wait.until(EC.presence_of_element_located((By.ID, "affiliates-grid")))
        time.sleep(1)

    def click_add_new(self):
        self.wait.until(EC.element_to_be_clickable(self.add_new_button)).click()
        time.sleep(1)

    def click_back_to_list(self):
        self.driver.find_element(*self.back_to_list_link).click()
        time.sleep(1)

    def click_first_edit(self):
        self.driver.find_element(*self.first_edit_button).click()
        time.sleep(1)

    def click_learn_more(self):
        self.driver.find_element(*self.learn_more_link).click()

    # ---------- Form handling ----------
    def fill_affiliate_form(self, first_name="", last_name="", email="", company="",
                             city="", address1="", zip_code="", phone="",
                             admin_comment="", friendly_url=""):
        """Fills the affiliate form. Leave args blank to test mandatory-field validation."""
        fields = {
            self.first_name: first_name,
            self.last_name: last_name,
            self.email: email,
            self.company: company,
            self.city: city,
            self.address1: address1,
            self.zip_code: zip_code,
            self.phone: phone,
            self.admin_comment: admin_comment,
            self.friendly_url_name: friendly_url,
        }
        for locator, value in fields.items():
            field = self.driver.find_element(*locator)
            field.clear()
            if value:
                field.send_keys(value)

    def save_affiliate(self):
        self.driver.find_element(*self.save_button).click()
        time.sleep(1)

    def save_and_continue(self):
        self.driver.find_element(*self.save_continue_button).click()
        time.sleep(1)

    def get_field_value(self, locator):
        return self.driver.find_element(*locator).get_attribute("value")

    # ---------- Validation ----------
    def is_validation_error_displayed(self):
        try:
            errors = self.driver.find_elements(*self.validation_summary)
            errors += self.driver.find_elements(*self.field_validation_errors)
            return any(e.is_displayed() and e.text.strip() != "" for e in errors)
        except Exception as e:
            print(f"Error checking validation messages: {e}")
            return False

    # ---------- Affiliate info collapsible panel ----------
    def is_affiliate_info_expanded(self):
        body = self.driver.find_element(*self.affiliate_info_body)
        return body.is_displayed()

    def toggle_affiliate_info(self):
        self.driver.find_element(*self.affiliate_info_header).click()
        time.sleep(0.5)

    # ---------- Help icon tooltip ----------
    def hover_help_icon(self):
        elements = self.driver.find_elements(*self.help_icon)
        if not elements:
            return None
        element = elements[0]
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        return element.get_attribute("data-original-title") or element.get_attribute("title")

    # ---------- Pagination ----------
    def select_page_size(self, size):
        """Finds the page-size <select> by locating the one whose options
        actually contain the target size — avoids hardcoding a name/id that
        differs between DataTables v1 and v2 markup."""
        size = str(size)
        selects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//select")))
        for sel in selects:
            option_texts = [o.text.strip() for o in sel.find_elements(By.TAG_NAME, "option")]
            if size in option_texts:
                Select(sel).select_by_visible_text(size)
                time.sleep(1)
                return
        raise NoSuchElementException(f"Could not find a page-size dropdown with option '{size}'")

    def get_total_entries(self):
        """Parses text like 'Showing 1 to 7 of 22 entries' to get the total count.
        Checks both DataTables v2 ('dt-info') and v1 ('*_info' id) markup."""
        candidates = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'dt-info')] | //div[contains(@id,'_info')]"
        )
        for el in candidates:
            match = re.search(r"of (\d+)", el.text)
            if match:
                return int(match.group(1))
        return 0

    def _find_next_button(self):
        """Tries several known DataTables v1/v2 patterns, falling back to
        plain visible-text matching, since the exact markup varies by version."""
        locator_candidates = [
            (By.XPATH, "//button[contains(@class,'dt-paging-button')][contains(normalize-space(.),'Next')]"),
            (By.XPATH, "//a[contains(@class,'paginate_button') and contains(@class,'next')]"),
            (By.XPATH, "//*[self::button or self::a][contains(normalize-space(.),'Next')]"),
        ]
        for locator in locator_candidates:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        raise NoSuchElementException("Could not locate the pagination 'Next' button")

    def is_next_button_enabled(self):
        next_btn = self._find_next_button()
        classes = (next_btn.get_attribute("class") or "").lower()
        aria_disabled = (next_btn.get_attribute("aria-disabled") or "").lower()
        return "disabled" not in classes and aria_disabled != "true"

    def click_next_page(self):
        self._find_next_button().click()
        time.sleep(1)