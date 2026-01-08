import copy
import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional, Dict, List

from BaseClasses import Item, ItemClassification
from Options import OptionError


class TCGSimulatorItem(Item):
    game: str = "TCG Card Shop Simulator"


@dataclass
class ItemData:
    code: int
    classification: ItemClassification
    amount: Optional[int] = 1

def create_item(world, name: str, classification: ItemClassification, amount: Optional[int] = 1):
    for i in range(amount):
        world.itempool.append(Item(name, classification, world.item_name_to_id[name], world.player))


def generate_ghost_card_items(world, ghost_goal_amount, locs_available):
    if locs_available * 5 < ghost_goal_amount:
        raise OptionError("Not enough locations for ghost goal")

    result = []
    remaining = ghost_goal_amount
    remaining_slots = locs_available

    while remaining > 0 and remaining_slots > 0:
        max_size = min(5 if remaining_slots < 50 else 2, remaining)
        min_size = max(1, remaining - (remaining_slots - 1) * 5)
        size = world.random.randint(min_size, max_size)

        result.append(size)
        remaining -= size
        remaining_slots -= 1

    return result


def create_items(world):

    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    # print(f"total locs at start {total_location_count}")
    # print(f"total Itempool at start {len(world.itempool)}")

    #grab starting items for precollection
    starting_items: List[Item] = []

    for item_id in world.starting_item_ids:
        starting_items.append(Item(world.item_id_to_name[item_id], ItemClassification.progression, item_id, world.player))

    if world.options.start_with_worker.value > 0:
        starting_items.append(
            Item(world.item_id_to_name[218 + world.options.start_with_worker.value], ItemClassification.progression, (218 + world.options.start_with_worker.value), world.player))
    starting_items.append(Item("FormatStandard", ItemClassification.useful, not_sellable_dict["FormatStandard"].code ,world.player))
    starting_items.append(Item("Progressive Shelf", ItemClassification.useful, not_sellable_dict["Progressive Shelf"].code ,world.player))
    #create all items except ghosts and junk
    num = 0
    for item_name, item_data in item_dict.items():
        if (item_data.code in world.pg1_licenses or
        item_data.code in world.pg2_licenses or
        item_data.code in world.pg3_licenses or
        item_data.code in world.tt_licenses) and item_data.code not in world.starting_item_ids:
            create_item(world, item_name, item_data.classification, item_data.amount)

    if total_location_count > 140:
        for item_name, item_data in not_sellable_dict.items():
            amount = item_data.amount
            if item_name in (item.name for item in starting_items):
                amount -= 1
            create_item(world, item_name, item_data.classification, amount)
    else:
        remaining_items = copy.deepcopy(not_sellable_dict)

        for item in starting_items:
            if item.name in remaining_items:
                remaining_items[item.name].amount -= 1
        # Add one of each progression item
        for item_name, item_data in remaining_items.items():
            if item_data.classification == ItemClassification.progression and item_data.amount > 0:
                if item_name not in (item.name for item in starting_items):
                    create_item(world, item_name, item_data.classification, 1)
                    item_data.amount -= 1

        worker_items = [name for name, data in remaining_items.items()
                        if name.startswith("Worker - ") and data.amount > 0]
        if worker_items:
            worker_name = world.random.choice(worker_items)
            worker_data = remaining_items[worker_name]
            create_item(world, worker_name, worker_data.classification, 1)
            worker_data.amount -= 1

        while len(world.itempool) < total_location_count * 0.9:
            eligible_items = [name for name, data in remaining_items.items() if data.amount > 0]
            if not eligible_items:
                break  # Nothing left to add
            item_name = world.random.choice(eligible_items)
            item_data = remaining_items[item_name]
            if item_data.amount > 0:
                create_item(world, item_name, item_data.classification, 1)
                item_data.amount -= 1
                if item_data.amount == 0:
                    del remaining_items[item_name]


    #create Ghost if in goal
    remaining_locations: int = total_location_count - len(world.itempool)
    ghost_counts = 0
    if world.options.goal.value == 2:
        ghost_items = generate_ghost_card_items(world, world.options.ghost_goal_amount.value, remaining_locations)

        ghost_counts = Counter(ghost_items)
        # print(f"ghost counts: {ghost_counts} from {ghost_items}")
        for bagsize, amount in ghost_counts.items():
            plural = "s" if bagsize > 1 else ""
            item_name = f"{bagsize} Ghost Card{plural}"
            create_item(world, item_name, ItemClassification.progression, amount)

        remaining_locations = remaining_locations - len(ghost_items)

    # print(f"Remaining locations here: {remaining_locations}")

    #traps and junk
    trap_count = round(remaining_locations * world.options.trap_fill.value / 100)

    # -1 on LevelGoal because I place a victory item at the goal level
    junk_count = remaining_locations - trap_count - (1 if world.options.goal == 0 else 0)

    print(f"junk count {junk_count + trap_count}")

    trap_weights = {
        "Stink Trap": world.options.stink_trap,
        "Poltergeist Trap": world.options.poltergeist_trap,
        "Credit Card Failure Trap": world.options.credit_card_failure_trap,
        "Market Change Trap":world.options.market_change_trap,
        "Decrease Card Luck":world.options.decrease_card_luck_trap,
        "Currency Trap":world.options.currency_trap
    }

    junk_weights["Small Xp"] =  world.options.xp_boosts * 0.5
    junk_weights["Medium Xp"] = world.options.xp_boosts * 0.3
    junk_weights["Large Xp"] = world.options.xp_boosts * 0.2
    junk_weights["Small Money"] = world.options.money_bags * 0.5
    junk_weights["Medium Money"] = world.options.money_bags * 0.3
    junk_weights["Large Money"] = world.options.money_bags * 0.2
    junk_weights["Random Card"] = world.options.random_card
    junk_weights["Random New Card"] = world.options.random_new_card
    junk_weights["Progressive Customer Money"] = world.options.customer_wealth
    junk_weights["Increase Card Luck"] = world.options.card_luck

    junk = get_junk_item_names(world.multiworld.random, junk_count)

    for name in junk:
        create_item(world, name, ItemClassification.filler)

    trap = get_trap_item_names(world.multiworld.random, trap_count, trap_weights)
    for name in trap:
        create_item(world, name, ItemClassification.trap)
    world.multiworld.itempool += world.itempool
    if len(world.itempool) > total_location_count:
        print(f"WARNING: Overfilled pool by {len(world.itempool) - total_location_count} items!")
    return starting_items, ghost_counts

