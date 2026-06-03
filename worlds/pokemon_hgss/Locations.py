from dataclasses import dataclass

from BaseClasses import Location


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSLocation(Location):
    game = GAME_NAME


@dataclass(frozen=True)
class LocationData:
    name: str
    code: int | None
    region: str


LOCATION_TABLE = (
    LocationData(
        "Violet City - Defeat Falkner",
        835001001,
        "Violet City",
    ),
    LocationData(
        "Azalea Town - Defeat Bugsy",
        835001002,
        "Azalea Town",
    ),
    LocationData(
        "Goldenrod City - Defeat Whitney",
        835001003,
        "Goldenrod City",
    ),
    LocationData(
        "Ecruteak City - Defeat Morty",
        835001004,
        "Ecruteak City",
    ),
    LocationData(
        "Cianwood City - Defeat Chuck",
        835001005,
        "Cianwood City",
    ),
    LocationData(
        "Olivine City - Defeat Jasmine",
        835001006,
        "Olivine City",
    ),
    LocationData(
        "Mahogany Town - Defeat Pryce",
        835001007,
        "Mahogany Town",
    ),
    LocationData(
        "Blackthorn City - Defeat Clair",
        835001008,
        "Blackthorn City",
    ),

    # Event location.
    # This has no Archipelago location ID because it is not a normal check.
    LocationData(
        "Pokemon League - Defeat Lance",
        None,
        "Pokemon League",
    ),
)


location_name_to_id = {
    location_data.name: location_data.code
    for location_data in LOCATION_TABLE
    if location_data.code is not None
}


def get_locations_for_region(region_name: str) -> list[LocationData]:
    return [
        location_data
        for location_data in LOCATION_TABLE
        if location_data.region == region_name
    ]