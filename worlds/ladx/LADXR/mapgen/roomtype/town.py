from .base import RoomType
from ..tileset import solid_tiles
import random


class Town(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "town"

    def seed(self, wfc, x, y):
        ex = x + 5 + random.randint(-1, 1)
        ey = y + 3 + random.randint(-1, 1)
        wfc.cell_data[(ex, ey)].init_options.intersection_update({0xE2})
        wfc.cell_data[(ex - 1, ey - 1)].init_options.intersection_update(solid_tiles)
        wfc.cell_data[(ex + 1, ey - 1)].init_options.intersection_update(solid_tiles)
