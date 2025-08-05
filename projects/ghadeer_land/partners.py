def add_partners(project):
    """Add all partners for the Ghadeer Land project"""
    partners = {}
    
    partners['hussain_alsalim'] = project.add_partner("Hussain AlSalim", 1000000)
    partners['ali_alfaraj'] = project.add_partner("Ali AlFaraj", 500000.40)
    partners['saleh_alnasser'] = project.add_partner("Saleh AlNasser", 440000 + 690)
    
    # Ali AlDawood's investment calculation
    ali_investment = (205481 + 221.60 + 703 + 400 + 920 + 394
                     + 9774.93 + 4715.88 + 330 + 8625 + 4286.35
                     + 6374 + 5222 + 80000 + 35000 + 100000
                     + 37651 + 1955 + 20368 + 10580 + 11902.50
                     + 4036.50 + 1955 + 500 + 174.02 + 255
                     + 20000 + 20000 + 598 + 50000 + 50000 + 2196.50)
    
    partners['ali_aldawood'] = project.add_partner("Ali AlDawood", ali_investment)
    partners['mohammed_alhawaj'] = project.add_partner("Mohammed AlHawaj", 120000)
    
    return partners