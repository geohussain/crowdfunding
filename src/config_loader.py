import yaml
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from .expression_evaluator import ExpressionEvaluator, ExpressionEvaluationError


class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


class ConfigLoader:
    """
    Loads and validates YAML configuration files for crowdfunding projects.

    Provides schema validation and error handling for project configurations.
    """

    REQUIRED_PROJECT_FIELDS = ['name', 'start_date', 'end_date']
    REQUIRED_PARTNER_FIELDS = ['name', 'investment_amount']
    REQUIRED_EXPENSE_FIELDS = ['description', 'amount', 'date']
    REQUIRED_PAYMENT_FIELDS = ['amount', 'date', 'partner', 'expense']

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load and validate a YAML configuration file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Validated configuration dictionary

        Raises:
            ConfigValidationError: If validation fails
            FileNotFoundError: If config file doesn't exist
        """
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Invalid YAML syntax: {e}")

        ConfigLoader._validate_config(config, config_path)
        return config

    @staticmethod
    def _validate_config(config: Dict[str, Any], config_path: str) -> None:
        """
        Validate the loaded configuration structure and content.

        Args:
            config: Configuration dictionary to validate
            config_path: Path for error reporting

        Raises:
            ConfigValidationError: If validation fails
        """
        if not isinstance(config, dict):
            raise ConfigValidationError("Configuration must be a dictionary")

        # Validate top-level sections
        required_sections = ['project', 'partners', 'expenses', 'payments']
        for section in required_sections:
            if section not in config:
                raise ConfigValidationError(f"Missing required section: {section}")

        # Validate project section
        ConfigLoader._validate_project(config['project'])

        # Validate partners section
        ConfigLoader._validate_partners(config['partners'])

        # Validate expenses section
        ConfigLoader._validate_expenses(config['expenses'])

        # Validate payments section
        ConfigLoader._validate_payments(config['payments'], config['partners'], config['expenses'])

    @staticmethod
    def _validate_project(project: Dict[str, Any]) -> None:
        """Validate project configuration section"""
        if not isinstance(project, dict):
            raise ConfigValidationError("Project section must be a dictionary")

        for field in ConfigLoader.REQUIRED_PROJECT_FIELDS:
            if field not in project:
                raise ConfigValidationError(f"Missing required project field: {field}")

        # Validate dates
        try:
            start_date = datetime.strptime(project['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(project['end_date'], '%Y-%m-%d')

            if end_date <= start_date:
                raise ConfigValidationError("Project end_date must be after start_date")

        except ValueError as e:
            raise ConfigValidationError(f"Invalid date format (use YYYY-MM-DD): {e}")

    @staticmethod
    def _validate_partners(partners: List[Dict[str, Any]]) -> None:
        """Validate partners configuration section"""
        if not isinstance(partners, list):
            raise ConfigValidationError("Partners section must be a list")

        if not partners:
            raise ConfigValidationError("At least one partner is required")

        partner_names = set()
        for i, partner in enumerate(partners):
            if not isinstance(partner, dict):
                raise ConfigValidationError(f"Partner {i + 1} must be a dictionary")

            for field in ConfigLoader.REQUIRED_PARTNER_FIELDS:
                if field not in partner:
                    raise ConfigValidationError(f"Partner {i + 1} missing required field: {field}")

            # Check for duplicate partner names
            name = partner['name']
            if name in partner_names:
                raise ConfigValidationError(f"Duplicate partner name: {name}")
            partner_names.add(name)

            # Validate investment amount (support expressions)
            try:
                amount = ExpressionEvaluator.evaluate_amount(partner['investment_amount'])
                if amount <= 0:
                    raise ConfigValidationError(f"Partner '{name}' investment_amount must be positive")
            except ExpressionEvaluationError as e:
                raise ConfigValidationError(f"Partner '{name}' investment_amount error: {e}")
            except (ValueError, TypeError):
                raise ConfigValidationError(f"Partner '{name}' investment_amount must be a number or expression")

    @staticmethod
    def _validate_expenses(expenses: List[Dict[str, Any]]) -> None:
        """Validate expenses configuration section"""
        if not isinstance(expenses, list):
            raise ConfigValidationError("Expenses section must be a list")

        if not expenses:
            raise ConfigValidationError("At least one expense is required")

        expense_descriptions = set()
        for i, expense in enumerate(expenses):
            if not isinstance(expense, dict):
                raise ConfigValidationError(f"Expense {i + 1} must be a dictionary")

            for field in ConfigLoader.REQUIRED_EXPENSE_FIELDS:
                if field not in expense:
                    raise ConfigValidationError(f"Expense {i + 1} missing required field: {field}")

            # Check for duplicate descriptions
            description = expense['description']
            if description in expense_descriptions:
                raise ConfigValidationError(f"Duplicate expense description: {description}")
            expense_descriptions.add(description)

            # Validate amount (support expressions)
            try:
                amount = ExpressionEvaluator.evaluate_amount(expense['amount'])
                if amount <= 0:
                    raise ConfigValidationError(f"Expense '{description}' amount must be positive")
            except ExpressionEvaluationError as e:
                raise ConfigValidationError(f"Expense '{description}' amount error: {e}")
            except (ValueError, TypeError):
                raise ConfigValidationError(f"Expense '{description}' amount must be a number or expression")

            # Validate date
            try:
                datetime.strptime(expense['date'], '%Y-%m-%d')
            except ValueError:
                raise ConfigValidationError(f"Expense '{description}' has invalid date format (use YYYY-MM-DD)")

    @staticmethod
    def _validate_payments(payments: List[Dict[str, Any]], partners: List[Dict[str, Any]],
                          expenses: List[Dict[str, Any]]) -> None:
        """Validate payments configuration section"""
        if not isinstance(payments, list):
            raise ConfigValidationError("Payments section must be a list")

        if not payments:
            raise ConfigValidationError("At least one payment is required")

        # Create lookup sets for validation
        partner_names = {p['name'] for p in partners}
        expense_descriptions = {e['description'] for e in expenses}

        for i, payment in enumerate(payments):
            if not isinstance(payment, dict):
                raise ConfigValidationError(f"Payment {i + 1} must be a dictionary")

            for field in ConfigLoader.REQUIRED_PAYMENT_FIELDS:
                if field not in payment:
                    raise ConfigValidationError(f"Payment {i + 1} missing required field: {field}")

            # Validate amount (support expressions)
            try:
                amount = ExpressionEvaluator.evaluate_amount(payment['amount'])
                if amount <= 0:
                    raise ConfigValidationError(f"Payment {i + 1} amount must be positive")
            except ExpressionEvaluationError as e:
                raise ConfigValidationError(f"Payment {i + 1} amount error: {e}")
            except (ValueError, TypeError):
                raise ConfigValidationError(f"Payment {i + 1} amount must be a number or expression")

            # Validate date
            try:
                datetime.strptime(payment['date'], '%Y-%m-%d')
            except ValueError:
                raise ConfigValidationError(f"Payment {i + 1} has invalid date format (use YYYY-MM-DD)")

            # Validate partner reference
            partner_name = payment['partner']
            if partner_name not in partner_names:
                raise ConfigValidationError(f"Payment {i + 1} references unknown partner: {partner_name}")

            # Validate expense reference
            expense_description = payment['expense']
            if expense_description not in expense_descriptions:
                raise ConfigValidationError(f"Payment {i + 1} references unknown expense: {expense_description}")