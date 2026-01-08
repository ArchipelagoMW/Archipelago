import logging
from typing import List, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .Types import ItemData, GameItem

if TYPE_CHECKING:
    from . import RaC3World

rac3_logger = logging.getLogger("Ratchet & Clank 3")
rac3_logger.setLevel(logging.DEBUG)


def create_itempool(world: "RaC3World") -> List[Item]:
    itempool: List[Item] = []
    options = world.options

    for name in item_table.keys():
        item_type: ItemClassification = item_table.get(name).classification
        item_amount: int = item_table.get(name).count

        # Already placed items (Starting items and vanilla)
        if name in world.preplaced_items:
            if item_amount == 1:
                continue
            else:
                item_amount -= 1  # remove one from the pool as it has already been placed

        # Progressive Weapons option
        if not options.enable_progressive_weapons.value:
            if name in progressive_weapons.keys():
                continue
        else:  # options.EnableProgressiveWeapons.value:
            if name in weapon_items.keys():
                continue

        # ExtraArmorUpgrade option
        if name == "Progressive Armor":
            item_amount += options.extra_armor_upgrade.value

        # Catch accidental duplicates
        if item_amount > 1 and "Progressive" not in name:
            rac3_logger.warning(f"multiple copies of {name} added to the item pool")

        itempool += create_multiple_items(world, name, item_amount, item_type)

    victory = create_item(world, "Biobliterator Defeated!")
    world.multiworld.get_location("Command Center: Biobliterator Defeated!", world.player).place_locked_item(victory)
    return itempool


