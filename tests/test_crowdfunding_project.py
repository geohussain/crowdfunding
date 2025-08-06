import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from io import StringIO
import sys
import os

# Add the parent directory to sys.path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crowdfunding_project import CrowdfundingProject
from src.expense import Expense
from src.partner import Partner
from src.payment import Payment
from src.sale import Sale
from src.payment_status import PaymentStatus


class TestCrowdfundingProject(unittest.TestCase):
    """Comprehensive test suite for CrowdfundingProject class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 12, 31)
        self.project = CrowdfundingProject(
            name="Test Project",
            start_date=self.start_date,
            end_date=self.end_date
        )

    def test_project_initialization(self):
        """Test proper initialization of CrowdfundingProject."""
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.start_date, self.start_date)
        self.assertEqual(self.project.end_date, self.end_date)
        self.assertEqual(len(self.project.expenses), 0)
        self.assertEqual(len(self.project.payments), 0)
        self.assertEqual(len(self.project.partners), 0)
        self.assertEqual(len(self.project.sales), 0)

    def test_add_expense_basic(self):
        """Test basic expense addition functionality."""
        expense = self.project.add_expense("Test Expense", 1000.0, datetime(2024, 1, 15))
        
        self.assertIsInstance(expense, Expense)
        self.assertEqual(expense.description, "Test Expense")
        self.assertEqual(expense.amount, 1000.0)
        self.assertEqual(expense.date, datetime(2024, 1, 15))
        self.assertEqual(len(self.project.expenses), 1)
        self.assertIn(expense, self.project.expenses)

    def test_add_multiple_expenses(self):
        """Test adding multiple expenses."""
        expense1 = self.project.add_expense("Expense 1", 500.0, datetime(2024, 1, 10))
        expense2 = self.project.add_expense("Expense 2", 750.0, datetime(2024, 2, 15))
        expense3 = self.project.add_expense("Expense 3", 1200.0, datetime(2024, 3, 20))
        
        self.assertEqual(len(self.project.expenses), 3)
        self.assertIn(expense1, self.project.expenses)
        self.assertIn(expense2, self.project.expenses)
        self.assertIn(expense3, self.project.expenses)

    def test_add_partner_basic(self):
        """Test basic partner addition functionality."""
        partner = self.project.add_partner("John Doe", 50000.0)
        
        self.assertIsInstance(partner, Partner)
        self.assertEqual(partner.name, "John Doe")
        self.assertEqual(partner.investment_amount, 50000.0)
        self.assertEqual(len(self.project.partners), 1)
        self.assertIn(partner, self.project.partners)

    def test_add_multiple_partners(self):
        """Test adding multiple partners."""
        partner1 = self.project.add_partner("Alice", 30000.0)
        partner2 = self.project.add_partner("Bob", 20000.0)
        partner3 = self.project.add_partner("Charlie", 50000.0)
        
        self.assertEqual(len(self.project.partners), 3)
        total_investment = sum(p.investment_amount for p in self.project.partners)
        self.assertEqual(total_investment, 100000.0)

    def test_add_payment_basic(self):
        """Test basic payment addition functionality."""
        expense = self.project.add_expense("Test Expense", 1000.0, datetime(2024, 1, 15))
        partner = self.project.add_partner("John Doe", 50000.0)
        
        payment = self.project.add_payment(500.0, datetime(2024, 1, 20), partner, expense)
        
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.amount, 500.0)
        self.assertEqual(payment.date, datetime(2024, 1, 20))
        self.assertEqual(payment.partner, partner)
        self.assertEqual(payment.expense, expense)
        self.assertEqual(len(self.project.payments), 1)

    def test_add_payment_without_expense(self):
        """Test adding payment without linking to specific expense."""
        partner = self.project.add_partner("Jane Doe", 25000.0)
        payment = self.project.add_payment(1000.0, datetime(2024, 2, 10), partner)
        
        self.assertEqual(payment.expense, None)
        self.assertEqual(payment.amount, 1000.0)
        self.assertEqual(payment.partner, partner)

    def test_add_sale_basic(self):
        """Test basic sale addition functionality."""
        sale = self.project.add_sale(75000.0, datetime(2024, 6, 1), "Property Sale #1")
        
        self.assertIsInstance(sale, Sale)
        self.assertEqual(sale.amount, 75000.0)
        self.assertEqual(sale.date, datetime(2024, 6, 1))
        self.assertEqual(sale.description, "Property Sale #1")
        self.assertEqual(len(self.project.sales), 1)

    def test_total_expenses(self):
        """Test calculation of total expenses."""
        self.project.add_expense("Expense 1", 1000.0, datetime(2024, 1, 1))
        self.project.add_expense("Expense 2", 2500.0, datetime(2024, 2, 1))
        self.project.add_expense("Expense 3", 750.0, datetime(2024, 3, 1))
        
        total = self.project.total_expenses()
        self.assertEqual(total, 4250.0)

    def test_total_payments(self):
        """Test calculation of total payments."""
        partner = self.project.add_partner("Test Partner", 10000.0)
        self.project.add_payment(500.0, datetime(2024, 1, 5), partner)
        self.project.add_payment(750.0, datetime(2024, 1, 10), partner)
        self.project.add_payment(1000.0, datetime(2024, 1, 15), partner)
        
        total = self.project.total_payments()
        self.assertEqual(total, 2250.0)

    def test_total_investments(self):
        """Test calculation of total investments."""
        self.project.add_partner("Partner 1", 15000.0)
        self.project.add_partner("Partner 2", 25000.0)
        self.project.add_partner("Partner 3", 10000.0)
        
        total = self.project.total_investments()
        self.assertEqual(total, 50000.0)

    def test_total_sales(self):
        """Test calculation of total sales."""
        self.project.add_sale(20000.0, datetime(2024, 4, 1), "Sale 1")
        self.project.add_sale(30000.0, datetime(2024, 5, 1), "Sale 2")
        self.project.add_sale(15000.0, datetime(2024, 6, 1), "Sale 3")
        
        total = self.project.total_sales()
        self.assertEqual(total, 65000.0)

    def test_project_balance(self):
        """Test project balance calculation (sales - payments)."""
        partner = self.project.add_partner("Partner", 10000.0)
        self.project.add_payment(5000.0, datetime(2024, 1, 1), partner)
        self.project.add_sale(8000.0, datetime(2024, 2, 1), "Sale")
        
        balance = self.project.project_balance()
        self.assertEqual(balance, 3000.0)  # 8000 - 5000

    def test_target_amount(self):
        """Test target amount calculation (total expenses)."""
        self.project.add_expense("Expense 1", 2000.0, datetime(2024, 1, 1))
        self.project.add_expense("Expense 2", 3000.0, datetime(2024, 2, 1))
        
        target = self.project.target_amount()
        self.assertEqual(target, 5000.0)

    def test_calculate_ownership_percentages_basic(self):
        """Test basic ownership percentage calculation."""
        self.project.add_partner("Partner A", 30000.0)  # 60%
        self.project.add_partner("Partner B", 20000.0)  # 40%
        
        percentages = self.project.calculate_ownership_percentages()
        
        self.assertEqual(len(percentages), 2)
        self.assertAlmostEqual(percentages["Partner A"], 60.0, places=1)
        self.assertAlmostEqual(percentages["Partner B"], 40.0, places=1)

    def test_calculate_ownership_percentages_zero_investment(self):
        """Test ownership percentage calculation with zero total investment."""
        percentages = self.project.calculate_ownership_percentages()
        self.assertEqual(percentages, {})

    def test_calculate_ownership_percentages_multiple_partners(self):
        """Test ownership percentage calculation with multiple partners."""
        self.project.add_partner("Alice", 25000.0)   # 25%
        self.project.add_partner("Bob", 50000.0)     # 50%
        self.project.add_partner("Charlie", 15000.0) # 15%
        self.project.add_partner("Diana", 10000.0)   # 10%
        
        percentages = self.project.calculate_ownership_percentages()
        
        self.assertAlmostEqual(percentages["Alice"], 25.0, places=1)
        self.assertAlmostEqual(percentages["Bob"], 50.0, places=1)
        self.assertAlmostEqual(percentages["Charlie"], 15.0, places=1)
        self.assertAlmostEqual(percentages["Diana"], 10.0, places=1)
        
        # Total should be 100%
        total_percentage = sum(percentages.values())
        self.assertAlmostEqual(total_percentage, 100.0, places=1)

    def test_get_partner_summary(self):
        """Test partner summary generation."""
        partner1 = self.project.add_partner("John", 40000.0)
        partner2 = self.project.add_partner("Jane", 60000.0)
        
        expense = self.project.add_expense("Test Expense", 5000.0, datetime(2024, 1, 1))
        self.project.add_payment(2000.0, datetime(2024, 1, 5), partner1, expense)
        self.project.add_payment(1500.0, datetime(2024, 1, 10), partner2, expense)
        
        summary = self.project.get_partner_summary()
        
        self.assertIn("John", summary)
        self.assertIn("Jane", summary)
        
        john_summary = summary["John"]
        self.assertEqual(john_summary["investment"], 40000.0)
        self.assertEqual(john_summary["total_payments"], 2000.0)
        self.assertEqual(john_summary["investment_balance"], 38000.0)
        self.assertAlmostEqual(john_summary["ownership_percentage"], 40.0, places=1)

    def test_get_expense_summary(self):
        """Test expense summary generation."""
        expense1 = self.project.add_expense("Expense 1", 1000.0, datetime(2024, 1, 1))
        expense2 = self.project.add_expense("Expense 2", 2000.0, datetime(2024, 1, 2))
        
        partner = self.project.add_partner("Partner", 10000.0)
        self.project.add_payment(500.0, datetime(2024, 1, 5), partner, expense1)  # Partial payment
        self.project.add_payment(2000.0, datetime(2024, 1, 6), partner, expense2)  # Full payment
        
        summary = self.project.get_expense_summary()
        
        self.assertIn("Expense 1", summary)
        self.assertIn("Expense 2", summary)
        
        exp1_summary = summary["Expense 1"]
        self.assertEqual(exp1_summary["total"], 1000.0)
        self.assertEqual(exp1_summary["paid"], 500.0)
        self.assertEqual(exp1_summary["remaining"], 500.0)
        self.assertEqual(exp1_summary["status"], PaymentStatus.PARTIALLY_PAID)
        
        exp2_summary = summary["Expense 2"]
        self.assertEqual(exp2_summary["status"], PaymentStatus.FULLY_PAID)

    def test_get_expense_summary_unpaid(self):
        """Test expense summary with unpaid expense."""
        self.project.add_expense("Unpaid Expense", 1500.0, datetime(2024, 1, 1))
        
        summary = self.project.get_expense_summary()
        exp_summary = summary["Unpaid Expense"]
        
        self.assertEqual(exp_summary["paid"], 0)
        self.assertEqual(exp_summary["remaining"], 1500.0)
        self.assertEqual(exp_summary["status"], PaymentStatus.UNPAID)

    def test_get_payment_summary(self):
        """Test payment summary generation."""
        partner = self.project.add_partner("Test Partner", 10000.0)
        expense = self.project.add_expense("Test Expense", 2000.0, datetime(2024, 1, 1))
        
        payment1 = self.project.add_payment(800.0, datetime(2024, 1, 5), partner, expense)
        payment2 = self.project.add_payment(1200.0, datetime(2024, 1, 10), partner, expense)
        
        summary = self.project.get_payment_summary()
        
        self.assertEqual(len(summary), 2)
        self.assertIn("Payment #1", summary)
        self.assertIn("Payment #2", summary)
        
        payment1_summary = summary["Payment #1"]
        self.assertEqual(payment1_summary["amount"], 800.0)
        self.assertEqual(payment1_summary["partner"], "Test Partner")
        self.assertEqual(payment1_summary["expense"], "Test Expense")
        self.assertEqual(payment1_summary["percentage"], 40.0)  # 800/2000 * 100

    def test_get_sale_summary(self):
        """Test sale summary generation."""
        self.project.add_sale(15000.0, datetime(2024, 3, 1), "Property A")
        self.project.add_sale(25000.0, datetime(2024, 4, 1), "Property B")
        
        summary = self.project.get_sale_summary()
        
        self.assertEqual(len(summary), 2)
        self.assertIn("Property A", summary)
        self.assertIn("Property B", summary)
        
        prop_a_summary = summary["Property A"]
        self.assertEqual(prop_a_summary["total"], 15000.0)
        self.assertEqual(prop_a_summary["date"], datetime(2024, 3, 1).date())

    def test_format_relative_date_today(self):
        """Test relative date formatting for today."""
        today = datetime.now()
        result = self.project._format_relative_date(today)
        self.assertIn("today", result.lower())

    def test_format_relative_date_yesterday(self):
        """Test relative date formatting for yesterday."""
        yesterday = datetime.now() - timedelta(days=1)
        result = self.project._format_relative_date(yesterday)
        self.assertIn("yesterday", result.lower())

    def test_format_relative_date_days_ago(self):
        """Test relative date formatting for days ago."""
        five_days_ago = datetime.now() - timedelta(days=5)
        result = self.project._format_relative_date(five_days_ago)
        self.assertIn("5 days ago", result.lower())

    def test_format_relative_date_months_ago(self):
        """Test relative date formatting for months ago."""
        sixty_days_ago = datetime.now() - timedelta(days=60)
        result = self.project._format_relative_date(sixty_days_ago)
        self.assertIn("month", result.lower())

    def test_format_relative_date_future(self):
        """Test relative date formatting for future dates."""
        tomorrow = datetime.now() + timedelta(days=1)
        result = self.project._format_relative_date(tomorrow)
        self.assertIn("tomorrow", result.lower())

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_partner_summary(self, mock_stdout):
        """Test partner summary printing."""
        self.project.add_partner("Test Partner", 50000.0)
        self.project.print_partner_summary()
        
        output = mock_stdout.getvalue()
        self.assertIn("PARTNERS SUMMARY", output)
        self.assertIn("Test Partner", output)
        self.assertIn("50,000.00", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_expense_summary(self, mock_stdout):
        """Test expense summary printing."""
        self.project.add_expense("Test Expense", 1000.0, datetime(2024, 1, 1))
        self.project.print_expense_summary()
        
        output = mock_stdout.getvalue()
        self.assertIn("EXPENSES SUMMARY", output)
        self.assertIn("Test Expense", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_payment_summary(self, mock_stdout):
        """Test payment summary printing."""
        partner = self.project.add_partner("Partner", 10000.0)
        expense = self.project.add_expense("Expense", 1000.0, datetime(2024, 1, 1))
        self.project.add_payment(500.0, datetime(2024, 1, 5), partner, expense)
        self.project.print_payment_summary()
        
        output = mock_stdout.getvalue()
        self.assertIn("PAYMENTS SUMMARY", output)
        self.assertIn("Partner", output)
        self.assertIn("500.00", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_expenses_by_date(self, mock_stdout):
        """Test printing expenses by date."""
        self.project.add_expense("Expense 1", 1000.0, datetime(2024, 1, 15))
        self.project.add_expense("Expense 2", 1500.0, datetime(2024, 2, 20))
        
        self.project.print_expenses_by_date()
        
        output = mock_stdout.getvalue()
        self.assertIn("EXPENSES BY DATE", output)
        self.assertIn("Expense 1", output)
        self.assertIn("Expense 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_expenses_by_date_with_filter(self, mock_stdout):
        """Test printing expenses by date with since filter."""
        self.project.add_expense("Old Expense", 1000.0, datetime(2024, 1, 1))
        self.project.add_expense("New Expense", 1500.0, datetime(2024, 6, 1))
        
        since_date = datetime(2024, 5, 1)
        self.project.print_expenses_by_date(since=since_date)
        
        output = mock_stdout.getvalue()
        self.assertIn("New Expense", output)
        self.assertNotIn("Old Expense", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_payments_by_date(self, mock_stdout):
        """Test printing payments by date."""
        partner = self.project.add_partner("Partner", 10000.0)
        expense = self.project.add_expense("Expense", 2000.0, datetime(2024, 1, 1))
        self.project.add_payment(1000.0, datetime(2024, 1, 15), partner, expense)
        
        self.project.print_payments_by_date()
        
        output = mock_stdout.getvalue()
        self.assertIn("PAYMENTS BY DATE", output)
        self.assertIn("Partner", output)

    def test_string_representation(self):
        """Test string representation of project."""
        self.project.add_expense("Test Expense", 5000.0, datetime(2024, 1, 1))
        self.project.add_partner("Partner", 10000.0)
        
        str_repr = str(self.project)
        
        self.assertIn("Test Project", str_repr)
        self.assertIn("5,000.00", str_repr)
        self.assertIn("10,000.00", str_repr)
        self.assertIn("PROJECT SUMMARY", str_repr)

    def test_complex_project_scenario(self):
        """Test a complex project scenario with multiple components."""
        # Add expenses
        exp1 = self.project.add_expense("Land Purchase", 100000.0, datetime(2024, 1, 1))
        exp2 = self.project.add_expense("Construction", 75000.0, datetime(2024, 2, 1))
        exp3 = self.project.add_expense("Legal Fees", 5000.0, datetime(2024, 1, 15))
        
        # Add partners
        p1 = self.project.add_partner("Alice", 80000.0)  # 44.4%
        p2 = self.project.add_partner("Bob", 60000.0)    # 33.3%
        p3 = self.project.add_partner("Charlie", 40000.0) # 22.2%
        
        # Add payments
        self.project.add_payment(50000.0, datetime(2024, 1, 5), p1, exp1)   # Partial land
        self.project.add_payment(50000.0, datetime(2024, 1, 10), p2, exp1)  # Complete land
        self.project.add_payment(5000.0, datetime(2024, 1, 20), p3, exp3)   # Complete legal
        self.project.add_payment(30000.0, datetime(2024, 2, 5), p1, exp2)   # Partial construction
        
        # Add sale
        self.project.add_sale(200000.0, datetime(2024, 6, 1), "Property Sale")
        
        # Verify totals
        self.assertEqual(self.project.total_expenses(), 180000.0)
        self.assertEqual(self.project.total_investments(), 180000.0)
        self.assertEqual(self.project.total_payments(), 135000.0)
        self.assertEqual(self.project.total_sales(), 200000.0)
        self.assertEqual(self.project.project_balance(), 65000.0)  # 200000 - 135000
        
        # Verify ownership percentages
        percentages = self.project.calculate_ownership_percentages()
        self.assertAlmostEqual(percentages["Alice"], 44.44, places=1)
        self.assertAlmostEqual(percentages["Bob"], 33.33, places=1)
        self.assertAlmostEqual(percentages["Charlie"], 22.22, places=1)
        
        # Verify expense statuses
        expense_summary = self.project.get_expense_summary()
        self.assertEqual(expense_summary["Land Purchase"]["status"], PaymentStatus.FULLY_PAID)
        self.assertEqual(expense_summary["Legal Fees"]["status"], PaymentStatus.FULLY_PAID)
        self.assertEqual(expense_summary["Construction"]["status"], PaymentStatus.PARTIALLY_PAID)

    def test_empty_project_calculations(self):
        """Test calculations on empty project."""
        self.assertEqual(self.project.total_expenses(), 0)
        self.assertEqual(self.project.total_payments(), 0)
        self.assertEqual(self.project.total_investments(), 0)
        self.assertEqual(self.project.total_sales(), 0)
        self.assertEqual(self.project.project_balance(), 0)
        self.assertEqual(self.project.target_amount(), 0)
        self.assertEqual(self.project.calculate_ownership_percentages(), {})

    def test_edge_case_zero_amounts(self):
        """Test handling of zero amounts in various scenarios."""
        partner = self.project.add_partner("Partner", 0.0)
        expense = self.project.add_expense("Zero Expense", 0.0, datetime(2024, 1, 1))
        payment = self.project.add_payment(0.0, datetime(2024, 1, 5), partner, expense)
        
        self.assertEqual(self.project.total_investments(), 0.0)
        self.assertEqual(self.project.total_expenses(), 0.0)
        self.assertEqual(self.project.total_payments(), 0.0)

    def tearDown(self):
        """Clean up after each test method."""
        # Reset any global state if needed
        pass


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCrowdfundingProject)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"CrowdfundingProject Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    print(f"{'='*70}")