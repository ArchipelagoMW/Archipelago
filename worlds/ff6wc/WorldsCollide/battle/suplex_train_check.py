from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Write
from ..instruction import asm as asm
from ..data import event_bit as event_bit

from ..data.spell_names import name_id as spell_name_id
from ..data.bosses import name_formation

class _SuplexTrainCheck:
    def __init__(self):
        formation_address = 0x3ed4
        train_formation = name_formation["GhostTrain"]
        suplex_id = spell_name_id["Suplex"]
        src = [
            asm.A16(),
            asm.PHA(),
            asm.A8(),
            asm.CMP(suplex_id, asm.IMM8),
            asm.BNE("RETURN"), # return if not suplex

            asm.A16(),
            asm.LDA(formation_address, asm.ABS),
            asm.CMP(train_formation, asm.IMM16),
            asm.BNE("RETURN"), # return if not train formation

            asm.A8(),
            asm.LDA(event_bit.address(event_bit.SUPLEXED_TRAIN), asm.ABS),
            asm.ORA(2 ** event_bit.bit(event_bit.SUPLEXED_TRAIN), asm.IMM8),
            asm.STA(event_bit.address(event_bit.SUPLEXED_TRAIN), asm.ABS), # set event bit

            "RETURN",
            asm.A16(),
            asm.PLA(),
            asm.A8(),
            asm.LDA(0x08, asm.IMM8),
            asm.STA(0x3412, asm.ABS),   # set flag to display blitz name at top of screen
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "blitz suplex a train check")
        suplex_train_check = space.start_address

        space = Reserve(0x215b0, 0x215b4, "if successful blitz, check if suplexing train", asm.NOP())
        space.write(
            asm.JSL(START_ADDRESS_SNES + suplex_train_check),
        )
suplex_train_check = _SuplexTrainCheck()
