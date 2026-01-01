from .base import RoomType
from ..tileset import open_tiles
import random


class Forest(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "forest"

    def seed(self, wfc, x, y):
        if self.room.room_up and isinstance(self.room.room_up.room_type, Forest) and self.room.edge_up.get_open_range() is None:
            self.room.edge_up.set_solid()
        if self.room.room_left and isinstance(self.room.room_left.room_type, Forest) and self.room.edge_left.get_open_range() is None:
            self.room.edge_left.set_solid()

        if self.room.room_up and isinstance(self.room.room_up.room_type, Forest) and random.random() < 0.5:
            door_x, door_y = x + 5 + random.randint(-1, 1), y + 3 + random.randint(-1, 1)
            wfc.cell_data[(door_x, door_y)].init_options.intersection_update({0xE3})
            self.room.edge_up.set_solid()
            if self.room.edge_left.get_open_range() is not None:
                for x0 in range(x + 1, door_x):
                    wfc.cell_data[(x0, door_y + 1)].init_options.intersection_update(open_tiles)
            if self.room.edge_right.get_open_range() is not None:
                for x0 in range(door_x + 1, x + 10):
                    wfc.cell_data[(x0, door_y + 1)].init_options.intersection_update(open_tiles)
        else:
            super().seed(wfc, x, y)
