from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .expense import Expense
from .partner import Partner
from .payment import Payment
from .sale import Sale
from .payment_status import PaymentStatus
from .helpers import separator, encapsulate_as_text_header, format_currency, create_table_row, create_section_divider


@dataclass
class CrowdfundingProject:
    """
    Represents a crowdfunding project for real estate.

    This class manages expenses, payments, partners, and sales related to the project.
    It provides methods to add new items, calculate totals, and generate summaries.

    Attributes:
        name (str): The name of the crowdfunding project.
        start_date (datetime): The start date of the project.
        end_date (datetime): The end date of the project.
        expenses (List[Expense]): A list of expenses associated with the project.
        payments (List[Payment]): A list of payments made in the project.
        partners (List[Partner]): A list of partners involved in the project.
        sales (List[Sale]): A list of sales made in the project.
    """

    name: str
    start_date: datetime
    end_date: datetime
    expenses: List[Expense] = field(default_factory=list)
    payments: List[Payment] = field(default_factory=list)
    partners: List[Partner] = field(default_factory=list)
    sales: List[Sale] = field(default_factory=list)

    def add_expense(self, description: str, amount: float, date: datetime) -> Expense:
        """
        Add a new expense to the project.

        Args:
            description (str): A brief description of the expense.
            amount (float): The monetary amount of the expense.
            date (datetime): The date when the expense occurred.

        Returns:
            Expense: The newly created Expense object.
        """
        expense = Expense(description, amount, date)
        self.expenses.append(expense)
        return expense

    def add_partner(self, name: str, investment_amount: float) -> Partner:
        """
        Add a new partner to the project.

        Args:
            name (str): The name of the partner.
            investment_amount (float): The amount invested by the partner.

        Returns:
            Partner: The newly created Partner object.
        """
        partner = Partner(name, investment_amount)
        self.partners.append(partner)
        return partner

    def add_payment(self, amount: float, date: datetime, partner: Partner,
                    expense: Optional[Expense] = None) -> Payment:
        """
        Adds a payment to the list of payments.

        :param amount: The amount of the payment.
        :type amount: float
        :param date: The date of the payment.
        :type date: datetime
        :param partner: The partner associated with the payment.
        :type partner: Partner
        :param expense: The expense associated with the payment, if any. (default: None)
        :type expense: Optional[Expense]

        :return: The new payment object that was added.
        :rtype: Payment
        """
        payment = Payment(amount, date, partner, expense)
        self.payments.append(payment)
        return payment

    def add_sale(self, amount: float, date: datetime, description: str) -> Sale:
        """
        Method to add a sale to the sales list.

        :param amount: The amount of the sale.
        :type amount: float
        :param date: The date of the sale.
        :type date: datetime
        :param description: The description of the sale.
        :type description: str

        :return: The created Sale object.
        :rtype: Sale
        """
        sale = Sale(amount, date, description)
        self.sales.append(sale)
        return sale

    def total_expenses(self) -> float:
        """Calculate the total amount of all expenses."""
        return sum(expense.amount for expense in self.expenses)

    def total_payments(self) -> float:
        """Calculate the total amount of all payments."""
        return sum(payment.amount for payment in self.payments)

    def total_investments(self) -> float:
        """Calculate the total amount invested by all partners."""
        return sum(partner.investment_amount for partner in self.partners)

    def total_sales(self) -> float:
        """Calculate the total amount of all sales."""
        return sum(sale.amount for sale in self.sales)

    def project_balance(self) -> float:
        """Calculate the current balance of the project."""
        return self.total_sales() - self.total_payments()

    def target_amount(self) -> float:
        """Calculate the target amount based on total expenses."""
        return self.total_expenses()

    def calculate_ownership_percentages(self) -> Dict[str, float]:
        """
        Calculate the ownership percentage for each partner based on their investment.

        Returns:
            Dict[str, float]: A dictionary with partner names as keys and their ownership percentages as values.
        """
        total_investment = self.total_investments()
        if total_investment == 0:
            return {partner.name: 0 for partner in self.partners}
        return {
            partner.name: (partner.investment_amount / total_investment) * 100
            for partner in self.partners
        }

    def get_partner_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Generate a summary of all partners, including their investments, ownership percentages, and total payments.

        Returns:
            Dict[str, Dict[str, float]]: A dictionary with partner names as keys and their summary details as values.
        """
        ownership_percentages = self.calculate_ownership_percentages()
        return {
            partner.name: {
                "investment": partner.investment_amount,
                "ownership_percentage": ownership_percentages[partner.name],
                "total_payments": sum(payment.amount for payment in self.payments if payment.partner == partner),
                "investment_balance": partner.investment_amount -
                           sum(payment.amount for payment in self.payments if payment.partner == partner)
            }
            for partner in self.partners
        }

    def get_expense_summary(self) -> Dict[str, Dict[str, float | PaymentStatus]]:
        """
        Generate a summary of all expenses, including their total amounts, paid amounts, remaining amounts, and payment status.

        Returns:
            Dict[str, Dict[str, float | PaymentStatus]]: A dictionary with expense descriptions as keys and their summary details as values.
        """
        expense_summary = {}
        for expense in self.expenses:
            paid_amount = sum(payment.amount for payment in self.payments if payment.expense == expense)
            remaining = expense.amount - paid_amount

            if remaining == expense.amount:
                status = PaymentStatus.UNPAID
            elif remaining == 0:
                status = PaymentStatus.FULLY_PAID
            else:
                status = PaymentStatus.PARTIALLY_PAID

            expense_summary[expense.description] = {
                "total": expense.amount,
                "paid": paid_amount,
                "remaining": remaining,
                "status": status
            }
        return expense_summary


    def get_payment_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get the payments summary.

        :return: A dictionary containing payment summary.
                 Each key represents a payment number and its corresponding value is a dictionary
                    containing the payment details.
                    The payment details include the payment date, partner name, payment amount, and expense description.
        :rtype: dict
        """
        return {
            f"Payment #{i+1}": {
                "date": payment.date.date(),
                "partner": payment.partner.name,
                "amount": payment.amount,
                "expense": payment.expense.description,
                "percentage": payment.amount / payment.expense.amount * 100
            }
            for i, payment in enumerate(self.payments)
        }

    def _format_relative_date(self, date: datetime) -> str:
        """
        Format a date as a relative time string with months and years support.
        
        Args:
            date: The date to format
            
        Returns:
            str: Formatted relative date string
        """
        today = datetime.now().date()
        target_date = date.date()
        
        diff = (today - target_date).days
        
        if diff == 0:
            return f"today ({target_date})"
        elif diff == 1:
            return f"yesterday ({target_date})"
        elif diff == -1:
            return f"tomorrow ({target_date})"
        elif diff > 1:
            # Calculate years, months, and days
            years = diff // 365
            remaining_days = diff % 365
            months = remaining_days // 30
            days = remaining_days % 30
            
            parts = []
            if years > 0:
                parts.append(f"{years} year{'s' if years != 1 else ''}")
            if months > 0:
                parts.append(f"{months} month{'s' if months != 1 else ''}")
            if days > 0 or not parts:  # Show days if no years/months, or if there are remaining days
                parts.append(f"{days} day{'s' if days != 1 else ''}")
            
            if len(parts) > 1:
                time_str = ", ".join(parts[:-1]) + f" and {parts[-1]} ago"
            else:
                time_str = f"{parts[0]} ago"
                
            return f"{time_str} ({target_date})"
        else:
            # Future dates
            abs_diff = abs(diff)
            years = abs_diff // 365
            remaining_days = abs_diff % 365
            months = remaining_days // 30
            days = remaining_days % 30
            
            parts = []
            if years > 0:
                parts.append(f"{years} year{'s' if years != 1 else ''}")
            if months > 0:
                parts.append(f"{months} month{'s' if months != 1 else ''}")
            if days > 0 or not parts:
                parts.append(f"{days} day{'s' if days != 1 else ''}")
            
            if len(parts) > 1:
                time_str = "in " + ", ".join(parts[:-1]) + f" and {parts[-1]}"
            else:
                time_str = f"in {parts[0]}"
                
            return f"{time_str} ({target_date})"

    def get_sale_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Generate a summary of all sales, including their total amounts and descriptions.

        Returns:
            Dict[str, Dict[str, float]]: A dictionary with sale descriptions as keys and their summary details as values.
        """
        return {
            sale.description: {
                "date": sale.date.date(),
                "total": sale.amount
            }
            for sale in self.sales
        }

    def print_partner_summary(self):
        """
        Print the summary of partners.

        :return: None
        """
        print(encapsulate_as_text_header("Partners Summary"))
        print()
        
        partner_summary = self.get_partner_summary()
        
        # Table header
        print(create_table_row("Partner", "Investment Plan", "Ownership %", "Total Payments", "Balance", 
                              widths=[20, 18, 12, 18, 18], align='left'))
        print('├' + '─' * 20 + '┼' + '─' * 18 + '┼' + '─' * 12 + '┼' + '─' * 18 + '┼' + '─' * 18 + '┤')
        
        for name, details in partner_summary.items():
            investment = format_currency(details['investment'])
            payments = format_currency(details['total_payments'])
            balance = format_currency(details['investment_balance'])
            ownership = f"{details['ownership_percentage']:.2f}%"
            
            print(create_table_row(name, investment, ownership, payments, balance,
                                 widths=[20, 18, 12, 18, 18], align='left'))
        
        print('└' + '─' * 20 + '┴' + '─' * 18 + '┴' + '─' * 12 + '┴' + '─' * 18 + '┴' + '─' * 18 + '┘')
        print()

    def print_expense_summary(self):
        """
        Prints the summary of expenses.

        :return: None
        """
        print(encapsulate_as_text_header("Expenses Summary"))
        expense_summary = self.get_expense_summary()
        for description, details in expense_summary.items():
            print(f"Expense: {description}")
            print(f"Total: SAR {details['total']:,.2f}")
            print(f"Paid: SAR {details['paid']:,.2f}")
            print(f"Remaining: SAR {details['remaining']:,.2f}")
            print(f"Status: {details['status'].value}")
            print(separator())
        print()

    def print_payment_summary(self):
        """
        Print the payment summary.

        :return: None
        """
        print(encapsulate_as_text_header("Payments Summary"))
        payment_summary = self.get_payment_summary()
        for description, details in payment_summary.items():
            print(f"Payment: {description}")
            print(f"Date: {details['date']}")
            print(f"Partner: {details['partner']}")
            print(f"Amount: SAR {details['amount']:,.2f}")
            print(f"Expense: {details['expense']}" + f" ({details['percentage']:,.2f}%)")
            print(separator())
        print()

    def print_expenses_by_date(self, since: datetime = None):
        """
        Print expenses sorted by date from oldest to newest with relative date formatting.
        
        Args:
            since (datetime, optional): Only show expenses from this date onwards
        """
        print(encapsulate_as_text_header("Expenses by Date"))
        print()
        
        # Sort expenses by date
        sorted_expenses = sorted(self.expenses, key=lambda x: x.date)
        
        # Filter by since date if provided
        if since:
            sorted_expenses = [exp for exp in sorted_expenses if exp.date >= since]
            print(f"📅 Showing expenses since: {self._format_relative_date(since)}")
            print(separator())
        
        current_month = None
        for expense in sorted_expenses:
            expense_month = expense.date.strftime("%B %Y")
            
            # Group by month
            if current_month != expense_month:
                if current_month is not None:
                    print()
                print(create_section_divider(expense_month))
                current_month = expense_month
                
            paid_amount = sum(payment.amount for payment in self.payments if payment.expense == expense)
            remaining = expense.amount - paid_amount
            
            if remaining == expense.amount:
                status = PaymentStatus.UNPAID
                status_icon = "❌"
            elif remaining == 0:
                status = PaymentStatus.FULLY_PAID
                status_icon = "✅"
            else:
                status = PaymentStatus.PARTIALLY_PAID
                status_icon = "⚠️"
            
            print(f"│ 📅 {self._format_relative_date(expense.date)}")
            print(f"│ 💰 {expense.description}")
            print(f"│ 📊 Total: {format_currency(expense.amount)} │ Paid: {format_currency(paid_amount)} │ Remaining: {format_currency(remaining)}")
            print(f"│ {status_icon} Status: {status.value}")
            print('├' + '─' * 48 + '┤')
        print('└' + '─' * 48 + '┘')
        print()

    def print_payments_by_date(self, since: datetime = None):
        """
        Print payments sorted by date from oldest to newest with relative date formatting.
        
        Args:
            since (datetime, optional): Only show payments from this date onwards
        """
        print(encapsulate_as_text_header("Payments by Date"))
        print()
        
        # Sort payments by date
        sorted_payments = sorted(self.payments, key=lambda x: x.date)
        
        # Filter by since date if provided
        if since:
            sorted_payments = [payment for payment in sorted_payments if payment.date >= since]
            print(f"📅 Showing payments since: {self._format_relative_date(since)}")
            print(separator())
        
        current_month = None
        for i, payment in enumerate(sorted_payments):
            payment_month = payment.date.strftime("%B %Y")
            
            # Group by month
            if current_month != payment_month:
                if current_month is not None:
                    print()
                print(create_section_divider(payment_month))
                current_month = payment_month
            
            percentage = payment.amount / payment.expense.amount * 100 if payment.expense else 0
            
            print(f"│ 💳 Payment #{i+1}")
            print(f"│ 📅 {self._format_relative_date(payment.date)}")
            print(f"│ 👤 Partner: {payment.partner.name}")
            print(f"│ 💰 Amount: {format_currency(payment.amount)}")
            if payment.expense:
                print(f"│ 📋 Expense: {payment.expense.description} ({percentage:,.1f}%)")
            else:
                print("│ 📋 Expense: Not specified")
            print('├' + '─' * 48 + '┤')
        print('└' + '─' * 48 + '┘')
        print()

    def print_sale_summary(self):
        """
        Prints the sales summary and partner details for each sale.

        :return: None
        """
        print(encapsulate_as_text_header("Sales Summary"))
        sales_summary = self.get_sale_summary()
        partner_summary = self.get_partner_summary()

        for sale, details in sales_summary.items():
            print(f"Sale: {sale}")
            print(f"Date: {details['date']}")
            print(f"Total: SAR {details['total']:,.2f}")
            print(separator())
            print()

            for name, partner_details in partner_summary.items():
                ownership_percentage = partner_details['ownership_percentage']
                amount = details['total'] * ownership_percentage / 100
                print(f"Partner: {name}")
                print(f"Amount based on ownership percentage of {ownership_percentage:,.2f} % : SAR {amount:,.2f}")
                print(separator())
            print()

    def __str__(self) -> str:
        """
        Generate a string representation of the CrowdfundingProject.

        Returns:
            str: A formatted string containing key information about the project.
        """
        gains_pct = self.project_balance() / self.total_payments() * 100 if self.total_payments() > 0 else 0
        remaining_expenses = self.total_expenses() - self.total_payments()
        
        # Status indicators
        balance_icon = "📈" if self.project_balance() >= 0 else "📉"
        completion_pct = (self.total_payments() / self.total_expenses() * 100) if self.total_expenses() > 0 else 0
        completion_icon = "✅" if completion_pct >= 100 else "🚧" if completion_pct >= 50 else "⏳"
        
        return (
            encapsulate_as_text_header("Project Summary") + "\n\n"
            f"🏗️  Project: {self.name}\n"
            f"🎯  Target Amount: {format_currency(self.target_amount())}\n"
            f"📅  Duration: {self.start_date.date()} → {self.end_date.date()}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰  Total Investments Plan: {format_currency(self.total_investments())}\n"
            f"📊  Total Expenses: {format_currency(self.total_expenses())}\n"
            f"💳  Total Payments: {format_currency(self.total_payments())}\n"
            f"💵  Total Sales: {format_currency(self.total_sales())}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{balance_icon}  Current Balance: {format_currency(self.project_balance())}\n"
            f"📈  Gains Percentage: {gains_pct:,.2f}%\n"
            f"{completion_icon}  Project Completion: {completion_pct:.1f}%\n"
            f"⏳  Remaining Expenses: {format_currency(remaining_expenses)}"
        )
