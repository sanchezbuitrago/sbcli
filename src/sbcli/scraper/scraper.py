import typer
import requests
from rich.table import Table
from rich.console import Console
from typing import List

from sbcli.commons.config import save_url, get_url
from sbcli.scraper.model import Book

console = Console()

scraper_app = typer.Typer(help="Comandos para la aplicacion de scraper scraper")
_CONTEXT = "scraper"

@scraper_app.command("config-url")
def config_url(link: str = typer.Option(..., "--link", "-l", help="URL del servicio")):
    save_url(url=link, context=_CONTEXT)
    typer.echo(f"✅ URL configurada exitosamente: {link}")


@scraper_app.command("get-url")
def config_url():
    url = get_url(context=_CONTEXT)
    typer.echo(f"✅ URL configurada: {url}")


@scraper_app.command("create-book")
def create_book(link: str = typer.Option(..., "--link", "-l", help="Enlace al recurso")):
    server_url = get_url(context=_CONTEXT)
    if not server_url:
        typer.secho("❌ Error: URL no configurada. Ejecuta 'sbcli scraper config-url --link <url>' primero.", fg="red")
        raise typer.Exit(code=1)
    typer.echo(f"🚀 [SCRAPER] Registrando el link: {link}:")

    try:
        response = requests.post(url=f"{server_url}/books", json={"link": link})
        response.raise_for_status()
        if response.status_code == 200:
            typer.echo("Libro creado exitosamente")
            typer.echo(response.json())

    except requests.HTTPError as e:
        typer.echo(f"Error creando el libro: {str(e)}")
        typer.echo(e.response.json())
    except Exception as e:
        typer.echo(f"No se pudo crear el libro: {str(e)}")


@scraper_app.command("get-books")
def get_books(display_in_table: bool = typer.Option(False, "--display-in-table", "-dt", help="Controla si se debe mostrar la informacion en una tabla")):
    server_url = get_url(context=_CONTEXT)
    if not server_url:
        typer.secho("❌ Error: URL no configurada. Ejecuta 'sbcli scraper config-url --link <url>' primero.", fg="red")
        raise typer.Exit(code=1)

    try:
        response = requests.get(url=f"{server_url}/books")
        response.raise_for_status()
        if response.status_code == 200:
            typer.echo("Libros consultados exitosamente")

            books: List[Book] = []
            count = response.json()["count"]
            typer.echo(f"Número de libros encontrados: {count}")
            for book in response.json()["books"]:
                books.append(Book.from_dict(data=book))

            if display_in_table:
                _print_book_table(books=books)
            else:
                for book in books:
                    typer.echo("__________")
                    typer.echo(f"Nombre: {book.title}")
                    typer.echo(f"Autor: {book.author}")
                    typer.echo(f"Precio Actual: {book.current_price:,.2f}")
                    typer.echo(f"Precio minimo: {book.min_price:,.2f}")
                    typer.echo(f"Precio maximo: {book.max_price:,.2f}")
                    typer.echo(f"Precio promedio: {book.average_price:,.2f}")
                    typer.echo(f"Fecha Actualizacion: {book.last_updated_at}")
                    typer.echo(f"Score de precio: {book.price_score}")

                    if book.book_with_error:
                        typer.echo(f"Error: {book.error_detail}")


    except requests.HTTPError as e:
        typer.echo(f"Error obteniendo el listado de libros: {str(e)}", err=True)
        typer.echo(e.response.json())
    except Exception as e:
        console.print_exception(show_locals=True)
        typer.echo(f"No se pudo consultar los libros: {str(e)}", err=True)


def _print_book_table(books: List[Book]) -> None:
    table = Table(title="Biblioteca Interna", show_header=True, header_style="bold magenta")

    # 2. Añadimos columnas
    table.add_column("Nombre")
    table.add_column("Autor")
    table.add_column("Precio Actual", justify="right")
    table.add_column("Precio Minimo", justify="right")
    table.add_column("Precio Maximo", justify="center")
    table.add_column("Precio promedio", justify="center")
    table.add_column("Fecha última actualizacion", justify="center")

    for book in books:
        table.add_row(book.title,book.author, str(book.current_price), str(book.min_price), str(book.max_price), str(book.average_price), str(book.last_updated_at))

    console.print(table)