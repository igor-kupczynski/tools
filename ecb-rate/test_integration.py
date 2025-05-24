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
def test_fetch_ecb_rate(date, expected_rate):
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
def test_find_previous_rate(date, expected_rate, expected_prev_date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    rate, found_date = find_previous_rate(dt)
    assert rate is not None and abs(rate - expected_rate) < 0.0001
    assert found_date == expected_prev_date
