import struct
import typing
from BaseClasses import CollectionState, Region
from struct import unpack

if typing.TYPE_CHECKING:
    from .Rom import RomData

animal_map = {
    "Rick Spawn": 0,
    "Kine Spawn": 1,
    "Coo Spawn": 2,
    "Nago Spawn": 3,
    "ChuChu Spawn": 4,
    "Pitch Spawn": 5
}


class Room(Region):
    pointer: int = 0
    level: int = 0
    stage: int = 0
    room: int = 0
    music: int = 0
    default_exits: typing.List[typing.Dict[str, typing.Union[int, typing.List[str]]]]
    animal_pointers: typing.List[int]
    enemies: typing.List[str]

    def __init__(self, name, player, multiworld, hint, level, stage, room, pointer, music, default_exits,
                 animal_pointers, enemies):
        super().__init__(name, player, multiworld, hint)
        self.level = level
        self.stage = stage
        self.room = room
        self.pointer = pointer
        self.music = music
        self.default_exits = default_exits
        self.animal_pointers = animal_pointers
        self.enemies = enemies

    def patch(self, rom: "RomData"):
        rom.write_byte(self.pointer + 2, self.music)
        animals = [x.item.name for x in self.locations if "Animal" in x.name]
        if len(animals) > 0:
            for current_animal, address in zip(animals, self.animal_pointers):
                rom.write_byte(self.pointer + address + 7, animal_map[current_animal])
