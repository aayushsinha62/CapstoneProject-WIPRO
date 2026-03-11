"""
Homepage Tests

Smoke tests to validate that the flight search homepage loads correctly
and that basic UI restrictions (such as past date selection) are enforced.
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.smoke
def test_homepage_load(driver):
    """
    Verify that the flights homepage opens successfully.
    """

    home = HomePage(driver)

    # Open flight search homepage
    home.open_home()

    # Validate that the correct page is loaded
    assert "flights" in driver.current_url.lower(), \
        "Homepage did not load correctly"


@pytest.mark.smoke
def test_past_date_not_selectable(driver):
    """
    Verify that past dates are disabled in the departure calendar.
    """

    home = HomePage(driver)

    # Open homepage
    home.open_home()

    # Open departure date calendar
    home.open_departure_calendar()

    # Get disabled dates from calendar
    disabled_dates = home.get_disabled_dates()

    # Validate that past dates exist and are disabled
    assert len(disabled_dates) > 0, \
        "Past dates are incorrectly selectable in the calendar"