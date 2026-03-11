"""
Paths Configuration

Centralizes commonly used project directories so they can be reused
throughout the automation framework.

This avoids hardcoding file paths and makes the framework easier
to maintain and scale.
"""

from pathlib import Path


# ==========================================================
# Project Root
# ==========================================================

# Root directory of the automation project
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==========================================================
# Artifacts Directory
# ==========================================================

# Main artifacts folder (stores logs, reports, screenshots)
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


# ==========================================================
# Artifact Subdirectories
# ==========================================================

# Directory for test execution logs
LOGS_DIR = ARTIFACTS_DIR / "logs"

# Directory for HTML reports
REPORTS_DIR = ARTIFACTS_DIR / "reports"

# Directory for screenshots captured during test execution
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"