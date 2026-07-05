"""This module contains constant strings for the IDs of other Ratchet and Clank games"""


class OTHERRATCHETGAMES:
    """Constant strings for the IDs of other Ratchet and Clank games"""
    RAC1_US = "SCUS-97199"
    RAC1_EU = "SCES-50916"
    RAC2_BL_US = "SCUS-97268"
    RAC2_BL_EU = "SCES-51607"
    RAC2_GH_US = "SCUS-97268GH"
    RAC4_US = "SCUS-97465"
    RAC4_EU = "SCES-53285"
    RAC5_US = "SCUS-97615"
    SAC_US = "SCUS-97623"


GAME_ID_TO_OTHER_RATCHET: dict[str, str] = {
    OTHERRATCHETGAMES.RAC1_US: "Ratchet and Clank 1 US",
    OTHERRATCHETGAMES.RAC1_EU: "Ratchet and Clank 1 EU/AUS",
    OTHERRATCHETGAMES.RAC2_BL_US: "Ratchet and Clank 2 Black Label US",
    OTHERRATCHETGAMES.RAC2_BL_EU: "Ratchet and Clank 2 Black Label EU/AUS",
    OTHERRATCHETGAMES.RAC2_GH_US: "Ratchet and Clank 2 Greatest Hits US",
    OTHERRATCHETGAMES.RAC4_US: "Ratchet 4: Deadlocked US",
    OTHERRATCHETGAMES.RAC4_EU: "Ratchet 4: Gladiator EU/AUS",
    OTHERRATCHETGAMES.RAC5_US: "Ratchet and Clank 5: Size Matters US",
    OTHERRATCHETGAMES.SAC_US: "Secret Agent Clank US",
}
