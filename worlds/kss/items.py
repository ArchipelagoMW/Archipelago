from typing import NamedTuple, Dict, Optional, Set
from BaseClasses import ItemClassification, Item
from .names import item_names

BASE_ID = 0x470000


class KSSItem(Item):
    game = "Kirby Super Star"


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    value: int = 0
    num: int = 1


sub_games: Dict[str, ItemData] = {
    item_names.spring_breeze: ItemData(BASE_ID + 0, ItemClassification.progression),
    item_names.dyna_blade: ItemData(BASE_ID + 1, ItemClassification.progression),
    item_names.gourmet_race: ItemData(BASE_ID + 2, ItemClassification.progression),
    item_names.great_cave_offensive: ItemData(BASE_ID + 3, ItemClassification.progression),
    item_names.revenge_of_meta_knight: ItemData(BASE_ID + 4, ItemClassification.progression),
    item_names.milky_way_wishes: ItemData(BASE_ID + 5, ItemClassification.progression),
    item_names.the_arena: ItemData(BASE_ID + 6, ItemClassification.progression),
}

sub_game_completion: Dict[str, ItemData] = {
    item_names.spring_breeze_complete: ItemData(None, ItemClassification.progression),
    item_names.dyna_blade_complete: ItemData(None, ItemClassification.progression),
    item_names.gourmet_race_complete: ItemData(None, ItemClassification.progression),
    item_names.great_cave_offensive_complete: ItemData(None, ItemClassification.progression),
    item_names.revenge_of_meta_knight_complete: ItemData(None, ItemClassification.progression),
    item_names.milky_way_wishes_complete: ItemData(None, ItemClassification.progression),
    item_names.the_arena_complete: ItemData(None, ItemClassification.progression),
}

copy_abilities: Dict[str, ItemData] = {
    item_names.cutter: ItemData(BASE_ID + 0x101, ItemClassification.progression),
    item_names.beam: ItemData(BASE_ID + 0x102, ItemClassification.progression),
    item_names.yoyo: ItemData(BASE_ID + 0x103, ItemClassification.progression),
    item_names.ninja: ItemData(BASE_ID + 0x104, ItemClassification.progression),
    item_names.wing: ItemData(BASE_ID + 0x105, ItemClassification.progression),
    item_names.fighter: ItemData(BASE_ID + 0x106, ItemClassification.progression),
    item_names.jet: ItemData(BASE_ID + 0x107, ItemClassification.progression),
    item_names.sword: ItemData(BASE_ID + 0x108, ItemClassification.progression),
    item_names.fire: ItemData(BASE_ID + 0x109, ItemClassification.progression),
    item_names.stone: ItemData(BASE_ID + 0x10A, ItemClassification.progression),
    item_names.bomb: ItemData(BASE_ID + 0x10B, ItemClassification.progression),
    item_names.plasma: ItemData(BASE_ID + 0x10C, ItemClassification.progression),
    item_names.wheel: ItemData(BASE_ID + 0x10D, ItemClassification.progression),
    item_names.ice: ItemData(BASE_ID + 0x10E, ItemClassification.progression),
    item_names.mirror: ItemData(BASE_ID + 0x10F, ItemClassification.progression),
    item_names.copy: ItemData(BASE_ID + 0x110, ItemClassification.progression),
    item_names.suplex: ItemData(BASE_ID + 0x111, ItemClassification.progression),
    item_names.hammer: ItemData(BASE_ID + 0x112, ItemClassification.progression),
    item_names.parasol: ItemData(BASE_ID + 0x113, ItemClassification.progression),
    item_names.mike: ItemData(BASE_ID + 0x114, ItemClassification.progression),
    item_names.sleep: ItemData(BASE_ID + 0x115, ItemClassification.trap),
    item_names.paint: ItemData(BASE_ID + 0x116, ItemClassification.useful),
    item_names.cook: ItemData(BASE_ID + 0x117, ItemClassification.useful),
    item_names.crash: ItemData(BASE_ID + 0x118, ItemClassification.progression),
}

