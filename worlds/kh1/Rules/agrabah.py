from rule_builder.rules import Has, HasAll, HasAny, HasAnyCount, HasGroup, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext


def build_rules(ctx: RuleContext, super_bosses: bool) -> dict[str, Rule]:
    hidden_room_rule = Or(
        Has("Yellow Trinity"),
        ctx.hj1 & ABOVE_BEGINNER,
        ctx.glide & ABOVE_NORMAL,
    )

    kurt_zisa_magic = Or(
        Has("Progressive Blizzard", count=3),
        HasAnyCount({"Progressive Blizzard": 2, "Progressive Fire": 3, "Progressive Thunder": 3,
                     "Progressive Gravity": 3}) & ABOVE_BEGINNER,
        HasAnyCount({"Progressive Blizzard": 1, "Progressive Fire": 2, "Progressive Thunder": 2,
                     "Progressive Gravity": 2}) & ABOVE_NORMAL,
        (
            HasAny("Progressive Fire", "Progressive Thunder", "Progressive Gravity")
            | (HasGroup("Magic") & HasAll("Mushu", "Genie", "Dumbo"))
        ) & ABOVE_PROUD,
    )
    kurt_zisa_rule = ctx.emblems & ctx.x_worlds_8 & ctx.defensive_tools & kurt_zisa_magic

    rules: dict[str, Rule] = {
        "Agrabah Storage Green Trinity Chest": Has("Green Trinity"),
        "Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest": Has("Blue Trinity"),
        "Agrabah Cave of Wonders Entrance White Trinity Chest": Has("White Trinity"),
        "Agrabah Bazaar Blue Trinity": Has("Blue Trinity"),
        "Agrabah Cave of Wonders Treasure Room Red Trinity": Has("Red Trinity"),

        "Agrabah Main Street High Above Palace Gates Entrance Chest": Or(
            ctx.hj1,
            ctx.glide & ABOVE_BEGINNER,
            ctx.dumbo_skip & ABOVE_NORMAL,
        ),
        "Agrabah Palace Gates High Opposite Palace Chest": Or(
            ctx.hj1,
            ctx.glide & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Agrabah Palace Gates High Close to Palace Chest": Or(
            ctx.hj_glide_all,
            ctx.hj3 & ABOVE_BEGINNER,
            (ctx.hj2 | ctx.glide | HasAll("High Jump", "Combo Master")) & ABOVE_NORMAL,
            (ctx.combo_master | ctx.dumbo_summon) & ABOVE_PROUD,
        ),
        "Agrabah Cave of Wonders Entrance Tall Tower Chest": Or(
            ctx.glide,
            ctx.hj2 & ABOVE_BEGINNER,
            (ctx.combo_master | ctx.dumbo_skip | ctx.hj1 | ctx.dodge_airguard_all) & ABOVE_NORMAL,
            True_() & ABOVE_PROUD,
        ),
        "Agrabah Cave of Wonders Bottomless Hall Pillar Chest": Or(
            ctx.glide,
            ctx.hj1 & ABOVE_BEGINNER,
            True_() & ABOVE_NORMAL,
        ),
        "Agrabah Cave of Wonders Hidden Room Right Chest": hidden_room_rule,
        "Agrabah Cave of Wonders Hidden Room Left Chest": hidden_room_rule,
        "Agrabah Cave of Wonders Dark Chamber Near Save Chest": Or(
            ctx.hj_glide_any,
            True_() & ABOVE_BEGINNER,
        ),

        # Kurt Zisa's locations only exist at all when super_bosses is on (see Regions.py) - unlike
        # the difficulty tiers above, that can't be expressed as an OptionFilter on the rule itself,
        # since it gates location creation, not just rule resolution. Conditionally unpacking a
        # sub-dict keeps this as one dict literal instead of a separate append step below.
        **({
            "Agrabah Defeat Kurt Zisa Ansem's Report 11": kurt_zisa_rule,
            "Agrabah Defeat Kurt Zisa Zantetsuken Event": kurt_zisa_rule,
        } if super_bosses else {}),
    }

    return rules
