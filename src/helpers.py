def separator(width=50, char='─') -> str:
    """
    Prints a separator line with the specified width and character.

    :param width: The width of the separator line (default is 50).
    :param char: The character used to create the separator line (default is '─').

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

    if level == 1:
        # Main header with box drawing
        border = '═' * (len(text) + 4)
        return f"╔{border}╗\n║  {text}  ║\n╚{border}╝"
    else:
        # Subheader with simple underline
        underline = '─' * len(text)
        return f"┌─ {text} ─┐\n{underline}"


def format_currency(amount: float, currency: str = "SAR") -> str:
    """
    Format currency with proper thousands separators and styling.
    
    :param amount: The amount to format
    :param currency: The currency symbol (default: SAR)
    :return: Formatted currency string
    """
    return f"{currency} {amount:,.2f}"


def create_table_row(*columns, widths=None, align='left') -> str:
    """
    Create a formatted table row with proper spacing.
    
    :param columns: Column values
    :param widths: List of column widths (optional)
    :param align: Text alignment ('left', 'right', 'center')
    :return: Formatted table row
    """
    if widths is None:
        widths = [20] * len(columns)
    
    formatted_cols = []
    for i, col in enumerate(columns):
        width = widths[i] if i < len(widths) else 20
        col_str = str(col)
        
        if align == 'right':
            formatted_cols.append(col_str.rjust(width))
        elif align == 'center':
            formatted_cols.append(col_str.center(width))
        else:
            formatted_cols.append(col_str.ljust(width))
    
    return '│ ' + ' │ '.join(formatted_cols) + ' │'


def create_section_divider(title: str = None) -> str:
    """
    Create a section divider with optional title.
    
    :param title: Optional section title
    :return: Formatted section divider
    """
    if title:
        title_len = len(title)
        side_len = (48 - title_len) // 2
        left_side = '─' * side_len
        right_side = '─' * (48 - title_len - side_len)
        return f"┌{left_side} {title} {right_side}┐"
    else:
        return '├' + '─' * 48 + '┤'
