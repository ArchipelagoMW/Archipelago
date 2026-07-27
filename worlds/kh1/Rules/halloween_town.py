from rule_builder.rules import Or, Has, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext
from ._helpers import has_key_item_rule, has_oogie_manor_rule


def build_rules(ctx: RuleContext) -> dict[str, Rule]:
    forget_me_not = has_key_item_rule("Forget-Me-Not")
    jack_in_the_box = has_key_item_rule("Jack-In-The-Box")
    fmn_and_jitb = forget_me_not & jack_in_the_box
    oogie_manor = has_oogie_manor_rule()

    pumpkin_structure = (
        Or(ctx.hj1, ctx.glide & ABOVE_BEGINNER, ctx.dumbo_skip & ABOVE_NORMAL)
        & Or(ctx.glide, ctx.hj2 & ABOVE_BEGINNER, (ctx.combo_master | ctx.dodge_airguard_all) & ABOVE_NORMAL)
    )

    return {
        "Halloween Town Moonlight Hill White Trinity Chest": Has("White Trinity") & forget_me_not,
        "Halloween Town Bridge Under Bridge": fmn_and_jitb,
        "Halloween Town Boneyard Tombstone Puzzle Chest": forget_me_not,
        "Halloween Town Cemetery Behind Grave Chest": fmn_and_jitb & oogie_manor,
        "Halloween Town Cemetery By Cat Shape Chest": fmn_and_jitb & oogie_manor,
        "Halloween Town Cemetery Between Graves Chest": fmn_and_jitb & oogie_manor,
        "Halloween Town Oogie's Manor Hollow Chest": fmn_and_jitb & oogie_manor,
        "Halloween Town Oogie's Manor Grounds Red Trinity Chest": fmn_and_jitb & Has("Red Trinity"),
        "Halloween Town Oogie's Manor Entrance Steps Chest": fmn_and_jitb,
        "Halloween Town Oogie's Manor Inside Entrance Chest": fmn_and_jitb,
        "Halloween Town Cemetery By Striped Grave Chest": fmn_and_jitb & oogie_manor,
        "Halloween Town Defeat Oogie Boogie Holy Circlet Event": fmn_and_jitb & oogie_manor,
        "Halloween Town Defeat Oogie's Manor Gravity Event": fmn_and_jitb & oogie_manor,
        "Halloween Town Seal Keyhole Pumpkinhead Event": fmn_and_jitb & oogie_manor,
        "Halloween Town Defeat Oogie Boogie Ansem's Report 7": fmn_and_jitb & oogie_manor,

        "Halloween Town Bridge Right of Gate Chest": fmn_and_jitb & Or(
            ctx.glide, ctx.hj3,
            ctx.hj2 & ABOVE_BEGINNER,
            ctx.hj1 & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Halloween Town Oogie's Manor Lower Iron Cage Chest": fmn_and_jitb & oogie_manor & Or(
            True_() & ABOVE_BEGINNER, ctx.basic_tools, ctx.glide,
        ),
        "Halloween Town Oogie's Manor Upper Iron Cage Chest": fmn_and_jitb & oogie_manor & Or(
            True_() & ABOVE_BEGINNER, ctx.basic_tools, ctx.hj_glide_all,
        ),
        "Halloween Town Guillotine Square High Tower Chest": Or(
            ctx.hj_glide_all,
            ctx.hj_glide_any & ABOVE_BEGINNER,
            ctx.dumbo_skip & ABOVE_NORMAL,
        ),
        "Halloween Town Guillotine Square Pumpkin Structure Left Chest": pumpkin_structure,
        "Halloween Town Guillotine Square Pumpkin Structure Right Chest": pumpkin_structure,
        "Halloween Town Bridge Left of Gate Chest": fmn_and_jitb & Or(ctx.glide, ctx.hj1, True_() & ABOVE_NORMAL),
    }
