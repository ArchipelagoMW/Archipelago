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
