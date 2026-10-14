from rule_builder.rules import Has, HasAll, HasAllCounts, Or, Rule

from ._helpers import DUMBO_SKIP, DUMBO_SUMMON, GLIDE, HIGH_JUMP, HIGH_JUMP_2
from ._helpers import HIGH_JUMP_3, HIGH_JUMP_AND_GLIDE, HIGH_JUMP_OR_GLIDE, X_WORLDS_3
from ._helpers import X_WORLDS_6, by_difficulty, can_early_tea_rule, has_key_item_rule


def build_rules() -> dict[str, Rule]:
    footprints = has_key_item_rule("Footprints")
    early_tea = can_early_tea_rule()

    queens_castle_hedge = by_difficulty(beginner=footprints | HIGH_JUMP, normal=GLIDE, proud=DUMBO_SUMMON)
    tea_party_garden_above_lotus = by_difficulty(
        beginner=GLIDE | early_tea,
        normal=HIGH_JUMP_2 & footprints,
        proud=(HIGH_JUMP | DUMBO_SKIP) & footprints,
    )
    tea_party_garden_chair = footprints | GLIDE | early_tea

    rabbit_hole_defeat_heartless_3_chest_rule = by_difficulty(
        beginner=X_WORLDS_6,
        proud=X_WORLDS_3,
        minimal=True,
    )
    lotus_forest_glide_chest_rule = by_difficulty(
        beginner=GLIDE | early_tea,
        proud=(HIGH_JUMP | DUMBO_SKIP) & footprints,
    )
    lotus_forest_corner_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        normal=HIGH_JUMP_OR_GLIDE,
        proud=True,
    )
    bear_and_clock_puzzle_chest_rule = by_difficulty(
        beginner=footprints | GLIDE,
        minimal=HasAllCounts({"Combo Master": 1, "High Jump": 3, "Air Combo Plus": 2}),
    )
    across_from_bizarre_room_chest_rule = by_difficulty(
        beginner=GLIDE | early_tea,
        normal=HIGH_JUMP_3 & footprints,
        proud=(HasAll("High Jump", "Combo Master") & footprints) | (HIGH_JUMP_2 & footprints),
    )

    return {
        "Wonderland Rabbit Hole Green Trinity Chest": Has("Green Trinity"),
        "Wonderland Bizarre Room Green Trinity Chest": Has("Green Trinity"),
        "Wonderland Lotus Forest Thunder Plant Chest": Has("Progressive Thunder") & footprints,
        "Wonderland Lotus Forest Through the Painting Thunder Plant Chest": Has("Progressive Thunder") & footprints,
        "Wonderland Lotus Forest Through the Painting White Trinity Chest": Has("White Trinity") & footprints,
        "Wonderland Bizarre Room Lamp Chest": footprints,
        "Wonderland Defeat Trickmaster Blizzard Event": footprints,
        "Wonderland Defeat Trickmaster Ifrit's Horn Event": footprints,
        "Wonderland Bizarre Room Read Book": footprints,
        "Wonderland Bizarre Room Navi-G Piece Event": footprints,
        "Wonderland Lotus Forest Blue Trinity in Alcove": Has("Blue Trinity"),
        "Wonderland Lotus Forest Blue Trinity by Moving Boulder": Has("Blue Trinity") & footprints,
        "Wonderland Bizarre Room Examine Flower Pot": footprints,
        "Wonderland Lotus Forest Yellow Elixir Flower Through Painting": footprints,
        "Wonderland Lotus Forest Yellow Potion Flower Through Painting": footprints,
        "Wonderland Lotus Forest Red Flower Raise Lily Pads": footprints,
        "Wonderland Stench Evidence Box": Or(HIGH_JUMP, GLIDE),
        "Wonderland Rabbit Hole Defeat Heartless 3 Chest": rabbit_hole_defeat_heartless_3_chest_rule,
        "Wonderland Queen's Castle Hedge Left Red Chest": queens_castle_hedge,
        "Wonderland Queen's Castle Hedge Right Blue Chest": queens_castle_hedge,
        "Wonderland Queen's Castle Hedge Right Red Chest": queens_castle_hedge,
        "Wonderland Lotus Forest Glide Chest": lotus_forest_glide_chest_rule,
        "Wonderland Lotus Forest Corner Chest": lotus_forest_corner_chest_rule,
        "Wonderland Tea Party Garden Above Lotus Forest Entrance 2nd Chest": tea_party_garden_above_lotus,
        "Wonderland Tea Party Garden Above Lotus Forest Entrance 1st Chest": tea_party_garden_above_lotus,
        "Wonderland Tea Party Garden Bear and Clock Puzzle Chest": bear_and_clock_puzzle_chest_rule,
        "Wonderland Tea Party Garden Across From Bizarre Room Entrance Chest": across_from_bizarre_room_chest_rule,
        "Wonderland Tea Party Garden Left Cushioned Chair": tea_party_garden_chair,
        "Wonderland Tea Party Garden Left Pink Chair": tea_party_garden_chair,
        "Wonderland Tea Party Garden Right Yellow Chair": tea_party_garden_chair,
        "Wonderland Tea Party Garden Left Gray Chair": tea_party_garden_chair,
        "Wonderland Tea Party Garden Right Brown Chair": tea_party_garden_chair,
    }
