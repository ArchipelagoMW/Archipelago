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
        "New Bark Town - Receive Starter",
        835001001,
        "New Bark Town",
    ),
    LocationData(
        "Route 30 - Visit Mr. Pokemon",
        835001002,
        "Route 30",
    ),
    LocationData(
        "Violet City - Defeat Falkner",
        835001003,
        "Violet City",
    ),
    LocationData(
        "Violet City - Receive Togepi Egg",
        835001004,
        "Violet City",
    ),
    LocationData(
        "Azalea Town - Clear Slowpoke Well",
        835001005,
        "Azalea Town",
    ),
    LocationData(
        "Azalea Town - Defeat Bugsy",
        835001006,
        "Azalea Town",
    ),
    LocationData(
        "Ilex Forest - Clear Farfetch'd Puzzle",
        835001007,
        "Ilex Forest",
    ),
    LocationData(
        "Goldenrod City - Defeat Whitney",
        835001008,
        "Goldenrod City",
    ),
    LocationData(
        "Goldenrod Radio Tower - Receive Radio Card",
        835001009,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Ecruteak City - Defeat Rival in Burned Tower",
        835001010,
        "Ecruteak City",
    ),
    LocationData(
        "Ecruteak City - Defeat Morty",
        835001011,
        "Ecruteak City",
    ),
    LocationData(
        "Ecruteak City - Defeat Kimono Girls",
        835001012,
        "Ecruteak City",
    ),
    LocationData(
        "Olivine Lighthouse - Reach Amphy",
        835001013,
        "Olivine Lighthouse",
    ),
    LocationData(
        "Cianwood City - Receive SecretPotion",
        835001014,
        "Cianwood City",
    ),
    LocationData(
        "Cianwood City - Defeat Chuck",
        835001015,
        "Cianwood City",
    ),
    LocationData(
        "Olivine City - Defeat Jasmine",
        835001016,
        "Olivine City",
    ),
    LocationData(
        "Mahogany Town - Clear Team Rocket HQ",
        835001017,
        "Mahogany Town",
    ),
    LocationData(
        "Mahogany Town - Defeat Pryce",
        835001018,
        "Mahogany Town",
    ),
    LocationData(
        "Goldenrod Underground - Receive Basement Key",
        835001019,
        "Goldenrod Underground",
    ),
    LocationData(
        "Goldenrod Radio Tower - Receive Card Key",
        835001020,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Goldenrod Radio Tower - Clear Radio Tower",
        835001021,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Blackthorn City - Defeat Clair",
        835001022,
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