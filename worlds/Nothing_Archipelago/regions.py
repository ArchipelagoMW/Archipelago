from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance,Region

if TYPE_CHECKING:
    from .world import NothingWorld

def create_and_connect_regions(world: NothingWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: NothingWorld) -> None:
    start = Region("start", world.player, world.multiworld)

    regions = [start]

    if world.options.shop_upgrades:
        if (world.options.giftcoins or world.options.goal > 1200):
            shopups = Region("shopups", world.player, world.multiworld)
            regions.append(shopups)
        shopdigits = Region("shopdigits", world.player, world.multiworld)
        regions.append(shopdigits)

    if world.options.shop_colors:
        if (world.options.giftcoins or world.options.goal > 1200):
            shopcolors = Region("shopcolors", world.player, world.multiworld)
            regions.append(shopcolors)

    if world.options.shop_music:
        if (world.options.giftcoins or world.options.goal > 1200):
            shopmusic = Region("shopmusic", world.player, world.multiworld)
            regions.append(shopmusic)

    if world.options.shop_sounds:
        if (world.options.giftcoins or world.options.goal > 1200):
            shopsounds = Region("shopsounds", world.player, world.multiworld)
            regions.append(shopsounds)

    world.multiworld.regions += regions

def connect_regions(world: NothingWorld) -> None:
    start = world.get_region("start")


    
    