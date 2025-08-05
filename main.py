from projects.ghadeer_land import create_ghadeer_land_project
from datetime import datetime


def main():
    # Create the Ghadeer Land project
    project = create_ghadeer_land_project()

    # Print all summaries
    project.print_partner_summary()
    # project.print_expense_summary()
    # project.print_payment_summary()
    
    # Print date-sorted summaries
    project.print_expenses_by_date()
    project.print_payments_by_date()
    
    # Example: Show only expenses/payments since a specific date
    # project.print_expenses_by_date(since=datetime(2025, 6, 1))
    # project.print_payments_by_date(since=datetime(2025, 6, 1))
    
    print(project)


if __name__ == "__main__":
    main()