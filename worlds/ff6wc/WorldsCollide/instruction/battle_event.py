from ..memory.space import START_ADDRESS_SNES, Bank, Reserve, Free, Write, Read
from ..instruction.event import _Instruction
from ..instruction import asm as asm
from ..instruction import c1 as c1

def _set_opcode_address(opcode, address):
    opcode_table_address = 0x1fdbe + opcode * 2
    space = Reserve(opcode_table_address, opcode_table_address + 1, "battle event table, {opcode} {hex(address)}")
    space.write(
        (address & 0xffff).to_bytes(2, "little"),
    )

def _add_remove_entity_mod():
    # move to a different part of c1 to allow increasing size of battle event opcode table
    src = [
        Read(0x1fde8, 0x1fdec),
    ]
    space = Write(Bank.C1, src, "c1 add remove entity")
    _set_opcode_address(0x13, space.start_address)
_add_remove_entity_mod()

class NOP(_Instruction):
    def __init__(self):
        super().__init__(0x02)

class End(_Instruction):
    def __init__(self):
        super().__init__(0xff)

class AddTarget(_Instruction):
    def __init__(self, entity_id):
        self.entity_id = entity_id
        super().__init__(0x13, entity_id & 0x7f)

    def __str__(self):
        return super().__str__(self.entity_id)

class RemoveTarget(_Instruction):
    def __init__(self, entity_id):
        self.entity_id = entity_id
        super().__init__(0x13, entity_id | 0x80)

    def __str__(self):
        return super().__str__(self.entity_id)

FIRST_CHARACTER_ANIMATION_SLOT = 3
LAST_CHARACTER_ANIMATION_SLOT = 6
_character_animation_slot = FIRST_CHARACTER_ANIMATION_SLOT
class AddCharacterAnimation(_Instruction):
    def __init__(self, character, address):
        global LAST_CHARACTER_ANIMATION_SLOT, _character_animation_slot
        self.character = character
        self.address = address
        self.slot = _character_animation_slot

        super().__init__(self.slot, self.character, (self.address & 0xffff).to_bytes(2, "little"))
        _character_animation_slot += 1
        assert _character_animation_slot <= LAST_CHARACTER_ANIMATION_SLOT

    def __str__(self):
        return super().__str__(f"{self.slot - 3} {self.character} {hex(self.address)}")

class ClearAnimations(_Instruction):
    def __init__(self):
        super().__init__(0x0e)

class ExecuteAnimations(_Instruction):
    def __init__(self):
        global FIRST_CHARACTER_ANIMATION_SLOT, _character_animation_slot
        super().__init__(0x0f)
        _character_animation_slot = FIRST_CHARACTER_ANIMATION_SLOT

class OpenMultiLineDialogWindow(_Instruction):
    def __init__(self):
        super().__init__(0x11)

class CloseMultiLineDialogWindow(_Instruction):
    def __init__(self):
        super().__init__(0x10)

class DisplaySingleLineDialog(_Instruction):
    def __init__(self, dialog_id):
        super().__init__(0x00, dialog_id)

class DisplayMultiLineDialog(_Instruction):
    def __init__(self, dialog_id):
        super().__init__(0x01, dialog_id)

class IncrementChecksComplete(_Instruction):
    def __init__(self):
        from ..data import event_word as event_word
        checks_complete_address = event_word.address(event_word.CHECKS_COMPLETE)

        src = [
            asm.INC(checks_complete_address, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.C1, src, "battle event increment checks complete command")
        address = space.start_address

        opcode = 0x15
        _set_opcode_address(opcode, address)

        IncrementChecksComplete.__init__ = lambda self : super().__init__(opcode)
        self.__init__()
