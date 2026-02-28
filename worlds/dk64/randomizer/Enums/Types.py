"""Location/item type enum."""

from randomizer.JsonReader import generate_globals
from js import getStringFile
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from randomizer.Enums.Types import Types

globals().update(generate_globals(__file__))

f = getStringFile("randomizer/Enums/Types.json")
_data = json.loads(f)
KeySelector = _data["KeySelector"]
ItemRandoSelector = _data["ItemRandoSelector"]
check_map = {
    "shop": 1,
    "moves": 2,
    "shockwave": 3,
    "bfi_gift": 4,
    "banana": 5,
    "banana_checks": 6,
    "toughbanana": 7,
    "arenas": 8,
    "crown": 9,
    "blueprint": 10,
    "kasplat": 11,
    "key": 12,
    "bosses": 13,
    "endofhelm": 14,
    "medal": 15,
    "medal_checks": 16,
    "medal_checks_helm": 17,
    "nintendocoin": 18,
    "arcade": 19,
    "rarewarecoin": 20,
    "jetpac": 21,
    "kong": 22,
    "kong_cages": 23,
    "fairy": 24,
    "fairy_checks": 25,
    "rainbowcoin": 26,
    "dirt_patches": 27,
    "pearl": 28,
    "clams": 29,
    "bean": 30,
    "anthillreward": 31,
    "crateitem": 32,
    "shopowners": 33,
    "hint": 34,
    "wrinkly": 35,
    "boulderitem": 36,
    "enemies": 37,
    "dummyitem_enemies": 38,
    "dummyitem_boulderitem": 39,
    "dummyitem_crateitem": 40,
    "trainingmoves": 41,
    "trainingbarrels": 42,
    "halfmedal": 43,
    "dummyitem_halfmedal": 44,
    "racebanana": 45,
    "gauntletbanana": 46,
    "blueprintbanana": 47,
    "sniderewards": 48,
}
for item in ItemRandoSelector:
    item["num_val"] = check_map.get(item["value"], 0)
ItemRandoFillerSelector = _data["ItemRandoFillerSelector"]
