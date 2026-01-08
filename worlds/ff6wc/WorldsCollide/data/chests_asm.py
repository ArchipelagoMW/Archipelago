from ..memory.space import Bank, Reserve, Write, Read, START_ADDRESS_SNES
from ..instruction import asm as asm
from ..instruction import c0 as c0

def _next_scaled_contents(bits, contents):
    # write chest contents in the order they should be received
    space = Write(Bank.C0, contents, "scaled chest contents table")
    scaled_contents_table = space.start_address + START_ADDRESS_SNES

    # write bits of chests which should be scaled
    space = Write(Bank.C0, bits, "scaled chest bits table")
    scaled_bits_table = space.start_address + START_ADDRESS_SNES
    scaled_bits_table_size = len(space)

    opened_bits_start = 0x1e40

    # count number of bits set (number of scaled chests opened) to get index of next scaled contents
    # return contents of next scaled chest
    src = [
        asm.PHP(),
        asm.PHY(),
        asm.AXY16(),

        asm.LDX(0x0000, asm.IMM16),                 # initialize table index to zero
        asm.LDY(0x0000, asm.IMM16),                 # initialize number of scaled chests opened to zero
        asm.PHX(),                                  # initialize current chest found flag to false

        "COUNT_OPENED_LOOP",

        # if current chest being opened equals scaled_bits_table[x] then set chest found flag to true
        asm.LDA(0x1e, asm.DIR),                     # a = chest being opened type/bit
        asm.AND(0x01ff, asm.IMM16),                 # a = chest being opened bit (remove type)
        asm.CMP(scaled_bits_table, asm.LNG_X),      # is the chest being opened the current chest in scaled_bits_table?
        asm.BNE("CHECK_OPENED"),                    # if not, check if skip setting flag to true
        asm.PLA(),                                  # pull not found flag from stack
        asm.LDA(0x0001, asm.IMM16),                 # a = 1 (chest being opened found in scaled_bits_table)
        asm.PHA(),                                  # push chest found flag onto stack

        # check if scaled_bits_table[x] has already been opened, if so increment scaled_contents_table index
        "CHECK_OPENED",
        asm.PHX(),
        asm.LDA(scaled_bits_table, asm.LNG_X),      # a = chest bit number
        asm.AND(0x0007, asm.IMM16),                 # a = chest bit number % 8
        asm.TAX(),                                  # x = chest bit number % 8
        asm.LDA(c0.power_of_two_table, asm.LNG_X),  # set bit x in 16-bit a
        asm.AND(0x00ff, asm.IMM16),                 # a = chest opened bitmask
        asm.PLX(),
        asm.PHX(),
        asm.PHA(),
        asm.LDA(scaled_bits_table, asm.LNG_X),      # a = chest bit number
        asm.LSR(),
        asm.LSR(),
        asm.LSR(),                                  # a = chest bit number / 8
        asm.TAX(),                                  # x = chest bit number / 8
        asm.PLA(),                                  # a = chest opened bitmask
        asm.BIT(opened_bits_start, asm.ABS_X),      # has this chest been opened?
        asm.BEQ("NEXT_TABLE_ENTRY"),                # if not, skip incrementing count
        asm.INY(),                                  # increment number of scaled chests opened
        "NEXT_TABLE_ENTRY",
        asm.PLX(),
        asm.INX(),
        asm.INX(),                                  # next chest bits table index
        asm.CPX(scaled_bits_table_size, asm.IMM16), # finished iterating through table?
        asm.BLT("COUNT_OPENED_LOOP"),               # branch if not

        # if current chest being opened is not in table of chest bits to be scaled then return original its contents
        asm.PLA(),                                  # pull chest found flag from stack
        asm.BNE("RETURN_NEXT_SCALED_CONTENTS"),     # if chest was found, scale the contents
        asm.A8(),
        asm.LDA(0x1a, asm.DIR),                     # otherwise, return original chest contents
        asm.BRA("RETURN"),

        # if current chest being opened is in table of chest bits to be scaled, return next scaled contents
        "RETURN_NEXT_SCALED_CONTENTS",
        asm.TYX(),                                  # x = number of scaled chests opened
        asm.DEX(),                                  # decrement, current chest was marked as opened before counting
        asm.TDC(),
        asm.A8(),
        asm.LDA(scaled_contents_table, asm.ABS_X),  # return contents of next unopened scaled chest

        "RETURN",
        asm.PLY(),
        asm.PLP(),
        asm.RTS(),
    ]
    space = Write(Bank.C0, src, "next unopened scaled chest contents")
    next_scaled_contents = space.start_address
    return next_scaled_contents

def scale_items(bits, contents):
    next_scaled_item = _next_scaled_contents(bits, contents)

    src = [
        asm.JSR(next_scaled_item, asm.ABS),         # a = next item
        asm.STA(0x1a, asm.DIR),                     # store id of item to add to inventory
        asm.STA(0x0583, asm.ABS),                   # store id of item name to display
        asm.RTS(),
    ]
    space = Write(Bank.C0, src, "load chest scaled item")
    load_scaled_item = space.start_address

    space = Reserve(0x04c86, 0x04c8a, "load chest item", asm.NOP())
    space.write(
        asm.JSR(load_scaled_item, asm.ABS),
    )

def scale_gold(bits, contents, exclude = None):
    next_scaled_amount = _next_scaled_contents(bits, contents)

    src = [
        asm.JSR(next_scaled_amount, asm.ABS),       # a = next gp amount
        asm.STA(0x1a, asm.DIR),                     # store amount of gp to add
        asm.STA(0x4202, asm.ABS),                   # store amount of gp to display
        asm.RTS(),
    ]
    space = Write(Bank.C0, src, "load chest scaled gp")
    load_scaled_gp = space.start_address

    space = Reserve(0x04c3b, 0x04c3f, "load chest gp", asm.NOP())
    space.write(
        asm.JSR(load_scaled_gp, asm.ABS),
    )
