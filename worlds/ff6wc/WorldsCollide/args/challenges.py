def name():
    return "Challenges"

def parse(parser):
    challenges = parser.add_argument_group("Challenges")
    challenges.add_argument("-nmc", "--no-moogle-charms", action = "store_true",
                            help = "Moogle Charms will not appear in coliseum/auction/shops/chests/events")
    challenges.add_argument("-nee", "--no-exp-eggs", action = "store_true",
                            help = "Exp. Eggs will not appear in coliseum/auction/shops/chests/events")
    challenges.add_argument("-nil", "--no-illuminas", action = "store_true",
                            help = "Illuminas will not appear in coliseum/auction/shops/chests/events")
    ultima = challenges.add_mutually_exclusive_group()
    challenges.add_argument("-noshoes", "--no-sprint-shoes", action = "store_true",
                            help = "Sprint Shoes will not appear in coliseum/auction/shops/chests")
    ultima.add_argument("-nu", "--no-ultima", action = "store_true",
                            help = "Ultima cannot be learned from espers/items/natural magic")
    ultima.add_argument("-u254", "--ultima-254-mp", action = "store_true",
                            help = "Ultima costs 254 MP")
    challenges.add_argument("-nfps", "--no-free-paladin-shields", action = "store_true",
                            help = "Paladin/Cursed Shields will not appear in coliseum/auction/shops/chests/events (Narshe WOR exclusive)")
    challenges.add_argument("-nfce", "--no-free-characters-espers", action = "store_true",
                            help = "Remove character/esper rewards from: Auction House, Collapsing House, Figaro Castle Throne, Gau's Father's House, Kohlingen Inn, Narshe Weapon Shop, Sealed Gate, South Figaro Basement")
    challenges.add_argument("-pd", "--permadeath", action = "store_true",
                            help = "Life spells cannot be learned. Fenix Downs unavailable (except from starting items). Buckets/inns/tents/events do not revive characters. Phoenix casts Life 3 on party instead of Life")
    challenges.add_argument("-rls", "--remove-learnable-spells", type = str,
                            help = "Remove spells from learnable sources: Items, Espers, Natural Magic, and Objectives")
    challenges.add_argument("-nosaves", "--no-saves", action = "store_true",
                            help = "Ironmog Mode: You cannot save (but save points still work for Tents/Sleeping Bags)")

def process(args):
    from ..constants.spells import black_magic_ids, white_magic_ids, gray_magic_ids, spell_id
    from ..data.esper_spell_tiers import top_spells
    # If no_ultima is on, add it to our exclude list for downstream use
    # If permadeath is on, add it to our exclude list for downstream use
    args.remove_learnable_spell_ids = []
    if args.no_ultima:
        args.remove_learnable_spell_ids.append(spell_id["Ultima"])
    if args.permadeath:
        args.remove_learnable_spell_ids.append(spell_id["Life"])
        args.remove_learnable_spell_ids.append(spell_id["Life 2"])

    if args.remove_learnable_spells:
        # Split the comma-separated string
        for a_spell_id in args.remove_learnable_spells.split(','):
            # look for strings first
            a_spell_id = a_spell_id.lower().strip()
            if a_spell_id == 'all':
                args.remove_learnable_spell_ids.extend(range(len(spell_id)))
            elif a_spell_id == 'white':
                args.remove_learnable_spell_ids.extend(white_magic_ids)
            elif a_spell_id == 'black':
                args.remove_learnable_spell_ids.extend(black_magic_ids)
            elif a_spell_id == 'gray' or a_spell_id == 'grey':
                args.remove_learnable_spell_ids.extend(gray_magic_ids)
            elif a_spell_id == 'top':
                args.remove_learnable_spell_ids.extend(top_spells)
            else:
                spell_ids_lower = {k.lower():v for k,v in spell_id.items()}
                if a_spell_id in spell_ids_lower:
                    args.remove_learnable_spell_ids.append(spell_ids_lower[a_spell_id])
                else:
                    # assuming it's a number... it'll error out if not
                    args.remove_learnable_spell_ids.append(int(a_spell_id))
    # remove duplicates and sort
    args.remove_learnable_spell_ids = list(set(args.remove_learnable_spell_ids))
    args.remove_learnable_spell_ids.sort()

def flags(args):
    flags = ""

    if args.no_moogle_charms:
        flags += " -nmc"
    if args.no_exp_eggs:
        flags += " -nee"
    if args.no_illuminas:
        flags += " -nil"
    if args.no_sprint_shoes:
        flags += " -noshoes"

    if args.no_ultima:
        flags += " -nu"
    elif args.ultima_254_mp:
        flags += " -u254"

    if args.no_free_paladin_shields:
        flags += " -nfps"
    if args.no_free_characters_espers:
        flags += " -nfce"
    if args.permadeath:
        flags += " -pd"
    if args.remove_learnable_spells:
        flags += f" -rls {args.remove_learnable_spells}"
    if args.no_saves:
        flags += " -nosaves"

    return flags

def options(args):
    ultima = "Original"
    if args.no_ultima:
        ultima = "N/A"
    elif args.ultima_254_mp:
        ultima = "254 MP"

    return [
        ("No Moogle Charms", args.no_moogle_charms),
        ("No Exp Eggs", args.no_exp_eggs),
        ("No Illuminas", args.no_illuminas),
        ("No Sprint Shoes", args.no_sprint_shoes),
        ("No Free Paladin Shields", args.no_free_paladin_shields),
        ("No Free Characters/Espers", args.no_free_characters_espers),
        ("Permadeath", args.permadeath),
        ("Ultima", ultima),
        ("Remove Learnable Spells", args.remove_learnable_spell_ids),
        ("No Saves", args.no_saves),
    ]


def _format_spells_log_entries(spell_ids):
    from ..constants.spells import id_spell
    spell_entries = []
    for i, spell_id in enumerate(spell_ids):
        spell_entries.append(("", id_spell[spell_id], f"rls_{i}"))
    return spell_entries

def _format_spells_log_entries(spell_ids):
    from ..constants.spells import id_spell
    spell_entries = []
    for spell_id in spell_ids:
        spell_entries.append(("", id_spell[spell_id]))
    return spell_entries

def menu(args):
    from ..menus.flags_remove_learnable_spells import FlagsRemoveLearnableSpells

    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == "No Free Paladin Shields":
            entries[index] = ("No Free Paladin Shlds", entry[1])
        elif key == "No Free Characters/Espers":
            entries[index] = ("No Free Chars/Espers", entry[1])
        elif key == "Remove Learnable Spells":
            entries[index] = ("Remove L. Spells", FlagsRemoveLearnableSpells(value)) # flags sub-menu

    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        key, value = entry
        if key == "Remove Learnable Spells":
            if len(value) == 0:
                entry = (key, "None")
            else:
                entry = (key, "") # The entries will show up on subsequent lines
            log.append(format_option(*entry))
            for spell_entry in _format_spells_log_entries(value):
                log.append(format_option(*spell_entry))
        else:
            log.append(format_option(*entry))

    return log
