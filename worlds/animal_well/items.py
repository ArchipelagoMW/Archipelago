from itertools import groupby
from typing import Dict, List, Set, NamedTuple
from BaseClasses import ItemClassification, Item
from .names import ItemNames as iname
IClass = ItemClassification  # just to make the lines shorter


class AWItem(Item):
    game: str = "ANIMAL WELL"


class AWItemData(NamedTuple):
    classification: ItemClassification
    quantity_in_item_pool: int  # put 0 for things not in the pool by default
    offset: int
    item_group: str = ""


item_base_id = 11553377

item_table: Dict[str, AWItemData] = {
    # Major progression items
    iname.bubble.value: AWItemData(IClass.progression | IClass.useful, 2, 0, "Toys"),  # progressive
    # iname.disc.value: AWItemData(IClass.progression | IClass.useful, 1, 1, "Toys"),
    iname.yoyo.value: AWItemData(IClass.progression | IClass.useful, 1, 2, "Toys"),
    iname.slink.value: AWItemData(IClass.progression | IClass.useful, 1, 3, "Toys"),
    iname.flute.value: AWItemData(IClass.progression | IClass.useful, 1, 4, "Toys"),
    iname.top.value: AWItemData(IClass.progression | IClass.useful, 1, 5, "Toys"),
    iname.lantern.value: AWItemData(IClass.progression | IClass.useful, 1, 6, "Toys"),
    iname.uv.value: AWItemData(IClass.progression | IClass.useful, 1, 7, "Toys"),
    iname.ball.value: AWItemData(IClass.progression | IClass.useful, 1, 8, "Toys"),
    iname.remote.value: AWItemData(IClass.progression | IClass.useful, 1, 9, "Toys"),
    iname.wheel.value: AWItemData(IClass.progression | IClass.useful, 1, 10, "Toys"),
    iname.firecrackers.value: AWItemData(IClass.progression | IClass.useful, 0, 11, "Toys"),

    # Minor progression items and keys
    iname.m_disc.value: AWItemData(IClass.progression | IClass.useful, 1, 12, "Toys"),
    iname.fanny_pack.value: AWItemData(IClass.useful, 1, 13),

    iname.match.value: AWItemData(IClass.progression, 9, 14),
    iname.matchbox.value: AWItemData(IClass.progression | IClass.useful, 0, 15, "Toys"),

    iname.key.value: AWItemData(IClass.progression, 6, 16, "Keys"),
    iname.key_ring.value: AWItemData(IClass.progression | IClass.useful, 0, 17, "Keys"),
    iname.house_key.value: AWItemData(IClass.progression, 1, 18, "Keys"),
    iname.office_key.value: AWItemData(IClass.progression, 1, 19, "Keys"),

    iname.e_medal.value: AWItemData(IClass.progression, 1, 20, "Keys"),
    iname.s_medal.value: AWItemData(IClass.progression, 1, 21, "Keys"),
    iname.k_shard.value: AWItemData(IClass.progression, 3, 22, "Keys"),

    # iname.blue_flame.value: AWItemData(IClass.progression | IClass.useful, 1, 23, "Flames"),
    # iname.green_flame.value: AWItemData(IClass.progression | IClass.useful, 1, 24, "Flames"),
    # iname.violet_flame.value: AWItemData(IClass.progression | IClass.useful, 1, 25, "Flames"),
    # iname.pink_flame.value: AWItemData(IClass.progression | IClass.useful, 1, 26, "Flames"),

    # Eggs
    iname.egg_reference.value: AWItemData(IClass.progression_skip_balancing, 1, 27, "Eggs"),
    iname.egg_brown.value: AWItemData(IClass.progression_skip_balancing, 1, 28, "Eggs"),
    iname.egg_raw.value: AWItemData(IClass.progression_skip_balancing, 1, 29, "Eggs"),
    iname.egg_pickled.value: AWItemData(IClass.progression_skip_balancing, 1, 30, "Eggs"),
    iname.egg_big.value: AWItemData(IClass.progression_skip_balancing, 1, 31, "Eggs"),
    iname.egg_swan.value: AWItemData(IClass.progression_skip_balancing, 1, 32, "Eggs"),
    iname.egg_forbidden.value: AWItemData(IClass.progression_skip_balancing, 1, 33, "Eggs"),
    iname.egg_shadow.value: AWItemData(IClass.progression_skip_balancing, 1, 34, "Eggs"),
    iname.egg_vanity.value: AWItemData(IClass.progression_skip_balancing, 1, 35, "Eggs"),
    iname.egg_service.value: AWItemData(IClass.progression_skip_balancing, 1, 36, "Eggs"),

    iname.egg_depraved.value: AWItemData(IClass.progression_skip_balancing, 1, 37, "Eggs"),
    iname.egg_chaos.value: AWItemData(IClass.progression_skip_balancing, 1, 38, "Eggs"),
    iname.egg_upside_down.value: AWItemData(IClass.progression_skip_balancing, 1, 39, "Eggs"),
    iname.egg_evil.value: AWItemData(IClass.progression_skip_balancing, 1, 40, "Eggs"),
    iname.egg_sweet.value: AWItemData(IClass.progression_skip_balancing, 1, 41, "Eggs"),
    iname.egg_chocolate.value: AWItemData(IClass.progression_skip_balancing, 1, 42, "Eggs"),
    iname.egg_value.value: AWItemData(IClass.progression_skip_balancing, 1, 43, "Eggs"),
    iname.egg_plant.value: AWItemData(IClass.progression_skip_balancing, 1, 44, "Eggs"),
    iname.egg_red.value: AWItemData(IClass.progression_skip_balancing, 1, 45, "Eggs"),
    iname.egg_orange.value: AWItemData(IClass.progression_skip_balancing, 1, 46, "Eggs"),
    iname.egg_sour.value: AWItemData(IClass.progression_skip_balancing, 1, 47, "Eggs"),
    iname.egg_post_modern.value: AWItemData(IClass.progression_skip_balancing, 1, 48, "Eggs"),

    iname.egg_universal.value: AWItemData(IClass.progression_skip_balancing, 1, 49, "Eggs"),
    iname.egg_lf.value: AWItemData(IClass.progression_skip_balancing, 1, 50, "Eggs"),
    iname.egg_zen.value: AWItemData(IClass.progression_skip_balancing, 1, 51, "Eggs"),
    iname.egg_future.value: AWItemData(IClass.progression_skip_balancing, 1, 52, "Eggs"),
    iname.egg_friendship.value: AWItemData(IClass.progression_skip_balancing, 1, 53, "Eggs"),
    iname.egg_truth.value: AWItemData(IClass.progression_skip_balancing, 1, 54, "Eggs"),
    iname.egg_transcendental.value: AWItemData(IClass.progression_skip_balancing, 1, 55, "Eggs"),
    iname.egg_ancient.value: AWItemData(IClass.progression_skip_balancing, 1, 56, "Eggs"),
    iname.egg_magic.value: AWItemData(IClass.progression_skip_balancing, 1, 57, "Eggs"),
    iname.egg_mystic.value: AWItemData(IClass.progression_skip_balancing, 1, 58, "Eggs"),
    iname.egg_holiday.value: AWItemData(IClass.progression_skip_balancing, 1, 59, "Eggs"),
    iname.egg_rain.value: AWItemData(IClass.progression_skip_balancing, 1, 60, "Eggs"),
    iname.egg_razzle.value: AWItemData(IClass.progression_skip_balancing, 1, 61, "Eggs"),
    iname.egg_dazzle.value: AWItemData(IClass.progression_skip_balancing, 1, 62, "Eggs"),

    iname.egg_virtual.value: AWItemData(IClass.progression_skip_balancing, 1, 63, "Eggs"),
    iname.egg_normal.value: AWItemData(IClass.progression_skip_balancing, 1, 64, "Eggs"),
    iname.egg_great.value: AWItemData(IClass.progression_skip_balancing, 1, 65, "Eggs"),
    iname.egg_gorgeous.value: AWItemData(IClass.progression_skip_balancing, 1, 66, "Eggs"),
    iname.egg_planet.value: AWItemData(IClass.progression_skip_balancing, 1, 67, "Eggs"),
    iname.egg_moon.value: AWItemData(IClass.progression_skip_balancing, 1, 68, "Eggs"),
    iname.egg_galaxy.value: AWItemData(IClass.progression_skip_balancing, 1, 69, "Eggs"),
    iname.egg_sunset.value: AWItemData(IClass.progression_skip_balancing, 1, 70, "Eggs"),
    iname.egg_goodnight.value: AWItemData(IClass.progression_skip_balancing, 1, 71, "Eggs"),
    iname.egg_dream.value: AWItemData(IClass.progression_skip_balancing, 1, 72, "Eggs"),
    iname.egg_travel.value: AWItemData(IClass.progression_skip_balancing, 1, 73, "Eggs"),
    iname.egg_promise.value: AWItemData(IClass.progression_skip_balancing, 1, 74, "Eggs"),
    iname.egg_ice.value: AWItemData(IClass.progression_skip_balancing, 1, 75, "Eggs"),
    iname.egg_fire.value: AWItemData(IClass.progression_skip_balancing, 1, 76, "Eggs"),

    iname.egg_bubble.value: AWItemData(IClass.progression_skip_balancing, 1, 77, "Eggs"),
    iname.egg_desert.value: AWItemData(IClass.progression_skip_balancing, 1, 78, "Eggs"),
    iname.egg_clover.value: AWItemData(IClass.progression_skip_balancing, 1, 79, "Eggs"),
    iname.egg_brick.value: AWItemData(IClass.progression_skip_balancing, 1, 80, "Eggs"),
    iname.egg_neon.value: AWItemData(IClass.progression_skip_balancing, 1, 81, "Eggs"),
    iname.egg_iridescent.value: AWItemData(IClass.progression_skip_balancing, 1, 82, "Eggs"),
    iname.egg_rust.value: AWItemData(IClass.progression_skip_balancing, 1, 83, "Eggs"),
    iname.egg_scarlet.value: AWItemData(IClass.progression_skip_balancing, 1, 84, "Eggs"),
    iname.egg_sapphire.value: AWItemData(IClass.progression_skip_balancing, 1, 85, "Eggs"),
    iname.egg_ruby.value: AWItemData(IClass.progression_skip_balancing, 1, 86, "Eggs"),
    iname.egg_jade.value: AWItemData(IClass.progression_skip_balancing, 1, 87, "Eggs"),
    iname.egg_obsidian.value: AWItemData(IClass.progression_skip_balancing, 1, 88, "Eggs"),
    iname.egg_crystal.value: AWItemData(IClass.progression_skip_balancing, 1, 89, "Eggs"),
    iname.egg_golden.value: AWItemData(IClass.progression_skip_balancing, 1, 90, "Eggs"),

    iname.egg_65.value: AWItemData(IClass.progression_skip_balancing, 1, 91),  # not in item group for hinting reasons
    
    "Firecracker Refill": AWItemData(IClass.filler, 0, 92, "Filler"),
    "Big Blue Fruit": AWItemData(IClass.filler, 0, 93, "Filler"),
}

item_name_to_id: Dict[str, int] = {name: item_base_id + data.offset for name, data in item_table.items()}

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == IClass.filler]


def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

# # extra groups for the purpose of aliasing items
extra_groups: Dict[str, Set[str]] = {
    "Flute": {"Animal Flute"},
    "Wand": {"B. Wand"},
    "Bubble Wand": {"B. Wand"},
    "Ball": {"B. Ball"},
}

item_name_groups.update(extra_groups)
