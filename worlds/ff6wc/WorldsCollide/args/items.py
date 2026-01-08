def name():
    return "Items"

def parse(parser):
    from ..data.characters import Characters
    items = parser.add_argument_group("Items")

    items_equipable = items.add_mutually_exclusive_group()
    items_equipable.add_argument("-ier", "--item-equipable-random",
                                 default = None, type = int, nargs = 2, metavar = ("MIN", "MAX"),
                                 choices = range(Characters.CHARACTER_COUNT + 1),
                                 help = "Each item equipable by between %(metavar)s random characters")
    items_equipable.add_argument("-iebr", "--item-equipable-balanced-random",
                                 default = None, type = int, metavar = "VALUE",
                                 choices = range(Characters.CHARACTER_COUNT + 1),
                                 help = "Each item equipable by %(metavar)s random characters. Total number of items equipable by each character is balanced")
    items_equipable.add_argument("-ietr", "--item-equipable-tiered-random",action = "store_true",
                                 help = "Equipment is categorized by tier and chance of being equipable by a character is chosen at random. Higher tier equipment is less likely to be equipable.")
    items_equipable.add_argument("-ieor", "--item-equipable-original-random",
                                 default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                 help = "Characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")
    items_equipable.add_argument("-iesr", "--item-equipable-shuffle-random",
                                 default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                 help = "Shuffle character equipment. After randomization, characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")

    items_equipable_relic = items.add_mutually_exclusive_group()
    items_equipable_relic.add_argument("-ierr", "--item-equipable-relic-random",
                                       default = None, type = int, nargs = 2, metavar = ("MIN", "MAX"),
                                       choices = range(Characters.CHARACTER_COUNT + 1),
                                       help = "Each relic equipable by between %(metavar)s random characters")
    items_equipable_relic.add_argument("-ierbr", "--item-equipable-relic-balanced-random",
                                       default = None, type = int, metavar = "VALUE",
                                       choices = range(Characters.CHARACTER_COUNT + 1),
                                       help = "Each relic equipable by %(metavar)s random characters. Total number of relics equipable by each character is balanced")
    items_equipable_relic.add_argument("-iertr", "--item-equipable-relic-tiered-random", action="store_true",
                                       help="Relics are categorized by tier and chance of being equipable by a character is chosen at random. Higher tier relics are less likely to be equipable.")
    items_equipable_relic.add_argument("-ieror", "--item-equipable-relic-original-random",
                                       default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                       help = "Characters have a %(metavar)s chance of being able to equip each relic they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each relic they could previously equip")
    items_equipable_relic.add_argument("-iersr", "--item-equipable-relic-shuffle-random",
                                       default = None, type = int, metavar = "PERCENT", choices = range(-100, 101),
                                       help = "Shuffle character relics. After randomization, characters have a %(metavar)s chance of being able to equip each item they could not previously equip. If %(metavar)s negative, characters have a -%(metavar)s chance of not being able to equip each item they could previously equip")
    items.add_argument("-ir", "--item-rewards", type=str,
                       help="Choose which items will be received as check rewards")
    items.add_argument("-csb", "--cursed-shield-battles", default = [256, 256], type = int,
                       nargs = 2, metavar = ("MIN", "MAX"), choices = range(257),
                       help = "Number of battles required to uncurse the cursed shield")

    items.add_argument("-mca", "--moogle-charm-all", action = "store_true",
                       help = "All characters can wear Moogle Charm relics which prevent random battles. Overrides Equipable option")
    items.add_argument("-stra", "--swdtech-runic-all", action = "store_true",
                       help = "All weapons enable swdtech and runic")

    items.add_argument("-saw", "--stronger-atma-weapon", action = "store_true",
                       help = "Atma Weapon moved to higher tier and divisor reduced from 64 to 32")