def get_junk_item_names(rand, k: int) -> str:
    junk = rand.choices(
        list(junk_weights.keys()),
        weights=list(junk_weights.values()),
        k=k)
    return junk


def get_trap_item_names(rand, k: int, trap_weights) -> str:
    trap = rand.choices(
        list(trap_weights.keys()),
        weights=list(trap_weights.values()),
        k=k)
    return trap


item_dict: Dict[str, ItemData] = {
    "Fire Battle Deck": ItemData(55, ItemClassification.progression),
    "Earth Battle Deck": ItemData(56, ItemClassification.progression),
    "Water Battle Deck": ItemData(57, ItemClassification.progression),
    "Wind Battle Deck": ItemData(58, ItemClassification.progression),
    "Fire Destiny Deck": ItemData(59, ItemClassification.progression),
    "Earth Destiny Deck": ItemData(60, ItemClassification.progression),
    "Water Destiny Deck": ItemData(61, ItemClassification.progression),
    "Wind Destiny Deck": ItemData(62, ItemClassification.progression),
    "Card Sleeves (Clear)": ItemData(63, ItemClassification.progression),
    "Card Sleeves (Tetramon)": ItemData(64, ItemClassification.progression),
    "D20 Dice Red": ItemData(29, ItemClassification.progression),
    "D20 Dice Blue": ItemData(30, ItemClassification.progression),
    "D20 Dice Black": ItemData(31, ItemClassification.progression),
    "D20 Dice White": ItemData(32, ItemClassification.progression),
    "Card Sleeves (Fire)": ItemData(65, ItemClassification.progression),
    "Card Sleeves (Earth)": ItemData(66, ItemClassification.progression),
    "Card Sleeves (Water)": ItemData(67, ItemClassification.progression),
    "Card Sleeves (Wind)": ItemData(68, ItemClassification.progression),
    "Progressive Deck Box Red": ItemData(24, ItemClassification.progression,2),
    "Progressive Deck Box Green": ItemData(25, ItemClassification.progression,2),
    "Progressive Deck Box Blue": ItemData(26, ItemClassification.progression,2),
    "Progressive Deck Box Yellow": ItemData(27, ItemClassification.progression,2),
    "Collection Book": ItemData(28, ItemClassification.progression),
    "Premium Collection Book": ItemData(54, ItemClassification.progression),
    "Playmat (Drilceros)": ItemData(71, ItemClassification.progression),
    "Playmat (Clamigo)": ItemData(69, ItemClassification.progression),
    "Playmat (Wispo)": ItemData(75, ItemClassification.progression),
    "Playmat (Lunight)": ItemData(83, ItemClassification.progression),
    "Playmat (Kyrone)": ItemData(78, ItemClassification.progression),
    "Playmat (Duel)": ItemData(70, ItemClassification.progression),
    "Playmat (Dracunix1)": ItemData(74, ItemClassification.progression),
    "Playmat (The Four Dragons)": ItemData(73, ItemClassification.progression),
    "Playmat (Drakon)": ItemData(72, ItemClassification.progression),
    "Playmat (GigatronX Evo)": ItemData(76, ItemClassification.progression),
    "Playmat (Fire)": ItemData(79, ItemClassification.progression),
    "Playmat (Earth)": ItemData(80, ItemClassification.progression),
    "Playmat (Water)": ItemData(82, ItemClassification.progression),
    "Playmat (Wind)": ItemData(81, ItemClassification.progression),
    "Playmat (Tetramon)": ItemData(77, ItemClassification.progression),
    "Playmat (Dracunix2)": ItemData(109, ItemClassification.progression),
    "Playmat (GigatronX)": ItemData(110, ItemClassification.progression),
    "Playmat (Katengu Black)": ItemData(111, ItemClassification.progression),
    "Playmat (Katengu White)": ItemData(112, ItemClassification.progression),
    "Manga 1": ItemData(95, ItemClassification.progression),
    "Manga 2": ItemData(96, ItemClassification.progression),
    "Manga 3": ItemData(97, ItemClassification.progression),
    "Manga 4": ItemData(98, ItemClassification.progression),
    "Manga 5": ItemData(99, ItemClassification.progression),
    "Manga 6": ItemData(100, ItemClassification.progression),
    "Manga 7": ItemData(101, ItemClassification.progression),
    "Manga 8": ItemData(102, ItemClassification.progression),
    "Manga 9": ItemData(103, ItemClassification.progression),
    "Manga 10": ItemData(104, ItemClassification.progression),
    "Manga 11": ItemData(105, ItemClassification.progression),
    "Manga 12": ItemData(106, ItemClassification.progression),
    "Pigni Plushie": ItemData(33, ItemClassification.progression),
    "Nanomite Plushie": ItemData(34, ItemClassification.progression),
    "Minstar Plushie": ItemData(35, ItemClassification.progression),
    "Nocti Plushie": ItemData(36, ItemClassification.progression),
    "Burpig Figurine": ItemData(39, ItemClassification.progression),
    "Decimite Figurine": ItemData(42, ItemClassification.progression),
    "Trickstar Figurine": ItemData(45, ItemClassification.progression),
    "Lunight Figurine": ItemData(48, ItemClassification.progression),
    "Inferhog Figurine": ItemData(40, ItemClassification.progression),
    "Meganite Figurine": ItemData(43, ItemClassification.progression),
    "Princestar Figurine": ItemData(46, ItemClassification.progression),
    "Vampicant Figurine": ItemData(49, ItemClassification.progression),
    "Blazoar Plushie": ItemData(41, ItemClassification.progression),
    "Giganite Statue": ItemData(44, ItemClassification.progression),
    "Kingstar Plushie": ItemData(47, ItemClassification.progression),
    "Dracunix Figurine": ItemData(50, ItemClassification.progression),
    "Bonfiox Plushie": ItemData(52, ItemClassification.progression),
    "Drilceros Action Figure": ItemData(51, ItemClassification.progression),
    "ToonZ Plushie": ItemData(53, ItemClassification.progression),
    "Penny Sleeves": ItemData(118, ItemClassification.progression),
    "Tower Deckbox": ItemData(124, ItemClassification.progression),
    "Magnetic Holder": ItemData(113, ItemClassification.progression),
    "Toploader": ItemData(117, ItemClassification.progression),
    "Card Preserver": ItemData(114, ItemClassification.progression),
    "Playmat Gray": ItemData(119, ItemClassification.progression),
    "Playmat Green": ItemData(120, ItemClassification.progression),
    "Playmat Purple": ItemData(121, ItemClassification.progression),
    "Playmat Yellow": ItemData(122, ItemClassification.progression),
    "Pocket Pages": ItemData(115, ItemClassification.progression),
    "Card Holder": ItemData(116, ItemClassification.progression),
    "Collectors Album": ItemData(123, ItemClassification.progression),
    "System Gate #1": ItemData(87, ItemClassification.progression),
    "System Gate #2": ItemData(88, ItemClassification.progression),
    "Mafia Works": ItemData(86, ItemClassification.progression),
    "Necromonsters": ItemData(84, ItemClassification.progression),
    "Claim!": ItemData(85, ItemClassification.progression),
    "Progressive Basic Card Pack": ItemData(190, ItemClassification.progression,2), #game id 0
    "Progressive Basic Card Box": ItemData(1, ItemClassification.progression,2),
    "Progressive Rare Card Pack": ItemData(2, ItemClassification.progression,2),
    "Progressive Rare Card Box": ItemData(3, ItemClassification.progression,2),
    "Progressive Epic Card Pack": ItemData(4, ItemClassification.progression,2),
    "Progressive Epic Card Box": ItemData(5, ItemClassification.progression,2),
    "Progressive Legendary Card Pack": ItemData(6, ItemClassification.progression,2),
    "Progressive Legendary Card Box": ItemData(7, ItemClassification.progression,2),
    "Progressive Basic Destiny Pack": ItemData(8, ItemClassification.progression,2),
    "Progressive Basic Destiny Box": ItemData(9, ItemClassification.progression,2),
    "Progressive Rare Destiny Pack": ItemData(10, ItemClassification.progression,2),
    "Progressive Rare Destiny Box": ItemData(11, ItemClassification.progression,2),
    "Progressive Epic Destiny Pack": ItemData(12, ItemClassification.progression,2),
    "Progressive Epic Destiny Box": ItemData(13, ItemClassification.progression,2),
    "Progressive Legendary Destiny Pack": ItemData(14, ItemClassification.progression,2),
    "Progressive Legendary Destiny Box": ItemData(15, ItemClassification.progression,2),
    "Progressive Cleanser": ItemData(23, ItemClassification.progression,2),
}

