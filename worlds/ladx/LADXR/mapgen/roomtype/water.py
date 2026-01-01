from .base import RoomType
import random


class Water(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "water"

    # def seed(self, wfc, x, y):
    #     wfc.cell_data[(x + 5 + random.randint(-1, 1), y + 3 + random.randint(-1, 1))].init_options.intersection_update({0x0E})


class Beach(RoomType):
    def __init__(self, room):
        super().__init__(room)
        room.tileset_id = "beach"
        if self.room.room_down is None:
            self.room.edge_left.set_open_max(4)
            self.room.edge_right.set_open_max(4)
        self.room.edge_up.set_open_min(4)
        self.room.edge_up.set_open_max(6)

    def seed(self, wfc, x, y):
        if self.room.room_down is None:
            for n in range(1, 9):
                wfc.cell_data[(x + n, y + 5)].init_options.intersection_update({0x1E})
            for n in range(1, 9):
                wfc.cell_data[(x + n, y + 7)].init_options.intersection_update({0x1F})
        super().seed(wfc, x, y)