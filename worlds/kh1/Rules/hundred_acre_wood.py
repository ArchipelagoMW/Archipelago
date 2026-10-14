from rule_builder.rules import Has, Rule

from ._helpers import COMBO_MASTER, DODGE_ROLL_AND_AIR_GUARD, HIGH_JUMP_AND_GLIDE
from ._helpers import HIGH_JUMP_OR_GLIDE, by_difficulty


def build_rules() -> dict[str, Rule]:
    torn_page_4_jump_bonus = by_difficulty(beginner=HIGH_JUMP_AND_GLIDE, normal=HIGH_JUMP_OR_GLIDE, proud=True)
    torn_page_4_rule = Has("Torn Page", count=4) & torn_page_4_jump_bonus

    rare_nut_5_rule = Has("Torn Page", count=4) & by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        normal=HIGH_JUMP_OR_GLIDE,
        minimal=COMBO_MASTER | DODGE_ROLL_AND_AIR_GUARD,
    )

    return {
        "100 Acre Wood Bouncing Spot Left Cliff Chest": torn_page_4_rule,
        "100 Acre Wood Bouncing Spot Right Tree Alcove Chest": torn_page_4_rule,
        "100 Acre Wood Bouncing Spot Under Giant Pot Chest": Has("Torn Page", count=4),
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 1": Has("Torn Page", count=4),
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 2": torn_page_4_rule,
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 3": torn_page_4_rule,
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 4": torn_page_4_rule,
        "100 Acre Wood Pooh's House Owl Cheer": Has("Torn Page", count=5),
        "100 Acre Wood Pooh's House Start Fire": Has("Torn Page", count=3),
        "100 Acre Wood Bouncing Spot Break Log": Has("Torn Page", count=4),
        "100 Acre Wood Bouncing Spot Fall Through Top of Tree Next to Pooh": torn_page_4_rule,
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 5": rare_nut_5_rule,
        "100 Acre Wood Convert Torn Page 1": Has("Torn Page", count=1),
        "100 Acre Wood Convert Torn Page 2": Has("Torn Page", count=2),
        "100 Acre Wood Convert Torn Page 3": Has("Torn Page", count=3),
        "100 Acre Wood Convert Torn Page 4": Has("Torn Page", count=4),
        "100 Acre Wood Convert Torn Page 5": Has("Torn Page", count=5),
    }
