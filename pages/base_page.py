"""
Base Page

Parent class for all Page Object classes in the framework.

Provides common reusable utilities such as:
- clicking elements
- typing text
- retrieving element text
- centralized explicit wait handling
- test-specific logging
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
from utils.config_reader import get_config


class BasePage:
    """
    BasePage acts as the foundation for all page objects.

    It initializes:
    - WebDriver instance
    - Explicit wait
    - Logger tied to the current test
    """

    def __init__(self, driver):
        """
        Initialize shared components used across all page objects.

        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance provided by pytest fixture
        """

        self.driver = driver

        # Load configuration values
        config = get_config()

        # Shared explicit wait used throughout the framework
        self.wait = WebDriverWait(driver, config["explicit_wait"])

        # Create logger associated with the running test
        self.logger = get_logger(driver.test_name)

    # ==========================================================
    # Common Element Actions
    # ==========================================================

    def click(self, locator):
        """
        Wait for an element to be clickable and perform click.

        Parameters
        ----------
        locator : tuple
            Selenium locator tuple (By, value)
        """

        self.logger.info(f"Clicking element: {locator}")

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        element.click()


    def type(self, locator, text):
        """
        Wait for an input field, clear existing value,
        and type the provided text.

        Parameters
        ----------
        locator : tuple
            Selenium locator tuple (By, value)

        text : str
            Text to type into the field
        """

        self.logger.info(f"Typing '{text}' into element: {locator}")

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """
        Retrieve visible text from an element.

        Parameters
        ----------
        locator : tuple
            Selenium locator tuple (By, value)

        Returns
        -------
        str
            Visible text of the element
        """

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return element.text