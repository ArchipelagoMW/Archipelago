from __future__ import annotations

import dataclasses as _dataclasses
import struct as _struct
import typing as _typing


def _pack(*args):
    return _struct.pack(*args)


JumpTarget = _typing.Union[str, int]


@_dataclasses.dataclass(frozen=True)
class Register:
    number: int


class GeneralRegister(Register):
    def __repr__(self):
        return f"r{self.number}"


class FloatRegister(Register):
    def __repr__(self):
        return f"f{self.number}"


class BaseInstruction:
    label: str | None
    name: str | None = None

    def __init__(self):
        self.label = None

    def with_label(self, label: str) -> BaseInstruction:
        self.label = label
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def bytes_for(self, address: int, symbols: dict[str, int]):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    @property
    def byte_count(self):
        raise NotImplementedError()


class Instruction(BaseInstruction):
    value: int

    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def bytes_for(self, address: int, symbols: dict[str, int]):
        return iter(_pack(">I", self.value))

    def __eq__(self, other):
        return isinstance(other, Instruction) and self.value == other.value

    def __repr__(self):
        if self.name is None:
            return f"<{self.value:08x}>"
        return f"<{self.name}>"

    @property
    def byte_count(self):
        return 4

    @classmethod
    def compose(cls, data: tuple[tuple[int, int, bool], ...]):
        value = 0
        bits_left = 32
        for item, bit_size, signed in data:
            bits_left -= bit_size
            if signed:
                assert -(1 << (bit_size - 1)) <= item < (1 << (bit_size - 1))
                if item < 0:
                    item += (1 << bit_size)
            else:
                assert 0 <= item < (1 << bit_size)
            value += item << bits_left

        assert bits_left == 0
        return cls(value)


class AddressDependantInstruction(BaseInstruction):
    def __init__(self, factory: _typing.Callable[[int], tuple[tuple[int, int, bool], ...]]):
        super().__init__()
        self.factory = factory

    def bytes_for(self, address: int, symbols: dict[str, int]):
        yield from Instruction.compose(self.factory(address)).bytes_for(address, symbols=symbols)

    def __eq__(self, other):
        return isinstance(other, AddressDependantInstruction) and self.factory == other.factory

    @property
    def byte_count(self):
        return 4


class RelativeAddressInstruction(BaseInstruction):
    def __init__(self,
                 address_or_symbol: JumpTarget,
                 factory: _typing.Callable[[int, int], tuple[tuple[int, int, bool], ...]]):
        super().__init__()
        self.address_or_symbol = address_or_symbol
        self.factory = factory

    def concrete_instruction(self, instruction_address: int, symbols: dict[str, int]) -> Instruction:
        if isinstance(self.address_or_symbol, str):
            address = symbols[self.address_or_symbol]
        else:
            address = self.address_or_symbol
        return Instruction.compose(self.factory(address, instruction_address))

    def bytes_for(self, instruction_address: int, symbols: dict[str, int]):
        instruction = self.concrete_instruction(instruction_address, symbols=symbols)
        yield from instruction.bytes_for(instruction_address, symbols=symbols)

    def __eq__(self, other):
        return isinstance(other, RelativeAddressInstruction) and (self.factory == other.factory and
                                                                  self.address_or_symbol == other.address_or_symbol)

    def __repr__(self):
        if self.name is None:
            return f"<relative: {self.address_or_symbol} - {self.factory}>"
        return f"<{self.name}>"

    @property
    def byte_count(self):
        return 4


r0 = GeneralRegister(0)
r1 = GeneralRegister(1)
r2 = GeneralRegister(2)
r3 = GeneralRegister(3)
r4 = GeneralRegister(4)
r5 = GeneralRegister(5)
r6 = GeneralRegister(6)
r7 = GeneralRegister(7)
r8 = GeneralRegister(8)
r9 = GeneralRegister(9)
r10 = GeneralRegister(10)
r11 = GeneralRegister(11)
r12 = GeneralRegister(12)
r13 = GeneralRegister(13)
r25 = GeneralRegister(25)
r26 = GeneralRegister(26)
r27 = GeneralRegister(27)
r28 = GeneralRegister(28)
r29 = GeneralRegister(29)
r30 = GeneralRegister(30)
r31 = GeneralRegister(31)

