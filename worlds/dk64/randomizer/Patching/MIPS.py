"""Porting functionality of MIPS ASM to hex."""

from enum import IntEnum, auto

# Based on the codebase of: https://www.eg.bucknell.edu/~csci320/mips_web/


class opcodeTable(IntEnum):
    """Opcode Table Enum."""

    SPECIAL = 0
    REGIMM = 1
    J = 2
    JAL = 3
    BEQ = 4
    BNE = 5
    BLEZ = 6
    BGTZ = 7
    ADDI = 8
    ADDIU = 9
    SLTI = 10
    SLTIU = 11
    ANDI = 12
    ORI = 13
    XORI = 14
    LUI = 15
    COP0 = 16
    COP1 = 17
    COP2 = 18
    COP3 = 19
    BEQL = 20
    BNEL = 21
    BLEZL = 22
    BGTZL = 23
    DADDI = 24
    DADDIU = 25
    LB = 32
    LH = 33
    LWL = 34
    LW = 35
    LBU = 36
    LHU = 37
    LWR = 38
    SB = 40
    SH = 41
    SWL = 42
    SW = 43
    SWR = 46
    CACHE = 47
    LLU = 48
    LWC1 = 49
    LWC2 = 50
    LWC3 = 51
    LDC1 = 53
    LDC2 = 54
    LDC3 = 55
    SC = 56
    SWC1 = 57
    SWC2 = 58
    SWC3 = 59
    SDC1 = 61
    SDC2 = 62
    SDC3 = 63


class functTable(IntEnum):
    """Function Table Enum."""

    SLL = 0
    SRL = 2
    SRA = 3
    SLLV = 4
    SRLV = 6
    SRAV = 7
    JR = 8
    JALR = 9
    SYSCALL = 12
    BREAK = 13
    MFHI = 16
    MTHI = 17
    MFLO = 18
    MTLO = 19
    DSLLV = 20
    DSRAV = 23
    MULT = 24
    MULTU = 25
    DIV = 26
    DIVU = 27
    DMULT = 28
    DMULTU = 29
    DDIV = 30
    DDIVU = 31
    ADD = 32
    ADDU = 33
    SUB = 34
    SUBU = 35
    AND = 36
    OR = 37
    XOR = 38
    NOR = 39
    SLT = 42
    SLTU = 43
    DADD = 44
    DADDU = 45
    TGE = 48
    TGEU = 49
    TLT = 50
    TLTU = 51
    TEQ = 52
    TNE = 54
    DSLL = 56
    DSRL = 58
    DSRA = 59
    DSLL32 = 60
    DSRL32 = 62
    DSRA32 = 63


class regimmTable(IntEnum):
    """RegiMM Table Enum."""

    BLTZ = 0
    BGEZ = 1
    BLTZL = 2
    BGEZL = 3
    TGEI = 8
    TGEIU = 9
    TLTI = 10
    TLTIU = 11
    TEQI = 12
    TNEI = 14
    BLTZAL = 16
    BGEZAL = 17
    BLTZALL = 18
    BGEZALL = 19


class Reg(IntEnum):
    """Register Enum."""

    zero = 0
    at = 1
    v0 = 2
    v1 = 3
    a0 = 4
    a1 = 5
    a2 = 6
    a3 = 7
    t0 = 8
    t1 = 9
    t2 = 10
    t3 = 11
    t4 = 12
    t5 = 13
    t6 = 14
    t7 = 15
    s0 = 16
    s1 = 17
    s2 = 18
    s3 = 19
    s4 = 20
    s5 = 21
    s6 = 22
    s7 = 23
    t8 = 24
    t9 = 25
    k0 = 26
    k1 = 27
    gp = 28
    sp = 29
    fp = 30
    ra = 31


