from rule_builder.field_resolvers import FromOption
from rule_builder.rules import AtLeast, Has, HasAll, HasAllCounts, HasAny
from rule_builder.rules import HasAnyCount, HasGroup, Or, Rule, True_

from ..Items import item_name_groups
from ..Options import RequiredLuckyEmblemsDoor, RequiredLuckyEmblemsEotW
from ..Data import CHEST_KEYBLADES, WORLD_KEY_ITEMS
from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD, EOTW_UNLOCK_LUCKY_EMBLEMS
from ._option_filters import EVIDENCE_BUNDLE_OFF, EVIDENCE_BUNDLE_ON, FINAL_REST_DOOR_LUCKY_EMBLEMS
from ._option_filters import FINAL_REST_DOOR_NOT_LUCKY_EMBLEMS, HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON
from ._option_filters import KEYBLADES_UNLOCK_CHESTS_OFF, SLIDES_BUNDLE_OFF
from ._option_filters import SLIDES_BUNDLE_ON, STACKING_WORLD_ITEMS_ON


def by_difficulty(beginner: Rule | bool | None = None, normal: Rule | bool | None = None,
                  proud: Rule | bool | None = None, minimal: Rule | bool | None = None) -> Rule:
    tiers = [(beginner, None), (normal, ABOVE_BEGINNER), (proud, ABOVE_NORMAL), (minimal, ABOVE_PROUD)]
    alternatives: list[Rule] = []
    for rule, difficulty in tiers:
        if rule is None:
            continue
        if rule is True:
            rule = True_()
        alternatives.append(rule if difficulty is None else rule & difficulty)
    return Or(*alternatives)


def _x_worlds_clauses() -> list[Rule]:
    clauses: list[Rule] = []
    for world, keyblade in CHEST_KEYBLADES.items():
        if world == "Traverse Town":
            world_clause: Rule = True_()
        elif world == "100 Acre Wood":
            world_clause = Has("Progressive Fire")
        else:
            world_clause = Has(world)
        clauses.append(world_clause)
        clauses.append(world_clause & (Has(keyblade) | KEYBLADES_UNLOCK_CHESTS_OFF))
    return clauses


def has_x_worlds_rule(num_of_worlds: int) -> Rule:
    at_least = AtLeast(num_of_worlds * 2, *_x_worlds_clauses())
    return by_difficulty(beginner=at_least, minimal=True)


def has_x_worlds_rule_pinned_to_beginner(num_of_worlds: int) -> Rule:
    return AtLeast(num_of_worlds * 2, *_x_worlds_clauses())


def has_emblems_rule() -> Rule:
    return HasAll(*sorted(item_name_groups["Emblem Pieces"])) & Has("Hollow Bastion") & has_x_worlds_rule(6)


def has_all_magic_lvx_rule(level: int) -> Rule:
    return HasAllCounts({spell: level for spell in sorted(item_name_groups["Spells"])})


def has_offensive_magic_rule() -> Rule:
    return by_difficulty(
        beginner=HasAny("Progressive Fire", "Progressive Blizzard"),
        proud=HasAny("Progressive Thunder", "Progressive Gravity"),
        minimal=Has("Progressive Stop"),
    )


def has_lucky_emblems_rule() -> Rule:
    return Has("Lucky Emblem", count=FromOption(RequiredLuckyEmblemsEotW))


def has_final_rest_door_rule() -> Rule:
    return Or(
        Has("Lucky Emblem", count=FromOption(RequiredLuckyEmblemsDoor)) & FINAL_REST_DOOR_LUCKY_EMBLEMS,
        Has("Final Door Key") & FINAL_REST_DOOR_NOT_LUCKY_EMBLEMS,
    )


def has_defensive_tools_rule() -> Rule:
    tools = (
        HasAllCounts({"Progressive Cure": 2, "Leaf Bracer": 1, "Dodge Roll": 1})
        & HasAnyCount({"Second Chance": 1, "MP Rage": 1, "Progressive Aero": 2})
    )
    return by_difficulty(beginner=tools, minimal=True)


def has_basic_tools_rule() -> Rule:
    return (
        HasAll("Dodge Roll", "Progressive Cure")
        & HasAny("Combo Master", "Strike Raid", "Sonic Blade", "Counterattack")
        & HasAny("Leaf Bracer", "Second Chance", "Guard")
        & HasAny("Progressive Fire", "Progressive Blizzard")
    )


