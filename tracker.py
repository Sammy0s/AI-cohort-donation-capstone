import typer
from database import init_db, get_connection

app = typer.Typer()

@app.command()
def log():
    date = typer.prompt("What was the date of your donation?(YYYY-MM-DD)")
    location = typer.prompt("Where did you donate?")
    blood_type = typer.prompt("What is your blood type?")
    pints = typer.prompt("How many pints did you donate?", default=1.0)
    # Okay I have all the info, now I need to save it to the database
    # Handle different error cases here too
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO donations (date, location, blood_type, pints) VALUES (?, ?, ?, ?)",
            (date, location, blood_type, pints)
        )

    # Log the donation to the console
    typer.echo(f"Donation logged: {date}, {location}, {blood_type}, {pints} pints")

@app.command()
def history():
    typer.echo("Donation history displayed!")

if __name__ == "__main__":
    app()