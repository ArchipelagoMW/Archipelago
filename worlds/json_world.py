from BaseClasses import CollectionRule, Item, ItemClassification, Location, Region  # Tutorial
from worlds.AutoWorld import World  # WebWorld
from rule_builder.rules import Rule, Or, HasAll

def build_item_datapackage(data) -> dict[str, int]:
    format = data.get("formats", {}).get("item_name_to_id", "explicit")
    if format == "explicit":
        return data["item_name_to_id"]
    raise Exception("unknown format type")


def build_location_datapackage(data) -> dict[str, int]:
    format = data.get("formats", {}).get("location_name_to_id", "explicit")
    if format == "explicit":
        return data["location_name_to_id"]
    raise Exception("unknown format type")


def build_item_groups(data) -> dict[str, int]:
    format = data.get("formats", {}).get("item_groups", "explicit")
    if format == "explicit":
        if "item_name_groups" not in data:
            return {}
        return {group: set(items) for group, items in data["item_name_groups"].items()}
    raise Exception("unknown format type")


def build_location_groups(data) -> dict[str, int]:
    format = data.get("formats", {}).get("location_name_groups", "explicit")
    if format == "explicit":
        if "location_name_groups" not in data:
            return {}
        return {group: set(locations) for group, locations in data["location_name_groups"].items()}
    raise Exception("unknown format type")


def build_region_list(data) -> list[str]:
    format = data.get("formats", {}).get("region_list", "explicit")
    if format == "explicit":
        return data["region_list"]
    if format == "region_map":
        region_set = set(data["region_map"].keys())
        for regions in data["region_map"].values():
            region_set.update(regions.keys())
        return sorted(region_set)
    raise Exception("unknown format type")


def create_rule(rule_data, rule_format) -> Rule | None:
    if rule_data is None:
        return None
    if rule_format == "dnf_items":
        return Or(*[HasAll(*inner) for inner in rule_data])
    raise Exception("unknown format type")


def build_region_map(data) -> dict[str, dict[str, Rule | None]]:
    format = data.get("formats", {}).get("region_map", "explicit")
    rule_format = data.get("formats", {}).get("rule", "dnf_items")
    if format == "explicit":
        return {region: {target: create_rule(rule_data, rule_format) for target, rule_data in entrance_data.items()}
                for region, entrance_data in data["region_map"].items()}
    raise Exception("unknown format type")


def build_location_map(data) -> dict[str, dict[str, Rule | None]]:
    format = data.get("formats", {}).get("location_map", "explicit")
    rule_format = data.get("formats", {}).get("rule", "dnf_items")
    if format == "explicit":
        return {region: {target: create_rule(rule_data, rule_format) for target, rule_data in entrance_data.items()}
                for region, entrance_data in data["location_map"].items()}
    raise Exception("unknown format type")


def build_event_map(data) -> dict[str, tuple[str, str, Rule | None]]:
    format = data.get("formats", {}).get("event_map", None)
    if format is None:
        return {}
    if format == "explicit":
        return {region: tuple(data) for region, data in data["event_map"]}
    raise Exception("unknown format type")


def build_item_list(data) -> list[str]:
    format = data.get("formats", {}).get("item_list", "explicit")
    if format == "explicit":
        return data["item_list"]
    if format == "counter":
        return [item for item, count in data["item_count"] for _ in range(count)]
    raise Exception("unknown format type")


def build_completion_rule(data) -> Rule:
    rule_format = data.get("formats", {}).get("rule", "dnf_items")
    if data["completion_rule"] is None:
        raise Exception("empty completion rule is not supported")
    return create_rule(data["completion_rule"], rule_format)


def build_classification_lookup(data) -> dict[str, ItemClassification]:
    format = data.get("formats", {}).get("classification_lookup", "explicit")
    if format == "explicit":
        return {key: getattr(ItemClassification, value) for key, value in data["classification_lookup"].items()}
    if format == "reverse_lookup":
        return {item: getattr(ItemClassification, classification) for classification, items in data["classification_lookup"].items() for item in items}
    raise Exception("unknown format type")


def build_filler_weights(data) -> dict[str, ItemClassification]:
    format = data.get("formats", {}).get("filler_weights", "explicit")
    if format == "explicit":
        return data["filler_weights"]
    if format == "single":
        return {data["filler_item"]: 1}
    raise Exception("unknown format type")


class JsonWorld(World):
    item_class: Item
    location_class: Location

    region_list: list[str]
    region_map: dict[str, dict[str, Rule | None]]
    location_map: dict[str, dict[str, Rule | None]]
    item_list: list[str]
    completion_rule: Rule

    classification_lookup: dict[str, ItemClassification]
    filler_weights: dict[str, int]

    @classmethod
    def from_json(cls, data):
        game_name = data["game_name"]
        description = data["description"]

        class JsonItem(Item):
            game = game_name
        class JsonLocation(Location):
            game = game_name

        # only need to define the class, the metaclass registers it for use later
        type(f"json_world_{game_name}", (JsonWorld,), {
            "__doc__": description,
            "game": game_name,
            # "web": WebWorld,
            "item_name_to_id": build_item_datapackage(data),
            "location_name_to_id": build_location_datapackage(data),
            "item_name_groups": build_item_groups(data),
            "location_name_groups": build_location_groups(data),

            "item_class": JsonItem,
            "location_class": JsonLocation,

            "region_list": build_region_list(data),
            "region_map": build_region_map(data),
            "location_map": build_location_map(data),
            # "event_map": dict[name, list[tuple[str, str, Rule | None]]]
            "item_list": build_item_list(data),
            "completion_rule": build_completion_rule(data),

            "classification_lookup": build_classification_lookup(data),
            "filler_weights": build_filler_weights(data),
        })

    # common World methods
    def create_regions(self) -> None:
        regions = {
            name: Region(name, self.player, self.multiworld)
            for name in self.region_list}
        self.multiworld.regions.extend(regions.values())

        # loop through region_map, letting add_exits add rules if present
        for region, connections in self.region_map.items():
            regions[region].add_exits(connections.keys(), connections)

        # loop through location_map, adding the rules if present to the location
        for region, placements in self.location_map.items():
            for location, rule in placements.items():
                loc = self.location_class(self.player, location, self.location_name_to_id[location], regions[region])
                if rule is not None:
                    self.set_rule(loc, rule)
                regions[region].locations.append(loc)

        for region, (location, item, rule) in self.event_map.items():
            regions[region].add_event(location, item, rule, self.location_class, self.item_class)

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
