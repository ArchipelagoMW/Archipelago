from typing import Any

from BaseClasses import ItemClassification

from .parse_data import (
    datapackage_item_groups,
    datapackage_items,
    datapackage_location_groups,
    datapackage_locations,
    effects_prog_lookup,
    hk_locations,
    hk_regions,
    options_pool_mappings,
    structure_transition_to_region_map,
    trando_transitions,
)
from .template_world import RandomizerCoreWorld


class HK2World(RandomizerCoreWorld):
    """
    Proof of concept about a minimal viable implementation of using rando core template world
    off of rando core extracted data
    """
    game = "Hollow Knight 2"
    item_name_to_id = datapackage_items
    location_name_to_id = datapackage_locations
    item_name_groups = datapackage_item_groups
    location_name_groups = datapackage_location_groups
    rc_regions: list[dict[str, Any]] = hk_regions
    rc_locations: list[dict[str, Any]] = hk_locations

    def set_victory(self) -> None:
        """Called at the end of create_regions() to set self.multiworld.completion_condition[self.player]"""
        pass

    def create_rule(self, rule):
        """Used to parse the logic format into an access_rule for Entrances and Locations."""
        return staticmethod(lambda state: True)

    def get_item_list(self) -> list[str]:
        """
        Called by create_items() to get a full list of item names to create for the world.
        Items sould be added to the list multiple times if you need multiple copies,
        and any alterations to the items in the pool based on options should be done here as well.
        """
        return [
            item
            for option, data in options_pool_mappings.items()
            for item in data["randomized"]["items"]
        ]

    def get_item_classification(self, name: str) -> ItemClassification:
        """Used to get the Item Classification by name for every item added to the Multiworld"""
        if name in effects_prog_lookup:
            return ItemClassification.progression
        return ItemClassification.filler

    def create_regions(self):
        super().create_regions()
        ret = {}
        ret["Menu"] = {"Tutorial_01": "Starting Area"}
        for name, trans_data in trando_transitions.items():
            if trans_data["vanilla_target"] is None:
                # is a one-way target
                continue

            region1 = structure_transition_to_region_map[name]
            region2 = structure_transition_to_region_map[trans_data["vanilla_target"]]
            if region1 not in ret:
                ret[region1] = {}
            ret[region1][region2] = name
        for region_name, exits in ret.items():
            self.get_region(region_name).add_exits(exits)
