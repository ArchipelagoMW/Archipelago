from typing import Dict, Set

from BaseClasses import MultiWorld

class TunicEntrance:
    name: str
    rule: bool

    def __init__(self, name, rule):
        self.name = name
        self.rule = rule


tunic_regions: Dict[str, Set[str]] = {
    "Menu": {"Overworld"},
    "Overworld": {"Menu", "Overworld Holy Cross", "East Forest", "Dark Tomb", "Bottom of the Well", "West Garden",
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry", "Swamp"},
    "Overworld Holy Cross": {"Overworld"},
    "East Forest": {"Overworld", "Eastern Vault Fortress"},
    "Dark Tomb": {"Overworld", "West Garden"},
    "Bottom of the Well": {"Overworld", "Dark Tomb"},
    "West Garden": {"Overworld", "Dark Tomb"},
    "Ruined Atoll": {"Overworld", "Frog's Domain", "Library"},
    "Frog's Domain": {"Ruined Atoll"},
    "Library": {"Ruined Atoll"},
    "Eastern Vault Fortress": {"Overworld", "Beneath the Vault"},
    "Beneath the Vault": {"Overworld", "Eastern Vault Fortress"},
    "Quarry": {"Overworld", "Lower Quarry"},
    "Lower Quarry": {"Quarry", "Rooted Ziggurat"},
    "Rooted Ziggurat": {"Lower Quarry"},
    "Swamp": {"Overworld", "Cathedral"},
    "Cathedral": {"Swamp"}
}

def set_region_rules(tunic_world):
    player = tunic_world.player
    multiworld: MultiWorld = tunic_world.multiworld

    laurels = lambda state: state.has("Hero's Laurels", player)
    grapple = lambda state: state.has("Magic Orb", player)
    lantern = lambda state: state.has("Lantern", player)
    mask = lambda state: state.has("Scavenger Mask", player)
    prayer = lambda state: state.has("Pages 24-25 (Prayer)", player)
    holy_cross = lambda state: state.has("Pages 42-43 (Holy Cross)", player)

    for entrance in multiworld.get_region("Overworld", player).entrances:
        if entrance.name == "Overworld Holy Cross" and multiworld.ability_shuffling[player].value:
            entrance.access_rule = holy_cross
        if entrance.name == "Dark Tomb":
            entrance.access_rule = lantern
        if entrance.name == "West Garden":
            entrance.access_rule = laurels
        if entrance.name == "Beneath the Vault":
            entrance.access_rule = lantern and prayer if multiworld.ability_shuffling[player].value else lantern

    for entrance in multiworld.get_region("East Forest", player).entrances:
        if entrance.name == "Eastern Vault Fortress":
            entrance.access_rule = laurels

    for entrance in multiworld.get_region("Bottom of the Well", player).entrances:
        if entrance.name == "Dark Tomb":
            entrance.access_rule = lantern

    for entrance in multiworld.get_region("West Garden", player).entrances:
        if entrance.name == "Dark Tomb":
            entrance.access_rule = lantern
        if entrance.name == "Overworld":
            entrance.access_rule = laurels

    for entrance in multiworld.get_region("Ruined Atoll", player).entrances:
        if entrance.name == "Library":
            entrance.access_rule = (grapple or laurels) and prayer if multiworld.ability_shuffling[player].value \
                else (grapple or laurels)

    for entrance in multiworld.get_region("Library", player).entrances:
        if multiworld.ability_shuffling[player].value:
            entrance.access_rule = prayer

    for entrance in multiworld.get_region("Eastern Vault Fortress", player).entrances:
        if entrance.name == "Beneath the Vault":
            entrance.access_rule = lantern

    for entrance in multiworld.get_region("Quarry", player).entrances:
        if entrance.name == "Lower Quarry":
            entrance.access_rule = mask

    for entrance in multiworld.get_region("Lower Quarry", player).entrances:
        if entrance.name == "Rooted Ziggurat":
            entrance.access_rule = (grapple and prayer) if multiworld.ability_shuffling[player].value else grapple

    for entrance in multiworld.get_region("Swamp", player).entrances:
        if entrance.name == "Cathedral":
            entrance.access_rule = (laurels and prayer) if multiworld.ability_shuffling[player].value else laurels



