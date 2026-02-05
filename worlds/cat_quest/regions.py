from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import CatQuestWorld

def create_and_connect_regions(world: CatQuestWorld) -> None:
    create_all_regions(world)

def create_all_regions(world: CatQuestWorld) -> None:
    felingard = Region("Felingard", world.player, world.multiworld)

    world.multiworld.regions += [felingard]
