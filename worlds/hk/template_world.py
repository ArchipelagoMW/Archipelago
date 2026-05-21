from typing import Any, ClassVar

from BaseClasses import CollectionRule, Item, ItemClassification, Location, Region
from rule_builder.rules import Rule
from worlds.AutoWorld import World


class RandomizerCoreWorld(World):
    rc_regions: ClassVar[list[dict[str, Any]]] = {}
    rc_locations: ClassVar[list[dict[str, Any]]] = {}
    rule_lookup: ClassVar[dict[str, Any]] = {}
    item_class = Item
    location_class = Location
    region_class = Region

# # black box methods
    def set_victory(self) -> None:
        """Called at the end of create_regions() to set self.multiworld.completion_condition[self.player]"""
        pass

    def create_rule(self, rule: Any) -> CollectionRule | Rule:
        """Used to parse the logic format into an access_rule for Entrances and Locations."""
        return staticmethod(lambda state: True)

    def get_item_list(self) -> list[str]:
        """
        Called by create_items() to get a full list of item names to create for the world.
        Items sould be added to the list multiple times if you need multiple copies,
        and any alterations to the items in the pool based on options should be done here as well.
        """
        return []

    def get_item_classification(self, name: str) -> ItemClassification:
        """Used to get the Item Classification by name for every item added to the Multiworld"""
        return ItemClassification.progression

# common methods
    def get_region_list(self) -> list[str]:
        """Base implementation of region data for use in create_regions"""
        return [region["name"] for region in self.rc_regions]

    def get_connections(self) -> list[tuple[str, str, Any | None]]:
        """Base implementation of region connection data for use in create_regions"""
        return [
            (region["name"], exit["target"], exit["logic"])
            for region in self.rc_regions for exit in region["exits"]
            ]

    def get_location_map(self) -> dict[str, dict[str, int | None]]:
        """Base implementation of location-region mapping data for use in create_regions"""
        return {
            region["name"]: {
                location: self.location_name_to_id.get(location, None)
                for location in region["locations"]
                }
            for region in self.rc_regions
            }

    def create_regions(self) -> None:
        # create a local map of get_region_list names to region object for referencing in create_regions
        # and adding those regions to the multiworld
        regions = dict.fromkeys(self.get_region_list(), None)
        for region in regions.keys():
            regions[region] = self.region_class(region, self.player, self.multiworld)
            self.multiworld.regions.append(regions[region])

        # loop through get_region_map, adding the rules per self.create_rule(rule) if present to the connections
        for region1, region2, rule in self.get_connections():
            ent = regions[region1].connect(regions[region2])
            if rule:
                self.set_rule(ent, self.create_rule(rule))

        # loop through get_location_map, adding the rules per self.create_rule(rule) if present to the location
        for region, placements in self.get_location_map().items():
            regions[region].add_locations(placements, self.location_class)
            for location_name, location_id in placements.items():
                loc = self.get_location(location_name)
                if location_name in self.rule_lookup:
                    self.set_rule(loc, self.create_rule(self.rule_lookup[location_name]))

                if not location_id:
                    loc.place_locked_item(
                        self.item_class(location_name, ItemClassification.progression, None, self.player))
                    loc.show_in_spoiler = False

        self.set_victory()

    # unneeded now with rulebuilder's world.set_rule
    # def set_rule(self, spot: Location | Entrance, rule: CollectionRule | Rule[Any]) -> None:
    #     """override for alternative access_rule formats"""
    #     spot.access_rule = rule

    def set_rules(self):
        pass

    def create_items(self) -> int:
        # create all items in get_item_list()
        itempool = [self.create_item(item) for item in self.get_item_list()]

        # fill in any difference in itempool with filler item and submit to multiworld
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        while len(itempool) < total_locations:
            itempool.append(self.create_filler())
        self.multiworld.itempool += itempool
        return len(itempool)

    def create_item(self, name: str) -> "Item":
        classification = self.get_item_classification(name)
        return self.item_class(name, classification, self.item_name_to_id.get(name, None), self.player)
