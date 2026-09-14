from rule_builder.rules import Has, CanReachLocation, CanReachRegion

from .constants import Events, Items
from .sections import Sections


def Started(event_name: str):
    return f"{event_name} Started"


def Cleared(event_name: str):
    return f"{event_name} Cleared"


def HasStarted(event_name: str):
    return CanReachLocation(Started(event_name))


def HasCleared(event_name: str):
    return CanReachLocation(Cleared(event_name))


class Rules:
    CAN_REACH_MUSHROOM_FOREST = HasStarted(Events.TO_PHOENIX_MOUNTAIN)
    HAS_PANTS_LEVEL_1 = Has(Items.FLASH_PANTS) | Has(Items.DASHING_PANTS) | Has(Items.JUMPING_PANTS)
    HAS_PANTS_LEVEL_2 = Has(Items.FLASH_PANTS) | Has(Items.DASHING_PANTS)
    HAS_PANTS_LEVEL_3 = Has(Items.FLASH_PANTS)
    HAS_ANY_FISH = Has(Items.SACRED_FISH) | Has(Items.PSYCHIC_FISH)
    HAS_ANY_JEWEL = Has(Items.JEWEL_OF_FIRE) | Has(Items.JEWEL_OF_WATER) | Has(Items.JEWEL_OF_WIND)
    HAS_BLUE_POWDER = Has(Items.BLUE_POWDER) & CAN_REACH_MUSHROOM_FOREST
    CAN_GRAPPLE = Has(Items.GRAPPLE) | Has(Items.GRAPPLEJACK)
    CAN_LIGHT_BREAK_STUFF = Has(Items.BLACKJACK) | Has(Items.WOOD_BOOMERANG)
    CAN_BREAK_STUFF = (
        CAN_LIGHT_BREAK_STUFF
        | Has(Items.STONE_BOOMERANG)
        | Has(Items.IRON_BOOMERANG)
        | Has(Items.GRAPPLEJACK)
        | Has(Items.JEWEL_OF_FIRE)
        | Has(Items.JEWEL_OF_WATER)
    )
    CAN_DASH = HasCleared(Events.A_HUNGRY_MONKEY) | Has(Items.SACRED_FISH)
    CAN_SWIM = HasCleared(Events.I_CANT_SWIM) | Has(Items.SACRED_FISH)
    CAN_DIVE = HasCleared(Events.WHATS_UNDERWATER)
    CAN_BIG_JUMP = HasCleared(Events.A_HUNGRY_MONKEY) | HAS_PANTS_LEVEL_1 | HAS_ANY_FISH | HAS_BLUE_POWDER
    CAN_BIGGEST_JUMP = (
        HasCleared(Events.A_HUNGRY_MONKEY) & (HAS_PANTS_LEVEL_1 | Has(Items.JEWEL_OF_FIRE) | Has(Items.JEWEL_OF_WATER))
        | Has(Items.JEWEL_OF_WIND)
        | HAS_ANY_FISH
        | HAS_BLUE_POWDER
    )
    CAN_CHANGE_MOOD = CanReachRegion(Sections.MUSHROOM_FOREST.name) | Has(Items.MYSTERIOUS_MUSHROOM)


def codify(name: str) -> str:
    """Transform string into acceptable codified version"""
    name = name.lower()
    name = name.replace("10,000", "ten_thousand")
    name = name.replace("1,000", "thousand")
    name = name.replace("100", "hundred")
    name = name.replace(".", "")
    name = name.replace("!", "")
    name = name.replace("'", "")
    name = name.replace("?", "")
    name = name.replace("+", "")
    name = name.replace("-", "")
    name = name.replace(",", "")
    name = name.replace("=", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("    ", "_")
    name = name.replace("   ", "_")
    name = name.replace("  ", "_")
    name = name.replace(" ", "_")
    return name
