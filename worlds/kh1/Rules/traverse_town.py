from math import ceil

from rule_builder.rules import Has, HasAll, HasAllCounts, Or, Rule

from worlds.generic.Rules import add_item_rule
from ..Items import item_name_groups
from ._helpers import COMBO_MASTER, DODGE_ROLL_AND_AIR_GUARD, DUMBO_SUMMON, GLIDE
from ._helpers import HIGH_JUMP, HIGH_JUMP_2, HIGH_JUMP_3
from ._helpers import PARASITE_CAGE, by_difficulty, has_all_magic_lvx_rule
from ._helpers import has_item_workshop_rule, has_x_worlds_rule_pinned_to_beginner


def build_rules(kh1world) -> dict[str, Rule]:
    player = kh1world.player
    puppy_value = kh1world.options.puppy_value.value
    item_workshop = has_item_workshop_rule()
    secret_waterway_rule = Has("Red Trinity")
    synth_items_rule = HasAllCounts({"Orichalcum": 17, "Mythril": 16}) & item_workshop

    inner_normal = (
        DUMBO_SUMMON
        | HIGH_JUMP_3
        | (COMBO_MASTER & (DODGE_ROLL_AND_AIR_GUARD | HIGH_JUMP_2 | (HIGH_JUMP & Has("Air Combo Plus", count=2))))
    )
    inner_proud = (
        Has("Mermaid Kick")
        | DODGE_ROLL_AND_AIR_GUARD
        | (COMBO_MASTER & (HIGH_JUMP | Has("Air Combo Plus", count=2)))
    )
    summon_gems_rule = HasAll("Progressive Fire", *sorted(item_name_groups["Summon Gems"]))
    mystical_house_yellow_trinity_rule = Has("Progressive Fire") & by_difficulty(
        beginner=Has("Yellow Trinity") | DUMBO_SUMMON,
        normal=HIGH_JUMP_2,
        proud=HIGH_JUMP,
    )
    blue_trinity_balcony_rule = by_difficulty(
        beginner=Has("Blue Trinity") & GLIDE,
        proud=GLIDE,
        minimal=DUMBO_SUMMON,
    )
    mystical_house_glide_rule = Has("Progressive Fire") & by_difficulty(
        beginner=GLIDE,
        proud=inner_normal,
        minimal=inner_proud,
    )
    all_arts_rule = (
        has_all_magic_lvx_rule(1)
        & HasAll(*sorted(item_name_groups["Arts"]))
        & has_x_worlds_rule_pinned_to_beginner(8)
    )
    synth_15_items_rule = Or(
        HasAllCounts({"Orichalcum": 6, "Mythril": 9}),
        HasAllCounts({"Orichalcum": 7, "Mythril": 8}),
        HasAllCounts({"Orichalcum": 8, "Mythril": 7}),
        HasAllCounts({"Orichalcum": 9, "Mythril": 6}),
    ) & item_workshop

    for i in range(33):
        add_item_rule(
            kh1world.get_location(f"Traverse Town Synth Item {i + 1:02}"),
            lambda item, _player=player: (item.player != _player or item.name not in ("Orichalcum", "Mythril")),
        )

    return {
        "Traverse Town 1st District Candle Puzzle Chest": Has("Progressive Blizzard"),
        "Traverse Town 1st District Accessory Shop Roof Chest": HIGH_JUMP,
        "Traverse Town Secret Waterway White Trinity Chest": secret_waterway_rule & Has("White Trinity"),
        "Traverse Town Secret Waterway Near Stairs Chest": secret_waterway_rule,
        "Traverse Town Leon Secret Waterway Earthshine Event": secret_waterway_rule,
        "Traverse Town Geppetto's House Chest": PARASITE_CAGE,
        "Traverse Town Item Workshop Right Chest": item_workshop,
        "Traverse Town Item Workshop Left Chest": item_workshop,
        "Traverse Town Alleyway Behind Crates Chest": Has("Red Trinity"),
        "Traverse Town Defeat Opposite Armor Aero Event": Has("Red Trinity"),
        "Traverse Town Defeat Opposite Armor Navi-G Piece Event": Has("Red Trinity"),
        "Traverse Town Magician's Study Obtained All LV1 Magic": has_all_magic_lvx_rule(1),
        "Traverse Town Magician's Study Obtained All LV3 Magic": has_all_magic_lvx_rule(3),
        "Traverse Town Gizmo Shop Postcard 1": Has("Progressive Thunder"),
        "Traverse Town Gizmo Shop Postcard 2": Has("Progressive Thunder"),
        "Traverse Town Item Workshop Postcard": item_workshop,
        "Traverse Town Geppetto's House Postcard": PARASITE_CAGE,
        "Traverse Town 1st District Blue Trinity by Exit Door": Has("Blue Trinity"),
        "Traverse Town 3rd District Blue Trinity": Has("Blue Trinity"),
        "Traverse Town Magician's Study Blue Trinity": HasAll("Blue Trinity", "Progressive Fire"),
        "Traverse Town Magician's Study Earthshine Event": HasAll("Progressive Fire", "Earthshine"),
        "Traverse Town Magician's Study Naturespark Event": HasAll("Progressive Fire", "Naturespark"),
        "Traverse Town Magician's Study Watergleam Event": HasAll("Progressive Fire", "Watergleam"),
        "Traverse Town Magician's Study Fireglow Event": HasAll("Progressive Fire", "Fireglow"),
        "Traverse Town Magician's Study Lord Fortune Event": summon_gems_rule,
        "Traverse Town Mystical House Yellow Trinity Chest": mystical_house_yellow_trinity_rule,
        "Traverse Town 1st District Blue Trinity Balcony Chest": blue_trinity_balcony_rule,
        "Traverse Town Mystical House Glide Chest": mystical_house_glide_rule,
        "Traverse Town Kairi Secret Waterway Oathkeeper Event": secret_waterway_rule,
        "Traverse Town Secret Waterway Navi Gummi Event": secret_waterway_rule,
        "Traverse Town Geppetto's House Geppetto Reward Hyperion Blueprint": PARASITE_CAGE & summon_gems_rule,
        "Traverse Town Geppetto's House Pinocchio Reward Chocobo Blueprint": PARASITE_CAGE,
        "Traverse Town Magician's Study Obtained All Arts Items": all_arts_rule,
        "Traverse Town Synth 15 Items": synth_15_items_rule,
        "Traverse Town Geppetto's House Geppetto Reward Cid Blueprint": PARASITE_CAGE,
        "Traverse Town Geppetto's House Geppetto Reward Geppetto Blueprint": PARASITE_CAGE,
        "Traverse Town Geppetto's House Geppetto Reward Aerith Blueprint": PARASITE_CAGE,
        "Traverse Town Geppetto's House Geppetto Reward Yuffie Blueprint": PARASITE_CAGE,
        "Traverse Town Geppetto's House Geppetto Reward Leon Blueprint": PARASITE_CAGE,
        "Traverse Town Geppetto's House Geppetto Reward Cactaur Blueprint": PARASITE_CAGE,
        "Traverse Town Piano Room Return 10 Puppies": Has("Puppy", count=ceil(10 / puppy_value)),
        "Traverse Town Piano Room Return 20 Puppies": Has("Puppy", count=ceil(20 / puppy_value)),
        "Traverse Town Piano Room Return 30 Puppies": Has("Puppy", count=ceil(30 / puppy_value)),
        "Traverse Town Piano Room Return 40 Puppies": Has("Puppy", count=ceil(40 / puppy_value)),
        "Traverse Town Piano Room Return 50 Puppies Reward 1": Has("Puppy", count=ceil(50 / puppy_value)),
        "Traverse Town Piano Room Return 50 Puppies Reward 2": Has("Puppy", count=ceil(50 / puppy_value)),
        "Traverse Town Piano Room Return 60 Puppies": Has("Puppy", count=ceil(60 / puppy_value)),
        "Traverse Town Piano Room Return 70 Puppies": Has("Puppy", count=ceil(70 / puppy_value)),
        "Traverse Town Piano Room Return 80 Puppies": Has("Puppy", count=ceil(80 / puppy_value)),
        "Traverse Town Piano Room Return 90 Puppies": Has("Puppy", count=ceil(90 / puppy_value)),
        "Traverse Town Piano Room Return 99 Puppies Reward 1": Has("Puppy", count=ceil(99 / puppy_value)),
        "Traverse Town Piano Room Return 99 Puppies Reward 2": Has("Puppy", count=ceil(99 / puppy_value)),
        "Traverse Town Mail Postcard 01 Event": Has("Postcard", count=1),
        "Traverse Town Mail Postcard 02 Event": Has("Postcard", count=2),
        "Traverse Town Mail Postcard 03 Event": Has("Postcard", count=3),
        "Traverse Town Mail Postcard 04 Event": Has("Postcard", count=4),
        "Traverse Town Mail Postcard 05 Event": Has("Postcard", count=5),
        "Traverse Town Mail Postcard 06 Event": Has("Postcard", count=6),
        "Traverse Town Mail Postcard 07 Event": Has("Postcard", count=7),
        "Traverse Town Mail Postcard 08 Event": Has("Postcard", count=8),
        "Traverse Town Mail Postcard 09 Event": Has("Postcard", count=9),
        "Traverse Town Mail Postcard 10 Event": Has("Postcard", count=10),
        "Traverse Town Synth Item 01": synth_items_rule,
        "Traverse Town Synth Item 02": synth_items_rule,
        "Traverse Town Synth Item 03": synth_items_rule,
        "Traverse Town Synth Item 04": synth_items_rule,
        "Traverse Town Synth Item 05": synth_items_rule,
        "Traverse Town Synth Item 06": synth_items_rule,
        "Traverse Town Synth Item 07": synth_items_rule,
        "Traverse Town Synth Item 08": synth_items_rule,
        "Traverse Town Synth Item 09": synth_items_rule,
        "Traverse Town Synth Item 10": synth_items_rule,
        "Traverse Town Synth Item 11": synth_items_rule,
        "Traverse Town Synth Item 12": synth_items_rule,
        "Traverse Town Synth Item 13": synth_items_rule,
        "Traverse Town Synth Item 14": synth_items_rule,
        "Traverse Town Synth Item 15": synth_items_rule,
        "Traverse Town Synth Item 16": synth_items_rule,
        "Traverse Town Synth Item 17": synth_items_rule,
        "Traverse Town Synth Item 18": synth_items_rule,
        "Traverse Town Synth Item 19": synth_items_rule,
        "Traverse Town Synth Item 20": synth_items_rule,
        "Traverse Town Synth Item 21": synth_items_rule,
        "Traverse Town Synth Item 22": synth_items_rule,
        "Traverse Town Synth Item 23": synth_items_rule,
        "Traverse Town Synth Item 24": synth_items_rule,
        "Traverse Town Synth Item 25": synth_items_rule,
        "Traverse Town Synth Item 26": synth_items_rule,
        "Traverse Town Synth Item 27": synth_items_rule,
        "Traverse Town Synth Item 28": synth_items_rule,
        "Traverse Town Synth Item 29": synth_items_rule,
        "Traverse Town Synth Item 30": synth_items_rule,
        "Traverse Town Synth Item 31": synth_items_rule,
        "Traverse Town Synth Item 32": synth_items_rule,
        "Traverse Town Synth Item 33": synth_items_rule,
    }
