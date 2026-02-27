"""This module contains the constant strings used to determine which version of RAC3 is being played"""


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
