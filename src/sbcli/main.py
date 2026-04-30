import typer
from sbcli.scraper.scraper import scraper_app
app = typer.Typer(help="SBCLI - Herramienta de gestión centralizada")

app.add_typer(scraper_app, name="scraper")

if __name__ == "__main__":
    app()