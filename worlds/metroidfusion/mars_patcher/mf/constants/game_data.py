from ...rom import Game, Region, Rom


def hatch_lock_events(rom: Rom) -> int:
    """Returns the address of the hatch lock events."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    if rom.region == Region.U:
        return 0x3C8A5C
    elif rom.region == Region.E:
        return 0x3C90B8
    elif rom.region == Region.J:
        return 0x3CB024
    elif rom.region == Region.C:
        return 0x3CB068
    else:
        raise ValueError(rom.region)


def hatch_lock_event_count(rom: Rom) -> int:
    """Returns the number of hatch lock events in the game."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    # Non-vanilla (original: 0x4B)
    return 0xF


def starting_equipment(rom: Rom) -> int:
    """Returns the address of the starting equipment data."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    if rom.region == Region.U:
        return 0x28D2AC
    elif rom.region == Region.E:
        return 0x28D908
    elif rom.region == Region.J:
        return 0x28F5B4
    elif rom.region == Region.C:
        return 0x28F5F8
    else:
        raise ValueError(rom.region)


def sprite_vram_sizes(rom: Rom) -> int:
    """Returns the address of the sprite VRAM sizes."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    if rom.region == Region.U:
        return 0x2E4A50
    elif rom.region == Region.E:
        return 0x2E50AC
    elif rom.region == Region.J:
        return 0x2E6D58
    elif rom.region == Region.C:
        return 0x2E6D9C
    else:
        raise ValueError(rom.region)


def sax_palettes(rom: Rom) -> list[tuple[int, int]]:
    """Returns a list of (address, row count) pairs for all of the SA-X's palettes."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    # Normal, Lab, Monster, Extra
    if rom.region == Region.U:
        return [(0x2E7D60, 2), (0x2E91D8, 2), (0x38CFB4, 8), (0x2B4368, 5)]
    elif rom.region == Region.E:
        return [(0x2E83BC, 2), (0x2E9834, 2), (0x38D610, 8), (0x2B49C4, 5)]
    elif rom.region == Region.J:
        return [(0x2EA068, 2), (0x2EB4E0, 2), (0x38F2BC, 8), (0x2B6670, 5)]
    elif rom.region == Region.C:
        return [(0x2EA0AC, 2), (0x2EB524, 2), (0x38F300, 8), (0x2B66B4, 5)]
    else:
        raise ValueError(rom.region)


def file_screen_text_ptrs(rom: Rom) -> int:
    """Returns the address of the file screen text pointers."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    if rom.region == Region.U:
        return 0x79EC68
    elif rom.region == Region.E:
        return 0x79F4C4
    elif rom.region == Region.J:
        return 0x7F13FC
    else:
        raise ValueError(rom.region)


def navigation_text_ptrs(rom: Rom) -> int:
    """Returns the address of the navigation text pointers."""
    if rom.game != Game.MF:
        raise ValueError(rom.game)
    if rom.region == Region.U:
        return 0x79C0F0
    elif rom.region == Region.E:
        return 0x79C924
    elif rom.region == Region.J:
        return 0x7EE7A0
    elif rom.region == Region.C:
        return 0x77DDF4
    else:
        raise ValueError(rom.region)
