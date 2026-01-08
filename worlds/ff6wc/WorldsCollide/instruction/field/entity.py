from ...instruction.event import _Instruction
from ...instruction.entity import *

CAMERA, PARTY0, PARTY1, PARTY2, PARTY3 = range(0x30, 0x35)

class MoveDiagonal(_Instruction):
    def __init__(self, dir1, dist1, dir2, dist2):
        from ...data import direction as direction
        dir_letter = { direction.UP : "u", direction.RIGHT : "r",
                       direction.DOWN : "d", direction.LEFT : "l" }
        dest_opcode = {"ru11" : 0xa0, "rd11" : 0xa1, "ld11" : 0xa2, "lu11" : 0xa3,
                       "ru12" : 0xa4, "ru21" : 0xa5, "rd21" : 0xa6, "rd12" : 0xa7,
                       "ld12" : 0xa8, "ld21" : 0xa9, "lu21" : 0xaa, "lu12" : 0xab, }

        if dir1 == direction.UP or dir1 == direction.DOWN:
            dir1, dir2 = dir2, dir1
            dist1, dist2 = dist2, dist1

        self.key = dir_letter[dir1] + dir_letter[dir2] + str(dist1) + str(dist2)
        super().__init__(dest_opcode[self.key])

    def __str__(self):
        return super().__str__(self.key)

class EnableWalkingAnimation(_Instruction):
    def __init__(self):
        super().__init__(0xc6)

class DisableWalkingAnimation(_Instruction):
    def __init__(self):
        super().__init__(0xc7)

class SetSpriteLayer(_Instruction):
    def __init__(self, layer):
        super().__init__(0xc8, layer)

    def __str__(self):
        return super().__str__(self.args[0])

class Hide(_Instruction):
    def __init__(self):
        super().__init__(0xd1)

class SetPosition(_Instruction):
    def __init__(self, x, y):
        super().__init__(0xd5, x, y)

    def __str__(self):
        return super().__str__(f"({self.args[0]}, {self.args[1]})")

class CenterScreen(_Instruction):
    def __init__(self):
        super().__init__(0xd7)

class AnimateStandingFront(_Instruction):
    def __init__(self):
        super().__init__(0x01)

class AnimateKneeling(_Instruction):
    def __init__(self):
        super().__init__(0x09)

class AnimateCloseEyes(_Instruction):
    def __init__(self):
        super().__init__(0x13)

class AnimateAttack(_Instruction):
    def __init__(self):
        super().__init__(0x0a)

class AnimateAttacked(_Instruction):
    def __init__(self):
        super().__init__(0x0b)

class AnimateHandsUp(_Instruction):
    def __init__(self):
        super().__init__(0x0f)

class AnimateFrontHandsUp(_Instruction):
    def __init__(self):
        super().__init__(0x16)

class AnimateFrontRightHandUp(_Instruction):
    def __init__(self):
        super().__init__(0x19)

class AnimateSurprised(_Instruction):
    def __init__(self):
        super().__init__(0x1f)

class AnimateStandingHeadDown(_Instruction):
    def __init__(self):
        super().__init__(0x20)

class AnimateKnockedOut(_Instruction):
    def __init__(self):
        super().__init__(0x28)

class AnimateKnockedOut2(_Instruction):
    def __init__(self):
        super().__init__(0x29)

class AnimateLowJump(_Instruction):
    def __init__(self):
        super().__init__(0xdc)

class AnimateHighJump(_Instruction):
    def __init__(self):
        super().__init__(0xdd)

class _BranchDistance(_Instruction):
    def __init__(self, opcode, distance, offset):
        self.distance = distance
        self.offset = offset
        super().__init__(opcode, distance)

    def __call__(self, space):
        arg = self.distance
        if isinstance(self.distance, str):
            arg = space.absolute_distance(arg) - self.offset
        return self.opcode, arg

    def __str__(self):
        if isinstance(self.distance, str):
            return super().__str__(f"'{self.distance}'")
        return super().__str__(hex(self.distance))

class RandomlyBranchBackwards(_BranchDistance):
    def __init__(self, distance):
        super().__init__(0xfa, distance, -1)

class RandomlyBranchForwards(_BranchDistance):
    def __init__(self, distance):
        super().__init__(0xfb, distance, 1)

class BranchBackwards(_BranchDistance):
    def __init__(self, distance):
        super().__init__(0xfc, distance, -1)

class BranchForwards(_BranchDistance):
    def __init__(self, distance):
        super().__init__(0xfd, distance, 1)
