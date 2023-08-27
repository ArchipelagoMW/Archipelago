from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from .Types import HatDLC
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification
    dlc_flags: typing.Optional[HatDLC] = HatDLC.none


class HatInTimeItem(Item):
    game: str = "A Hat in Time"


def item_dlc_enabled(world: World, name: str) -> bool:
    data = item_table[name]

    if data.dlc_flags == HatDLC.none:
        return True
    elif data.dlc_flags == HatDLC.dlc1 and world.multiworld.EnableDLC1[world.player].value > 0:
        return True
    elif data.dlc_flags == HatDLC.dlc2 and world.multiworld.EnableDLC2[world.player].value > 0:
        return True
    elif data.dlc_flags == HatDLC.death_wish and world.multiworld.EnableDeathWish[world.player].value > 0:
        return True

    return False


def get_total_time_pieces(world: World) -> int:
    count: int = 40
    if world.multiworld.EnableDLC1[world.player].value > 0:
        count += 6

    return min(40+world.multiworld.MaxExtraTimePieces[world.player].value, count)


def create_item(world: World, name: str) -> Item:
    data = item_table[name]
    return HatInTimeItem(name, data.classification, data.code, world.player)


def create_multiple_items(world: World, name: str, count: int = 1) -> typing.List[Item]:
    data = item_table[name]
    itemlist: typing.List[Item] = []

    for i in range(count):
        itemlist += [HatInTimeItem(name, data.classification, data.code, world.player)]

    return itemlist


def create_junk_items(world: World, count: int) -> typing.List[Item]:
    trap_chance = world.multiworld.TrapChance[world.player].value
    junk_pool: typing.List[Item] = []
    junk_list: typing.Dict[str, int] = {}
    trap_list: typing.Dict[str, int] = {}
    ic: ItemClassification

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)
        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "Baby Trap":
                trap_list[name] = world.multiworld.BabyTrapWeight[world.player].value
            elif name == "Laser Trap":
                trap_list[name] = world.multiworld.LaserTrapWeight[world.player].value
            elif name == "Parade Trap":
                trap_list[name] = world.multiworld.ParadeTrapWeight[world.player].value

    for i in range(count):
        if trap_chance > 0 and world.multiworld.random.randint(1, 100) <= trap_chance:
            junk_pool += [world.create_item(
                world.multiworld.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0])]
        else:
            junk_pool += [world.create_item(
                world.multiworld.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0])]

    return junk_pool


