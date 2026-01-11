from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Write, Read
from ..instruction import asm as asm

from ..data import event_bit as event_bit
from .. import objectives as objectives

class _MagitekUpgrade:
    '''Set the Magitek menu in battle to match the Magitek Upgrade objective result.'''
    def __init__(self):
        # Write our 2 magitek tables
        # We're moving them from C1/910C - C1/911B
        # Default: Match Regular character's default
        src = [
            0x00, 0x01, #FIRE_BEAM, BOLT_BEAM, 
            0x02, 0xFF, #ICE_BEAM, <empty>, 
            0x04, 0xFF, #HEAL_FORCE, <empty>, 
            0xFF, 0xFF  #<empty>, <empty>
        ]
        space = Write(Bank.F0, src, "magitek default table")
        magitek_default_table_addr = space.start_address

        # Upgraded: Match Terra's options
        src = [
            0x00, 0x01, #FIRE_BEAM, BOLT_BEAM,
            0x02, 0x03, #ICE_BEAM, BIO_BLAST, 
            0x04, 0x05, #HEAL_FORCE, CONFUSER, 
            0x06, 0x07  #X_FER, TEKMISSILE
        ]
        space = Write(Bank.F0, src, "magitek upgraded table")
        magitek_upgraded_table_addr = space.start_address

        # Write our modifications to the C1 routines that use the 
        # magitek tables.
        # There are 2 that use the magitek tables in C1:
        #  1) C1/4D42 - C1/4D6D builds the magitek menu by writing to $575A & $5760
        #  2) C1/866A - C1/8683 used when selecting from the menu - 
        #                stores the menu option in A. 
        self.magitek_upgrade_name = "Magitek Upgrade"
        magitek_upgrade_name_upper = self.magitek_upgrade_name.upper()

        # 1) Build the magitek menu
        branch_name = f"{magitek_upgrade_name_upper}_MENU"
        src = self.get_branch_if_objective_complete_src(branch_name)
        src += [
            f"NO_{branch_name}",
            asm.LDA(START_ADDRESS_SNES + magitek_default_table_addr, asm.LNG_X),
            asm.STA(0x575A, asm.ABS),
            asm.LDA(START_ADDRESS_SNES + magitek_default_table_addr + 1, asm.LNG_X),
            asm.STA(0x5760, asm.ABS),
            asm.RTL(),
            branch_name,
            asm.LDA(START_ADDRESS_SNES + magitek_upgraded_table_addr, asm.LNG_X),
            asm.STA(0x575A, asm.ABS),
            asm.LDA(START_ADDRESS_SNES + magitek_upgraded_table_addr + 1, asm.LNG_X),
            asm.STA(0x5760, asm.ABS),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "build magitek menu")
        build_magitek_menu_addr = space.start_address

        space = Reserve(0x14d42, 0x14d6d, "build magitek menu jsl", asm.NOP())
        space.write(
            asm.JSL(START_ADDRESS_SNES + build_magitek_menu_addr),
        )

        # 2) Select from the magitek menu
        branch_name = f"{magitek_upgrade_name_upper}_SELECT"
        src = self.get_branch_if_objective_complete_src(branch_name)
        src += [
            f"NO_{branch_name}",
            asm.LDA(START_ADDRESS_SNES + magitek_default_table_addr, asm.LNG_X),
            asm.RTL(),
            branch_name,
            asm.LDA(START_ADDRESS_SNES + magitek_upgraded_table_addr, asm.LNG_X),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "select from magitek menu")
        select_from_magitek_menu_addr_snes = space.start_address_snes

        space = Reserve(0x1866a, 0x18683, "select from magitek menu jsl", asm.NOP())
        space.write(
            asm.JSL(select_from_magitek_menu_addr_snes),
        )

    def get_branch_if_objective_complete_src(self, branch_name):
        src = []
        if self.magitek_upgrade_name in objectives.results:
            for objective in objectives.results[self.magitek_upgrade_name]:
                objective_event_bit = event_bit.objective(objective.id)
                bit = event_bit.bit(objective_event_bit)
                address = event_bit.address(objective_event_bit)

                src += [
                    asm.LDA(address, asm.ABS),
                    asm.AND(2 ** bit, asm.IMM8),
                    asm.BNE(branch_name),
                ]
        return src

magitek_upgrade = _MagitekUpgrade()

