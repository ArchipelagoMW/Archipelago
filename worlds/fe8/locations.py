from typing import Optional

from BaseClasses import Location, LocationProgressType

from .constants import FE8_NAME, FE8_ID_PREFIX


class FE8Location(Location):
    game = FE8_NAME
    local_address: int

    def __init__(self, player: int, name, address: int, parent):
        super(FE8Location, self).__init__(player, name, FE8_ID_PREFIX + address, parent)
        self.local_address = address
        self.event = False