not_sellable_dict: Dict[str, ItemData] = {
    "FormatStandard": ItemData(207, ItemClassification.useful),
    "FormatPauper": ItemData(208, ItemClassification.useful),
    "FormatFireCup": ItemData(209, ItemClassification.useful),
    "FormatEarthCup": ItemData(210, ItemClassification.useful),
    "FormatWaterCup": ItemData(211, ItemClassification.useful),
    "FormatWindCup": ItemData(212, ItemClassification.useful),
    "FormatFirstEditionVintage": ItemData(213, ItemClassification.useful),
    "FormatSilverBorder": ItemData(214, ItemClassification.useful),
    "FormatGoldBorder": ItemData(215, ItemClassification.useful),
    "FormatExBorder": ItemData(216, ItemClassification.useful),
    "FormatFullArtBorder": ItemData(217, ItemClassification.useful),
    "FormatFoil": ItemData(218, ItemClassification.useful),

    "Progressive Card Table": ItemData(200, ItemClassification.progression, 2),
    "Progressive Card Display": ItemData(201, ItemClassification.useful, 3),
    "Progressive Personal Shelf": ItemData(202, ItemClassification.useful, 3),
    "Progressive Auto Scent": ItemData(203, ItemClassification.progression, 3),
    "Progressive Warehouse Shelf": ItemData(204, ItemClassification.progression, 2),
    "Shop Expansion": ItemData(205, ItemClassification.progression, 30),
    "Warehouse Expansion": ItemData(206, ItemClassification.progression, 15),
    "Worker - Zachery": ItemData(219, ItemClassification.progression),
    "Worker - Terence": ItemData(220, ItemClassification.useful),
    "Worker - Dennis": ItemData(221, ItemClassification.useful),
    "Worker - Clark": ItemData(222, ItemClassification.useful),
    "Worker - Angus": ItemData(223, ItemClassification.useful),
    "Worker - Benji": ItemData(224, ItemClassification.useful),
    "Worker - Lauren": ItemData(225, ItemClassification.useful),
    "Worker - Axel": ItemData(226, ItemClassification.useful),
    "Progressive Shelf": ItemData(227, ItemClassification.progression, 6),
    "Progressive Wall Display Case": ItemData(228, ItemClassification.useful, 5),
    "Progressive Card Projector": ItemData(229, ItemClassification.progression, 3),
    "Progressive Pack Opener": ItemData(230, ItemClassification.useful, 3),
    "Worker - Alexander": ItemData(231, ItemClassification.useful),
    "Progressive Play Table": ItemData(232, ItemClassification.progression, 3),
    "Workbench": ItemData(233, ItemClassification.progression),
    "Trash Bin": ItemData(234, ItemClassification.useful),
    "Checkout Counter": ItemData(235, ItemClassification.progression),
}

