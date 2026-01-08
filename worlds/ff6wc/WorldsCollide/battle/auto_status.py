from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Write
from ..instruction import asm as asm

from ..constants import status_effects as status_effects
from ..data import event_bit as event_bit
from .. import objectives as objectives

class _AutoStatus:
    def __init__(self):
        auto_a_status_effects = ["Dark", "Clear", "Imp"]
        auto_b_status_effects = ["Condemned", "Image", "Mute", "Berserk", "Muddle", "Seizure", "Sleep"]
        auto_c_status_effects = ["Float", "Regen", "Slow", "Haste", "Shell", "Safe", "Reflect"]
        auto_d_status_effects = ["Life 3", "Dog Block"]
        auto_phantasm_overcast_status_effects = ["Overcast"]

        auto_addresses = []
        for status in auto_a_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.A))
        for status in auto_b_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.B))
        for status in auto_c_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.C))
        for status in auto_d_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.D))
        for status in auto_phantasm_overcast_status_effects:
            auto_addresses.append(self.auto_status(status, status_effects.PhantasmOvercast))
        

        src = [
            # original replaced code
            asm.LDA(0xbc, asm.DIR),
            asm.STA(0x3c6c, asm.ABS_X),     # store status b granted by equipment
            asm.LDA(0xd4, asm.DIR),
            asm.STA(0x3c6d, asm.ABS_X),     # store status c granted by equipment
        ]

        # auto status effects granted by objectives
        for address in auto_addresses:
            src += [
                asm.JSR(address, asm.ABS),
            ]
        src += [
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "auto status effects")
        auto_status_effects = space.start_address

        space = Reserve(0x228bf, 0x228c8, "equipment status effects", asm.NOP())
        space.write(
            asm.JSL(START_ADDRESS_SNES + auto_status_effects),
        )

        # Ensure that Life 3 can also be applied at the start of battle
        space = Reserve(0x22823, 0x22823, "Only keep Dog Block and Float")
        space.write(0xC4) # Original: 0xC0; also keeping Life 3

    def auto_status(self, status_name, status_effects_group):
        auto_status_name = "Auto " + status_name
        auto_status_name_upper = auto_status_name.upper()

        if status_name == "Float":
            status_bit = 1 << status_effects_group.name_id["Dance"]
        else:
            status_bit = 1 << status_effects_group.name_id[status_name]
        if status_effects_group == status_effects.A:
            status_address = 0x1614
            opcode = asm.ABS_Y
        elif status_effects_group == status_effects.B:
            status_address = 0x3c6c
            opcode = asm.ABS_X
        elif status_effects_group == status_effects.C:
            status_address = 0x3c6d
            opcode = asm.ABS_X
        elif status_effects_group == status_effects.D:
            status_address = 0x1615 
            opcode = asm.ABS_Y
        elif status_effects_group == status_effects.PhantasmOvercast:
            status_address = 0x3e4d
            opcode = asm.ABS_X

        src = []
        if auto_status_name in objectives.results:
            for objective in objectives.results[auto_status_name]:
                objective_event_bit = event_bit.objective(objective.id)
                bit = event_bit.bit(objective_event_bit)
                address = event_bit.address(objective_event_bit)

                src += [
                    asm.LDA(address, asm.ABS),
                    asm.AND(2 ** bit, asm.IMM8),
                    asm.BNE(auto_status_name_upper),
                ]
        src += [
            "NO_ " + auto_status_name_upper,
            asm.RTS(),

            auto_status_name_upper,
        ]
        
        # if the opcode is Y, that means we're accessing the SRAM offset, for which Y is multiples of 37
        if(opcode == asm.ABS_Y):
            src += [
                asm.PHY(), # push current Y
                asm.XY16(), # 16-bit X & Y
                asm.LDY(0x3010, asm.ABS_X) # get the pointer to the character
            ]
        src += [
            asm.LDA(status_address, opcode),
            asm.ORA(status_bit, asm.IMM8),
            asm.STA(status_address, opcode),
        ]
        if(opcode == asm.ABS_Y):
            src += [
                asm.XY8(), # revert back to 8-bit X&Y
                asm.PLY(), # pull original Y
            ]
        src += [
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, auto_status_name)
        return space.start_address
auto_status = _AutoStatus()
