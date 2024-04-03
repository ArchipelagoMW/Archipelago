import pkgutil
import typing
from typing import Optional, TYPE_CHECKING
import hashlib
import Utils
import os

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from . import Names
from .Text import MM2TextEntry
from .Color import get_colors_for_item, write_palette_shuffle

if TYPE_CHECKING:
    from . import MM2World

MM2LCHASH = "19de63834393b5988d41441f83a36df5"
PROTEUSHASH = "9ff045a3ca30018b6e874c749abb3ec4"
MM2NESHASH = "302761a666ac89c21f185052d02127d3"
MM2VCHASH = "77b51417eb66e8119c85689a093be857"

picopico_weakness_ptrs = {
    0: 0x3EA12,
    1: 0x3EA8E,
    2: 0x3EB06,
    3: 0x3EB7E,
    4: 0x3EBF6,
    5: 0x3EC6E,
    6: 0x3ECE6,
    7: 0x3ED5E,
}


class RomData:
    def __init__(self, file: bytes, name: str = None):
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset):
        return self.file[offset]

    def read_bytes(self, offset, length):
        return self.file[offset:offset + length]

    def write_byte(self, offset, value):
        self.file[offset] = value

    def write_bytes(self, offset, values):
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)


class MM2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [MM2LCHASH, MM2NESHASH, MM2VCHASH]
    game = "Mega Man 2"
    patch_file_ending = ".apmm2"
    result_file_ending = ".nes"
    name: bytearray

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MM2World", patch: MM2ProcedurePatch):
    patch.write_byte(0x3403C, 0x8A)  # Read for setting robot master face tiles
    patch.write_byte(0x34083, 0x8A)  # Read for setting robot master face sprites
    patch.write_bytes(0x340DD, [0x9B, 0xC9, 0x07])  # Dr. Wily checking for Items
    patch.write_byte(0x340ED, 0x8A)  # Check for allowing access to stage
    patch.write_bytes(0x3806C, [0xFF, 0x85, 0x8A])  # initialize starting robot master
    patch.write_bytes(0x38076, [0xA9, 0x00])  # Block auto-Wily
    patch.write_bytes(0x3C264, [0xA9, 0x00])  # Block auto-Wily
    patch.write_bytes(0x3C24D, [0x8B, 0x85, 0x8B])  # Write stage completion to $8B
    patch.write_bytes(0x3C254, [0x8C, 0x85, 0x8C])  # Write item checks to $8C
    patch.write_bytes(0x3C1CC, [0xEA, 0xEA])  # Remove e-tank loss on game over
    patch.write_bytes(0x36325, [0xEA, 0xEA, 0xEA, 0xEA])  # Remove weapon loss on startup

    # Store Wily Progress, and stage completion
    patch.write_bytes(0x37B18, [0x20, 0x2F, 0xF4,
                                0xEA,
                                ])
    patch.write_bytes(0x340E2, [0x20, 0x80, 0xF3, 0xEA, ])
    patch.write_bytes(0x3C271, [0x20, 0xA0, 0xF3, 0xEA, ])
    patch.write_bytes(0x3F390, [0xA5, 0x23,
                                0xC9, 0x0C,
                                0xF0, 0x04,
                                0xA5, 0x8D,
                                0xD0, 0x02,
                                0xA9, 0x08,
                                0x85, 0x2A,
                                0x60,
                                ])
    patch.write_bytes(0x3F3B0, [0xA9, 0x01,
                                0x9D, 0x70, 0x0F,
                                0xE6, 0x2A,
                                0xA5, 0x2A,
                                0x85, 0x8D,
                                0x60,
                                ])
    patch.write_bytes(0x3F43F, [0x85, 0x2A,
                                0x8A,
                                0x48,
                                0xA6, 0x2A,
                                0xA9, 0x01,
                                0x9D, 0x70, 0x0F,
                                0x68,
                                0xAA,
                                0xA9, 0x17,
                                0x60,
                                ])
    # Deathlink and Soft-reset Kill
    patch.write_bytes(0x3C11E, [0x27, 0xF5])
    patch.write_bytes(0x38188, [0x20, 0x8F, 0xF3, 0xEA, ])
    patch.write_bytes(0x3823D, [0x20, 0x8F, 0xF3, 0xEA, ])
    patch.write_bytes(0x3E5BC, [0x85, 0x8F, 0xEA, ])  # null deathlink on death
    patch.write_bytes(0x3F381, [
        0xA9, 0x10,  # LDA #$10
        0x8D, 0x00, 0x20,  # STA PpuControl_2000
        0xA9, 0x06,  # LDA #$06
        0x8D, 0x01, 0x20,  # STA PpuMask_2001
        0x4C, 0xBE, 0xC1,  # JMP $C1BE
        0xEA,
        0xEA,
    ])
    patch.write_bytes(0x3F39F, [0xA5, 0x23,
                                0xC9, 0x0F,
                                0xD0, 0x03,
                                0x4C, 0x71, 0xF3,
                                0x4C, 0x1A, 0xF5,
                                0x60, ])
    patch.write_bytes(0x3F52A, [0xA5, 0x8F,
                                0xC9, 0x01,
                                0xD0, 0x03,
                                0x4C, 0xA8, 0xE5,
                                0x4C, 0xBB, 0xF3,
                                0x60, ])
    patch.write_bytes(0x3F537, [0x20, 0x51, 0xC0,
                                0xA9, 0x00,
                                0x8D, 0xC0, 0x06,
                                0x60, ])
    patch.write_bytes(0x3F3CB, [
        0xA5, 0x27,
        0x29, 0x08,
        0x60,
        0xEA,
        0xEA, ])

    # Wily 5 Requirement
    patch.write_bytes(0x3843F, [
        0x4C, 0xF7, 0xF5,  # JMP $F5F7
        0xEA  # NOP
    ])
    patch.write_bytes(0x3F607, [
        0xA9, 0x01,  # LDA #$01
        0xA2, 0x08,  # LDX #$08
        0xA0, 0x00,  # LDY #$00
        # Head:
        0x24, 0xBC,  # BIT $BC
        0xF0, 0x01,  # BEQ Skip
        0xC8,  # INY
        # Skip:
        0xCA,  # DEX
        0x0A,  # ASL
        0xE0, 0x00,  # CPX #$00
        0xD0, 0xF5,  # BNE Head
        0xC0, world.options.wily_5_requirement.value,  # CPY Wily Requirement
        0xB0, 0x03,  # BCS SpawnTeleporter
        0x4C, 0x50, 0x84,  # JMP $8450
        # SpawnTeleporter:
        0xA9, 0xFF,  # LDA #$FF
        0x85, 0xBC,  # STA $BC
        0xA9, 0x01,  # LDA #$01
        0x85, 0x99,  # STA $99
        0x4C, 0x33, 0x84,  # JMP $8433
    ])
    patch.write_bytes(0x381EE, [  # This spawns the actual teleport object, while the earlier branch spawns the visual
        0xA5, 0x99,  # LDA $99
        0xC9, 0x01,  # CMP #$01
        0x90, 0x15,  # BCC $81F9
    ])
    # clean $99 on stage load
    patch.write_bytes(0x3F62A, [
        0xA9, 0x00,  # LDA #$01
        0x85, 0xBC,  # STA $BC
        0x85, 0x99,  # STA $99
        0x4C, 0xAB, 0x80,  # JMP $80AB
    ])
    patch.write_bytes(0x380B7, [
        0x4C, 0x1A, 0xF6,  # JMP $F61A
        0xEA,  # NOP
    ])

    # text writing
    # write our font
    font = pkgutil.get_data(__name__, os.path.join("data", "mm2font.dat"))
    patch.write_bytes(0x20410, font)
    patch.write_bytes(0x3F540, [
        0x84, 0x00, 0x0A, 0x0A, 0x0A, 0x0A, 0xA8, 0xA5, 0xDB, 0x69, 0x00, 0x85, 0xC8, 0xA9, 0x40, 0x85,
        0xC9, 0xA9, 0xF6, 0x18, 0x65, 0xC8, 0x85, 0xCA, 0xB1, 0xC9, 0x8D, 0xB6, 0x03, 0x98, 0x18, 0x69,
        0x01, 0xA8, 0xA5, 0xCA, 0x69, 0x00, 0x85, 0xCA, 0xB1, 0xC9, 0x8D, 0xB7, 0x03, 0x98, 0x18, 0x69,
        0x01, 0xA8, 0xA5, 0xCA, 0x69, 0x00, 0x85, 0xCA, 0x84, 0xFE, 0xA9, 0x0E, 0x85, 0xFD, 0x20, 0x34,
        0xBD, 0xA4, 0xFE, 0xC0, 0x40, 0xD0, 0x05, 0xAD, 0x20, 0x04, 0xD0, 0x02, 0xB1, 0xC9, 0x8D, 0xB8,
        0x03, 0xE6, 0x47, 0xEE, 0xB7, 0x03, 0xA5, 0xFE, 0x18, 0x69, 0x01, 0x85, 0xFE, 0xA5, 0xCA, 0x69,
        0x00, 0x85, 0xCA, 0xC6, 0xFD, 0xD0, 0xD7, 0xA4, 0x00, 0x20, 0xAB, 0xC0, 0x60, 0xA5, 0x2A, 0xA2,
        0x00, 0xB0, 0x02, 0xA2, 0x02, 0x86, 0xDB, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0x0A, 0x0A, 0x48, 0x38,
        0x20, 0x30, 0xF5, 0x68, 0x69, 0x00, 0x48, 0x38, 0x20, 0x30, 0xF5, 0x68, 0x69, 0x00, 0x48, 0x38,
        0x20, 0x30, 0xF5, 0xA9, 0x00, 0x38, 0x20, 0x3E, 0xBD, 0x68, 0x69, 0x00, 0x38, 0x20, 0x30, 0xF5,
        0x60, 0xA9, 0x7D, 0x85, 0xFD, 0xAD, 0x20, 0x04, 0x29, 0x0F, 0x0A, 0x38, 0x69, 0x1A, 0x85, 0xFF,
        0x60,
    ])
    patch.write_bytes(0x37B84, [0x20, 0x9D, 0xF5,
                                0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])
    patch.write_bytes(0x37D02, [0x07, 0x20, 0xA3, 0xF5, ])  # items text
    patch.write_bytes(0x37D06, [0x20, 0xD1, 0xF5, 0xEA, 0xA6, 0xFF, ])  # items color special casing
    patch.write_bytes(0x37E2A, MM2TextEntry("FOR           ", 0xCB).resolve())
    patch.write_bytes(0x37EAA, MM2TextEntry("GET EQUIPPED  ", 0x0B).resolve())
    patch.write_bytes(0x37EBA, MM2TextEntry("WITH          ", 0x2B).resolve())

    base_address = 0x3F650
    color_address = 0x37F6C
    for i, location in zip(range(11), [
        Names.atomic_fire_get,
        Names.air_shooter_get,
        Names.leaf_shield_get,
        Names.bubble_lead_get,
        Names.quick_boomerang_get,
        Names.time_stopper_get,
        Names.metal_blade_get,
        Names.crash_bomber_get,
        Names.item_1_get,
        Names.item_2_get,
        Names.item_3_get
    ]):
        item = world.multiworld.get_location(location, world.player).item
        if len(item.name) <= 14:
            # we want to just place it in the center
            first_str = ""
            second_str = item.name
            third_str = ""
        elif len(item.name) <= 28:
            # spread across second and third
            first_str = ""
            second_str = item.name[:14]
            third_str = item.name[14:]
        else:
            # all three
            first_str = item.name[:14]
            second_str = item.name[14:28]
            third_str = item.name[28:]
            if len(third_str) > 16:
                third_str = third_str[:16]
        player_str = world.multiworld.get_player_name(item.player)
        if len(player_str) > 14:
            player_str = player_str[:14]
        patch.write_bytes(base_address + (64 * i), MM2TextEntry(first_str, 0x4B).resolve())
        patch.write_bytes(base_address + (64 * i) + 16, MM2TextEntry(second_str, 0x6B).resolve())
        patch.write_bytes(base_address + (64 * i) + 32, MM2TextEntry(third_str, 0x8B).resolve())
        patch.write_bytes(base_address + (64 * i) + 48, MM2TextEntry(player_str, 0xEB).resolve())

        colors = get_colors_for_item(item.name)
        if i > 7:
            patch.write_bytes(color_address + 27 + ((i - 8) * 2), colors)
        else:
            patch.write_bytes(color_address + (i * 2), colors)

    write_palette_shuffle(world, patch)

    if world.options.strict_weakness or world.options.random_weakness:
        # we need to write boss weaknesses
        output = bytearray()
        for weapon in world.weapon_damage:
            weapon_damage = [world.weapon_damage[weapon][i]
                             if world.weapon_damage[weapon][i] >= 0
                             else 256 + world.weapon_damage[weapon][i]
                             for i in range(14)]
            output.extend(weapon_damage)
        patch.write_bytes(0x2E952, bytes(output))
        wily_5_weaknesses = [i for i in range(8) if world.weapon_damage[i][12] > 4]
        world.random.shuffle(wily_5_weaknesses)
        if len(wily_5_weaknesses) >= 3:
            weak1 = wily_5_weaknesses.pop()
            weak2 = wily_5_weaknesses.pop()
            weak3 = wily_5_weaknesses.pop()
        elif len(wily_5_weaknesses) == 2:
            weak1 = weak2 = wily_5_weaknesses.pop()
            weak3 = wily_5_weaknesses.pop()
        else:
            weak1 = weak2 = weak3 = 0
        patch.write_byte(0x2DA2E, weak1)
        patch.write_byte(0x2DA32, weak2)
        patch.write_byte(0x2DA3A, weak3)
        for weapon in picopico_weakness_ptrs:
            p_damage = world.weapon_damage[weapon][9]
            if p_damage < 0:
                p_damage = 256 + p_damage
            patch.write_byte(picopico_weakness_ptrs[weapon], p_damage)
            b_damage = world.weapon_damage[weapon][11]
            if b_damage < 0:
                b_damage = 256 + b_damage
            patch.write_byte(picopico_weakness_ptrs[weapon] + 3, b_damage)

    if world.options.quickswap:
        patch.write_bytes(0x3F533, [0x4C, 0xAC, 0xF3, ])  # add jump to check for holding select
        patch.write_bytes(0x3F3BC, [0xA5, 0x27,
                                    0x29, 0x04,
                                    0xF0, 0x09,
                                    0x4C, 0xE1, 0xF5,
                                    ])
        patch.write_bytes(0x3F5F1, [
            0xA2, 0x0F,  # LDX #$0F
            0xBD, 0x20, 0x04,  # LDA $0420, X
            0x30, 0x0E,  # BMI $F5F6 # Branch if spawned
            0xCA,  # DEX
            0xE0, 0x01,  # CPX #$01
            0xD0, 0xF6,  # BNE $F5E3 # branch loop head
            0xA6, 0xA9,  # LDX $A9
            0xD0, 0x02,  # BNE $F5F3
            0xA2, 0x00,  # LDX #$00
            0x4C, 0xC0, 0xF3,  # JMP $F3C0
            0x60,  # RTS
        ])
        patch.write_bytes(0x3F3D0, [
            0x98,
            0x48,
            0xA6, 0xA9,
            0xE8,
            0xE0, 0x09,
            0x10, 0x1F,
            0xA9, 0x01,
            0xCA,
            0xF0, 0x05,
            0x0A,
            0xE0, 0x00,
            0xD0, 0xF8,
            0xA6, 0xA9,
            0xE8,
            0x48,
            0x25, 0x9A,
            0xD0, 0x09,
            0x68,
            0xE8,
            0xE0, 0x09,
            0x10, 0x07,
            0x0A,
            0xD0, 0xF2,
            0x68,
            0x38,
            0xB0, 0x20,
            0x8A,
            0x48,
            0x38,
            0xE9, 0x08,
            0xAA,
            0xA9, 0x01,
            0xCA,
            0xF0, 0x05,
            0x0A,
            0xE0, 0x00,
            0xD0, 0xF8,
            0xA8,
            0x68,
            0xAA,
            0x98,
            0x48,
            0x25, 0x9B,
            0xD0, 0xE3,
            0x68,
            0xE8,
            0x0A,
            0xD0, 0xF6,
            0xA2, 0x00,
            0xA9, 0x0D,
            0x20, 0x00, 0xC0,
            0xA5, 0xB5,
            0x48,
            0xA5, 0xB6,
            0x48,
            0xA5, 0xB7,
            0x48,
            0xA5, 0xB8,
            0x48,
            0xA5, 0xB9,
            0x48,
            0xA5, 0x20,
            0x48,
            0xA5, 0x1F,
            0x48,
            0x20, 0x40, 0xF4,
            0xA9, 0x0E,
            0x20, 0x00, 0xC0,
            0x68,
            0xA8,
            0x60,
        ])
        patch.write_bytes(0x3F450, [0x68,
                                    0x8D, 0xFE, 0x0F,
                                    0x68,
                                    0x8D, 0xFF, 0x0F,
                                    0x86, 0xA9,
                                    0x20, 0x6C, 0xCC,
                                    0xA5, 0x1A,
                                    0x48,
                                    0xA2, 0x00,
                                    0x86, 0xFD,
                                    0x18,
                                    0xA5, 0x52,
                                    0x7D, 0x7F, 0x95,
                                    0x85, 0x08,
                                    0xA5, 0x53,
                                    0x69, 0x00,
                                    0x85, 0x09,
                                    0xA5, 0x08,
                                    0x46, 0x09,
                                    0x6A,
                                    0x46, 0x09,
                                    0x6A,
                                    0x85, 0x08,
                                    0x29, 0x3F,
                                    0x85, 0x1A,
                                    0x18,
                                    0xA5, 0x09,
                                    0x69, 0x85,
                                    0x85, 0x09,
                                    0xA9, 0x00,
                                    0x85, 0x1B,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xA5, 0xFD,
                                    0xC9, 0x08,
                                    0xB0, 0x12,
                                    0xA6, 0xA9,
                                    0xBD, 0x64, 0x96,
                                    0xA8,
                                    0xE0, 0x09,
                                    0x90, 0x04,
                                    0xA2, 0x00,
                                    0xF0, 0x08,
                                    0xA2, 0x05,
                                    0xD0, 0x04,
                                    0xA0, 0x90,
                                    0xA2, 0x00,
                                    0x20, 0x60, 0xC7,
                                    0x20, 0xAB, 0xC0,
                                    0xA6, 0xFD,
                                    0xE8,
                                    0xE0, 0x0F,
                                    0xD0, 0xAB,
                                    0x86, 0xFD,
                                    0xA0, 0x90,
                                    0xA2, 0x00,
                                    0x20, 0x60, 0xC7,
                                    0x20, 0xED, 0xD2,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0x68,
                                    0x85, 0x1A,
                                    0xA5, 0x2A,
                                    0xC9, 0x0A,
                                    0xD0, 0x18,
                                    0xA5, 0xB1,
                                    0xF0, 0x14,
                                    0xA2, 0x02,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xCA,
                                    0x10, 0xEE,
                                    0xA2, 0x11,
                                    0xBD, 0x00, 0x07,
                                    0xEA,
                                    0xEA,
                                    0xEA,
                                    0xCA,
                                    0x10, 0xF7,
                                    0x68,
                                    0x85, 0x1F,
                                    0x68,
                                    0x85, 0x20,
                                    0x68,
                                    0x85, 0xB9,
                                    0x68,
                                    0x85, 0xB8,
                                    0x68,
                                    0x85, 0xB7,
                                    0x68,
                                    0x85, 0xB6,
                                    0x68,
                                    0x85, 0xB5,
                                    0xA9, 0x00,
                                    0x85, 0xAC,
                                    0x85, 0x2C,
                                    0x8D, 0x80, 0x06,
                                    0x8D, 0xA0, 0x06,
                                    0xA9, 0x1A,
                                    0x8D, 0x00, 0x04,
                                    0xA9, 0x03,
                                    0x85, 0xAA,
                                    0xA9, 0x30,
                                    0x20, 0x51, 0xC0,
                                    0xAD, 0xFF, 0x0F,
                                    0x48,
                                    0xAD, 0xFE, 0x0F,
                                    0x48,
                                    0x60,
                                    ])

    if world.options.consumables:
        patch.write_bytes(0x3E5F8, [0x20, 0x00, 0xF3])  # jump to our handler for consumable checks
        patch.write_bytes(0x3F310, [0x99, 0x40, 0x01,
                                    0x8A,
                                    0x48,
                                    0xA5, 0xAD,
                                    0xC9, 0x7C,
                                    0x10, 0x02,
                                    0xA9, 0x00,
                                    0x85, 0xAD,
                                    0xA5, 0x2A,
                                    0x0A,
                                    0x0A,
                                    0xAA,
                                    0x98,
                                    0xC9, 0x08,
                                    0x30, 0x05,
                                    0xE8,
                                    0xE9, 0x08,
                                    0xD0, 0xF7,
                                    0xA8,
                                    0xA9, 0x01,
                                    0xC0, 0x00,
                                    0xF0, 0x04,
                                    0x0A,
                                    0x88,
                                    0xD0, 0xF8,
                                    0x1D, 0x80, 0x0F,
                                    0x9D, 0x80, 0x0F,
                                    0x68,
                                    0xAA,
                                    0x60,
                                    ])

    from Utils import __version__
    patch.name = bytearray(f'MM2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0',
                           'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x3FFC0, patch.name)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name: str = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() == PROTEUSHASH:
            base_rom_bytes = extract_mm2(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {MM2LCHASH, MM2NESHASH, MM2VCHASH}:
            print(basemd5.hexdigest())
            raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mm2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


header = b'\x4E\x45\x53\x1A\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
prg_offset = 0x8ED70
prg_size = 0x40000


def extract_mm2(proteus: bytes) -> bytes:
    mm2 = bytearray(header)
    mm2.extend(proteus[prg_offset:prg_offset + prg_size])
    return bytes(mm2)
