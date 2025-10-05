from __future__ import annotations
from typing import Set, Callable, Dict, List, Union, TYPE_CHECKING, Any, NamedTuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..mission_tables import SC2Mission
from ..item.item_tables import item_table
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from .nodes import SC2MOGenMission

def always_true(state: CollectionState) -> bool:
    """Helper method to avoid creating trivial lambdas"""
    return True


class EntryRule(ABC):
    buffer_fulfilled: bool
    buffer_depth: int

    def __init__(self) -> None:
        self.buffer_fulfilled = False
        self.buffer_depth = -1
    
    def is_always_fulfilled(self, in_region_creation: bool = False) -> bool:
        return self.is_fulfilled(set(), in_region_creation)

    @abstractmethod
    def _is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_creation: bool) -> bool:
        """Used during region creation to ensure a beatable mission order.
        
        `in_region_creation` should determine whether rules that cannot be handled during region creation (like Item rules)
        report themselves as fulfilled or unfulfilled."""
        return False

    def is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_creation: bool) -> bool:
        if len(beaten_missions) == 0:
            # Special-cased to avoid the buffer
            # This is used to determine starting missions
            return self._is_fulfilled(beaten_missions, in_region_creation)
        self.buffer_fulfilled = self.buffer_fulfilled or self._is_fulfilled(beaten_missions, in_region_creation)
        return self.buffer_fulfilled

    @abstractmethod
    def _get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        """Used during region creation to determine the minimum depth this entry rule can be cleared at."""
        return -1
    
    def get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        if not self.is_fulfilled(beaten_missions, in_region_creation = True):
            return -1
        if self.buffer_depth == -1:
            self.buffer_depth = self._get_depth(beaten_missions)
        return self.buffer_depth

    @abstractmethod
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        """Passed to Archipelago for use during item placement."""
        return lambda _: False
    
    @abstractmethod
    def to_slot_data(self) -> RuleData:
        """Used in the client to determine accessibility while playing and to populate tooltips."""
        pass

    @abstractmethod
    def find_mandatory_mission(self) -> SC2MOGenMission | None:
        """Should return any mission that is mandatory to fulfill the entry rule, or `None` if there is no such mission."""
        return None


@dataclass
class RuleData(ABC):
    @abstractmethod
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission], done_color: str, not_done_color: str) -> str:
        return ""
    
    @abstractmethod
    def shows_single_rule(self) -> bool:
        return False

    @abstractmethod
    def is_accessible(
        self, beaten_missions: Set[int], received_items: Dict[int, int]
    ) -> bool:
        return False


class BeatMissionsEntryRule(EntryRule):
    missions_to_beat: List[SC2MOGenMission]
    visual_reqs: List[Union[str, SC2MOGenMission]]

    def __init__(self, missions_to_beat: List[SC2MOGenMission], visual_reqs: List[Union[str, SC2MOGenMission]]):
        super().__init__()
        self.missions_to_beat = missions_to_beat
        self.visual_reqs = visual_reqs
    
    def _is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_check: bool) -> bool:
        return beaten_missions.issuperset(self.missions_to_beat)
    
    def _get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        return max(mission.min_depth for mission in self.missions_to_beat)

    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_all([mission.beat_item() for mission in self.missions_to_beat], player)
    
    def to_slot_data(self) -> RuleData:
        resolved_reqs: List[Union[str, int]] = [req if isinstance(req, str) else req.mission.id for req in self.visual_reqs]
        mission_ids = [mission.mission.id for mission in self.missions_to_beat]
        return BeatMissionsRuleData(
            mission_ids,
            resolved_reqs
        )
    
    def find_mandatory_mission(self) -> SC2MOGenMission | None:
        if len(self.missions_to_beat) > 0:
            return self.missions_to_beat[0]
        return None


