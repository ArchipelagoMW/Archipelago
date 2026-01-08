from ..memory.space import Reserve, Write, Bank, Read
from ..instruction import asm as asm
from .. import args as args

class YNPC:
    def __init__(self):
        self.button_check()
        self.interact()

    def button_check(self):
        NPC_INTERACT = 0x472c

        src = [
            asm.LDA(0x06, asm.DIR),     # a = a, x, l, r buttons
            asm.BMI("NPC_INTERACT"),    # branch if a button pressed
            asm.LDA(0x0d, asm.DIR),     # a = b, y, select, start, up, down, left, right buttons
            asm.AND(0x40, asm.IMM8),    # a = y button pressed?
            asm.BNE("NPC_INTERACT"),    # branch if so
            asm.RTS(),

            "NPC_INTERACT",
            asm.JMP(NPC_INTERACT, asm.ABS),
        ]
        space = Write(Bank.C0, src, "npc y button check")
        button_check_address = space.start_address

        if args.y_npc:
            space = Reserve(0x4727, 0x472a, "field button press check", asm.NOP())
            space.write(
                asm.JSR(button_check_address, asm.ABS),
            )

    def interact(self):
        from ..memory.space import START_ADDRESS_SNES
        from ..instruction.field import Y_NPC
        y_npc_event_bytes = (Y_NPC + START_ADDRESS_SNES).to_bytes(3, "little")

        from ..data.characters import Characters
        src = [
            asm.LDA(0x0d, asm.DIR),     # a = b, y, select, start, up, down, left, right buttson
            asm.AND(0x40, asm.IMM8),    # a = y button pressed?
            asm.BEQ("ORIGINAL_EVENT"),  # branch if y button not pressed (i.e. a button pressed)

            asm.LDX(0x1e, asm.DIR),
            asm.LDA(0x7e2000, asm.LNG_X),   # a = npc id * 2
            asm.LSR(),                      # a = npc id

            asm.CMP(Characters.CHARACTER_COUNT, asm.IMM8),
            asm.BLT("ORIGINAL_EVENT"),  # branch if this is a character (e.g. split parties)

            # store id of npc so it can be used later in the event code commands
            asm.STA(0x1187, asm.ABS),   # store npc id in unused field ram

            # set new npc event address
            asm.LDA(y_npc_event_bytes[0], asm.IMM8),
            asm.STA(0xe5, asm.DIR),
            asm.STA(0x05f4, asm.ABS),

            asm.LDA(y_npc_event_bytes[1], asm.IMM8),
            asm.STA(0xe6, asm.DIR),
            asm.STA(0x05f5, asm.ABS),

            asm.LDA(y_npc_event_bytes[2], asm.IMM8),
            asm.STA(0xe7, asm.DIR),
            asm.STA(0x05f6, asm.ABS),

            asm.RTS(),

            "ORIGINAL_EVENT",
            Read(0x4816, 0x4830),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "npc y button pressed")
        interact_address = space.start_address

        if args.y_npc:
            space = Reserve(0x4816, 0x4830, "npc interact", asm.NOP())
            space.write(
                asm.JSR(interact_address, asm.ABS),
            )
