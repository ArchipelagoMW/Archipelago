from typing import Dict, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule
from .regions import get_entrance_info
from .locations import get_location_info
from .data import iname

if TYPE_CHECKING:
    from . import CotMWorld


class CotMRules:
    player: int
    world: "CotMWorld"
    rules: Dict[str, CollectionRule]
    required_last_keys: int
    break_iron_maidens: int
    ignore_cleansing: int

    def __init__(self, world: "CotMWorld") -> None:
        self.player = world.player
        self.world = world
        self.required_last_keys = world.required_last_keys
        self.break_iron_maidens = world.options.break_iron_maidens.value
        self.ignore_cleansing = world.options.ignore_cleansing.value

        self.rules = {
            "Roc": lambda state: state.has(iname.roc_wing, self.player),
            "Push": lambda state: state.has(iname.heavy_ring, self.player),
            "Tackle": lambda state: state.has(iname.tackle, self.player),
            "Tackle AND Roc": lambda state: state.has(iname.tackle, self.player) and state.has(iname.roc_wing,
                                                                                               self.player),
            "Tackle AND Push": lambda state: state.has(iname.tackle, self.player) and state.has(iname.heavy_ring,
                                                                                                self.player),
            "Double": lambda state: state.has(iname.double, self.player) or state.has(iname.roc_wing, self.player),
            "Double AND Freeze": lambda state: (state.has(iname.double, self.player) and self.has_ice_or_stone(
                state)) or state.has(iname.roc_wing, self.player),
            "Double OR Kick": lambda state: state.has(iname.double, self.player) or state.has(
                iname.kick_boots, self.player) or state.has(iname.roc_wing, self.player),
            "Kick": lambda state: state.has(iname.kick_boots, self.player) or state.has(iname.roc_wing, self.player),
            "Kick AND Freeze": lambda state: (state.has(iname.kick_boots, self.player) and self.has_ice_or_stone(
                state)) or state.has(iname.roc_wing, self.player),
            "Freeze": lambda state: self.has_ice_or_stone(state) or state.has(iname.roc_wing, self.player),
            "Cleansing": self.can_touch_water,
            "Iron Maiden": self.broke_iron_maidens,
            "Iron Maiden AND Push": lambda state: self.broke_iron_maidens(state) and state.has(iname.heavy_ring,
                                                                                               self.player),
            "Last Keys": self.can_open_ceremonial_door
        }

    def has_ice_or_stone(self, state: CollectionState) -> bool:
        return state.has_any([iname.serpent, iname.cockatrice], self.player) and \
               state.has_any([iname.mercury, iname.mars], self.player)

    def can_touch_water(self, state: CollectionState) -> bool:
        if self.ignore_cleansing:
            return True
        return state.has(iname.cleansing, self.player)

    def broke_iron_maidens(self, state: CollectionState) -> bool:
        if self.break_iron_maidens:
            return True
        return state.has(iname.ironmaidens, self.player)

    def can_open_ceremonial_door(self, state: CollectionState) -> bool:
        if self.required_last_keys:
            return state.has(iname.last_key, self.player, self.required_last_keys)
        return True

    def set_cotm_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            # Set each Entrance's rule if it should have one.
            for entrance in region.entrances:
                ent_rule = get_entrance_info(entrance.name, "rule")
                if ent_rule is not None:
                    entrance.access_rule = self.rules[ent_rule]

            # Set each Location's rule if it should have one.
            for loc in region.locations:
                loc_rule = get_location_info(loc.name, "rule")
                if loc_rule is not None:
                    loc.access_rule = self.rules[loc_rule]
