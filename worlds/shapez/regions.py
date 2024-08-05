from typing import Callable

from BaseClasses import Entrance, Region, CollectionState
from . import ShapezWorld
from .locations import ShapezLocation

all_regions = {
    "Main",
    "Levels with 1 Building",
    "Levels with 2 Buildings",
    "Levels with 3 Buildings",
    "Levels with 4 Buildings",
    "Levels with 5 Buildings",
    "Upgrades Tier II",
    "Upgrades with 1 Building",
    "Upgrades with 2 Buildings",
    "Upgrades with 3 Buildings",
    "Upgrades with 4 Buildings",
    "Upgrades with 5 Buildings",
    "Cut Shape Achievements",
    "Rotated Shape Achievements",
    "Stacked Shape Achievements",
    "Painted Shape Achievements",
    "Stored Shape Achievements",
    "Trashed Shape Achievements",
    "Wiring Achievements",
    "All Buildings Shapes"
}


class ShapezRegion(Region):
    """Don't know why I need to create this class"""


def create_entrance(player: int, name: str, parent: Region, connects: Region, rule: Callable[[CollectionState], bool]):
    entr = Entrance(player, name, parent)
    entr.connected_region = connects
    entr.access_rule = rule
    parent.exits.append(entr)
    connects.entrances.append(entr)


def create_shapez_regions(world: ShapezWorld) -> list[ShapezRegion]:
    regions = {name: ShapezRegion(name, world.player, world.multiworld) for name in all_regions}

    # Creates ShapezLocations for every included location and puts them into the correct region
    for name, data in world.included_locations.items():
        regions[data[0]].locations += ShapezLocation(world.player, name, world.location_name_to_id[name], regions[data[0]], data[1])

    # Delete unused regions
    for name, region in regions.items():
        if len(region.locations) == 0:
            regions.pop(name)

    # Create Entrances for regions
    create_entrance(world.player, "Cutter needed", regions["Main"], regions["Cut Shape Achievements"],
                    lambda state: state.has("Cutter", world.player))
    create_entrance(world.player, "Rotator needed", regions["Main"], regions["Rotated Shape Achievements"],
                    lambda state: state.has("Rotator", world.player))
    create_entrance(world.player, "Stacker needed", regions["Main"], regions["Stacked Shape Achievements"],
                    lambda state: state.has("Stacker", world.player))
    create_entrance(world.player, "Painter needed", regions["Main"], regions["Painted Shape Achievements"],
                    lambda state: state.has("Painter", world.player))
    create_entrance(world.player, "Storage needed", regions["Main"], regions["Stored Shape Achievements"],
                    lambda state: state.has("Storage", world.player))
    create_entrance(world.player, "Trash needed", regions["Main"], regions["Trashed Shape Achievements"],
                    lambda state: state.has("Trash", world.player))
    create_entrance(world.player, "Wires needed", regions["Main"], regions["Wiring Achievements"],
                    lambda state: state.has("Wires", world.player))
    create_entrance(world.player, "More than cutter needed",
                    regions["Cut Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Stacker", "Painter", "Color Mixer"], world.player))
    create_entrance(world.player, "More than rotator needed",
                    regions["Rotated Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Cutter", "Stacker", "Painter", "Color Mixer"], world.player))
    create_entrance(world.player, "More than stacker needed",
                    regions["Stacked Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Cutter", "Painter", "Color Mixer"], world.player))
    create_entrance(world.player, "More than painter needed",
                    regions["Painted Shape Achievements"], regions["All Buildings Shapes"],
                    lambda state: state.has_all(["Rotator", "Stacker", "Cutter", "Color Mixer"], world.player))
    create_entrance(world.player, "Upgrades Access",
                    regions["Main"], regions["Upgrades Tier II"],
                    lambda state: state.has("Upgrades", world.player))

    level_logic = world.options.randomize_level_logic.value
    upgrade_logic = world.options.randomize_upgrade_logic.value
    if level_logic < 4: # if not hardcore
        create_entrance(world.player, "First level building needed",
                        regions["Main"], regions["Levels with 1 Building"],
                        lambda state: state.has(world.level_logic[0], world.player))
        create_entrance(world.player, "Second level building needed",
                        regions["Levels with 1 Building"], regions["Levels with 2 Buildings"],
                        lambda state: state.has(world.level_logic[1], world.player))
        create_entrance(world.player, "Third level building needed",
                        regions["Levels with 2 Buildings"], regions["Levels with 3 Buildings"],
                        lambda state: state.has(world.level_logic[2], world.player))
        create_entrance(world.player, "Fourth level building needed",
                        regions["Levels with 3 Buildings"], regions["Levels with 4 Buildings"],
                        lambda state: state.has(world.level_logic[3], world.player))
        create_entrance(world.player, "Fifth level building needed",
                        regions["Levels with 4 Buildings"], regions["Levels with 5 Buildings"],
                        lambda state: state.has(world.level_logic[4], world.player))
    else:
        create_entrance(world.player, "All level buildings needed",
                        regions["Main"], regions["Levels with 5 Buildings"],
                        lambda state: state.has_all(world.level_logic, world.player))
    if upgrade_logic == 0:
        create_entrance(world.player, "First 3 upgrade buildings needed",
                        regions["Upgrades Tier II"], regions["Upgrades with 3 Buildings"],
                        lambda state: state.has_all(world.upgrade_logic[:3], world.player))
        create_entrance(world.player, "All upgrade buildings needed",
                        regions["Upgrades with 3 Buildings"], regions["Upgrades with 5 Buildings"],
                        lambda state: state.has_all(world.upgrade_logic[3:], world.player))
    elif upgrade_logic == 1:
        create_entrance(world.player, "First upgrade building needed",
                        regions["Upgrades Tier II"], regions["Upgrades with 1 Building"],
                        lambda state: state.has(world.upgrade_logic[0], world.player))
        create_entrance(world.player, "Second upgrade building needed",
                        regions["Upgrades with 1 Building"], regions["Upgrades with 2 Buildings"],
                        lambda state: state.has(world.upgrade_logic[1], world.player))
        create_entrance(world.player, "Third upgrade building needed",
                        regions["Upgrades with 2 Buildings"], regions["Upgrades with 3 Buildings"],
                        lambda state: state.has(world.upgrade_logic[2], world.player))
        create_entrance(world.player, "Fourth upgrade building needed",
                        regions["Upgrades with 3 Buildings"], regions["Upgrades with 4 Buildings"],
                        lambda state: state.has(world.upgrade_logic[3], world.player))
        create_entrance(world.player, "Fifth upgrade building needed",
                        regions["Upgrades with 4 Buildings"], regions["Upgrades with 5 Buildings"],
                        lambda state: state.has(world.upgrade_logic[4], world.player))
    else:
        create_entrance(world.player, "All upgrade buildings needed",
                        regions["Upgrades Tier II"], regions["Upgrades with 5 Buildings"],
                        lambda state: state.has_all(world.upgrade_logic, world.player))

    return list(regions.values())
