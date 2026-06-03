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


GYM_LEADER_LOCATIONS = {
    "Violet City - Defeat Falkner",
    "Azalea Town - Defeat Bugsy",
    "Goldenrod City - Defeat Whitney",
    "Ecruteak City - Defeat Morty",
    "Cianwood City - Defeat Chuck",
    "Olivine City - Defeat Jasmine",
    "Mahogany Town - Defeat Pryce",
    "Blackthorn City - Defeat Clair",
}


EARLY_JOHTO_LOCATIONS = {
    "New Bark Town - Receive Starter",
    "New Bark Town - Receive Pokegear",
    "Cherrygrove City - Receive Running Shoes",
    "Cherrygrove City - Receive Map Card",
    "Route 30 - Visit Mr. Pokemon",
    "Route 30 - Receive Apricorn Box",
    "Violet City - Clear Sprout Tower",
    "Violet City - Defeat Falkner",
    "Violet City - Receive Togepi Egg",
    "Route 32 - Receive Miracle Seed",
    "Union Cave - Reach South Exit",
    "Azalea Town - Clear Slowpoke Well",
    "Azalea Town - Defeat Bugsy",
    "Ilex Forest - Clear Farfetch'd Puzzle",
}


RADIO_TOWER_LOCATIONS = {
    "Goldenrod Radio Tower - Receive Radio Card",
    "Goldenrod Underground - Receive Basement Key",
    "Goldenrod Radio Tower - Receive Card Key",
    "Goldenrod Radio Tower - Clear Radio Tower",
}


STORY_LOCATIONS = {
    "New Bark Town - Receive Starter",
    "New Bark Town - Receive Pokegear",
    "Cherrygrove City - Receive Running Shoes",
    "Cherrygrove City - Receive Map Card",
    "Route 30 - Visit Mr. Pokemon",
    "Route 30 - Receive Apricorn Box",
    "Violet City - Clear Sprout Tower",
    "Violet City - Receive Togepi Egg",
    "Azalea Town - Clear Slowpoke Well",
    "Ilex Forest - Clear Farfetch'd Puzzle",
    "Goldenrod City - Receive Bicycle",
    "Goldenrod Radio Tower - Receive Radio Card",
    "Route 35 - Receive Kenya",
    "National Park - Receive Quick Claw",
    "Ecruteak City - Defeat Rival in Burned Tower",
    "Ecruteak City - Clear Dance Theater",
    "Ecruteak City - Defeat Kimono Girls",
    "Olivine City - Receive Good Rod",
    "Olivine Lighthouse - Reach Amphy",
    "Cianwood City - Receive SecretPotion",
    "Cianwood City - Receive Shuckle",
    "Mahogany Town - Clear Team Rocket HQ",
    "Lake of Rage - Defeat Red Gyarados",
    "Goldenrod Underground - Receive Basement Key",
    "Goldenrod Radio Tower - Receive Card Key",
    "Goldenrod Radio Tower - Clear Radio Tower",
    "Victory Road - Defeat Rival",
}


