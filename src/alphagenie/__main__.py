"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """AlphaGenie."""
    click.echo("Hello, world!")


if __name__ == "__main__":
    main(prog_name="alphagenie")  # pragma: no cover
