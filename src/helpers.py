def separator(width=20, char='-') -> str:
    """
    Prints a separator line with the specified width and character.

    :param width: The width of the separator line (default is 20).
    :param char: The character used to create the separator line (default is '-').

    :return: The separator line as a string.
    """
    return char * width


def encapsulate_as_text_header(text, level=1) -> str:
    """
    :param text: The text to be encapsulated as a header.
    :param level: The level of the header. Defaults to 1.

    :return: The encapsulated text as a header.
    """
    if level < 1 or level > 2:
        raise ValueError("Header level must be 1 or 2")

    underline_char = '=' if level == 1 else '-'
    underline = underline_char * len(text)

    return f"*{text}*\n{underline}"
