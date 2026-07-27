from rule_builder.rules import Has, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext


def build_rules(ctx: RuleContext, enabled: bool) -> dict[str, Rule]:
    torn_page_4_jump_bonus = Or(ctx.hj_glide_all, ctx.hj_glide_any & ABOVE_BEGINNER, True_() & ABOVE_NORMAL)
    torn_page_4_rule = Has("Torn Page", count=4) & torn_page_4_jump_bonus

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
        "100 Acre Wood Bouncing Spot Turn in Rare Nut 5": Has("Torn Page", count=4) & Or(
            ctx.hj_glide_all,
            ctx.hj_glide_any & ABOVE_BEGINNER,
            (ctx.combo_master | ctx.dodge_airguard_all) & ABOVE_PROUD,
        ),

        **{f"100 Acre Wood Convert Torn Page {i}": Has("Torn Page", count=i) for i in range(1, 6)},
    } if enabled else {}
