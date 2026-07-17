import argparse
import re
import sys
from dataclasses import dataclass

DATA = "."
COMMENT = "#"
LABEL = ":"


class CompilerException(Exception):
    pass


@dataclass
class OpCode:
    name: str
    primary_code: int
    secondary_code: int = 0x00


class OpCodeHandler:
    opcodes: list[OpCode] = [
        OpCode("nop", 0x00),
        OpCode("jr", 0x00, 0x08),
        OpCode("addu", 0x00, 0x21),
        OpCode("j", 0x02),
        OpCode("jal", 0x03),
        OpCode("beq", 0x04),
        OpCode("bne", 0x05),
        OpCode("blez", 0x06),
        OpCode("bgtz", 0x07),
        OpCode("addi", 0x08),
        OpCode("addiu", 0x09),
        OpCode("slti", 0x0A),
        OpCode("sltiu", 0x0B),
        OpCode("andi", 0x0C),
        OpCode("ori", 0x0D),
        OpCode("xori", 0x0E),
        OpCode("lui", 0x0F),
        OpCode("lb", 0x20),
        OpCode("lh", 0x21),
        OpCode("lwl", 0x22),
        OpCode("lw", 0x23),
        OpCode("lbu", 0x24),
        OpCode("lhu", 0x25),
        OpCode("lwr", 0x26),
        OpCode("sb", 0x28),
        OpCode("sh", 0x29),
        OpCode("swl", 0x2A),
        OpCode("sw", 0x2B),
    ]

    by_name: dict[str, OpCode] = {}
    for opcode in opcodes:
        by_name[opcode.name] = opcode


@dataclass
class Register:
    name: str
    code: int


class RegisterHandler:
    registers: list[Register] = [
        Register("zero", 0x00),
        Register("at", 0x01),
        Register("v0", 0x02),
        Register("v1", 0x03),
        Register("a0", 0x04),
        Register("a1", 0x05),
        Register("a2", 0x06),
        Register("a3", 0x07),
        Register("t0", 0x08),
        Register("t1", 0x09),
        Register("t2", 0x0A),
        Register("t3", 0x0B),
        Register("t4", 0x0C),
        Register("t5", 0x0D),
        Register("t6", 0x0E),
        Register("t7", 0x0F),
        Register("s0", 0x10),
        Register("s1", 0x11),
        Register("s2", 0x12),
        Register("s3", 0x13),
        Register("s4", 0x14),
        Register("s5", 0x15),
        Register("s6", 0x16),
        Register("s7", 0x17),
        Register("t8", 0x18),
        Register("t9", 0x19),
        Register("k0", 0x1A),
        Register("k1", 0x1B),
        Register("gp", 0x1C),
        Register("sp", 0x1D),
        Register("fp", 0x1E),
        Register("s8", 0x1E),
        Register("ra", 0x1F),
    ]

    by_name: dict[str, Register] = {}
    for register in registers:
        by_name[register.name] = register


@dataclass
class Symbol:
    name: str
    address: int


def get_reg(register: str) -> int:
    """Helper to convert a register token into its integer encoding."""
    register = register.lstrip("$")

    if register in RegisterHandler.by_name:
        return RegisterHandler.by_name[register].code

    raise ValueError(f"Unknown register: {register}")


def get_imm(immeadiate_str: str) -> int:
    """Helper to safely parse hex or decimal integer immediate values."""
    if immeadiate_str.startswith("0x") or immeadiate_str.startswith("-0x"):
        # Handle negative hex syntax strings like '-0x24'
        is_negative = immeadiate_str.startswith("-")
        immeadiate_str = immeadiate_str.replace("-", "")

        val = int(immeadiate_str, 16)

        return -val if is_negative else val

    return int(immeadiate_str)


def get_offset(source: int, destination: int) -> int:
    return (destination - (source + 4)) // 4