@dataclass
class BeatMissionsRuleData(RuleData):
    mission_ids: List[int]
    visual_reqs: List[Union[str, int]]

    def tooltip(self, indents: int, missions: Dict[int, SC2Mission], done_color: str, not_done_color: str) -> str:
        indent = " ".join("" for _ in range(indents))
        if len(self.visual_reqs) == 1:
            req = self.visual_reqs[0]
            return f"Beat {missions[req].mission_name if isinstance(req, int) else req}"
        tooltip = f"Beat all of these:\n{indent}- "
        reqs = [missions[req].mission_name if isinstance(req, int) else req for req in self.visual_reqs]
        tooltip += f"\n{indent}- ".join(req for req in reqs)
        return tooltip
    
    def shows_single_rule(self) -> bool:
        return len(self.visual_reqs) == 1

    def is_accessible(
        self, beaten_missions: Set[int], received_items: Dict[int, int]
    ) -> bool:
        # Beat rules are accessible if all their missions are beaten and accessible
        if not beaten_missions.issuperset(self.mission_ids):
            return False
        return True


class CountMissionsEntryRule(EntryRule):
    missions_to_count: List[SC2MOGenMission]
    target_amount: int
    visual_reqs: List[Union[str, SC2MOGenMission]]

    def __init__(self, missions_to_count: List[SC2MOGenMission], target_amount: int, visual_reqs: List[Union[str, SC2MOGenMission]]):
        super().__init__()
        self.missions_to_count = missions_to_count
        if target_amount <= -1 or target_amount > len(missions_to_count):
            self.target_amount = len(missions_to_count)
        else:
            self.target_amount = target_amount
        self.visual_reqs = visual_reqs

    def _is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_check: bool) -> bool:
        return self.target_amount <= len(beaten_missions.intersection(self.missions_to_count))
    
    def _get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        sorted_missions = sorted(beaten_missions.intersection(self.missions_to_count), key = lambda mission: mission.min_depth)
        mission_depth = max(mission.min_depth for mission in sorted_missions[:self.target_amount])
        return max(mission_depth, self.target_amount - 1) # -1 because depth is zero-based but amount is one-based

    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        if self.target_amount == 0:
            return always_true
        
        beat_items = [mission.beat_item() for mission in self.missions_to_count]
        def count_missions(state: CollectionState) -> bool:
            count = 0
            for mission in range(len(self.missions_to_count)):
                if state.has(beat_items[mission], player):
                    count += 1
                    if count == self.target_amount:
                        return True
            return False
        
        return count_missions
    
    def to_slot_data(self) -> RuleData:
        resolved_reqs: List[Union[str, int]] = [req if isinstance(req, str) else req.mission.id for req in self.visual_reqs]
        mission_ids = [mission.mission.id for mission in sorted(self.missions_to_count, key = lambda mission: mission.min_depth)]
        return CountMissionsRuleData(
            mission_ids,
            self.target_amount,
            resolved_reqs
        )
    
    def find_mandatory_mission(self) -> SC2MOGenMission | None:
        if self.target_amount > 0 and self.target_amount == len(self.missions_to_count):
            return self.missions_to_count[0]
        return None


@dataclass
class CountMissionsRuleData(RuleData):
    mission_ids: List[int]
    amount: int
    visual_reqs: List[Union[str, int]]

    def tooltip(self, indents: int, missions: Dict[int, SC2Mission], done_color: str, not_done_color: str) -> str:
        indent = " ".join("" for _ in range(indents))
        if self.amount == len(self.mission_ids):
            amount = "all"
        else:
            amount = str(self.amount)
        if len(self.visual_reqs) == 1:
            req = self.visual_reqs[0]
            req_str = missions[req].mission_name if isinstance(req, int) else req
            if self.amount == 1:
                if type(req) == int:
                    return f"Beat {req_str}"
                return f"Beat any mission from {req_str}"
            return f"Beat {amount} missions from {req_str}"
        if self.amount == 1:
            tooltip = f"Beat any mission from:\n{indent}- "
        else:
            tooltip = f"Beat {amount} missions from:\n{indent}- "
        reqs = [missions[req].mission_name if isinstance(req, int) else req for req in self.visual_reqs]
        tooltip += f"\n{indent}- ".join(req for req in reqs)
        return tooltip
    
    def shows_single_rule(self) -> bool:
        return len(self.visual_reqs) == 1

    def is_accessible(
        self, beaten_missions: Set[int], received_items: Dict[int, int]
    ) -> bool:
        # Count rules are accessible if enough of their missions are beaten and accessible
        return len([mission_id for mission_id in self.mission_ids if mission_id in beaten_missions]) >= self.amount


