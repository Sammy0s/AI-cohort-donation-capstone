import pytest
from datetime import date, timedelta
from logic import get_next_eligible_date


# ─────────────────────────────────────────────
# BASIC MATH
# ─────────────────────────────────────────────

def test_basic_56_day_math():
    result = get_next_eligible_date("2026-01-01")
    assert result == date(2026, 2, 26)

def test_known_date_correct_output():
    result = get_next_eligible_date("2026-05-29")
    assert result == date(2026, 7, 24)

# ─────────────────────────────────────────────
# YEAR BOUNDARY
# ─────────────────────────────────────────────

def test_year_boundary_dec_31():
    result = get_next_eligible_date("2025-12-31")
    assert result == date(2026, 2, 25)

def test_year_boundary_rolls_correctly():
    result = get_next_eligible_date("2025-11-15")
    assert result == date(2026, 1, 10)

# ─────────────────────────────────────────────
# LEAP YEAR
# ─────────────────────────────────────────────

def test_leap_year_feb_29_input():
    result = get_next_eligible_date("2024-02-29")
    assert result == date(2024, 4, 25)

def test_leap_year_result_lands_on_feb_29():
    # Jan 4 2028 + 56 days = Feb 29 2028 (2028 is a leap year)
    result = get_next_eligible_date("2028-01-04")
    assert result == date(2028, 2, 29)

# ─────────────────────────────────────────────
# ALREADY ELIGIBLE
# ─────────────────────────────────────────────

def test_old_donation_still_returns_correct_date():
    result = get_next_eligible_date("2020-01-01")
    assert result == date(2020, 2, 26)

def test_eligible_date_in_past_does_not_crash():
    try:
        get_next_eligible_date("2020-01-01")
    except Exception as e:
        pytest.fail(f"Crashed on old donation date: {e}")

# ─────────────────────────────────────────────
# TODAY'S DONATION
# ─────────────────────────────────────────────

def test_todays_donation_is_56_days_from_now():
    today = date.today().strftime("%Y-%m-%d")
    result = get_next_eligible_date(today)
    assert result == date.today() + timedelta(days=56)

# ─────────────────────────────────────────────
# RETURN TYPE
# ─────────────────────────────────────────────

def test_return_type_is_date_object():
    result = get_next_eligible_date("2026-05-29")
    assert isinstance(result, date)

def test_return_type_is_not_string():
    result = get_next_eligible_date("2026-05-29")
    assert not isinstance(result, str)

# ─────────────────────────────────────────────
# INVALID INPUTS
# ─────────────────────────────────────────────

def test_blank_string_raises_value_error():
    with pytest.raises(ValueError):
        get_next_eligible_date("")

def test_none_input_raises_value_error():
    with pytest.raises(ValueError):
        get_next_eligible_date(None)

def test_wrong_format_raises_value_error():
    with pytest.raises(ValueError):
        get_next_eligible_date("05-29-2026")

def test_nonsense_string_raises_value_error():
    with pytest.raises(ValueError):
        get_next_eligible_date("yesterday")

def test_invalid_date_raises_value_error():
    with pytest.raises(ValueError):
        get_next_eligible_date("2026-02-30")