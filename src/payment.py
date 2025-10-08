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
        partner (Optional[Partner]): The partner who made the payment (None if from_sales=True).
        expense (Optional[Expense]): The expense associated with the payment, if any.
        from_sales (bool): Whether this payment comes from sales revenue instead of partner investment.
    """

    amount: float
    date: datetime
    partner: Optional[Partner] = None
    expense: Optional[Expense] = None
    from_sales: bool = False

    def __post_init__(self):
        """Validate payment data after initialization."""
        if self.from_sales and self.partner is not None:
            raise ValueError("Payment from sales cannot have an associated partner")
        if not self.from_sales and self.partner is None:
            raise ValueError("Payment not from sales must have an associated partner")
        if self.amount <= 0:
            raise ValueError("Payment amount must be positive")
