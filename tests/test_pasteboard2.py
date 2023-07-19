import pytest

from pasteboard2 import *


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


def test_pasteboard_types_str_empty_at_start():
    assert get_types_str() == ""


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
    assert pasteboard2.PLAIN_TEXT_UTF8 in get_types()
