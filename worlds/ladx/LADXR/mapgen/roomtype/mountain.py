from .base import RoomType
from ..locations.entrance import EggEntrance
import random


class Mountain(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "mountains"
        room.edge_left.set_open_min(3)
        room.edge_right.set_open_min(3)

    def seed(self, wfc, x, y):
        super().seed(wfc, x, y)
        if y == 0:
            if x == 0:
                wfc.cell_data[(0, 1)].init_options.intersection_update({0})
            if x == wfc.w - 10:
                wfc.cell_data[(x + 9, 1)].init_options.intersection_update({0})
            wfc.cell_data[(x + random.randint(3, 6), random.randint(0, 1))].init_options.intersection_update({0})


class MountainEgg(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "egg"
        room.edge_left.force_solid()
        room.edge_right.force_solid()
        room.edge_down.set_open_min(5)
        room.edge_down.set_open_max(6)

        EggEntrance(room, 5, 4)

    def seed(self, wfc, x, y):
        super().seed(wfc, x, y)
        wfc.cell_data[(x + 2, y + 1)].init_options.intersection_update({0x00})
        wfc.cell_data[(x + 2, y + 2)].init_options.intersection_update({0xEF})
        wfc.cell_data[(x + 5, y + 3)].init_options.intersection_update({0xAA})
