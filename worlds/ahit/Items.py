from BaseClasses import Item, ItemClassification
from .Types import HatDLC, HatType, hat_type_to_item, Difficulty, ItemData, HatInTimeItem
from .Locations import get_total_locations
from .Rules import get_difficulty
from .Options import get_total_time_pieces, CTRLogic
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import HatInTimeWorld


def create_itempool(world: "HatInTimeWorld") -> List[Item]:
    itempool: List[Item] = []
    if world.has_yarn():
        yarn_pool: List[Item] = create_multiple_items(world, "Yarn",
                                                      world.options.YarnAvailable.value,
                                                      ItemClassification.progression_skip_balancing)

        for i in range(int(len(yarn_pool) * (0.01 * world.options.YarnBalancePercent))):
            yarn_pool[i].classification = ItemClassification.progression

        itempool += yarn_pool

    for name in item_table.keys():
        if name == "Yarn":
            continue

        if not item_dlc_enabled(world, name):
            continue

        if not world.options.HatItems and name in hat_type_to_item.values():
            continue

        item_type: ItemClassification = item_table.get(name).classification

        if world.is_dw_only():
            if item_type is ItemClassification.progression \
               or item_type is ItemClassification.progression_skip_balancing:
                continue
        else:
            if name == "Scooter Badge":
                if world.options.CTRLogic == CTRLogic.option_scooter or get_difficulty(world) >= Difficulty.MODERATE:
                    item_type = ItemClassification.progression
            elif name == "No Bonk Badge" and world.is_dw():
                item_type = ItemClassification.progression

        # some death wish bonuses require one hit hero + hookshot
        if world.is_dw() and name == "Badge Pin" and not world.is_dw_only():
            item_type = ItemClassification.progression

        if item_type is ItemClassification.filler or item_type is ItemClassification.trap:
            continue

        if name in act_contracts.keys() and not world.options.ShuffleActContracts:
            continue

        if name in alps_hooks.keys() and not world.options.ShuffleAlpineZiplines:
            continue

        if name == "Progressive Painting Unlock" and not world.options.ShuffleSubconPaintings:
            continue

        if world.options.StartWithCompassBadge and name == "Compass Badge":
            continue

        if name == "Time Piece":
            tp_list: List[Item] = create_multiple_items(world, name, get_total_time_pieces(world), item_type)
            for i in range(int(len(tp_list) * (0.01 * world.options.TimePieceBalancePercent))):
                tp_list[i].classification = ItemClassification.progression

            itempool += tp_list
            continue

        itempool += create_multiple_items(world, name, item_frequencies.get(name, 1), item_type)

    itempool += create_junk_items(world, get_total_locations(world) - len(itempool))
    return itempool


def calculate_yarn_costs(world: "HatInTimeWorld"):
    min_yarn_cost = int(min(world.options.YarnCostMin.value, world.options.YarnCostMax.value))
    max_yarn_cost = int(max(world.options.YarnCostMin.value, world.options.YarnCostMax.value))

    max_cost = 0
    for i in range(5):
        hat: HatType = HatType(i)
        if not world.is_hat_precollected(hat):
            cost: int = world.random.randint(min_yarn_cost, max_yarn_cost)
            world.hat_yarn_costs[hat] = cost
            max_cost += cost
        else:
            world.hat_yarn_costs[hat] = 0

    available_yarn: int = world.options.YarnAvailable.value
    if max_cost > available_yarn:
        world.options.YarnAvailable.value = max_cost
        available_yarn = max_cost

    extra_yarn = max_cost + world.options.MinExtraYarn - available_yarn
    if extra_yarn > 0:
        world.options.YarnAvailable.value += extra_yarn


def item_dlc_enabled(world: "HatInTimeWorld", name: str) -> bool:
    data = item_table[name]

    if data.dlc_flags == HatDLC.none:
        return True
    elif data.dlc_flags == HatDLC.dlc1 and world.is_dlc1():
        return True
    elif data.dlc_flags == HatDLC.dlc2 and world.is_dlc2():
        return True
    elif data.dlc_flags == HatDLC.death_wish and world.is_dw():
        return True

    return False


