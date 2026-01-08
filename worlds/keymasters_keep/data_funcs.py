from typing import Dict, List, Optional, Union

from .data.item_data import item_data, KeymastersKeepItemData
from .data.location_data import location_data, KeymastersKeepLocationData

from .enums import KeymastersKeepItems, KeymastersKeepLocations, KeymastersKeepGoals


flat_location_data: List[KeymastersKeepLocationData] = list()

d: Union[KeymastersKeepLocationData, List[KeymastersKeepLocationData]]
for _, d in location_data.items():
    if isinstance(d, KeymastersKeepLocationData):
        flat_location_data.append(d)
        continue

    flat_location_data.extend(d)


def item_names_to_id() -> Dict[str, int]:
    return {item.value: data.archipelago_id for item, data in item_data.items()}


def location_names_to_id() -> Dict[str, int]:
    names_to_id: Dict[str, int] = dict()

    for location, data in location_data.items():
        if isinstance(data, KeymastersKeepLocationData):
            names_to_id[location.value] = data.archipelago_id
            continue

        for nested_data in data:
            names_to_id[nested_data.name] = nested_data.archipelago_id

    return names_to_id


def id_to_items() -> Dict[int, KeymastersKeepItems]:
    return {data.archipelago_id: item for item, data in item_data.items()}


def id_to_item_data() -> Dict[int, KeymastersKeepItemData]:
    return {data.archipelago_id: data for data in item_data.values()}


def id_to_location_data() -> Dict[int, KeymastersKeepLocations]:
    return {
        data.archipelago_id: data
        for data in flat_location_data
        if data.archipelago_id is not None
    }


def item_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    item: KeymastersKeepItems
    data: KeymastersKeepItemData
    for item, data in item_data.items():
        if data.tags is not None:
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(item.value)

    return {k: v for k, v in groups.items() if len(v)}


def location_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    data: KeymastersKeepLocationData
    for data in flat_location_data:
        if data.tags is not None:
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(data.name)

    return {k: v for k, v in groups.items() if len(v)}


def id_to_goals() -> Dict[int, KeymastersKeepGoals]:
    return {goal.value: goal for goal in KeymastersKeepGoals}


def access_rule_for(items: Optional[List[KeymastersKeepItems]], player: int) -> Optional[str]:
    if items is None:
        return None
    elif len(items) == 1:
        return f"lambda state: state.has(\"{items[0].value}\", {player})"

    item_strings: List[str] = list()

    item: KeymastersKeepItems
    for item in items:
        item_strings.append(f"\"{item.value}\"")

    return f"lambda state: state.has_all([{', '.join(item_strings)}], {player})"
