from datetime import datetime
from src.crowdfunding_project import CrowdfundingProject


def print_separator(width=20, char='-'):
    """Prints a separator line with a given width and character.

    :param width: The width of the separator line (default is 50).
    :param char: The character to use for the separator line (default is '=').
    :return: None
    """
    print(char * width)


def encapsulate_as_text_header(text, level=1):
    """
    :param text: A string representing the content of the text header.
    :param level: An integer indicating the level of the header. Must be 1 or 2. Defaults to 1.
    :return: None

    Encapsulates the given text as a text header by printing it along with an underline that matches the length of the text. The underline character used depends on the level of the header.

    Example usage:
        encapsulate_as_text_header("Hello, World!")
        encapsulate_as_text_header("Important Information", level=2)
    """
    if level < 1 or level > 2:
        raise ValueError("Header level must be 1 or 2")

    underline_char = '=' if level == 1 else '-'
    underline = underline_char * len(text)

    print(f"*{text}*\n{underline}")

def main():
    # Create a new crowdfunding project
    project = CrowdfundingProject("Ghadeer Land", datetime(2024, 7, 22), datetime(2025, 7, 22))

    # Add expenses
    land_price = project.add_expense("Land Price from Auction", 1885908, datetime(2024, 7, 22))
    price_increase = project.add_expense("Price Increase after Auction", 178102, datetime(2024, 7, 22))
    auction_fees = project.add_expense("Auction Agent Fees", 54221, datetime(2024, 7, 22))
    vat = project.add_expense("VAT", 94295.40, datetime(2024, 7, 22))
    agent_fees = project.add_expense("Agent Fees", 52955, datetime(2024, 7, 22))

    # Add partners
    hussain_alsalim = project.add_partner("Hussain AlSalim", 1000000)
    ali_alfaraj = project.add_partner("Ali AlFaraj", 500000.40)
    saleh_alnasser = project.add_partner("Saleh AlNasser", 440000)
    ali_aldawood = project.add_partner("Ali AlDawood", 205481)
    mohammed_alhawaj = project.add_partner("Mohammed AlHawaj", 120000)

    # Add payments
    project.add_payment(52955, datetime(2024, 7, 22), hussain_alsalim, agent_fees)
    project.add_payment(94295.40, datetime(2024, 7, 23), ali_alfaraj, vat)

    # Add a sale
    # project.add_sale(1250000, datetime(2025, 6, 1), "Duplex 1 Sale")

    # Print partner summary
    encapsulate_as_text_header("Partners Summary")
    partner_summary = project.get_partner_summary()
    for name, details in partner_summary.items():
        print(f"Partner: {name}")
        print(f"Investment Plan: SAR {details['investment']:,.2f}")
        print(f"Ownership Percentage: {details['ownership_percentage']:.2f}%")
        print(f"Total Payments: SAR {details['total_payments']:,.2f}")
        print(f"Investment Balance: SAR {details['investment_balance']:,.2f}")
        print_separator()
    print()

    # Print expense summary
    encapsulate_as_text_header("Expenses Summary")
    expense_summary = project.get_expense_summary()
    for description, details in expense_summary.items():
        print(f"Expense: {description}")
        print(f"Total: SAR {details['total']:,.2f}")
        print(f"Paid: SAR {details['paid']:,.2f}")
        print(f"Remaining: SAR {details['remaining']:,.2f}")
        print(f"Status: {details['status'].value}")
        print_separator()
    print()

    # Print payment summary
    encapsulate_as_text_header("Payments Summary")
    payment_summary = project.get_payment_summary()
    for description, details in payment_summary.items():
        print(f"Payment: {description}")
        print(f"Date: {details['date']}")
        print(f"Partner: {details['partner']}")
        print(f"Amount: SAR {details['amount']:,.2f}")
        print(f"Expense: {details['expense']}" + f" ({details['percentage']:,.2f}%)")
        print_separator()
    print()

    # Print project summary
    encapsulate_as_text_header("Project Summary")
    print(project)


if __name__ == "__main__":
    main()