class Symbol(IntEnum):
    """Instruction Symbol Enum."""

    ADD = auto()
    ADDI = auto()
    ADDIU = auto()
    ADDU = auto()
    AND = auto()
    ANDI = auto()
    BEQ = auto()
    BEQL = auto()
    BGEZ = auto()
    BGEZAL = auto()
    BGEZALL = auto()
    BGEZL = auto()
    BGTZ = auto()
    BGTZL = auto()
    BLEZ = auto()
    BLEZL = auto()
    BLTZ = auto()
    BLTZAL = auto()
    BLTZALL = auto()
    BLTZL = auto()
    BNE = auto()
    BNEL = auto()
    BREAK = auto()
    COP0 = auto()
    COP1 = auto()
    COP2 = auto()
    COP3 = auto()
    DADD = auto()
    DADDI = auto()
    DADDIU = auto()
    DADDU = auto()
    DDIV = auto()
    DDIVU = auto()
    DIV = auto()
    DIVU = auto()
    DMULT = auto()
    DMULTU = auto()
    DSLL = auto()
    DSLL32 = auto()
    DSLLV = auto()
    DSRA = auto()
    DSRA32 = auto()
    DSRAV = auto()
    DSRL = auto()
    DSRL32 = auto()
    DSRLV = auto()
    DSUB = auto()
    DSUBU = auto()
    J = auto()
    JAL = auto()
    JALR = auto()
    JR = auto()
    LB = auto()
    LBU = auto()
    LD = auto()
    LDC1 = auto()
    LDC2 = auto()
    LDL = auto()
    LDR = auto()
    LH = auto()
    LHU = auto()
    LL = auto()
    LLD = auto()
    LUI = auto()
    LW = auto()
    LWC1 = auto()
    LWC2 = auto()
    LWC3 = auto()
    LWL = auto()
    LWR = auto()
    LWU = auto()
    MFHI = auto()
    MFLO = auto()
    MOVN = auto()
    MOVZ = auto()
    MTHI = auto()
    MTLO = auto()
    MULT = auto()
    MULTU = auto()
    NOP = auto()
    NOR = auto()
    OR = auto()
    ORI = auto()
    PREF = auto()
    SB = auto()
    SC = auto()
    SCD = auto()
    SD = auto()
    SDC1 = auto()
    SDC2 = auto()
    SDL = auto()
    SDR = auto()
    SH = auto()
    SLL = auto()
    SLLV = auto()
    SLT = auto()
    SLTI = auto()
    SLTIU = auto()
    SLTU = auto()
    SRA = auto()
    SRAV = auto()
    SRL = auto()
    SRLV = auto()
    SUB = auto()
    SUBU = auto()
    SW = auto()
    SWC1 = auto()
    SWC2 = auto()
    SWC3 = auto()
    SWL = auto()
    SWR = auto()
    SYNC = auto()
    SYSCALL = auto()
    TEQ = auto()
    TEQI = auto()
    TGE = auto()
    TGEI = auto()
    TGEIU = auto()
    TGEU = auto()
    TLT = auto()
    TLTI = auto()
    TLTIU = auto()
    TLTU = auto()
    TNE = auto()
    TNEI = auto()
    XOR = auto()
    XORI = auto()


class InstructionSegment(IntEnum):
    """Instruction Segment Enum."""

    special = auto()
    rs = auto()
    rd = auto()
    rt = auto()
    sa = auto()
    regimm = auto()
    static = auto()
    immediate = auto()
    base = auto()
    offset = auto()
    code = auto()
    cop_fun = auto()
    target = auto()
    hint = auto()
    stype = auto()


default_segment_value = {
    InstructionSegment.special: 0,
    InstructionSegment.regimm: 1,
}


class InstructionBit:
    """Segment data on an instruction."""

    def __init__(self, start_bit: int, end_bit: int, bit_type: InstructionSegment, value: str = None):
        """Initialize with given parameters."""
        self.start_bit = start_bit
        self.end_bit = end_bit
        self.size = (self.start_bit - self.end_bit) + 1
        self.filter = (1 << self.size) - 1
        self.bit_type = bit_type
        if isinstance(value, str):
            value = int(value, 2)
        elif self.bit_type == InstructionSegment.static and value is None:
            value = 0
        self.value = value


class InstructionFormat:
    """Layout of a written instruction."""

    def __init__(self, instruction: str, segments: str):
        """Initialize with given parameters."""
        self.instruction = instruction
        self.segments = segments


class Instruction:
    """Global instruction information."""

    def __init__(self, name: str, architecture: int, bits: list[InstructionBit], format: InstructionFormat):
        """Initialize with given parameters."""
        self.name = name
        self.architecture = architecture
        self.bits = bits.copy()
        self.format = format