treasures: Dict[str, ItemData] = {
    item_names.gold_medal: ItemData(BASE_ID + 0x201, ItemClassification.progression, 10000),
    item_names.gold_coin: ItemData(BASE_ID + 0x202, ItemClassification.progression, 1000),
    item_names.whip: ItemData(BASE_ID + 0x203, ItemClassification.progression, 6800),
    item_names.crystal_ball: ItemData(BASE_ID + 0x204, ItemClassification.progression, 200000),
    item_names.lucky_cat: ItemData(BASE_ID + 0x205, ItemClassification.progression, 500),
    item_names.seiryu_sword: ItemData(BASE_ID + 0x206, ItemClassification.progression, 142000),
    item_names.screw_ball: ItemData(BASE_ID + 0x207, ItemClassification.progression, 80000),
    item_names.echigo_candy: ItemData(BASE_ID + 0x208, ItemClassification.progression, 8000),
    item_names.zebra_mask: ItemData(BASE_ID + 0x209, ItemClassification.progression, 278000),
    item_names.star_stone: ItemData(BASE_ID + 0x20A, ItemClassification.progression, 82100),
    item_names.beast_fang: ItemData(BASE_ID + 0x20B, ItemClassification.progression, 7300),
    item_names.bandanna: ItemData(BASE_ID + 0x20C, ItemClassification.progression, 1990),
    item_names.springtime: ItemData(BASE_ID + 0x20D, ItemClassification.progression, 250000),
    item_names.dime: ItemData(BASE_ID + 0x20E, ItemClassification.progression, 10),
    item_names.glass_slippers: ItemData(BASE_ID + 0x20F, ItemClassification.progression, 120000),
    item_names.goblet: ItemData(BASE_ID + 0x210, ItemClassification.progression, 800),
    item_names.saucepan: ItemData(BASE_ID + 0x211, ItemClassification.progression, 10),
    item_names.brass_knuckle: ItemData(BASE_ID + 0x212, ItemClassification.progression, 20000),
    item_names.amber_rose: ItemData(BASE_ID + 0x213, ItemClassification.progression, 22100),
    item_names.fish_fossil: ItemData(BASE_ID + 0x214, ItemClassification.progression, 8250),
    item_names.beast_fossil: ItemData(BASE_ID + 0x215, ItemClassification.progression, 24220),
    item_names.nunchuks: ItemData(BASE_ID + 0x216, ItemClassification.progression, 55480),
    item_names.bucket: ItemData(BASE_ID + 0x217, ItemClassification.progression, 200),
    item_names.summertime: ItemData(BASE_ID + 0x218, ItemClassification.progression, 250000),
    item_names.hundred_dollar_coin: ItemData(BASE_ID + 0x219, ItemClassification.progression, 10000),
    item_names.ancient_gem: ItemData(BASE_ID + 0x21A, ItemClassification.progression, 68000),
    item_names.falcon_helmet: ItemData(BASE_ID + 0x21B, ItemClassification.progression, 41000),
    item_names.dud: ItemData(BASE_ID + 0x21C, ItemClassification.progression, 30),
    item_names.truth_mirror: ItemData(BASE_ID + 0x21D, ItemClassification.progression, 500000),
    item_names.star_tiara: ItemData(BASE_ID + 0x21E, ItemClassification.progression, 408200),
    item_names.turtle_shell: ItemData(BASE_ID + 0x21F, ItemClassification.progression, 800),
    item_names.falchion: ItemData(BASE_ID + 0x220, ItemClassification.progression, 325000),
    item_names.warrior_shield: ItemData(BASE_ID + 0x221, ItemClassification.progression, 50000),
    item_names.unicorn_horn: ItemData(BASE_ID + 0x222, ItemClassification.progression, 80300),
    item_names.autumntime: ItemData(BASE_ID + 0x223, ItemClassification.progression, 250000),
    item_names.rice_bowl: ItemData(BASE_ID + 0x224, ItemClassification.progression, 50),
    item_names.tut_mask: ItemData(BASE_ID + 0x225, ItemClassification.progression, 160000),
    item_names.mr_saturn: ItemData(BASE_ID + 0x226, ItemClassification.progression, 120000),
    item_names.armor: ItemData(BASE_ID + 0x227, ItemClassification.progression, 212000),
    item_names.treasure_box: ItemData(BASE_ID + 0x228, ItemClassification.progression, 100000),
    item_names.mannequin: ItemData(BASE_ID + 0x229, ItemClassification.progression, 3000),
    item_names.gold_crown: ItemData(BASE_ID + 0x22A, ItemClassification.progression, 528000),
    item_names.king_cape: ItemData(BASE_ID + 0x22B, ItemClassification.progression, 508000),
    item_names.model_ship: ItemData(BASE_ID + 0x22C, ItemClassification.progression, 800000),
    item_names.sun_ring: ItemData(BASE_ID + 0x22D, ItemClassification.progression, 800000),
    item_names.wintertime: ItemData(BASE_ID + 0x22E, ItemClassification.progression, 250000),
    item_names.katana: ItemData(BASE_ID + 0x22F, ItemClassification.progression, 990000),
    item_names.charm: ItemData(BASE_ID + 0x230, ItemClassification.progression, 8000),
    item_names.xmas_tree: ItemData(BASE_ID + 0x231, ItemClassification.progression, 40000),
    item_names.kong_barrel: ItemData(BASE_ID + 0x232, ItemClassification.progression, 1500),
    item_names.lamia_scale: ItemData(BASE_ID + 0x233, ItemClassification.progression, 12800),
    item_names.shiny_bamboo: ItemData(BASE_ID + 0x234, ItemClassification.progression, 600000),
    item_names.tire: ItemData(BASE_ID + 0x235, ItemClassification.progression, 1100),
    item_names.spirit_charm: ItemData(BASE_ID + 0x236, ItemClassification.progression, 78500),
    item_names.pegasus_wing: ItemData(BASE_ID + 0x237, ItemClassification.progression, 42800),
    item_names.raccoon_doll: ItemData(BASE_ID + 0x238, ItemClassification.progression, 8150),
    item_names.shell_whistle: ItemData(BASE_ID + 0x239, ItemClassification.progression, 82000),
    item_names.orichalcum: ItemData(BASE_ID + 0x23A, ItemClassification.progression, 512000),
    item_names.platinum_ring: ItemData(BASE_ID + 0x23B, ItemClassification.progression, 40000),
    item_names.triforce: ItemData(BASE_ID + 0x23C, ItemClassification.progression, 800000),
}

