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
def show():
    """Print the API as OpenAPI JSON document to stdout."""
    click.echo(json.dumps(api.openapi(), indent=2))


if __name__ == "__main__":
    cli()
