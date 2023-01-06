from typing import Dict, Callable
from BaseClasses import CollectionState
from .Constants import NOTES, PHOBEKINS


class MessengerRules:
    def __init__(self, player: int):
        self.region_rules: Dict[str, Callable] = {
            "Ninja Village": lambda state: self.has_wingsuit(state, player),
            "Autumn Hills": lambda state: self.has_wingsuit(state, player),
            "Catacombs": lambda state: self.has_wingsuit(state, player),
            "Bamboo Creek": lambda state: self.has_wingsuit(state, player),
            "Searing Crags Upper": lambda state: self.has_vertical(state, player),
            "Cloud Ruins": lambda state: self.has_wingsuit(state, player) and state.has("Ruxxtin's Amulet", player),
            "Underworld": lambda state: self.has_tabi(state, player),
            "Forlorn Temple": lambda state: state.has_all(PHOBEKINS, player) and self.has_wingsuit(state, player),
            "Glacial Peak": lambda state: self.has_vertical(state, player),
            "Elemental Skylands": lambda state: state.has("Fairy Bottle", player),
            "Music Box": lambda state: state.has_all(NOTES, player)
        }

        self.location_rules: Dict[str, Callable] = {
            # ninja village
            "Candle": lambda state: state.has("Astral Tea Leaves", player),
            "Ninja Village Seal - Tree House": lambda state: self.has_dart(state, player),
            # autumn hills
            "Key of Hope": lambda state: self.has_dart(state, player),
            # howling grotto
            "Howling Grotto Seal - Windy Saws and Balls": lambda state: self.has_wingsuit(state, player),
            "Howling Grotto Seal - Crushing Pits": lambda state: self.has_wingsuit(state, player)
                                                                 and self.has_dart(state, player),
            # searing crags
            "Key of Strength": lambda state: state.has("Power Thistle", player),
            "Astral Tea Leaves": lambda state: state.has("Astral Seed", player),
            # glacial peak
            "Glacial Peak Seal - Ice Climbers": lambda state: self.has_dart(state, player),
            "Glacial Peak Seal - Projectile Spike Pit": lambda state: self.has_vertical(state, player),
            "Glacial Peak Seal - Glacial Air Swag": lambda state: self.has_vertical(state, player),
            # tower of time
            "Tower of Time Seal - Time Waster Seal": lambda state: self.has_dart(state, player),
            "Tower of Time Seal - Lantern Climb": lambda state: self.has_wingsuit(state, player),
            "Tower of Time Seal - Arcane Orbs": lambda state: self.has_wingsuit(state, player)
                                                              and self.has_dart(state, player),
            # underworld
            "Underworld Seal - Sharp and Windy Climb": lambda state: self.has_wingsuit(state, player),
            "Underworld Seal - Fireball Wave": lambda state: self.has_wingsuit(state, player),
            "Underworld Seal - Rising Fanta": lambda state: self.has_dart(state, player),
            # sunken shrine
            "Sun Crest": lambda state: self.has_tabi(state, player),
            "Moon Crest": lambda state: self.has_tabi(state, player),
            "Key of Love": lambda state: state.has_all({"Sun Crest", "Moon Crest"}, player),
            "Sunken Shrine Seal - Waterfall Paradise": lambda state: self.has_tabi(state, player),
            "Sunken Shrine Seal - Tabi Gauntlet": lambda state: self.has_tabi(state, player),
            # riviere turquoise
            "Fairy Bottle": lambda state: self.has_vertical(state, player),
            "Riviere Turquoise Seal - Flower Power": lambda state: self.has_vertical(state, player),
            # elemental skylands
            "Key of Symbiosis": lambda state: self.has_dart(state, player),
            "Elemental Skylands Seal - Air": lambda state: self.has_wingsuit(state, player),
            "Elemental Skylands Seal - Water": lambda state: self.has_dart(state, player),
            "Elemental Skylands Seal - Fire": lambda state: self.has_dart(state, player),
            # corrupted future
            "Key of Courage": lambda state: state.has_all({"Demon King Crown", "Fairy Bottle"}, player),
        }

    def has_wingsuit(self, state: CollectionState, player: int) -> bool:
        return state.has("Wingsuit", player)

    def has_dart(self, state: CollectionState, player: int) -> bool:
        return state.has("Rope Dart", player)

    def has_tabi(self, state: CollectionState, player: int) -> bool:
        return state.has("Ninja Tabi", player)

    def has_vertical(self, state: CollectionState, player: int) -> bool:
        return self.has_wingsuit(state, player) or self.has_dart(state, player)