def process(args):
    from ..constants.items import good_items, stronger_items, premium_items
    from ..constants.items import id_name, name_id

    args._process_min_max("item_equipable_random")
    if args.item_equipable_balanced_random is not None:
        args.item_equipable_balanced_random_value = args.item_equipable_balanced_random
        args.item_equipable_balanced_random = True
    if args.item_equipable_original_random is not None:
        args.item_equipable_original_random_percent = args.item_equipable_original_random
        args.item_equipable_original_random = True
    if args.item_equipable_shuffle_random is not None:
        args.item_equipable_shuffle_random_percent = args.item_equipable_shuffle_random
        args.item_equipable_shuffle_random = True

    args._process_min_max("item_equipable_relic_random")
    if args.item_equipable_relic_balanced_random is not None:
        args.item_equipable_relic_balanced_random_value = args.item_equipable_relic_balanced_random
        args.item_equipable_relic_balanced_random = True
    if args.item_equipable_relic_original_random is not None:
        args.item_equipable_relic_original_random_percent = args.item_equipable_relic_original_random
        args.item_equipable_relic_original_random = True
    if args.item_equipable_relic_shuffle_random is not None:
        args.item_equipable_relic_shuffle_random_percent = args.item_equipable_relic_shuffle_random
        args.item_equipable_relic_shuffle_random = True

    args.item_rewards_ids = []

    if not args.item_rewards:
        args.item_rewards = 'standard'

    # Split the comma-separated string
    for a_item_id in args.item_rewards.split(','):
        # look for strings first
        a_item_id = a_item_id.lower().strip()
        if a_item_id == 'none':
            args.item_rewards_ids = []
        elif a_item_id == 'standard':
            args.item_rewards_ids = [name_id[name] for name in good_items]
        elif a_item_id == 'stronger':
            args.item_rewards_ids = [name_id[name] for name in stronger_items]
        elif a_item_id == 'premium':
            args.item_rewards_ids = [name_id[name] for name in premium_items]
        else:
            item_ids_lower = {k.lower(): v for k, v in name_id.items()}
            if a_item_id in item_ids_lower:
                args.item_rewards_ids.append(item_ids_lower[a_item_id])
            else:
                # assuming it's a number... it'll error out if not
                args.item_rewards_ids.append(int(a_item_id))

    # remove duplicates and sort
    args.item_rewards_ids = list(set(args.item_rewards_ids))
    args.item_rewards_ids.sort()

    # Remove Atma Weapon is it's not Stronger and we're in standard/premium
    if not args.stronger_atma_weapon and name_id["Atma Weapon"] in args.item_rewards_ids \
       and any(s.lower().strip() in args.item_rewards.split(',') for s in ('none', 'standard', 'stronger', 'premium')):
        args.item_rewards_ids.remove(name_id["Atma Weapon"])

    # Remove excluded items
    if args.no_free_paladin_shields and name_id["Paladin Shld"] in args.item_rewards_ids:
        args.item_rewards_ids.remove(name_id["Paladin Shld"])
    if args.no_exp_eggs and name_id["Exp. Egg"] in args.item_rewards_ids:
        args.item_rewards_ids.remove(name_id["Exp. Egg"])
    if args.no_illuminas and name_id["Illumina"] in args.item_rewards_ids:
        args.item_rewards_ids.remove(name_id["Illumina"])
    if args.no_sprint_shoes and name_id["Sprint Shoes"] in args.item_rewards_ids:
        args.item_rewards_ids.remove(name_id["Sprint Shoes"])
    if args.no_moogle_charms and name_id["Moogle Charm"] in args.item_rewards_ids:
        args.item_rewards_ids.remove(name_id["Moogle Charm"])

    # Make dead checks award "empty" if the item reward list is empty (e.g. all items were supposed to be Illuminas and
    # the No Illumina flag is on)
    if len(args.item_rewards_ids) < 1:
        args.item_rewards_ids.append(name_id["Empty"])

    # always add ArchplgoItem into reward pool so AP can process it later
    args.item_rewards_ids.append(name_id["ArchplgoItem"])

    args._process_min_max("cursed_shield_battles")
    args.cursed_shield_battles_original = args.cursed_shield_battles_min == 256 and\
                                          args.cursed_shield_battles_max == 256

