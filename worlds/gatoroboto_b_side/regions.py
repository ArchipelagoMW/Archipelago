from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region, CollectionState

if TYPE_CHECKING:
    from .world import GatoRobotoWorld

def create_and_connect_regions(world: GatoRobotoWorld) -> None:
    create_all_regions(world)
    connect_regions(world)
    if world.options.nexus_start:
        world.origin_region_name = "Nexus"


def create_all_regions(world: GatoRobotoWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    landing_site = Region("Landing Site", world.player, world.multiworld)
    nexus = Region("Nexus", world.player, world.multiworld)
    aqueducts = Region("Aqueducts", world.player, world.multiworld)
    heater_core = Region("Heater Core", world.player, world.multiworld)
    ventilation = Region("Ventilation", world.player, world.multiworld)
    incubator = Region("Incubator", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [landing_site, nexus, aqueducts, heater_core, ventilation, incubator]

    world.multiworld.regions += regions


def connect_regions(world: GatoRobotoWorld) -> None:
    landing_site = world.get_region("Landing Site")
    nexus = world.get_region("Nexus")
    aqueducts = world.get_region("Aqueducts")
    heater_core = world.get_region("Heater Core")
    ventilation = world.get_region("Ventilation")
    incubator = world.get_region("Incubator")



    # An even easier way is to use the region.connect helper.
    landing_site.connect(nexus, "Zu Nexus")
    nexus.connect(landing_site, "Zu Landing Site")
    nexus.connect(aqueducts, "Zu Aqueducts")
    nexus.connect(heater_core, "Zu Heater Core")
    if world.options.unlock_all_warps:
        nexus.connect(ventilation, "Zu Ventilation")
    else:
        heater_core.connect(ventilation, "Zu Ventilation")
    nexus.connect(incubator, "Zu Incubator")

    #overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))