"""
conftest.py

Central pytest configuration file used across the entire automation framework.

Responsibilities:
1. Clean previous test artifacts before execution
2. Initialize and teardown WebDriver for each test
3. Attach screenshots to pytest HTML report
4. Configure HTML report location and format
"""

import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Ensure project root is included in Python path
# ---------------------------------------------------------------------
# This allows Python to locate framework modules such as:
# utils/, pages/, config/, etc.

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
import shutil  #used for file operation - delete folders
import os
import pytest_html
import re

from utils.driver_factory import get_driver
from utils.logger import get_logger
from utils.paths import ARTIFACTS_DIR, LOGS_DIR, REPORTS_DIR, SCREENSHOTS_DIR


# ---------------------------------------------------------------------
# Clean artifacts before test execution
# ---------------------------------------------------------------------
# This fixture runs once per test session and removes old reports,
# logs, and screenshots before starting a new run.
# It prevents mixing artifacts from previous executions.

@pytest.fixture(scope="session", autouse=True)
def clean_artifacts():

    # Prevent multiple pytest-xdist workers from deleting artifacts simultaneously
    if os.environ.get("PYTEST_XDIST_WORKER") is None:

        # Remove old artifacts folder if it exists
        if ARTIFACTS_DIR.exists():
            shutil.rmtree(ARTIFACTS_DIR, ignore_errors=True)

        # Recreate required artifact directories
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# WebDriver Fixture
# ---------------------------------------------------------------------
# Initializes WebDriver before each test and ensures proper teardown
# after test execution.

@pytest.fixture
def driver(request):

    # Get current test name from pytest
    test_name = request.node.name

    # Create logger specific to this test
    logger = get_logger(test_name)

    # Initialize WebDriver
    driver = get_driver(logger)

    # Attach metadata to driver (used by logger and screenshot decorator)
    driver.test_name = test_name
    driver.step_counter = 1

    yield driver

    # Teardown: close browser after test execution
    if driver:
        driver.quit()


# ---------------------------------------------------------------------
# Attach screenshots to HTML report
# ---------------------------------------------------------------------
# This pytest hook runs after each test phase and attaches captured
# screenshots to the HTML report for easier debugging.

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Only attach screenshots after the actual test execution phase
    if report.when == "call":

        driver = item.funcargs.get("driver")

        if driver:

            safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", item.name)[:60]
            folder = SCREENSHOTS_DIR / safe_name

            extras = getattr(report, "extras", [])

            if folder.exists():

                screenshots = sorted(folder.glob("*.png"))
                html_content = ""

                # Embed screenshots inside HTML report
                for shot in screenshots:

                    step_name = shot.stem.replace("_", " ")

                    html_content += f"""
                    <div style="margin-bottom:15px;">
                        <b>{step_name}</b><br>
                        <img src="{shot}" style="width:400px;border:1px solid #ccc;">
                    </div>
                    """

                extras.append(pytest_html.extras.html(html_content))

            report.extras = extras


# ---------------------------------------------------------------------
# Configure HTML Report
# ---------------------------------------------------------------------
# Defines the output location of pytest HTML report and enables
# self-contained reports (all resources embedded).

def pytest_configure(config):

    report_path = (REPORTS_DIR / "report.html").resolve()

    config.option.htmlpath = str(report_path)
    config.option.self_contained_html = True