class SubRuleEntryRule(EntryRule):
    rule_id: int
    rules_to_check: List[EntryRule]
    target_amount: int
    min_depth: int

    def __init__(self, rules_to_check: List[EntryRule], target_amount: int, rule_id: int):
        super().__init__()
        self.rule_id = rule_id
        self.rules_to_check = rules_to_check
        self.min_depth = -1
        if target_amount <= -1 or target_amount > len(rules_to_check):
            self.target_amount = len(rules_to_check)
        else:
            self.target_amount = target_amount

    def _is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_check: bool) -> bool:
        if len(self.rules_to_check) == 0:
            return True
        count = 0
        for rule in self.rules_to_check:
            if rule.is_fulfilled(beaten_missions, in_region_check):
                count += 1
                if count == self.target_amount:
                    return True
        return False
    
    def _get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        if len(self.rules_to_check) == 0:
            return self.min_depth
        # It should be guaranteed by is_fulfilled that enough rules have a valid depth because they are fulfilled
        filtered_rules = [rule for rule in self.rules_to_check if rule.get_depth(beaten_missions) > -1]
        sorted_rules = sorted(filtered_rules, key = lambda rule: rule.get_depth(beaten_missions))
        required_depth = max(rule.get_depth(beaten_missions) for rule in sorted_rules[:self.target_amount])
        return max(required_depth, self.min_depth)

    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        sub_lambdas = [rule.to_lambda(player) for rule in self.rules_to_check]
        if self.target_amount == 0:
            return always_true
        if len(sub_lambdas) == 1:
            return sub_lambdas[0]
        
        def count_rules(state: CollectionState) -> bool:
            count = 0
            for sub_lambda in sub_lambdas:
                if sub_lambda(state):
                    count += 1
                    if count == self.target_amount:
                        return True
            return False
        
        return count_rules
    
    def to_slot_data(self) -> SubRuleRuleData:
        sub_rules = [rule.to_slot_data() for rule in self.rules_to_check]
        return SubRuleRuleData(
            self.rule_id,
            sub_rules,
            self.target_amount
        )
    
    def find_mandatory_mission(self) -> SC2MOGenMission | None:
        if self.target_amount > 0 and self.target_amount == len(self.rules_to_check):
            for sub_rule in self.rules_to_check:
                mandatory_mission = sub_rule.find_mandatory_mission()
                if mandatory_mission is not None:
                    return mandatory_mission
        return None


