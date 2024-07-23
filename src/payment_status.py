from enum import Enum


class PaymentStatus(Enum):
    """
    Enum representing the status of a payment.

    Attributes:
        UNPAID: The expense is completely unpaid.
        PARTIALLY_PAID: The expense is partially paid.
        FULLY_PAID: The expense is fully paid.
    """

    UNPAID = "Unpaid"
    PARTIALLY_PAID = "Partially Paid"
    FULLY_PAID = "Fully Paid"
