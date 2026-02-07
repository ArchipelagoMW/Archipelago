from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TVRUHHWorld



def create_and_connect_regions(world: TVRUHHWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TVRUHHWorld) -> None:
    #create regions
    start = Region("Start", world.player, world.multiworld)
    post_50monsters = Region("Unlocked 50 Monsters", world.player, world.multiworld)
    quickplay_unlocked = Region("Unlocked Quickplay", world.player, world.multiworld)

    #collection of regions
    regions = [
        start,
        post_50monsters,
        quickplay_unlocked
    ]

    #submit regions
    world.multiworld.regions += regions
    
def connect_regions(world: TVRUHHWorld) -> None:
    #get regions
    start = world.get_region("Start")
    post_50monsters = world.get_region("Unlocked 50 Monsters")
    quickplay_unlocked = world.get_region("Unlocked Quickplay")

    start.connect(post_50monsters,"Start to having 50 Monsters unlocked")
    start.connect(quickplay_unlocked,"Start to Quickplay")
