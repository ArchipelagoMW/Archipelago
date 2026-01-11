from ..data.control import Control
from ..data.structures import DataArray
from ..memory.space import Reserve, Allocate, Bank, Write
from ..instruction import asm as asm

class Controls():
    ATTACKS_DATA_START = 0xf3d00
    ATTACKS_DATA_END = 0xf42ff
    ATTACKS_DATA_SIZE = 4
    ATTACKS_DATA_TOTAL_BYTES = (ATTACKS_DATA_END - ATTACKS_DATA_START) + 1

    def __init__(self, rom, args, enemies, rages):
        self.rom = rom
        self.args = args
        self.enemies = enemies
        self.rages = rages

        # Copy the vanilla table to a new location, so that any modifications do not affect Coliseum/Muddle behavior
        self.new_attack_data_space = Allocate(Bank.F0, self.ATTACKS_DATA_TOTAL_BYTES, "new Controls table")
        self.new_attack_data_space.copy_from(self.ATTACKS_DATA_START, self.ATTACKS_DATA_END)

        self.attack_data = DataArray(self.rom, self.new_attack_data_space.start_address, self.new_attack_data_space.end_address, self.ATTACKS_DATA_SIZE)

        self.controls = []
        for control_index in range(len(self.attack_data)):
            control = Control(control_index, self.attack_data[control_index])
            self.controls.append(control)

    def split_control_table(self):
        # Update the vanilla lookup of the table for Control commands
        # Default: LDA $CF3D00,X
        space = Reserve(0x23758, 0x2375B, "get Control command table")
        space.write(
            asm.LDA(self.new_attack_data_space.start_address_snes, asm.LNG_X)
        )

    def ignore_randomize_target(self):
        # Ignoring Randomize Target bit when Control is used, to ensure that those commands respect the selected targetting
        # This is a bug-fix for a vanilla bug, in which Controlled Dance abilities (ex: Sandstorm) swap targetting.
        src = [ 
            asm.LDA(0x3A7A, asm.ABS), # load the command
            asm.CMP(0x0E, asm.IMM8),  # is it Control?
            asm.BEQ("exit"),          # if so, skip over displaced code
            # displaced code from C2/276A - C2/2771 to read the "Randomize target bit" and set the equivalent in $BA
            asm.LDA(0x01, asm.S),
            asm.AND(0x10, asm.IMM8),
            asm.ASL(),
            asm.ASL(),
            asm.TSB(0xBA, asm.DIR),
            "exit",
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "Control: ignore Randomize Target bit")
        ignore_randomize_target_addr = space.start_address

        # Call our new subroutine 
        space = Reserve(0x2276A, 0x22771, "control: call ignore randomize target bit subroutine", asm.NOP())
        space.write(
            asm.JSR(ignore_randomize_target_addr, asm.ABS)
        )

    def enable_control_casters_stats(self):
        src = [
            # X = entity using command (in Control case, this is the monster being controlled)
            asm.LDA(0x32B9,asm.ABS_X),    # who's Controlling this entity?
            asm.CMP(0xFF, asm.IMM8),
            asm.BEQ("exit"),              # branch if nobody controls them
            asm.TAX(),                    # if there's a valid Controller, use their stats (vigor/magic/level)
            asm.LDA(0x11A2, asm.ABS),     #Spell Properties
            asm.LSR(),                    #Check if Physical/Magical
            asm.LDA(0x3B41, asm.ABS_X),   #Controller's Mag.Pwr
            asm.BCC("magical"),           #Branch if not physical damage
            asm.LDA(0x3B2C, asm.ABS_X),   #Controller's Vigor * 2
            "magical",
            asm.STA(0x11AE, asm.ABS),     #Set Controller's Magic or Vigor
            "exit",
            asm.LDA(0x3B18, asm.ABS_X),   # displaced code: get Level
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "Controller Caster Stats")
        use_controller_stats_addr = space.start_address

        # Call our new subroutine
        space = Reserve(0x22c28, 0x22c2A, "jump to new routine")
        space.write(
            asm.JSR(use_controller_stats_addr, asm.ABS)
        )

    def enable_control_chances_always(self):
        # Always Control if the target is valid
        # NOPing the JSR and BCS that can prevent Control from working
        space = Reserve(0x023ae8, 0x023aec, "control always", asm.NOP())

    def enable_control_improved_abilities(self):
        from ..data.spell_names import name_id
        # Ensure that Rage & Special are available (if there are open Controls)
        for control in self.controls:
            # Search for blanks, rages, and specials
            index_of_blank = self.ATTACKS_DATA_SIZE # default to end
            control_has_rage = False
            control_has_special = False
            for attack_index, attack in enumerate(control.attack_data()):
                # Look for the first blank entry
                if index_of_blank == self.ATTACKS_DATA_SIZE and attack == name_id["??????????"]:
                    index_of_blank = attack_index
                # Look for a rage
                if control.id < self.rages.RAGE_COUNT: # Enemy has a rage
                    if attack == self.rages.rages[control.id].attack2 and not control_has_rage:
                        control_has_rage = True
                else:
                    control_has_rage = True # no rages to have
                # Look for a special
                if attack == name_id["Special"] and not control_has_special:
                    control_has_special = True

            # If we found that it doesn't have a rage and there's room, add the rage
            if not control_has_rage and index_of_blank < self.ATTACKS_DATA_SIZE:
                control.attack_data_array[index_of_blank] = self.rages.rages[control.id].attack2
                # Avoid duplicate Specials if Rage == Special
                if control.attack_data_array[index_of_blank] == name_id["Special"]:
                    control_has_special = True
                index_of_blank = index_of_blank + 1

            # If we found that it doesn't have a Special and there's room, add the Special
            if not control_has_special and index_of_blank < self.ATTACKS_DATA_SIZE:
                control.attack_data_array[index_of_blank] = name_id["Special"]
                index_of_blank = index_of_blank + 1

    def mod(self):

        self.ignore_randomize_target()

        if self.args.sketch_control_improved_stats:
            self.enable_control_chances_always()
            self.enable_control_casters_stats()
        if self.args.sketch_control_improved_abilities:
            self.split_control_table()
            self.enable_control_improved_abilities()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for control_index, control in enumerate(self.controls):
            self.attack_data[control_index] = control.attack_data()

        self.attack_data.write()

    def log(self):
        pass

    def print(self):
        for control in self.controls:
            control.print()