def create_item(world: "HatInTimeWorld", name: str) -> Item:
    data = item_table[name]
    return HatInTimeItem(name, data.classification, data.code, world.player)


def create_multiple_items(world: "HatInTimeWorld", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:

    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [HatInTimeItem(name, item_type, data.code, world.player)]

    return itemlist


def create_junk_items(world: "HatInTimeWorld", count: int) -> List[Item]:
    trap_chance = world.options.TrapChance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}
    ic: ItemClassification

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            if world.is_dw_only() and "Pons" in name:
                continue

            junk_list[name] = junk_weights.get(name)

        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "Baby Trap":
                trap_list[name] = world.options.BabyTrapWeight.value
            elif name == "Laser Trap":
                trap_list[name] = world.options.LaserTrapWeight.value
            elif name == "Parade Trap":
                trap_list[name] = world.options.ParadeTrapWeight.value

    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool


def get_shop_trap_name(world: "HatInTimeWorld") -> str:
    rand = world.random.randint(1, 9)
    name = ""
    if rand == 1:
        name = "Time Plece"
    elif rand == 2:
        name = "Time Piece (Trust me bro)"
    elif rand == 3:
        name = "TimePiece"
    elif rand == 4:
        name = "Time Piece?"
    elif rand == 5:
        name = "Time Pizza"
    elif rand == 6:
        name = "Time piece"
    elif rand == 7:
        name = "TIme Piece"
    elif rand == 8:
        name = "Time Piece (maybe)"
    elif rand == 9:
        name = "Time Piece ;)"

    return name


