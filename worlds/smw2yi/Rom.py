import Utils
from Patch import read_rom, APDeltaPatch
from .Locations import lookup_id_to_name, all_locations

USHASH = 'CB472164C5A71CCD3739963390EC6A50'
ROM_PLAYER_LIMIT = '65535'

import hashlib
import os
import math

def get_base_rom_path(file_name: str = "") -> str:
    return file_name