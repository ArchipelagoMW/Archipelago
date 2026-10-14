from rule_builder.rules import Has, HasAll, HasAny, Rule

from ._helpers import GLIDE, HIGH_JUMP_3, by_difficulty, has_all_magic_lvx_rule


def build_rules() -> dict[str, Rule]:
    neverland_hold_flight = by_difficulty(beginner=Has("Green Trinity") | GLIDE, normal=HIGH_JUMP_3)

    phantom_magic = by_difficulty(
        beginner=has_all_magic_lvx_rule(3),
        normal=has_all_magic_lvx_rule(2),
        proud=HasAll("Progressive Fire", "Progressive Blizzard", "Progressive Thunder", "Progressive Stop"),
        minimal=(
            HasAny("Progressive Fire", "Progressive Blizzard")
            & HasAny("Progressive Fire", "Progressive Thunder")
            & HasAny("Progressive Thunder", "Progressive Blizzard")
            & Has("Progressive Stop")
        ),
    )
    phantom_rule = (
        Has("Green Trinity") & phantom_magic
        & by_difficulty(beginner=Has("Leaf Bracer"), proud=True)
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
        "Neverland Clock Tower 01:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 02:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 03:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 04:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 05:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 06:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 07:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 08:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 09:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 10:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 11:00 Door": Has("Green Trinity"),
        "Neverland Clock Tower 12:00 Door": Has("Green Trinity"),
        "Neverland Defeat Phantom Stop Event": phantom_rule,
    }
