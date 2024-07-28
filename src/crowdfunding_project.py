from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from .expense import Expense
from .partner import Partner
from .payment import Payment
from .sale import Sale
from .payment_status import PaymentStatus
from .helpers import separator, encapsulate_as_text_header


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

    def add_payment(self, amount: float, date: datetime, partner: Partner, expense: Optional[Expense] = None) -> None:
        """
        Add a new payment to the project.

        Args:
            amount (float): The amount of the payment.
            date (datetime): The date when the payment was made.
            partner (Partner): The partner who made the payment.
            expense (Optional[Expense]): The expense associated with the payment, if any.
        """
        self.payments.append(Payment(amount, date, partner, expense))

    def add_sale(self, amount: float, date: datetime, description: str) -> None:
        """
        Add a new sale to the project.

        Args:
            amount (float): The amount of the sale.
            date (datetime): The date when the sale occurred.
            description (str): A brief description of the sale.
        """
        self.sales.append(Sale(amount, date, description))

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
        print(encapsulate_as_text_header("Partners Summary"))
        partner_summary = self.get_partner_summary()
        for name, details in partner_summary.items():
            print(f"Partner: {name}")
            print(f"Investment Plan: SAR {details['investment']:,.2f}")
            print(f"Ownership Percentage: {details['ownership_percentage']:.2f}%")
            print(f"Total Payments: SAR {details['total_payments']:,.2f}")
            print(f"Investment Balance: SAR {details['investment_balance']:,.2f}")
            print(separator())
        print()

    def print_expense_summary(self):
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

    def print_sale_summary(self):
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
        return (
            encapsulate_as_text_header("Project Summary") + "\n"
            f"Crowdfunding Project: {self.name}\n"
            f"Target Amount: SAR {self.target_amount():,.2f}\n"
            f"Start Date: {self.start_date.date()}\n"
            f"End Date: {self.end_date.date()}\n"
            f"Total Investments Plan: SAR {self.total_investments():,.2f}\n"
            f"Total Expenses: SAR {self.total_expenses():,.2f}\n"
            f"Total Payments: SAR {self.total_payments():,.2f}\n"
            f"Total Sales: SAR {self.total_sales():,.2f}\n"
            f"Current Balance: SAR {self.project_balance():,.2f}\n"
            f"Gains Percentage: {self.project_balance() / self.total_payments() * 100:,.2f} %\n"
            f"Remaining Total Expenses: SAR {self.total_expenses() - self.total_payments():,.2f}"
        )
