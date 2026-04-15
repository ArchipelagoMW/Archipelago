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
]

VERSION_TO_BLACK_SCREEN_ORIGINAL_VALUE: dict[str, int] = {
    RAC3VERSION.US_ID: 0x8C,
    RAC3VERSION.EU_ID: 0x80
}