f0 = FloatRegister(0)
f1 = FloatRegister(1)
f2 = FloatRegister(2)
f3 = FloatRegister(3)

# Special Registers
LR = 8
CTR = 9


def lmw(start_register: GeneralRegister, offset: int, input_register: GeneralRegister):
    return Instruction.compose(((46, 6, False),
                                (start_register.number, 5, False),
                                (input_register.number, 5, False),
                                (offset, 16, True)))


def lwz(output_register: GeneralRegister, offset: int, input_register: GeneralRegister):
    """
    *(output_register + offset) = input_register
    """
    return Instruction.compose(((32, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (offset, 16, True))).with_name(f"lwz {output_register}, 0x{offset:x}({input_register})")


def lwzx(output_register: GeneralRegister, input_register_a: GeneralRegister, input_register_b: GeneralRegister):
    """
    output_register = *(input_register_a + input_register_b)
    https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_lwzx_lx_lwzi_instrus.html
    """
    return Instruction.compose(((31, 6, False),
                                (output_register.number, 5, False),
                                (input_register_a.number, 5, False),
                                (input_register_b.number, 5, False),
                                (23, 10, False),
                                (0, 1, False),
                                ))


def lhz(output_register: GeneralRegister, offset: int, input_register: GeneralRegister):
    """
    *(output_register + offset) = input_register
    """
    return Instruction.compose(((40, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (offset, 16, True)))


def lbz(output_register: GeneralRegister, offset: int, input_register: GeneralRegister):
    """
    *(output_register + offset) = input_register
    """
    return Instruction.compose(((34, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (offset, 16, True)))


def rlwinm(output_register: GeneralRegister, input_register: GeneralRegister,
           shift: int, mask_begin: int, mask_end: int):
    """
    https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_rlwinm_rlinm_rtlwrdimm_instrs.html
    """
    return Instruction.compose(((21, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (shift, 5, False),
                                (mask_begin, 5, False),
                                (mask_end, 5, False),
                                (0, 1, False),
                                ))


def or_(output_register: GeneralRegister, input_register_a: GeneralRegister, input_register_b: GeneralRegister,
        record_bit: bool = False):
    """
    output_register = input_register_a | input_register_b
    """
    # See https://www.ibm.com/support/knowledgecenter/en/ssw_aix_72/assembler/idalangref_or_instruction.html
    return Instruction.compose(((31, 6, False),
                                (input_register_a.number, 5, False),
                                (output_register.number, 5, False),
                                (input_register_b.number, 5, False),
                                (444, 10, False),
                                (int(record_bit), 1, False),
                                ))


def ori(output_register: GeneralRegister, input_register: GeneralRegister, constant: int):
    """
    output_register = input_register | constant
    """
    return Instruction.compose(((24, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (constant, 16, False)))


def nop():
    return ori(r0, r0, 0x0)


def li(register: GeneralRegister, literal: int):
    """
    register = literal
    """
    return addi(register, r0, literal).with_name(f"li {register}, {literal}")


def lis(register: GeneralRegister, literal: int):
    """
    register = literal
    """
    return addis(register, r0, literal)


def lfs(output_register: FloatRegister, offset: int, input_register: GeneralRegister):
    """
    output_register = (float) *(input_register + offset)

    output_register is a float register.
    """
    return Instruction.compose(((48, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (offset, 16, True)))


def cmpwi(input_register: GeneralRegister, literal: int):
    return Instruction.compose(((11, 6, False),
                                (0, 3, False),
                                (0, 1, False),
                                (0, 1, False),
                                (input_register.number, 5, False),
                                (literal, 16, True)))


def cmp(bf, unused, ra: GeneralRegister, rb: GeneralRegister):
    """
    https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_cmp_instr.html
    :param bf: Specifies Condition Register Field 0-7 which indicates result of compare.
    :param unused: Must be set to 0 for the 32-bit subset architecture.
    :param ra: Specifies source general-purpose register for operation.
    :param rb: Specifies source general-purpose register for operation.
    :return:
    """
    return Instruction.compose(((31, 6, False),
                                (bf, 3, False),
                                (0, 1, False),
                                (unused, 1, False),
                                (ra.number, 5, False),
                                (rb.number, 5, False),
                                (0, 10, False),
                                (0, 1, False),
                                ))


def cmpw(bf, ra, rb):
    """https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_em_fpcinst.html"""
    return cmp(bf, 0, ra, rb)


def _jump_to_relative_address(address_or_symbol: JumpTarget, *, relative: bool, link: bool):
    def with_inc_address(address: int, instruction_address: int):
        jump_offset = (address - instruction_address) // 4
        return (((18, 6, False),
                 (jump_offset, 24, True),
                 (0, 1, False),
                 (int(link), 1, False)))

    instruction = RelativeAddressInstruction(address_or_symbol, with_inc_address)
    if relative:
        return instruction.concrete_instruction(0, {})
    else:
        return instruction


def b(address_or_symbol: JumpTarget, *, relative: bool = False):
    """
    jumps to the given address, not setting the link register
    """
    return _jump_to_relative_address(address_or_symbol, relative=relative, link=False).with_name(
        f"b {address_or_symbol}"
    )


def bl(address_or_symbol: JumpTarget, *, relative: bool = False):
    """
    jumps to the given address, setting the link register
    """
    return _jump_to_relative_address(address_or_symbol, relative=relative, link=True).with_name(
        f"bl {address_or_symbol}"
    )


def _conditional_branch(bo: int, bi: int, address_or_symbol: JumpTarget, *, relative: bool = False,
                        absolute_address: bool = False, link_bit: bool = False):
    # https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_ext_br_mnem_bofield.html#idalangref_ext_br_mnem_bofield__row-d2e17648

    def with_inc_address(address: int, instruction_address: int):
        jump_offset = (address - instruction_address) // 4
        return (((16, 6, False),
                 (bo, 5, False),
                 (bi, 5, False),
                 (jump_offset, 14, True),
                 (int(absolute_address), 1, False),
                 (int(link_bit), 1, False)))

    instruction = RelativeAddressInstruction(address_or_symbol, with_inc_address)
    if relative:
        return instruction.concrete_instruction(0, {})
    else:
        return instruction


def bdnz(address_or_symbol: JumpTarget, relative: bool = False):
    """https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_brmenmonics_booperand.html"""
    bo = 16
    bi = 0
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def beq(address_or_symbol: JumpTarget, relative: bool = False):
    """
    jumps to the given address, if last comparison was a successful equality
    """
    bo = 12  # Branch if condition true (BO=12)
    bi = 2  # condition: equals
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def bgt(address_or_symbol: JumpTarget, relative: bool = False):
    """
    jumps to the given address, if last comparison was a successful equality
    """
    bo = 12  # Branch if condition false (BO=4)
    bi = 1  # condition: less than
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def bge(address_or_symbol: JumpTarget, relative: bool = False):
    """
    jumps to the given address, if last comparison was a successful equality
    """
    bo = 4  # Branch if condition false (BO=4)
    bi = 0  # condition: less than
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def ble(address_or_symbol: JumpTarget, relative: bool = False):
    """
    jumps to the given address, if last comparison was a successful equality
    """
    bo = 4  # Branch if condition false (BO=4)
    bi = 1  # condition: less than
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def bne(address_or_symbol: JumpTarget, relative: bool = False):
    """
    jumps to the given address, if last comparison was a successful equality
    """
    bo = 4  # Branch if condition false (BO=4)
    bi = 2  # condition: equals
    return _conditional_branch(bo, bi, address_or_symbol, relative=relative)


def bclr(bo, bi, bh):
    # https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_branch_conditional_link_register.html
    lk = 0
    return Instruction.compose(((19, 6, False),
                                (bo, 5, False),
                                (bi, 5, False),
                                (0, 3, False),
                                (bh, 2, False),
                                (16, 10, False),
                                (lk, 1, False)))


def blr():
    """Branches to the address set by the link register. Does not set the link register."""
    return bclr(20, 0, 0)


def bcctrl(bo, bi, bh):
    """Branch conditionally. Sets the link register."""
    lk = 1
    return Instruction.compose(((19, 6, False),
                                (bo, 5, False),
                                (bi, 5, False),
                                (0, 3, False),
                                (bh, 2, False),
                                (528, 10, False),
                                (lk, 1, False)))


def bctrl():
    """Branches always. Sets the link register."""
    return bcctrl(20, 0, 0)


def _store(input_register: Register, offset: int, output_register: GeneralRegister, op_code: int):
    return Instruction.compose(((op_code, 6, False),
                                (input_register.number, 5, False),
                                (output_register.number, 5, False),
                                (offset, 16, True)))


def stb(input_register: GeneralRegister, offset: int, output_register: GeneralRegister):
    """
    *(output_register +offset) = input_register
    """
    return _store(input_register, offset, output_register, 38)


def stw(input_register: GeneralRegister, offset: int, output_register: GeneralRegister):
    """
    *(output_register +offset) = input_register
    """
    return _store(input_register, offset, output_register, 36)


def stfs(input_register: FloatRegister, offset: int, output_register: GeneralRegister):
    """
    *(float*)(output_register +offset) = input_register
    """
    return _store(input_register, offset, output_register, 52)


def stwu(input_register: GeneralRegister, offset: int, output_register: GeneralRegister):
    return _store(input_register, offset, output_register, 37)


def stmw(start_register: GeneralRegister, offset: int, output_register: GeneralRegister):
    return _store(start_register, offset, output_register, 47)


def sync():
    return Instruction(0x7c0004ac)


def icbi(ra: int, rb: int):
    value = 0x7C0007AC + (ra << 16) + (rb << 11)
    return Instruction(value)


def dcbi(ra: int, rb: int):
    return Instruction.compose(((31, 6, False),
                                (0, 5, False),
                                (ra, 5, False),
                                (rb, 5, False),
                                (470, 10, False),
                                (0, 1, False)))


def isync():
    return Instruction(0x4C00012C)


def addi(output_register: GeneralRegister, input_register: GeneralRegister, literal: int):
    """
    output_register = input_register + literal
    """
    return Instruction.compose(((14, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (literal, 16, True)))


def addis(output_register: GeneralRegister, input_register: GeneralRegister, literal: int):
    """
    output_register = (input_register + literal) << 16
    """
    return Instruction.compose(((15, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (literal, 16, False)))


def _special_register_op(input_register: Register, special_register: int, magic_value: int, op_code: int):
    special_register_top = special_register >> 5
    special_register_bot = special_register & 0b11111

    return Instruction.compose(((op_code, 6, False),
                                (input_register.number, 5, False),
                                (special_register_bot, 5, False),
                                (special_register_top, 5, False),
                                (magic_value, 10, False),
                                (0, 1, False),
                                ))


def mtspr(special_register, input_register: GeneralRegister):
    return _special_register_op(input_register, special_register, 467, 31)


def mtctr(rs: GeneralRegister):
    return mtspr(CTR, rs)


def mfspr(output_register: GeneralRegister, special_register):
    """
    Move from Special-Purpose Register
    https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/idalangref_mfspr_spr_instrs.html
    """
    return _special_register_op(output_register, special_register, 339, 31)


def mulli(output_register: GeneralRegister, input_register: GeneralRegister, literal: int):
    return Instruction.compose(((7, 6, False),
                                (output_register.number, 5, False),
                                (input_register.number, 5, False),
                                (literal, 16, True)))
