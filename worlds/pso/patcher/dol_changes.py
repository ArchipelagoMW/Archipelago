from BaseClasses import NamedTuple

class PatchData(NamedTuple):
    address: int
    data: list[int]

# This file contains all the changes that will be applied by the patcher and applied to the ROM
# before any randomization is done
CODE_PATCHES = [
    PatchData(0x0, [0x0, 0x0, 0x0, 0x0])
]