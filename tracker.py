import typer
from rich.console import Console
from rich.panel import Panel
from datetime import datetime, date
from database import init_db, get_connection

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
    typer.echo("Donation history — coming soon!")


@app.command()
def status():
    """Show eligibility and donation stats."""
    typer.echo("Status — coming soon!")


if __name__ == "__main__":
    app()
