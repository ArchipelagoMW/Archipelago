from ....memory.space import Bank, Reserve, Write, Read
from ....instruction.event import _Instruction
from ....instruction import asm as asm
from ....instruction import c0 as c0

from enum import IntEnum
from ....instruction.field.custom import _set_opcode_address

# set graphics for last npc interacted with using y button
# if sprite, palette, or vehicle argument is 0xff, they will remain unmodified (TODO: 0xff restore original values?)
class SetYNPCGraphics(_Instruction):
    def __init__(self, sprite, palette, vehicle):
        src = [
            # store sprite as 4th argument (so eb can be overwritten)
            asm.LDA(0xeb, asm.DIR),         # a = sprite argument
            asm.PHA(),
            asm.LDA(0xec, asm.DIR),         # a = palette argument
            asm.PHA(),

            asm.LDA(0x1187, asm.ABS),       # a = npc id
            asm.STA(0xeb, asm.DIR),         # $eb = npc id

            asm.LDA(0xed, asm.DIR),         # a = vehicle argument
            asm.CMP(0xff, asm.IMM8),        # compare vehicle argument with 0xff
            asm.BEQ("SET_PALETTE"),         # if equal, skip changing vehicle

            asm.STA(0xec, asm.DIR),         # $ec = vehicle argument
            asm.JSR(c0.set_vehicle, asm.ABS),

            "SET_PALETTE",
            asm.PLA(),                      # a = palette argument
            asm.CMP(0xff, asm.IMM8),        # compare palette argument with 0xff
            asm.BEQ("SET_SPRITE"),          # if equal, skip changing palette

            asm.STA(0xec, asm.DIR),         # $ec = palette argument
            asm.JSR(c0.set_palette, asm.ABS),

            "SET_SPRITE",
            asm.PLA(),                      # a = sprite argument
            asm.CMP(0xff, asm.IMM8),        # compare palette argument with 0xff
            asm.BEQ("EXIT"),                # if equal, skip changing sprite

            asm.STA(0xec, asm.DIR),         # $ec = sprite argument
            asm.JSR(c0.set_sprite, asm.ABS),

            "EXIT",
            asm.LDA(0x04, asm.IMM8),        # command size
            asm.JMP(0x9b5c, asm.ABS),       # next command
        ]
        space = Write(Bank.C0, src, "custom set_y_npc_graphics command")
        address = space.start_address

        opcode = 0x9e
        _set_opcode_address(opcode, address)

        SetYNPCGraphics.__init__ = (lambda self, sprite, palette, vehicle :
                                    super().__init__(opcode, sprite, palette, vehicle))
        self.__init__(sprite, palette, vehicle)

    def __str__(self):
        return super().__str__(f"{self.args[0]}, {self.args[1]}, {self.args[2]}")

# apply various effects to last npc interacted with using y button
class YEffect(IntEnum):
    SHOW                = 0x00
    HIDE                = 0x01
    STOP                = 0x02
    DELETE              = 0x03
    REFLECT             = 0x04
    RANDOM_GRAPHIC      = 0x05
    ANY_RANDOM_GRAPHIC  = 0x06 # includes glitchy graphics