# unused 0x1F2800D7
random_ghost_dict: Dict[str, ItemData] = {
    "1 Ghost Card": ItemData(326, ItemClassification.progression, 0),
    "2 Ghost Cards": ItemData(327, ItemClassification.progression, 0),
    "3 Ghost Cards": ItemData(328, ItemClassification.progression, 0),
    "4 Ghost Cards": ItemData(329, ItemClassification.progression, 0),
    "5 Ghost Cards": ItemData(330, ItemClassification.progression, 0),
}
ghost_dict: Dict[str, ItemData] = {
    "Ghost Blazoar (white)": ItemData(0x1F280062, ItemClassification.progression_skip_balancing),
    "Ghost Blazoar (Black)": ItemData(0x1F280063, ItemClassification.progression_skip_balancing),
    "Foil Ghost Blazoar (white)": ItemData(0x1F280064, ItemClassification.progression_skip_balancing),
    "Foil Ghost Blazoar (Black)": ItemData(0x1F280065, ItemClassification.progression_skip_balancing),
    "Ghost Kyuenbi (white)": ItemData(0x1F280066, ItemClassification.progression_skip_balancing),
    "Ghost Kyuenbi (Black)": ItemData(0x1F280067, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kyuenbi (white)": ItemData(0x1F280068, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kyuenbi (Black)": ItemData(0x1F280069, ItemClassification.progression_skip_balancing),
    "Ghost Giganite (white)": ItemData(0x1F28006A, ItemClassification.progression_skip_balancing),
    "Ghost Giganite (Black)": ItemData(0x1F28006B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Giganite (white)": ItemData(0x1F28006C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Giganite (Black)": ItemData(0x1F28006D, ItemClassification.progression_skip_balancing),
    "Ghost Mammotree (white)": ItemData(0x1F28006E, ItemClassification.progression_skip_balancing),
    "Ghost Mammotree (Black)": ItemData(0x1F28006F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Mammotree (white)": ItemData(0x1F280070, ItemClassification.progression_skip_balancing),
    "Foil Ghost Mammotree (Black)": ItemData(0x1F280071, ItemClassification.progression_skip_balancing),
    "Ghost Kingstar (white)": ItemData(0x1F280072, ItemClassification.progression_skip_balancing),
    "Ghost Kingstar (Black)": ItemData(0x1F280073, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kingstar (white)": ItemData(0x1F280074, ItemClassification.progression_skip_balancing),
    "Foil Ghost Kingstar (Black)": ItemData(0x1F280075, ItemClassification.progression_skip_balancing),
    "Ghost Fistronk (white)": ItemData(0x1F280076, ItemClassification.progression_skip_balancing),
    "Ghost Fistronk (Black)": ItemData(0x1F280077, ItemClassification.progression_skip_balancing),
    "Foil Ghost Fistronk (white)": ItemData(0x1F280078, ItemClassification.progression_skip_balancing),
    "Foil Ghost Fistronk (Black)": ItemData(0x1F280079, ItemClassification.progression_skip_balancing),
    "Ghost Royalama (white)": ItemData(0x1F28007A, ItemClassification.progression_skip_balancing),
    "Ghost Royalama (Black)": ItemData(0x1F28007B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Royalama (white)": ItemData(0x1F28007C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Royalama (Black)": ItemData(0x1F28007D, ItemClassification.progression_skip_balancing),
    "Ghost Dracunix (white)": ItemData(0x1F28007E, ItemClassification.progression_skip_balancing),
    "Ghost Dracunix (Black)": ItemData(0x1F28007F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Dracunix (white)": ItemData(0x1F280080, ItemClassification.progression_skip_balancing),
    "Foil Ghost Dracunix (Black)": ItemData(0x1F280081, ItemClassification.progression_skip_balancing),
    "Ghost Magnoria (white)": ItemData(0x1F280082, ItemClassification.progression_skip_balancing),
    "Ghost Magnoria (Black)": ItemData(0x1F280083, ItemClassification.progression_skip_balancing),
    "Foil Ghost Magnoria (white)": ItemData(0x1F280084, ItemClassification.progression_skip_balancing),
    "Foil Ghost Magnoria (Black)": ItemData(0x1F280085, ItemClassification.progression_skip_balancing),
    "Ghost Hydroid (white)": ItemData(0x1F280086, ItemClassification.progression_skip_balancing),
    "Ghost Hydroid (Black)": ItemData(0x1F280087, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydroid (white)": ItemData(0x1F280088, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydroid (Black)": ItemData(0x1F280089, ItemClassification.progression_skip_balancing),
    "Ghost Drakon (white)": ItemData(0x1F28008A, ItemClassification.progression_skip_balancing),
    "Ghost Drakon (Black)": ItemData(0x1F28008B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Drakon (white)": ItemData(0x1F28008C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Drakon (Black)": ItemData(0x1F28008D, ItemClassification.progression_skip_balancing),
    "Ghost Bogon (white)": ItemData(0x1F28008E, ItemClassification.progression_skip_balancing),
    "Ghost Bogon (Black)": ItemData(0x1F28008F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Bogon (white)": ItemData(0x1F280090, ItemClassification.progression_skip_balancing),
    "Foil Ghost Bogon (Black)": ItemData(0x1F280091, ItemClassification.progression_skip_balancing),
    "Ghost Hydron (white)": ItemData(0x1F280092, ItemClassification.progression_skip_balancing),
    "Ghost Hydron (Black)": ItemData(0x1F280093, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydron (white)": ItemData(0x1F280094, ItemClassification.progression_skip_balancing),
    "Foil Ghost Hydron (Black)": ItemData(0x1F280095, ItemClassification.progression_skip_balancing),
    "Ghost Raizon (white)": ItemData(0x1F280096, ItemClassification.progression_skip_balancing),
    "Ghost Raizon (Black)": ItemData(0x1F280097, ItemClassification.progression_skip_balancing),
    "Foil Ghost Raizon (white)": ItemData(0x1F280098, ItemClassification.progression_skip_balancing),
    "Foil Ghost Raizon (Black)": ItemData(0x1F280099, ItemClassification.progression_skip_balancing),
    "Ghost Lucadence (white)": ItemData(0x1F28009A, ItemClassification.progression_skip_balancing),
    "Ghost Lucadence (Black)": ItemData(0x1F28009B, ItemClassification.progression_skip_balancing),
    "Foil Ghost Lucadence (white)": ItemData(0x1F28009C, ItemClassification.progression_skip_balancing),
    "Foil Ghost Lucadence (Black)": ItemData(0x1F28009D, ItemClassification.progression_skip_balancing),
    "Ghost Jigajawr (white)": ItemData(0x1F28009E, ItemClassification.progression_skip_balancing),
    "Ghost Jigajawr (Black)": ItemData(0x1F28009F, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jigajawr (white)": ItemData(0x1F2800A0, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jigajawr (Black)": ItemData(0x1F2800A1, ItemClassification.progression_skip_balancing),
    "Ghost Jacktern (white)": ItemData(0x1F2800A2, ItemClassification.progression_skip_balancing),
    "Ghost Jacktern (Black)": ItemData(0x1F2800A3, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jacktern (white)": ItemData(0x1F2800A4, ItemClassification.progression_skip_balancing),
    "Foil Ghost Jacktern (Black)": ItemData(0x1F2800A5, ItemClassification.progression_skip_balancing),
    "Ghost GigatronX (white)": ItemData(0x1F2800A6, ItemClassification.progression_skip_balancing),
    "Ghost GigatronX (Black)": ItemData(0x1F2800A7, ItemClassification.progression_skip_balancing),
    "Foil Ghost GigatronX (white)": ItemData(0x1F2800A8, ItemClassification.progression_skip_balancing),
    "Foil Ghost GigatronX (Black)": ItemData(0x1F2800A9, ItemClassification.progression_skip_balancing),
    "Ghost Clawcifear (white)": ItemData(0x1F2800AA, ItemClassification.progression_skip_balancing),
    "Ghost Clawcifear (Black)": ItemData(0x1F2800AB, ItemClassification.progression_skip_balancing),
    "Foil Ghost Clawcifear (white)": ItemData(0x1F2800AC, ItemClassification.progression_skip_balancing),
    "Foil Ghost Clawcifear (Black)": ItemData(0x1F2800AD, ItemClassification.progression_skip_balancing),
    "Ghost Katengu (white)": ItemData(0x1F2800AE, ItemClassification.progression_skip_balancing),
    "Ghost Katengu (Black)": ItemData(0x1F2800AF, ItemClassification.progression_skip_balancing),
    "Foil Ghost Katengu (white)": ItemData(0x1F2800B0, ItemClassification.progression_skip_balancing),
    "Foil Ghost Katengu (Black)": ItemData(0x1F2800B1, ItemClassification.progression_skip_balancing),
}

junk_dict: Dict[str, ItemData] = {
    "Small Xp": ItemData(300, ItemClassification.filler),
    "Small Money": ItemData(301, ItemClassification.filler),
    "Medium Xp": ItemData(302, ItemClassification.filler),
    "Medium Money": ItemData(303, ItemClassification.filler),
    "Large Xp": ItemData(304, ItemClassification.filler),
    "Large Money": ItemData(305, ItemClassification.filler),
    "Random Card": ItemData(306, ItemClassification.filler),
    "Random New Card": ItemData(307, ItemClassification.filler),
    "Progressive Customer Money": ItemData(308, ItemClassification.filler),
    "Increase Card Luck": ItemData(309, ItemClassification.filler),
}

trap_dict: Dict[str, ItemData] = {
    "Stink Trap": ItemData(320, ItemClassification.trap),
    "Poltergeist Trap": ItemData(321, ItemClassification.trap),
    "Credit Card Failure Trap": ItemData(322, ItemClassification.trap),
    "Decrease Card Luck": ItemData(323, ItemClassification.trap),
    "Market Change Trap": ItemData(324, ItemClassification.trap),
    "Currency Trap": ItemData(325, ItemClassification.trap),
}

junk_weights = {
    "Small Xp": 25,
    "Small Money": 25,
    "Medium Money": 15,
    "Medium Xp": 15,
    "Large Money": 10,
    "Large Xp": 10,
    "Random Card": 50,
    "Random New Card": 50,
    "Progressive Customer Money": 50,
    "Increase Card Luck": 0
}

full_item_dict: Dict[str, ItemData] = {**item_dict, **not_sellable_dict, **random_ghost_dict, **ghost_dict, **junk_dict, **trap_dict}


