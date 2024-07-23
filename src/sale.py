from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sale:
    """
    Represents a sale in the crowdfunding project.

    Attributes:
        amount (float): The amount of the sale.
        date (datetime): The date when the sale occurred.
        description (str): A brief description of the sale.
    """

    amount: float
    date: datetime
    description: str
