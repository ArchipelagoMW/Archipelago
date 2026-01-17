from typing import Dict

GAME_NAME: str = "UFO 50"
BASE_ID: int = 21061550_00_000  # UFO50, 2 digits for the game number, 3 digits for its items/locations

# client installation data
CLIENT_NAME = f"{GAME_NAME.replace(' ', '')}Client"
GAME_HASH = "b2408e0357ef3cb62bae6af109cd5819"  # md5 for data.win
DLL_NAME = "gm-apclientpp.dll"
DLL_URL = "https://api.github.com/repos/black-sliver/gm-apclientpp/releases"
PATCH_NAME = "ufo_50_basepatch.bsdiff4"
PATCH_URL = "https://api.github.com/repos/UFO-50-Archipelago/basepatch/releases"


# the ids here are the internal ids, the order is the in-game order
game_ids: Dict[str, int] = {
    "Main Menu": 0,
    "Barbuta": 40,
    "Bug Hunter": 20,
    "Ninpek": 34,
    "Paint Chase": 49,
    "Magic Garden": 27,
    "Mortol": 29,
    "Velgress": 15,
    "Planet Zoldath": 48,
    "Attactics": 2,
    "Devilition": 5,
    "Kick Club": 26,
    "Avianos": 50,
    "Mooncat": 11,
    "Bushido Ball": 22,
    "Block Koala": 18,
    "Camouflage": 4,
    "Campanella": 3,
    "Golfaria": 6,
    "The Big Bell Race": 28,
    "Warptank": 16,
    "Waldorf's Journey": 21,  # same as the in-game number
    "Porgy": 10,
    "Onion Delivery": 32,
    "Caramel Caramel": 46,
    "Party House": 36,
    "Hot Foot": 43,
    "Divers": 19,
    "Rail Heist": 13,
    "Vainger": 7,
    "Rock On! Island": 44,
    "Pingolf": 23,
    "Mortol II": 1,
    "Fist Hell": 9,
    "Overbold": 30,
    "Campanella 2": 38,
    "Hyper Contender": 42,
    "Valbrace": 35,
    "Rakshasa": 24,
    "Star Waspir": 17,
    "Grimstone": 12,
    "Lords of Diskonia": 33,
    "Night Manor": 39,
    "Elfazar's Hat": 31,
    "Pilot Quest": 37,
    "Mini & Max": 41,
    "Combatants": 25,
    "Quibble Race": 14,
    "Seaside Drive": 47,
    "Campanella 3": 8,
    "Cyber Owls": 45,
}


def get_game_base_id(game_name: str) -> int:
    return BASE_ID + game_ids[game_name] * 1000
