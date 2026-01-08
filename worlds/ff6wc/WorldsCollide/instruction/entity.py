from ..instruction.event import _Instruction
from enum import IntEnum
from .. import data

class End(_Instruction):
    def __init__(self):
        super().__init__(0xff)

class Pause(_Instruction):
    def __init__(self, units):
        # units = frames // 4, e.g. 24 frames = 6 units * 4
        super().__init__(0xe0, units)

    def __str__(self):
        return super().__str__(str(self.args[0]))

class Move(_Instruction):
    def __init__(self, direction, distance):
        if distance > 8:
            print("Warning: char.move: distance > 8, reducing to 8")
            distance = 8

        self.direction = direction
        self.distance = distance

        from ..data import direction as data_direction
        opcode = (distance - 1) * 4
        if direction == data_direction.UP:
            opcode += 0x80
        elif direction == data_direction.RIGHT:
            opcode += 0x81
        elif direction == data_direction.DOWN:
            opcode += 0x82
        elif direction == data_direction.LEFT:
            opcode += 0x83
        super().__init__(opcode)

    def __str__(self):
        return super().__str__(f"{str(self.direction)} {str(self.distance)}")

class Turn(_Instruction):
    def __init__(self, direction):
        self.direction = direction

        from ..data import direction as data_direction
        if direction == data_direction.UP:
            super().__init__(0xcc)
        elif direction == data_direction.RIGHT:
            super().__init__(0xcd)
        elif direction == data_direction.DOWN:
            super().__init__(0xce)
        elif direction == data_direction.LEFT:
            super().__init__(0xcf)

    def __str__(self):
        return super().__str__(str(self.direction))

class Speed(IntEnum):
    SLOWEST = 0xc0
    SLOW    = 0xc1
    NORMAL  = 0xc2
    FAST    = 0xc3
    FASTEST = 0xc4
class SetSpeed(_Instruction):
    def __init__(self, speed):
        super().__init__(speed)

    def __str__(self):
        return super().__str__(str(self.opcode))
