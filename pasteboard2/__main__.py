#!/usr/bin/env python

from pathlib import Path

import typer

from pasteboard2 import *

PGM = Path(__file__).name


class Main:
    app = typer.Typer(add_completion=False)

    def __init__(self):
        pass

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
            types_str = "".join([f"- {x}\n" for x in types])
            typer.echo(
                f"""
            Unknown content type{'s' if len(types) > 1 else ''}:
            {types_str}
            Call `{PGM} clip -t TYPE`
            with the type of content you want to get, e.g.:
            {PGM} clip -t {types[0]}
            """
            )


def main():
    manager = Main()
    manager.app()


if __name__ == "__main__":
    main()
