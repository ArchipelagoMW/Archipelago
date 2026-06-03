from collections import Counter

from BaseClasses import ItemClassification

from .Items import (
    ITEM_TABLE,
    item_name_groups,
)
from .Locations import (
    LOCATION_TABLE,
    location_name_groups,
)
from .Regions import (
    REGION_CONNECTIONS,
    REGION_ORDER,
)
from .Rules import (
    ENTRANCE_RULES,
    LOCATION_RULES,
)


def get_duplicates(values) -> list:
    counts = Counter(values)

    return [
        value
        for value, count in counts.items()
        if count > 1
    ]


def raise_validation_errors(errors: list[str]) -> None:
    if errors:
        error_text = "\n".join(
            f"- {error}"
            for error in errors
        )

        raise ValueError(
            "Pokemon HGSS world data validation failed:\n"
            f"{error_text}"
        )


def validate_item_data(errors: list[str]) -> None:
    item_codes = [
        item_data.code
        for item_data in ITEM_TABLE.values()
        if item_data.code is not None
    ]

    duplicate_item_codes = get_duplicates(item_codes)

    for item_code in duplicate_item_codes:
        errors.append(f"Duplicate item code found: {item_code}")

    known_item_names = set(ITEM_TABLE)

    for group_name, group_items in item_name_groups.items():
        invalid_items = group_items - known_item_names

        for item_name in sorted(invalid_items):
            errors.append(
                f"Item group '{group_name}' contains unknown item "
                f"'{item_name}'"
            )


def validate_location_data(errors: list[str]) -> None:
    location_names = [
        location_data.name
        for location_data in LOCATION_TABLE
    ]

    location_codes = [
        location_data.code
        for location_data in LOCATION_TABLE
        if location_data.code is not None
    ]

    duplicate_location_names = get_duplicates(location_names)
    duplicate_location_codes = get_duplicates(location_codes)

    for location_name in duplicate_location_names:
        errors.append(f"Duplicate location name found: {location_name}")

    for location_code in duplicate_location_codes:
        errors.append(f"Duplicate location code found: {location_code}")

    known_region_names = set(REGION_ORDER)

    for location_data in LOCATION_TABLE:
        if location_data.region not in known_region_names:
            errors.append(
                f"Location '{location_data.name}' uses unknown region "
                f"'{location_data.region}'"
            )

    known_location_names = set(location_names)

    for group_name, group_locations in location_name_groups.items():
        invalid_locations = group_locations - known_location_names

        for location_name in sorted(invalid_locations):
            errors.append(
                f"Location group '{group_name}' contains unknown location "
                f"'{location_name}'"
            )


def validate_region_data(errors: list[str]) -> None:
    duplicate_region_names = get_duplicates(REGION_ORDER)

    for region_name in duplicate_region_names:
        errors.append(f"Duplicate region name found: {region_name}")

    known_region_names = set(REGION_ORDER)

    entrance_names = [
        connection.entrance_name
        for connection in REGION_CONNECTIONS
    ]

    duplicate_entrance_names = get_duplicates(entrance_names)

    for entrance_name in duplicate_entrance_names:
        errors.append(f"Duplicate entrance name found: {entrance_name}")

    for connection in REGION_CONNECTIONS:
        if connection.source not in known_region_names:
            errors.append(
                f"Entrance '{connection.entrance_name}' has unknown source "
                f"region '{connection.source}'"
            )

        if connection.target not in known_region_names:
            errors.append(
                f"Entrance '{connection.entrance_name}' has unknown target "
                f"region '{connection.target}'"
            )


def validate_rule_data(errors: list[str]) -> None:
    known_location_names = {
        location_data.name
        for location_data in LOCATION_TABLE
    }

    known_entrance_names = {
        connection.entrance_name
        for connection in REGION_CONNECTIONS
    }

    for location_name in LOCATION_RULES:
        if location_name not in known_location_names:
            errors.append(
                f"Location rule references unknown location "
                f"'{location_name}'"
            )

    for entrance_name in ENTRANCE_RULES:
        if entrance_name not in known_entrance_names:
            errors.append(
                f"Entrance rule references unknown entrance "
                f"'{entrance_name}'"
            )


def validate_item_pool_size(errors: list[str]) -> None:
    normal_location_count = sum(
        1
        for location_data in LOCATION_TABLE
        if location_data.code is not None
    )

    required_item_count = sum(
        item_data.pool_count
        for item_data in ITEM_TABLE.values()
        if (
            item_data.code is not None
            and item_data.classification != ItemClassification.filler
        )
    )

    filler_item_names = [
        item_name
        for item_name, item_data in ITEM_TABLE.items()
        if item_data.classification == ItemClassification.filler
    ]

    if required_item_count > normal_location_count:
        errors.append(
            "Required item pool is larger than the number of normal "
            f"locations. Required items: {required_item_count}, "
            f"normal locations: {normal_location_count}."
        )

    if required_item_count < normal_location_count and not filler_item_names:
        errors.append(
            "There are more locations than required items, but no filler "
            "items are defined."
        )


def validate_hgss_data() -> None:
    errors: list[str] = []

    validate_item_data(errors)
    validate_location_data(errors)
    validate_region_data(errors)
    validate_rule_data(errors)
    validate_item_pool_size(errors)

    raise_validation_errors(errors)