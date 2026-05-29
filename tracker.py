import typer

app = typer.Typer()

@app.command()
def log():
    typer.echo("Donation logged!")

@app.command()
def history():
    typer.echo("Donation history displayed!")

if __name__ == "__main__":
    app()