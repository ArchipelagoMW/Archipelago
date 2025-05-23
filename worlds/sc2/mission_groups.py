"""
Mission group aliases for use in yaml options.
"""

from typing import Dict, List, Set
from .mission_tables import SC2Mission, MissionFlag, SC2Campaign


class MissionGroupNames:
    ALL_MISSIONS = "All Missions"
    WOL_MISSIONS = "WoL Missions"
    HOTS_MISSIONS = "HotS Missions"
    LOTV_MISSIONS = "LotV Missions"
    NCO_MISSIONS = "NCO Missions"
    PROPHECY_MISSIONS = "Prophecy Missions"
    PROLOGUE_MISSIONS = "Prologue Missions"
    EPILOGUE_MISSIONS = "Epilogue Missions"

    TERRAN_MISSIONS = "Terran Missions"
    ZERG_MISSIONS = "Zerg Missions"
    PROTOSS_MISSIONS = "Protoss Missions"
    NOBUILD_MISSIONS = "No-Build Missions"
    DEFENSE_MISSIONS = "Defense Missions"
    AUTO_SCROLLER_MISSIONS = "Auto-Scroller Missions"
    COUNTDOWN_MISSIONS = "Countdown Missions"
    KERRIGAN_MISSIONS = "Kerrigan Missions"
    VANILLA_SOA_MISSIONS = "Vanilla SOA Missions"
    TERRAN_ALLY_MISSIONS = "Controllable Terran Ally Missions"
    ZERG_ALLY_MISSIONS = "Controllable Zerg Ally Missions"
    PROTOSS_ALLY_MISSIONS = "Controllable Protoss Ally Missions"
    VS_TERRAN_MISSIONS = "Vs Terran Missions"
    VS_ZERG_MISSIONS = "Vs Zerg Missions"
    VS_PROTOSS_MISSIONS = "Vs Protoss Missions"
    RACESWAP_MISSIONS = "Raceswap Missions"

    # By planet
    PLANET_MAR_SARA_MISSIONS = "Planet Mar Sara"
    PLANET_CHAR_MISSIONS = "Planet Char"
    PLANET_KORHAL_MISSIONS = "Planet Korhal"
    PLANET_AIUR_MISSIONS = "Planet Aiur"

    # By quest chain
    WOL_MAR_SARA_MISSIONS = "WoL Mar Sara"
    WOL_COLONIST_MISSIONS = "WoL Colonist"
    WOL_ARTIFACT_MISSIONS = "WoL Artifact"
    WOL_COVERT_MISSIONS = "WoL Covert"
    WOL_REBELLION_MISSIONS = "WoL Rebellion"
    WOL_CHAR_MISSIONS = "WoL Char"

    HOTS_UMOJA_MISSIONS = "HotS Umoja"
    HOTS_KALDIR_MISSIONS = "HotS Kaldir"
    HOTS_CHAR_MISSIONS = "HotS Char"
    HOTS_ZERUS_MISSIONS = "HotS Zerus"
    HOTS_SKYGEIRR_MISSIONS = "HotS Skygeirr Station"
    HOTS_DOMINION_SPACE_MISSIONS = "HotS Dominion Space"
    HOTS_KORHAL_MISSIONS = "HotS Korhal"

    LOTV_AIUR_MISSIONS = "LotV Aiur"
    LOTV_KORHAL_MISSIONS = "LotV Korhal"
    LOTV_SHAKURAS_MISSIONS = "LotV Shakuras"
    LOTV_ULNAR_MISSIONS = "LotV Ulnar"
    LOTV_PURIFIER_MISSIONS = "LotV Purifier"
    LOTV_TALDARIM_MISSIONS = "LotV Tal'darim"
    LOTV_MOEBIUS_MISSIONS = "LotV Moebius"
    LOTV_RETURN_TO_AIUR_MISSIONS = "LotV Return to Aiur"

    NCO_MISSION_PACK_1 = "NCO Mission Pack 1"
    NCO_MISSION_PACK_2 = "NCO Mission Pack 2"
    NCO_MISSION_PACK_3 = "NCO Mission Pack 3"

    @classmethod
    def get_all_group_names(cls) -> Set[str]:
        return {
            name
            for identifier, name in cls.__dict__.items()
            if not identifier.startswith("_") and not identifier.startswith("get_")
        }


