from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, HasAll, HasAllCounts, HasAny, HasAnyCount, HasGroup, Or, Rule, True_

from ..Data import WORLD_KEY_ITEMS
from ..Options import RequiredLuckyEmblemsDoor, RequiredLuckyEmblemsEotW
from ._constants import ALL_MAGIC, DODGE_AIRGUARD, EMBLEM_PIECES, HJ_GLIDE, KEYBLADES, WORLDS
from ._custom_rules import AtLeast
from ._field_resolvers import PuppiesRequiredCount
from ._option_filters import (
    ABOVE_BEGINNER,
    ABOVE_NORMAL,
    ABOVE_PROUD,
    AT_LEAST_MINIMAL,
    BELOW_MINIMAL,
    FINAL_REST_DOOR_LUCKY_EMBLEMS,
    FINAL_REST_DOOR_NOT_LUCKY_EMBLEMS,
    HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON,
    HUNDRED_ACRE_WOOD_OFF,
    HUNDRED_ACRE_WOOD_ON,
    KEYBLADES_UNLOCK_CHESTS_OFF,
    KEYBLADES_UNLOCK_CHESTS_ON,
    STACKING_WORLD_ITEMS_ON,
)


def _x_worlds_clauses() -> list[Rule]:
    clauses: list[Rule] = []
    for i, world in enumerate(WORLDS):
        if world == "Traverse Town":
            world_clause: Rule = True_()
        elif world == "100 Acre Wood":
            world_clause = Or(
                Has("Progressive Fire") & HUNDRED_ACRE_WOOD_ON,
                Has(world) & HUNDRED_ACRE_WOOD_OFF,
            )
        else:
            world_clause = Has(world)
        clauses.append(world_clause)
        clauses.append(Or(
            (world_clause & Has(KEYBLADES[i])) & KEYBLADES_UNLOCK_CHESTS_ON,
            world_clause & KEYBLADES_UNLOCK_CHESTS_OFF,
        ))
    return clauses


def has_x_worlds_rule(num_of_worlds: int) -> Rule:
    at_least = AtLeast(num_of_worlds * 2, *_x_worlds_clauses())
    return Or(True_() & AT_LEAST_MINIMAL, at_least & BELOW_MINIMAL)


def has_x_worlds_rule_pinned_to_beginner(num_of_worlds: int) -> Rule:
    """Same as has_x_worlds_rule, but ignores the configured difficulty entirely (always behaves as
    if it were LOGIC_BEGINNER). Used by exactly one location - see traverse_town.py's "Magician's
    Study Obtained All Arts Items" - which Rules.py deliberately pins this way for softlock
    prevention, regardless of what difficulty the player actually chose.
    """
    return AtLeast(num_of_worlds * 2, *_x_worlds_clauses())


def has_emblems_rule() -> Rule:
    return HasAll(*EMBLEM_PIECES) & has_x_worlds_rule(6)


def has_puppies_rule(puppies_required: int) -> Rule:
    return Has("Puppy", count=PuppiesRequiredCount(puppies_required))


def has_all_magic_lvx_rule(level: int) -> Rule:
    return HasAllCounts({spell: level for spell in ALL_MAGIC})


def has_offensive_magic_rule() -> Rule:
    return Or(
        HasAny("Progressive Fire", "Progressive Blizzard"),
        HasAny("Progressive Thunder", "Progressive Gravity") & ABOVE_NORMAL,
        Has("Progressive Stop") & ABOVE_PROUD,
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
    return Or(True_() & AT_LEAST_MINIMAL, tools & BELOW_MINIMAL)


def has_basic_tools_rule() -> Rule:
    return (
        HasAll("Dodge Roll", "Progressive Cure")
        & HasAny("Combo Master", "Strike Raid", "Sonic Blade", "Counterattack")
        & HasAny("Leaf Bracer", "Second Chance", "Guard")
        # offensive magic pinned to LOGIC_BEGINNER, per Rules.py's has_basic_tools - at Beginner,
        # has_offensive_magic_rule's ABOVE_NORMAL/ABOVE_PROUD tiers can never apply, so this is
        # exactly that rule's Beginner-equivalent form.
        & HasAny("Progressive Fire", "Progressive Blizzard")
    )


def can_dumbo_skip_rule() -> Rule:
    return Has("Dumbo") & HasGroup("Magic")


def has_oogie_manor_rule() -> Rule:
    return Or(
        Has("Progressive Fire"),
        Has("High Jump", count=3) & ABOVE_BEGINNER,
        Has("High Jump", count=2) & ABOVE_NORMAL,
        # NOTE: in Rules.py these next two clauses are NOT actually gated by `difficulty > LOGIC_NORMAL`
        # due to `and`/`or` precedence - replicated as unconditional here. See has_oogie_manor in Rules.py.
        HasAll(*HJ_GLIDE),
        can_dumbo_skip_rule(),
        HasAny(*HJ_GLIDE) & ABOVE_PROUD,
    )


def has_item_workshop_rule() -> Rule:
    return Or(
        Has("Green Trinity"),
        (Has("High Jump", count=2) | (can_dumbo_skip_rule() & Has("Summon Anywhere"))) & ABOVE_NORMAL,
    )


def has_parasite_cage_rule() -> Rule:
    return (
        Has("Monstro")
        & Or(
            Has("High Jump"),
            Has("Progressive Glide") & ABOVE_BEGINNER,
            (can_dumbo_skip_rule() & Has("Summon Anywhere")) & ABOVE_NORMAL,
        )
        & has_x_worlds_rule(3)
    )


def has_key_item_rule(key_item: str) -> Rule:
    clauses: list[Rule] = [
        Has(key_item),
        Has(WORLD_KEY_ITEMS[key_item], count=2) & STACKING_WORLD_ITEMS_ON,
    ]
    if key_item == "Jack-In-The-Box":
        clauses.append(Has("Forget-Me-Not") & HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON)
    rule = Or(*clauses)
    if key_item == "Crystal Trident":
        rule = rule & Or(Has("Crabclaw") & KEYBLADES_UNLOCK_CHESTS_ON, True_() & KEYBLADES_UNLOCK_CHESTS_OFF)
    return rule


def can_early_tea_rule() -> Rule:
    return Or(
        Has("Progressive Glide"),
        (HasAll(*DODGE_AIRGUARD) & Has("Progressive High Jump", count=3)) & ABOVE_NORMAL,
        (
            HasAllCounts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2})
            | (
                HasAll(*DODGE_AIRGUARD)
                & (Has("High Jump", count=2) | HasAllCounts({"Combo Master": 1, "High Jump": 1, "Air Combo Plus": 2}))
            )
        ) & ABOVE_PROUD,
    )