planets: Dict[str, ItemData] = {
    item_names.floria: ItemData(BASE_ID + 0x400, ItemClassification.progression),
    item_names.hotbeat: ItemData(BASE_ID + 0x401, ItemClassification.progression),
    item_names.skyhigh: ItemData(BASE_ID + 0x402, ItemClassification.progression),
    item_names.cavios: ItemData(BASE_ID + 0x403, ItemClassification.progression),
    item_names.aqualiss: ItemData(BASE_ID + 0x404, ItemClassification.progression),
    item_names.mecheye: ItemData(BASE_ID + 0x405, ItemClassification.progression),
    item_names.halfmoon: ItemData(BASE_ID + 0x406, ItemClassification.progression),
    item_names.copy_planet: ItemData(BASE_ID + 0x407, ItemClassification.progression),
}

dyna_items: Dict[str, ItemData] = {
    item_names.dyna_blade_ex1: ItemData(BASE_ID + 0x800, ItemClassification.progression),
    item_names.dyna_blade_ex2: ItemData(BASE_ID + 0x801, ItemClassification.progression),
    item_names.progressive_dyna_blade: ItemData(BASE_ID + 0x802, ItemClassification.progression, num=4)
}

misc_items: Dict[str, ItemData] = {
    item_names.one_up: ItemData(BASE_ID + 0x1001, ItemClassification.filler),
    item_names.maxim_tomato: ItemData(BASE_ID + 0x1002, ItemClassification.filler),
    item_names.invincible_candy: ItemData(BASE_ID + 0x1003, ItemClassification.filler),
    item_names.rainbow_star: ItemData(BASE_ID + 0x1004, ItemClassification.progression)
}

filler_item_weights: Dict[str, int] = {
    item_names.one_up: 4,
    item_names.maxim_tomato: 2,
    item_names.invincible_candy: 2
}

item_table: Dict[str, ItemData] = {
    **sub_games,
    **sub_game_completion,
    **copy_abilities,
    **treasures,
    **planets,
    **dyna_items,
    **misc_items
}

item_groups: Dict[str, Set[str]] = {
    "Copy Ability": {name for name in copy_abilities},
    "Treasures": {name for name in treasures},
    "Planets": {name for name in planets}
}

lookup_item_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
