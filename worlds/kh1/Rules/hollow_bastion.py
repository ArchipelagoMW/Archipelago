from rule_builder.rules import Has, HasAll, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext
from ._helpers import has_key_item_rule


def build_rules(ctx: RuleContext, super_bosses: bool, final_rest_door_key: str) -> dict[str, Rule]:
    theon_vol_6 = has_key_item_rule("Theon Vol. 6")

    gravity_access_bonus = Or(
        ctx.emblems,
        (ctx.hj3 & ctx.glide) & ABOVE_BEGINNER,
        ((ctx.hj2 | ctx.dumbo_skip) & ctx.glide) & ABOVE_NORMAL,
        ctx.hj_glide_all & ABOVE_PROUD,
    )
    emblems_or_high_jump = Or(
        ctx.emblems,
        ctx.hj3 & ABOVE_BEGINNER,
        (ctx.hj2 | ctx.dumbo_skip) & ABOVE_NORMAL,
        ctx.hj_glide_all & ABOVE_PROUD,
    )
    emblem_piece_chest_fountain_rule = Or(theon_vol_6, ctx.emblems, ctx.hj3 & ABOVE_BEGINNER, ctx.hj2 & ABOVE_NORMAL)
    unknown_rule = (
        ctx.emblems & ctx.x_worlds_8 & ctx.defensive_tools
        & Or(True_() & ABOVE_BEGINNER, Has("Progressive Gravity"))
    )

    return {
        "Hollow Bastion Rising Falls Under Water 2nd Chest": ctx.emblems,
        "Hollow Bastion Great Crest Lower Chest": ctx.emblems,
        "Hollow Bastion Great Crest After Battle Platform Chest": ctx.emblems,
        "Hollow Bastion High Tower 2nd Gravity Chest": Has("Progressive Gravity") & ctx.emblems,
        "Hollow Bastion High Tower 1st Gravity Chest": Has("Progressive Gravity") & ctx.emblems,
        "Hollow Bastion High Tower Above Sliding Blocks Chest": ctx.emblems,
        "Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest": (
            Has("Progressive Gravity") & ctx.emblems
        ),
        "Hollow Bastion Lift Stop Library Node Gravity Chest": Has("Progressive Gravity"),
        "Hollow Bastion Lift Stop Outside Library Gravity Chest": Has("Progressive Gravity"),
        "Hollow Bastion Grand Hall Steps Right Side Chest": ctx.emblems,
        "Hollow Bastion Grand Hall Oblivion Chest": ctx.emblems,
        "Hollow Bastion Grand Hall Left of Gate Chest": ctx.emblems,
        "Hollow Bastion Rising Falls White Trinity Chest": Has("White Trinity"),
        "Hollow Bastion Defeat Maleficent Donald Cheer Event": ctx.emblems,
        "Hollow Bastion Defeat Dragon Maleficent Fireglow Event": ctx.emblems,
        "Hollow Bastion Defeat Riku II Ragnarok Event": ctx.emblems,
        "Hollow Bastion Defeat Behemoth Omega Arts Event": ctx.emblems,
        "Hollow Bastion Speak to Princesses Fire Event": ctx.emblems,
        "Hollow Bastion Speak with Aerith Ansem's Report 2": ctx.emblems,
        "Hollow Bastion Speak with Aerith Ansem's Report 4": ctx.emblems,
        "Hollow Bastion Defeat Maleficent Ansem's Report 5": ctx.emblems,
        "Hollow Bastion Speak with Aerith Ansem's Report 6": ctx.emblems,
        "Hollow Bastion Speak with Aerith Ansem's Report 10": ctx.emblems,
        "Hollow Bastion Library Speak to Belle Divine Rose": ctx.emblems,
        "Hollow Bastion Library Speak to Aerith Cure": ctx.emblems,
        "Hollow Bastion Great Crest Blue Trinity": Has("Blue Trinity") & ctx.emblems,
        "Hollow Bastion Dungeon Blue Trinity": Has("Blue Trinity"),

        "Hollow Bastion Rising Falls Floating Platform Near Save Chest": Or(
            ctx.hj1, ctx.glide, Has("Progressive Blizzard"),
            ctx.dumbo_summon & ABOVE_NORMAL,
            ctx.dodge_airguard_all & ABOVE_PROUD,
        ),
        "Hollow Bastion Rising Falls Floating Platform Near Bubble Chest": Or(
            ctx.hj1, ctx.glide, Has("Progressive Blizzard"),
            ctx.dumbo_summon & ABOVE_NORMAL,
            (HasAll("Dodge Roll", "Air Guard/Dodge Roll", "Combo Master")
             & Has("Air Combo Plus", count=2)) & ABOVE_PROUD,
        ),
        "Hollow Bastion Rising Falls High Platform Chest": Or(
            ctx.glide, Has("Progressive Blizzard") & ctx.emblems,
            ctx.hj3 & ABOVE_BEGINNER,
            (ctx.hj1 | ctx.combo_master | ctx.dodge_airguard_all | ctx.dumbo_summon) & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Hollow Bastion Castle Gates Gravity Chest": Has("Progressive Gravity") & gravity_access_bonus,
        "Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest": (
            Has("Progressive Gravity") & gravity_access_bonus
        ),
        "Hollow Bastion Lift Stop from Waterway Examine Node": gravity_access_bonus,
        "Hollow Bastion Castle Gates Freestanding Pillar Chest": emblems_or_high_jump,
        "Hollow Bastion Castle Gates High Pillar Chest": emblems_or_high_jump,
        "Hollow Bastion Base Level Platform Near Entrance Chest": Or(True_() & ABOVE_BEGINNER, ctx.glide | ctx.hj1),
        "Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest": (
            ctx.emblems & Has("Progressive Gravity") & Or(True_() & ABOVE_BEGINNER, ctx.glide)
        ),
        "Hollow Bastion Waterway Blizzard on Bubble Chest": Or(
            Has("Progressive Blizzard") & ctx.hj1, ctx.hj3 & ABOVE_BEGINNER,
        ),
        "Hollow Bastion Entrance Hall Left of Emblem Door Chest": Or(
            ctx.hj1, (ctx.dumbo_skip & (ctx.emblems | Has("Summon Anywhere"))) & ABOVE_NORMAL,
        ),
        "Hollow Bastion Entrance Hall Emblem Piece (Flame)": (
            emblem_piece_chest_fountain_rule
            & Or(Has("Progressive Fire"), True_() & ABOVE_PROUD)
            & Or(ctx.glide, Has("Progressive Thunder"), ctx.hj1 & ABOVE_BEGINNER, True_() & ABOVE_NORMAL)
        ),
        "Hollow Bastion Entrance Hall Emblem Piece (Chest)": emblem_piece_chest_fountain_rule,
        "Hollow Bastion Entrance Hall Emblem Piece (Statue)": (
            emblem_piece_chest_fountain_rule & Has("Red Trinity")
        ),
        "Hollow Bastion Entrance Hall Emblem Piece (Fountain)": emblem_piece_chest_fountain_rule,

        **({
            "Hollow Bastion Defeat Unknown Ansem's Report 13": unknown_rule,
            "Hollow Bastion Defeat Unknown EXP Necklace Event": unknown_rule,
        } if super_bosses or final_rest_door_key == "unknown" else {}),
    }
