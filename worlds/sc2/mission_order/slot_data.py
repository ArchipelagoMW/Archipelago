"""
Houses the data structures representing a mission order in slot data.
Creating these is handled by the nodes they represent in .nodes.py.
"""

from __future__ import annotations
from typing import List
from dataclasses import dataclass

from .entry_rules import SubRuleRuleData

@dataclass
class MissionOrderObjectSlotData:
    entry_rule: SubRuleRuleData

@dataclass
class CampaignSlotData(MissionOrderObjectSlotData):
    name: str
    entry_rule: SubRuleRuleData
    exits: List[int]
    layouts: List[LayoutSlotData]

    def __init__(self, name, entry_rule, exits, layouts):
        self.name = name
        self.entry_rule = entry_rule
        self.exits = exits
        self.layouts = layouts

    @staticmethod
    def legacy(name: str, layouts: List[LayoutSlotData]) -> CampaignSlotData:
        return CampaignSlotData(name, SubRuleRuleData.empty(), [], layouts)


@dataclass
class LayoutSlotData(MissionOrderObjectSlotData):
    name: str
    exits: List[int]
    missions: List[List[MissionSlotData]]

    def __init__(self, name, entry_rule, exits, missions):
        self.name = name
        self.entry_rule = entry_rule
        self.exits = exits
        self.missions = missions

    @staticmethod
    def legacy(name: str, missions: List[List[MissionSlotData]]) -> LayoutSlotData:
        return LayoutSlotData(name, SubRuleRuleData.empty(), [], missions)


@dataclass
class MissionSlotData(MissionOrderObjectSlotData):
    mission_id: int
    prev_mission_ids: List[int]
    victory_cache_size: int = 0

    def __init__(self, mission_id, entry_rule, prev_mission_ids, victory_cache_size = 0):
        self.mission_id = mission_id
        self.entry_rule = entry_rule
        self.prev_mission_ids = prev_mission_ids
        self.victory_cache_size = victory_cache_size

    @staticmethod
    def empty() -> MissionSlotData:
        return MissionSlotData(-1, [], SubRuleRuleData.empty())

    @staticmethod
    def legacy(mission_id: int, prev_mission_ids: List[int], entry_rule: SubRuleRuleData) -> MissionSlotData:
        return MissionSlotData(mission_id, prev_mission_ids, entry_rule)
