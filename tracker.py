import typer
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from datetime import datetime, date
from database import init_db, get_connection, get_history, get_latest_donation_date, get_total_pints
from logic import get_next_eligible_date, pints_to_gallons, get_lives_saved

app = typer.Typer()
console = Console()

VALID_BLOOD_TYPES = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}


def _prompt_date() -> str:
    while True:
        raw = typer.prompt("Donation date (YYYY-MM-DD)")
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Invalid format — use YYYY-MM-DD (e.g. 2026-05-29).[/red]")
            continue
        if d > date.today():
            console.print("[red]Donation date can't be in the future.[/red]")
            continue
        return raw


def _prompt_location() -> str:
    while True:
        raw = typer.prompt("Donation location").strip()
        if raw:
            return raw
        console.print("[red]Location can't be blank.[/red]")


def _prompt_blood_type() -> str:
    options = ", ".join(sorted(VALID_BLOOD_TYPES))
    while True:
        raw = typer.prompt(f"Blood type ({options})").strip().upper()
        if raw in VALID_BLOOD_TYPES:
            return raw
        console.print(f"[red]'{raw}' isn't valid. Choose from: {options}[/red]")


def _prompt_pints() -> float:
    while True:
        raw = typer.prompt("Pints donated", default="1.0").strip()
        try:
            pints = float(raw)
        except ValueError:
            console.print("[red]Enter a number (e.g. 1 or 1.5).[/red]")
            continue
        if pints <= 0:
            console.print("[red]Pints must be greater than 0.[/red]")
        elif pints > 3:
            console.print("[red]That's more than 3 pints — double-check and try again.[/red]")
        else:
            return pints


@app.command()
def log():
    """Log a new blood donation."""
    init_db()
    console.print("\n[bold cyan]Log a Donation[/bold cyan]")

    donation_date = _prompt_date()
    location = _prompt_location()
    blood_type = _prompt_blood_type()
    pints = _prompt_pints()

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO donations (date, location, blood_type, pints) VALUES (?, ?, ?, ?)",
                (donation_date, location, blood_type, pints),
            )
    except Exception as e:
        console.print(f"[red]Failed to save donation: {e}[/red]")
        raise typer.Exit(code=1)

    console.print(Panel(
        f"[bold]Date:[/bold]       {donation_date}\n"
        f"[bold]Location:[/bold]   {location}\n"
        f"[bold]Blood type:[/bold] {blood_type}\n"
        f"[bold]Pints:[/bold]      {pints}",
        title="[bold green]Donation Saved[/bold green]",
        border_style="green",
    ))


@app.command()
def history():
    """Display all past donations."""
    init_db()
    rows = get_history()

    if not rows:
        console.print("[yellow]No donations logged yet. Run 'python tracker.py log' to add one.[/yellow]")
        return

    table = Table(title="Donation History", header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Date", width=12)
    table.add_column("Location")
    table.add_column("Blood Type", width=10)
    table.add_column("Pints", width=6)

    for row in rows:
        table.add_row(
            str(row["id"]),
            row["date"],
            escape(row["location"]) if row["location"] else "—",
            row["blood_type"] or "—",
            str(row["pints"]),
        )

    console.print(table)


@app.command()
def status():
    """Show eligibility and donation stats."""
    init_db()
    latest_date = get_latest_donation_date()

    if not latest_date:
        console.print("[yellow]No donations logged yet. Run 'python tracker.py log' to add one.[/yellow]")
        return

    total_pints = get_total_pints()
    gallons = pints_to_gallons(total_pints)
    lives = get_lives_saved(total_pints)
    next_eligible = get_next_eligible_date(latest_date)
    next_eligible_str = next_eligible.strftime("%B %d, %Y")

    goal = 1.0
    filled = min(int((gallons / goal) * 16), 16)
    bar = "[bold red]" + "█" * filled + "[/bold red]" + "[dim]" + "░" * (16 - filled) + "[/dim]"

    content = (
        f"[bold]Next eligible:[/bold]   {next_eligible_str} ⏳\n"
        f"[bold]Gallons donated:[/bold] {bar} {gallons:.3f} gal\n"
        f"[bold]Lives saved:[/bold]     ~{lives}"
    )

    console.print(Panel(content, title="🩸 Blood Donation Status", border_style="red"))


if __name__ == "__main__":
    app()
