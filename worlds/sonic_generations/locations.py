from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items, names, regions

if TYPE_CHECKING:
    from .world import SonicGensWorld

LOCATION_NAME_TO_ID = {
    names.Locations.EGreen:     1,
    names.Locations.EPurple:    2,
    names.Locations.EBlue:      3,
    names.Locations.EYellow:    4,
    names.Locations.ERed:       5,
    names.Locations.ECyan:      6,
    names.Locations.EWhite:     7,

    names.Locations.BKGHZ:      50,
    names.Locations.BKCPZ:      51,
    names.Locations.BKSSZ:      52,
    names.Locations.BKSPH:      53,
    names.Locations.BKCTE:      54,
    names.Locations.BKSSH:      55,
    names.Locations.BKCSC:      56,
    names.Locations.BKEUC:      57,
    names.Locations.BKPLA:      58,

    names.Locations.ClearGHZ1:  100,
    names.Locations.ClearGHZ2:  101,
    names.Locations.ClearCPZ1:  102,
    names.Locations.ClearCPZ2:  103,
    names.Locations.ClearSSZ1:  104,
    names.Locations.ClearSSZ2:  105,
    names.Locations.ClearSPH1:  106,
    names.Locations.ClearSPH2:  107,
    names.Locations.ClearCTE1:  108,
    names.Locations.ClearCTE2:  109,
    names.Locations.ClearSSH1:  110,
    names.Locations.ClearSSH2:  111,
    names.Locations.ClearCSC1:  112,
    names.Locations.ClearCSC2:  113,
    names.Locations.ClearEUC1:  114,
    names.Locations.ClearEUC2:  115,
    names.Locations.ClearPLA1:  116,
    names.Locations.ClearPLA2:  117,
    names.Locations.ClearBMS:   118,
    names.Locations.ClearBSD:   119,
    names.Locations.ClearBSL:   120,
    names.Locations.ClearBDE:   121,
    names.Locations.ClearBPC:   122,
    names.Locations.ClearBNE:   123,
    names.Locations.ClearBLB:   124
}

def get_location_names_with_ids(locations: list[str]) -> dict[str, int | None]:
    return {name: LOCATION_NAME_TO_ID[name] for name in locations}

class SonicGensLocation(Location):
    game = names.GameName

def create_all_locations(world: SonicGensWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: SonicGensWorld) -> None:
    world.get_region(names.Regions.WSClassic).add_locations(get_location_names_with_ids([names.Locations.EPurple, names.Locations.EGreen, names.Locations.BKGHZ, names.Locations.BKCPZ, names.Locations.BKSSZ]), SonicGensLocation)
    world.get_region(names.Regions.WSDreamcast).add_locations(get_location_names_with_ids([names.Locations.EYellow, names.Locations.EBlue, names.Locations.BKSPH, names.Locations.BKCTE, names.Locations.BKSSH]), SonicGensLocation)
    world.get_region(names.Regions.WSModern).add_locations(get_location_names_with_ids([names.Locations.EWhite, names.Locations.ECyan, names.Locations.ERed, names.Locations.BKCSC, names.Locations.BKEUC, names.Locations.BKPLA]), SonicGensLocation)
    
    world.get_region(names.Regions.GHZ1).add_locations(get_location_names_with_ids([names.Locations.ClearGHZ1]), SonicGensLocation)
    world.get_region(names.Regions.GHZ2).add_locations(get_location_names_with_ids([names.Locations.ClearGHZ2]), SonicGensLocation)
    world.get_region(names.Regions.CPZ1).add_locations(get_location_names_with_ids([names.Locations.ClearCPZ1]), SonicGensLocation)
    world.get_region(names.Regions.CPZ2).add_locations(get_location_names_with_ids([names.Locations.ClearCPZ2]), SonicGensLocation)
    world.get_region(names.Regions.SSZ1).add_locations(get_location_names_with_ids([names.Locations.ClearSSZ1]), SonicGensLocation)
    world.get_region(names.Regions.SSZ2).add_locations(get_location_names_with_ids([names.Locations.ClearSSZ2]), SonicGensLocation)
    world.get_region(names.Regions.BMS).add_locations(get_location_names_with_ids([names.Locations.ClearBMS]), SonicGensLocation)
    world.get_region(names.Regions.BDE).add_locations(get_location_names_with_ids([names.Locations.ClearBDE]), SonicGensLocation)
    world.get_region(names.Regions.SPH1).add_locations(get_location_names_with_ids([names.Locations.ClearSPH1]), SonicGensLocation)
    world.get_region(names.Regions.SPH2).add_locations(get_location_names_with_ids([names.Locations.ClearSPH2]), SonicGensLocation)
    world.get_region(names.Regions.CTE1).add_locations(get_location_names_with_ids([names.Locations.ClearCTE1]), SonicGensLocation)
    world.get_region(names.Regions.CTE2).add_locations(get_location_names_with_ids([names.Locations.ClearCTE2]), SonicGensLocation)
    world.get_region(names.Regions.SSH1).add_locations(get_location_names_with_ids([names.Locations.ClearSSH1]), SonicGensLocation)
    world.get_region(names.Regions.SSH2).add_locations(get_location_names_with_ids([names.Locations.ClearSSH2]), SonicGensLocation)
    world.get_region(names.Regions.BSD).add_locations(get_location_names_with_ids([names.Locations.ClearBSD]), SonicGensLocation)
    world.get_region(names.Regions.BPC).add_locations(get_location_names_with_ids([names.Locations.ClearBPC]), SonicGensLocation)
    world.get_region(names.Regions.CSC1).add_locations(get_location_names_with_ids([names.Locations.ClearCSC1]), SonicGensLocation)
    world.get_region(names.Regions.CSC2).add_locations(get_location_names_with_ids([names.Locations.ClearCSC2]), SonicGensLocation)
    world.get_region(names.Regions.EUC1).add_locations(get_location_names_with_ids([names.Locations.ClearEUC1]), SonicGensLocation)
    world.get_region(names.Regions.EUC2).add_locations(get_location_names_with_ids([names.Locations.ClearEUC2]), SonicGensLocation)
    world.get_region(names.Regions.PLA1).add_locations(get_location_names_with_ids([names.Locations.ClearPLA1]), SonicGensLocation)
    world.get_region(names.Regions.PLA2).add_locations(get_location_names_with_ids([names.Locations.ClearPLA2]), SonicGensLocation)
    world.get_region(names.Regions.BSL).add_locations(get_location_names_with_ids([names.Locations.ClearBSL]), SonicGensLocation)
    world.get_region(names.Regions.BNE).add_locations(get_location_names_with_ids([names.Locations.ClearBNE]), SonicGensLocation)
    world.get_region(names.Regions.BLB).add_locations(get_location_names_with_ids([names.Locations.ClearBLB]), SonicGensLocation)

def create_events(world: SonicGensWorld) -> None:
    pass