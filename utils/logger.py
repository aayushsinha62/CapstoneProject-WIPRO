"""
Logger Utility

Provides a centralized logger configuration for the automation framework.

Each test receives its own logger instance, which writes logs to:
1. Console (for real-time visibility during execution)
2. Log file inside artifacts/logs (for debugging and reporting)
"""

import logging
import sys
from utils.paths import LOGS_DIR


def get_logger(test_name):
    """
    Create and return a configured logger for a specific test.

    Parameters
    ----------
    test_name : str
        Name of the currently executing test.

    Returns
    -------
    Logger
        Configured logger instance for the test.
    """

    # Ensure log directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if logger is reused
    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        # ------------------------------------------------------
        # File Handler (stores logs in artifacts/logs)
        # ------------------------------------------------------

        log_file = LOGS_DIR / f"{test_name}.log"

        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)

        # ------------------------------------------------------
        # Console Handler (prints logs in terminal)
        # ------------------------------------------------------

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Prevent logs from propagating to root logger
        logger.propagate = False

    return logger