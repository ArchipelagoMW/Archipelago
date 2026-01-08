from copy import copy
from typing import Dict, Optional

from .Errors import *
from .MnemonicsTree import MNEMONICS
from .Util import *
from ..Util import hex_str


class GameboyAddress:
    def __init__(self, bank: int, offset: int):
        self.bank = bank
        self.offset = offset - 0x4000 if 0x8000 > offset > 0x4000 else offset

    def address_in_rom(self):
        return (self.bank * 0x4000) + self.offset

    def to_word(self):
        mapped_offset = self.offset
        if self.bank > 0:
            mapped_offset += 0x4000
        return f"${hex_str(mapped_offset, 2)}"


class Z80Block:
    local_labels: Dict[str, GameboyAddress]

    def __init__(self, metalabel: str, contents: str):
        split_metalabel = metalabel.split("/")
        if len(split_metalabel) != 3:
            raise Exception(f"Invalid metalabel '{metalabel}'")
        if split_metalabel[1] == "":
            split_metalabel[1] = "ffff"  # <-- means that it needs to be injected in some code cave

        bank = int(split_metalabel[0], 16)
        offset = int(split_metalabel[1], 16)
        if offset != 0xffff:
            if bank > 0:
                offset -= 0x4000
            if offset < 0x0000 or offset >= 0x4000:
                raise InvalidAddressError(split_metalabel[1])
        self.addr = GameboyAddress(bank, offset)

        self.label = split_metalabel[2]

        stripped_lines = [strip_line(line) for line in contents.split("\n")]
        self.content_lines = [line for line in stripped_lines if line]

        self.local_labels = {}
        self.byte_array = []
        self.precompiled_size = 0

    def set_base_offset(self, new_offset):
        old_offset = self.addr.offset
        self.addr.offset = new_offset

        shifted_labels = {}
        for name, addr in self.local_labels.items():
            shifted_offset = addr.offset - old_offset + new_offset
            shifted_labels[name] = GameboyAddress(addr.bank, shifted_offset)
        self.local_labels = shifted_labels

    def requires_injection(self):
        return self.addr.offset == 0xffff