@dataclass
class SubRuleRuleData(RuleData):
    rule_id: int
    sub_rules: List[RuleData]
    amount: int

    @staticmethod
    def parse_from_dict(data: Dict[str, Any]) -> SubRuleRuleData:
        amount = data["amount"]
        rule_id = data["rule_id"]
        sub_rules: List[RuleData] = []
        for rule_data in data["sub_rules"]:
            if "sub_rules" in rule_data:
                rule: RuleData = SubRuleRuleData.parse_from_dict(rule_data)
            elif "item_ids" in rule_data:
                # Slot data converts Dict[int, int] to Dict[str, int] for some reason
                item_ids = {int(item): item_amount for (item, item_amount) in rule_data["item_ids"].items()}
                rule = ItemRuleData(
                    item_ids,
                    rule_data["visual_reqs"]
                )
            elif "amount" in rule_data:
                rule = CountMissionsRuleData(
                    **{field: value for field, value in rule_data.items()}
                )
            else:
                rule = BeatMissionsRuleData(
                    **{field: value for field, value in rule_data.items()}
                )
            sub_rules.append(rule)
        rule = SubRuleRuleData(
            rule_id,
            sub_rules,
            amount
        )
        return rule
    
    @staticmethod
    def empty() -> SubRuleRuleData:
        return SubRuleRuleData(-1, [], 0)
    
    def tooltip(self, indents: int, missions: Dict[int, SC2Mission], done_color: str, not_done_color: str) -> str:
        indent = " ".join("" for _ in range(indents))
        if self.amount == len(self.sub_rules):
            if self.amount == 1:
                return self.sub_rules[0].tooltip(indents, missions, done_color, not_done_color)
            amount = "all"
        elif self.amount == 1:
            amount = "any"
        else:
            amount = str(self.amount)
        tooltip = f"Fulfill {amount} of these conditions:\n{indent}- "
        subrule_tooltips: List[str] = []
        for rule in self.sub_rules:
            sub_tooltip = rule.tooltip(indents + 4, missions, done_color, not_done_color)
            if getattr(rule, "was_accessible", False):
                subrule_tooltips.append(f"[color={done_color}]{sub_tooltip}[/color]")
            else:
                subrule_tooltips.append(f"[color={not_done_color}]{sub_tooltip}[/color]")
        tooltip += f"\n{indent}- ".join(sub_tooltip for sub_tooltip in subrule_tooltips)
        return tooltip

    def shows_single_rule(self) -> bool:
        return self.amount == len(self.sub_rules) == 1 and self.sub_rules[0].shows_single_rule()

    def is_accessible(
        self, beaten_missions: Set[int], received_items: Dict[int, int]
    ) -> bool:
        # Sub-rule rules are accessible if enough of their child rules are accessible
        accessible_count = 0
        success = accessible_count >= self.amount
        if self.amount > 0:
            for rule in self.sub_rules:
                if rule.is_accessible(beaten_missions, received_items):
                    rule.was_accessible = True
                    accessible_count += 1
                    if accessible_count >= self.amount:
                        success = True
                        break
                else:
                    rule.was_accessible = False

        return success

class MissionEntryRules(NamedTuple):
    mission_rule: SubRuleRuleData
    layout_rule: SubRuleRuleData
    campaign_rule: SubRuleRuleData


class ItemEntryRule(EntryRule):
    items_to_check: Dict[str, int]

    def __init__(self, items_to_check: Dict[str, int]) -> None:
        super().__init__()
        self.items_to_check = items_to_check

    def _is_fulfilled(self, beaten_missions: Set[SC2MOGenMission], in_region_check: bool) -> bool:
        # Region creation should assume items can be placed,
        # but later uses (eg. starter missions) should respect that this locks a mission
        return in_region_check
    
    def _get_depth(self, beaten_missions: Set[SC2MOGenMission]) -> int:
        # Depth 0 means this rule requires 0 prior beaten missions
        return 0
    
    def to_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has_all_counts(self.items_to_check, player)
    
    def to_slot_data(self) -> RuleData:
        item_ids = {item_table[item].code: amount for (item, amount) in self.items_to_check.items()}
        visual_reqs = [item if amount == 1 else str(amount) + "x " + item for (item, amount) in self.items_to_check.items()]
        return ItemRuleData(
            item_ids,
            visual_reqs
        )
    
    def find_mandatory_mission(self) -> SC2MOGenMission | None:
        return None


@dataclass
class ItemRuleData(RuleData):
    item_ids: Dict[int, int]
    visual_reqs: List[str]

    def tooltip(self, indents: int, missions: Dict[int, SC2Mission], done_color: str, not_done_color: str) -> str:
        indent = " ".join("" for _ in range(indents))
        if len(self.visual_reqs) == 1:
            return f"Find {self.visual_reqs[0]}"
        tooltip = f"Find all of these:\n{indent}- "
        tooltip += f"\n{indent}- ".join(req for req in self.visual_reqs)
        return tooltip
    
    def shows_single_rule(self) -> bool:
        return len(self.visual_reqs) == 1

    def is_accessible(
        self, beaten_missions: Set[int], received_items: Dict[int, int]
    ) -> bool:
        return all(
            item in received_items and received_items[item] >= amount
            for (item, amount) in self.item_ids.items()
        )
