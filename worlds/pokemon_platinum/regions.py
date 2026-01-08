# regions.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from BaseClasses import Region
from collections.abc import Callable, Mapping, MutableSet, Sequence
from dataclasses import dataclass
from typing import Tuple, TYPE_CHECKING

from worlds.pokemon_platinum.options import PokemonPlatinumOptions

from .data import regions as regiondata
from .data.encounters import encounter_types, encounters
from .locations import PokemonPlatinumLocation

if TYPE_CHECKING:
    from . import PokemonPlatinumWorld

@dataclass(frozen=True)
class RegionType:
    is_enabled: Callable[[PokemonPlatinumOptions], bool]

region_groups: Mapping[str, RegionType] = {
    "generic": RegionType(is_enabled = lambda _ : True),
    "fight_area": RegionType(is_enabled = lambda _ : True),
}

def is_region_enabled(region: str | None, opts: PokemonPlatinumOptions) -> bool:
    if region is not None:
        if region in regiondata.regions:
            return region_groups[regiondata.regions[region].group].is_enabled(opts)
        else:
            return True
    else:
        return False

def is_event_region_enabled(event: str, opts: PokemonPlatinumOptions) -> bool:
    return is_region_enabled(regiondata.event_region_map[event], opts)

def create_regions(world: "PokemonPlatinumWorld") -> Mapping[str, Region]:
    regions: Mapping[str, Region] = {}
    connections: Sequence[Tuple[str, str, str]] = []

    def setup_wild_regions(parent_region: Region, wild_region_data: regiondata.RegionData):
        header = wild_region_data.header
        if header not in encounters:
            return
        encs = encounters[wild_region_data.header]
        for type in encounter_types:
            if type not in wild_region_data.accessible_encounters:
                continue
            e = getattr(encs, type)
            if not e:
                continue
            name = f"{header}_{type}"
            if name not in regions:
                wild_region = Region(name, world.player, world.multiworld)
                regions[name] = wild_region

                for i, mon in enumerate(e):
                    location = PokemonPlatinumLocation(
                        world.player,
                        f"{name}_{i + 1}",
                        "mon_event",
                        parent=wild_region,
                    )
                    location.show_in_spoiler = False
                    location.place_locked_item(world.create_event(f"mon_{mon}"))
                    wild_region.locations.append(location)
            else:
                wild_region = regions[name]
            parent_region.connect(wild_region, f"{parent_region.name} -> {name}")


    ignored_regions: MutableSet[str] = set()
    for region_name, region_data in regiondata.regions.items():
        if not region_groups[region_data.group].is_enabled(world.options):
            ignored_regions.add(region_name)
            continue
        new_region = Region(region_name, world.player, world.multiworld)

        regions[region_name] = new_region

        for event in region_data.events:
            event_loc = PokemonPlatinumLocation(
                world.player,
                event,
                "event",
                parent=new_region)
            event_loc.show_in_spoiler = False
            event_loc.place_locked_item(world.create_event(event))
            new_region.locations.append(event_loc)

        setup_wild_regions(new_region, region_data)

        for region_exit in region_data.exits:
            connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    for name, source, dest in connections:
        if dest in ignored_regions:
            continue
        regions[source].connect(regions[dest], name)

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    regions["Menu"].connect(regions["twinleaf_town_player_house_2f"], "Start Game")

    return regions
