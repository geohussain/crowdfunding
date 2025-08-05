# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based crowdfunding project management system for real estate investments. It tracks expenses, payments, partners, and sales for a crowdfunding project called "Ghadeer Land". The system calculates ownership percentages, payment statuses, and project balances.

## Commands

### Running the Application
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Architecture

### Core Components

- **CrowdfundingProject** (`src/crowdfunding_project.py`): Main orchestrator class that manages all project aspects including expenses, payments, partners, and sales. Provides comprehensive reporting and calculation methods.

- **Partner** (`src/partner.py`): Represents investors with their investment amounts. Used to calculate ownership percentages.

- **Expense** (`src/expense.py`): Represents project costs that need to be covered by partner payments.

- **Payment** (`src/payment.py`): Links partners to expenses, tracking who paid what toward which expense.

- **Sale** (`src/sale.py`): Represents revenue from property sales.

- **PaymentStatus** (`src/payment_status.py`): Enum for tracking expense payment completion (UNPAID, PARTIALLY_PAID, FULLY_PAID).

- **Helpers** (`src/helpers.py`): Utility functions for formatting output displays.

### Data Flow

1. The main application (`main.py`) creates a CrowdfundingProject instance
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
└── helpers.py              # Display formatting utilities
```

The main application logic is in `main.py` which demonstrates usage with the "Ghadeer Land" real estate project data.