import json

try:
    import click
except ImportError:
    raise ImportError("Click is required to use this command, try `pip install click`.")

from .main import api


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True, allow_dash=True),
    default="-",
    help="Output file.",
)
def show(output):
    """Print the API as OpenAPI JSON document to stdout."""
    if output == "-":
        click.echo(json.dumps(api.openapi(), indent=2))
    else:
        # We only write the file if it either does not exist or in case it
        # actually differs to avoid modifying the file metadata on every commit.
        try:
            current_api = click.open_file(output, "r").read()
        except FileNotFoundError:
            current_api = None
        new_api = json.dumps(api.openapi(), indent=2) + "\n"
        if current_api != new_api:
            click.open_file(output, "w").write(new_api)


if __name__ == "__main__":
    cli()