instructions = {
    Symbol.ADD: Instruction(
        "Add Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100000"),
        ],
        InstructionFormat("ADD", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.ADDI: Instruction(
        "Add Immediate Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001000"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("ADDI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.ADDIU: Instruction(
        "Add Immediate Unsigned Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001001"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("ADDIU", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.ADDU: Instruction(
        "Add Unsigned Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100001"),
        ],
        InstructionFormat("ADDU", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.AND: Instruction(
        "And",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100100"),
        ],
        InstructionFormat("AND", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.ANDI: Instruction(
        "And Immediate",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001100"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("ANDI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.BEQ: Instruction(
        "Branch on Equal",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "000100"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BEQ", [InstructionSegment.rs, InstructionSegment.rt, InstructionSegment.offset]),
    ),
    Symbol.BEQL: Instruction(
        "Branch on Equal Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010100"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BEQL", [InstructionSegment.rs, InstructionSegment.rt, InstructionSegment.offset]),
    ),
    Symbol.BGEZ: Instruction(
        "Branch on Greater Than or Equal to Zero",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00001"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGEZ", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BGEZAL: Instruction(
        "Branch on Greater Than or Equal to Zero and Link",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "10001"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGEZAL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BGEZALL: Instruction(
        "Branch on Greater Than or Equal to Zero and Link Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "10011"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGEZALL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BGEZL: Instruction(
        "Branch on Greater Than or Equal to Zero Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00011"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGEZL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BGTZ: Instruction(
        "Branch on Greater Than Zero",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "000111"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGTZ", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BGTZL: Instruction(
        "Branch on Greater Than Zero Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010111"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BGTZL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLEZ: Instruction(
        "Branch on Less Than or Equal to Zero",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "000110"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLEZ", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLEZL: Instruction(
        "Branch on Less Than or Equal to Zero Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010110"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLEZL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLTZ: Instruction(
        "Branch on Less Than Zero",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLTZ", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLTZAL: Instruction(
        "Branch on Less Than Zero And Link",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "10000"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLTZAL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLTZALL: Instruction(
        "Branch on Less Than Zero And Link Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "10010"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLTZALL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BLTZL: Instruction(
        "Branch on Less Than Zero Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00010"),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BLTZL", [InstructionSegment.rs, InstructionSegment.offset]),
    ),
    Symbol.BNE: Instruction(
        "Branch on Not Equal",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "000101"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BNE", [InstructionSegment.rs, InstructionSegment.rt, InstructionSegment.offset]),
    ),
    Symbol.BNEL: Instruction(
        "Branch on Not Equal Likely",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010101"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("BNEL", [InstructionSegment.rs, InstructionSegment.rt, InstructionSegment.offset]),
    ),
    Symbol.BREAK: Instruction(
        "Breakpoint",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "001101"),
        ],
        InstructionFormat("BREAK", []),
    ),
    Symbol.COP0: Instruction(
        "Coprocessor Operation",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010000"),
            InstructionBit(25, 0, InstructionSegment.cop_fun),
        ],
        InstructionFormat("COP0", [InstructionSegment.cop_fun]),
    ),
    Symbol.COP1: Instruction(
        "Coprocessor Operation",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010001"),
            InstructionBit(25, 0, InstructionSegment.cop_fun),
        ],
        InstructionFormat("COP1", [InstructionSegment.cop_fun]),
    ),
    Symbol.COP2: Instruction(
        "Coprocessor Operation",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010010"),
            InstructionBit(25, 0, InstructionSegment.cop_fun),
        ],
        InstructionFormat("COP2", [InstructionSegment.cop_fun]),
    ),
    Symbol.COP3: Instruction(
        "Coprocessor Operation",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "010011"),
            InstructionBit(25, 0, InstructionSegment.cop_fun),
        ],
        InstructionFormat("COP3", [InstructionSegment.cop_fun]),
    ),
    Symbol.DADD: Instruction(
        "Doubleword Add",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101100"),
        ],
        InstructionFormat("DADD", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DADDI: Instruction(
        "Doubleword Add Immediate",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "011000"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("DADDI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.DADDIU: Instruction(
        "Doubleword Add Immediate Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "011001"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("DADDIU", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.DADDU: Instruction(
        "Doubleword Add Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101101"),
        ],
        InstructionFormat("DADDU", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DDIV: Instruction(
        "Doubleword Divide",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011110"),
        ],
        InstructionFormat("DDIV", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DDIVU: Instruction(
        "Doubleword Divide Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011111"),
        ],
        InstructionFormat("DDIVU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DIV: Instruction(
        "Divide Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011010"),
        ],
        InstructionFormat("DIV", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DIVU: Instruction(
        "Divide Unsigned Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011011"),
        ],
        InstructionFormat("DIVU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DMULT: Instruction(
        "Doubleword Multiply",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011100"),
        ],
        InstructionFormat("DMULT", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DMULTU: Instruction(
        "Doubleword Multiply Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011101"),
        ],
        InstructionFormat("DMULTU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DSLL: Instruction(
        "Doubleword Shift Left Logical",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111000"),
        ],
        InstructionFormat("DSLL", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSLL32: Instruction(
        "Doubleword Shift Left Logical Plus 32",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111100"),
        ],
        InstructionFormat("DSLL32", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSLLV: Instruction(
        "Doubleword Shift Left Logical Variable",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "010100"),
        ],
        InstructionFormat("DSLLV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.DSRA: Instruction(
        "Doubleword Shift Right Arithmetic",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111011"),
        ],
        InstructionFormat("DSRA", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSRA32: Instruction(
        "Doubleword Shift Right Arithmetic Plus 32",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111111"),
        ],
        InstructionFormat("DSRA32", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSRAV: Instruction(
        "Doubleword Shift Right Arithmetic Variable",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "010111"),
        ],
        InstructionFormat("DSRAV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.DSRL: Instruction(
        "Doubleword Shift Right Logical",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111010"),
        ],
        InstructionFormat("DSRL", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSRL32: Instruction(
        "Doubleword Shift Right Logical Plus 32",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "111110"),
        ],
        InstructionFormat("DSRL32", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.DSRLV: Instruction(
        "Doubleword Shift Right Logical Variable",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "010110"),
        ],
        InstructionFormat("DSRLV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.DSUB: Instruction(
        "Doubleword Subtract",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101110"),
        ],
        InstructionFormat("DSUB", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.DSUBU: Instruction(
        "Doubleword Subtract Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101111"),
        ],
        InstructionFormat("DSUBU", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.J: Instruction(
        "Jump",
        1,
        [InstructionBit(31, 26, InstructionSegment.static, "000010"), InstructionBit(25, 0, InstructionSegment.target)],
        InstructionFormat("J", [InstructionSegment.target]),
    ),
    Symbol.JAL: Instruction(
        "Jump And Link",
        1,
        [InstructionBit(31, 26, InstructionSegment.static, "000011"), InstructionBit(25, 0, InstructionSegment.target)],
        InstructionFormat("JAL", [InstructionSegment.target]),
    ),
    Symbol.JALR: Instruction(
        "Jump And Link Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "00000"),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "001001"),
        ],
        InstructionFormat("JALR", [InstructionSegment.rd, InstructionSegment.rs]),
    ),
    Symbol.JR: Instruction(
        "Jump Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 6, InstructionSegment.static, "000000000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "001000"),
        ],
        InstructionFormat("JR", [InstructionSegment.rs]),
    ),
    Symbol.LB: Instruction(
        "Load Byte",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100000"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LB", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LBU: Instruction(
        "Load Byte Unsigned",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100100"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LBU", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LD: Instruction(
        "Load Doubleword",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110111"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LD", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LDC1: Instruction(
        "Load Doubleword to Coprocessor",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110101"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LDC1", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LDC2: Instruction(
        "Load Doubleword to Coprocessor",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110110"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LDC2", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LDL: Instruction(
        "Load Doubleword Left",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "011010"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LDL", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LDR: Instruction(
        "Load Doubleword Right",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "011011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LDR", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LH: Instruction(
        "Load Halfword",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100001"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LH", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LHU: Instruction(
        "Load Halfword Unsigned",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100101"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LHU", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LL: Instruction(
        "Load Linked Word",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110000"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LL", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LLD: Instruction(
        "Load Linked Doubleword",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110100"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LLD", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LUI: Instruction(
        "Load Upper Immediate",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001111"),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("LUI", [InstructionSegment.rt, InstructionSegment.immediate]),
    ),
    Symbol.LW: Instruction(
        "Load Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LW", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWC1: Instruction(
        "Load Word To Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110001"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWC1", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWC2: Instruction(
        "Load Word To Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110010"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWC2", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWC3: Instruction(
        "Load Word To Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWC3", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWL: Instruction(
        "Load Word Left",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100010"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWL", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWR: Instruction(
        "Load Word Right",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100110"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWR", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.LWU: Instruction(
        "Load Word Unsigned",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "100111"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("LWU", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.MFHI: Instruction(
        "Move From HI Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 16, InstructionSegment.static, "0000000000"),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "010000"),
        ],
        InstructionFormat("MFHI", [InstructionSegment.rd]),
    ),
    Symbol.MFLO: Instruction(
        "Move From LO Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 16, InstructionSegment.static, "0000000000"),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "010010"),
        ],
        InstructionFormat("MFLO", [InstructionSegment.rd]),
    ),
    Symbol.MOVN: Instruction(
        "Move Conditional on Not Zero",
        4,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "001011"),
        ],
        InstructionFormat("MOVN", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.MOVZ: Instruction(
        "Move Conditional on Zero",
        4,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "001010"),
        ],
        InstructionFormat("MOVZ", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.MTHI: Instruction(
        "Move To HI Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 6, InstructionSegment.static, "000000000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "010001"),
        ],
        InstructionFormat("MTHI", [InstructionSegment.rs]),
    ),
    Symbol.MTLO: Instruction(
        "Move To LO Register",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 6, InstructionSegment.static, "000000000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "010011"),
        ],
        InstructionFormat("MTLO", [InstructionSegment.rs]),
    ),
    Symbol.MULT: Instruction(
        "Multiply Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011000"),
        ],
        InstructionFormat("MULT", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.MULTU: Instruction(
        "Multiply Unsigned Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.static, "0000000000"),
            InstructionBit(5, 0, InstructionSegment.static, "011001"),
        ],
        InstructionFormat("MULTU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.NOR: Instruction(
        "Not Or",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100111"),
        ],
        InstructionFormat("NOR", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.OR: Instruction(
        "Or",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100101"),
        ],
        InstructionFormat("OR", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.ORI: Instruction(
        "Or Immediate",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001101"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("ORI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.PREF: Instruction(
        "Prefetch",
        4,
        [
            InstructionBit(31, 26, InstructionSegment.static, "110011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.hint),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("PREF", [InstructionSegment.hint, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SB: Instruction(
        "Store Byte",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101000"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SB", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SC: Instruction(
        "Store Conditional Word",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111000"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SC", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SCD: Instruction(
        "Store Conditional Doubleword",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111100"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SCD", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SD: Instruction(
        "Store Doubleword",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111111"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SD", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SDC1: Instruction(
        "Store Doubleword From Coprocessor",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111101"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SDC1", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SDC2: Instruction(
        "Store Doubleword From Coprocessor",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111110"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SDC2", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SDL: Instruction(
        "Store Doubleword Left",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101100"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SDL", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SDR: Instruction(
        "Store Doubleword Right",
        3,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101101"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SDR", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SH: Instruction(
        "Store Halfword",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101001"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SH", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SLL: Instruction(
        "Shift Word Left Logical",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "000000"),
        ],
        InstructionFormat("SLL", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.SLLV: Instruction(
        "Shift Word Left Logical Variable",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "000100"),
        ],
        InstructionFormat("SLLV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.SLT: Instruction(
        "Set On Less Than",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101010"),
        ],
        InstructionFormat("SLT", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.SLTI: Instruction(
        "Set on Less Than Immediate",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001010"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("SLTI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.SLTIU: Instruction(
        "Set on Less Than Immediate Unsigned",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001011"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("SLTIU", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.SLTU: Instruction(
        "Set on Less Than Unsigned",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "101011"),
        ],
        InstructionFormat("SLTU", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.SRA: Instruction(
        "Shift Word Right Arithmetic",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "000011"),
        ],
        InstructionFormat("SRA", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.SRAV: Instruction(
        "Shift Word Right Arithmetic Variable",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "000111"),
        ],
        InstructionFormat("SRAV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.SRL: Instruction(
        "Shift Word Right Logical",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.static, "00000"),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.sa),
            InstructionBit(5, 0, InstructionSegment.static, "000010"),
        ],
        InstructionFormat("SRL", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.sa]),
    ),
    Symbol.SRLV: Instruction(
        "Shift Word Right Logical Variable",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "000110"),
        ],
        InstructionFormat("SRLV", [InstructionSegment.rd, InstructionSegment.rt, InstructionSegment.rs]),
    ),
    Symbol.SUB: Instruction(
        "Subtract Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100010"),
        ],
        InstructionFormat("SUB", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.SUBU: Instruction(
        "Subtract Unsigned Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100011"),
        ],
        InstructionFormat("SUBU", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.SW: Instruction(
        "Store Word",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SW", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SWC1: Instruction(
        "Store Word From Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111001"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SWC1", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SWC2: Instruction(
        "Store Word From Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111010"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SWC2", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SWC3: Instruction(
        "Store Word From Coprocessor",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "111011"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SWC3", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SWL: Instruction(
        "Store Word Left",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101010"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SWL", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SWR: Instruction(
        "Store Word Right",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "101110"),
            InstructionBit(25, 21, InstructionSegment.base),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.offset),
        ],
        InstructionFormat("SWR", [InstructionSegment.rt, InstructionSegment.offset, InstructionSegment.base]),
    ),
    Symbol.SYNC: Instruction(
        "Synchronize Shared Memory",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 11, InstructionSegment.static, "000000000000000"),
            InstructionBit(10, 6, InstructionSegment.stype),
            InstructionBit(5, 0, InstructionSegment.static, "001111"),
        ],
        InstructionFormat("SYNC", []),
    ),
    Symbol.SYSCALL: Instruction(
        "System Call",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "001100"),
        ],
        InstructionFormat("SYSCALL", []),
    ),
    Symbol.TEQ: Instruction(
        "Trap if Equal",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110100"),
        ],
        InstructionFormat("TEQ", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TEQI: Instruction(
        "Trap if Equal Immediate",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01100"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TEQI", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.TGE: Instruction(
        "Trap if Greater or Equal",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110000"),
        ],
        InstructionFormat("TGE", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TGEI: Instruction(
        "Trap if Greater or Equal Immediate",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01000"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TGEI", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.TGEIU: Instruction(
        "Trap If Greater Or Equal Immediate Unsigned",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01001"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TGEIU", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.TGEU: Instruction(
        "Trap If Greater or Equal Unsigned",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110001"),
        ],
        InstructionFormat("TGEU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TLT: Instruction(
        "Trap if Less Than",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110010"),
        ],
        InstructionFormat("TLT", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TLTI: Instruction(
        "Trap if Less Than Immediate",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01010"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TLTI", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.TLTIU: Instruction(
        "Trap if Less Than Immediate Unsigned",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01011"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TLTIU", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.TLTU: Instruction(
        "Trap if Less Than Unsigned",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110011"),
        ],
        InstructionFormat("TLTU", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TNE: Instruction(
        "Trap if Not Equal",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 6, InstructionSegment.code),
            InstructionBit(5, 0, InstructionSegment.static, "110110"),
        ],
        InstructionFormat("TNE", [InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.TNEI: Instruction(
        "Trap if Not Equal Immediate",
        2,
        [
            InstructionBit(31, 26, InstructionSegment.regimm),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.static, "01110"),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("TNEI", [InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.XOR: Instruction(
        "Exclusive OR",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.special),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 11, InstructionSegment.rd),
            InstructionBit(10, 6, InstructionSegment.static, "00000"),
            InstructionBit(5, 0, InstructionSegment.static, "100110"),
        ],
        InstructionFormat("XOR", [InstructionSegment.rd, InstructionSegment.rs, InstructionSegment.rt]),
    ),
    Symbol.XORI: Instruction(
        "Exclusive OR Immediate",
        1,
        [
            InstructionBit(31, 26, InstructionSegment.static, "001110"),
            InstructionBit(25, 21, InstructionSegment.rs),
            InstructionBit(20, 16, InstructionSegment.rt),
            InstructionBit(15, 0, InstructionSegment.immediate),
        ],
        InstructionFormat("XORI", [InstructionSegment.rt, InstructionSegment.rs, InstructionSegment.immediate]),
    ),
    Symbol.NOP: Instruction(
        "No Operation",
        1,
        [
            InstructionBit(31, 0, InstructionSegment.static),
        ],
        InstructionFormat("NOP", []),
    ),
}


class MIPS:
    """MIPS Instruction Parser."""

    def __init__(self, symbol: Symbol, args: list):
        """Initialize with given parameters, parse."""
        self.symbol = symbol
        self.args = args.copy()
        if self.symbol not in instructions:
            raise Exception("Invalid operation")
        ins = instructions[self.symbol]
        arg_mapping = {}
        for seg_idx in range(len(ins.format.segments)):
            arg_mapping[ins.format.segments[seg_idx]] = self.args[seg_idx]
        value = 0
        for bit in ins.bits:
            input = 0
            if bit.bit_type in arg_mapping:
                input = int(arg_mapping[bit.bit_type])
            elif bit.bit_type in default_segment_value:
                input = default_segment_value[bit.bit_type]
            elif bit.bit_type == InstructionSegment.static:
                input = bit.value
            else:
                raise Exception(f"Invalid seg type {bit.bit_type}")
            input &= bit.filter
            value |= input << bit.end_bit
        self.value = value
