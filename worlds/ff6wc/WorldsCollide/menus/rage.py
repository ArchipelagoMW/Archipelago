from ..memory.space import Bank, Reserve, Allocate, Write
from ..instruction import asm as asm
from ..data.spell_names import name_id, id_name


class RageMenu:
    def __init__(self, rages, enemies):
        self.rages = rages
        self.enemies = enemies

        # Build an array to lookup enemy-specific Special command effects
        from ..constants.status_effects import A, B, C, D
        self.status_effects = []
        self.status_effects.extend(list(A.id_name.values()))
        self.status_effects.extend(list(B.id_name.values()))
        self.status_effects.extend(list(C.id_name.values()))
        self.status_effects.extend(list(D.id_name.values()))

        # Remove death from the status effects list, as it requires a second bit from flags1 
        self.status_effects = list(map(lambda x: x.replace("Death", ""), self.status_effects))

        # Remove other statuses that aren't really relevant
        self.status_effects = list(map(lambda x: x.replace("Near Fatal", ""), self.status_effects))
        self.status_effects = list(map(lambda x: x.replace("Hide", ""), self.status_effects))

        self.special_effects = []  
        self.special_effects.extend(self.status_effects)
        for i in range(15, 95, 5): # going from 1.5x - 9.0x damage
            dmg_multiplier = i / 10
            self.special_effects.append(f"{dmg_multiplier:.1f}x dmg")
        self.special_effects.append("Drain HP")
        self.special_effects.append("Drain MP")
        self.special_effects.append("Remove Reflect")

        self.mod()

    def get_rage_string(self, id, attack_id):
        from ..data.spell_names import id_name, name_id

        if attack_id == name_id["Special"]:
            # handle special name lookup + special attack info (dmg multipler, status effect)
            enemy = self.enemies.enemies[id]
            special_name = enemy.special_name
            special_effect = enemy.special_effect

            rage_str = f"{special_name}: "
            rage_str += self.special_effects[special_effect]
        else:
            rage_str = f"{id_name[attack_id]}"

        # # remove duplicate white spaces
        import re
        rage_str = re.sub(' +', ' ', rage_str)

        # remove leading and trailing spaces
        rage_str = rage_str.strip()
        return rage_str

    def draw_ability_names_mod(self):
        from ..data import text as text

        # Get the custom strings for each rage to be written to the ROM
        lines = []
        for rage in self.rages.rages:
            # Only focusing on attack2, as attack1 is simply "Battle" -- if that changes in the future, this string can be revisited
            rage_str = f"{self.get_rage_string(rage.id, rage.attack2)}<end>"
            lines.append(rage_str)

        line_offsets = [0]
        running_offset = 0
        # Write the lines to F0
        src = []
        for line in lines:
            # convert to bytes
            bytes = text.get_bytes(line, text.TEXT3)
            running_offset += len(bytes)
            line_offsets.append(running_offset)
            src.append(bytes)
        space = Write(Bank.F0, src, "rage description lines table")
        lines_table = space.start_address_snes

        # write the 2-byte line offsets to F0
        src = []
        for offset in line_offsets:
            src.append(offset.to_bytes(2, 'little'))
        space = Write(Bank.F0, src, "rage description lines table offsets")
        lines_table_offsets = space.start_address_snes

        src = [
            asm.LDX(0x9ec9, asm.IMM16),     # dest WRAM LBs
            asm.STX(0x2181, asm.ABS),       # store dest WRAM LBs

            asm.TDC(),                      # a = 0x0000
            asm.LDA(0x4b, asm.DIR),         # a = cursor index (rage index)
            asm.TAX(),                      # x = cursor index (rage index)
            asm.LDA(0x7e9d89, asm.LNG_X),   # a = rage at cursor index
            asm.CMP(0xff, asm.IMM8),        # compare with no rage
            asm.BEQ("END_STRING_RETURN"),   # branch if rage at cursor index not learned
            asm.A16(),
            asm.ASL(),                      # a = rage index * 2 (2 bytes per table offset)
            asm.TAX(),                      # x = rage index * 2 
            asm.LDA(lines_table_offsets, asm.LNG_X), # get the offset
            asm.TAX(),
            asm.A8(),
            "STRING_LOOP_START",
            asm.LDA(lines_table, asm.LNG_X), # get the character
            asm.STA(0x2180, asm.ABS),        # add character to string
            asm.CMP(0x00, asm.IMM8),         # was it the end of the string? 
            asm.BEQ("RETURN"),               # if so, be done
            asm.INX(),                       # move to next character in ability name
            asm.BRA("STRING_LOOP_START"),    
            "END_STRING_RETURN",
            asm.STZ(0x2180, asm.ABS),       # end string
            "RETURN",
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "draw ability names")
        draw_ability_names = space.start_address

        sustain_replace = 0x328c6   # handle L and R
        replace_size = 3            # replacing jsr instructions

        src = [
            asm.LDA(0x10, asm.IMM8),# enable description menu flag bitmask
            asm.TRB(0x45, asm.DIR), # enable descriptions
            asm.JSR(0x4c52, asm.ABS),  # displaced code: handle D-Pad
            asm.JMP(draw_ability_names, asm.ABS),
        ]
        space = Write(Bank.C3, src, "sustain rage list")
        sustain_rage_list = space.start_address

        space = Reserve(sustain_replace, sustain_replace + replace_size - 1, "rage menu sustain handle D-Pad")
        space.write(
            asm.JSR(sustain_rage_list, asm.ABS),
        )

    def mod(self):
        self.draw_ability_names_mod()