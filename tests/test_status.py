import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from datetime import date, timedelta
from database import init_db, get_connection, get_total_pints
from logic import get_next_eligible_date, pints_to_gallons, get_lives_saved


def clear_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donations")
    conn.commit()
    conn.close()

def insert_donation(date_str, location, blood_type, pints):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO donations (date, location, blood_type, pints) VALUES (?, ?, ?, ?)",
        (date_str, location, blood_type, pints),
    )
    conn.commit()
    conn.close()

def setup_function():
    init_db()
    clear_db()


# ELIGIBILITY
def test_next_eligible_is_56_days_later():
    result = get_next_eligible_date("2026-05-29")
    assert result == date(2026, 7, 24)

def test_next_eligible_wrong_format_raises():
    with pytest.raises((ValueError, Exception)):
        get_next_eligible_date("29-05-2026")

def test_next_eligible_empty_string_raises():
    with pytest.raises((ValueError, Exception)):
        get_next_eligible_date("")


# GALLONS
def test_pints_to_gallons_one_pint():
    assert pints_to_gallons(1.0) == 0.125

def test_pints_to_gallons_two_pints():
    assert pints_to_gallons(2.0) == 0.25

def test_total_pints_single_donation():
    insert_donation("2026-05-29", "Red Cross", "O+", 1.0)
    assert get_total_pints() == 1.0

def test_total_pints_multiple_donations():
    insert_donation("2026-01-01", "Red Cross", "O+", 1.0)
    insert_donation("2026-03-01", "Dell Seton", "O+", 1.0)
    assert get_total_pints() == 2.0


# LIVES SAVED
def test_lives_saved_one_pint():
    assert get_lives_saved(1.0) == 3

def test_lives_saved_two_pints():
    assert get_lives_saved(2.0) == 6

def test_lives_saved_zero():
    assert get_lives_saved(0.0) == 0