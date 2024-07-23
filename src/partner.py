from dataclasses import dataclass


@dataclass
class Partner:
    """
    Represents a partner in the crowdfunding project.

    Attributes:
        name (str): The name of the partner.
        investment_amount (float): The amount invested by the partner.
    """

    name: str
    investment_amount: float