mission_groups: Dict[str, List[str]] = {}

mission_groups[MissionGroupNames.ALL_MISSIONS] = [mission.mission_name for mission in SC2Mission]
for group_name, campaign in (
    (MissionGroupNames.WOL_MISSIONS, SC2Campaign.WOL),
    (MissionGroupNames.HOTS_MISSIONS, SC2Campaign.HOTS),
    (MissionGroupNames.LOTV_MISSIONS, SC2Campaign.LOTV),
    (MissionGroupNames.NCO_MISSIONS, SC2Campaign.NCO),
    (MissionGroupNames.PROPHECY_MISSIONS, SC2Campaign.PROPHECY),
    (MissionGroupNames.PROLOGUE_MISSIONS, SC2Campaign.PROLOGUE),
    (MissionGroupNames.EPILOGUE_MISSIONS, SC2Campaign.EPILOGUE),
):
    mission_groups[group_name] = [mission.mission_name for mission in SC2Mission if mission.campaign == campaign]

for group_name, flags in (
    (MissionGroupNames.TERRAN_MISSIONS, MissionFlag.Terran),
    (MissionGroupNames.ZERG_MISSIONS, MissionFlag.Zerg),
    (MissionGroupNames.PROTOSS_MISSIONS, MissionFlag.Protoss),
    (MissionGroupNames.NOBUILD_MISSIONS, MissionFlag.NoBuild),
    (MissionGroupNames.DEFENSE_MISSIONS, MissionFlag.Defense),
    (MissionGroupNames.AUTO_SCROLLER_MISSIONS, MissionFlag.AutoScroller),
    (MissionGroupNames.COUNTDOWN_MISSIONS, MissionFlag.Countdown),
    (MissionGroupNames.KERRIGAN_MISSIONS, MissionFlag.Kerrigan),
    (MissionGroupNames.VANILLA_SOA_MISSIONS, MissionFlag.VanillaSoa),
    (MissionGroupNames.TERRAN_ALLY_MISSIONS, MissionFlag.AiTerranAlly),
    (MissionGroupNames.ZERG_ALLY_MISSIONS, MissionFlag.AiZergAlly),
    (MissionGroupNames.PROTOSS_ALLY_MISSIONS, MissionFlag.AiProtossAlly),
    (MissionGroupNames.VS_TERRAN_MISSIONS, MissionFlag.VsTerran),
    (MissionGroupNames.VS_ZERG_MISSIONS, MissionFlag.VsZerg),
    (MissionGroupNames.VS_PROTOSS_MISSIONS, MissionFlag.VsProtoss),
    (MissionGroupNames.RACESWAP_MISSIONS, MissionFlag.RaceSwap),
):
    mission_groups[group_name] = [mission.mission_name for mission in SC2Mission if flags in mission.flags]

for group_name, campaign, chain_name in (
    (MissionGroupNames.WOL_MAR_SARA_MISSIONS, SC2Campaign.WOL, "Mar Sara"),
    (MissionGroupNames.WOL_COLONIST_MISSIONS, SC2Campaign.WOL, "Colonist"),
    (MissionGroupNames.WOL_ARTIFACT_MISSIONS, SC2Campaign.WOL, "Artifact"),
    (MissionGroupNames.WOL_COVERT_MISSIONS, SC2Campaign.WOL, "Covert"),
    (MissionGroupNames.WOL_REBELLION_MISSIONS, SC2Campaign.WOL, "Rebellion"),
    (MissionGroupNames.WOL_CHAR_MISSIONS, SC2Campaign.WOL, "Char"),
    (MissionGroupNames.HOTS_UMOJA_MISSIONS, SC2Campaign.HOTS, "Umoja"),
    (MissionGroupNames.HOTS_KALDIR_MISSIONS, SC2Campaign.HOTS, "Kaldir"),
    (MissionGroupNames.HOTS_CHAR_MISSIONS, SC2Campaign.HOTS, "Char"),
    (MissionGroupNames.HOTS_ZERUS_MISSIONS, SC2Campaign.HOTS, "Zerus"),
    (MissionGroupNames.HOTS_SKYGEIRR_MISSIONS, SC2Campaign.HOTS, "Skygeirr Station"),
    (MissionGroupNames.HOTS_DOMINION_SPACE_MISSIONS, SC2Campaign.HOTS, "Dominion Space"),
    (MissionGroupNames.HOTS_KORHAL_MISSIONS, SC2Campaign.HOTS, "Korhal"),
    (MissionGroupNames.LOTV_AIUR_MISSIONS, SC2Campaign.LOTV, "Aiur"),
    (MissionGroupNames.LOTV_KORHAL_MISSIONS, SC2Campaign.LOTV, "Korhal"),
    (MissionGroupNames.LOTV_SHAKURAS_MISSIONS, SC2Campaign.LOTV, "Shakuras"),
    (MissionGroupNames.LOTV_ULNAR_MISSIONS, SC2Campaign.LOTV, "Ulnar"),
    (MissionGroupNames.LOTV_PURIFIER_MISSIONS, SC2Campaign.LOTV, "Purifier"),
    (MissionGroupNames.LOTV_TALDARIM_MISSIONS, SC2Campaign.LOTV, "Tal'darim"),
    (MissionGroupNames.LOTV_MOEBIUS_MISSIONS, SC2Campaign.LOTV, "Moebius"),
    (MissionGroupNames.LOTV_RETURN_TO_AIUR_MISSIONS, SC2Campaign.LOTV, "Return to Aiur"),
):
    mission_groups[group_name] = [
        mission.mission_name for mission in SC2Mission if mission.campaign == campaign and mission.area == chain_name
    ]

