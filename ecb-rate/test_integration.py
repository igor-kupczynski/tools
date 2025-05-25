import pytest
from datetime import datetime
from ecb_rate import fetch_ecb_rate, find_previous_rate

fetch_cases = [
    ("2025-04-29", 1.1373),
    ("2025-04-30", 1.1373),
    ("2025-05-01", None),
    ("2025-05-02", 1.1343),
    ("2025-05-03", None),
    ("2025-05-04", None),
    ("2025-05-05", 1.1343),
]

@pytest.mark.parametrize("date,expected_rate", fetch_cases)
def test_fetch_ecb_rate_usd(date, expected_rate):
    rate = fetch_ecb_rate(date)
    if expected_rate is None:
        assert rate is None
    else:
        assert rate is not None
        assert abs(rate - expected_rate) < 0.0001

find_previous_cases = [
    ("2025-05-01", 1.1373, "2025-04-30"),
    ("2025-05-03", 1.1343, "2025-05-02"),
    ("2025-05-04", 1.1343, "2025-05-02"),
]

@pytest.mark.parametrize("date,expected_rate,expected_prev_date", find_previous_cases)
def test_find_previous_rate_usd(date, expected_rate, expected_prev_date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    rate, found_date = find_previous_rate(dt)
    assert rate is not None and abs(rate - expected_rate) < 0.0001
    assert found_date == expected_prev_date

# --- EURPLN TESTS ---
pln_fetch_cases = [
    ("2024-12-27", 4.2753),
    ("2024-12-28", None),
    ("2024-12-29", None),
    ("2024-12-30", 4.2655),
    ("2024-12-31", 4.2750),
    ("2025-01-01", None),
]

@pytest.mark.parametrize("date,expected_rate", pln_fetch_cases)
def test_fetch_ecb_rate_pln(date, expected_rate):
    rate = fetch_ecb_rate(date, target_currency="PLN")
    if expected_rate is None:
        assert rate is None
    else:
        assert rate is not None
        assert abs(rate - expected_rate) < 0.0001

pln_find_previous_cases = [
    ("2024-12-28", 4.2753, "2024-12-27"),
    ("2024-12-29", 4.2753, "2024-12-27"),
    ("2024-12-30", 4.2753, "2024-12-27"),
    ("2025-01-01", 4.2750, "2024-12-31"),
]

@pytest.mark.parametrize("date,expected_rate,expected_prev_date", pln_find_previous_cases)
def test_find_previous_rate_pln(date, expected_rate, expected_prev_date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    rate, found_date = find_previous_rate(dt, target_currency="PLN")
    assert rate is not None and abs(rate - expected_rate) < 0.0001
    assert found_date == expected_prev_date
