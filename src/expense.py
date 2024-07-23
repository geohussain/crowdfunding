from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    """
    Represents an expense in the crowdfunding project.

    Attributes:
        description (str): A brief description of the expense.
        amount (float): The monetary amount of the expense.
        date (datetime): The date when the expense occurred.
    """

    description: str
    amount: float
    date: datetime
