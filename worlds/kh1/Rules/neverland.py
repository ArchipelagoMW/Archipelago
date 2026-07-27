from rule_builder.rules import Has, HasAll, HasAny, Or, Rule, True_

from ._option_filters import ABOVE_BEGINNER, ABOVE_NORMAL, ABOVE_PROUD
from ._context import RuleContext
from ._helpers import has_all_magic_lvx_rule


def build_rules(ctx: RuleContext, super_bosses: bool) -> dict[str, Rule]:
    neverland_hold_flight = Or(Has("Green Trinity"), ctx.glide, ctx.hj3 & ABOVE_BEGINNER)

    phantom_magic = Or(
        has_all_magic_lvx_rule(3),
        has_all_magic_lvx_rule(2) & ABOVE_BEGINNER,
        HasAll("Progressive Fire", "Progressive Blizzard", "Progressive Thunder",
               "Progressive Stop") & ABOVE_NORMAL,
        (
            HasAny("Progressive Fire", "Progressive Blizzard")
            & HasAny("Progressive Fire", "Progressive Thunder")
            & HasAny("Progressive Thunder", "Progressive Blizzard")
            & Has("Progressive Stop")
        ) & ABOVE_PROUD,
    )
    phantom_rule = (
        Has("Green Trinity") & ctx.emblems & phantom_magic
        & Or(Has("Leaf Bracer"), True_() & ABOVE_NORMAL)
    )

    return {
        "Neverland Pirate Ship Deck White Trinity Chest": HasAll("White Trinity", "Green Trinity"),
        "Neverland Pirate Ship Crows Nest Chest": Has("Green Trinity"),
        "Neverland Hold Yellow Trinity Right Blue Chest": Has("Yellow Trinity"),
        "Neverland Hold Yellow Trinity Left Blue Chest": Has("Yellow Trinity"),
        "Neverland Cabin Chest": Has("Green Trinity"),
        "Neverland Clock Tower Chest": Has("Green Trinity"),
        "Neverland Hold Yellow Trinity Green Chest": Has("Yellow Trinity"),
        "Neverland Captain's Cabin Chest": Has("Green Trinity"),
        "Neverland Hold Aero Chest": Has("Yellow Trinity"),
        "Neverland Defeat Anti Sora Raven's Claw Event": Has("Green Trinity"),
        "Neverland Encounter Hook Cure Event": Has("Green Trinity"),
        "Neverland Seal Keyhole Fairy Harp Event": Has("Green Trinity"),
        "Neverland Seal Keyhole Tinker Bell Event": Has("Green Trinity"),
        "Neverland Seal Keyhole Glide Event": Has("Green Trinity"),
        "Neverland Seal Keyhole Navi-G Piece Event": Has("Green Trinity"),
        "Neverland Defeat Captain Hook Ars Arcanum Event": Has("Green Trinity"),
        "Neverland Defeat Hook Ansem's Report 9": Has("Green Trinity"),
        "Neverland Hold Flight 1st Chest": neverland_hold_flight,
        "Neverland Hold Flight 2nd Chest": neverland_hold_flight,

        **{f"Neverland Clock Tower {i:02}:00 Door": Has("Green Trinity") for i in range(1, 13)},

        **({"Neverland Defeat Phantom Stop Event": phantom_rule} if super_bosses else {}),
    }
