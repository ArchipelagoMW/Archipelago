from .data.entrance_rule_data import entrance_rule_data
from .data.item_data import item_data
from .data.location_data import location_data

from .enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorTags,
)


def item_names_to_id():
    return {item.value: data.archipelago_id for item, data in item_data.items()}


def location_names_to_id():
    return {
        location.value: data.archipelago_id
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def id_to_goals():
    return {goal.value: goal for goal in ZorkGrandInquisitorGoals}


def id_to_items():
    return {data.archipelago_id: item for item, data in item_data.items()}


def id_to_locations():
    return {
        data.archipelago_id: location
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def item_groups():
    groups = dict()

    for tag in ZorkGrandInquisitorTags:
        groups[tag.value] = set()

    for item, data in item_data.items():
        if data.tags is not None:
            for tag in data.tags:
                groups[tag.value].add(item.value)

    return {k: v for k, v in groups.items() if len(v)}


def items_with_tag(tag):
    items = set()

    for item, data in item_data.items():
        if data.tags is not None and tag in data.tags:
            items.add(item)

    return items


def game_id_to_items():
    mapping = dict()

    for item, data in item_data.items():
        if data.game_state_keys is not None:
            for key in data.game_state_keys:
                mapping[key] = item

    return mapping


def location_groups():
    groups = dict()

    for tag in ZorkGrandInquisitorTags:
        groups[tag.value] = set()

    for location, data in location_data.items():
        if data.tags is not None:
            for tag in data.tags:
                groups[tag.value].add(location.value)

    return {k: v for k, v in groups.items() if len(v)}


def locations_by_region(include_deathsanity=False):
    mapping = dict()

    for region in ZorkGrandInquisitorRegions:
        mapping[region] = set()

    for location, data in location_data.items():
        if include_deathsanity is False and ZorkGrandInquisitorTags.DEATHSANITY in (
            data.tags or tuple()
        ):
            continue

        mapping[data.region].add(location)

    return mapping


def location_access_rule_for(location, player):
    data = location_data[location]

    if data.requirements is None:
        return "lambda state: True"

    lambda_string = "lambda state: "

    for i, requirement in enumerate(data.requirements):
        lambda_string += f"state.has(\"{requirement.value}\", {player})"

        if i < len(data.requirements) - 1:
            lambda_string += " and "

    return lambda_string


def entrance_access_rule_for(region_origin, region_destination, player):
    data = entrance_rule_data[(region_origin, region_destination)]

    if data is None:
        return "lambda state: True"

    lambda_string = "lambda state: "

    for i, requirement_group in enumerate(data):
        lambda_string += "("

        for ii, requirement in enumerate(requirement_group):
            requirement_type = type(requirement)

            if requirement_type in (ZorkGrandInquisitorEvents, ZorkGrandInquisitorItems):
                lambda_string += f"state.has(\"{requirement.value}\", {player})"
            elif requirement_type == ZorkGrandInquisitorRegions:
                lambda_string += f"state.can_reach(\"{requirement.value}\", \"Region\", {player})"
            elif requirement_type == ZorkGrandInquisitorLocations:
                lambda_string += f"state.can_reach(\"{requirement.value}\", \"Location\", {player})"

            if ii < len(requirement_group) - 1:
                lambda_string += " and "

        lambda_string += ")"

        if i < len(data) - 1:
            lambda_string += " or "

    return lambda_string
