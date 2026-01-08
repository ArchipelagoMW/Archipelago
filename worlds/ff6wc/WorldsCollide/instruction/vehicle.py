from ..instruction.event import _Instruction, _Branch, _LoadMap
from ..data import event_bit as event_bit

class End(_Instruction):
    def __init__(self):
        super().__init__(0xff)

class SetPosition(_Instruction):
    def __init__(self, x, y):
        super().__init__(0xc7, x, y) # defined at ee/727b

    def __str__(self):
        return super().__str__(f"({self.args[0]}, {self.args[1]})")

class SetEventBit(_Instruction):
    def __init__(self, event_bit):
        self.event_bit = event_bit
        assert event_bit <= 0x6ff

        super().__init__(0xc8, self.event_bit.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class ClearEventBit(_Instruction):
    def __init__(self, event_bit):
        self.event_bit = event_bit
        assert event_bit <= 0x6ff

        super().__init__(0xc9, self.event_bit.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class BranchIfEventBitClear(_Branch):
    def __init__(self, event_bit, destination):
        self.event_bit = event_bit
        event_bit_arg = event_bit.to_bytes(2, "little")

        super().__init__(0xb0, [event_bit_arg], destination)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class Branch(BranchIfEventBitClear):
    def __init__(self, destination):
        super().__init__(event_bit.ALWAYS_CLEAR, destination)

class FadeLoadMap(_LoadMap):
    # same as load_map, except fades out screen
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0xd2, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)

class LoadMap(_LoadMap):
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0xd3, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)