def can_dumbo_skip_rule() -> Rule:
    return Has("Dumbo") & HasGroup("Spells")


def has_oogie_manor_rule() -> Rule:
    return by_difficulty(
        beginner=Has("Progressive Fire") | HasAll("High Jump", "Progressive Glide") | can_dumbo_skip_rule(),
        normal=Has("High Jump", count=3),
        proud=Has("High Jump", count=2),
        minimal=HasAny("High Jump", "Progressive Glide"),
    )


def has_item_workshop_rule() -> Rule:
    return by_difficulty(
        beginner=Has("Green Trinity"),
        proud=Has("High Jump", count=2) | (can_dumbo_skip_rule() & Has("Summon Anywhere")),
    )


def has_parasite_cage_rule() -> Rule:
    return (
        Has("Monstro")
        & by_difficulty(
            beginner=Has("High Jump"),
            normal=Has("Progressive Glide"),
            proud=can_dumbo_skip_rule() & Has("Summon Anywhere"),
        )
        & has_x_worlds_rule(3)
    )


def has_key_item_rule(key_item: str) -> Rule:
    clauses: list[Rule] = [
        Has(key_item),
        Has(WORLD_KEY_ITEMS[key_item], count=2) & STACKING_WORLD_ITEMS_ON,
    ]
    if key_item == "Slide 1":
        clauses = [
            Has("Slide 1") & SLIDES_BUNDLE_ON,
            HasAll(*sorted(item_name_groups["Slides"])) & SLIDES_BUNDLE_OFF,
            Has(WORLD_KEY_ITEMS[key_item], count=2) & STACKING_WORLD_ITEMS_ON,
        ]
    if key_item == "Footprints":
        clauses = [
            Has("Footprints") & EVIDENCE_BUNDLE_ON,
            HasAny(*sorted(item_name_groups["Evidence"])) & EVIDENCE_BUNDLE_OFF,
            Has(WORLD_KEY_ITEMS[key_item], count=2) & STACKING_WORLD_ITEMS_ON,
        ]
    if key_item == "Jack-In-The-Box":
        clauses.append(Has("Forget-Me-Not") & HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON)
    rule = Or(*clauses)
    if key_item == "Crystal Trident":
        rule = rule & (Has("Crabclaw") | KEYBLADES_UNLOCK_CHESTS_OFF)
    return rule


def can_early_tea_rule() -> Rule:
    return by_difficulty(
        beginner=Has("Progressive Glide"),
        proud=HasAll("Dodge Roll", "Air Guard/Dodge Roll") & Has("Progressive High Jump", count=3),
        minimal=(
            HasAllCounts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2})
            | (
                HasAll("Dodge Roll", "Air Guard/Dodge Roll")
                & (Has("High Jump", count=2) | HasAllCounts({"Combo Master": 1, "High Jump": 1, "Air Combo Plus": 2}))
            )
        ),
    )


DUMBO_SKIP = can_dumbo_skip_rule()
DUMBO_SUMMON = DUMBO_SKIP & Has("Summon Anywhere")
EMBLEMS = has_emblems_rule()
X_WORLDS_3 = has_x_worlds_rule(3)
X_WORLDS_4 = has_x_worlds_rule(4)
X_WORLDS_6 = has_x_worlds_rule(6)
X_WORLDS_8 = has_x_worlds_rule(8)
PARASITE_CAGE = has_parasite_cage_rule()
BASIC_TOOLS = has_basic_tools_rule()
DEFENSIVE_TOOLS = has_defensive_tools_rule()
HIGH_JUMP = Has("High Jump")
HIGH_JUMP_2 = Has("High Jump", count=2)
HIGH_JUMP_3 = Has("High Jump", count=3)
GLIDE = Has("Progressive Glide")
HIGH_JUMP_AND_GLIDE = HasAll("High Jump", "Progressive Glide")
HIGH_JUMP_OR_GLIDE = HasAny("High Jump", "Progressive Glide")
DODGE_ROLL_AND_AIR_GUARD = HasAll("Dodge Roll", "Air Guard/Dodge Roll")
COMBO_MASTER = Has("Combo Master")
EOTW_ACCESS = Or(has_lucky_emblems_rule() & EOTW_UNLOCK_LUCKY_EMBLEMS, Has("End of the World"))
