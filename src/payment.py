from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .partner import Partner
from .expense import Expense


@dataclass
class Payment:
    """
    Represents a payment in the crowdfunding project.

    Attributes:
        amount (float): The amount of the payment.
        date (datetime): The date when the payment was made.
        partner (Partner): The partner who made the payment.
        expense (Optional[Expense]): The expense associated with the payment, if any.
    """

    amount: float
    date: datetime
    partner: Partner
    expense: Optional[Expense] = None
