from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule, CollectionRule

from .Items import get_event_item_name
from .Locations import unlock_location_list

if TYPE_CHECKING:
    from . import A1800World


def _has(player: int, *requirements: str) -> CollectionRule:
    return lambda state: all(state.has(get_event_item_name(requirement), player) for requirement in requirements)


class _Rules:
    def __init__(self, world: "A1800World") -> None:
        self.world = world

    def create_rule(self, location_name: str, *requirements: str) -> None:
        set_rule(self.world.multiworld.get_location(location_name,
                 self.world.player), _has(self.world.player, f"Unlock: {location_name}", *requirements))


def set_rules(world: "A1800World") -> None:
    rules = _Rules(world)

    for data in unlock_location_list:
        if "Farmer" in data.name:
            rules.create_rule(data.name, "Farmers")
        elif "Worker" in data.name:
            rules.create_rule(data.name, "Workers")
        elif "Artisan" in data.name:
            rules.create_rule(data.name, "Artisans")

    rules.create_rule("OW: Marketplace", "Timber")
    rules.create_rule("OW: Farmer Residence")  # No requirement for timber to avoid circular logic
    rules.create_rule("OW: Lumberjack's Hut", "Farmers")
    rules.create_rule("OW: Sawmill", "Farmers", "Wood")
    rules.create_rule("OW: Fishery", "Farmers", "Timber")
    rules.create_rule("OW: Sheep Farm", "Farmers", "Timber")
    rules.create_rule("OW: Framework Knitters", "Farmers", "Timber", "Wool")
    rules.create_rule("OW: Potato Farm", "Farmers", "Timber")
    rules.create_rule("OW: Schnapps Distillery", "Farmers", "Timber", "Potatoes")
    rules.create_rule("OW: Worker Residence", "Timber", "Market", "Fish", "Work Clothes")
    rules.create_rule("OW: Fire Station", "Timber")
    rules.create_rule("OW: Pub", "Timber")
    rules.create_rule("OW: Clay Pit", "Workers", "Timber")
    rules.create_rule("OW: Brick Factory", "Workers", "Timber", "Clay")
    rules.create_rule("OW: Pig Farm", "Farmers", "Timber")
    rules.create_rule("OW: Slaughterhouse", "Workers", "Timber", "Bricks", "Pigs")
    rules.create_rule("OW: Grain Farm", "Farmers", "Timber")
    rules.create_rule("OW: Flour Mill", "Farmers", "Timber", "Bricks", "Grain")
    rules.create_rule("OW: Bakery", "Workers", "Timber", "Bricks", "Flour")
    rules.create_rule("OW: Church", "Timber", "Bricks")
    rules.create_rule("OW: Sailmakers", "Workers", "Timber", "Bricks", "Wool")
    rules.create_rule("OW: Sailing Shipyard", "Workers", "Timber", "Bricks", "Sails")
    rules.create_rule("OW: Charcoal Kiln", "Workers", "Timber", "Bricks")
    rules.create_rule("OW: Iron Mine", "Workers", "Timber", "Bricks")
    rules.create_rule("OW: Furnace", "Workers", "Timber", "Bricks", "Coal", "Iron")
    rules.create_rule("OW: Steelworks", "Workers", "Timber", "Bricks", "Steel")
    rules.create_rule("OW: Rendering Works", "Workers", "Timber", "Bricks", "Steel Beams", "Pigs")
    rules.create_rule("OW: Soap Factory", "Workers", "Timber", "Bricks", "Steel Beams", "Tallow")
    rules.create_rule("OW: Weapon Factory", "Workers", "Timber", "Bricks", "Steel Beams", "Steel")
    rules.create_rule("OW: Hop Farm", "Farmers", "Timber")
    rules.create_rule("OW: Malthouse", "Workers", "Timber", "Bricks", "Steel Beams", "Grain")
    rules.create_rule("OW: Brewery", "Workers", "Timber", "Bricks", "Steel Beams", "Hops", "Malt")
    rules.create_rule("OW: Police Station", "Timber", "Bricks")
    rules.create_rule("OW: School", "Timber", "Bricks", "Steel Beams")
    rules.create_rule("OW: Artisan Residence", "Timber", "Bricks", "Steel Beams", "Market", "Fish", "Work Clothes",
                      "Sausages", "Bread", "Soap", "School")
    rules.create_rule("Victory Condition", "Artisans")

    world.multiworld.completion_condition[world.player] = _has(world.player, "Victory")
