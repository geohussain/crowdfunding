import re
from typing import Union


class ExpressionEvaluationError(Exception):
    """Raised when expression evaluation fails"""
    pass


class ExpressionEvaluator:
    """
    Evaluates mathematical expressions in configuration values.

    Supports safe evaluation of addition expressions like "153 + 123 + 45.67".
    Only allows numbers, decimal points, plus signs, and whitespace for security.
    """

    # Pattern to match valid mathematical expressions (numbers and addition only)
    VALID_EXPRESSION_PATTERN = re.compile(r'^[\d\s+.]+$')

    # Pattern to extract numbers from expression
    NUMBER_PATTERN = re.compile(r'\d+(?:\.\d+)?')

    @staticmethod
    def evaluate_amount(value: Union[str, int, float]) -> float:
        """
        Evaluate a mathematical expression or return numeric value.

        Args:
            value: The value to evaluate (can be number or string expression)

        Returns:
            Evaluated numeric result as float

        Raises:
            ExpressionEvaluationError: If expression is invalid or evaluation fails
        """
        # If it's already a number, return it as float
        if isinstance(value, (int, float)):
            return float(value)

        # If it's a string, check if it's an expression
        if isinstance(value, str):
            value = value.strip()

            # If it's just a number string, convert directly
            try:
                return float(value)
            except ValueError:
                pass  # Not a simple number, try expression evaluation

            # Validate expression contains only safe characters
            if not ExpressionEvaluator.VALID_EXPRESSION_PATTERN.match(value):
                raise ExpressionEvaluationError(
                    f"Invalid characters in expression '{value}'. "
                    "Only numbers, decimal points, plus signs (+), and spaces are allowed."
                )

            # Check for consecutive operators or other invalid patterns
            if '++' in value or value.startswith('+') or value.endswith('+'):
                raise ExpressionEvaluationError(
                    f"Invalid expression format '{value}'. "
                    "Cannot have consecutive operators or start/end with operators."
                )

            # Extract all numbers from the expression
            numbers = ExpressionEvaluator.NUMBER_PATTERN.findall(value)

            if not numbers:
                raise ExpressionEvaluationError(f"No valid numbers found in expression '{value}'")

            # Verify the expression only contains numbers and plus signs by reconstructing
            reconstructed = ' + '.join(numbers)
            normalized_original = re.sub(r'\s+', ' ', value.replace('+', ' + ')).strip()
            normalized_reconstructed = reconstructed

            # Convert both to same format for comparison
            original_parts = [part.strip() for part in normalized_original.split('+')]
            reconstructed_parts = [part.strip() for part in normalized_reconstructed.split('+')]

            if len(original_parts) != len(reconstructed_parts):
                raise ExpressionEvaluationError(f"Invalid expression structure '{value}'")

            # Sum all the numbers
            try:
                total = sum(float(num) for num in numbers)
                return total
            except ValueError as e:
                raise ExpressionEvaluationError(f"Failed to evaluate numbers in expression '{value}': {e}")

        # If it's neither string nor number
        raise ExpressionEvaluationError(f"Unsupported value type for amount: {type(value)}")

    @staticmethod
    def is_expression(value: Union[str, int, float]) -> bool:
        """
        Check if a value is a mathematical expression (contains + operator).

        Args:
            value: The value to check

        Returns:
            True if value is a string expression, False otherwise
        """
        return isinstance(value, str) and '+' in value

    @staticmethod
    def validate_expression(value: str) -> bool:
        """
        Validate that an expression is safe and correctly formatted.

        Args:
            value: The expression string to validate

        Returns:
            True if expression is valid, False otherwise
        """
        try:
            ExpressionEvaluator.evaluate_amount(value)
            return True
        except ExpressionEvaluationError:
            return False