from rule_builder.rules import Has, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext


def build_rules(ctx: RuleContext) -> dict[str, Rule]:
    monstro_mouth_high_platform = Or(
        ctx.hj1,
        ctx.glide & ABOVE_BEGINNER,
        ctx.dumbo_summon & ABOVE_NORMAL,
    )

    return {
        "Monstro Mouth Blue Trinity": Has("Blue Trinity"),
        "Monstro Throat Blue Trinity": Has("Blue Trinity") & ctx.parasite_cage,
        "Monstro Chamber 5 Blue Trinity": Has("Blue Trinity"),
        "Monstro Chamber 6 White Trinity Chest": Has("White Trinity"),
        "Monstro Defeat Parasite Cage II Stop Event": ctx.parasite_cage,

        "Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest": Or(ctx.hj1, True_() & ABOVE_NORMAL),
        "Monstro Chamber 6 Other Platform Chest": Or(
            ctx.hj_glide_all,
            (ctx.combo_master | ctx.hj1 | ctx.glide | ctx.dodge_airguard_all | ctx.dumbo_skip) & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest": Or(
            ctx.hj_glide_all,
            (ctx.combo_master | ctx.hj1 | ctx.glide | ctx.dodge_airguard_all | ctx.dumbo_summon) & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Monstro Mouth High Platform Boat Side Chest": monstro_mouth_high_platform,
        "Monstro Mouth High Platform Across from Boat Chest": monstro_mouth_high_platform,
        "Monstro Mouth Green Trinity Top of Boat Chest": monstro_mouth_high_platform & Has("Green Trinity"),
        "Monstro Mouth Near Ship Chest": Or(True_() & ABOVE_BEGINNER, ctx.hj_glide_any, ctx.basic_tools),
        "Monstro Chamber 2 Platform Chest": Or(ctx.hj_glide_any, True_() & ABOVE_BEGINNER),
        "Monstro Chamber 5 Platform Chest": Or(ctx.hj1, True_() & ABOVE_NORMAL),
        "Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest": Or(ctx.hj1, True_() & ABOVE_BEGINNER),
        "Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest": Or(ctx.hj1, True_() & ABOVE_BEGINNER),
        "Monstro Chamber 5 Atop Barrel Chest": Or(ctx.hj1, True_() & ABOVE_NORMAL),
    }
