from interwebs_speed import __app_name__, __version__
import typer

from typing import Optional

from interwebs_speed.services import analisys_service, summary_service

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command(name="analyze")
def analize_command() -> None:
    analisys_service.analyze()


@app.command(name="summary")
def summary_command(
    previous_month: bool = typer.Option(
        False,
        "--previous-month",
        "-p",
        help="Send the summary of the previous month.",
    )
) -> None:
    summary_service.send_monthly_summary(previous_month)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
