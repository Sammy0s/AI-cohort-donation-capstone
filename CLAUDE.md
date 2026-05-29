# Blood Donation Tracker — CLAUDE.md

## Project Overview
A Python CLI app for tracking personal blood donations. Users can log donations, view history, and check their current status including next eligible donation date and total blood donated visualized in gallons.

## Stack
- **Language:** Python 3
- **CLI framework:** Typer
- **Terminal UI:** Rich
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **DB file:** `donations.db` (auto-created on first run, gitignored)

## File Structure
```
capstonedonation/
├── tracker.py      # Entry point, all CLI commands (log, history, status)
├── database.py     # DB connection and schema setup
├── logic.py        # Business logic (eligibility dates, gallons calc, lives saved)
├── CLAUDE.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Commands
| Command | What it does |
|---|---|
| `python tracker.py log` | Prompt user to log a new donation |
| `python tracker.py history` | Display all past donations as a table |
| `python tracker.py status` | Show eligibility, gallons donated, lives saved |

## Key Rules
- Never hardcode donation data — always read from `donations.db`
- 56 days between whole blood donations (standard Red Cross rule)
- 1 donation = 1 pint = ~0.125 gallons
- 1 donation = up to 3 lives saved
- All dates stored as `YYYY-MM-DD` strings in the DB