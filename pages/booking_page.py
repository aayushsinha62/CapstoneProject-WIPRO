"""
Booking Page Object

Handles the passenger details form, payment selection,
booking confirmation, and validation of successful booking.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from pages.base_page import BasePage
from utils.decorators import log_and_screenshot
import re
import time
from pathlib import Path


class BookingPage(BasePage):
    """
    Page Object representing the Flight Booking page.

    Responsibilities:
    - Fill passenger details
    - Select payment method
    - Accept booking terms
    - Confirm booking
    - Validate booking success and invoice download
    """

    # ==========================================================
    # Guest Details Locators
    # ==========================================================

    TITLE = (By.XPATH, "//select[@x-model='primary_guest.title']")
    FIRSTNAME = (By.XPATH, "//input[@placeholder='Enter First Name']")
    LASTNAME = (By.XPATH, "//input[@placeholder='Enter Last Name']")
    EMAIL = (By.XPATH, "//input[@x-model='primary_guest.email']")
    COUNTRY_CODE = (By.XPATH, "//select[@x-model='primary_guest.country_code']")
    PHONE = (By.XPATH, "//input[@placeholder='Enter Phone Number']")

    NATIONALITY = (By.XPATH, "(//select[@class='select'])[4]")
    PASSPORT = (By.XPATH, "//input[@placeholder='6 - 15 Numbers']")

    # ==========================================================
    # Payment Locators
    # ==========================================================

    CREDIT_CARD = (By.XPATH, "//div[normalize-space()='Credit Card']")
    TERMS = (
        By.XPATH,
        "(//span[@class='material-symbols-outlined text-white text-xs checkbox-icon'][normalize-space()='check'])[2]"
    )
    CONFIRM = (By.XPATH, "//span[.='Confirm Booking']")

    # ==========================================================
    # Booking Success Locators
    # ==========================================================

    INVOICE_BUTTON = (
        By.XPATH,
        "(//div[@class='btn light w-full flex items-center justify-start gap-2 cursor-pointer'])[1]"
    )

    # ==========================================================
    # Page Load Handling
    # ==========================================================

    def wait_for_page(self):
        """
        Wait until the booking page is fully loaded.

        The page is considered ready when the
        passenger first name field becomes visible.
        """
        self.wait.until(
            EC.visibility_of_element_located(self.FIRSTNAME)
        )

    # ==========================================================
    # Passenger Details
    # ==========================================================

    @log_and_screenshot
    def fill_passenger_details(
        self,
        title,
        firstname,
        lastname,
        email,
        phone,
        nationality,
        passport
    ):
        """
        Fill the primary passenger details form.

        Parameters:
        ----------
        title : str
        firstname : str
        lastname : str
        email : str
        phone : str
        nationality : str
        passport : str
        """

        # Some environments trigger a backend alert popup
        # Handle it safely if present
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass

        # Wait for booking form to load
        self.wait_for_page()

        # Fill basic passenger information
        self.driver.find_element(*self.TITLE).send_keys(title)
        self.type(self.FIRSTNAME, firstname)
        self.type(self.LASTNAME, lastname)
        self.type(self.EMAIL, email)

        # Select default country code
        self.driver.find_element(*self.COUNTRY_CODE).send_keys("IN +91")

        self.type(self.PHONE, phone)

        # Scroll down to nationality and passport section
        self.driver.execute_script("window.scrollBy(0,600)")

        nationality_field = self.wait.until(
            EC.element_to_be_clickable(self.NATIONALITY)
        )
        nationality_field.send_keys(nationality)

        passport_field = self.wait.until(
            EC.element_to_be_clickable(self.PASSPORT)
        )
        passport_field.send_keys(passport)

    # ==========================================================
    # Payment Selection
    # ==========================================================

    @log_and_screenshot
    def select_payment(self):
        """
        Select 'Credit Card' as the payment method.
        """

        credit = self.wait.until(
            EC.element_to_be_clickable(self.CREDIT_CARD)
        )

        # Scroll element into view before clicking
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            credit
        )

        # Use JS click to avoid overlay issues
        self.driver.execute_script(
            "arguments[0].click();",
            credit
        )

    # ==========================================================
    # Terms & Conditions
    # ==========================================================

    @log_and_screenshot
    def accept_terms(self):
        """
        Accept the booking terms and conditions checkbox.
        """

        checkbox = self.wait.until(
            EC.presence_of_element_located(self.TERMS)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

    # ==========================================================
    # Booking Confirmation
    # ==========================================================

    @log_and_screenshot
    def confirm_booking(self):
        """
        Click the 'Confirm Booking' button to complete booking.
        """

        confirm = self.wait.until(
            EC.presence_of_element_located(self.CONFIRM)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            confirm
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm
        )

    # ==========================================================
    # Booking Verification
    # ==========================================================

    @log_and_screenshot
    def verify_booking_success(self):
        """
        Verify that the booking is successful by:
        1. Checking if the invoice button appears
        2. Navigating to the invoice page
        3. Validating that the invoice file is downloaded
        """

        invoice_button = self.wait.until(
            EC.element_to_be_clickable(self.INVOICE_BUTTON)
        )

        # Ensure booking completed successfully
        assert invoice_button.is_displayed(), "Booking failed"

        invoice_button.click()

        # Wait until redirected to invoice page
        self.wait.until(
            lambda driver: "invoice" in driver.current_url
        )

        url = self.driver.current_url

        # Extract invoice ID from URL
        invoice_id = re.search(r'\d+$', url).group()

        self.logger.info(f"Invoice ID from URL: {invoice_id}")

        download_path = Path.home() / "Downloads"

        timeout = 15
        start_time = time.time()

        downloaded_file = None

        # Wait until invoice file appears in Downloads
        while time.time() - start_time < timeout:

            files = list(download_path.glob(f"*{invoice_id}*"))

            if files:
                downloaded_file = files[0]
                break

            time.sleep(1)

        assert downloaded_file is not None, \
            f"Invoice file with ID {invoice_id} not downloaded"

        self.logger.info(
            f"Invoice file downloaded: {downloaded_file.name}"
        )