def create_multiple_items(world: "RaC3World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [GameItem(name, item_type, data.ap_code, world.player)]

    return itemlist


def create_item(world: "RaC3World", name: str) -> Item:
    data = item_table[name]
    return GameItem(name, data.classification, data.ap_code, world.player)


def get_filler_item_selection(world: "RaC3World"):
    frequencies = dict.fromkeys(junk_items.keys(), 1)
    if not world.options.enable_progressive_weapons.value:
        weapon_exp = dict.fromkeys(junk_weapon_exp, 1)
        frequencies.update(weapon_exp)
    # if world.options.traps_enabled:
    #     traps = trap_items.copy()
    #     frequencies.update(traps)
    return [name for name, count in frequencies.items() for _ in range(count)]


weapon_items = {
    "Shock Blaster": ItemData(50000000, ItemClassification.useful, 1),
    "Nitro Launcher": ItemData(50000001, ItemClassification.useful, 1),
    "N60 Storm": ItemData(50000002, ItemClassification.useful, 1),
    "Plasma Whip": ItemData(50000003, ItemClassification.progression, 1),
    "Infector": ItemData(50000004, ItemClassification.progression, 1),
    "Suck Cannon": ItemData(50000005, ItemClassification.progression, 1),
    "Spitting Hydra": ItemData(50000006, ItemClassification.progression, 1),
    "Agents of Doom": ItemData(50000007, ItemClassification.useful, 1),
    "Flux Rifle": ItemData(50000008, ItemClassification.progression, 1),
    "Annihilator": ItemData(50000009, ItemClassification.progression, 1),
    "Holo-Shield Glove": ItemData(50000010, ItemClassification.useful, 1),
    "Disk-Blade Gun": ItemData(50000011, ItemClassification.progression, 1),
    "Rift Inducer": ItemData(50000012, ItemClassification.progression, 1),
    "Qwack-O-Ray": ItemData(50000013, ItemClassification.progression, 1),
    "RY3N0": ItemData(50000014, ItemClassification.progression, 1),
    "Mini-Turret Glove": ItemData(50000015, ItemClassification.useful, 1),
    "Lava Gun": ItemData(50000016, ItemClassification.useful, 1),
    "Shield Charger": ItemData(50000017, ItemClassification.useful, 1),
    "Bouncer": ItemData(50000018, ItemClassification.useful, 1),
    "Plasma Coil": ItemData(50000019, ItemClassification.useful, 1)
}

progressive_weapons = {
    "Progressive Shock Blaster": ItemData(50000020, ItemClassification.useful, 5),
    "Progressive Nitro Launcher": ItemData(50000021, ItemClassification.useful, 5),
    "Progressive N60 Storm": ItemData(50000022, ItemClassification.useful, 5),
    "Progressive Plasma Whip": ItemData(50000023, ItemClassification.progression, 5),
    "Progressive Infector": ItemData(50000024, ItemClassification.progression, 5),
    "Progressive Suck Cannon": ItemData(50000025, ItemClassification.progression, 5),
    "Progressive Spitting Hydra": ItemData(50000026, ItemClassification.progression, 5),
    "Progressive Agents of Doom": ItemData(50000027, ItemClassification.useful, 5),
    "Progressive Flux Rifle": ItemData(50000028, ItemClassification.progression, 5),
    "Progressive Annihilator": ItemData(50000029, ItemClassification.progression, 5),
    "Progressive Holo-Shield Glove": ItemData(50000030, ItemClassification.useful, 5),
    "Progressive Disk-Blade Gun": ItemData(50000031, ItemClassification.progression, 5),
    "Progressive Rift Inducer": ItemData(50000032, ItemClassification.progression, 5),
    "Progressive Qwack-O-Ray": ItemData(50000033, ItemClassification.progression, 5),
    "Progressive RY3N0": ItemData(50000034, ItemClassification.progression, 5),
    "Progressive Mini-Turret Glove": ItemData(50000035, ItemClassification.useful, 5),
    "Progressive Lava Gun": ItemData(50000036, ItemClassification.useful, 5),
    "Progressive Shield Charger": ItemData(50000037, ItemClassification.useful, 5),
    "Progressive Bouncer": ItemData(50000038, ItemClassification.useful, 5),
    "Progressive Plasma Coil": ItemData(50000039, ItemClassification.useful, 5)
}
gadget_items = {
    "Hacker": ItemData(50000040, ItemClassification.progression, 1),
    "Hypershot": ItemData(50000041, ItemClassification.progression, 1),
    "Refractor": ItemData(50000042, ItemClassification.progression, 1),
    "Tyhrra-Guise": ItemData(50000043, ItemClassification.progression, 1),
    "Gravity-Boots": ItemData(50000044, ItemClassification.progression, 1),
    "Bolt Grabber V2": ItemData(50000045, ItemClassification.useful, 1),
    "Map-O-Matic": ItemData(50000046, ItemClassification.useful, 1),
    "Nano Pak": ItemData(50000047, ItemClassification.useful, 1),
    "Warp Pad": ItemData(50000048, ItemClassification.progression, 1),
    "Gadgetron PDA": ItemData(50000049, ItemClassification.useful, 1),
    "Charge-Boots": ItemData(50000050, ItemClassification.progression, 1),
    "Box Breaker": ItemData(50000051, ItemClassification.progression, 1),
    "Master Plan": ItemData(50000052, ItemClassification.progression, 1)
}

post_planets = {
    "Infobot: Florana": ItemData(50000053, ItemClassification.progression, 1),
    "Infobot: Starship Phoenix": ItemData(50000054, ItemClassification.progression, 1),
    "Infobot: Marcadia": ItemData(50000055, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 1
    "Infobot: Annihilation Nation": ItemData(50000056, ItemClassification.progression, 1),
    # Post Starship Phoenix Visit 2 + Qwark VidComic 1
    "Infobot: Aquatos": ItemData(50000057, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 3
    "Infobot: Tyhrranosis": ItemData(50000058, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 4
    "Infobot: Daxx": ItemData(50000059, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 5
    "Infobot: Obani Gemini": ItemData(50000060, ItemClassification.progression, 1),  # Post Daxx
    "Infobot: Blackwater City": ItemData(50000061, ItemClassification.progression, 1),  # Post Obani Gemini
    "Infobot: Holostar Studios": ItemData(50000062, ItemClassification.progression, 1),
    # Post Blackwater City + Annihilation Nation Challenges
    "Infobot: Obani Draco": ItemData(50000063, ItemClassification.progression, 1),  # Post Holostar Studios
    "Infobot: Zeldrin Starport": ItemData(50000064, ItemClassification.progression, 1),  # Post Obani Draco
    "Infobot: Metropolis": ItemData(50000065, ItemClassification.progression, 1),
    # Post Zeldrin Starport + Qwark VidComic 4
    "Infobot: Crash Site": ItemData(50000066, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 7
    "Infobot: Aridia": ItemData(50000067, ItemClassification.progression, 1),  # Post Crash Site
    "Infobot: Qwarks Hideout": ItemData(50000068, ItemClassification.progression, 1),
    # Post Starship Phoenix Visit 8 + Qwark VidComic 5
    "Infobot: Koros": ItemData(50000069, ItemClassification.progression, 1),  # Post Starship Phoenix Visit 9
    "Infobot: Command Center": ItemData(50000070, ItemClassification.progression, 1),  # Post-Koros
}
progressive_vidcomics = {
    "Progressive VidComic": ItemData(50000075, ItemClassification.progression, 5),
}

progressive_armor = {
    "Progressive Armor": ItemData(50000080, ItemClassification.useful, 4),
}

t_bolts = {
    "Titanium Bolt": ItemData(50000090, ItemClassification.filler, 0)
}

junk_weapon_exp = {
    "Weapon EXP": ItemData(50000092, ItemClassification.filler, 0)
}

junk_items = {
    "Bolts": ItemData(50000091, ItemClassification.filler, 0),
    "Inferno Mode": ItemData(50000093, ItemClassification.filler, 0),
    "Jackpot Mode": ItemData(50000094, ItemClassification.filler, 0)
}

victory_item = {
    "Dr. Nefarious Defeated!": ItemData(50000100, ItemClassification.progression, 0),
    "Biobliterator Defeated!": ItemData(50000101, ItemClassification.progression, 0)
}

item_table = {
    **weapon_items,
    **progressive_weapons,
    **gadget_items,
    **post_planets,
    **progressive_vidcomics,
    **progressive_armor,
    **t_bolts,
    **junk_items,
    **junk_weapon_exp,
    **victory_item
}

# Todo: Add Item Groups (see location_groups)
item_group = {

}

# class ItemData(NamedTuple):
#    ap_code: Optional[int]
#    classification: ItemClassification
#    count: Optional[int] = 1

default_starting_weapons = {name: 1 for name in weapon_items.keys()}


def filter_items(classification):
    return filter(lambda l: l[1].classification == classification, item_table.items())


def filter_item_names(classification):
    return map(lambda entry: entry[0], filter_items(classification))


def starting_weapons(world, weapon_dict: dict[str, int]) -> list[str]:
    weapon_list: list[str] = []
    for name in weapon_dict:
        count = weapon_dict[name]
        if count == 0:
            continue
        if world.options.enable_progressive_weapons.value:
            for i in range(count):
                weapon_list.append(f"Progressive {name}")
        else:
            weapon_list.append(name)
    world.random.shuffle(weapon_list)
    return [weapon_list[0], weapon_list[1]]
