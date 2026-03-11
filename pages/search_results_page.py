"""
Search Results Page Object

Handles interactions and validations on the flight
search results page such as verifying results,
selecting flights, and validating displayed prices.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.decorators import log_and_screenshot


class SearchResultsPage(BasePage):
    """
    Page Object representing the Flight Search Results page.

    Responsibilities:
    - Validate search results are loaded
    - Select a flight from available results
    - Verify flight price visibility
    """

    # ==========================================================
    # Locators
    # ==========================================================

    # Main results container
    RESULTS_CONTAINER = (By.XPATH, "//main")

    # All available "Book" buttons (each flight card)
    BOOK_BUTTONS = (By.XPATH, "//button[contains(.,'Book')]")

    # Flight price element on booking page
    PRICE = (By.XPATH, "(//p[contains(text(),'BDT')])[2]")

    # ==========================================================
    # Results Validation
    # ==========================================================

    @log_and_screenshot
    def verify_results(self):
        """
        Verify that flight results are successfully loaded.

        Returns
        -------
        int
            Number of available flights found on the page.
        """

        # Wait for results container to appear
        self.wait.until(
            EC.presence_of_element_located(self.RESULTS_CONTAINER)
        )

        # Collect all available flight booking buttons
        flights = self.wait.until(
            EC.presence_of_all_elements_located(self.BOOK_BUTTONS)
        )

        self.logger.info(f"Number of flights found: {len(flights)}")

        return len(flights)

    # ==========================================================
    # Flight Selection
    # ==========================================================

    @log_and_screenshot
    def click_first_flight(self):
        """
        Select the first available flight from search results.
        """

        # Ensure results section is loaded
        self.wait.until(
            EC.presence_of_element_located(self.RESULTS_CONTAINER)
        )

        flights = self.driver.find_elements(*self.BOOK_BUTTONS)

        assert flights, "No flights available to select"

        first_button = flights[0]

        # Scroll flight card into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            first_button
        )

        # Use JavaScript click to avoid overlay issues
        self.driver.execute_script(
            "arguments[0].click();",
            first_button
        )

    # ==========================================================
    # Price Validation
    # ==========================================================

    @log_and_screenshot
    def verify_price_displayed(self):
        """
        Verify that the flight price is visible on the booking page.

        Returns
        -------
        str
            The displayed flight price.
        """

        price = self.wait.until(
            EC.visibility_of_element_located(self.PRICE)
        )

        self.logger.info(f"Flight price displayed: {price.text}")

        return price.text