class YNPCEffect(_Instruction):
    def __init__(self, effect):
        src = [
            asm.TDC(),                      # clear a
            asm.LDA(0xeb, asm.DIR),         # a = npc id
            asm.ASL(),                      # a = npc id * 2
            asm.TAX(),                      # x = npc id * 2
            asm.LDY(0x0799, asm.ABS_X),     # y = pointer to npc data = npc id * 0x29
            asm.LSR(),                      # a = npc id
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect get_npc_id")
        get_npc_id = space.start_address

        # npc ids on map stored at 0x7e2000 to 0x7e5fff
        # down/up are +/- 0x100, so for adjacent check 2 tiles left/right and up/down
        adjacent = [
            0x00, 0x00, # 0                 # current tile
            0x01, 0x00, # +1                # right 1
            0x02, 0x00, # +2                # right 2
            0xff, 0xff, # -1                # left 1
            0xfe, 0xff, # -2                # left 2
            0x00, 0x01, # +100              # down 1
            0x00, 0x02, # +200              # down 2
            0x00, 0xff, # -100              # up 1
            0x00, 0xfe, # -200              # up 2
        ]
        space = Write(Bank.C0, adjacent, "custom y_npc_effect adjacent_tiles")
        adjacent_tiles = space.start_address

        # if hide/delete an npc in the middle of moving from one tile to the next
        # the npc can be on two tiles but hide/delete will only delete the one pointed to at $087a
        # check current and adjacent tiles for the npc id and delete if found
        src = [
            asm.PHP(),
            asm.A16(),
            asm.PHA(),
            asm.PHY(),
            asm.LDY(0x0000, asm.IMM16),         # initialize adjacent_tiles index

            "ADJACENT_LOOP_START",
            asm.PHX(),                          # push address of npc tile (offset to 0x7e2000)
            asm.TXA(),                          # a = address of npc tile
            asm.ADC(adjacent_tiles, asm.ABS_Y), # a = address of adjacent tile
            asm.CMP(0x4000, asm.IMM16),         # prevent accessing memory beyond map objects (>= 0x7e6000)
            asm.BGE("NEXT_TILE"),               # branch if out of bounds
            asm.TAX(),
            asm.A8(),
            asm.LDA(0x7e2000, asm.LNG_X),       # a = object id at current tile
            asm.CMP(0xeb, asm.DIR),             # compare to npc id
            asm.BNE("NEXT_TILE"),               # branch if npc not at this tile
            asm.LDA(0xff, asm.IMM8),            # a = 0xff (no npc id)
            asm.STA(0x7e2000, asm.LNG_X),       # remove npc from this tile

            "NEXT_TILE",
            asm.A16(),
            asm.PLX(),                          # pop address of npc tile
            asm.INY(),
            asm.INY(),                          # y += 2 (2 bytes per adjacent offset)
            asm.CPY(len(adjacent), asm.IMM16),  # compare with number of tiles to check
            asm.BNE("ADJACENT_LOOP_START"),     # branch if not done

            asm.PLY(),
            asm.PLA(),
            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect delete_collision")
        delete_collision = space.start_address

        src = [
            asm.JSR(get_npc_id, asm.ABS),
            asm.LDX(0x087a, asm.ABS_Y),         # x = pointer to npc in map data
            asm.ASL(0xeb, asm.DIR),             # $eb = npc id * 2

            # vanilla hide/delete object functions do not completely remove npcs if
            # they are in the middle of walking, call delete_collision to fix this
            asm.JSR(delete_collision, asm.ABS),

            asm.LSR(0xeb, asm.DIR),             # $eb = npc id
            asm.JSR(c0.hide_object, asm.ABS),   # hide object
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect delete")
        delete = space.start_address

        from ....instruction.event import EVENT_CODE_START
        from ....instruction.field.functions import RETURN
        return_event = (RETURN - EVENT_CODE_START).to_bytes(3, "little")
        src = [
            asm.JSR(get_npc_id, asm.ABS),

            # set npc event to just return
            asm.LDA(return_event[0], asm.IMM8),
            asm.STA(0x0889, asm.ABS_Y),
            asm.LDA(return_event[1], asm.IMM8),
            asm.STA(0x088a, asm.ABS_Y),
            asm.LDA(return_event[2], asm.IMM8),
            asm.STA(0x088b, asm.ABS_Y),

            asm.LDA(0x087c, asm.ABS_Y),         # a = object movement
            asm.AND(0xf0, asm.IMM8),            # clear movement bits (stop movement)
            asm.ORA(0x20, asm.IMM8),            # disable facing player during interaction
            asm.STA(0x087c, asm.ABS_Y),         # store object movement

            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect stop")
        stop = space.start_address

        src = [
            asm.LDY(0x0803, asm.ABS),           # y = party leader object pointer = party leader id * 0x29
            asm.PHY(),
            asm.LDA(0x0879, asm.ABS_Y),         # a = party leader graphic index
            asm.STA(0xec, asm.DIR),             # $ec = sprite
            asm.JSR(c0.set_sprite, asm.ABS),
            asm.PLY(),

            asm.LDA(0x0880, asm.ABS_Y),         # a = party leader palette index
            asm.LSR(),
            asm.AND(0x07, asm.IMM8),            # palette mask 0000 1110
            asm.STA(0xec, asm.DIR),             # $ec = palette
            asm.JSR(c0.set_palette, asm.ABS),

            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect reflect")
        reflect = space.start_address

        effects = [
            c0.show_object.to_bytes(2, "little"),
            c0.hide_object.to_bytes(2, "little"),
            stop.to_bytes(2, "little"),
            delete.to_bytes(2, "little"),
            reflect.to_bytes(2, "little"),
            c0.random_sprite_palette.to_bytes(2, "little"),
            c0.any_random_sprite_palette.to_bytes(2, "little"),
        ]
        space = Write(Bank.C0, effects, "custom y_npc_effect effects")
        effects_table = space.start_address

        src = [
            asm.LDA(0xeb, asm.DIR),             # a = effect argument
            asm.PHA(),
            asm.LDA(0x1187, asm.ABS),           # a = npc id
            asm.STA(0xeb, asm.DIR),             # $eb = npc id (overwrite effect argument)
            asm.PLA(),                          # a = effect argument

            asm.ASL(),                          # a = effect index * 2 (2 bytes per table entry)
            asm.TAX(),                          # x = effect index * 2
            asm.JSR(effects_table, asm.ABS_X_16),   # call effect function

            asm.LDA(0x02, asm.IMM8),            # command size
            asm.JMP(0x9b5c, asm.ABS),           # next command
        ]
        space = Write(Bank.C0, src, "custom y_npc_effect command")
        address = space.start_address

        opcode = 0x9f
        _set_opcode_address(opcode, address)

        YNPCEffect.__init__ = lambda self, effect : super().__init__(opcode, effect)
        self.__init__(effect)

    def __str__(self):
        return super().__str__(self.args[0])

