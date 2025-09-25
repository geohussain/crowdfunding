import argparse
import sys
from datetime import datetime
from pathlib import Path

# Import both old and new project creation methods
from projects.ghadeer_land import create_ghadeer_land_project
from src.project_factory import ProjectFactory
from src.config_loader import ConfigValidationError


def create_argument_parser():
    """Create and configure the command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Crowdfunding Project Management System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                           # Run default Ghadeer Land project
  python main.py --config projects/ghadeer_land.yaml      # Run from YAML config
  python main.py --config projects/my_project.yaml --partners     # Show partners only
  python main.py --config projects/my_project.yaml --expenses-by-date --since 2025-06-01
  python main.py --config projects/my_project.yaml --all  # Show all reports
        """
    )

    # Configuration file
    parser.add_argument(
        '--config',
        type=str,
        metavar='PATH',
        help='Path to YAML configuration file (default: use hardcoded Ghadeer Land project)'
    )

    # Report selection flags
    parser.add_argument(
        '--partners',
        action='store_true',
        help='Show partner ownership summary'
    )

    parser.add_argument(
        '--expenses',
        action='store_true',
        help='Show expense summary by category'
    )

    parser.add_argument(
        '--payments',
        action='store_true',
        help='Show payment summary by partner'
    )

    parser.add_argument(
        '--expenses-by-date',
        action='store_true',
        help='Show expenses chronologically'
    )

    parser.add_argument(
        '--payments-by-date',
        action='store_true',
        help='Show payments chronologically'
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show overall project financial summary'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Show all available reports (default behavior)'
    )

    # Filter options
    parser.add_argument(
        '--since',
        type=str,
        metavar='YYYY-MM-DD',
        help='Filter date-based reports to show only entries since this date'
    )

    # Utility flags
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate the configuration file, don\'t run reports'
    )

    return parser


def parse_since_date(since_str):
    """Parse the --since date argument"""
    if not since_str:
        return None

    try:
        return datetime.strptime(since_str, '%Y-%m-%d')
    except ValueError:
        print(f"Error: Invalid date format '{since_str}'. Use YYYY-MM-DD format.")
        sys.exit(1)


def load_project(config_path):
    """Load project either from config file or use default Ghadeer Land"""
    if config_path:
        try:
            return ProjectFactory.create_from_config(config_path)
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {config_path}")
            sys.exit(1)
        except ConfigValidationError as e:
            print(f"Error: Configuration validation failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to load project from config: {e}")
            sys.exit(1)
    else:
        # Use the original hardcoded Ghadeer Land project
        return create_ghadeer_land_project()


def run_reports(project, args):
    """Run the selected reports based on command line arguments"""
    since_date = parse_since_date(args.since)

    # If no specific flags are provided, or --all is specified, run default reports
    no_specific_flags = not any([
        args.partners, args.expenses, args.payments,
        args.expenses_by_date, args.payments_by_date, args.summary
    ])

    if args.all or no_specific_flags:
        # Default behavior - run the current set of reports
        project.print_partner_summary()
        project.print_expenses_by_date(since=since_date)
        project.print_payments_by_date(since=since_date)
        print(project)
        return

    # Run specific reports based on flags
    if args.partners:
        project.print_partner_summary()

    if args.expenses:
        project.print_expense_summary()

    if args.payments:
        project.print_payment_summary()

    if args.expenses_by_date:
        project.print_expenses_by_date(since=since_date)

    if args.payments_by_date:
        project.print_payments_by_date(since=since_date)

    if args.summary:
        print(project)


def main():
    """Main application entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Load project
    project = load_project(args.config)

    # If validate-only flag is set, just validate and exit
    if args.validate_only:
        print("✅ Configuration validation passed successfully!")
        return

    # Run selected reports
    run_reports(project, args)


if __name__ == "__main__":
    main()