import os
import struct
from typing import TYPE_CHECKING, List, Optional
import zipfile
from worlds.Files import APPlayerContainer
import py_randomprime  # type: ignore


from .MetroidPrimeInterface import GAMES, HUD_MESSAGE_DURATION

if TYPE_CHECKING:
    from ppc_asm.assembler.ppc import GeneralRegister  # type: ignore


class MetroidPrimeContainer(APPlayerContainer):
    game: str = "Metroid Prime"  # type: ignore

    def __init__(
        self,
        config_json: str,
        options_json: str,
        outfile_name: str,
        output_directory: str,
        player: Optional[int] = None,
        player_name: str = "",
        server: str = "",
    ):
        self.config_json = config_json
        self.config_path = "config.json"
        self.options_path = "options.json"
        self.options_json = options_json
        container_path = os.path.join(output_directory, outfile_name + ".apmp1")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(self.config_path, self.config_json)
        opened_zipfile.writestr(self.options_path, self.options_json)
        super().write_contents(opened_zipfile)


def add(
    output_register: "GeneralRegister",
    input_register1: "GeneralRegister",
    input_register2: "GeneralRegister",
):
    """
    output_register = input_register1 + input_register2
    """
    from ppc_asm.assembler.ppc import Instruction

    return Instruction.compose(
        (
            (31, 6, False),  # Opcode for add
            (output_register.number, 5, False),
            (input_register1.number, 5, False),
            (input_register2.number, 5, False),
            (266, 10, False),  # Function code for add
            (0, 1, False),  # Rc bit
        )
    )


def slw(
    output_register: "GeneralRegister",
    input_register: "GeneralRegister",
    shift_amount_register: "GeneralRegister",
):
    """
    output_register = input_register << shift_amount_register
    """
    from ppc_asm.assembler.ppc import Instruction

    return Instruction.compose(
        (
            (31, 6, False),  # Opcode for slw
            (input_register.number, 5, False),
            (output_register.number, 5, False),
            (shift_amount_register.number, 5, False),
            (24, 10, False),  # Function code for slw
            (0, 1, False),  # Rc bit
        )
    )


def slwi(
    output_register: "GeneralRegister", input_register: "GeneralRegister", literal: int
):
    """
    output_register = input_register << shift_amount_register
    """
    from ppc_asm.assembler.ppc import Instruction

    return Instruction.compose(
        (
            (21, 6, False),  # Opcode for slwi
            (input_register.number, 5, False),
            (output_register.number, 5, False),
            (literal, 5, False),
            (0, 5, False),
            (31 - literal, 5, False),
            (0, 1, False),  # Rc bit
        )
    )


def construct_hook_patch(game_version: str, progressive_beams: bool) -> List[int]:
    from ppc_asm.assembler.ppc import (
        addi,
        bl,
        li,
        lwz,
        r1,
        r3,
        r4,
        r5,
        r6,
        r31,
        stw,
        cmpwi,
        bne,
        mtspr,
        blr,
        lmw,
        r0,
        LR,
        stwu,
        mfspr,
        or_,
        lbz,
        stmw,
        stb,
        lis,
        r7,
        r9,
        nop,
        ori,
        GeneralRegister,
    )
    from ppc_asm import assembler

    symbols = py_randomprime.symbols_for_version(game_version)

    # UpdateHintState is 0x1BC in length, 111 instructions
    num_preserved_registers = 2
    num_required_instructions = 111
    instruction_size = 4
    block_size = 32
    patch_stack_length = 0x30 + (num_preserved_registers * instruction_size)
    instructions: List = [
        stwu(r1, -(patch_stack_length - instruction_size), r1),
        mfspr(r0, LR),
        stw(r0, patch_stack_length, r1),
        stmw(
            GeneralRegister(block_size - num_preserved_registers),
            patch_stack_length
            - instruction_size
            - num_preserved_registers * instruction_size,
            r1,
        ),
        or_(r31, r3, r3),
        # Check if trigger is set
        lis(
            r6, GAMES[game_version]["HUD_TRIGGER_ADDRESS"] >> 16
        ),  # Load upper 16 bits of address
        ori(
            r6, r6, GAMES[game_version]["HUD_TRIGGER_ADDRESS"] & 0xFFFF
        ),  # Load lower 16 bits of address
        lbz(r5, 0, r6),
        cmpwi(r5, 1),
        bne("early_return_hud"),
        # If trigger is set then reset it to 0
        li(r5, 0),
        stb(r5, 0, r6),
        # Prep function arguments
        lis(
            r5, struct.unpack("<I", struct.pack("<f", HUD_MESSAGE_DURATION))[0] >> 16
        ),  # Float duration to show message
        li(r6, 0x0),
        li(r7, 0x1),
        li(r9, 0x9),
        stw(r5, 0x10, r1),
        stb(r7, 0x14, r1),
        stb(r6, 0x15, r1),
        stb(r6, 0x16, r1),
        stb(r7, 0x17, r1),
        stw(r9, 0x18, r1),
        addi(r3, r1, 0x1C),
        lis(
            r4, GAMES[game_version]["HUD_MESSAGE_ADDRESS"] >> 16
        ),  # Load upper 16 bits of message address
        ori(
            r4, r4, GAMES[game_version]["HUD_MESSAGE_ADDRESS"] & 0xFFFF
        ),  # Load lower 16 bits of message address
        bl(symbols["wstring_l__4rstlFPCw"]),
        addi(r4, r1, 0x10),
        # Call function
        bl(symbols["DisplayHudMemo__9CSamusHudFRC7wstringRC12SHudMemoInfo"]),
        nop().with_label("early_return_hud"),
        # Progressive Beam Patch
        *construct_progressive_beam_patch(game_version, progressive_beams),
        # Early return
        lmw(
            GeneralRegister(block_size - num_preserved_registers),
            patch_stack_length
            - instruction_size
            - num_preserved_registers * instruction_size,
            r1,
        ).with_label("early_return_beam"),
        lwz(r0, patch_stack_length, r1),
        mtspr(LR, r0),
        addi(r1, r1, patch_stack_length - instruction_size),
        blr(),
    ]

    # Fill remaining instructions with nops
    while len(instructions) < num_required_instructions:
        instructions.append(nop())

    if len(instructions) > num_required_instructions:
        raise Exception(
            f"Patch function is too long: {len(instructions)}/{num_required_instructions}"
        )

    return list(
        assembler.assemble_instructions(
            symbols["UpdateHintState__13CStateManagerFf"], instructions, symbols=symbols
        )
    )