LOCATION_TABLE = (
    LocationData(
        "New Bark Town - Receive Starter",
        835001001,
        "New Bark Town",
    ),
    LocationData(
        "New Bark Town - Receive Pokegear",
        835001002,
        "New Bark Town",
    ),
    LocationData(
        "Cherrygrove City - Receive Running Shoes",
        835001003,
        "Cherrygrove City",
    ),
    LocationData(
        "Cherrygrove City - Receive Map Card",
        835001004,
        "Cherrygrove City",
    ),
    LocationData(
        "Route 30 - Visit Mr. Pokemon",
        835001005,
        "Route 30",
    ),
    LocationData(
        "Route 30 - Receive Apricorn Box",
        835001006,
        "Route 30",
    ),
    LocationData(
        "Violet City - Clear Sprout Tower",
        835001007,
        "Violet City",
    ),
    LocationData(
        "Violet City - Defeat Falkner",
        835001008,
        "Violet City",
    ),
    LocationData(
        "Violet City - Receive Togepi Egg",
        835001009,
        "Violet City",
    ),
    LocationData(
        "Route 32 - Receive Miracle Seed",
        835001010,
        "Route 32",
    ),
    LocationData(
        "Union Cave - Reach South Exit",
        835001011,
        "Union Cave",
    ),
    LocationData(
        "Azalea Town - Clear Slowpoke Well",
        835001012,
        "Azalea Town",
    ),
    LocationData(
        "Azalea Town - Defeat Bugsy",
        835001013,
        "Azalea Town",
    ),
    LocationData(
        "Ilex Forest - Clear Farfetch'd Puzzle",
        835001014,
        "Ilex Forest",
    ),
    LocationData(
        "Goldenrod City - Defeat Whitney",
        835001015,
        "Goldenrod City",
    ),
    LocationData(
        "Goldenrod City - Receive Bicycle",
        835001016,
        "Goldenrod City",
    ),
    LocationData(
        "Goldenrod Radio Tower - Receive Radio Card",
        835001017,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Route 35 - Receive Kenya",
        835001018,
        "Route 35",
    ),
    LocationData(
        "National Park - Receive Quick Claw",
        835001019,
        "National Park",
    ),
    LocationData(
        "Ecruteak City - Defeat Rival in Burned Tower",
        835001020,
        "Ecruteak City",
    ),
    LocationData(
        "Ecruteak City - Defeat Morty",
        835001021,
        "Ecruteak City",
    ),
    LocationData(
        "Ecruteak City - Clear Dance Theater",
        835001022,
        "Ecruteak City",
    ),
    LocationData(
        "Ecruteak City - Defeat Kimono Girls",
        835001023,
        "Ecruteak City",
    ),
    LocationData(
        "Olivine City - Receive Good Rod",
        835001024,
        "Olivine City",
    ),
    LocationData(
        "Olivine Lighthouse - Reach Amphy",
        835001025,
        "Olivine Lighthouse",
    ),
    LocationData(
        "Cianwood City - Receive SecretPotion",
        835001026,
        "Cianwood City",
    ),
    LocationData(
        "Cianwood City - Defeat Chuck",
        835001027,
        "Cianwood City",
    ),
    LocationData(
        "Cianwood City - Receive Shuckle",
        835001028,
        "Cianwood City",
    ),
    LocationData(
        "Olivine City - Defeat Jasmine",
        835001029,
        "Olivine City",
    ),
    LocationData(
        "Mahogany Town - Clear Team Rocket HQ",
        835001030,
        "Mahogany Town",
    ),
    LocationData(
        "Lake of Rage - Defeat Red Gyarados",
        835001031,
        "Lake of Rage",
    ),
    LocationData(
        "Mahogany Town - Defeat Pryce",
        835001032,
        "Mahogany Town",
    ),
    LocationData(
        "Goldenrod Underground - Receive Basement Key",
        835001033,
        "Goldenrod Underground",
    ),
    LocationData(
        "Goldenrod Radio Tower - Receive Card Key",
        835001034,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Goldenrod Radio Tower - Clear Radio Tower",
        835001035,
        "Goldenrod Radio Tower",
    ),
    LocationData(
        "Blackthorn City - Defeat Clair",
        835001036,
        "Blackthorn City",
    ),
    LocationData(
        "Victory Road - Defeat Rival",
        835001037,
        "Victory Road",
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


location_name_groups = {
    "Gym Leaders": GYM_LEADER_LOCATIONS,
    "Early Johto": EARLY_JOHTO_LOCATIONS,
    "Radio Tower": RADIO_TOWER_LOCATIONS,
    "Story": STORY_LOCATIONS,
}


def get_locations_for_region(region_name: str) -> list[LocationData]:
    return [
        location_data
        for location_data in LOCATION_TABLE
        if location_data.region == region_name
    ]