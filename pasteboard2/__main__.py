#!/usr/bin/env python

import importlib.metadata as im
import sys
import tomllib
from pathlib import Path

import typer

from pasteboard2 import *


def _get_name(module_name):
    ep_key = f"{module_name}.{Path(__file__).stem}:main"
    eps = im.entry_points()
    ep = eps.select(value=ep_key)
    name = tuple(ep)[0].name if ep else Path(sys.argv[0]).name
    return ep, name


class Main:
    app = typer.Typer(add_completion=False)

    MODULE_NAME = Path(__file__).parent.name
    ep, name = _get_name(MODULE_NAME)

    @staticmethod
    @app.command()
    def version():
        """
        Outputs the version number.
        """
        if Main.ep:
            typer.echo(im.version(Main.MODULE_NAME))
        else:
            pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"
            print(f"no meta info available for {Main.MODULE_NAME}")
            print(f"taking version from {pyproject_toml}:")
            v = tomllib.loads(pyproject_toml.read_text())["project"]["version"]
            typer.echo(v)

    @staticmethod
    @app.command()
    def clear():
        """
        Empties the pasteboard.
        """
        clear_pb()

    @staticmethod
    @app.command()
    def types():
        """
        List the content types of the current pasteboard.
        """
        t_str = get_types_str()
        typer.echo(t_str or "clipboard empty, hence no types")

    @staticmethod
    @app.command()
    def clip(
        clip_type: str = typer.Option(
            None, "--type", "-t", help="The type of content to get"
        )
    ):
        """
        Print the content of the pasteboard if it's a string.
        """
        if content := get_content(clip_type):
            typer.echo(f"clipboard contains: '{content}'")
            typer.echo(get_types_str())
        elif is_empty():
            typer.echo("No content")
        else:
            types = get_types()
            typer.echo(
                f"Unknown content type{'s' if len(types) > 1 else ''}:\n"
                f"{get_types_str()}\n"
                f"Call `{Main.name} clip -t TYPE`\n"
                "with the type of content you want to get, e.g.:\n"
                f"{Main.name} clip -t {types[0]}\n"
                "(only works for types with known string representation.)\n"
            )


def main():
    manager = Main()
    manager.app()


if __name__ == "__main__":
    main()
