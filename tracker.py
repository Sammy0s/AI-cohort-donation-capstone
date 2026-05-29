import typer

app = typer.Typer()

@app.command()
def log():
    date = typer.prompt("What was the date of your donation?(YYYY-MM-DD)")
    location = typer.prompt("Where did you donate?")
    blood_type = typer.prompt("What is your blood type?")
    pints = typer.prompt("How many pints did you donate?", default=1.0)
    # Okay I have all the info, now I need to save it to the database
    # Handle different error cases here too
    typer.echo(f"Donation logged: {date}, {location}, {blood_type}, {pints} pints")

@app.command()
def history():
    typer.echo("Donation history displayed!")

if __name__ == "__main__":
    app()