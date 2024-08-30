"""
Defines constants for different types of locations in the game
"""
from typing import TYPE_CHECKING

from .data import static_locations as static_witness_locations
from .data import static_logic as static_witness_logic
from .player_logic import WitnessPlayerLogic

if TYPE_CHECKING:
    from . import WitnessWorld


class WitnessPlayerLocations:
    """
    Class that defines locations for a single player
    """

    def __init__(self, world: "WitnessWorld", player_logic: WitnessPlayerLogic) -> None:
        """Defines locations AFTER logic changes due to options"""

        self.PANEL_TYPES_TO_SHUFFLE = {"General", "Good Boi"}
        self.CHECK_LOCATIONS = static_witness_locations.GENERAL_LOCATIONS.copy()

        if world.options.shuffle_discarded_panels:
            self.PANEL_TYPES_TO_SHUFFLE.add("Discard")

        if world.options.shuffle_vault_boxes:
            self.PANEL_TYPES_TO_SHUFFLE.add("Vault")

        if world.options.shuffle_EPs == "individual":
            self.PANEL_TYPES_TO_SHUFFLE.add("EP")
        elif world.options.shuffle_EPs == "obelisk_sides":
            self.PANEL_TYPES_TO_SHUFFLE.add("Obelisk Side")

            for obelisk_loc in static_witness_locations.OBELISK_SIDES:
                obelisk_loc_hex = static_witness_logic.ENTITIES_BY_NAME[obelisk_loc]["entity_hex"]
                if player_logic.REQUIREMENTS_BY_HEX[obelisk_loc_hex] == frozenset({frozenset()}):
                    self.CHECK_LOCATIONS.discard(obelisk_loc)

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | player_logic.ADDED_CHECKS

        self.CHECK_LOCATIONS.discard(static_witness_logic.ENTITIES_BY_HEX[player_logic.VICTORY_LOCATION]["checkName"])

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS - {
            static_witness_logic.ENTITIES_BY_HEX[entity_hex]["checkName"]
            for entity_hex in player_logic.COMPLETELY_DISABLED_ENTITIES
        }

        self.CHECK_PANELHEX_TO_ID = {
            static_witness_logic.ENTITIES_BY_NAME[ch]["entity_hex"]: static_witness_locations.ALL_LOCATIONS_TO_ID[ch]
            for ch in self.CHECK_LOCATIONS
            if static_witness_logic.ENTITIES_BY_NAME[ch]["locationType"] in self.PANEL_TYPES_TO_SHUFFLE
        }

        self.CHECK_PANELHEX_TO_ID = dict(
            sorted(self.CHECK_PANELHEX_TO_ID.items(), key=lambda item: item[1])
        )

        self.EVENT_LOCATION_TABLE = {
            event_location: None
            for event_location in player_logic.EVENT_ITEM_PAIRS
        }

        check_dict = {
            static_witness_logic.ENTITIES_BY_HEX[location]["checkName"]:
            static_witness_locations.get_id(static_witness_logic.ENTITIES_BY_HEX[location]["entity_hex"])
            for location in self.CHECK_PANELHEX_TO_ID
        }

        self.CHECK_LOCATION_TABLE = {**self.EVENT_LOCATION_TABLE, **check_dict}

    def add_location_late(self, entity_name: str) -> None:
        entity_hex = static_witness_logic.ENTITIES_BY_NAME[entity_name]["entity_hex"]
        self.CHECK_LOCATION_TABLE[entity_hex] = static_witness_locations.get_id(entity_hex)
        self.CHECK_PANELHEX_TO_ID[entity_hex] = static_witness_locations.get_id(entity_hex)
