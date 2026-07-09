from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from . import constants

if TYPE_CHECKING:
    from .world import TombaWorld


def create_and_connect_regions(world: TombaWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TombaWorld) -> None:
    village_of_all_beginnings = Region(constants.VILLAGE_OF_ALL_BEGINNINGS, world.player, world.multiworld)

    regions = [village_of_all_beginnings]

    world.multiworld.regions += regions


def connect_regions(world: TombaWorld) -> None:
    pass