@dataclass
class Instruction:
    operation: str
    operands: list[str]

    def assemble(self, symbols: dict[str, Symbol], current_address: int) -> str:
        op = self.operation
        binary = 0

        primary = OpCodeHandler.by_name[op].primary_code
        secondary = OpCodeHandler.by_name[op].secondary_code

        if op == "nop":
            pass

        # --- JUMP TYPE INSTRUCTIONS (26-bit targets) ---
        elif op in ["j", "jal"]:
            imm26 = self.operands[0]

            if imm26 in symbols:
                target_address = symbols[imm26].address
            else:
                target_address = get_imm(imm26)

            # MIPS jumps drop the highest 4 bits and the lowest 2 bits (target >> 2)
            imm26 = (target_address & 0x0FFFFFFF) >> 2
            binary = (primary << 26) | imm26

        # --- BRANCH INSTRUCTIONS (16-bit relative PC offsets) ---
        elif op in ["beq", "bne"]:
            rs = get_reg(self.operands[0])
            rt = get_reg(self.operands[1])
            imm16 = self.operands[2]

            if imm16 in symbols:
                offset = get_offset(current_address, symbols[imm16].address)
            else:
                offset = get_imm(imm16)

            binary = (primary << 26) | (rs << 21) | (rt << 16) | (offset & 0xFFFF)

        elif op in ["blez", "bgtz"]:
            rs = get_reg(self.operands[0])
            imm16 = self.operands[1]

            if imm16 in symbols:
                offset = get_offset(symbols[imm16].address, current_address)
            else:
                offset = get_imm(imm16)

            binary = (primary << 26) | (rs << 21) | (offset & 0xFFFF)

        # --- LUI (Load Upper Immediate) ---
        elif op == "lui":
            rt = get_reg(self.operands[0])
            imm16 = get_imm(self.operands[1])
            binary = (primary << 26) | (rt << 16) | (imm16 & 0xFFFF)

        # --- ALU IMMEDIATE INSTRUCTIONS ---
        elif op in ["addi", "addiu", "slti", "sltiu", "andi", "ori", "xori"]:
            rt = get_reg(self.operands[0])
            rs = get_reg(self.operands[1])
            imm16 = get_imm(self.operands[2])
            binary = (primary << 26) | (rs << 21) | (rt << 16) | (imm16 & 0xFFFF)

        # --- LOAD / STORE INSTRUCTIONS ---
        elif op in ["lb", "lh", "lwl", "lw", "lbu", "lhu", "sb", "sh", "swl", "sw"]:
            rt = get_reg(self.operands[0])
            imm16 = get_imm(self.operands[1])
            rs = get_reg(self.operands[2])  # The base pointer inside the parentheses
            binary = (primary << 26) | (rs << 21) | (rt << 16) | (imm16 & 0xFFFF)

        # --- SPECIAL REGISTER INSTRUCTIONS (JR) ---
        elif op == "jr":
            rs = get_reg(self.operands[0])
            binary = (primary << 26) | (rs << 21) | secondary

        # --- ALU REGISTER INSTRUCTIONS ---
        elif op in ["add", "addu", "sub", "subu", "and", "or", "xor", "nor", "slt", "sltu"]:
            rd = get_reg(self.operands[0])
            rs = get_reg(self.operands[1])
            rt = get_reg(self.operands[2])
            binary = (rs << 21) | (rt << 16) | (rd << 11) | secondary

        else:
            raise CompilerException(f"Unhandled operation: {op}")

        return binary.to_bytes(4, byteorder="little").hex()

    def __repr__(self) -> str:
        return f"{self.operation} {self.operands}"


class Compiler:
    filepath: str = ""
    symbols: list[Symbol] = []
    instructions: list[Instruction] = []
    base_address: int = 0

    def parse_line(self, line: str):
        line = line.split(COMMENT)[0].strip()
        if not line:
            return

        if LABEL in line:
            symbol, address_str = line.split(LABEL)
            address = self.base_address + len(self.instructions) * 4
            if len(address_str) > 0:
                address = get_imm(address_str)

            self.symbols.append(Symbol(symbol.lower(), address))

            return

        # Tokenize by space, comma, and parentheses
        # "sw   s0,0x1c(sp)" -> ['sw', 's0', '0x1c', 'sp']
        tokens = [t.lower() for t in re.split(r"[\s,()]+", line) if t]
        if not tokens:
            return

        operation = tokens[0]
        operands = tokens[1:]

        if operation.startswith(DATA):
            if len(self.instructions) > 0 or len(self.symbols) > 0:
                raise AttributeError(
                    "Unsupported metadata in the middle of the code: Should be at the top of the ASM file"
                )

            if operation == ".base":
                self.base_address = get_imm(operands[0])
            return

        self.instructions.append(Instruction(operation, operands))

    def compile(self, filepath: str) -> str:
        self.symbols = []
        self.instructions = []

        # Parse source file
        self.filepath = filepath
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                self.parse_line(line)

        # Rearange symbols for easy access
        symbols_by_name: dict[str, Symbol] = {}
        for symbol in self.symbols:
            symbols_by_name[symbol.name] = symbol

        # Assemble instructions
        program = ""
        for instruction in self.instructions:
            code = instruction.assemble(symbols_by_name, self.base_address + len(program) // 2)
            program += code

        return program.upper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PSX Compiler")
    parser.add_argument("--filename", default=None, help="Filename in src directory.")
    args = parser.parse_args(sys.argv[1:])

    filename = "interface.asm"
    if args.filename is not None:
        filename = args.filename

    compiler = Compiler()
    print(compiler.compile(f"worlds/tomba/client/src/{filename}"))
