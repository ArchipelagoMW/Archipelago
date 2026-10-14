from rule_builder.rules import Has, Rule

from ._helpers import DODGE_ROLL_AND_AIR_GUARD, DUMBO_SKIP, DUMBO_SUMMON, GLIDE
from ._helpers import HIGH_JUMP, HIGH_JUMP_2, HIGH_JUMP_OR_GLIDE, by_difficulty


def build_rules() -> dict[str, Rule]:
    giant_crevasse_2nd_3rd = by_difficulty(beginner=HIGH_JUMP_OR_GLIDE, normal=True)

    giant_crevasse_4th_chest_rule = by_difficulty(
        beginner=GLIDE,
        proud=HIGH_JUMP_2 | DUMBO_SUMMON,
        minimal=DODGE_ROLL_AND_AIR_GUARD,
    )
    world_terminus_agrabah_chest_rule = by_difficulty(
        beginner=HIGH_JUMP,
        proud=DUMBO_SKIP & (GLIDE | Has("Summon Anywhere")),
    )

    return {
        "End of the World Giant Crevasse 5th Chest": by_difficulty(beginner=GLIDE, proud=True),
        "End of the World Giant Crevasse 1st Chest": by_difficulty(beginner=HIGH_JUMP | GLIDE, proud=True),
        "End of the World Giant Crevasse 2nd Chest": giant_crevasse_2nd_3rd,
        "End of the World Giant Crevasse 3rd Chest": giant_crevasse_2nd_3rd,
        "End of the World Giant Crevasse 4th Chest": giant_crevasse_4th_chest_rule,
        "End of the World World Terminus Agrabah Chest": world_terminus_agrabah_chest_rule,
    }
