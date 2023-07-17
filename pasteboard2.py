#!/usr/bin/env python

from pathlib import Path

from AppKit import NSPasteboard  # type: ignore

PLAIN_TEXT_UTF8 = "public.utf8-plain-text"


def set_content(content: str, for_type: str = PLAIN_TEXT_UTF8) -> None:
    """
    Set content in the pasteboard.

    Args:
        content: The content to be added in the pasteboard.

    Returns:
        None
    """
    clear_pb()
    get_pasteboard().setString_forType_(content, for_type)


def get_pasteboard() -> NSPasteboard:
    """
    Retrieves the (possibly cached) pasteboard.
    """
    if not hasattr(get_pasteboard, "cache_"):
        get_pasteboard.cache_ = NSPasteboard.generalPasteboard()
    return get_pasteboard.cache_


def clear_pb() -> None:
    """
    Clear the pasteboard.
    Returns:

    """
    get_pasteboard().clearContents()


def is_empty() -> bool:
    return len(get_pasteboard().types()) == 0


def get_types() -> list[str]:
    """
    Get the content types of the current pasteboard.

    Returns:
        A list of content types.

    >>> isinstance(get_types(), list)
    True
    """
    return list(get_pasteboard().types())


def get_types_str() -> str:
    """
    Get the content types of the current pasteboard.

    Returns:
        A string of content types.

    >>> isinstance(get_types_str(), str)
    True
    """

    types = get_types()
    return "".join([f"- {x}\n" for x in types])


def get_content(t: str = None) -> str | None:
    """
    Get the content of the pasteboard if it's a string.

    Returns:
        The content of the pasteboard as a string, or None if the
        content isn't a string.

    >>> pb_content = get_content()
    >>> isinstance(pb_content, (str, type(None)))
    True
    """
    t = t or PLAIN_TEXT_UTF8
    if content := get_pasteboard().stringForType_(t):
        return content


## Tests #######################################################################

import pytest


def save_clipboard_state():
    clipboard = get_pasteboard()

    # Get the available types on the clipboard
    types = clipboard.types()

    return {typ: clipboard.dataForType_(typ) for typ in types}


def resurrect_clipboard_state(clipboard_state):
    clipboard = get_pasteboard()

    # Clear the current clipboard contents
    clipboard.clearContents()

    # Set the clipboard contents based on the saved state
    for typ, data in clipboard_state.items():
        clipboard.setData_forType_(data, typ)


#
# assert former pasteboard state is recuperated after test suite is run.
#
@pytest.fixture(scope="session", autouse=True)
def save_and_restore_clipboard():
    content = save_clipboard_state()
    yield
    resurrect_clipboard_state(content)


#
# assert pasteboard is clear before each test
#
@pytest.fixture(autouse=True)
def assert_clear():
    clear_pb()
    yield


def test_pasteboard_empty_at_start():
    assert is_empty()


def test_pasteboard_types_empty_at_start():
    assert get_types() == []


def test_pasteboard_set_content():
    # Set content to pasteboard
    set_content("Hello, World!")
    # Assert that the content has been correctly set
    assert get_content() == "Hello, World!"


def test_pasteboard_get_nonexistent_content():
    # Clear the pasteboard
    clear_pb()
    # Assert that is_empty() is true when there's no content
    assert is_empty()


def test_pasteboard_clear_content():
    # Set content to pasteboard
    set_content("Hello, World!")
    # Clear the pasteboard
    clear_pb()
    # Assert that is_empty() is true when there's no content
    assert is_empty()


def test_get_pasteboard_types():
    # Clear the pasteboard
    clear_pb()
    # Assert that the pasteboard is empty after clearing
    assert is_empty()

    # Set content to pasteboard
    set_content("Hello, World!")
    # Assert that the list includes PLAIN_TEXT_UTF8 after adding text content
    assert PLAIN_TEXT_UTF8 in get_types()


## Main ########################################################################

if __name__ == "__main__":
    import doctest

    import pytest
    import typer

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
        def test():
            """
            Run tests with pytest and doctest.
            """
            pytest.main([__file__])
            results = doctest.testmod()
            if results.failed == 0:
                print("All doctests passed successfully.")
            else:
                print(
                    f"{results.failed} "
                    f"doctest{'s' if results.failed > 1 else ''} "
                    "failed."
                )

        @staticmethod
        @app.command()
        def types():
            """
            List the content types of the current pasteboard.
            """
            typer.echo(get_types_str())

        @staticmethod
        @app.command()
        def clip(
            clip_type: str = typer.Option(
                PLAIN_TEXT_UTF8, "--type", "-t", help="The type of content to get"
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
                Call `{PGM} clip -t TYPE` with the type of content you want to get,
                e.g.:
                {PGM} clip -t {types[0]}
                """
                )

    def main():
        manager = Main()
        manager.app()

    main()