mission_groups[MissionGroupNames.NCO_MISSION_PACK_1] = [
    SC2Mission.THE_ESCAPE.mission_name,
    SC2Mission.SUDDEN_STRIKE.mission_name,
    SC2Mission.ENEMY_INTELLIGENCE.mission_name,
]
mission_groups[MissionGroupNames.NCO_MISSION_PACK_2] = [
    SC2Mission.TROUBLE_IN_PARADISE.mission_name,
    SC2Mission.NIGHT_TERRORS.mission_name,
    SC2Mission.FLASHPOINT.mission_name,
]
mission_groups[MissionGroupNames.NCO_MISSION_PACK_3] = [
    SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name,
    SC2Mission.DARK_SKIES.mission_name,
    SC2Mission.END_GAME.mission_name,
]

mission_groups[MissionGroupNames.PLANET_MAR_SARA_MISSIONS] = [
    SC2Mission.LIBERATION_DAY.mission_name,
    SC2Mission.THE_OUTLAWS.mission_name,
    SC2Mission.ZERO_HOUR.mission_name,
]
mission_groups[MissionGroupNames.PLANET_CHAR_MISSIONS] = [
    SC2Mission.GATES_OF_HELL.mission_name,
    SC2Mission.BELLY_OF_THE_BEAST.mission_name,
    SC2Mission.SHATTER_THE_SKY.mission_name,
    SC2Mission.ALL_IN.mission_name,
    SC2Mission.DOMINATION.mission_name,
    SC2Mission.FIRE_IN_THE_SKY.mission_name,
    SC2Mission.OLD_SOLDIERS.mission_name,
]
mission_groups[MissionGroupNames.PLANET_KORHAL_MISSIONS] = [
    SC2Mission.MEDIA_BLITZ.mission_name,
    SC2Mission.PLANETFALL.mission_name,
    SC2Mission.DEATH_FROM_ABOVE.mission_name,
    SC2Mission.THE_RECKONING.mission_name,
    SC2Mission.SKY_SHIELD.mission_name,
    SC2Mission.BROTHERS_IN_ARMS.mission_name,
]
mission_groups[MissionGroupNames.PLANET_AIUR_MISSIONS] = [
    SC2Mission.ECHOES_OF_THE_FUTURE.mission_name,
    SC2Mission.FOR_AIUR.mission_name,
    SC2Mission.THE_GROWING_SHADOW.mission_name,
    SC2Mission.THE_SPEAR_OF_ADUN.mission_name,
    SC2Mission.TEMPLAR_S_RETURN.mission_name,
    SC2Mission.THE_HOST.mission_name,
    SC2Mission.SALVATION.mission_name,
]

for mission in SC2Mission:
    if mission.flags & MissionFlag.HasRaceSwap:
        short_name = mission.get_short_name()
        mission_groups[short_name] = [
            mission_var.mission_name for mission_var in SC2Mission if short_name in mission_var.mission_name
        ]
