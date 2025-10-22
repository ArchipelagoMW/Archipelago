"""
Houses the data structures representing a mission order in slot data.
Creating these is handled by the nodes they represent in .nodes.py.
"""

from __future__ import annotations
from typing import List, Protocol
from dataclasses import dataclass

from .entry_rules import SubRuleRuleData

class MissionOrderObjectSlotData(Protocol):
    entry_rule: SubRuleRuleData


@dataclass
class CampaignSlotData:
    name: str
    entry_rule: SubRuleRuleData
    exits: List[int]
    layouts: List[LayoutSlotData]

    @staticmethod
    def legacy(name: str, layouts: List[LayoutSlotData]) -> CampaignSlotData:
        return CampaignSlotData(name, SubRuleRuleData.empty(), [], layouts)


@dataclass
class LayoutSlotData:
    name: str
    entry_rule: SubRuleRuleData
    exits: List[int]
    missions: List[List[MissionSlotData]]

    @staticmethod
    def legacy(name: str, missions: List[List[MissionSlotData]]) -> LayoutSlotData:
        return LayoutSlotData(name, SubRuleRuleData.empty(), [], missions)


@dataclass
class MissionSlotData:
    mission_id: int
    prev_mission_ids: List[int]
    entry_rule: SubRuleRuleData
    victory_cache_size: int = 0

    @staticmethod
    def empty() -> MissionSlotData:
        return MissionSlotData(-1, [], SubRuleRuleData.empty())

    @staticmethod
    def legacy(mission_id: int, prev_mission_ids: List[int], entry_rule: SubRuleRuleData) -> MissionSlotData:
        return MissionSlotData(mission_id, prev_mission_ids, entry_rule)
