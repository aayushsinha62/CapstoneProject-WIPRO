"""
Driver Factory

Responsible for creating and configuring the Selenium WebDriver instance
used throughout the automation framework.

The browser type and driver settings are loaded from the configuration
file so tests can run on different browsers without changing the code.

This module also applies global WebDriver settings such as implicit waits.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config_reader import get_config


# Suppress verbose webdriver-manager logs for cleaner output
logging.getLogger("WDM").setLevel(logging.WARNING)


def get_driver(logger):
    """
    Initialize and return a configured Selenium WebDriver instance.

    Parameters
    ----------
    logger : Logger
        Logger instance tied to the current test

    Returns
    -------
    WebDriver
        Initialized Selenium WebDriver
    """

    logger.info("STEP 00: Initialize WebDriver")

    # Load configuration settings
    config = get_config()
    browser = config["browser"].lower()

    # ==========================================================
    # Chrome Browser Setup
    # ==========================================================

    if browser == "chrome":

        options = webdriver.ChromeOptions()

        # Start browser maximized
        options.add_argument("--start-maximized")

        # Optional: enable headless(without GUI) execution if needed
                              # for use in CI/CD pipelines

        if config.get("headless"):
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    # ==========================================================
    # Firefox Browser Setup
    # ==========================================================

    elif browser == "firefox":

        options = webdriver.FirefoxOptions()

        if config.get("headless"):
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

    else:
        raise Exception(f"Unsupported browser: {browser}")

    # Apply global implicit wait
    driver.implicitly_wait(config["implicit_wait"])

    return driver