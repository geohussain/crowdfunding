# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based crowdfunding project management system for real estate investments. It tracks expenses, payments, partners, and sales for a crowdfunding project called "Ghadeer Land". The system calculates ownership percentages, payment statuses, and project balances.

## Commands

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running the Application

#### Default Mode (Hardcoded Ghadeer Land Project)
```bash
python main.py
```

#### Configuration File Mode (Recommended)
```bash
# Run with YAML configuration file
python main.py --config projects/ghadeer_land.yaml

# Show all available command line options
python main.py --help
```

### Reporting Options

#### Show Specific Reports
```bash
# Show only partner summary
python main.py --config projects/ghadeer_land.yaml --partners

# Show only expenses chronologically
python main.py --config projects/ghadeer_land.yaml --expenses-by-date

# Show only payments chronologically
python main.py --config projects/ghadeer_land.yaml --payments-by-date

# Show only project summary
python main.py --config projects/ghadeer_land.yaml --summary

# Show all reports (same as default)
python main.py --config projects/ghadeer_land.yaml --all
```

#### Date Filtering
```bash
# Show expenses since June 1, 2025
python main.py --config projects/ghadeer_land.yaml --expenses-by-date --since 2025-06-01

# Show payments since August 1, 2025
python main.py --config projects/ghadeer_land.yaml --payments-by-date --since 2025-08-01

# Combine multiple reports with date filter
python main.py --config projects/ghadeer_land.yaml --expenses-by-date --payments-by-date --since 2025-07-01
```

#### Configuration Validation
```bash
# Validate configuration file without running reports
python main.py --config projects/ghadeer_land.yaml --validate-only
```

## Configuration System

### YAML Configuration Format

The system supports configurable projects via YAML files. This allows easy creation and management of multiple projects without hardcoding data.

#### Configuration File Structure
```yaml
project:
  name: "Project Name"
  start_date: "YYYY-MM-DD"
  end_date: "YYYY-MM-DD"

partners:
  - name: "Partner Name"
    investment_amount: 100000.00
    # OR use mathematical expressions:
    # investment_amount: "50000 + 30000 + 20000"

expenses:
  - description: "Expense Description"
    amount: 50000.00
    # OR use mathematical expressions:
    # amount: "25000 + 15000 + 10000"
    date: "YYYY-MM-DD"

payments:
  - amount: 50000.00
    # OR use mathematical expressions:
    # amount: "25000 + 25000"
    date: "YYYY-MM-DD"
    partner: "Partner Name"
    expense: "Expense Description"
```

#### Mathematical Expressions

The system supports mathematical expressions in amount fields using addition (+) operations:

**Supported Formats:**
- Simple numbers: `100000`, `1500.50`
- Addition expressions: `"100 + 200 + 300"`
- Mixed decimals: `"1000.50 + 500.25"`
- Flexible spacing: `"100+200"`, `"100 + 200"`, `"  100  +  200  "`

**Examples:**
```yaml
partners:
  - name: "Ali AlDawood"
    # Break down complex calculations for clarity
    investment_amount: "205481 + 221.60 + 703 + 400 + 920 + 394"

expenses:
  - description: "Total Construction Cost"
    amount: "50000 + 30000 + 20000"  # 100000

payments:
  - amount: "25000 + 25000"  # 50000
    partner: "Partner Name"
    expense: "Expense Description"
```

**Security Notes:**
- Only addition (+) operations are supported for security
- Only numbers, decimal points, plus signs, and spaces are allowed
- Expressions are validated before evaluation
- Invalid expressions will cause clear error messages

#### Creating New Projects

1. **Copy the template**: Use `projects/ghadeer_land.yaml` as a starting point
2. **Update project info**: Modify name, dates, and project details
3. **Add partners**: List all investors with their investment amounts
4. **Add expenses**: List all project costs with amounts and dates
5. **Add payments**: Link partners to expenses they've paid for
6. **Validate**: Use `--validate-only` flag to check for errors
7. **Run**: Use `--config path/to/your/project.yaml` to run reports

#### Configuration Validation

The system validates:
- Required fields are present
- Date formats are correct (YYYY-MM-DD)
- Investment and expense amounts are positive numbers
- Partner and expense references in payments exist
- No duplicate partner names or expense descriptions

## Architecture

### Core Components

- **CrowdfundingProject** (`src/crowdfunding_project.py`): Main orchestrator class that manages all project aspects including expenses, payments, partners, and sales. Provides comprehensive reporting and calculation methods.

- **Partner** (`src/partner.py`): Represents investors with their investment amounts. Used to calculate ownership percentages.

- **Expense** (`src/expense.py`): Represents project costs that need to be covered by partner payments.

- **Payment** (`src/payment.py`): Links partners to expenses, tracking who paid what toward which expense.

- **Sale** (`src/sale.py`): Represents revenue from property sales.

- **PaymentStatus** (`src/payment_status.py`): Enum for tracking expense payment completion (UNPAID, PARTIALLY_PAID, FULLY_PAID).

- **Helpers** (`src/helpers.py`): Utility functions for formatting output displays.

- **ConfigLoader** (`src/config_loader.py`): Loads and validates YAML configuration files with comprehensive error handling.

- **ProjectFactory** (`src/project_factory.py`): Creates CrowdfundingProject instances from YAML configuration files.

- **ExpressionEvaluator** (`src/expression_evaluator.py`): Safely evaluates mathematical expressions in configuration values, supporting addition operations with comprehensive validation.

### Data Flow

#### Configuration-Based Flow (Recommended)
1. The main application (`main.py`) parses command-line arguments
2. ConfigLoader loads and validates the YAML configuration file
3. ProjectFactory creates a CrowdfundingProject instance from the configuration
4. Partners, expenses, and payments are automatically added from configuration data
5. The system calculates ownership percentages based on investment amounts
6. Selected reports are displayed based on command-line flags

#### Legacy Flow (Hardcoded Data)
1. The main application (`main.py`) imports hardcoded project data
2. Expenses are added to define project costs
3. Partners are added with their investment commitments
4. Payments link partners to specific expenses they're covering
5. The system calculates ownership percentages based on investment amounts
6. Various summary reports show project status, partner positions, and expense tracking

### Key Business Logic

- **Ownership Calculation**: Based on partner investment amounts as percentage of total investments
- **Payment Tracking**: Associates payments with specific expenses to track completion status
- **Balance Calculation**: Revenue (sales) minus payments to show project profitability
- **Investment Balance**: Shows remaining committed investment per partner after payments made

## Project Structure

```
src/
├── crowdfunding_project.py  # Main project management class
├── partner.py              # Partner/investor representation
├── expense.py              # Project expense tracking
├── payment.py              # Payment linking partners to expenses
├── sale.py                 # Revenue tracking
├── payment_status.py       # Payment completion status enum
├── helpers.py              # Display formatting utilities
├── config_loader.py        # YAML configuration file loader and validator
└── project_factory.py      # Creates projects from configuration files

projects/
├── ghadeer_land.yaml       # Ghadeer Land project configuration file
└── ghadeer_land/           # Legacy hardcoded project data
    ├── __init__.py
    ├── partners.py
    ├── expenses.py
    └── payments.py
```

The main application logic is in `main.py` which supports both configuration-driven projects (recommended) and legacy hardcoded project data.