def flags(args):
    flags = ""

    if args.item_equipable_random:
        flags += f" -ier {args.item_equipable_random_min} {args.item_equipable_random_max}"
    elif args.item_equipable_balanced_random:
        flags += f" -iebr {args.item_equipable_balanced_random_value}"
    elif args.item_equipable_tiered_random:
        flags += f" -ietr"
    elif args.item_equipable_original_random:
        flags += f" -ieor {args.item_equipable_original_random_percent}"
    elif args.item_equipable_shuffle_random:
        flags += f" -iesr {args.item_equipable_shuffle_random_percent}"

    if args.item_equipable_relic_random:
        flags += f" -ierr {args.item_equipable_relic_random_min} {args.item_equipable_relic_random_max}"
    elif args.item_equipable_relic_balanced_random:
        flags += f" -ierbr {args.item_equipable_relic_balanced_random_value}"
    elif args.item_equipable_relic_tiered_random:
        flags += f" -iertr"
    elif args.item_equipable_relic_original_random:
        flags += f" -ieror {args.item_equipable_relic_original_random_percent}"
    elif args.item_equipable_relic_shuffle_random:
        flags += f" -iersr {args.item_equipable_relic_shuffle_random_percent}"

    if args.item_rewards:
        flags += f" -ir {args.item_rewards}"

    if args.cursed_shield_battles_min != 256 or args.cursed_shield_battles_max != 256:
        flags += f" -csb {args.cursed_shield_battles_min} {args.cursed_shield_battles_max}"

    if args.moogle_charm_all:
        flags += " -mca"
    if args.swdtech_runic_all:
        flags += " -stra"

    if args.stronger_atma_weapon:
        flags += " -saw"

    return flags

def options(args):
    equipable = "Original"
    if args.item_equipable_random:
        equipable = f"Random {args.item_equipable_random_min}-{args.item_equipable_random_max}"
    elif args.item_equipable_balanced_random:
        equipable = f"Balanced Random {args.item_equipable_balanced_random_value}"
    elif args.item_equipable_tiered_random:
        equipable = f"Tiered Random"
    elif args.item_equipable_original_random:
        equipable = f"Original + Random {args.item_equipable_original_random_percent}%"
    elif args.item_equipable_shuffle_random:
        equipable = f"Shuffle + Random {args.item_equipable_shuffle_random_percent}%"

    equipable_relics = "Original"
    if args.item_equipable_relic_random:
        equipable_relics = f"Random {args.item_equipable_relic_random_min}-{args.item_equipable_relic_random_max}"
    elif args.item_equipable_relic_balanced_random:
        equipable_relics = f"Balanced Random {args.item_equipable_relic_balanced_random_value}"
    elif args.item_equipable_relic_tiered_random:
        equipable_relics = f"Tiered Random"
    elif args.item_equipable_relic_original_random:
        equipable_relics = f"Original + Random {args.item_equipable_relic_original_random_percent}%"
    elif args.item_equipable_relic_shuffle_random:
        equipable_relics = f"Shuffle + Random {args.item_equipable_relic_shuffle_random_percent}%"

    cursed_shield_battles = f"{args.cursed_shield_battles_min}-{args.cursed_shield_battles_max}"

    return [
        ("Equipable", equipable),
        ("Equipable Relics", equipable_relics),
        ("Cursed Shield Battles", cursed_shield_battles),
        ("Moogle Charm All", args.moogle_charm_all),
        ("SwdTech Runic All", args.swdtech_runic_all),
        ("Stronger Atma Weapon", args.stronger_atma_weapon),
        ("Item Rewards", args.item_rewards_ids),
    ]


def _format_items_log_entries(item_ids):
    from ..constants.items import id_name
    item_entries = []
    for item_id in item_ids:
        item_entries.append(("", id_name[item_id]))
    return item_entries


def menu(args):
    from ..menus.flags_reward_items import FlagsRewardItems

    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        try:
            if key == "Equipable":
                key = "Equip"
            elif key == "Equipable Relics":
                key = "EquipR"
            elif key == "Item Rewards":
                entries[index] = ("Item Rewards", FlagsRewardItems(value))  # flags sub-menu
            elif key == "Cursed Shield Battles":
                key = "Cursed Shield"
            value = value.replace("Balanced Random", "Balanced")
            value = value.replace("Tiered Random", "Tiered")
            value = value.replace("Original + Random", "Original + ")
            value = value.replace("Shuffle + Random", "Shuffle + ")
            entries[index] = (key, value)
        except:
            pass
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    '''for entry in entries:
        log.append(format_option(*entry))
    '''
    for entry in entries:
        key, value, unique_name = entry
        if key == "Item Rewards":
            if len(value) == 0:
                entry = (key, "None")
            else:
                entry = (key, "")  # The entries will show up on subsequent lines
            log.append(format_option(*entry))
            for item_entry in _format_items_log_entries(value):
                log.append(format_option(*item_entry))
        else:
            log.append(format_option(*entry))

    return log
