from rule_builder.rules import Has, Rule

from ._helpers import BASIC_TOOLS, COMBO_MASTER, DODGE_ROLL_AND_AIR_GUARD, DUMBO_SKIP, GLIDE
from ._helpers import HIGH_JUMP, HIGH_JUMP_2, HIGH_JUMP_3, HIGH_JUMP_AND_GLIDE
from ._helpers import HIGH_JUMP_OR_GLIDE, by_difficulty, has_key_item_rule, has_oogie_manor_rule


def build_rules() -> dict[str, Rule]:
    forget_me_not = has_key_item_rule("Forget-Me-Not")
    jack_in_the_box = has_key_item_rule("Jack-In-The-Box")
    fmn_and_jitb = forget_me_not & jack_in_the_box
    oogie_manor = has_oogie_manor_rule()

    pumpkin_structure = (
        by_difficulty(beginner=HIGH_JUMP, normal=GLIDE, proud=DUMBO_SKIP)
        & by_difficulty(beginner=GLIDE, normal=HIGH_JUMP_2, proud=COMBO_MASTER | DODGE_ROLL_AND_AIR_GUARD)
    )

    bridge_right_of_gate_chest_rule = fmn_and_jitb & by_difficulty(
        beginner=GLIDE | HIGH_JUMP_3,
        normal=HIGH_JUMP_2,
        proud=HIGH_JUMP,
        minimal=True,
    )
    lower_iron_cage_chest_rule = fmn_and_jitb & oogie_manor & by_difficulty(
        beginner=BASIC_TOOLS | GLIDE,
        normal=True,
    )
    upper_iron_cage_chest_rule = fmn_and_jitb & oogie_manor & by_difficulty(
        beginner=BASIC_TOOLS | HIGH_JUMP_AND_GLIDE,
        normal=True,
    )
    guillotine_square_high_tower_chest_rule = by_difficulty(
        beginner=HIGH_JUMP_AND_GLIDE,
        normal=HIGH_JUMP_OR_GLIDE,
        proud=DUMBO_SKIP,
    )
    bridge_left_of_gate_chest_rule = fmn_and_jitb & by_difficulty(
        beginner=GLIDE | HIGH_JUMP,
        proud=True,
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
        "Halloween Town Bridge Right of Gate Chest": bridge_right_of_gate_chest_rule,
        "Halloween Town Oogie's Manor Lower Iron Cage Chest": lower_iron_cage_chest_rule,
        "Halloween Town Oogie's Manor Upper Iron Cage Chest": upper_iron_cage_chest_rule,
        "Halloween Town Guillotine Square High Tower Chest": guillotine_square_high_tower_chest_rule,
        "Halloween Town Guillotine Square Pumpkin Structure Left Chest": pumpkin_structure,
        "Halloween Town Guillotine Square Pumpkin Structure Right Chest": pumpkin_structure,
        "Halloween Town Bridge Left of Gate Chest": bridge_left_of_gate_chest_rule,
    }
