from rule_builder.rules import Has, Rule

from ._helpers import BASIC_TOOLS, COMBO_MASTER, DODGE_ROLL_AND_AIR_GUARD, DUMBO_SKIP
from ._helpers import DUMBO_SUMMON, GLIDE, HIGH_JUMP, HIGH_JUMP_AND_GLIDE
from ._helpers import HIGH_JUMP_OR_GLIDE, PARASITE_CAGE, by_difficulty


def build_rules() -> dict[str, Rule]:
    monstro_mouth_high_platform = by_difficulty(beginner=HIGH_JUMP, normal=GLIDE, proud=DUMBO_SUMMON)

    chamber_6_other_platform_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        proud=COMBO_MASTER | HIGH_JUMP | GLIDE | DODGE_ROLL_AND_AIR_GUARD | DUMBO_SKIP,
        minimal=True,
    )
    chamber_6_raised_area_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        proud=COMBO_MASTER | HIGH_JUMP | GLIDE | DODGE_ROLL_AND_AIR_GUARD | DUMBO_SUMMON,
        minimal=True,
    )

    return {
        "Monstro Mouth Blue Trinity": Has("Blue Trinity"),
        "Monstro Throat Blue Trinity": Has("Blue Trinity") & PARASITE_CAGE,
        "Monstro Chamber 5 Blue Trinity": Has("Blue Trinity"),
        "Monstro Chamber 6 White Trinity Chest": Has("White Trinity"),
        "Monstro Defeat Parasite Cage II Stop Event": PARASITE_CAGE,
        "Monstro Chamber 6 Platform Near Chamber 5 Entrance Chest": by_difficulty(beginner=HIGH_JUMP, proud=True),
        "Monstro Chamber 6 Other Platform Chest": chamber_6_other_platform_chest_rule,
        "Monstro Chamber 6 Raised Area Near Chamber 1 Entrance Chest": chamber_6_raised_area_chest_rule,
        "Monstro Mouth High Platform Boat Side Chest": monstro_mouth_high_platform,
        "Monstro Mouth High Platform Across from Boat Chest": monstro_mouth_high_platform,
        "Monstro Mouth Green Trinity Top of Boat Chest": monstro_mouth_high_platform & Has("Green Trinity"),
        "Monstro Mouth Near Ship Chest": by_difficulty(beginner=HIGH_JUMP_OR_GLIDE | BASIC_TOOLS, normal=True),
        "Monstro Chamber 2 Platform Chest": by_difficulty(beginner=HIGH_JUMP_OR_GLIDE, normal=True),
        "Monstro Chamber 5 Platform Chest": by_difficulty(beginner=HIGH_JUMP, proud=True),
        "Monstro Chamber 3 Platform Above Chamber 2 Entrance Chest": by_difficulty(beginner=HIGH_JUMP, normal=True),
        "Monstro Chamber 3 Platform Near Chamber 6 Entrance Chest": by_difficulty(beginner=HIGH_JUMP, normal=True),
        "Monstro Chamber 5 Atop Barrel Chest": by_difficulty(beginner=HIGH_JUMP, proud=True),
    }
