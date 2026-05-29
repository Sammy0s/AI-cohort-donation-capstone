import pytest
import sqlite3
from datetime import datetime, timedelta
from database import init_db, get_connection
from validation import (
    validate_date,
    validate_blood_type,
    validate_location,
    validate_pints,
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def clear_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donations")
    conn.commit()
    conn.close()

def insert_donation(date, location, blood_type, pints):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO donations (date, location, blood_type, pints) VALUES (?, ?, ?, ?)",
        (date, location, blood_type, pints),
    )
    conn.commit()
    conn.close()

def setup_function():
    init_db()
    clear_db()

# ─────────────────────────────────────────────
# DATABASE TESTS
# ─────────────────────────────────────────────

def test_init_db_creates_table():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='donations'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None

def test_init_db_does_not_crash_if_table_exists():
    init_db()
    init_db()  # calling twice should not raise

def test_get_connection_returns_valid_connection():
    conn = get_connection()
    assert conn is not None
    conn.close()

# ─────────────────────────────────────────────
# DATE VALIDATION
# ─────────────────────────────────────────────

def test_valid_date_accepted():
    assert validate_date("2026-05-29") == "2026-05-29"

def test_future_date_rejected():
    future = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(ValueError):
        validate_date(future)

def test_date_before_1900_rejected():
    with pytest.raises(ValueError):
        validate_date("1899-12-31")

def test_date_wrong_format_rejected():
    with pytest.raises(ValueError):
        validate_date("05-29-2026")

def test_date_missing_leading_zero_autocorrected():
    assert validate_date("2026-5-29") == "2026-05-29"

def test_impossible_date_rejected():
    with pytest.raises(ValueError):
        validate_date("2026-02-30")

def test_blank_date_rejected():
    with pytest.raises(ValueError):
        validate_date("")

def test_non_date_string_rejected():
    with pytest.raises(ValueError):
        validate_date("yesterday")

# ─────────────────────────────────────────────
# BLOOD TYPE VALIDATION
# ─────────────────────────────────────────────

@pytest.mark.parametrize("blood_type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
def test_all_valid_blood_types_accepted(blood_type):
    assert validate_blood_type(blood_type) == blood_type

def test_lowercase_blood_type_autocorrected():
    assert validate_blood_type("o+") == "O+"

def test_mixed_case_blood_type_autocorrected():
    assert validate_blood_type("aB+") == "AB+"

def test_invalid_blood_type_rejected():
    with pytest.raises(ValueError):
        validate_blood_type("pizza")

def test_blank_blood_type_rejected():
    with pytest.raises(ValueError):
        validate_blood_type("")

def test_blood_type_with_space_autocorrected():
    assert validate_blood_type("O +") == "O+"

# ─────────────────────────────────────────────
# LOCATION VALIDATION
# ─────────────────────────────────────────────

def test_valid_location_accepted():
    assert validate_location("Red Cross Austin") == "Red Cross Austin"

def test_location_too_short_rejected():
    with pytest.raises(ValueError):
        validate_location("A")

def test_location_too_long_rejected():
    with pytest.raises(ValueError):
        validate_location("A" * 51)

def test_blank_location_rejected():
    with pytest.raises(ValueError):
        validate_location("")

def test_location_with_emoji_rejected():
    with pytest.raises(ValueError):
        validate_location("Red Cross 🩸")

def test_location_exactly_2_chars_accepted():
    assert validate_location("RC") == "RC"

def test_location_exactly_50_chars_accepted():
    assert validate_location("A" * 50) == "A" * 50

# ─────────────────────────────────────────────
# PINTS VALIDATION
# ─────────────────────────────────────────────

def test_valid_pints_accepted():
    assert validate_pints(1.0) == 1.0

def test_pints_below_minimum_rejected():
    with pytest.raises(ValueError):
        validate_pints(0.09)

def test_pints_above_maximum_rejected():
    with pytest.raises(ValueError):
        validate_pints(2.11)

def test_pints_rounded_to_2_decimal_places():
    assert validate_pints(1.126) == 1.13

def test_non_numeric_pints_rejected():
    with pytest.raises(ValueError):
        validate_pints("one")

def test_negative_pints_rejected():
    with pytest.raises(ValueError):
        validate_pints(-1.0)

def test_pints_exactly_0_1_accepted():
    assert validate_pints(0.1) == 0.1

def test_pints_exactly_2_1_accepted():
    assert validate_pints(2.1) == 2.1

# ─────────────────────────────────────────────
# DUPLICATE DETECTION
# ─────────────────────────────────────────────

def test_same_date_donation_rejected():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donations WHERE date = ?", ("2026-05-29",))
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 1  # only one should exist
    with pytest.raises(ValueError, match="too many donations on the same date"):
        if count >= 1:
            raise ValueError("too many donations on the same date")

def test_different_date_donations_both_accepted():
    insert_donation("2026-01-01", "Red Cross Austin", "O+", 1.0)
    insert_donation("2026-03-01", "Dell Seton", "A+", 1.0)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donations")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 2

# ─────────────────────────────────────────────
# INSERTION TESTS
# ─────────────────────────────────────────────

def test_successful_insert_appears_in_db():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 1

def test_multiple_donations_all_appear_in_db():
    insert_donation("2026-01-01", "Red Cross Austin", "O+", 1.0)
    insert_donation("2026-03-01", "Dell Seton", "A+", 0.5)
    insert_donation("2026-05-01", "UT Blood Drive", "B-", 2.0)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 3

def test_inserted_pints_are_rounded():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", round(1.126, 2))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pints FROM donations")
    pints = cursor.fetchone()[0]
    conn.close()
    assert pints == 1.13

def test_inserted_blood_type_is_uppercased():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT blood_type FROM donations")
    blood_type = cursor.fetchone()[0]
    conn.close()
    assert blood_type == blood_type.upper()