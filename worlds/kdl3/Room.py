import struct
import typing
from BaseClasses import Region, ItemClassification

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


class KDL3Room(Region):
    pointer: int = 0
    level: int = 0
    stage: int = 0
    room: int = 0
    music: int = 0
    default_exits: typing.List[typing.Dict[str, typing.Union[int, typing.List[str]]]]
    animal_pointers: typing.List[int]
    enemies: typing.List[str]
    entity_load: typing.List[typing.List[int]]
    consumables: typing.List[typing.Dict[str, typing.Union[int, str]]]

    def __init__(self, name, player, multiworld, hint, level, stage, room, pointer, music, default_exits,
                 animal_pointers, enemies, entity_load, consumables, consumable_pointer):
        super().__init__(name, player, multiworld, hint)
        self.level = level
        self.stage = stage
        self.room = room
        self.pointer = pointer
        self.music = music
        self.default_exits = default_exits
        self.animal_pointers = animal_pointers
        self.enemies = enemies
        self.entity_load = entity_load
        self.consumables = consumables
        self.consumable_pointer = consumable_pointer

    def patch(self, rom: "RomData"):
        rom.write_byte(self.pointer + 2, self.music)
        animals = [x.item.name for x in self.locations if "Animal" in x.name]
        if len(animals) > 0:
            for current_animal, address in zip(animals, self.animal_pointers):
                rom.write_byte(self.pointer + address + 7, animal_map[current_animal])
        if self.multiworld.worlds[self.player].options.consumables:
            load_len = len(self.entity_load)
            for consumable in self.consumables:
                location = next(x for x in self.locations if x.name == consumable["name"])
                assert location.item
                is_progression = location.item.classification & ItemClassification.progression
                if load_len == 8:
                    # edge case, there is exactly 1 room with 8 entities and only 1 consumable among them
                    if not (any(x in self.entity_load for x in [[0, 22], [1, 22]])
                            and any(x in self.entity_load for x in [[2, 22], [3, 22]])):
                        replacement_target = self.entity_load.index(
                            next(x for x in self.entity_load if x in [[0, 22], [1, 22], [2, 22], [3, 22]]))
                        if is_progression:
                            vtype = 0
                        else:
                            vtype = 2
                        rom.write_byte(self.pointer + 88 + (replacement_target * 2), vtype)
                        self.entity_load[replacement_target] = [vtype, 22]
                else:
                    if is_progression:
                        # we need to see if 1-ups are in our load list
                        if any(x not in self.entity_load for x in [[0, 22], [1, 22]]):
                            self.entity_load.append([0, 22])
                    else:
                        if any(x not in self.entity_load for x in [[2, 22], [3, 22]]):
                            # edge case: if (1, 22) is in, we need to load (3, 22) instead
                            if [1, 22] in self.entity_load:
                                self.entity_load.append([3, 22])
                            else:
                                self.entity_load.append([2, 22])
                if load_len < len(self.entity_load):
                    rom.write_bytes(self.pointer + 88 + (load_len * 2), bytes(self.entity_load[load_len]))
                    rom.write_bytes(self.pointer + 104 + (load_len * 2),
                                    bytes(struct.pack("H", self.consumable_pointer)))
                if is_progression:
                    if [1, 22] in self.entity_load:
                        vtype = 1
                    else:
                        vtype = 0
                else:
                    if [3, 22] in self.entity_load:
                        vtype = 3
                    else:
                        vtype = 2
                rom.write_byte(self.pointer + consumable["pointer"] + 7, vtype)
