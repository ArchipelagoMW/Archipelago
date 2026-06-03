from BaseClasses import Location


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSLocation(Location):
    game = GAME_NAME


LOCATION_TABLE = {
    "New Bark Town - Receive Starter": 835001001,
    "Violet City - Defeat Falkner": 835001002,
    "Azalea Town - Defeat Bugsy": 835001003,
    "Goldenrod City - Defeat Whitney": 835001004,
}


location_name_to_id = {
    location_name: location_id
    for location_name, location_id in LOCATION_TABLE.items()
}