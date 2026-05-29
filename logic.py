from datetime import date, timedelta


def get_next_eligible_date(last_donation_date: str) -> date:
    last = date.fromisoformat(last_donation_date)
    return last + timedelta(days=56)
