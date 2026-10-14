from rule_builder.rules import Has, HasAll, HasAny, HasAnyCount, HasGroup, Rule

from ._helpers import COMBO_MASTER, DEFENSIVE_TOOLS, DODGE_ROLL_AND_AIR_GUARD, DUMBO_SKIP
from ._helpers import DUMBO_SUMMON, GLIDE
from ._helpers import HIGH_JUMP, HIGH_JUMP_2, HIGH_JUMP_3
from ._helpers import HIGH_JUMP_AND_GLIDE, HIGH_JUMP_OR_GLIDE, X_WORLDS_8, by_difficulty


def build_rules() -> dict[str, Rule]:
    hidden_room_rule = by_difficulty(beginner=Has("Yellow Trinity"), normal=HIGH_JUMP, proud=GLIDE)

    kurt_zisa_magic = by_difficulty(
        beginner=Has("Progressive Blizzard", count=3),
        normal=HasAnyCount({
            "Progressive Blizzard": 2,
            "Progressive Fire": 3,
            "Progressive Thunder": 3,
            "Progressive Gravity": 3,
        }),
        proud=HasAnyCount({
            "Progressive Blizzard": 1,
            "Progressive Fire": 2,
            "Progressive Thunder": 2,
            "Progressive Gravity": 2,
        }),
        minimal=(
            HasAny("Progressive Fire", "Progressive Thunder", "Progressive Gravity")
            | (HasGroup("Spells") & HasAll("Mushu", "Genie", "Dumbo"))
        ),
    )
    kurt_zisa_rule = X_WORLDS_8 & DEFENSIVE_TOOLS & kurt_zisa_magic

    main_street_high_chest_rule = by_difficulty(
        beginner=HIGH_JUMP,
        normal=GLIDE,
        proud=DUMBO_SKIP,
    )
    palace_gates_opposite_chest_rule = by_difficulty(
        beginner=HIGH_JUMP,
        proud=GLIDE,
        minimal=True,
    )
    palace_gates_close_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        normal=HIGH_JUMP_3,
        proud=HIGH_JUMP_2 | GLIDE | HasAll("High Jump", "Combo Master"),
        minimal=COMBO_MASTER | DUMBO_SUMMON,
    )
    tall_tower_chest_rule = by_difficulty(
        beginner=GLIDE,
        normal=HIGH_JUMP_2,
        proud=COMBO_MASTER | DUMBO_SKIP | HIGH_JUMP | DODGE_ROLL_AND_AIR_GUARD,
        minimal=True,
    )
    bottomless_hall_pillar_chest_rule = by_difficulty(
        beginner=GLIDE,
        normal=HIGH_JUMP,
        proud=True,
    )

    rules: dict[str, Rule] = {
        "Agrabah Storage Green Trinity Chest": Has("Green Trinity"),
        "Agrabah Cave of Wonders Silent Chamber Blue Trinity Chest": Has("Blue Trinity"),
        "Agrabah Cave of Wonders Entrance White Trinity Chest": Has("White Trinity"),
        "Agrabah Bazaar Blue Trinity": Has("Blue Trinity"),
        "Agrabah Cave of Wonders Treasure Room Red Trinity": Has("Red Trinity"),
        "Agrabah Main Street High Above Palace Gates Entrance Chest": main_street_high_chest_rule,
        "Agrabah Palace Gates High Opposite Palace Chest": palace_gates_opposite_chest_rule,
        "Agrabah Palace Gates High Close to Palace Chest": palace_gates_close_chest_rule,
        "Agrabah Cave of Wonders Entrance Tall Tower Chest": tall_tower_chest_rule,
        "Agrabah Cave of Wonders Bottomless Hall Pillar Chest": bottomless_hall_pillar_chest_rule,
        "Agrabah Cave of Wonders Hidden Room Right Chest": hidden_room_rule,
        "Agrabah Cave of Wonders Hidden Room Left Chest": hidden_room_rule,
        "Agrabah Cave of Wonders Dark Chamber Near Save Chest": by_difficulty(beginner=HIGH_JUMP_OR_GLIDE, normal=True),
        "Agrabah Defeat Kurt Zisa Ansem's Report 11": kurt_zisa_rule,
        "Agrabah Defeat Kurt Zisa Zantetsuken Event": kurt_zisa_rule,
    }

    return rules
