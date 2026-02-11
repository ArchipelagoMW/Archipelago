from typing import Any, Iterator

from ...data import PointsItemData
from ...data.items import RewardType, all_items
from ...output import Shapez2ScenarioContainer
from ...data.required_amounts import task_lines as shape_amounts


reward_types = {
    RewardType.building: ("BuildingReward", "BuildingDefinitionGroupId"),
    RewardType.island_building: ("IslandGroupReward", "GroupId"),
    RewardType.mechanic: ("MechanicReward", "MechanicId"),
    RewardType.platforms: ("ChunkLimitReward", "Amount"),
    RewardType.blueprint_points: ("BlueprintCurrencyReward", "Amount"),
    RewardType.research_points: ("ResearchPointsReward", "Amount"),
}


def get_task_lines(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                   other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    multiplier = container.world.options.location_adjustments["Required shapes multiplier"]
    locked = "Lock task lines" in container.world.options.location_modifiers
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

    out = []
    for task_line in range(container.world.options.location_adjustments["Task lines"]):
        shapes = container.world.task_shapes[task_line]
        amounts = shape_amounts[task_line]
        tasks = []
        for task_num in range(len(shapes)):
            loc_item = container.world.get_location(f"Task #{task_line+1}-{task_num+1}").item
            if loc_item.player != container.world.player:
                if not show_other:
                    rewards = [{"$type": "MechanicReward", "MechanicId": "RUAPItem"}]
                else:
                    rewards = []
                    add_other_item(mechanics, rewards, loc_item, other_players_items, container.world)
            else:
                rewards = [*get_rewards(loc_item.name)]
            tasks.append({
                "Id": f"LocTask_{task_line}_{task_num}",
                "Rewards": rewards,
                "Costs": [{
                    "Shape": shapes[task_num],
                    "Amount": max(1, amounts[
                        -1 if task_num == len(shapes) - 1
                        else (0 if task_num == 0 else (task_num - 1) * (len(amounts) - 2) // (len(shapes) - 2) + 1)
                    ] * multiplier // 100)
                }]
            })
        out.append({
            "Title": f"Task Line #{task_line + 1}",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [f"TaskLine{task_line + 1}"] if locked else [],
            "SideQuests": tasks,
        })

    return out
