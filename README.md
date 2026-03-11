# Flight Booking Automation Framework ✈️

## Project Overview

This project automates the **Flight Booking functionality** of the demo website:

https://phptravels.net/flights

The automation framework is built using **Python, Selenium WebDriver, and Pytest**, following the **Page Object Model (POM)** design pattern to ensure clean, scalable, and maintainable test automation.

The framework demonstrates several **industry-standard automation practices**, including:

- Page Object Model (POM)
- Data Driven Testing (CSV based)
- Parallel Test Execution
- HTML Reporting
- Test-level logging
- Screenshot capture for each test step
- Retry mechanism for flaky tests
- Automatic artifact management
- Config-driven framework setup

This project was implemented as part of a **Selenium Automation Capstone Project**.

---

# Tech Stack

- Python
- Selenium WebDriver
- Pytest
- Pytest HTML Reports
- Pytest-xdist (Parallel execution)
- Pytest-rerunfailures (Retry failed tests)
- Pandas (Data driven testing)
- WebDriver Manager

---

# Project Structure

```
flight_booking_framework
│
├── artifacts
│   ├── logs
│   ├── reports
│   └── screenshots
│
├── config
│   └── config.json
│
├── data
│   ├── oneway_data.csv
│   └── roundtrip_data.csv
│
├── pages
│   ├── base_page.py
│   ├── home_page.py
│   ├── search_results_page.py
│   └── booking_page.py
│
├── tests
│   ├── test_homepage.py
│   ├── test_oneway_search.py
│   ├── test_roundtrip_search.py
│   ├── test_oneway_booking.py
│   └── test_roundtrip_booking.py
│
├── utils
│   ├── driver_factory.py
│   ├── logger.py
│   ├── decorators.py
│   ├── data_reader.py
│   ├── config_reader.py
│   └── paths.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Framework Features

## Page Object Model (POM)

All UI interactions are encapsulated within **Page Classes**, keeping test logic separate from page interaction logic. This improves maintainability and scalability.

---

## Data Driven Testing

Test data is stored in **CSV files** and dynamically read during execution, allowing multiple test scenarios to be executed without modifying the test code.

---

## Logging

Each test generates its own **log file**, making debugging easier and providing detailed execution traces.

---

## Screenshot Capture

Screenshots are captured **automatically after each step** using decorators and attached to the HTML report for better test visibility.

---

## HTML Reports

Pytest generates a **self-contained HTML report** after execution, including logs and screenshots.

---

## Retry Mechanism

Flaky tests automatically retry once using **pytest-rerunfailures**, improving test reliability.

---

## Artifact Management

Logs, reports, and screenshots are stored inside the **artifacts folder**, which is automatically cleaned before each test run.

---

## Config Driven Execution

Framework settings such as **browser type, base URL, and wait durations** are stored in a configuration file, allowing easy modification without changing the framework code.

Example configuration:

`config/config.json`

```json
{
  "base_url": "https://phptravels.net/flights",
  "browser": "chrome",
  "implicit_wait": 10,
  "explicit_wait": 20
}
```

---

# Setup Instructions

## 1. Clone the Repository

```
git clone <repository-url>
cd flight_booking_framework
```

---

## 2. Create Virtual Environment

```
python -m venv .venv
```

Activate the environment:

### Windows

```
.venv\Scripts\activate
```

### Mac/Linux

```
source .venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

# Running Tests

Run all tests:

```
pytest
```

Run only **smoke tests**:

```
pytest -m smoke
```

Run only **regression tests**:

```
pytest -m regression
```

Run tests in **parallel**:

```
pytest -n auto
```

---

# Test Reports

After execution, reports are generated inside:

```
artifacts/reports/report.html
```

Logs are stored in:

```
artifacts/logs/
```

Screenshots are stored in:

```
artifacts/screenshots/
```

---

# Author

**Aayush Sinha**  
Selenium Automation Capstone Project