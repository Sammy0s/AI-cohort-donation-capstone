from datetime import date, timedelta


def get_next_eligible_date(last_donation_date: str) -> date:
    if not isinstance(last_donation_date, str):
        raise ValueError(f"Expected a date string, got {type(last_donation_date).__name__}")
    last = date.fromisoformat(last_donation_date)
    return last + timedelta(days=56)

def pints_to_gallons(pints: float) -> float:
    return pints * 0.125

def get_lives_saved(total_pints: float) -> int:
    return int(total_pints * 3)
