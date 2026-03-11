"""
Custom Decorators

Provides a decorator used across Page Object methods to:
1. Log the executed test step
2. Capture a screenshot after the step execution

This improves debugging and enhances HTML reports.
"""

import functools
import re
from utils.paths import SCREENSHOTS_DIR


def _safe_test_name(name):
    """
    Convert pytest node name into a filesystem-safe folder name.

    Removes invalid characters and limits length to avoid
    Windows path length issues.
    """
    name = re.sub(r"[^A-Za-z0-9_-]", "_", name)
    return name[:60]


def log_and_screenshot(step_description=None):
    """
    Decorator that logs a step and captures a screenshot after execution.

    Usage:
        @log_and_screenshot
        def click_search(self):

        @log_and_screenshot("Select Departure Date")
        def select_departure(self):

    Parameters
    ----------
    step_description : str, optional
        Custom step name to appear in logs and screenshots.
    """

    # ---------------------------------------------------------
    # Case 1: Used without parentheses
    # Example:
    # @log_and_screenshot
    # ---------------------------------------------------------
    if callable(step_description):
        func = step_description
        step_description = None

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return _execute_step(self, func, step_description, *args, **kwargs)

        return wrapper

    # ---------------------------------------------------------
    # Case 2: Used with custom description
    # Example:
    # @log_and_screenshot("Open Search Page")
    # ---------------------------------------------------------
    def decorator(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return _execute_step(self, func, step_description, *args, **kwargs)

        return wrapper

    return decorator


def _execute_step(self, func, step_description, *args, **kwargs):
    """
    Internal helper function that executes the wrapped step,
    logs it, and captures a screenshot.
    """

    # Initialize step counter if not already set
    if not hasattr(self.driver, "step_counter"):
        self.driver.step_counter = 1

    step_number = self.driver.step_counter

    # Determine step name
    step_name = step_description or func.__name__.replace("_", " ").title()

    # Log step execution
    self.logger.info(f"STEP {step_number:02d}: {step_name}")

    # Create safe folder name for screenshots
    safe_name = _safe_test_name(self.driver.test_name)

    folder = SCREENSHOTS_DIR / safe_name
    folder.mkdir(parents=True, exist_ok=True)

    # Build screenshot filename
    file = folder / f"{step_number:02d}_{step_name.replace(' ', '_')}.png"

    try:
        # Execute the actual page method
        result = func(self, *args, **kwargs)

    except Exception:
        # Take screenshot even if step fails
        self.driver.save_screenshot(str(file))
        raise

    else:
        # Take screenshot if step succeeds
        self.driver.save_screenshot(str(file))
        self.driver.step_counter += 1
        return result