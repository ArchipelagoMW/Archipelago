from BaseClasses import Region, Location, Item, ItemClassification, Tutorial, CollectionRule
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import (
    Component,
    components,
    Type as component_type,
    )
from collections import defaultdict
from rule_builder.rules import Rule, Or, HasAll, Has

## flatten lists of locations and items so they are indexed for name_to_id
#location_list = [location for locations in json_world["location_map"].values() for location in locations.keys()]
#item_list = [item for item_lists in json_world["items"].values() for item in item_lists]


class JsonWorld(World):
    item_class: Item
    location_class: Location

    region_list: list[str]
    region_connections: dict[str, dict[str, CollectionRule | Rule | None]]
    location_map: dict[str, dict[str, CollectionRule | Rule | None]]
    item_list: list[str]
    completion_rule: CollectionRule | Rule

    classification_lookup: dict[str, ItemClassification]
    filler_weights: dict[str, int]

    @classmethod
    def from_json(cls, data):
        game_name = data["game_name"]
        description = data["description"]

        item_name_to_id = data["item_name_to_id"]
        location_name_to_id = data["location_name_to_id"]

        region_set = set(data["region_map"].keys())
        for regions in data["region_map"].values():
            region_set.update(regions.keys())
        region_list = list(region_set)
        region_connections = {
            region: {
                target: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for target, rule in mapping.items()
            }
            for region, mapping in data["region_map"].items()
        }
        location_map = {
            region: {
                location: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for location, rule in mapping.items()
            }
            for region, mapping in data["location_map"].items()
        }
        item_list = data["items"]["prog_items"]
        item_list.extend(data["items"]["filler_items"])
        completion_rule = Or(*[HasAll(*inner) for inner in data["completion_rule"]])

        classification_lookup = {
            **{n: ItemClassification.progression for n in data["items"]["prog_items"]},
            **{n: ItemClassification.filler for n in data["items"]["filler_items"]}
        }
        filler_weights = {data["filler_name"]: 1}

        class JsonItem(Item):
            game = game_name
        class JsonLocation(Location):
            game = game_name

        # only need to define the class, the metaclass registers it for use later
        type(f"json_world_{game_name}", (JsonWorld,), {
            "__doc__": description,
            "game": game_name,
            # "web": WebWorld,
            "item_name_to_id": item_name_to_id,
            "location_name_to_id": location_name_to_id,
            # "item_name_groups": dict[str, set[str, ...]]
            # "location_name_groups": dict[str, set[str, ...]]

            "item_class": JsonItem,
            "location_class": JsonLocation,

            "region_list": region_list,
            "region_connections": region_connections,
            "location_map": location_map,
            # "event_map": dict[name, list[tuple[str, str, CollectionRule | Rule | None]]]
            "item_list": item_list,
            "completion_rule": completion_rule,

            "classification_lookup": classification_lookup,
            "filler_weights": filler_weights,
        })

# basic getters for json_world data, any option based modifications can be done here; may cache these later
# expect authors to modify the return of super() per options, or fully override if their format is different
    def get_region_list(self) -> list[str]:
        """
        Parser method to return the list of all regions to be created.
        Currently flattens region_map to create all regions with a connection in or out
        """
        ret = {
            r for connections in json_world["region_map"].values()
            for r in connections.keys()
        }.union(json_world["region_map"].keys())
        return ret

    def get_connections(self) -> dict[str, dict[str, Rule | None]]:
        """
        Parser method to convert the region definitions in the json_world object
        into a dict of connection entries formatted as {parent_region_name: {target_region_name: rule}}
        """
        return {
            region1: {
                region2: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for region2, rule in connections.items()
                }
            for region1, connections in json_world["region_map"].items()
        }

    def get_location_map(self) -> dict[str, dict[str, Rule | None]]:
        """
        Parser method to convert the location definitions in the json_world object
        into a list of location entries formatted as {parent_region_name: {location_name: rule}}
        """
        return {
            region: {
                location: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for location, rule in placements.items()
                }
            for region, placements in json_world["location_map"].items()
        }

    # common World methods
    def create_regions(self) -> None:
        # create a local map of get_region_list names to region object
        # for referencing in create_regions and adding those regions to the multiworld
        regions = {
            name: Region(name, self.player, self.multiworld)
            for name in self.region_list}
        self.multiworld.regions.extend(regions.values())

        # loop through get_region_map, letting add_exits add rules if present
        for region, connections in self.region_connections.items():
            regions[region].add_exits(connections.keys(), connections)

        # loop through get_location_map, adding the rules if present to the location
        for region, placements in self.location_map.items():
            for location, rule in placements.items():
                loc = self.location_class(self.player, location, self.location_name_to_id[location], regions[region])
                if rule is not None:
                    self.set_rule(loc, rule)
                regions[region].locations.append(loc)

    def create_items(self) -> None:
        # create all items in item_list
        itempool = [self.create_item(item) for item in self.item_list]

        # fill in any difference in itempool with filler item and submit to multiworld
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        missing_items = total_locations - len(itempool)
        if missing_items > 0:
            itempool += [self.create_filler() for _ in range(missing_items)]
        elif missing_items < 0:
            raise Exception(f"Too many items were defined for the location pool. for game {self.game} slot {self.player}")
        self.multiworld.itempool += itempool

    def set_rules(self):
        self.set_completion_rule(self.completion_rule)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(self.filler_weights.keys()), self.filler_weights.values(), k=1)[0]

    def create_item(self, name: str) -> Item:
        return self.item_class(
            name,
            self.classification_lookup.get(name, ItemClassification.filler),
            self.item_name_to_id.get(name, None),
            self.player)
