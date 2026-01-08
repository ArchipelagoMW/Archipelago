from ..instruction.event import _Instruction, _Branch, _LoadMap
from ..instruction.entity import *
from ..data import event_bit as event_bit

class SubmergeFigaroCastle(_Instruction):
    def __init__(self):
        super().__init__(0xfd)

class EmergeFigaroCastle(_Instruction):
    def __init__(self):
        super().__init__(0xfe)

class FadeLoadMap(_LoadMap):
    # same as load map, except fades out screen
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0xd2, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)

class LoadMap(_LoadMap):
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0xd3, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)

class BranchIfEventBitSet(_Branch):
    def __init__(self, event_bit, destination):
        self.event_bit = event_bit
        event_bit_arg = (event_bit | 0x8000).to_bytes(2, "little")

        super().__init__(0xb0, [event_bit_arg], destination)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class BranchIfEventBitClear(_Branch):
    def __init__(self, event_bit, destination):
        self.event_bit = event_bit
        event_bit_arg = event_bit.to_bytes(2, "little")

        super().__init__(0xb0, [event_bit_arg], destination)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class EndIfEventBitSet(BranchIfEventBitSet):
    def __init__(self, event_bit):
        from ..instruction.field.functions import END
        super().__init__(event_bit, END)

class EndIfEventBitClear(BranchIfEventBitClear):
    def __init__(self, event_bit):
        from ..instruction.field.functions import END
        super().__init__(event_bit, END)

class Branch(BranchIfEventBitClear):
    def __init__(self, destination):
        super().__init__(event_bit.ALWAYS_CLEAR, destination)
