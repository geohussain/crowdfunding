from datetime import datetime


def add_expenses(project):
    """Add all expenses for the Ghadeer Land project"""
    expenses = {}
    
    # Initial land acquisition expenses
    expenses['land_price'] = project.add_expense("Land Price from Auction", 1885908, datetime(2024, 7, 22))
    expenses['price_increase'] = project.add_expense("Price Increase after Auction", 178102, datetime(2024, 7, 22))
    expenses['auction_fees'] = project.add_expense("Auction Agent Fees", 54221, datetime(2024, 7, 22))
    expenses['vat'] = project.add_expense("VAT", 94295.40, datetime(2024, 7, 22))
    expenses['agent_fees'] = project.add_expense("Agent Fees", 52955, datetime(2024, 7, 22))

    # Legal and administrative fees
    expenses['lawyer_land_buying_fee'] = project.add_expense("Lawyer Land Buying Fee", 690, datetime(2024, 8, 18))
    expenses['land_split_fees'] = project.add_expense("Land Split Fees", 221.60, datetime(2024, 11, 4))
    expenses['land_split_fees_order'] = project.add_expense("Land Split Fees order", 703, datetime(2024, 12, 18))
    expenses['land_split_fee_two_lands'] = project.add_expense("Land Split Two Lands", 400, datetime(2024, 12, 29))
    expenses['land_report_fees'] = project.add_expense("Land Report Fees", 920, datetime(2025, 2, 6))
    expenses['land_report_fees_2'] = project.add_expense("Land Report Fees - Sadad Balady", 394, datetime(2025, 2, 11))
    expenses['land_one_geographic_report'] = project.add_expense("Area Report Fees - Land One", 330, datetime(2025, 2, 18))

    # Construction insurance and licenses
    expenses['construction_insurance_1'] = project.add_expense("Construction Insurance - Land One - Part One", 9774.93, datetime(2025, 2, 16))
    expenses['construction_insurance_2'] = project.add_expense("Construction Insurance - Land One - Part Two", 4715.88, datetime(2025, 2, 16))
    expenses['construction_insurance_3'] = project.add_expense("Construction Insurance - Land Two - Part One", 8625, datetime(2025, 3, 10))
    expenses['construction_insurance_4'] = project.add_expense("Construction Insurance - Land Two - Part Two", 4286.35, datetime(2025, 3, 10))
    expenses['building_license_1'] = project.add_expense("Building License Fee - Land One", 5222, datetime(2025, 5, 2))
    expenses['building_license_2'] = project.add_expense("Building License Fee - Land Two", 6374, datetime(2025, 4, 21))

    # Construction and development expenses
    expenses['blueprints_fees'] = project.add_expense("Blueprints Fees", 80000, datetime(2025, 5, 25))
    expenses['land_one_fill'] = project.add_expense("Land One Fill", 35000, datetime(2025, 6, 4))
    expenses['cementing_fees_1'] = project.add_expense("Cementing Fees #1", 100000, datetime(2025, 6, 12))
    expenses['land_one_sand_fill'] = project.add_expense("Land One Sand Fill", 20400, datetime(2025, 8, 22))

    # Materials and supplies
    expenses['base_steel_bars'] = project.add_expense("Base Steel Bars Fees", 37651, datetime(2025, 6, 21))
    expenses['base_concrete_blocks'] = project.add_expense("Base Concrete Blocks Fees", 1955, datetime(2025, 6, 21))
    expenses['plastic_cover_fee_1'] = project.add_expense("Plastic Cover Fees #1", 147.20, datetime(2025, 6, 21))
    expenses['plastic_cover_fee_2'] = project.add_expense("Plastic Cover Fees #2", 220.80, datetime(2025, 6, 21))
    expenses['deformed_steel_bars'] = project.add_expense("Deformed Steel Bars Fees", 10580, datetime(2025, 6, 23))
    expenses['base_steel_bars_2'] = project.add_expense("Base Steel Bars Fees #2", 11902.50, datetime(2025, 6, 25))
    expenses['base_concrete_blocks_2'] = project.add_expense("Base Concrete Blocks Fees #2", 4036.50, datetime(2025, 7, 23))
    expenses['base_concrete_blocks_3'] = project.add_expense("Base Concrete Blocks Fees #3", 1955, datetime(2025, 7, 29))
    expenses['base_concrete_blocks_4'] = project.add_expense("Base Concrete Blocks Fees #4", 598, datetime(2025, 7, 30))
    expenses['concrete_blocks_top_up'] = project.add_expense("Concrete Blocks Top Up", 50000, datetime(2025, 7, 31))
    expenses['steel_bars_top_up'] = project.add_expense("Steel Bars Top Up", 50000, datetime(2025, 7, 31))
    expenses['black_tar'] = project.add_expense("Black Tar", 2196.50, datetime(2025, 8, 4))

    # Contracting payments
    expenses['contracting_payment_1'] = project.add_expense("Contracting Payment Fees #1", 20000, datetime(2025, 6, 21))
    expenses['contracting_payment_2'] = project.add_expense("Contracting Payment Fees #2", 20000, datetime(2025, 7, 29))
    expenses['contracting_payment_3'] = project.add_expense("Contracting Payment Fees #3", 20000, datetime(2025, 7, 29))

    # Miscellaneous expenses
    expenses['misc_fee_1'] = project.add_expense("Misc Fee #1", 500, datetime(2025, 7, 29))
    expenses['misc_fee_2'] = project.add_expense("Misc Fee #2", 174.02, datetime(2025, 7, 29))
    expenses['misc_fee_3'] = project.add_expense("Misc Fee #3", 255, datetime(2025, 7, 29))

    return expenses
