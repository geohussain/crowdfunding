from datetime import datetime
from src.crowdfunding_project import CrowdfundingProject


def main():
    # Create a new crowdfunding project
    project = CrowdfundingProject("Ghadeer Land", datetime(2024, 7, 22), datetime(2025, 7, 22))

    # Add expenses
    land_price = project.add_expense("Land Price from Auction", 1885908, datetime(2024, 7, 22))
    price_increase = project.add_expense("Price Increase after Auction", 178102, datetime(2024, 7, 22))
    auction_fees = project.add_expense("Auction Agent Fees", 54221, datetime(2024, 7, 22))
    vat = project.add_expense("VAT", 94295.40, datetime(2024, 7, 22))
    agent_fees = project.add_expense("Agent Fees", 52955, datetime(2024, 7, 22))
    lawyer_land_buying_fee = project.add_expense("Lawyer Land Buying Fee", 690, datetime(2024, 8, 18))
    land_split_fees = project.add_expense("Land Split Fees", 221.60, datetime(2024, 11, 4))
    land_split_fees_order = project.add_expense("Land Split Fees order", 703, datetime(2024, 12, 18))
    land_split_fee_two_lands = project.add_expense("Land Split Two Lands", 400, datetime(2024, 12, 29))
    land_report_fees = project.add_expense("Land Report Fees", 920, datetime(2025, 2, 6))
    land_report_fees_2 = project.add_expense("Land Report Fees - Sadad Balady", 394, datetime(2025, 2, 11))
    construction_insurance_1 = project.add_expense("Construction Insurance - Part One", 9774.93, datetime(2025, 2, 16))
    construction_insurance_2 = project.add_expense("Construction Insurance - Part Two", 4715.88, datetime(2025, 2, 16))
    land_one_geographic_report = project.add_expense("Area Report Fees - Land One", 330, datetime(2025, 2, 18))

    # Add partners
    hussain_alsalim = project.add_partner("Hussain AlSalim", 1000000)
    ali_alfaraj = project.add_partner("Ali AlFaraj", 500000.40)
    saleh_alnasser = project.add_partner("Saleh AlNasser", 440000 + 690)
    ali_aldawood = project.add_partner("Ali AlDawood",
                                       205481 + 221.60 + 703 + 400 + 920 + 394
                                       + 9774.93 + 4715.88 + 330)
    mohammed_alhawaj = project.add_partner("Mohammed AlHawaj", 120000)

    # Add payments
    project.add_payment(52955, datetime(2024, 7, 22), hussain_alsalim, agent_fees)
    project.add_payment(94295.40, datetime(2024, 7, 23), ali_alfaraj, vat)
    project.add_payment(947045, datetime(2024, 7, 24), hussain_alsalim, land_price)
    project.add_payment(120000, datetime(2024, 7, 28), mohammed_alhawaj, land_price)
    project.add_payment(205481, datetime(2024, 7, 28), ali_aldawood, land_price)
    project.add_payment(405705, datetime(2024, 8, 15), ali_alfaraj, land_price)
    project.add_payment(207677, datetime(2024, 8, 15), saleh_alnasser, land_price)
    project.add_payment(178102, datetime(2024, 8, 15), saleh_alnasser, price_increase)
    project.add_payment(54221, datetime(2024, 8, 15), saleh_alnasser, auction_fees)
    project.add_payment(690, datetime(2024, 8, 18), saleh_alnasser, lawyer_land_buying_fee)
    project.add_payment(221.60, datetime(2024, 11, 4), ali_aldawood, land_split_fees)
    project.add_payment(703, datetime(2024, 12, 18), ali_aldawood, land_split_fees_order)
    project.add_payment(400, datetime(2024, 12, 29), ali_aldawood, land_split_fee_two_lands)
    project.add_payment(920, datetime(2025, 2, 6), ali_aldawood, land_report_fees)
    project.add_payment(394, datetime(2025, 2, 11), ali_aldawood, land_report_fees_2)
    project.add_payment(9774.93, datetime(2025, 2, 16), ali_aldawood, construction_insurance_1)
    project.add_payment(4715.88, datetime(2025, 2, 16), ali_aldawood, construction_insurance_2)
    project.add_payment(330, datetime(2025, 2, 18), ali_aldawood, land_one_geographic_report)

    # Add a sale
    # project.add_sale(1250000, datetime(2025, 6, 1), "Duplex 1 Sale")

    # Print partner summary
    project.print_partner_summary()

    # Print expense summary
    project.print_expense_summary()

    # Print payment summary
    project.print_payment_summary()

    # Print sales summary
    # project.print_sale_summary()

    # Print project summary
    print(project)


if __name__ == "__main__":
    main()