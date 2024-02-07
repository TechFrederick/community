import typer

from .build import build
from .services.fetcher.commands import fetch


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
app.command()(build)
app.command()(fetch)
