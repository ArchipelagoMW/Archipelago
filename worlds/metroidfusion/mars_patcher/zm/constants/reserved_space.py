from enum import IntEnum, auto

from typing_extensions import Self


class ReservedConstantsZM:
    """
    These are constants that are in the ROM's 'Reserved Space'; things that are intended to be
    modified by this patcher. Most of these are pointers at a hard-coded address that point to
    various pieces of data.
    """

    # Important addresses:
    # 0x760D38 - End of data (U region)
    # 0x7C0000 - Patcher data free space
    # 0x7D0000 - Randomizer data pointers
    # 0x7D8000 - NES Metroid data

    # Hardcoded address for the pointers listed below; see linker.ld (around line 12)
    RANDO_POINTERS_ADDR = 0x7D0000

    # Address for any additional data that the patcher may need to write
    PATCHER_FREE_SPACE_ADDR = 0x7C0000
    PATCHER_FREE_SPACE_END = RANDO_POINTERS_ADDR - PATCHER_FREE_SPACE_ADDR


class ReservedPointersZM(IntEnum):
    # These need to be kept in sync with the data pointers in the decomp, which can be found in
    # src/data/randomizer_pointers.c

    # Existing data
    ROOM_AREA_ENTRIES_PTR = 0
    """Pointer to the list of pointers to the room entries for each area."""
    TILESET_ENTRIES_PTR = auto()
    """Pointer to the list of tileset entries."""
    TILESET_TILEMAP_SIZES_PTR = auto()
    """Pointer to an array containing the size of each tileset's tilemap."""
    MINIMAPS_PTR = auto()
    """Pointer to a list of pointers to the minimap data for each area."""
    AREA_DOORS_PTR = auto()
    """Pointer to the list of pointers to the door entries for each area."""
    AREA_CONNECTIONS_PTR = auto()
    """Pointer to the list of area connections."""
    ANIM_PALETTE_ENTRIES_PTR = auto()
    """Pointer to the list of animated palette entries."""
    SPRITE_GRAPHICS_PTR = auto()
    """Pointer to the list of pointers to the graphics for each sprite."""
    SPRITE_PALETTES_PTR = auto()
    """Pointer to the list of pointers to the palette for each sprite."""
    SPRITESET_PTR = auto()
    """Pointer to the list of pointers to spriteset entries."""
    SAMUS_PALETTES_PTR = auto()
    """Pointer to the start of all of Samus's palettes."""
    HELMET_CURSOR_PALETTES_PTR = auto()
    """Pointer to the palette used for the helmet cursor in menus."""
    BEAM_PALETTES_PTR = auto()
    """Pointer to the start of the beam palettes."""
    CHARACTER_WIDTHS_PTR = auto()
    """Pointer to the character widths table."""
    SOUND_DATA_PTR = auto()
    """Pointer to the list of sound data entries."""
    CHOZO_STATUE_TARGETS_PTR = auto()
    """Pointer to the list of Chozo statue targets."""

    # Rando data
    INTRO_CUTSCENE_DATA_PTR = auto()
    """Pointer to the in-game cutscene data for the intro cutscene;
    needed for writing the starting area."""
    STARTING_INFO_PTR = auto()
    """Pointer to a struct containing the starting location and items."""
    MAJOR_LOCATIONS_PTR = auto()
    """Pointer to a list of major locations and the items they have."""
    MINOR_LOCATIONS_PTR = auto()
    """Pointer to a list of minor locations and the items they have."""

    # Rando options
    DIFFICULTY_OPTIONS_PTR = auto()
    METROID_SPRITE_STATS_PTR = auto()
    BLACK_PIRATES_REQUIRE_PLASMA_PTR = auto()
    SKIP_DOOR_TRANSITIONS_PTR = auto()
    BALL_LAUNCHER_WITHOUT_BOMBS_PTR = auto()
    DISABLE_MIDAIR_BOMB_JUMP_PTR = auto()
    DISABLE_WALLJUMP_PTR = auto()
    REMOVE_CUTSCENES_PTR = auto()
    SKIP_SUITLESS_SEQUENCE_PTR = auto()

    ENERGY_TANK_INCREASE_AMOUNT_PTR = auto()
    MISSILE_TANK_INCREASE_AMOUNT_PTR = auto()
    SUPER_MISSILE_TANK_INCREASE_AMOUNT_PTR = auto()
    POWER_BOMB_TANK_INCREASE_AMOUNT_PTR = auto()

    TITLE_TEXT_LINES_PTR = auto()

    def __new__(cls, offset: int) -> Self:
        obj = int.__new__(cls)
        obj._value_ = ReservedConstantsZM.RANDO_POINTERS_ADDR + (offset * 4)
        return obj
