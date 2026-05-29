import re
from datetime import datetime

VALID_BLOOD_TYPES = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F000-\U0001FFFF"  # misc symbols, emoticons, transport, etc.
    "\U00002700-\U000027BF"  # dingbats
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U00002600-\U000026FF"  # misc symbols (hearts, stars, etc.)
    "]",
    flags=re.UNICODE,
)


def validate_date(date: str) -> str:
    """
    Accepts YYYY-MM-DD or YYYY-M-D (autocorrects leading zeros).
    Rejects blank, non-date strings, dates before 1900, and future dates.
    Returns normalized YYYY-MM-DD string.
    """
    if not date or not date.strip():
        raise ValueError("Date cannot be blank.")

    date = date.strip()

    # Attempt to normalize missing leading zeros by padding each part
    parts = date.split("-")
    if len(parts) == 3:
        try:
            year = parts[0].zfill(4)
            month = parts[1].zfill(2)
            day = parts[2].zfill(2)
            date = f"{year}-{month}-{day}"
        except Exception:
            raise ValueError(f"Invalid date format: '{date}'. Use YYYY-MM-DD.")

    # Parse strictly
    try:
        parsed = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date: '{date}'. Use YYYY-MM-DD.")

    if parsed.year < 1900:
        raise ValueError("Date cannot be before 1900.")

    if parsed.date() > datetime.today().date():
        raise ValueError("Date cannot be in the future.")

    return parsed.strftime("%Y-%m-%d")


def validate_blood_type(blood_type: str) -> str:
    """
    Autocorrects case and removes spaces (e.g. 'o +' -> 'O+').
    Rejects blank or unrecognized blood types.
    Returns normalized uppercase blood type string.
    """
    if not blood_type or not blood_type.strip():
        raise ValueError("Blood type cannot be blank.")

    normalized = blood_type.replace(" ", "").upper()

    if normalized not in VALID_BLOOD_TYPES:
        raise ValueError(
            f"Invalid blood type: '{blood_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_BLOOD_TYPES))}."
        )

    return normalized


def validate_location(location: str) -> str:
    """
    Rejects blank, under 2 chars, over 50 chars, and emoji-containing locations.
    Returns stripped location string.
    """
    if not location or not location.strip():
        raise ValueError("Location cannot be blank.")

    location = location.strip()

    if len(location) < 2:
        raise ValueError("Location must be at least 2 characters.")

    if len(location) > 50:
        raise ValueError("Location must be 50 characters or fewer.")

    if EMOJI_PATTERN.search(location):
        raise ValueError("Location cannot contain emojis.")

    return location


def validate_pints(pints) -> float:
    """
    Accepts numeric values between 0.1 and 2.1 inclusive.
    Rejects non-numeric input, negatives, and out-of-range values.
    Returns value rounded to 2 decimal places.
    """
    try:
        pints = float(pints)
    except (ValueError, TypeError):
        raise ValueError(f"Pints must be a number, got: '{pints}'.")

    if pints < 0.1:
        raise ValueError("Pints must be at least 0.1.")

    if pints > 2.1:
        raise ValueError("Pints cannot exceed 2.1.")

    return round(pints, 2)