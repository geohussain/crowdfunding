from datetime import datetime
from typing import Dict, Any

from .crowdfunding_project import CrowdfundingProject
from .config_loader import ConfigLoader
from .expression_evaluator import ExpressionEvaluator


class ProjectFactory:
    """
    Factory class for creating CrowdfundingProject instances from configuration files.

    Handles the complete process of loading, validating, and instantiating a project
    from a YAML configuration file.
    """

    @staticmethod
    def create_from_config(config_path: str) -> CrowdfundingProject:
        """
        Create a CrowdfundingProject instance from a YAML configuration file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Fully configured CrowdfundingProject instance

        Raises:
            ConfigValidationError: If configuration validation fails
            FileNotFoundError: If config file doesn't exist
        """
        # Load and validate configuration
        config = ConfigLoader.load_config(config_path)

        # Create project instance
        project = ProjectFactory._create_project(config['project'])

        # Add partners and create lookup dictionary
        partners = ProjectFactory._add_partners(project, config['partners'])

        # Add expenses and create lookup dictionary
        expenses = ProjectFactory._add_expenses(project, config['expenses'])

        # Add payments using partner and expense references
        ProjectFactory._add_payments(project, config['payments'], partners, expenses)

        return project

    @staticmethod
    def _create_project(project_config: Dict[str, Any]) -> CrowdfundingProject:
        """Create the base CrowdfundingProject instance from project configuration"""
        name = project_config['name']
        start_date = datetime.strptime(project_config['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(project_config['end_date'], '%Y-%m-%d')

        return CrowdfundingProject(name, start_date, end_date)

    @staticmethod
    def _add_partners(project: CrowdfundingProject, partners_config: list) -> Dict[str, Any]:
        """
        Add partners to the project and return a lookup dictionary.

        Args:
            project: CrowdfundingProject instance to add partners to
            partners_config: List of partner configurations

        Returns:
            Dictionary mapping partner names to Partner instances
        """
        partners = {}

        for partner_config in partners_config:
            name = partner_config['name']
            investment_amount = ExpressionEvaluator.evaluate_amount(partner_config['investment_amount'])

            partner = project.add_partner(name, investment_amount)
            partners[name] = partner

        return partners

    @staticmethod
    def _add_expenses(project: CrowdfundingProject, expenses_config: list) -> Dict[str, Any]:
        """
        Add expenses to the project and return a lookup dictionary.

        Args:
            project: CrowdfundingProject instance to add expenses to
            expenses_config: List of expense configurations

        Returns:
            Dictionary mapping expense descriptions to Expense instances
        """
        expenses = {}

        for expense_config in expenses_config:
            description = expense_config['description']
            amount = ExpressionEvaluator.evaluate_amount(expense_config['amount'])
            date = datetime.strptime(expense_config['date'], '%Y-%m-%d')

            expense = project.add_expense(description, amount, date)
            expenses[description] = expense

        return expenses

    @staticmethod
    def _add_payments(project: CrowdfundingProject, payments_config: list,
                      partners: Dict[str, Any], expenses: Dict[str, Any]) -> None:
        """
        Add payments to the project using partner and expense references.

        Args:
            project: CrowdfundingProject instance to add payments to
            payments_config: List of payment configurations
            partners: Dictionary mapping partner names to Partner instances
            expenses: Dictionary mapping expense descriptions to Expense instances
        """
        for payment_config in payments_config:
            amount = ExpressionEvaluator.evaluate_amount(payment_config['amount'])
            date = datetime.strptime(payment_config['date'], '%Y-%m-%d')
            partner_name = payment_config['partner']
            expense_description = payment_config['expense']

            # Get partner and expense references
            partner = partners[partner_name]
            expense = expenses[expense_description]

            project.add_payment(amount, date, partner, expense)