from datetime import datetime
from src.crowdfunding_project import CrowdfundingProject


def print_separator(width=50, char='='):
    print(char * width)

def main():
    # Create a new crowdfunding project
    project = CrowdfundingProject("Ghadeer Land", datetime(2024, 7, 22), datetime(2025, 7, 22))

    # Add expenses
    land_price = project.add_expense("Land Price from Auction", 1885908, datetime(2024, 7, 22))
    price_increase = project.add_expense("Price Increase after Auction", 178102, datetime(2024, 7, 22))
    auction_fees = project.add_expense("Auction Agent Fees", 54221, datetime(2024, 7, 22))
    vat = project.add_expense("VAT", 94295, datetime(2024, 7, 22))
    agent_fees = project.add_expense("Agent Fees", 52955, datetime(2024, 7, 22))

    # Add partners
    hussain_alsalim = project.add_partner("Hussain AlSalim", 1000000)
    ali_alfaraj = project.add_partner("Ali AlFaraj", 500000)
    saleh_alnasser = project.add_partner("Saleh AlNasser", 440000)
    ali_aldawood = project.add_partner("Ali AlDawood", 205481)
    mohammed_alhawaj = project.add_partner("Mohammed AlHawaj", 120000)

    # Add payments
    project.add_payment(52955, datetime(2024, 7, 22), hussain_alsalim, agent_fees)

    # Add a sale
    # project.add_sale(1250000, datetime(2025, 6, 1), "Duplex 1 Sale")

    # Print partner summary
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
    expense_summary = project.get_expense_summary()
    for description, details in expense_summary.items():
        print(f"Expense: {description}")
        print(f"Total: SAR {details['total']:,.2f}")
        print(f"Paid: SAR {details['paid']:,.2f}")
        print(f"Remaining: SAR {details['remaining']:,.2f}")
        print(f"Status: {details['status'].value}")
        print_separator()
        print()

    # Print project summary
    print(project)


if __name__ == "__main__":
    main()