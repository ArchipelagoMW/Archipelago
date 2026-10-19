
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from BaseClasses import CollectionRule
from rule_builder.rules import Rule, Has, True_
from .. import GeneratedLocationData
from ..regions.regions import GenericRegions
from ... import Events
from ...constants import LOCATIONS_EVENTS_OFFSET

if TYPE_CHECKING:
    from ...world_base import TCGSimulatorBase


class EventFormat(IntEnum):
    STANDARD = 0
    PAUPER = 1
    FIRE_CUP = 2
    EARTH_CUP = 3
    WATER_CUP = 4
    WIND_CUP = 5
    FIRST_EDITION_VINTAGE = 6
    SILVER_BORDER = 7
    GOLD_BORDER = 8
    EX_BORDER = 9
    FULL_ART_BORDER = 10
    FOIL = 11
    NO_FORMAT = 12


FORMAT_NAMES: dict[EventFormat, tuple[str, CollectionRule | Rule[TCGSimulatorBase]]] = {
    EventFormat.STANDARD: ("Standard", Has(Events.STANDARD.value)),
    EventFormat.PAUPER: ("Pauper", Has(Events.PAUPER.value)),
    EventFormat.FIRE_CUP: ("Fire Cup", Has(Events.FIRE_CUP.value)),
    EventFormat.EARTH_CUP: ("Earth Cup", Has(Events.EARTH_CUP.value)),
    EventFormat.WATER_CUP: ("Water Cup", Has(Events.WATER_CUP.value)),
    EventFormat.WIND_CUP: ("Wind Cup", Has(Events.WIND_CUP.value)),
    EventFormat.FIRST_EDITION_VINTAGE: ("First Edition Vintage", Has(Events.FIRST_EDITION_VINTAGE.value)),
    EventFormat.SILVER_BORDER: ("Silver Border", Has(Events.SILVER_BORDER.value)),
    EventFormat.GOLD_BORDER: ("Gold Border", Has(Events.GOLD_BORDER.value)),
    EventFormat.EX_BORDER: ("EX Border", Has(Events.EX_BORDER.value)),
    EventFormat.FULL_ART_BORDER: ("Full Art Border", Has(Events.FULL_ART_BORDER.value)),
    EventFormat.FOIL: ("Foil", Has(Events.FOIL.value)),
    EventFormat.NO_FORMAT: ("No Format", True_()),
}


def generate_event_locations(formats: list[EventFormat], games_per_format: int = 15) -> list[GeneratedLocationData]:
    if not 0 <= games_per_format < 1000:
        raise ValueError("Play Table Games out of range")
    return [
        GeneratedLocationData(
            name=(f"Play {n} Event Games" if tableFormat == EventFormat.NO_FORMAT
                  else f"Play {n} {FORMAT_NAMES[tableFormat][0]} Format Games"),
            location_id=(LOCATIONS_EVENTS_OFFSET + (tableFormat.value * 1000) + n),
            region=GenericRegions.EVENTS,
            rule=FORMAT_NAMES[tableFormat][1]
        )
        for tableFormat in formats
        for n in range(1, games_per_format + 1)
    ]
