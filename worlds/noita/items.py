import itertools
from collections import Counter
from typing import Dict, List, NamedTuple, Set, TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .options import BossesAsChecks, VictoryCondition, ExtraOrbs

if TYPE_CHECKING:
    from . import NoitaWorld
else:
    NoitaWorld = object


class ItemData(NamedTuple):
    code: int
    group: str
    classification: ItemClassification = ItemClassification.progression
    required_num: int = 0


class NoitaItem(Item):
    game: str = "Noita"


def create_item(player: int, name: str) -> Item:
    item_data = item_table[name]
    return NoitaItem(name, item_data.classification, item_data.code, player)


def create_fixed_item_pool() -> List[str]:
    required_items: Dict[str, int] = {name: data.required_num for name, data in item_table.items()}
    return list(Counter(required_items).elements())


def create_orb_items(victory_condition: VictoryCondition, extra_orbs: ExtraOrbs) -> List[str]:
    orb_count = extra_orbs.value
    if victory_condition == VictoryCondition.option_pure_ending:
        orb_count = orb_count + 11
    elif victory_condition == VictoryCondition.option_peaceful_ending:
        orb_count = orb_count + 33
    return ["Orb" for _ in range(orb_count)]


def create_spatial_awareness_item(bosses_as_checks: BossesAsChecks) -> List[str]:
    return ["Spatial Awareness Perk"] if bosses_as_checks.value >= BossesAsChecks.option_all_bosses else []


def create_kantele(victory_condition: VictoryCondition) -> List[str]:
    return ["Kantele"] if victory_condition.value >= VictoryCondition.option_pure_ending else []


def create_random_items(world: NoitaWorld, weights: Dict[str, int], count: int) -> List[str]:
    filler_pool = weights.copy()
    if not world.options.bad_effects:
        filler_pool["Trap"] = 0
        filler_pool["Greed Die"] = 0

    return world.random.choices(population=list(filler_pool.keys()),
                                weights=list(filler_pool.values()),
                                k=count)


def create_all_items(world: NoitaWorld) -> None:
    player = world.player
    locations_to_fill = len(world.multiworld.get_unfilled_locations(player))

    itempool = (
        create_fixed_item_pool()
        + create_orb_items(world.options.victory_condition, world.options.extra_orbs)
        + create_spatial_awareness_item(world.options.bosses_as_checks)
        + create_kantele(world.options.victory_condition)
    )

    # if there's not enough shop-allowed items in the pool, we can encounter gen issues
    # 39 is the number of shop-valid items we need to guarantee
    if len(itempool) < 39:
        itempool += create_random_items(world, shop_only_filler_weights, 39 - len(itempool))
        # this is so that it passes tests and gens if you have minimal locations and only one player
        if world.multiworld.players == 1:
            for location in world.multiworld.get_unfilled_locations(player):
                if "Shop Item" in location.name:
                    location.item = create_item(player, itempool.pop())
            locations_to_fill = len(world.multiworld.get_unfilled_locations(player))

    itempool += create_random_items(world, filler_weights, locations_to_fill - len(itempool))
    world.multiworld.itempool += [create_item(player, name) for name in itempool]


# 110000 - 110032
item_table: Dict[str, ItemData] = {
    "Trap":                                 ItemData(110000, "Traps", ItemClassification.trap),
    "Extra Max HP":                         ItemData(110001, "Pickups", ItemClassification.useful),
    "Spell Refresher":                      ItemData(110002, "Pickups", ItemClassification.filler),
    "Potion":                               ItemData(110003, "Items", ItemClassification.filler),
    "Gold (200)":                           ItemData(110004, "Gold", ItemClassification.filler),
    "Gold (1000)":                          ItemData(110005, "Gold", ItemClassification.filler),
    "Wand (Tier 1)":                        ItemData(110006, "Wands", ItemClassification.useful),
    "Wand (Tier 2)":                        ItemData(110007, "Wands", ItemClassification.useful),
    "Wand (Tier 3)":                        ItemData(110008, "Wands", ItemClassification.useful),
    "Wand (Tier 4)":                        ItemData(110009, "Wands", ItemClassification.useful),
    "Wand (Tier 5)":                        ItemData(110010, "Wands", ItemClassification.useful, 1),
    "Wand (Tier 6)":                        ItemData(110011, "Wands", ItemClassification.useful, 1),
    "Kantele":                              ItemData(110012, "Wands", ItemClassification.useful),
    "Fire Immunity Perk":                   ItemData(110013, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Toxic Immunity Perk":                  ItemData(110014, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Explosion Immunity Perk":              ItemData(110015, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Melee Immunity Perk":                  ItemData(110016, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Electricity Immunity Perk":            ItemData(110017, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Tinker with Wands Everywhere Perk":    ItemData(110018, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "All-Seeing Eye Perk":                  ItemData(110019, "Perks", ItemClassification.progression | ItemClassification.useful, 1),
    "Spatial Awareness Perk":               ItemData(110020, "Perks", ItemClassification.progression),
    "Extra Life Perk":                      ItemData(110021, "Repeatable Perks", ItemClassification.useful, 1),
    "Orb":                                  ItemData(110022, "Orbs", ItemClassification.progression_skip_balancing),
    "Random Potion":                        ItemData(110023, "Items", ItemClassification.filler),
    "Secret Potion":                        ItemData(110024, "Items", ItemClassification.filler),
    "Powder Pouch":                         ItemData(110025, "Items", ItemClassification.filler),
    "Chaos Die":                            ItemData(110026, "Items", ItemClassification.filler),
    "Greed Die":                            ItemData(110027, "Items", ItemClassification.trap),
    "Kammi":                                ItemData(110028, "Items", ItemClassification.filler, 1),
    "Refreshing Gourd":                     ItemData(110029, "Items", ItemClassification.filler, 1),
    "Sädekivi":                             ItemData(110030, "Items", ItemClassification.filler),
    "Broken Wand":                          ItemData(110031, "Items", ItemClassification.filler),
}

shop_only_filler_weights: Dict[str, int] = {
    "Trap":             15,
    "Extra Max HP":     25,
    "Spell Refresher":  20,
    "Wand (Tier 1)":    10,
    "Wand (Tier 2)":    8,
    "Wand (Tier 3)":    7,
    "Wand (Tier 4)":    6,
    "Wand (Tier 5)":    5,
    "Wand (Tier 6)":    4,
    "Extra Life Perk":  10,
}

filler_weights: Dict[str, int] = {
    **shop_only_filler_weights,
    "Gold (200)":       15,
    "Gold (1000)":      6,
    "Potion":           40,
    "Random Potion":    9,
    "Secret Potion":    10,
    "Powder Pouch":     10,
    "Chaos Die":        4,
    "Greed Die":        4,
    "Kammi":            4,
    "Refreshing Gourd": 4,
    "Sädekivi":         3,
    "Broken Wand":      10,
}


# These helper functions make the comprehensions below more readable
def get_item_group(item_name: str) -> str:
    return item_table[item_name].group


def item_is_filler(item_name: str) -> bool:
    return item_table[item_name].classification == ItemClassification.filler


def item_is_perk(item_name: str) -> bool:
    return item_table[item_name].group == "Perks"


filler_items: List[str] = list(filter(item_is_filler, item_table.keys()))
item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}

item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in itertools.groupby(item_table, get_item_group)
}
