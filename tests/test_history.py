import pytest
from database import init_db, get_connection, get_history

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

def insert_donation_with_nulls(date, location, blood_type, pints):
    """Inserts directly allowing None values to test null handling."""
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
# EMPTY STATE
# ─────────────────────────────────────────────

def test_history_empty_returns_empty_list():
    result = get_history()
    assert result == []

def test_history_empty_does_not_crash():
    try:
        get_history()
    except Exception as e:
        pytest.fail(f"get_history() crashed on empty DB: {e}")

# ─────────────────────────────────────────────
# SINGLE DONATION
# ─────────────────────────────────────────────

def test_history_single_donation_returns_one_row():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert len(result) == 1

def test_history_single_donation_correct_date():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert result[0]["date"] == "2026-05-29"

def test_history_single_donation_correct_location():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert result[0]["location"] == "Red Cross Austin"

def test_history_single_donation_correct_blood_type():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert result[0]["blood_type"] == "O+"

def test_history_single_donation_correct_pints():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert result[0]["pints"] == 1.0

# ─────────────────────────────────────────────
# MULTIPLE DONATIONS
# ─────────────────────────────────────────────

def test_history_multiple_donations_returns_all():
    insert_donation("2026-01-01", "Red Cross Austin", "O+", 1.0)
    insert_donation("2026-03-01", "Dell Seton", "A+", 0.5)
    insert_donation("2026-05-01", "UT Blood Drive", "B-", 2.0)
    result = get_history()
    assert len(result) == 3

# ─────────────────────────────────────────────
# SORT ORDER — newest first
# ─────────────────────────────────────────────

def test_history_sorted_newest_first():
    insert_donation("2026-01-01", "Red Cross Austin", "O+", 1.0)
    insert_donation("2026-05-29", "Dell Seton", "A+", 1.0)
    insert_donation("2026-03-15", "UT Blood Drive", "B-", 1.0)
    result = get_history()
    dates = [row["date"] for row in result]
    assert dates == sorted(dates, reverse=True)

def test_history_sort_correct_across_months():
    """Ensures Sept vs Oct sorts correctly (string sort edge case)."""
    insert_donation("2025-09-01", "Location A", "O+", 1.0)
    insert_donation("2025-10-01", "Location B", "O+", 1.0)
    insert_donation("2025-11-01", "Location C", "O+", 1.0)
    result = get_history()
    dates = [row["date"] for row in result]
    assert dates[0] == "2025-11-01"
    assert dates[1] == "2025-10-01"
    assert dates[2] == "2025-09-01"

def test_history_sort_correct_across_years():
    insert_donation("2024-12-31", "Location A", "O+", 1.0)
    insert_donation("2025-01-01", "Location B", "O+", 1.0)
    result = get_history()
    assert result[0]["date"] == "2025-01-01"
    assert result[1]["date"] == "2024-12-31"

# ─────────────────────────────────────────────
# NULL / NONE VALUE HANDLING
# ─────────────────────────────────────────────

def test_history_handles_null_location():
    insert_donation_with_nulls("2026-05-29", None, "O+", 1.0)
    try:
        result = get_history()
        assert result[0]["location"] is None or result[0]["location"] == ""
    except Exception as e:
        pytest.fail(f"get_history() crashed on null location: {e}")

def test_history_handles_null_blood_type():
    insert_donation_with_nulls("2026-05-29", "Red Cross Austin", None, 1.0)
    try:
        result = get_history()
        assert result[0]["blood_type"] is None or result[0]["blood_type"] == ""
    except Exception as e:
        pytest.fail(f"get_history() crashed on null blood_type: {e}")

# ─────────────────────────────────────────────
# PINTS DISPLAY
# ─────────────────────────────────────────────

def test_history_pints_stored_as_float():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 1.5)
    result = get_history()
    assert isinstance(result[0]["pints"], float)

def test_history_pints_value_correct():
    insert_donation("2026-05-29", "Red Cross Austin", "O+", 0.5)
    result = get_history()
    assert result[0]["pints"] == 0.5

# ─────────────────────────────────────────────
# LARGE DATASET
# ─────────────────────────────────────────────

def test_history_large_dataset_returns_all():
    from datetime import date, timedelta
    base = date(2020, 1, 1)
    for i in range(100):
        d = (base + timedelta(days=i * 60)).strftime("%Y-%m-%d")
        insert_donation(d, "Red Cross Austin", "O+", 1.0)
    result = get_history()
    assert len(result) == 100

def test_history_large_dataset_sorted_newest_first():
    from datetime import date, timedelta
    base = date(2020, 1, 1)
    for i in range(100):
        d = (base + timedelta(days=i * 60)).strftime("%Y-%m-%d")
        insert_donation(d, "Red Cross Austin", "O+", 1.0)
    result = get_history()
    dates = [row["date"] for row in result]
    assert dates == sorted(dates, reverse=True)