"""This module contains the constant strings used to determine which version of RAC3 is being played"""

from worlds.rac3.constants.region import RAC3REGION


class RAC3VERSION:
    """Constant Strings for the ID of each known version of RAC3"""
    US_ID = "SCUS-97353"
    US_BETA_ID = "SCUS-97413"
    US_DEMO_ID = "SCUS-97411"
    US_GH_ID = "SCUS-97518"
    JP_ID = "SCPS-15084"
    JP_TRIAL_ID = "PCPX-96653"
    JP_TB_ID = "SCPS-19309"
    KO_ID = "SCKA-20037"
    CH_ID = "SCAJ-20109"
    EU_ID = "SCES-52456"
    EU_BETA_ID = "TCES-52456"
    EU_DEMO_ID = "SCED-52847"


GAME_ID_TO_VERSION: dict[str, str] = {
    RAC3VERSION.US_ID: "US release",
    RAC3VERSION.US_BETA_ID: "US beta",
    RAC3VERSION.US_DEMO_ID: "US demo",
    RAC3VERSION.US_GH_ID: "US Greatest Hits release",
    RAC3VERSION.JP_ID: "Japanese release",
    RAC3VERSION.JP_TRIAL_ID: "Japanese trial version",
    RAC3VERSION.JP_TB_ID: "Japanese The Best release",
    RAC3VERSION.KO_ID: "Korean release",
    RAC3VERSION.CH_ID: "Chinese release",
    RAC3VERSION.EU_ID: "EU release",
    RAC3VERSION.EU_BETA_ID: "EU beta",
    RAC3VERSION.EU_DEMO_ID: "EU demo",
}

GAME_ID_TO_OFFSET: dict[str, int] = {
    RAC3VERSION.US_ID: 0x0,
    RAC3VERSION.EU_ID: -0x80
}

PAL_SHIFTED_PLANETS: list[str] = [
    RAC3REGION.VELDIN,
    RAC3REGION.FLORANA,
    RAC3REGION.STARSHIP_PHOENIX,
    RAC3REGION.MARCADIA,
    RAC3REGION.DAXX,
    RAC3REGION.TYHRRANOSIS,
    RAC3REGION.ZELDRIN_STARPORT,
    RAC3REGION.BLACKWATER_CITY,
    RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3REGION.ARIDIA,
    RAC3REGION.OBANI_DRACO,
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK,
    RAC3REGION.METROPOLIS_RANGERS,
    RAC3REGION.QWARK_VID_COMIC_1,
    RAC3REGION.QWARK_VID_COMIC_2,
    RAC3REGION.QWARK_VID_COMIC_3,
    RAC3REGION.QWARK_VID_COMIC_5,
]

VERSION_TO_BLACK_SCREEN_ORIGINAL_VALUE: dict[str, int] = {
    RAC3VERSION.US_ID: 0x8C,
    RAC3VERSION.EU_ID: 0x80
}

JP_SHIFTED_PLANETS: list[str] = [
    RAC3REGION.FLORANA,
    RAC3REGION.AQUATOS_SEWERS,
    RAC3REGION.AQUATOS_BASE,
    RAC3REGION.PHOENIX_ASSAULT,
    RAC3REGION.OBANI_GEMINI,
    RAC3REGION.OBANI_DRACO,
    RAC3REGION.CRASH_SITE,
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK,
    RAC3REGION.AQUATOS,
    RAC3REGION.ZELDRIN_STARPORT,
    RAC3REGION.ANNIHILATION_NATION,
    RAC3REGION.MUSEUM,
    RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3REGION.KOROS,
    RAC3REGION.QWARKS_HIDEOUT,
    RAC3REGION.METROPOLIS,
    RAC3REGION.MARCADIA,
]

JP_PAUSE_CORRECTION_OFFSET: dict[str, int] = {
    RAC3REGION.METROPOLIS:      0x8EC,
    RAC3REGION.TYHRRANOSIS:     0x8EC,
    RAC3REGION.ARIDIA:          0x7EC,
    RAC3REGION.MARCADIA:        0xAAC,
    RAC3REGION.DAXX:            0xD6C,
    RAC3REGION.TYHRRANOSIS_RANGERS:  0xDEC,
    RAC3REGION.METROPOLIS_RANGERS:   0xA6C,
    RAC3REGION.BLACKWATER_CITY: 0xBAC,
    RAC3REGION.COMMAND_CENTER:  0xB6C,
    RAC3REGION.COMMAND_CENTER_2: 0x7AC,
}

JP_VENDOR_OFFSET_CORRECTION: dict[str, int] = {
    RAC3REGION.QWARKS_HIDEOUT: -0x40,
    RAC3REGION.MARCADIA:       -0x40,
    RAC3REGION.TYHRRANOSIS:    -0x40,
    RAC3REGION.OBANI_DRACO:    -0x40,
}

def jp_convert_address(address: int, planet: str) -> int:
    """Convert a US-relative address to its JP equivalent."""
    addr = address
    if planet in JP_SHIFTED_PLANETS and 0x001DE000 <= addr < 0x001DF000:
        addr += 0x80
    for start, end, offset in [
        (0x0016C000, 0x0016CFFF,  0x9310),
        (0x00140000, 0x0019FFFF,   -0x80),
        (0x001A0000, 0x001B0000,  0x9280),
        (0x0010BB00, 0x001BFFFF,  0x9298),
        (0x001C0000, 0x001D4CFF,  0x92C0),
        (0x001D545C, 0x001DF000,  0x9300),
        (0x001DF001, 0x001DFFFF,  0x9380),
        (0x001E0000, 0x00200000,  0x106C),
        (0x00200001, 0x002418BF,  0x9380),
        (0x002418C0, 0x00300000,  0x93C0),
    ]:
        if start <= addr <= end:
            addr += offset
            break
    return addr

def jp_get_pause_physical_address(pause_addr: int, planet: str) -> int | None:
    """Return the JP physical address for reading the pause flag, or None if standard path applies.

    Returns a raw physical address — callers must use super()._read8, not the address_convert path.
    """
    if 0x001E0000 <= pause_addr < 0x00200000 and planet in JP_PAUSE_CORRECTION_OFFSET:
        return pause_addr + JP_PAUSE_CORRECTION_OFFSET[planet]
    # RAC3STATUS.PAUSE_BASE = 0x001DF068
    if planet in JP_SHIFTED_PLANETS and 0x001DF068 <= pause_addr < 0x001E0000:
        return jp_convert_address(pause_addr + 0x18, planet)
    return None
