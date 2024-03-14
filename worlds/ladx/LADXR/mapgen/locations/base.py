from ...roomEditor import RoomEditor
from ..map import RoomInfo


class LocationBase:
    MAX_COUNT = 9999

    def __init__(self, room: RoomInfo, x, y):
        self.room = room
        self.x = x
        self.y = y
        room.locations.append(self)

    def prepare(self, rom):
        pass

    def update_room(self, rom, re: RoomEditor):
        pass

    def connect_logic(self, logic_location):
        raise NotImplementedError(self.__class__)

    def get_item_pool(self):
        raise NotImplementedError(self.__class__)
