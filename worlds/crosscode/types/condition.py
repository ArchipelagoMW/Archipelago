import typing
import abc
from dataclasses import field, dataclass

from BaseClasses import CollectionState
from ..options import ShopReceiveMode

from .items import ItemData

class LogicDict(typing.TypedDict):
    mode: str
    variables: dict[str, list[str]]
    variable_definitions: dict[str, dict[str, list["Condition"]]]
    keyrings: set[str]
    item_progressive_replacements: dict[str, list[tuple[str, int]]]
    chest_clearance_levels: dict[int, str]
    shop_receive_mode: int | None
    shop_unlock_by_id: dict[int, ItemData]
    shop_unlock_by_shop: dict[str, ItemData]
    shop_unlock_by_shop_and_id: dict[tuple[str, int], ItemData]

class Condition(abc.ABC):
    @abc.abstractmethod
    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        pass

@dataclass
class ItemCondition(Condition):
    item_name: str
    amount: int = 1

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        target = self.amount
        if self.item_name in args["keyrings"]:
            target = 1

        replacements = args["item_progressive_replacements"]

        if self.item_name in replacements:
            for prog_item_name, quantity in replacements[self.item_name]:
                if state.has(prog_item_name, player, quantity):
                    return True

        return state.has(self.item_name, player, target)

@dataclass
class QuestCondition(Condition):
    quest_name: str

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return state.has(f"{self.quest_name} (Event)", player)

@dataclass
class LocationCondition(Condition):
    location_name: str

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return state.has(f"{self.location_name} (Event)", player)

@dataclass
class RegionCondition(Condition):
    target_mode: typing.Optional[str]
    region_name: str

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        # target_mode == None means that it matches in all modes.
        # so if target_mode == None, check if we can reach that region.
        # else, if the target mode matches, also check if we can reach that region.
        # otherwise, if the target mode does not match, return true (assume that it's being ANDed with other conditions)

        mode: str = args["mode"]
        if self.target_mode is None or mode == self.target_mode:
            return state.can_reach_region(self.region_name, player)

        return True

@dataclass
class AnyElementCondition(Condition):
    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return any([
            state.has("Heat", player),
            state.has("Cold", player),
            state.has("Shock", player),
            state.has("Wave", player),
        ])

@dataclass
class OrCondition(Condition):
    subconditions: list[Condition]

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return any(map(lambda x: x.satisfied(state, player, location, args), self.subconditions))

@dataclass
class AndCondition(Condition):
    subconditions: list[Condition]

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return all(map(lambda x: x.satisfied(state, player, location, args), self.subconditions))

@dataclass
class VariableCondition(Condition):
    name: str

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        variables = args["variables"]
        variable_definitions = args["variable_definitions"]

        if self.name not in variables:
            return True

        for value in variables[self.name]:
            if not all(map(lambda c: c.satisfied(state, player, location, args), variable_definitions[self.name][value])):
                return False

        return True

@dataclass
class ChestKeyCondition(Condition):
    default_level: str

    clearance_items: typing.ClassVar[dict[str, str]] =  {
        "Bronze": "Thief's Key",
        "Silver": "White Key",
        "Gold": "Radiant Key",
    }

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        chest_levels = args["chest_clearance_levels"]

        if location is None:
            raise RuntimeError("An event cannot have a chest key condition")

        level: str = chest_levels.get(location, self.default_level)

        if level == "Default":
            return True

        return state.has(ChestKeyCondition.clearance_items[level], player)

@dataclass
class ShopSlotCondition(Condition):
    shop_name: str
    item_id: int

    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        if args["shop_receive_mode"] is None:
            return True
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_item_type:
            return state.has(args["shop_unlock_by_id"][self.item_id].name, player)
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_shop:
            return state.has(args["shop_unlock_by_shop"][self.shop_name].name, player)
        if args["shop_receive_mode"] == ShopReceiveMode.option_per_slot:
            return state.has(args["shop_unlock_by_shop_and_id"][self.shop_name, self.item_id].name, player)
        return True

class NeverCondition(Condition):
    def satisfied(self, state: CollectionState, player: int, location: int | None, args: LogicDict) -> bool:
        return False

__all__ = [
    "Condition",
    "ItemCondition",
    "QuestCondition",
    "LocationCondition",
    "RegionCondition",
    "AnyElementCondition",
    "OrCondition",
    "AndCondition",
    "VariableCondition",
    "ChestKeyCondition",
    "ShopSlotCondition",
    "NeverCondition"
]
