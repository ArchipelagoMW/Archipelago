"""File containing enums to represent all settings."""

from __future__ import annotations

from typing import TYPE_CHECKING
from randomizer.JsonReader import generate_globals

# I KNOW all of these enums are listed as unused, but they are used in the settings.jsonc file so they are not actually unused
from enum import IntEnum, auto, Enum
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Enums.Maps import Maps

# Each select-based setting should have its own associated enum class. The enum
# values should exactly match the input values in the HTML (not the IDs).
# Do not change the values of any enums in this file, or settings strings will
# break.
# Get the current file name, but replace the extension with ".json" to get the
# associated JSON file.

globals().update(generate_globals(__file__))
