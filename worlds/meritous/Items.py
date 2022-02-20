# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Item


class MeritousItem(Item):
    game: str = "Meritous"

    def __init__(self, name, advancement, code, player):
        super(MeritousItem, self).__init__(name, advancement, code, player)
        if "Trap" in name:
            self.type = "Trap"
            self.trap = True
        elif "PSI Key" in name:
            self.type = "PSI Key"
        elif "upgrade" in name:
            self.type = "Ability upgrade"
        elif "Crystals" in name:
            self.type = "Crystals"
        elif name == "Nothing":
            self.type = "Nothing"
        elif name == "Cursed Seal" or name == "Agate Knife":
            self.type = name
        elif name == "Extra Life":
            self.type = "Other"
        else:
            self.type = "Artifact"
            self.never_exclude = True
        
        # TODO: LttP credits text



offset = 593_000

item_table = {
    "Nothing": offset + 0,
    "Reflect Shield upgrade": offset + 1,
    "Circuit Charge upgrade": offset + 2,
    "Circuit Refill upgrade": offset + 3,
    "Map": offset + 4,
    "Shield Boost": offset + 5,
    "Crystal Efficiency": offset + 6,
    "Circuit Booster": offset + 7,
    "Metabolism": offset + 8,
    "Dodge Enhancer": offset + 9,
    "Ethereal Monocle": offset + 10,
    "Crystal Gatherer": offset + 11,
    "PSI Key 1": offset + 12,
    "PSI Key 2": offset + 13,
    "PSI Key 3": offset + 14,
    "Cursed Seal": offset + 15,
    "Agate Knife": offset + 16,
    "Evolution Trap": offset + 17,
    "Crystals x500": offset + 18,
    "Crystals x1000": offset + 19,
    "Crystals x2000": offset + 20,
    "Extra Life": offset + 21
}

item_groups = {
    "PSI Keys": [f"PSI Key {x}" for x in range(1, 4)],
    "Upgrades": ["Reflect Shield upgrade", "Circuit Charge upgrade", "Circuit Refill upgrade"],
    "Artifacts": ["Map", "Shield Boost", "Crystal Efficiency", "Circuit Booster",
                  "Metabolism", "Dodge Enhancer", "Ethereal Monocle", "Crystal Gatherer"],
    "Crystals": ["Crystals x500", "Crystals x1000", "Crystals x2000"]
}
