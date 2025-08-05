def separator(width=30, char='-') -> str:
    """
    Prints a separator line with the specified width and character.

    :param width: The width of the separator line (default is 30).
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

    if level == 1:
        # Main header - mobile friendly
        return f"📋 {text.upper()}"
    else:
        # Subheader - simple format
        return f"📌 {text}"


def format_currency(amount: float, currency: str = "SAR") -> str:
    """
    Format currency with proper thousands separators and styling.
    
    :param amount: The amount to format
    :param currency: The currency symbol (default: SAR)
    :return: Formatted currency string
    """
    return f"{currency} {amount:,.2f}"


def create_mobile_card(title: str, items: dict) -> str:
    """
    Create a mobile-friendly card format for displaying data.
    
    :param title: Card title/header
    :param items: Dictionary of key-value pairs to display
    :return: Formatted mobile card
    """
    lines = [f"💳 {title}"]
    for key, value in items.items():
        lines.append(f"  {key}: {value}")
    lines.append("")  # Empty line for spacing
    return "\n".join(lines)


def create_section_divider(title: str = None) -> str:
    """
    Create a mobile-friendly section divider.
    
    :param title: Optional section title
    :return: Formatted section divider
    """
    if title:
        return f"\n🗓️ {title.upper()}\n{'-' * 25}"
    else:
        return f"{'-' * 30}"


def create_compact_summary(icon: str, label: str, value: str) -> str:
    """
    Create a compact one-line summary for mobile.
    
    :param icon: Emoji icon
    :param label: Description label
    :param value: Value to display
    :return: Formatted summary line
    """
    return f"{icon} {label}: {value}"
