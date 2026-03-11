"""
Home Page Object

Represents the flight search homepage.

Handles actions such as:
- selecting flight type
- selecting cities
- selecting flight class
- selecting passengers
- selecting dates
- initiating flight search
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.decorators import log_and_screenshot
from utils.config_reader import get_config


class HomePage(BasePage):

    # ==========================================================
    # Page Elements
    # ==========================================================

    # Page loader
    LOADER = (By.ID, "page-loader")

    # Flight type dropdown
    TRIP_TYPE = (By.XPATH, "//span[@x-text='getSelectedName()']/parent::div")

    # Flight Class dropdown
    FLIGHT_CLASS_DROPDOWN = (
        By.XPATH,
        "//div[@x-data='flightSearchData()']//div[@class='grid grid-cols-2 lg:grid-cols-2 gap-4 col-span-2 lg:col-span-1']/div[2]//div[1]"
    )

    ROUNDTRIP = (
        By.XPATH,
        "//div[contains(@class,'input-dropdown-content') and contains(@class,'show')]//li[contains(.,'Round Trip')]"
    )

    ONEWAY = (
        By.XPATH,
        "//div[contains(@class,'input-dropdown-content') and contains(@class,'show')]//li[contains(.,'One Way')]"
    )

    # Flight class options
    FLIGHT_CLASS_OPTION = (
        By.XPATH,
        "//div[contains(@class,'show')]//li"
    )

    # Passenger dropdown
    PASSENGER_DROPDOWN = (
        By.XPATH,
        "//div[@class='form-control col-span-2 lg:col-span-1']//div[@class='input-dropdown']//div[@class='input cursor-pointer flex items-center justify-between']"
    )

    # City input fields
    FROM_CITY = (By.XPATH, "//input[@x-ref='fromInput']")
    TO_CITY = (By.XPATH, "//input[@x-ref='toInput']")

    # Auto-suggestion dropdown results
    AUTO_SUGGEST = (
        By.XPATH,
        "//div[contains(@class,'absolute')]//div[contains(@class,'cursor-pointer')]"
    )

    # Date fields
    DEPARTURE = (By.XPATH, "//input[@placeholder='Departure Date']")
    RETURN = (By.XPATH, "//input[@placeholder='Return Date']")

    # Search button
    SEARCH = (By.XPATH, "//button[@type='submit']")

    # ==========================================================
    # Page Load
    # ==========================================================

    @log_and_screenshot
    def open_home(self):
        """Open the flight search homepage and wait until fully loaded"""

        config = get_config()

        # Open homepage
        self.driver.get(config["base_url"])

        # Wait for page DOM to finish loading
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # Wait for loading spinner to disappear
        self.wait.until(
            EC.invisibility_of_element_located(self.LOADER)
        )

    # ==========================================================
    # Flight Type Selection
    # ==========================================================

    @log_and_screenshot
    def select_oneway(self):
        """Select 'One Way' flight type"""

        # Directly update flight type via JS
        self.driver.execute_script("""
            document.querySelector("input[name='flight_type']").value = 'oneway';
        """)

    @log_and_screenshot
    def select_roundtrip(self):
        """Select 'Round Trip' flight type"""

        self.driver.execute_script("""
            document.querySelector("input[name='flight_type']").value='roundtrip';
            document.querySelector("[x-text='getSelectedName()']").innerText='Round Trip';
        """)

    # ==========================================================
    # Flight Class Selection
    # ==========================================================

    @log_and_screenshot
    def select_flight_class(self, flight_class):
        """Select flight class from dropdown"""

        class_index = {
            "economy": 1,
            "economy premium": 2,
            "business": 3,
            "first class": 4
        }

        index = class_index.get(flight_class.lower())

        if not index:
            raise Exception(f"Invalid flight class: {flight_class}")

        # Open dropdown
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.FLIGHT_CLASS_DROPDOWN)
        )
        dropdown.click()

        # Select option dynamically
        option_xpath = f"(//div[contains(@class,'input-dropdown-content') and contains(@class,'show')]//div)[{index}]"

        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )

        self.driver.execute_script("arguments[0].click();", option)

    # ==========================================================
    # Passenger Selection
    # ==========================================================

    @log_and_screenshot
    def select_passenger_one(self):
        """
        Open passenger dropdown, verify default passenger count
        is 1, then close dropdown.
        """

        passenger = self.wait.until(
            EC.element_to_be_clickable(self.PASSENGER_DROPDOWN)
        )

        passenger.click()

        # Verify passenger count is visible
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='1']")
            )
        )

        passenger.click()

    # ==========================================================
    # City Selection
    # ==========================================================

    @log_and_screenshot
    def select_city(self, field, city):
        """Select departure or arrival city from suggestion list"""

        element = self.wait.until(
            EC.element_to_be_clickable(field)
        )

        element.click()
        element.clear()
        element.send_keys(city)

        # Wait for suggestions
        self.wait.until(
            EC.visibility_of_element_located(self.AUTO_SUGGEST)
        )

        suggestions = self.wait.until(
            EC.visibility_of_all_elements_located(self.AUTO_SUGGEST)
        )

        for option in suggestions:

            code_elements = option.find_elements(By.XPATH, ".//span")

            for code in code_elements:
                if code.text.strip().upper() == city.upper():

                    self.driver.execute_script(
                        "arguments[0].click();", option
                    )
                    return

        raise Exception(f"City {city} not found in suggestions")

    # ==========================================================
    # Date Selection
    # ==========================================================

    @log_and_screenshot
    def select_departure(self, date):
        """Set departure date using JavaScript"""

        field = self.wait.until(
            EC.presence_of_element_located(self.DEPARTURE)
        )

        # Remove readonly restriction
        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly')", field
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1]", field, date
        )

    @log_and_screenshot
    def select_return(self, date):
        """Set return date using JavaScript"""

        field = self.wait.until(
            EC.presence_of_element_located(self.RETURN)
        )

        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly')", field
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1]", field, date
        )

    # ==========================================================
    # Flight Search
    # ==========================================================

    @log_and_screenshot
    def click_search(self):
        """Click search button and wait for results page"""

        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH)
        )

        self.driver.execute_script(
            "arguments[0].click();", search_button
        )

        # Wait until results appear
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(.,'Book')]")
            )
        )

    # ==========================================================
    # Calendar Validation
    # ==========================================================

    @log_and_screenshot
    def open_departure_calendar(self):
        """Open the departure calendar"""

        calendar = self.wait.until(
            EC.element_to_be_clickable(self.DEPARTURE)
        )
        calendar.click()

    def get_disabled_dates(self):
        """Return list of disabled (past) dates in calendar"""

        return self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'disabled')]"
        )