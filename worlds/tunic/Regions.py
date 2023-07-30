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
                  "Ruined Atoll", "Eastern Vault Fortress", "Beneath the Vault", "Quarry", "Swamp", "Boss Arena"},
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
    "Cathedral": {"Swamp"},
    "Boss Arena": {"Overworld"}
}



def set_region_rules(multiworld: MultiWorld, player: int):
    laurels = "Hero's Laurels"
    grapple = "Magic Orb"
    lantern = "Lantern"
    mask = "Scavenger Mask"
    prayer = "Pages 24-25 (Prayer)"
    holy_cross = "Pages 42-43 (Holy Cross)"
    red_hexagon = "Red Hexagon"
    green_hexagon = "Green Hexagon"
    blue_hexagon = "Blue Hexagon"

    ability_shuffle = multiworld.ability_shuffling[player].value

    if ability_shuffle:
        multiworld.get_entrance("Overworld -> Overworld Holy Cross", player).access_rule = lambda state: state.has(holy_cross, player)
        multiworld.get_entrance("Library -> Ruined Atoll", player).access_rule = lambda state: state.has(prayer, player)
        multiworld.get_entrance("Overworld -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player) and state.has(prayer, player)
        multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = lambda state: state.has(grapple, player) and state.has(prayer, player)
        multiworld.get_entrance("Swamp -> Cathedral", player).access_rule = lambda state: state.has(laurels, player) and state.has(prayer, player)
        multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = lambda state: (state.has(grapple, player) or state.has(laurels, player)) and state.has(prayer, player)
        multiworld.get_entrance("Overworld -> Boss Arena", player).access_rule = lambda state: state.has(prayer, player) and state.has(red_hexagon, player) and state.has(green_hexagon, player) and state.has(blue_hexagon, player)
    else:
        multiworld.get_entrance("Overworld -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player)
        multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = lambda state: state.has(grapple, player)
        multiworld.get_entrance("Swamp -> Cathedral", player).access_rule = lambda state: state.has(laurels, player)
        multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = lambda state: state.has(grapple, player) or state.has(laurels, player)
        multiworld.get_entrance("Overworld -> Boss Arena", player).access_rule = lambda state: state.has(red_hexagon, player) and state.has(green_hexagon, player) and state.has(blue_hexagon, player)

    multiworld.get_entrance("Overworld -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Overworld -> West Garden", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("Overworld -> Eastern Vault Fortress", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("East Forest -> Eastern Vault Fortress", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("Bottom of the Well -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("West Garden -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Eastern Vault Fortress -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Quarry -> Lower Quarry", player).access_rule = lambda state: state.has(mask, player)


