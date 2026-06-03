from BaseClasses import Location


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSLocation(Location):
    game = GAME_NAME


LOCATION_TABLE = {
    "Violet City - Defeat Falkner": 835001001,
    "Azalea Town - Defeat Bugsy": 835001002,
    "Goldenrod City - Defeat Whitney": 835001003,
    "Ecruteak City - Defeat Morty": 835001004,
    "Cianwood City - Defeat Chuck": 835001005,
    "Olivine City - Defeat Jasmine": 835001006,
    "Mahogany Town - Defeat Pryce": 835001007,
    "Blackthorn City - Defeat Clair": 835001008,
}


location_name_to_id = {
    location_name: location_id
    for location_name, location_id in LOCATION_TABLE.items()
}