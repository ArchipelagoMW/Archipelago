import json
from pkgutil import get_data
# Used in PsychoSeed.py to show current versions in generated RandoSeed.lua
# Helps with troubleshooting apworld and mod version mismatches
# Update with each new PsychoRando Version released
PSYCHORANDO_VERSION = "2.0.3"

# Gets world_version from archipelago.json
_MANIFEST = json.loads(get_data("worlds.psychonauts", "archipelago.json"))
GAME_NAME = _MANIFEST["game"]
version: str = _MANIFEST["world_version"]
# Want the apworld version with periods used for RandoSeed.lua
AP_WORLD_VERSION_FOR_RANDOSEED = version
_MAJOR, _MINOR, _PATCH = map(int, version.split("."))
AP_WORLD_VERSION: tuple[int, int, int] = (_MAJOR, _MINOR, _PATCH)
del _MANIFEST