ahit_items = {
    "Yarn": ItemData(2000300001, ItemClassification.progression_skip_balancing),
    "Time Piece": ItemData(2000300002, ItemClassification.progression_skip_balancing),

    # for HatItems option
    "Sprint Hat": ItemData(2000300049, ItemClassification.progression),
    "Brewing Hat": ItemData(2000300050, ItemClassification.progression),
    "Ice Hat": ItemData(2000300051, ItemClassification.progression),
    "Dweller Mask": ItemData(2000300052, ItemClassification.progression),
    "Time Stop Hat": ItemData(2000300053, ItemClassification.progression),

    # Badges
    "Projectile Badge": ItemData(2000300024, ItemClassification.useful),
    "Fast Hatter Badge": ItemData(2000300025, ItemClassification.useful),
    "Hover Badge": ItemData(2000300026, ItemClassification.useful),
    "Hookshot Badge": ItemData(2000300027, ItemClassification.progression),
    "Item Magnet Badge": ItemData(2000300028, ItemClassification.useful),
    "No Bonk Badge": ItemData(2000300029, ItemClassification.useful),
    "Compass Badge": ItemData(2000300030, ItemClassification.useful),
    "Scooter Badge": ItemData(2000300031, ItemClassification.useful),
    "One-Hit Hero Badge": ItemData(2000300038, ItemClassification.progression, HatDLC.death_wish),
    "Camera Badge": ItemData(2000300042, ItemClassification.progression, HatDLC.death_wish),

    # Relics
    "Relic (Burger Patty)": ItemData(2000300006, ItemClassification.progression),
    "Relic (Burger Cushion)": ItemData(2000300007, ItemClassification.progression),
    "Relic (Mountain Set)": ItemData(2000300008, ItemClassification.progression),
    "Relic (Train)": ItemData(2000300009, ItemClassification.progression),
    "Relic (UFO)": ItemData(2000300010, ItemClassification.progression),
    "Relic (Cow)": ItemData(2000300011, ItemClassification.progression),
    "Relic (Cool Cow)": ItemData(2000300012, ItemClassification.progression),
    "Relic (Tin-foil Hat Cow)": ItemData(2000300013, ItemClassification.progression),
    "Relic (Crayon Box)": ItemData(2000300014, ItemClassification.progression),
    "Relic (Red Crayon)": ItemData(2000300015, ItemClassification.progression),
    "Relic (Blue Crayon)": ItemData(2000300016, ItemClassification.progression),
    "Relic (Green Crayon)": ItemData(2000300017, ItemClassification.progression),
    # DLC
    "Relic (Cake Stand)": ItemData(2000300018, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Shortcake)": ItemData(2000300019, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Chocolate Cake Slice)": ItemData(2000300020, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Chocolate Cake)": ItemData(2000300021, ItemClassification.progression, HatDLC.dlc1),
    "Relic (Necklace Bust)": ItemData(2000300022, ItemClassification.progression, HatDLC.dlc2),
    "Relic (Necklace)": ItemData(2000300023, ItemClassification.progression, HatDLC.dlc2),

    # Garbage items
    "25 Pons": ItemData(2000300034, ItemClassification.filler),
    "50 Pons": ItemData(2000300035, ItemClassification.filler),
    "100 Pons": ItemData(2000300036, ItemClassification.filler),
    "Health Pon": ItemData(2000300037, ItemClassification.filler),
    "Random Cosmetic": ItemData(2000300044, ItemClassification.filler),

    # Traps
    "Baby Trap": ItemData(2000300039, ItemClassification.trap),
    "Laser Trap": ItemData(2000300040, ItemClassification.trap),
    "Parade Trap": ItemData(2000300041, ItemClassification.trap),

    # Other
    "Badge Pin": ItemData(2000300043, ItemClassification.useful),
    "Umbrella": ItemData(2000300033, ItemClassification.progression),
    "Progressive Painting Unlock": ItemData(2000300003, ItemClassification.progression),
    # DLC
    "Metro Ticket - Yellow": ItemData(2000300045, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Green": ItemData(2000300046, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Blue": ItemData(2000300047, ItemClassification.progression, HatDLC.dlc2),
    "Metro Ticket - Pink": ItemData(2000300048, ItemClassification.progression, HatDLC.dlc2),
}

act_contracts = {
    "Snatcher's Contract - The Subcon Well": ItemData(2000300200, ItemClassification.progression),
    "Snatcher's Contract - Toilet of Doom": ItemData(2000300201, ItemClassification.progression),
    "Snatcher's Contract - Queen Vanessa's Manor": ItemData(2000300202, ItemClassification.progression),
    "Snatcher's Contract - Mail Delivery Service": ItemData(2000300203, ItemClassification.progression),
}

alps_hooks = {
    "Zipline Unlock - The Birdhouse Path": ItemData(2000300204, ItemClassification.progression),
    "Zipline Unlock - The Lava Cake Path": ItemData(2000300205, ItemClassification.progression),
    "Zipline Unlock - The Windmill Path": ItemData(2000300206, ItemClassification.progression),
    "Zipline Unlock - The Twilight Bell Path": ItemData(2000300207, ItemClassification.progression),
}

relic_groups = {
    "Burger": {"Relic (Burger Patty)", "Relic (Burger Cushion)"},
    "Train": {"Relic (Mountain Set)", "Relic (Train)"},
    "UFO": {"Relic (UFO)", "Relic (Cow)", "Relic (Cool Cow)", "Relic (Tin-foil Hat Cow)"},
    "Crayon": {"Relic (Crayon Box)", "Relic (Red Crayon)", "Relic (Blue Crayon)", "Relic (Green Crayon)"},
    "Cake": {"Relic (Cake Stand)", "Relic (Chocolate Cake)", "Relic (Chocolate Cake Slice)", "Relic (Shortcake)"},
    "Necklace": {"Relic (Necklace Bust)", "Relic (Necklace)"},
}

item_frequencies = {
    "Badge Pin": 2,
    "Progressive Painting Unlock": 3,
}

junk_weights = {
    "25 Pons": 50,
    "50 Pons": 25,
    "100 Pons": 10,
    "Health Pon": 35,
    "Random Cosmetic": 35,
}

item_table = {
    **ahit_items,
    **act_contracts,
    **alps_hooks,
}
