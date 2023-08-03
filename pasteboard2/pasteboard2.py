#!/usr/bin/env python


from AppKit import NSPasteboard  # type: ignore


class Exportable:
    """
    Decorator to mark the functions that shall be exported.
    It simply collects all functions decorated with
    @exportable in the instance var exported_names.
    At the end of this source code, we call:
    __all__ = exportable.exported_names
    """

    def __init__(self):
        self.exported_names = []

    def __call__(self, obj, name=None):
        if callable(obj):  # If the object is callable (function/class)
            self.exported_names.append(obj.__name__)
        else:  # If the object is not callable (constant)
            if name is None:
                raise ValueError("You must provide a name for non-callable objects")
            self.exported_names.append(name)
        return obj


exportable = Exportable()

PLAIN_TEXT_UTF8 = exportable("public.utf8-plain-text", "PLAIN_TEXT_UTF8")


@exportable
def set_content(content: str, for_type: str = PLAIN_TEXT_UTF8) -> None:
    """
    Set content in the pasteboard.

    Args:
        content: The content to be added in the pasteboard.
        for_type: The type of the content.

    Returns:
        None
    """
    clear_pb()
    get_pasteboard().setString_forType_(content, for_type)


@exportable
def get_pasteboard() -> NSPasteboard:
    """
    Retrieves the (possibly cached) pasteboard.

    Returns:
        The (possibly cached) pasteboard.
    """
    if not hasattr(get_pasteboard, "cache_"):
        get_pasteboard.cache_ = NSPasteboard.generalPasteboard()
    return get_pasteboard.cache_


@exportable
def clear_pb() -> None:
    """
    Clears the pasteboard.

    Returns:
        None
    """
    get_pasteboard().clearContents()


@exportable
def is_empty() -> bool:
    """
    Returns True if the clipboard is empty.

    Returns:
        True if the clipboard is empty.
    """
    return len(get_pasteboard().types()) == 0


@exportable
def get_types() -> list[str]:
    """
    Get the content types of the current pasteboard.

    Returns:
        A list of content types.

    >>> isinstance(get_types(), list)
    True
    """
    return list(get_pasteboard().types())


@exportable
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


@exportable
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


__all__ = exportable.exported_names
