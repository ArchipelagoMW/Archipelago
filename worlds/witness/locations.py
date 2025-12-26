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

        self.PANEL_TYPES_TO_SHUFFLE = {"General", "Good Boi", "Easter Egg Total"}
        self.CHECK_LOCATIONS = static_witness_locations.GENERAL_LOCATIONS.copy()

        if world.options.shuffle_discarded_panels:
            self.PANEL_TYPES_TO_SHUFFLE.add("Discard")

        if world.options.shuffle_vault_boxes:
            self.PANEL_TYPES_TO_SHUFFLE.add("Vault")

        if world.options.shuffle_EPs == "individual":
            self.PANEL_TYPES_TO_SHUFFLE.add("EP")
        elif world.options.shuffle_EPs == "obelisk_sides":
            self.PANEL_TYPES_TO_SHUFFLE.add("Obelisk Side")

            for obelisk_side_name in static_witness_locations.OBELISK_SIDES:
                obelisk_side_id = static_witness_logic.ENTITIES_BY_NAME[obelisk_side_name].entity_id
                if player_logic.REQUIREMENTS_BY_ENTITY_ID[obelisk_side_id] == frozenset({frozenset()}):
                    self.CHECK_LOCATIONS.discard(obelisk_side_name)

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | player_logic.ADDED_CHECKS

        self.CHECK_LOCATIONS.discard(static_witness_logic.ENTITIES_BY_ID[player_logic.VICTORY_LOCATION].entity_name)

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS - {
            static_witness_logic.ENTITIES_BY_ID[entity_id].entity_name
            for entity_id in player_logic.COMPLETELY_DISABLED_ENTITIES
        }

        self.CHECK_LOCATION_IDS = sorted({
            static_witness_locations.ALL_LOCATIONS_TO_ID[check_name]
            for check_name in self.CHECK_LOCATIONS
            if static_witness_logic.ENTITIES_BY_NAME[check_name].location_type in self.PANEL_TYPES_TO_SHUFFLE
        })

        self.EVENT_LOCATION_TABLE = {
            event_location: None
            for event_location in player_logic.EVENT_ITEM_PAIRS
        }

        check_dict = {
            static_witness_logic.ENTITIES_BY_ID[location_id].entity_name:
            static_witness_logic.ENTITIES_BY_ID[location_id].entity_id
            for location_id in self.CHECK_LOCATION_IDS
        }

        self.CHECK_LOCATION_TABLE = {**self.EVENT_LOCATION_TABLE, **check_dict}

    def add_location_late(self, entity_name: str) -> None:
        entity_id = static_witness_logic.ENTITIES_BY_NAME[entity_name].entity_id
        self.CHECK_LOCATION_TABLE[entity_name] = entity_id
        self.CHECK_LOCATION_IDS = sorted([*self.CHECK_LOCATION_IDS, entity_id])
