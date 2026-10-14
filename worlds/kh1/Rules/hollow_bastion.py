from rule_builder.rules import Has, HasAll, Rule

from ._helpers import COMBO_MASTER, DEFENSIVE_TOOLS, DODGE_ROLL_AND_AIR_GUARD, DUMBO_SKIP
from ._helpers import DUMBO_SUMMON, EMBLEMS, GLIDE, HIGH_JUMP
from ._helpers import HIGH_JUMP_2, HIGH_JUMP_3, HIGH_JUMP_AND_GLIDE
from ._helpers import X_WORLDS_8, by_difficulty, has_key_item_rule


def build_rules() -> dict[str, Rule]:
    theon_vol_6 = has_key_item_rule("Theon Vol. 6")

    emblems_or_high_jump_and_glide = by_difficulty(
        beginner=EMBLEMS,
        normal=HIGH_JUMP_3 & GLIDE,
        proud=(HIGH_JUMP_2 | DUMBO_SKIP) & GLIDE,
        minimal=HIGH_JUMP_AND_GLIDE,
    )
    emblems_or_high_jump = by_difficulty(
        beginner=EMBLEMS,
        normal=HIGH_JUMP_3,
        proud=HIGH_JUMP_2 | DUMBO_SKIP,
        minimal=HIGH_JUMP_AND_GLIDE,
    )
    emblem_piece_chest_fountain_rule = by_difficulty(
        beginner=theon_vol_6 | EMBLEMS,
        normal=HIGH_JUMP_3,
        proud=HIGH_JUMP_2,
    )
    unknown_rule = (
        EMBLEMS & X_WORLDS_8 & DEFENSIVE_TOOLS
        & by_difficulty(beginner=Has("Progressive Gravity"), normal=True)
    )

    library_node_gravity_chest_rule = Has("Progressive Gravity") & EMBLEMS
    floating_platform_near_save_chest_rule = by_difficulty(
        beginner=HIGH_JUMP | GLIDE | Has("Progressive Blizzard"),
        proud=DUMBO_SUMMON,
        minimal=DODGE_ROLL_AND_AIR_GUARD,
    )
    floating_platform_near_bubble_chest_rule = by_difficulty(
        beginner=HIGH_JUMP | GLIDE | Has("Progressive Blizzard"),
        proud=DUMBO_SUMMON,
        minimal=HasAll("Dodge Roll", "Air Guard/Dodge Roll", "Combo Master") & Has("Air Combo Plus", count=2),
    )
    rising_falls_high_platform_chest_rule = by_difficulty(
        beginner=GLIDE | (Has("Progressive Blizzard") & EMBLEMS),
        normal=HIGH_JUMP_3,
        proud=HIGH_JUMP | COMBO_MASTER | DODGE_ROLL_AND_AIR_GUARD | DUMBO_SUMMON,
        minimal=True,
    )
    heartless_sigil_door_gravity_chest_rule = Has("Progressive Gravity") & emblems_or_high_jump_and_glide
    base_level_platform_near_entrance_chest_rule = by_difficulty(
        beginner=GLIDE | HIGH_JUMP,
        normal=True,
    )
    sliding_blocks_chest_rule = EMBLEMS & Has("Progressive Gravity") & by_difficulty(beginner=GLIDE, normal=True)
    waterway_blizzard_on_bubble_chest_rule = by_difficulty(
        beginner=Has("Progressive Blizzard") & HIGH_JUMP,
        normal=HIGH_JUMP_3,
    )
    left_of_emblem_door_chest_rule = by_difficulty(
        beginner=HIGH_JUMP,
        proud=DUMBO_SKIP & (EMBLEMS | Has("Summon Anywhere")),
    )
    flame_emblem_piece_rule = (
        emblem_piece_chest_fountain_rule
        & by_difficulty(beginner=Has("Progressive Fire"), minimal=True)
        & by_difficulty(beginner=GLIDE | Has("Progressive Thunder"), normal=HIGH_JUMP, proud=True)
    )

    return {
        "Hollow Bastion Rising Falls Under Water 2nd Chest": EMBLEMS,
        "Hollow Bastion Great Crest Lower Chest": EMBLEMS,
        "Hollow Bastion Great Crest After Battle Platform Chest": EMBLEMS,
        "Hollow Bastion High Tower 2nd Gravity Chest": Has("Progressive Gravity") & EMBLEMS,
        "Hollow Bastion High Tower 1st Gravity Chest": Has("Progressive Gravity") & EMBLEMS,
        "Hollow Bastion High Tower Above Sliding Blocks Chest": EMBLEMS,
        "Hollow Bastion Lift Stop Library Node After High Tower Switch Gravity Chest": library_node_gravity_chest_rule,
        "Hollow Bastion Lift Stop Library Node Gravity Chest": Has("Progressive Gravity"),
        "Hollow Bastion Lift Stop Outside Library Gravity Chest": Has("Progressive Gravity"),
        "Hollow Bastion Grand Hall Steps Right Side Chest": EMBLEMS,
        "Hollow Bastion Grand Hall Oblivion Chest": EMBLEMS,
        "Hollow Bastion Grand Hall Left of Gate Chest": EMBLEMS,
        "Hollow Bastion Rising Falls White Trinity Chest": Has("White Trinity"),
        "Hollow Bastion Defeat Maleficent Donald Cheer Event": EMBLEMS,
        "Hollow Bastion Defeat Dragon Maleficent Fireglow Event": EMBLEMS,
        "Hollow Bastion Defeat Riku II Ragnarok Event": EMBLEMS,
        "Hollow Bastion Defeat Behemoth Omega Arts Event": EMBLEMS,
        "Hollow Bastion Speak to Princesses Fire Event": EMBLEMS,
        "Hollow Bastion Speak with Aerith Ansem's Report 2": EMBLEMS,
        "Hollow Bastion Speak with Aerith Ansem's Report 4": EMBLEMS,
        "Hollow Bastion Defeat Maleficent Ansem's Report 5": EMBLEMS,
        "Hollow Bastion Speak with Aerith Ansem's Report 6": EMBLEMS,
        "Hollow Bastion Speak with Aerith Ansem's Report 10": EMBLEMS,
        "Hollow Bastion Library Speak to Belle Divine Rose": EMBLEMS,
        "Hollow Bastion Library Speak to Aerith Cure": EMBLEMS,
        "Hollow Bastion Great Crest Blue Trinity": Has("Blue Trinity") & EMBLEMS,
        "Hollow Bastion Dungeon Blue Trinity": Has("Blue Trinity"),
        "Hollow Bastion Rising Falls Floating Platform Near Save Chest": floating_platform_near_save_chest_rule,
        "Hollow Bastion Rising Falls Floating Platform Near Bubble Chest": floating_platform_near_bubble_chest_rule,
        "Hollow Bastion Rising Falls High Platform Chest": rising_falls_high_platform_chest_rule,
        "Hollow Bastion Castle Gates Gravity Chest": Has("Progressive Gravity") & emblems_or_high_jump_and_glide,
        "Hollow Bastion Lift Stop Heartless Sigil Door Gravity Chest": heartless_sigil_door_gravity_chest_rule,
        "Hollow Bastion Lift Stop from Waterway Examine Node": emblems_or_high_jump_and_glide,
        "Hollow Bastion Castle Gates Freestanding Pillar Chest": emblems_or_high_jump,
        "Hollow Bastion Castle Gates High Pillar Chest": emblems_or_high_jump,
        "Hollow Bastion Base Level Platform Near Entrance Chest": base_level_platform_near_entrance_chest_rule,
        "Hollow Bastion Lift Stop Under High Tower Sliding Blocks Chest": sliding_blocks_chest_rule,
        "Hollow Bastion Waterway Blizzard on Bubble Chest": waterway_blizzard_on_bubble_chest_rule,
        "Hollow Bastion Entrance Hall Left of Emblem Door Chest": left_of_emblem_door_chest_rule,
        "Hollow Bastion Entrance Hall Emblem Piece (Flame)": flame_emblem_piece_rule,
        "Hollow Bastion Entrance Hall Emblem Piece (Chest)": emblem_piece_chest_fountain_rule,
        "Hollow Bastion Entrance Hall Emblem Piece (Statue)": emblem_piece_chest_fountain_rule & Has("Red Trinity"),
        "Hollow Bastion Entrance Hall Emblem Piece (Fountain)": emblem_piece_chest_fountain_rule,
        "Hollow Bastion Defeat Unknown Ansem's Report 13": unknown_rule,
        "Hollow Bastion Defeat Unknown EXP Necklace Event": unknown_rule,
    }
