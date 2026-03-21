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

    if world.options.shop_upgrades:
        shopdigits = world.get_region("shopdigits")
        start.connect(shopdigits, "Start to shopdigits")

    if (world.options.giftcoins or world.options.goal > 1200): 
        if world.options.shop_upgrades:   
            shopups = world.get_region("shopups")
            start.connect(shopups, "Start to shopupgrades")
        if world.options.shop_colors:
            shopcolors = world.get_region("shopcolors")
            start.connect(shopcolors, "Start to shopcolors")
        if world.options.shop_music:
            shopmusic = world.get_region("shopmusic")
            start.connect(shopmusic, "Start to shopmusic")
        if world.options.shop_sounds:
            shopsounds = world.get_region("shopsounds")
            start.connect(shopsounds, "Start to shopsounds")

    
    