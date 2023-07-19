#!/usr/bin/env python


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
