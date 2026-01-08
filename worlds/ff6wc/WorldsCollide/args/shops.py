def name():
    return "Shops"

def parse(parser):
    shops = parser.add_argument_group("Shops")

    shops_inventory = shops.add_mutually_exclusive_group()
    shops_inventory.add_argument("-sisr", "--shop-inventory-shuffle-random",
                                 default = None, type = int, metavar = "PERCENT", choices = range(101),
                                 help = "Shop inventories randomized based on type. All weapon shops randomized, all armor shops, etc...")
    shops_inventory.add_argument("-sirt", "--shop-inventory-random-tiered", action = "store_true",
                                 help = "Shop inventories randomized based on type and tier. All weapon shops randomized, all armor shops, etc...")
    shops_inventory.add_argument("-sie", "--shop-inventory-empty", action = "store_true",
                                 help = "Shop inventories empty")

    shops_prices = shops.add_mutually_exclusive_group()
    shops_prices.add_argument("-sprv", "--shop-prices-random-value", default = None, type = int,
                              nargs = 2, metavar = ("MIN", "MAX"), choices = range(2**16),
                              help = "Each item cost set to random value within given range")
    shops_prices.add_argument("-sprp", "--shop-prices-random-percent", default = None, type = int,
                              nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                              help = "Each item cost set to random percent of original within given range")

    shops_sell_fraction = shops.add_mutually_exclusive_group()
    shops_sell_fraction.add_argument("-ssf4", "--shop-sell-fraction4", action = "store_true",
                                     help = "Items sell for 1/4 their price")
    shops_sell_fraction.add_argument("-ssf8", "--shop-sell-fraction8", action = "store_true",
                                     help = "Items sell for 1/8 their price")
    shops_sell_fraction.add_argument("-ssf0", "--shop-sell-fraction0", action = "store_true",
                                     help = "Items sell for zero")

    shops.add_argument("-sdm", "--shop-dried-meat", default = 1, type = int, choices = range(6), metavar = "COUNT",
                        help = "%(metavar)s shops will contain dried meat")
    shops.add_argument("-npi", "--no-priceless-items", action = "store_true",
                       help = "Assign values to items which normally sell for 1 gold. Recommended with random inventory")

    shops.add_argument("-snbr", "--shops-no-breakable-rods", action = "store_true",
                       help = "Poison, Fire, Ice, Thunder, Gravity, and Pearl Rods not sold in shops")
    shops.add_argument("-sebr", "--shops-expensive-breakable-rods", action = "store_true",
                       help = "Poison, Fire, Ice, Thunder, Gravity, and Pearl Rods base price increased")

    shops.add_argument("-snes", "--shops-no-elemental-shields", action = "store_true",
                       help = "Flame, Ice, and Thunder Shields not sold in shops")

    shops.add_argument("-snsb", "--shops-no-super-balls", action = "store_true",
                       help = "Super Balls not sold in shops")
    shops.add_argument("-sesb", "--shops-expensive-super-balls", action = "store_true",
                       help = "Super Balls base price increase")
    

    shops.add_argument("-snee", "--shops-no-exp-eggs", action = "store_true",
                       help = "Exp. Eggs not sold in shops")
    shops.add_argument("-snil", "--shops-no-illuminas", action = "store_true",
                       help = "Illuminas not sold in shops")

def process(args):
    if args.shop_inventory_shuffle_random is not None:
        args.shop_inventory_shuffle_random_percent = args.shop_inventory_shuffle_random
        args.shop_inventory_shuffle_random = True

    args._process_min_max("shop_prices_random_value")
    args._process_min_max("shop_prices_random_percent")

def flags(args):
    flags = ""

    if args.shop_inventory_shuffle_random:
        flags += f" -sisr {args.shop_inventory_shuffle_random_percent}"
    elif args.shop_inventory_random_tiered:
        flags += " -sirt"
    elif args.shop_inventory_empty:
        flags += " -sie"

    if args.shop_prices_random_value:
        flags += f" -sprv {args.shop_prices_random_value_min} {args.shop_prices_random_value_max}"
    elif args.shop_prices_random_percent:
        flags += f" -sprp {args.shop_prices_random_percent_min} {args.shop_prices_random_percent_max}"

    if args.shop_sell_fraction4:
        flags += " -ssf4"
    elif args.shop_sell_fraction8:
        flags += " -ssf8"
    elif args.shop_sell_fraction0:
        flags += " -ssf0"

    if args.shop_dried_meat != 1:
        flags += f" -sdm {args.shop_dried_meat}"
    if args.no_priceless_items:
        flags += " -npi"

    if args.shops_no_breakable_rods:
        flags += " -snbr"
    if args.shops_expensive_breakable_rods:
        flags += " -sebr"

    if args.shops_no_elemental_shields:
        flags += " -snes"

    if args.shops_no_super_balls:
        flags += " -snsb"
    if args.shops_expensive_super_balls:
        flags += " -sesb"

    if args.shops_no_exp_eggs:
        flags += " -snee"
    if args.shops_no_illuminas:
        flags += " -snil"

    return flags

def options(args):
    inventory = "Original"
    if args.shop_inventory_shuffle_random:
        inventory = "Shuffle + Random"
    elif args.shop_inventory_random_tiered:
        inventory = "Random Tiered"
    elif args.shop_inventory_empty:
        inventory = "Empty"

    price = "Original"
    if args.shop_prices_random_value:
        price = f"Random Value {args.shop_prices_random_value_min}-{args.shop_prices_random_value_max}"
    elif args.shop_prices_random_percent:
        price = f"Random Percent {args.shop_prices_random_percent_min}-{args.shop_prices_random_percent_max}%"

    sell_fraction = "1/2"
    if args.shop_sell_fraction4:
        sell_fraction = "1/4"
    elif args.shop_sell_fraction8:
        sell_fraction = "1/8"
    elif args.shop_sell_fraction0:
        sell_fraction = "0"

    breakable_rods = "Available"
    if args.shops_no_breakable_rods:
        breakable_rods = "No"
    elif args.shops_expensive_breakable_rods:
        breakable_rods = "Expensive"

    super_balls = "Available"
    if args.shops_no_super_balls:
        super_balls = "No"
    elif args.shops_expensive_super_balls:
        super_balls = "Expensive"

    result = [("Inventory", inventory)]
    if args.shop_inventory_shuffle_random:
        result.append(("Random Percent", f"{args.shop_inventory_shuffle_random_percent}%"))

    result.extend([
        ("Price", price),
        ("Sell Fraction", sell_fraction),
        ("Dried Meat", args.shop_dried_meat),
        ("No Priceless Items", args.no_priceless_items),
        ("No Breakable Rods", args.shops_no_breakable_rods),
        ("Expensive Rods", args.shops_expensive_breakable_rods),
        ("No Elemental Shields", args.shops_no_elemental_shields),
        ("No Super Balls", args.shops_no_super_balls),
        ("Expensive Balls", args.shops_expensive_super_balls),
        ("No Exp. Eggs", args.shops_no_exp_eggs),
        ("No Illuminas", args.shops_no_illuminas),
    ])
    return result

def menu(args):
    entries = options(args)
    if args.shop_inventory_shuffle_random:
        entries[0] = ("Shuffle + Random", entries[1][1])    # put percent on same line
        del entries[1]                                      # delete random percent line
    else:
        entries[0] = (entries[0][1], "")

    if args.shop_prices_random_value:
        entries[1] = (entries[1][0], entries[1][1].replace("Random Value ", ""))
    elif args.shop_prices_random_percent:
        entries[1] = (entries[1][0], entries[1][1].replace("Random Percent ", ""))
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
