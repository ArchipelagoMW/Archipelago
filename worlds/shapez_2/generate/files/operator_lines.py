from typing import Any, Iterator

from ...data import PointsItemData
from ...data.items import RewardType, all_items
from ...output import Shapez2ScenarioContainer
from ...generate.shapes import Processor


reward_types = {
    RewardType.building: ("BuildingReward", "BuildingDefinitionGroupId"),
    RewardType.island_building: ("IslandGroupReward", "GroupId"),
    RewardType.mechanic: ("MechanicReward", "MechanicId"),
    RewardType.platforms: ("ChunkLimitReward", "Amount"),
    RewardType.blueprint_points: ("BlueprintCurrencyReward", "Amount"),
    RewardType.research_points: ("ResearchPointsReward", "Amount"),
}

line_data_by_processors = {
    0: (50000, 30),
    1: (15000, 22),
    2: (15000, 18),
    3: (15000, 18),
    4: (12000, 17),
    5: (10000, 16),
    6: (8000, 16),
    7: (8000, 15),
    8: (8000, 15),
}


def get_operator_lines(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:

    multiplier = container.world.options.location_adjustments["Required shapes multiplier"]
    locked = "Lock operator lines" in container.world.options.location_modifiers

    out = []
    for line in range(container.world.options.location_adjustments["Operator lines"]):
        processors = container.world.operator_processors[line]
        shape = container.world.operator_shapes[line]
        line_obj = {
            "Id": f"Random{line + 1}",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [f"OperatorLine{line + 1}"] if locked else [],
        }
        if shape is None:
            has_crystals = Processor.CRYSTALLIZER in processors
            line_obj.update({
                "Randomized": True,
                "RandomizedUseCrystals": has_crystals,
                "StartingAmount": 1000,
                "ExponentialGrowthPercentPerLevel": 4 if has_crystals else 5,
            })
        elif isinstance(shape, int):
            line_obj.update({
                "Shape": container.world.milestone_shapes[shape][0][-1],
                "StartingAmount": max(1, line_data_by_processors[len(processors)][0] * multiplier // 100),
                "ExponentialGrowthPercentPerLevel": line_data_by_processors[len(processors)][1],
            })
        else:
            line_obj.update({
                "Shape": shape,
                "StartingAmount": max(1, line_data_by_processors[len(processors)][0] * multiplier // 100),
                "ExponentialGrowthPercentPerLevel": line_data_by_processors[len(processors)][1],
            })
        out.append(line_obj)
    return out


def get_operator_rewards(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                         other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    show_other = container.world.options.show_other_players_items.value
    all_worlds = container.world.multiworld.worlds

    def get_rewards(_item: str) -> Iterator[dict[str, str | int]]:
        _data = all_items[_item]
        _type, _key = reward_types[_data.reward_type]
        if isinstance(_data, PointsItemData):
            yield {"$type": _type, "Amount": _data.amount}
        else:
            for _rew in _data.reward_ids:
                yield {"$type": _type, _key: _rew}

    checks_count = container.world.options.location_adjustments["Operator level checks"]
    out = [{
        "MinimumLevel": max(25, checks_count + 1),
        "Rewards": [
            {"$type": "ChunkLimitReward", "Amount": 100},
            {"$type": "BlueprintCurrencyReward", "Amount": 20000},
            {"$type": "ResearchPointsReward", "Amount": 10}
        ]
    }]
    if checks_count < 24:
        out.append({
            "MinimumLevel": max(10, checks_count + 1),
            "Rewards": [
                {"$type": "ChunkLimitReward", "Amount": 50},
                {"$type": "BlueprintCurrencyReward", "Amount": 10000},
                {"$type": "ResearchPointsReward", "Amount": 4}
            ]
        })
    if checks_count < 9:
        out.append({
            "MinimumLevel": checks_count + 1,
            "Rewards": [
                {"$type": "ChunkLimitReward", "Amount": 25},
                {"$type": "BlueprintCurrencyReward", "Amount": 5000},
                {"$type": "ResearchPointsReward", "Amount": 2}
            ]
        })
    for check in range(checks_count):
        loc_item = container.world.get_location(f"Operator level {checks_count - check}").item
        if loc_item.player != container.world.player:
            if not show_other:
                rewards = [{"$type": "MechanicReward", "MechanicId": "RUAPItem"}]
            else:
                rewards = []
                add_other_item(mechanics, rewards, loc_item, other_players_items, container.world)
        else:
            rewards = [*get_rewards(loc_item.name)]
        out.append({
            "MinimumLevel": checks_count - check,
            "Rewards": rewards
        })
    return out
