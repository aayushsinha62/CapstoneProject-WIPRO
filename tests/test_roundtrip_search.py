"""
Round Trip Flight Search Tests

Validates that users can search for round-trip flights
using data-driven inputs from CSV.
"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.data_reader import get_test_data


@pytest.mark.smoke
@pytest.mark.parametrize(
    "flight_class,from_city,to_city,departure,return_date",
    [row[:5] for row in get_test_data("data/roundtrip_data.csv")]
)
def test_roundtrip_search(
    driver,
    flight_class,
    from_city,
    to_city,
    departure,
    return_date
):
    """
    Verify that a user can search for round-trip flights
    and that valid results are returned.
    """

    home = HomePage(driver)
    results = SearchResultsPage(driver)

    # Open flight search homepage
    home.open_home()

    # Select round-trip option
    home.select_roundtrip()

    # Select flight class
    home.select_flight_class(flight_class)

    # Select passenger count
    home.select_passenger_one()

    # Select departure and destination cities
    home.select_city(home.FROM_CITY, from_city)
    home.select_city(home.TO_CITY, to_city)

    # Select travel dates
    home.select_departure(departure)
    home.select_return(return_date)

    # Perform flight search
    home.click_search()

    # Validate that search results appear
    flights_found = results.verify_results()
    assert flights_found > 0, "No round-trip flights found for the given search"

    # Validate that flight price is displayed
    price = results.verify_price_displayed()
    assert price.strip() != "", "Flight price is not displayed"