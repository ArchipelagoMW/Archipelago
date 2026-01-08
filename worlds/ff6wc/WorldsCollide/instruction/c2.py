from ..memory.space import Bank, START_ADDRESS_SNES, Space, Reserve, Allocate, Free, Write
from ..instruction import asm as asm
from .. import args as args

def _multiply_mod():
    # 16 bit a = high byte of a * low byte of a
    return 0x24781
multiply = _multiply_mod()

def _multiply_a_e8_mod():
    # 24 bit e8 = 8 bit e8 * 16 bit a
    # 16 bit a = (8 bit e8 * 16 bit a) / 256
    # 16 bit ec = 8 bit e8 * high byte of a
    return 0x247b7
multiply_a_e8 = _multiply_a_e8_mod()

def _multiply_max_100_mod():
    # 16 bit a = high byte of a * low byte of a
    # if result is > 100, then it is rounded down to 100
    src = [
        asm.PHP(),
        asm.A16(),
        asm.JSR(multiply, asm.ABS),
        asm.CMP(101, asm.IMM16),
        asm.BLT("RETURN"),
        asm.LDA(100, asm.IMM16),

        "RETURN",
        asm.PLP(),
        asm.RTS(),
    ]
    space = Write(Bank.C2, src, "c2 multiply_max_100, a = low a * high a")
    return space.start_address
multiply_max_100 = _multiply_max_100_mod()

def _multiply_max_255_mod():
    # 8 bit a = high byte of a * low byte of a
    # if result is > 255, then it is rounded down to 255
    src = [
        asm.PHP(),
        asm.A16(),
        asm.JSR(multiply, asm.ABS),
        asm.CMP(256, asm.IMM16),
        asm.BLT("RETURN"),
        asm.LDA(255, asm.IMM16),

        "RETURN",
        asm.PLP(),
        asm.RTS(),
    ]
    space = Write(Bank.C2, src, "c2 multiply_max_255, a = low a * high a")
    return space.start_address
multiply_max_255 = _multiply_max_255_mod()

def _multiply_max_65535_mod():
    # 16 bit a = 8 bit e8 * 16 bit a
    # if result > 65535, then it is rounded down to 65535
    src = [
        asm.PHP(),
        asm.A16(),
        asm.JSR(multiply_a_e8, asm.ABS),
        asm.LDA(0xe9, asm.DIR),     # load high bytes of 24 bit result
        asm.AND(0xff00, asm.IMM16), # extract high byte
        asm.CMP(0x0000, asm.IMM16), # high byte zero? (> 16 bit result?)
        asm.BNE("RETURN_MAX"),      # branch if result > 0xffff
        asm.LDA(0xe8, asm.DIR),
        asm.PLP(),
        asm.RTS(),

        "RETURN_MAX",
        asm.LDA(0xffff, asm.IMM16),
        asm.PLP(),
        asm.RTS(),
    ]
    space = Write(Bank.C2, src, "c2 multiply_max_65535, a = e8 * a")
    return space.start_address
multiply_max_65535 = _multiply_max_65535_mod()

def _divide_mod():
    # 16 bit a = 16 bit a // 8 bit x
    # 8 bit x = 16 bit a % 8 bit x
    return 0x24792
divide = _divide_mod()

def _rng_carry_mod():
    # randomly set/clear carry bit
    return 0x24b53
rng_carry = _rng_carry_mod()

def _rng_mod():
    # a = random number (0 to 255)
    return 0x24b5a
rng = _rng_mod()

def _rng_a_mod():
    # a = random number (0 to a register - 1)
    return 0x24b65
rng_a = _rng_a_mod()

def _set_bit_x_mod():
    # set bit #x in a
    return 0x21e57
set_bit_x = _set_bit_x_mod()
