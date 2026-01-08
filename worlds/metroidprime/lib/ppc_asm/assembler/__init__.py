import copy
import typing

from ppc_asm.assembler.ppc import BaseInstruction, Instruction

__all__ = [
    "Instruction",
    "BaseInstruction",
    "assemble_instructions",
    "byte_count",
]


def assemble_instructions(address: int,
                          instructions: typing.List[BaseInstruction],
                          symbols: typing.Dict[str, int] = None,
                          ) -> typing.Iterable[int]:
    if symbols is not None:
        symbols = copy.copy(symbols)
    else:
        symbols = {}

    b = address
    for instruction in instructions:
        if instruction.label is not None:
            symbols[instruction.label] = b
        b += instruction.byte_count

    for i, instruction in enumerate(instructions):
        data = list(instruction.bytes_for(address, symbols=symbols))
        yield from data
        address += len(data)


def byte_count(instructions: typing.Iterable[BaseInstruction]) -> int:
    return sum(instruction.byte_count for instruction in instructions)
