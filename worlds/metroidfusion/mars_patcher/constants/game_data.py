from ..rom import Game, Region, Rom
from ..zm.constants.reserved_space import ReservedPointersZM


def area_room_entry_ptrs(rom: Rom) -> int:
    """Returns the address of the area room entry pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79B8BC
        elif rom.region == Region.E:
            return 0x79C0F0
        elif rom.region == Region.J:
            return 0x7EDF6C
        elif rom.region == Region.C:
            return 0x77D5C0
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.ROOM_AREA_ENTRIES_PTR)

    raise ValueError("Rom has unknown game loaded.")


def tileset_entries(rom: Rom) -> int:
    """Returns the address of the tileset entries."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x3BF888
        elif rom.region == Region.E:
            return 0x3BFEE4
        elif rom.region == Region.J:
            return 0x3C1E50
        elif rom.region == Region.C:
            return 0x3C1E94
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.TILESET_ENTRIES_PTR)

    raise ValueError("Rom has unknown game loaded.")


def tileset_count(rom: Rom) -> int:
    """Returns the number of tilesets in the game."""
    if rom.game == Game.MF:
        return 0x62
    elif rom.game == Game.ZM:
        return 0x4F
    raise ValueError(rom.game)


def area_doors_ptrs(rom: Rom) -> int:
    """Returns the address of the area doors pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79B894
        elif rom.region == Region.E:
            return 0x79C0C8
        elif rom.region == Region.J:
            return 0x7EDF44
        elif rom.region == Region.C:
            return 0x77D598
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.AREA_DOORS_PTR)

    raise ValueError("Rom has unknown game loaded.")


def area_connections(rom: Rom) -> int:
    """Returns the address of the area connections list."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x3C8B90
        elif rom.region == Region.E:
            return 0x3C91EC
        elif rom.region == Region.J:
            return 0x3CB158
        elif rom.region == Region.C:
            return 0x3CB19C
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.AREA_CONNECTIONS_PTR)

    raise ValueError("Rom has unknown game loaded.")


def area_connections_count(rom: Rom) -> int:
    """Returns the number of area connections in the game. Excludes the final entry of FFs."""
    if rom.game == Game.MF:
        return 0x22
    elif rom.game == Game.ZM:
        return 0x19

    raise ValueError("Rom has unknown game loaded.")


def anim_palette_entries(rom: Rom) -> int:
    """Returns the address of the animated palette entries."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x3E3764
        elif rom.region == Region.E:
            return 0x3E3DC0
        elif rom.region == Region.J:
            return 0x3E5D38
        elif rom.region == Region.C:
            return 0x3E5D7C
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.ANIM_PALETTE_ENTRIES_PTR)

    raise ValueError("Rom has unknown game loaded.")


def anim_palette_count(rom: Rom) -> int:
    """Returns the number of animated palettes in the game."""
    if rom.game == Game.MF:
        if rom.region == Region.U or rom.region == Region.E:
            return 0x21
        elif rom.region == Region.J or rom.region == Region.C:
            return 0x22
    elif rom.game == Game.ZM:
        return 0x12
    raise ValueError(rom.game, rom.region)


def sprite_graphics_ptrs(rom: Rom) -> int:
    """Returns the address of the sprite graphics pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79A5D8
        elif rom.region == Region.E:
            return 0x79AE0C
        elif rom.region == Region.J:
            return 0x7ECC88
        elif rom.region == Region.C:
            return 0x77C2DC
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.SPRITE_GRAPHICS_PTR)
    raise ValueError(rom.game, rom.region)


def sprite_palette_ptrs(rom: Rom) -> int:
    """Returns the address of the sprite palette pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79A8D4
        elif rom.region == Region.E:
            return 0x79B108
        elif rom.region == Region.J:
            return 0x7ECF84
        elif rom.region == Region.C:
            return 0x77C5D8
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.SPRITE_PALETTES_PTR)
    raise ValueError(rom.game, rom.region)


def sprite_count(rom: Rom) -> int:
    """Returns the number of sprites in the game."""
    if rom.game == Game.MF:
        return 0xCF
    elif rom.game == Game.ZM:
        return 0xCE
    raise ValueError(rom.game)


def spriteset_ptrs(rom: Rom) -> int:
    """Returns the address of the spriteset pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79ADD8
        elif rom.region == Region.E:
            return 0x79B60C
        elif rom.region == Region.J:
            return 0x7ED488
        elif rom.region == Region.C:
            return 0x77CADC
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.SPRITESET_PTR)
    raise ValueError(rom.game, rom.region)