ahit_items = {
    "Yarn": ItemData(300001, ItemClassification.progression_skip_balancing),
    "Time Piece": ItemData(300002, ItemClassification.progression_skip_balancing),
    "Progressive Painting Unlock": ItemData(300003, ItemClassification.progression),

    # Relics
    "Relic (Burger Patty)": ItemData(300006, ItemClassification.progression),
    "Relic (Burger Cushion)": ItemData(300007, ItemClassification.progression),
    "Relic (Mountain Set)": ItemData(300008, ItemClassification.progression),
    "Relic (Train)": ItemData(300009, ItemClassification.progression),
    "Relic (UFO)": ItemData(300010, ItemClassification.progression),
    "Relic (Cow)": ItemData(300011, ItemClassification.progression),
    "Relic (Cool Cow)": ItemData(300012, ItemClassification.progression),
    "Relic (Tin-foil Hat Cow)": ItemData(300013, ItemClassification.progression),
    "Relic (Crayon Box)": ItemData(300014, ItemClassification.progression),
    "Relic (Red Crayon)": ItemData(300015, ItemClassification.progression),
    "Relic (Blue Crayon)": ItemData(300016, ItemClassification.progression),
    "Relic (Green Crayon)": ItemData(300017, ItemClassification.progression),

    # Badges
    "Projectile Badge": ItemData(300024, ItemClassification.useful),
    "Fast Hatter Badge": ItemData(300025, ItemClassification.useful),
    "Hover Badge": ItemData(300026, ItemClassification.useful),
    "Hookshot Badge": ItemData(300027, ItemClassification.progression),
    "Item Magnet Badge": ItemData(300028, ItemClassification.useful),
    "No Bonk Badge": ItemData(300029, ItemClassification.useful),
    "Compass Badge": ItemData(300030, ItemClassification.useful),
    "Scooter Badge": ItemData(300031, ItemClassification.progression),
    "Badge Pin": ItemData(300043, ItemClassification.useful),

    # Other
    # "Rift Token": ItemData(300032, ItemClassification.filler),
    "Random Cosmetic": ItemData(300044, ItemClassification.filler),
    "Umbrella": ItemData(300033, ItemClassification.progression),

    # Garbage items
    "25 Pons": ItemData(300034, ItemClassification.filler),
    "50 Pons": ItemData(300035, ItemClassification.filler),
    "100 Pons": ItemData(300036, ItemClassification.filler),
    "Health Pon": ItemData(300037, ItemClassification.filler),

    # Traps
    "Baby Trap": ItemData(300039, ItemClassification.trap),
    "Laser Trap": ItemData(300040, ItemClassification.trap),
    "Parade Trap": ItemData(300041, ItemClassification.trap),

    # DLC1 items
    "Relic (Cake Stand)": ItemData(300018, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Cake)": ItemData(300019, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Cake Slice)": ItemData(300020, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Shortcake)": ItemData(300021, ItemClassification.progression, HatDLC.dlc1),

    # DLC2 items
    "Relic (Necklace Bust)": ItemData(300022, ItemClassification.progression, HatDLC.dlc2),
    "Relic (Necklace)": ItemData(300023, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Yellow": ItemData(300045, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Green": ItemData(300046, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Blue": ItemData(300047, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Pink": ItemData(300048, ItemClassification.progression, HatDLC.dlc2),

    # Death Wish items
    "One-Hit Hero Badge": ItemData(300038, ItemClassification.progression, HatDLC.death_wish),
    "Camera Badge": ItemData(300042, ItemClassification.progression, HatDLC.death_wish),
}

act_contracts = {
    "Snatcher's Contract - The Subcon Well": ItemData(300200, ItemClassification.progression),
    "Snatcher's Contract - Toilet of Doom": ItemData(300201, ItemClassification.progression),
    "Snatcher's Contract - Queen Vanessa's Manor": ItemData(300202, ItemClassification.progression),
    "Snatcher's Contract - Mail Delivery Service": ItemData(300203, ItemClassification.progression),
}

alps_hooks = {
    "Zipline Unlock - The Birdhouse Path": ItemData(300204, ItemClassification.progression),
    "Zipline Unlock - The Lava Cake Path": ItemData(300205, ItemClassification.progression),
    "Zipline Unlock - The Windmill Path": ItemData(300206, ItemClassification.progression),
    "Zipline Unlock - The Twilight Bell Path": ItemData(300207, ItemClassification.progression),
}

relic_groups = {
    "Burger": {"Relic (Burger Patty)", "Relic (Burger Cushion)"},
    "Train": {"Relic (Mountain Set)", "Relic (Train)"},
    "UFO": {"Relic (UFO)", "Relic (Cow)", "Relic (Cool Cow)", "Relic (Tin-foil Hat Cow)"},
    "Crayon": {"Relic (Crayon Box)", "Relic (Red Crayon)", "Relic (Blue Crayon)", "Relic (Green Crayon)"},
    "Cake": {"Relic (Cake Stand)", "Relic (Cake)", "Relic (Cake Slice)", "Relic (Shortcake)"},
    "Necklace": {"Relic (Necklace Bust)", "Relic (Necklace)"},
}

item_frequencies = {
    "Badge Pin": 2,
    "Progressive Painting Unlock": 3,
}

junk_weights = {
    "25 Pons": 50,
    "50 Pons": 10,
    "Health Pon": 35,
    "100 Pons": 5,
    "Random Cosmetic": 25,
}

item_table = {
    **ahit_items,
    **act_contracts,
    **alps_hooks,
}