def _load_player_state_to_r6(game_version: str) -> List[int]:
    from ppc_asm.assembler.ppc import lis, ori, lwz, r6, r5

    cstate_manager_global = GAMES[game_version]["cstate_manager_global"]
    return [
        # Get the player state address
        lis(
            r6, cstate_manager_global >> 16
        ),  # Load upper 16 bits of cstate_manager_global
        ori(
            r6, r6, cstate_manager_global & 0xFFFF
        ),  # Load lower 16 bits of cstate_manager_global
        lwz(
            r6, 0x8B8, r6
        ),  # Load the player state address from cstate_manager_global + 0x8B8
        # : Dereference the player state address pointer to get the actual player state address
        lwz(r6, 0, r6),  # Load the player state address from the pointer stored in r6
    ]


def construct_progressive_beam_patch(
    game_version: str, progressive_beams: bool
) -> List[int]:
    from ppc_asm.assembler.ppc import (
        addi,
        bl,
        b,
        li,
        lwz,
        r1,
        r3,
        r4,
        r5,
        r6,
        r8,
        r10,
        r31,
        stw,
        cmpwi,
        bgt,
        mtspr,
        blr,
        lmw,
        r0,
        LR,
        stwu,
        mfspr,
        or_,
        stmw,
        stw,
        lis,
        r7,
        r9,
        nop,
        ori,
        GeneralRegister,
        Instruction,
    )

    def add(
        output_register: GeneralRegister,
        input_register1: GeneralRegister,
        input_register2: GeneralRegister,
    ):
        """
        output_register = input_register1 + input_register2
        """
        return Instruction.compose(
            (
                (31, 6, False),  # Opcode for add
                (output_register.number, 5, False),
                (input_register1.number, 5, False),
                (input_register2.number, 5, False),
                (266, 10, False),  # Function code for add
                (0, 1, False),  # Rc bit
            )
        )

    if not progressive_beams:
        return []
    cstate_manager_global = GAMES[game_version]["cstate_manager_global"]
    charge_beam_offset = 0x7C
    instructions: List = [
        # Step 0: Get the player state address
        *_load_player_state_to_r6(game_version),
        # Step 1: Get the current beam from the player state
        lwz(r5, 0x8, r6),  # Load the current beam value
        # Step 2: Read the value at the beam address in CPlayerState::PowerUps[41]
        slwi(r5, r5, 3),  # Multiply by 8
        addi(r7, r6, 0x2C),  # Add powerups array offset + 4 (to get item capacity)
        add(r7, r7, r5),  # Add power beam offset
        lwz(r8, 0, r7),  # Load the value at the progressive beam address
        # Step 3: Check the value and set the appropriate address
        cmpwi(r8, 1),
        bgt("activate_charge_beam"),
        # If value is 0, set the byte at player state address + charge_beam_offset to 0
        li(r9, 0),
        b("set_charge_beam"),
        # If value is 1, set the byte at player state address + charge_beam_offset to 1
        li(r9, 1).with_label("activate_charge_beam"),
        # Set charge beam state
        addi(r10, r6, charge_beam_offset).with_label(
            "set_charge_beam"
        ),  # Calculate player state address + charge_beam_offset
        stw(r9, 0, r10),  # Store 1 at the calculated address
        b("early_return_beam"),
    ]
    return instructions
