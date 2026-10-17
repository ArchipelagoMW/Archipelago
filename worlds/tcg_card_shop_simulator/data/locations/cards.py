from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from . import GeneratedLocationData
from ..helpers.card_types import (
    Border, CardSpecies, Expansion, Foil, Rarity,
    SPECIES_NAMES, SPECIES_RARITIES,
)
from ..regions.regions import region_by_pack

if TYPE_CHECKING:
    from ...world_base import TCGSimulatorBase

def generate_card_sanity_locations(
    unique_foils: bool,
    percent_in_multiworld: float,
    world: TCGSimulatorBase | None
) -> list[GeneratedLocationData]:
    if percent_in_multiworld < 0 or percent_in_multiworld > 1:
        raise ValueError("percent not a percent")
    if percent_in_multiworld > 0 and world is None:
        raise ValueError("Card sanity Generation must provide a world for random")

    result: list[GeneratedLocationData] = []
    foils = ((Foil.NON_FOIL, Foil.FOIL) if unique_foils
             else (Foil.NON_FOIL,))
    for expansion in Expansion:
        for rarity in Rarity:
            region = region_by_pack[(expansion, rarity)]
            for species in CardSpecies:
                if SPECIES_RARITIES[species] != rarity:
                    continue
                for border in Border:
                    for foil in foils:
                        location_id = 1 << 51 | (expansion.value << 12) | (border.value << 8) | (foil << 7) | species
                        is_in_multiworld = False
                        if percent_in_multiworld > 0:
                            is_in_multiworld = world.random.random() < percent_in_multiworld

                        result.append(GeneratedLocationData(
                            name=(f"{SPECIES_NAMES[species]} "
                                  f"{border.name.replace('_', ' ').title()} "
                                  f"{foil.name.replace('_', ' ').title()} "
                                  f"{expansion.name.title()}"),
                            location_id=location_id,
                            region=region,
                            progress_type= LocationProgressType.DEFAULT if is_in_multiworld else LocationProgressType.EXCLUDED,
                        ))
    return result