from BaseClasses import Region
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import FaxanaduWorld


def create_region(name, player, multiworld):
    region = Region(name, player, multiworld)
    multiworld.regions.append(region)
    return region


def create_regions(faxanadu_world: "FaxanaduWorld"):
    player = faxanadu_world.player
    multiworld = faxanadu_world.multiworld

    # Create regions
    menu = create_region("Menu", player, multiworld)
    eolis = create_region("Eolis", player, multiworld)
    path_to_apolune = create_region("Path to Apolune", player, multiworld)
    apolune = create_region("Apolune", player, multiworld)
    create_region("Tower of Trunk", player, multiworld)
    path_to_forepaw = create_region("Path to Forepaw", player, multiworld)
    forepaw = create_region("Forepaw", player, multiworld)
    trunk = create_region("Trunk", player, multiworld)
    create_region("Joker Spring", player, multiworld)
    create_region("Tower of Fortress", player, multiworld)
    path_to_mascon = create_region("Path to Mascon", player, multiworld)
    create_region("Tower of Red Potion", player, multiworld)
    mascon = create_region("Mascon", player, multiworld)
    path_to_victim = create_region("Path to Victim", player, multiworld)
    create_region("Tower of Suffer", player, multiworld)
    victim = create_region("Victim", player, multiworld)
    mist = create_region("Mist", player, multiworld)
    create_region("Useless Tower", player, multiworld)
    create_region("Tower of Mist", player, multiworld)
    path_to_conflate = create_region("Path to Conflate", player, multiworld)
    create_region("Helm Branch", player, multiworld)
    create_region("Conflate", player, multiworld)
    branches = create_region("Branches", player, multiworld)
    path_to_daybreak = create_region("Path to Daybreak", player, multiworld)
    daybreak = create_region("Daybreak", player, multiworld)
    dartmoor_castle = create_region("Dartmoor Castle", player, multiworld)
    create_region("Dartmoor", player, multiworld)
    create_region("Fraternal Castle", player, multiworld)
    create_region("Evil Fortress", player, multiworld)

    # Create connections
    menu.add_exits(["Eolis"])
    eolis.add_exits(["Path to Apolune"])
    path_to_apolune.add_exits(["Apolune"])
    apolune.add_exits(["Tower of Trunk", "Path to Forepaw"])
    path_to_forepaw.add_exits(["Forepaw"])
    forepaw.add_exits(["Trunk"])
    trunk.add_exits(["Joker Spring", "Tower of Fortress", "Path to Mascon"])
    path_to_mascon.add_exits(["Tower of Red Potion", "Mascon"])
    mascon.add_exits(["Path to Victim"])
    path_to_victim.add_exits(["Tower of Suffer", "Victim"])
    victim.add_exits(["Mist"])
    mist.add_exits(["Useless Tower", "Tower of Mist", "Path to Conflate"])
    path_to_conflate.add_exits(["Helm Branch", "Conflate", "Branches"])
    branches.add_exits(["Path to Daybreak"])
    path_to_daybreak.add_exits(["Daybreak"])
    daybreak.add_exits(["Dartmoor Castle"])
    dartmoor_castle.add_exits(["Dartmoor", "Fraternal Castle", "Evil Fortress"])
