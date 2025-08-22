from datetime import datetime


def add_payments(project, partners, expenses):
    """Add all payments for the Ghadeer Land project"""
    
    # Initial payments
    project.add_payment(52955, datetime(2024, 7, 22), partners['hussain_alsalim'], expenses['agent_fees'])
    project.add_payment(94295.40, datetime(2024, 7, 23), partners['ali_alfaraj'], expenses['vat'])
    project.add_payment(947045, datetime(2024, 7, 24), partners['hussain_alsalim'], expenses['land_price'])
    project.add_payment(120000, datetime(2024, 7, 28), partners['mohammed_alhawaj'], expenses['land_price'])
    project.add_payment(205481, datetime(2024, 7, 28), partners['ali_aldawood'], expenses['land_price'])
    project.add_payment(405705, datetime(2024, 8, 15), partners['ali_alfaraj'], expenses['land_price'])
    project.add_payment(207677, datetime(2024, 8, 15), partners['saleh_alnasser'], expenses['land_price'])
    project.add_payment(178102, datetime(2024, 8, 15), partners['saleh_alnasser'], expenses['price_increase'])
    project.add_payment(54221, datetime(2024, 8, 15), partners['saleh_alnasser'], expenses['auction_fees'])
    project.add_payment(690, datetime(2024, 8, 18), partners['saleh_alnasser'], expenses['lawyer_land_buying_fee'])
    
    # Legal and administrative payments
    project.add_payment(221.60, datetime(2024, 11, 4), partners['ali_aldawood'], expenses['land_split_fees'])
    project.add_payment(703, datetime(2024, 12, 18), partners['ali_aldawood'], expenses['land_split_fees_order'])
    project.add_payment(400, datetime(2024, 12, 29), partners['ali_aldawood'], expenses['land_split_fee_two_lands'])
    project.add_payment(920, datetime(2025, 2, 6), partners['ali_aldawood'], expenses['land_report_fees'])
    project.add_payment(394, datetime(2025, 2, 11), partners['ali_aldawood'], expenses['land_report_fees_2'])
    project.add_payment(330, datetime(2025, 2, 18), partners['ali_aldawood'], expenses['land_one_geographic_report'])
    
    # Insurance and license payments
    project.add_payment(9774.93, datetime(2025, 2, 16), partners['ali_aldawood'], expenses['construction_insurance_1'])
    project.add_payment(4715.88, datetime(2025, 2, 16), partners['ali_aldawood'], expenses['construction_insurance_2'])
    project.add_payment(8625, datetime(2025, 3, 10), partners['ali_aldawood'], expenses['construction_insurance_3'])
    project.add_payment(4286.35, datetime(2025, 3, 10), partners['ali_aldawood'], expenses['construction_insurance_4'])
    project.add_payment(6374, datetime(2025, 4, 21), partners['ali_aldawood'], expenses['building_license_2'])
    project.add_payment(5222, datetime(2025, 5, 2), partners['ali_aldawood'], expenses['building_license_1'])
    
    # Development and construction payments
    project.add_payment(80000, datetime(2025, 5, 25), partners['ali_aldawood'], expenses['blueprints_fees'])
    project.add_payment(35000, datetime(2025, 6, 4), partners['ali_aldawood'], expenses['land_one_fill'])
    project.add_payment(100000, datetime(2025, 6, 12), partners['ali_aldawood'], expenses['cementing_fees_1'])
    project.add_payment(20400, datetime(2025, 8, 22), partners['ali_aldawood'], expenses['land_one_sand_fill'])
    
    # Materials payments
    project.add_payment(37651, datetime(2025, 6, 21), partners['ali_aldawood'], expenses['base_steel_bars'])
    project.add_payment(1955, datetime(2025, 6, 21), partners['ali_aldawood'], expenses['base_concrete_blocks'])
    project.add_payment(147.20, datetime(2025, 6, 21), partners['ali_aldawood'], expenses['plastic_cover_fee_1'])
    project.add_payment(220.80, datetime(2025, 6, 21), partners['ali_aldawood'], expenses['plastic_cover_fee_2'])
    project.add_payment(10580, datetime(2025, 6, 23), partners['ali_aldawood'], expenses['deformed_steel_bars'])
    project.add_payment(11902.50, datetime(2025, 6, 25), partners['ali_aldawood'], expenses['base_steel_bars_2'])
    project.add_payment(4036.50, datetime(2025, 7, 23), partners['ali_aldawood'], expenses['base_concrete_blocks_2'])
    project.add_payment(1955, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['base_concrete_blocks_3'])
    project.add_payment(598, datetime(2025, 7, 30), partners['ali_aldawood'], expenses['base_concrete_blocks_4'])
    project.add_payment(50000, datetime(2025, 7, 31), partners['ali_aldawood'], expenses['concrete_blocks_top_up'])
    project.add_payment(50000, datetime(2025, 7, 31), partners['ali_aldawood'], expenses['steel_bars_top_up'])
    project.add_payment(2196.50, datetime(2025, 8, 4), partners['ali_aldawood'], expenses['black_tar'])
    
    # Contracting payments
    project.add_payment(20000, datetime(2025, 6, 21), partners['ali_aldawood'], expenses['contracting_payment_1'])
    project.add_payment(20000, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['contracting_payment_2'])
    project.add_payment(20000, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['contracting_payment_3'])
    
    # Miscellaneous payments
    project.add_payment(500, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['misc_fee_1'])
    project.add_payment(174.02, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['misc_fee_2'])
    project.add_payment(255, datetime(2025, 7, 29), partners['ali_aldawood'], expenses['misc_fee_3'])