# 🏗️ Crowdfunding Project Management System

A Python-based financial tracking and reporting system designed for real estate crowdfunding projects. Track expenses, payments, partner investments, and generate comprehensive reports with mobile-friendly formatting.

## ✨ Features

### 📊 **Financial Tracking**
- **Expense Management**: Categorized expense tracking with payment status
- **Partner Investments**: Track investor contributions and ownership percentages
- **Payment Linking**: Connect payments to specific expenses and partners
- **Revenue Tracking**: Sales and income recording (future sales support)

### 📱 **Mobile-Optimized Reports**
- **Text Message Ready**: Formatted for SMS, WhatsApp, and messaging apps
- **Chronological Views**: Date-sorted expenses and payments with relative time
- **Card-Based Layouts**: Clean, scannable format for mobile devices
- **Status Indicators**: Visual payment completion tracking (✅❌⚠️)

### 🗓️ **Advanced Reporting**
- **Relative Dates**: Human-readable time formatting ("2 months ago", "yesterday")
- **Monthly Grouping**: Organized chronological reports by month/year
- **Ownership Calculations**: Automatic percentage calculations based on investments
- **Project Completion**: Progress tracking and completion metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Basic terminal/command line knowledge

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/geohussain/crowdfunding.git
   cd crowdfunding
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Usage Examples

### Basic Project Setup
```python
from src.crowdfunding_project import CrowdfundingProject
from datetime import datetime

# Create a new project
project = CrowdfundingProject("My Project", 
                             datetime(2024, 1, 1), 
                             datetime(2024, 12, 31))

# Add expenses
land_expense = project.add_expense("Land Purchase", 1000000, datetime(2024, 1, 15))

# Add partners
partner1 = project.add_partner("John Doe", 500000)  # 50% ownership

# Link payments
project.add_payment(500000, datetime(2024, 1, 20), partner1, land_expense)
```

### Generate Reports
```python
# Mobile-friendly partner summary
project.print_partner_summary()

# Chronological expense tracking
project.print_expenses_by_date()

# Payments with relative dates
project.print_payments_by_date()

# Filter by date range
project.print_expenses_by_date(since=datetime(2024, 6, 1))
```

## 📁 Project Structure

```
crowdfunding/
├── src/                          # Core application modules
│   ├── crowdfunding_project.py   # Main project management class
│   ├── partner.py                # Partner/investor representation
│   ├── expense.py                # Expense tracking
│   ├── payment.py                # Payment linking system
│   ├── sale.py                   # Revenue tracking
│   ├── payment_status.py         # Payment completion status
│   └── helpers.py                # Formatting and display utilities
├── projects/                     # Project-specific data modules
│   └── ghadeer_land/            # Example: Ghadeer Land project
│       ├── __init__.py          # Project factory function
│       ├── expenses.py          # Project expense definitions
│       ├── partners.py          # Partner configurations
│       └── payments.py          # Payment linkages
├── main.py                      # Application entry point
├── CLAUDE.md                    # AI assistant guidance
└── README.md                    # This file
```

## 💡 Key Concepts

### **CrowdfundingProject**
Central class managing all project aspects:
- Tracks expenses, payments, partners, and sales
- Calculates ownership percentages automatically
- Provides comprehensive reporting methods
- Handles payment status tracking

### **Modular Project Organization**
- Each project lives in its own `projects/` subdirectory
- Separate modules for expenses, partners, and payments
- Factory functions for easy project initialization
- Scalable architecture for multiple projects

### **Mobile-First Design**
- Card-based layouts instead of complex tables
- 30-character width optimization for text messages
- Emoji categorization for quick visual scanning
- Vertical information flow for portrait screens

## 📊 Sample Output

### Partner Summary
```
📋 PARTNERS SUMMARY
💳 John Doe
  Investment: SAR 500,000.00
  Ownership: 50.0%
  Paid: SAR 500,000.00
  Balance: SAR 0.00

💳 Jane Smith
  Investment: SAR 300,000.00
  Ownership: 30.0%
  Paid: SAR 300,000.00
  Balance: SAR 0.00
```

### Chronological Expenses
```
📋 EXPENSES BY DATE

🗓️ JANUARY 2024
-------------------------
💰 Land Purchase
📅 2 months ago (2024-01-15)
💵 Total: SAR 1,000,000.00
✅ Paid: SAR 1,000,000.00
✅ PAID
------------------------------
```

## 🛠️ Development

### Adding New Projects
1. Create a new directory under `projects/`
2. Add `expenses.py`, `partners.py`, `payments.py` modules
3. Create `__init__.py` with factory function
4. Import and use in `main.py`

### Extending Functionality
- **New Report Types**: Add methods to `CrowdfundingProject`
- **Custom Formatting**: Extend `helpers.py` utility functions
- **Data Export**: Add JSON/CSV export capabilities
- **Database Integration**: Replace in-memory storage

### Testing
```bash
# Run the application
python main.py

# Check output formatting
python main.py | head -20
```

## 📈 Use Cases

### **Real Estate Development**
- Track land acquisition, construction costs, permits
- Manage multiple investor contributions
- Monitor project completion and profitability
- Generate investor reports and updates

### **Group Investment Projects**
- Shared expense tracking for group purchases
- Proportional ownership calculations
- Payment responsibility tracking
- Financial transparency for all participants

### **Crowdfunding Campaigns**
- Expense categorization and tracking
- Backer contribution management
- Progress reporting and updates
- Financial accountability documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- See `CLAUDE.md` for detailed development guidance
- Check inline code documentation for API details
- Review example project in `projects/ghadeer_land/`

### Issues
For bug reports and feature requests, please open an issue on GitHub.

---

**Built with ❤️ for transparent financial tracking in collaborative projects**

*Perfect for sharing updates via text message, email, or any mobile device!* 📱✨