def spriteset_count(rom: Rom) -> int:
    """Returns the number of spritesets in the game."""
    if rom.game == Game.MF:
        return 0x82
    elif rom.game == Game.ZM:
        return 0x72
    raise ValueError(rom.game)


def samus_palettes(rom: Rom) -> list[tuple[int, int]]:
    """Returns a list of (address, row count) pairs for all of Samus's palettes."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return [(0x28DD7C, 0x5E), (0x28EAFC, 0x70), (0x565D48, 3)]
        elif rom.region == Region.E:
            return [(0x28E3D8, 0x5E), (0x28F158, 0x70), (0x5663A4, 3)]
        elif rom.region == Region.J:
            return [(0x290084, 0x5E), (0x290E04, 0x70), (0x568424, 3)]
        elif rom.region == Region.C:
            return [(0x2900C8, 0x5E), (0x290E48, 0x70), (0x56CC68, 3)]
    elif rom.game == Game.ZM:
        addr = rom.read_ptr(ReservedPointersZM.AREA_DOORS_PTR)
        return [(addr, 0xA3)]
    raise ValueError(rom.game, rom.region)


def helmet_cursor_palettes(rom: Rom) -> list[tuple[int, int]]:
    """
    Returns a list of (address, row count) pairs for Samus's helmet as a cursor
    (file select and game over)
    """
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return [(0x740E08, 1), (0x740EA8, 2), (0x73C544, 1), (0x73C584, 2)]
        elif rom.region == Region.E:
            return [(0x741618, 1), (0x7416B8, 2), (0x73CD54, 1), (0x73CD94, 2)]
        elif rom.region == Region.J:
            return [(0x73FCDC, 1), (0x73FD7C, 2), (0x73C030, 1), (0x73C070, 2)]
        elif rom.region == Region.C:
            return [(0x6CE360, 1), (0x6CE400, 2), (0x6CA8F8, 1), (0x6CA938, 2)]
    elif rom.game == Game.ZM:
        addr = rom.read_ptr(ReservedPointersZM.HELMET_CURSOR_PALETTES_PTR)
        return [(addr, 1), (addr + 0x80, 1)]
    raise ValueError(rom.game, rom.region)


def beam_palettes(rom: Rom) -> list[tuple[int, int]]:
    """Returns a list of (address, row count) pairs for beam palettes."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return [(0x58B464, 6)]
        elif rom.region == Region.E:
            return [(0x58BAC0, 6)]
        elif rom.region == Region.J:
            return [(0x58BBF4, 6)]
        elif rom.region == Region.C:
            return [(0x592578, 6)]
    elif rom.game == Game.ZM:
        addr = rom.read_ptr(ReservedPointersZM.BEAM_PALETTES_PTR)
        return [(addr, 6)]
    raise ValueError(rom.game, rom.region)


def character_widths(rom: Rom) -> int:
    """Returns the address of the character widths."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x576234
        elif rom.region == Region.E:
            return 0x576890
        elif rom.region == Region.J:
            return 0x578934
        elif rom.region == Region.C:
            return 0x57D21C
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.CHARACTER_WIDTHS_PTR)
    raise ValueError(rom.game, rom.region)


def sound_data_entries(rom: Rom) -> int:
    """Returns the address of the sound data entries."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0xA8D3C
        elif rom.region == Region.E:
            return 0xA9398
        elif rom.region == Region.J:
            return 0xAB0A0
        elif rom.region == Region.C:
            return 0xAB0E4
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.SOUND_DATA_PTR)
    raise ValueError(rom.game, rom.region)


def sound_count(rom: Rom) -> int:
    """Returns the number of sounds in the game."""
    if rom.game == Game.MF:
        return 0x2E9
    elif rom.game == Game.ZM:
        return 0x2C4
    raise ValueError(rom.game)


def minimap_ptrs(rom: Rom) -> int:
    """Returns the address of the minimap data pointers."""
    if rom.game == Game.MF:
        if rom.region == Region.U:
            return 0x79BE5C
        elif rom.region == Region.E:
            return 0x79C690
        elif rom.region == Region.J:
            return 0x7EE50C
        elif rom.region == Region.C:
            return 0x77DB60
    elif rom.game == Game.ZM:
        return rom.read_ptr(ReservedPointersZM.MINIMAPS_PTR)
    raise ValueError(rom.game, rom.region)


def minimap_count(rom: Rom) -> int:
    """Returns the number of minimaps in the game."""
    if rom.game == Game.MF:
        return 11
    elif rom.game == Game.ZM:
        return 11
    raise ValueError(rom.game)
