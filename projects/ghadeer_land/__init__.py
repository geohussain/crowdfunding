from datetime import datetime
from src.crowdfunding_project import CrowdfundingProject
from .expenses import add_expenses
from .partners import add_partners
from .payments import add_payments


def create_ghadeer_land_project():
    """Create and configure the Ghadeer Land project"""
    project = CrowdfundingProject("Ghadeer Land", datetime(2024, 7, 22), datetime(2025, 7, 22))
    
    # Add expenses and get expense references
    expenses = add_expenses(project)
    
    # Add partners and get partner references  
    partners = add_partners(project)
    
    # Add payments using the expense and partner references
    add_payments(project, partners, expenses)
    
    return project