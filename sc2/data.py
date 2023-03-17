""" For the list of enums, see here

https://github.com/Blizzard/s2client-api/blob/d9ba0a33d6ce9d233c2a4ee988360c188fbe9dbf/include/sc2api/sc2_gametypes.h
https://github.com/Blizzard/s2client-api/blob/d9ba0a33d6ce9d233c2a4ee988360c188fbe9dbf/include/sc2api/sc2_action.h
https://github.com/Blizzard/s2client-api/blob/d9ba0a33d6ce9d233c2a4ee988360c188fbe9dbf/include/sc2api/sc2_unit.h
https://github.com/Blizzard/s2client-api/blob/d9ba0a33d6ce9d233c2a4ee988360c188fbe9dbf/include/sc2api/sc2_data.h
"""
import enum
from typing import Dict, Set

from s2clientprotocol import common_pb2 as common_pb
from s2clientprotocol import data_pb2 as data_pb
from s2clientprotocol import error_pb2 as error_pb
from s2clientprotocol import raw_pb2 as raw_pb
from s2clientprotocol import sc2api_pb2 as sc_pb

from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

CreateGameError = enum.Enum("CreateGameError", sc_pb.ResponseCreateGame.Error.items())

PlayerType = enum.Enum("PlayerType", sc_pb.PlayerType.items())
Difficulty = enum.Enum("Difficulty", sc_pb.Difficulty.items())
AIBuild = enum.Enum("AIBuild", sc_pb.AIBuild.items())
Status = enum.Enum("Status", sc_pb.Status.items())
Result = enum.Enum("Result", sc_pb.Result.items())
Alert = enum.Enum("Alert", sc_pb.Alert.items())
ChatChannel = enum.Enum("ChatChannel", sc_pb.ActionChat.Channel.items())

Race = enum.Enum("Race", common_pb.Race.items())

DisplayType = enum.Enum("DisplayType", raw_pb.DisplayType.items())
Alliance = enum.Enum("Alliance", raw_pb.Alliance.items())
CloakState = enum.Enum("CloakState", raw_pb.CloakState.items())

Attribute = enum.Enum("Attribute", data_pb.Attribute.items())
TargetType = enum.Enum("TargetType", data_pb.Weapon.TargetType.items())
Target = enum.Enum("Target", data_pb.AbilityData.Target.items())

ActionResult = enum.Enum("ActionResult", error_pb.ActionResult.items())

race_worker: Dict[Race, UnitTypeId] = {
    Race.Protoss: UnitTypeId.PROBE,
    Race.Terran: UnitTypeId.SCV,
    Race.Zerg: UnitTypeId.DRONE,
}

race_townhalls: Dict[Race, Set[UnitTypeId]] = {
    Race.Protoss: {UnitTypeId.NEXUS},
    Race.Terran: {
        UnitTypeId.COMMANDCENTER,
        UnitTypeId.ORBITALCOMMAND,
        UnitTypeId.PLANETARYFORTRESS,
        UnitTypeId.COMMANDCENTERFLYING,
        UnitTypeId.ORBITALCOMMANDFLYING,
    },
    Race.Zerg: {UnitTypeId.HATCHERY, UnitTypeId.LAIR, UnitTypeId.HIVE},
    Race.Random: {
        # Protoss
        UnitTypeId.NEXUS,
        # Terran
        UnitTypeId.COMMANDCENTER,
        UnitTypeId.ORBITALCOMMAND,
        UnitTypeId.PLANETARYFORTRESS,
        UnitTypeId.COMMANDCENTERFLYING,
        UnitTypeId.ORBITALCOMMANDFLYING,
        # Zerg
        UnitTypeId.HATCHERY,
        UnitTypeId.LAIR,
        UnitTypeId.HIVE,
    },
}

warpgate_abilities: Dict[AbilityId, AbilityId] = {
    AbilityId.GATEWAYTRAIN_ZEALOT: AbilityId.WARPGATETRAIN_ZEALOT,
    AbilityId.GATEWAYTRAIN_STALKER: AbilityId.WARPGATETRAIN_STALKER,
    AbilityId.GATEWAYTRAIN_HIGHTEMPLAR: AbilityId.WARPGATETRAIN_HIGHTEMPLAR,
    AbilityId.GATEWAYTRAIN_DARKTEMPLAR: AbilityId.WARPGATETRAIN_DARKTEMPLAR,
    AbilityId.GATEWAYTRAIN_SENTRY: AbilityId.WARPGATETRAIN_SENTRY,
    AbilityId.TRAIN_ADEPT: AbilityId.TRAINWARP_ADEPT,
}

race_gas: Dict[Race, UnitTypeId] = {
    Race.Protoss: UnitTypeId.ASSIMILATOR,
    Race.Terran: UnitTypeId.REFINERY,
    Race.Zerg: UnitTypeId.EXTRACTOR,
}
