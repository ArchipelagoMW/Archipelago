from ..memory.space import Bank, Allocate, Reserve, Read
from ..instruction import field as field
from ..instruction import asm as asm
from .. import args as args

class Permadeath:
    def __init__(self):
        self.death_mask = field.Status.DEATH >> 8
        self.current_status = 0x1614 # character status effects address

        remove_status_space = Allocate(Bank.C0, 9, "permadeath remove status effects command", asm.NOP())
        heal_hp_space = Allocate(Bank.C0, 16, "permadeath heal hp command", asm.NOP())
        if args.permadeath:
            self.remove_status_mod(remove_status_space)
            self.heal_hp_mod(heal_hp_space)

    def remove_status_mod(self, space):
        # change remove status effects field command to never remove death
        space.write(
            asm.LDA(0xec, asm.DIR),                     # load status effects to keep argument
            asm.ORA(self.death_mask, asm.IMM16),        # add death
            asm.AND(self.current_status, asm.ABS_Y),    # and with character's current status effects
            asm.RTS(),
        )
        remove_status_effects = space.start_address

        space = Reserve(0x0ae37, 0x0ae3b, "permadeath call remove status effects", asm.NOP())
        space.write(
            asm.JSR(remove_status_effects, asm.ABS),
        )

    def heal_hp_mod(self, space):
        # change heal hp field command to not heal hp if character has death status effect
        space.write(
            asm.LDA(self.current_status, asm.ABS_Y),    # a = character's current status effects (high byte)
            asm.BIT(self.death_mask, asm.IMM8),         # death bit set?
            asm.BEQ("HEAL_HP"),                         # branch if not
            asm.JMP(0x0aed3, asm.ABS),                  # otherwise skip healing

            "HEAL_HP",
            Read(0x0ae86, 0x0ae88),                     # $1e = max hp
            asm.JMP(0x0ae89, asm.ABS),                  # return and continue as normal
        )
        death_or_max_hp = space.start_address

        space = Reserve(0x0ae86, 0x0ae88, "permadeath call death or max hp", asm.NOP())
        space.write(
            asm.JMP(death_or_max_hp, asm.ABS),
        )
