from rule_builder.rules import Has, HasAll, Rule

from ..Items import item_name_groups
from ._helpers import DEFENSIVE_TOOLS, X_WORLDS_4, X_WORLDS_8, by_difficulty, has_key_item_rule


def build_rules() -> dict[str, Rule]:
    entry_pass = has_key_item_rule("Entry Pass")
    all_cups = HasAll(*sorted(item_name_groups["Cups"]))

    phil_cup_rule = Has("Phil Cup") & entry_pass
    pegasus_cup_rule = Has("Pegasus Cup") & entry_pass
    hercules_cup_rule = Has("Hercules Cup") & entry_pass & X_WORLDS_4
    hades_cup_rule = all_cups & entry_pass & X_WORLDS_8 & DEFENSIVE_TOOLS
    ice_titan_rule = (
        all_cups & entry_pass & by_difficulty(beginner=Has("Guard"), minimal=True) & X_WORLDS_8
        & DEFENSIVE_TOOLS
    )
    sephiroth_rule = all_cups & entry_pass & X_WORLDS_8 & DEFENSIVE_TOOLS

    return {
        "Olympus Coliseum Coliseum Gates Right Blue Trinity Chest": Has("Blue Trinity"),
        "Olympus Coliseum Coliseum Gates Left Blue Trinity Chest": Has("Blue Trinity"),
        "Olympus Coliseum Coliseum Gates White Trinity Chest": Has("White Trinity"),
        "Olympus Coliseum Coliseum Gates Blizzara Chest": Has("Progressive Blizzard", count=2),
        "Olympus Coliseum Coliseum Gates Blizzaga Chest": Has("Progressive Blizzard", count=3),
        "Olympus Coliseum Coliseum Gates Green Trinity": Has("Green Trinity"),
        "Olympus Coliseum Coliseum Gates Hero's License Event": entry_pass,
        "Olympus Coliseum Defeat Cerberus Inferno Band Event": entry_pass,
        "Olympus Coliseum Cloud Sonic Blade Event": entry_pass,
        "Complete Phil Cup": phil_cup_rule,
        "Complete Phil Cup Solo": phil_cup_rule,
        "Complete Phil Cup Time Trial": phil_cup_rule,
        "Complete Pegasus Cup": pegasus_cup_rule,
        "Complete Pegasus Cup Solo": pegasus_cup_rule,
        "Complete Pegasus Cup Time Trial": pegasus_cup_rule,
        "Complete Hercules Cup": hercules_cup_rule,
        "Complete Hercules Cup Solo": hercules_cup_rule,
        "Complete Hercules Cup Time Trial": hercules_cup_rule,
        "Hercules Cup Defeat Cloud Event": hercules_cup_rule,
        "Hercules Cup Yellow Trinity Event": hercules_cup_rule,
        "Olympus Coliseum Olympia Chest": all_cups & entry_pass & X_WORLDS_4,
        "Olympus Coliseum Defeat Hades Ansem's Report 8": hades_cup_rule,
        "Complete Hades Cup": hades_cup_rule,
        "Complete Hades Cup Solo": hades_cup_rule,
        "Complete Hades Cup Time Trial": hades_cup_rule,
        "Hades Cup Defeat Cloud and Leon Event": hades_cup_rule,
        "Hades Cup Defeat Yuffie Event": hades_cup_rule,
        "Hades Cup Defeat Cerberus Event": hades_cup_rule,
        "Hades Cup Defeat Behemoth Event": hades_cup_rule,
        "Hades Cup Defeat Hades Event": hades_cup_rule,
        "Olympus Coliseum Gates Purple Jar After Defeating Hades": hades_cup_rule,
        "Olympus Coliseum Defeat Ice Titan Diamond Dust Event": ice_titan_rule,
        "Olympus Coliseum Defeat Sephiroth Ansem's Report 12": sephiroth_rule,
        "Olympus Coliseum Defeat Sephiroth One-Winged Angel Event": sephiroth_rule,
    }