class Z80Assembler:
    def __init__(self, bank_caves: List[int], defines: Dict[str, str], seasons_rom: bytes, ages_rom: Optional[bytes]):
        self.defines = {}
        for key, value in defines.items():
            self.define(key, value)

        self.bank_caves = copy(bank_caves)

        self.floating_chunks = {}
        self.global_labels = {}
        self.blocks = []
        self.seasons_rom = seasons_rom
        self.ages_rom = ages_rom

    def define(self, key: str, replacement_string: str):
        if key in self.defines:
            raise Exception(f"Attempting to re-define a value for key '{key}'.")
        self.defines[key] = replacement_string

    def define_byte(self, key: str, byte: int):
        while byte < 0:
            byte += 0x100
        while byte >= 0x100:
            byte -= 0x100
        self.define(key, f"${hex_str(byte)}")

    def define_word(self, key: str, word: int):
        while word < 0:
            word += 0x10000
        while word >= 0x10000:
            word -= 0x10000
        self.define(key, f"${hex_str(word, 2)}")

    def add_floating_chunk(self, name: str, byte_array: List[int]):
        """
        Add a named byte array to the collection of "floating chunks", which can then be inserted anywhere
        using the "/include" directive in assembly
        """
        if name in self.floating_chunks:
            raise f"Attempting to re-define a floating chunk with name '{name}'."
        self.floating_chunks[name] = byte_array

    def add_global_label(self, name: str, addr: GameboyAddress):
        if name in self.global_labels:
            raise Exception(f"Attempting to re-define a global label with name '{name}'.")
        self.global_labels[name] = addr

    def add_block(self, block: Z80Block):
        # Perform a first "precompilation" pass to determine block size once compiled and local labels' offsets.
        self._precompile_block(block)

        if block.requires_injection():
            bank_cave = self.bank_caves[block.addr.bank]
            if isinstance(bank_cave, list):
                if block.label.startswith("dma_"):
                    raise Exception(f"Graphics are not implemented yet for block {block.label}")
                for i in range(len(bank_cave) - 1):
                    cave_range = bank_cave[i]
                    if cave_range[0] + block.precompiled_size > cave_range[1]:
                        continue
                    injection_offset = cave_range[0]
                    cave_range[0] += block.precompiled_size
                    break
                else:
                    injection_offset = bank_cave[-1]
                    bank_cave[-1] += block.precompiled_size
            else:
                injection_offset = bank_cave
                # If block is meant to be loaded in the graphics memory, it needs to be aligned particularly
                if block.label.startswith("dma_") and injection_offset % 0x10 != 0:
                    injection_offset += 0x10 - (injection_offset % 0x10)

                self.bank_caves[block.addr.bank] = injection_offset + block.precompiled_size

            if injection_offset + block.precompiled_size > 0x4000:
                raise Exception(f"Not enough space for block {block.label} in bank {hex_str(block.addr.bank)} "
                                f"({hex(injection_offset + block.precompiled_size)})."
                                f"Block size: {hex(block.precompiled_size)}; "
                                f"Space left: {hex((sum([cave_range[1] - cave_range[0] + 1 for cave_range in self.bank_caves[block.addr.bank]]) if isinstance(self.bank_caves[block.addr.bank], list) else 0) + 0x4001 - injection_offset)}")
            block.set_base_offset(injection_offset)

        if block.label:
            self.add_global_label(block.label, block.addr)
        for label in block.local_labels:
            if not label.startswith("@"):
                self.add_global_label(label, block.local_labels[label])

        self.blocks.append(block)

    def resolve_names(self, arg: str, current_addr: GameboyAddress, local_labels: Dict[str, GameboyAddress], opcode: str):
        arg = arg.strip()
        if arg.startswith("(") and arg.endswith(")"):
            return f"({self.resolve_names(arg[1:-1], current_addr, local_labels, opcode)})"

        HANDLED_OPERATORS = ["+", "-", "*", "|"]
        for operator in HANDLED_OPERATORS:
            if operator in arg:
                split = arg.split(operator)
                arg_1 = self.resolve_names(split[0], current_addr, local_labels, opcode)
                arg_2 = self.resolve_names(split[1], current_addr, local_labels, opcode)
                return f"{arg_1}{operator}{arg_2}"

        output = arg
        if arg in self.defines:
            # Do another pass in case the define is a label
            return self.resolve_names(self.defines[arg], current_addr, local_labels, opcode)
        else:
            addr = None
            if arg in local_labels:
                addr = local_labels[arg]
            elif arg in self.global_labels:
                addr = self.global_labels[arg]
            if addr:
                if opcode == "jr" and current_addr.bank == addr.bank:
                    # If opcode is "jr", we need to use an 8-bit relative offset instead of a 16-bit absolute address
                    difference = addr.offset - (current_addr.offset + 2)
                    if difference > 0x7f or difference < (-1 * 0x7f):
                        raise Exception(f"Label {arg} is too far away, offset cannot be expressed as a single byte ({difference})")
                    if difference < 0:
                        difference = 0x100 + difference
                    output = f"${hex_str(difference)}"
                else:
                    output = addr.to_word()

        return output

    def compile_all(self):
        """
        Perform a full compilation of all previously added blocks.
        """
        for block in self.blocks:
            self._compile_block(block)

    def _precompile_block(self, block: Z80Block):
        block.byte_array = []
        current_offset = 0
        for line in block.content_lines:
            addr = GameboyAddress(block.addr.bank, block.addr.offset + current_offset)
            current_offset += self._evaluate_line_size(line, addr, block)
        block.precompiled_size = current_offset

    def _compile_block(self, block: Z80Block):
        block.byte_array = []
        for line in block.content_lines:
            addr = GameboyAddress(block.addr.bank, block.addr.offset + len(block.byte_array))
            block.byte_array.extend(self._compile_line_to_bytes(line, addr, block))

        if block.precompiled_size != len(block.byte_array):
            raise Exception(f"Block {block.label} size prediction was wrong: "
                            f"{block.precompiled_size} -> {len(block.byte_array)}")

    def _evaluate_line_size(self, line: str, current_addr: GameboyAddress, block: Z80Block):
        opcode = line.split(" ")[0]

        # If it ends with ':', it's a local label and needs to be registered as such
        if opcode.endswith(":"):
            block.local_labels[opcode[:-1]] = current_addr
            return 0

        args = line[len(opcode) + 1:].split(",")
        if len(args) == 0:
            args = [""]

        if opcode == "/include":
            if args[0] not in self.floating_chunks:
                raise UnknownFloatingChunkError(args[0])
            return len(self.floating_chunks[args[0]])
        if opcode == "/copy":
            return parse_hex_string_to_value(args[3])
        if opcode == "db":
            return len(args)
        if opcode == "dw" or opcode == "dwbe":
            return len(args) * 2

        # ...then try matching a mnemonic
        extra_size = 0
        mnemonic_tree = MNEMONICS[opcode]
        for arg in args:
            if not isinstance(mnemonic_tree, collections.abc.Mapping):
                raise TooManyArgsError(line)

            if arg not in mnemonic_tree:
                # Argument could not be found in mnemonic tree, this means it's either a literal or a
                # yet-unknown label / define. In that case, assume the size to be the one for the literal
                # type that can be used for this mnemonic (if it exists)
                for size in [8, 16]:
                    generic_arg = f"${size}"
                    if arg.startswith("("):
                        generic_arg = f"({generic_arg})"
                    if generic_arg in mnemonic_tree:
                        arg = generic_arg
                        extra_size = int(size / 8)
                        break
                if extra_size == 0:
                    raise UnknownMnemonicError(arg, line)

            mnemonic_tree = mnemonic_tree[arg]

        if isinstance(mnemonic_tree, collections.abc.Mapping):
            raise IncompleteMnemonicError(line)
        if isinstance(mnemonic_tree, list):
            # Multi-byte opcode (CB prefix case)
            return 2 + extra_size
        else:
            # Single-byte opcode
            return 1 + extra_size

    def _compile_line_to_bytes(self, line: str, current_addr: GameboyAddress, block: Z80Block):
        split = line.split(" ")
        opcode = split[0]

        # If it ends with ':', it's a local label and needs to be ignored (since it was already registered
        # during precompilation)
        if opcode.endswith(":"):
            return []

        args = [""]
        if len(split) > 1:
            args = " ".join(split[1:]).split(",")

        # Perform includes before resolving names
        if opcode == "/include":
            if args[0] not in self.floating_chunks:
                raise UnknownFloatingChunkError(args[0])
            return self.floating_chunks[args[0]]

        # Resolve defines & labels to actual values. The ones that could not be resolved are let as-is.
        args = [self.resolve_names(arg, current_addr, block.local_labels, opcode) for arg in args]

        # First try matching a specific keyword
        if opcode == "db":
            # Declare byte
            return [parse_byte(arg) for arg in args]
        if opcode == "dw":
            # Declare word
            return [b for arg in args for b in parse_hex_word(arg)]
        if opcode == "dwbe":
            # Declare word big endian (reversed)
            return [b for arg in args for b in reversed(parse_hex_word(arg))]
        if opcode == "/copy":
            offset = parse_hex_string_to_value(args[2])
            if offset > 0x4000:
                offset -= 0x4000
            address = 0x4000 * parse_hex_string_to_value(args[1]) + offset
            if args[0] == "s":
                return self.seasons_rom[address:address + parse_hex_string_to_value(args[3])]
            else:
                return self.ages_rom[address:address + parse_hex_string_to_value(args[3])]

        # ...then try matching a mnemonic
        extra_bytes = []
        mnemonic_tree = MNEMONICS[opcode]
        for arg in args:
            if not isinstance(mnemonic_tree, collections.abc.Mapping):
                raise TooManyArgsError(line)

            generic_arg, value_byte_array = parse_argument(arg, mnemonic_tree)
            if generic_arg not in mnemonic_tree:
                raise UnknownMnemonicError(generic_arg, line)

            mnemonic_tree = mnemonic_tree[generic_arg]
            extra_bytes.extend(value_byte_array)

        if isinstance(mnemonic_tree, collections.abc.Mapping):
            raise IncompleteMnemonicError(line)
        if isinstance(mnemonic_tree, list):
            # Multi-byte opcode (CB prefix case)
            output = copy(mnemonic_tree)
        else:
            # Single-byte opcode
            output = [mnemonic_tree]

        output.extend(extra_bytes)

        return output
