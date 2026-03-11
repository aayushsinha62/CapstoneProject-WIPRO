"""
Round Trip Booking Tests

Validates the complete round-trip flight booking flow including:
- flight search
- flight selection
- passenger details entry
- payment selection
- booking confirmation
"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.booking_page import BookingPage
from utils.data_reader import get_test_data


@pytest.mark.regression
@pytest.mark.parametrize(
    "flight_class,from_city,to_city,departure,return_date,title,firstname,lastname,email,phone,nationality,passport",
    get_test_data("data/roundtrip_data.csv")
)
def test_roundtrip_booking(
    driver,
    flight_class,
    from_city,
    to_city,
    departure,
    return_date,
    title,
    firstname,
    lastname,
    email,
    phone,
    nationality,
    passport
):
    """
    Verify that a user can successfully complete a round-trip flight booking.
    """

    home = HomePage(driver)
    results = SearchResultsPage(driver)
    booking = BookingPage(driver)

    # Open flight search homepage
    home.open_home()

    # Select round-trip trip type
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

    # Select the first available flight
    results.click_first_flight()

    # Fill passenger information
    booking.fill_passenger_details(
        title,
        firstname,
        lastname,
        email,
        phone,
        nationality,
        passport
    )

    # Select payment method
    booking.select_payment()

    # Accept booking terms
    booking.accept_terms()

    # Confirm booking
    booking.confirm_booking()

    # Validate booking success and invoice generation
    booking.verify_booking_success()