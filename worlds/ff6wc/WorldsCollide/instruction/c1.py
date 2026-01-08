from ..memory.space import START_ADDRESS_SNES, Bank, Reserve, Free, Write, Read
from ..instruction import asm as asm

def _color_absolute_addition_mod():
    from ..instruction import f0 as f0

    # move to f0 to make room in c1
    space = Reserve(0x1fd00, 0x1fd04, "c1 color absolute addition")
    space.write(
        asm.JSL(START_ADDRESS_SNES + f0.color_absolute_addition),
        asm.RTS(),
    )
    Free(space.end_address + 1, 0x1fd66)
color_absolute_addition = _color_absolute_addition_mod()

def _color_absolute_subtraction_mod():
    from ..instruction import f0 as f0

    # move to f0 to make room in c1
    space = Reserve(0x1fc99, 0x1fc9d, "c1 color absolute subtraction")
    space.write(
        asm.JSL(START_ADDRESS_SNES + f0.color_absolute_subtraction),
        asm.RTS(),
    )
    Free(space.end_address + 1, 0x1fcff)
color_absolute_subtraction = _color_absolute_subtraction_mod()

def _display_multi_line_dialog_mod():
    # input: x = dialog id * 2
    src = [
        asm.PHX(),
        Read(0x196c1, 0x196cc),

        # 981a loads the multi line dialog id from the next battle event byte
        # however, we cannot hardcode the dialog id as an argument because it must be displayed conditionally for objectives
        # instead, dialog id * 2 is in the x register and do not read/increment event queue
        asm.PLX(),
        asm.LDA(0xd0, asm.IMM8),        # a = 0xd0 = multi line dialog offset bank
        asm.STA(0x88d9, asm.ABS),
        asm.A16(),
        asm.LDA(0xd0d000, asm.LNG_X),   # a = multi line dialog ptr
        asm.STA(0x88d7, asm.ABS),
        asm.TDC(),
        asm.A8(),
        asm.JSR(0x96cd, asm.ABS),       # finish displaying multi line battle dialog
        asm.RTL(),
    ]
    space = Write(Bank.C1, src, "battle event display multi line dialog")
    return space.start_address
display_multi_line_dialog = _display_multi_line_dialog_mod()
