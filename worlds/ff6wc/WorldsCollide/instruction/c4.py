from ..memory.space import Bank, Allocate, Write, Read
from ..instruction import asm as asm

def _multiply_mod():
    # 16 bit a = low a * high a
    src = Read(0x24781, 0x24791)
    space = Write(Bank.C4, src, "c4 multiply a = low a * high a")
    return space.start_address
multiply = _multiply_mod()

def _divide_mod():
    # 16 bit a = 16 bit a / 8 bit x and x = 8 bit remainder
    src = Read(0x24792, 0x247b6)
    space = Write(Bank.C4, src, "c4 divide a = a / x, x = a % x")
    return space.start_address
divide = _divide_mod()

def _battle_rng():
    # a = random number (0 to 255)
    # NOTE: increments $be (battle ram rng index)
    src = Read(0x24b5a, 0x24b64)
    space = Write(Bank.C4, src, "c4 battle_rng (0 to 255)")
    return space.start_address
battle_rng = _battle_rng()

def _battle_rng_a():
    # a = random number (0 to a register - 1)
    # NOTE: increments $be (battle ram rng index)
    src = [
        Read(0x24b65, 0x24b72),
        asm.JSR(multiply, asm.ABS),          # use multiply function in c4
        Read(0x24b76, 0x24b7a),
    ]
    space = Write(Bank.C4, src, "c4 battle_rng_a (0 to a - 1)")
    return space.start_address
battle_rng_a = _battle_rng_a()
