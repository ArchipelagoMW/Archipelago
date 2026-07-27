from rule_builder.rules import Has, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext


def build_rules(ctx: RuleContext) -> dict[str, Rule]:
    giant_crevasse_2nd_3rd = Or(ctx.hj_glide_any, True_() & ABOVE_BEGINNER)

    return {
        "End of the World Giant Crevasse 5th Chest": Or(ctx.glide, True_() & ABOVE_NORMAL),
        "End of the World Giant Crevasse 1st Chest": Or(ctx.hj1, ctx.glide, True_() & ABOVE_NORMAL),
        "End of the World Giant Crevasse 2nd Chest": giant_crevasse_2nd_3rd,
        "End of the World Giant Crevasse 3rd Chest": giant_crevasse_2nd_3rd,
        "End of the World Giant Crevasse 4th Chest": Or(
            ctx.glide,
            (ctx.hj2 | ctx.dumbo_summon) & ABOVE_NORMAL,
            ctx.dodge_airguard_all & ABOVE_PROUD,
        ),
        "End of the World World Terminus Agrabah Chest": Or(
            ctx.hj1, (ctx.dumbo_skip & (ctx.glide | Has("Summon Anywhere"))) & ABOVE_NORMAL,
        ),
    }
