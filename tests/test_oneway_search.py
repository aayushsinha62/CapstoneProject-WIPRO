"""
One Way Flight Search Tests

Validates that users can successfully search for one-way flights
using data-driven inputs from CSV.
"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.data_reader import get_test_data


@pytest.mark.smoke
@pytest.mark.parametrize(
    "flight_class,from_city,to_city,departure",
    [row[:4] for row in get_test_data("data/oneway_data.csv")]
)
def test_oneway_search(
    driver,
    flight_class,
    from_city,
    to_city,
    departure
):
    """
    Verify that a user can search for one-way flights
    and that valid results are returned.
    """

    home = HomePage(driver)
    results = SearchResultsPage(driver)

    # Open flight search homepage
    home.open_home()

    # Select flight class
    home.select_flight_class(flight_class)

    # Select passenger count
    home.select_passenger_one()

    # Select departure and destination cities
    home.select_city(home.FROM_CITY, from_city)
    home.select_city(home.TO_CITY, to_city)

    # Select departure date
    home.select_departure(departure)

    # Perform flight search
    home.click_search()

    # Validate search results appear
    flights_found = results.verify_results()
    assert flights_found > 0, "No flights found for the given search criteria"

    # Validate flight price is displayed
    price = results.verify_price_displayed()
    assert price.strip() != "", "Flight price is not displayed"