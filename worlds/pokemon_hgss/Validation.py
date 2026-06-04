from collections import Counter

from BaseClasses import ItemClassification

from .GameChecks import (
    GAME_CHECKS,
    event_key_to_location_name,
)
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


def get_normal_location_count() -> int:
    return sum(
        1
        for location_data in LOCATION_TABLE
        if location_data.code is not None
    )


def get_required_item_count() -> int:
    return sum(
        item_data.pool_count
        for item_data in ITEM_TABLE.values()
        if (
            item_data.code is not None
            and item_data.classification != ItemClassification.filler
        )
    )


def get_filler_item_count() -> int:
    return sum(
        1
        for item_data in ITEM_TABLE.values()
        if item_data.classification == ItemClassification.filler
    )


def get_event_location_count() -> int:
    return sum(
        1
        for location_data in LOCATION_TABLE
        if location_data.code is None
    )


def get_event_item_count() -> int:
    return sum(
        1
        for item_data in ITEM_TABLE.values()
        if item_data.code is None
    )


def get_game_check_count() -> int:
    return len(GAME_CHECKS)


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


def validate_game_check_data(errors: list[str]) -> None:
    event_keys = [
        game_check.event_key
        for game_check in GAME_CHECKS
    ]

    mapped_location_names = [
        game_check.location_name
        for game_check in GAME_CHECKS
    ]

    duplicate_event_keys = get_duplicates(event_keys)
    duplicate_mapped_locations = get_duplicates(mapped_location_names)

    for event_key in duplicate_event_keys:
        errors.append(f"Duplicate game event key found: {event_key}")

    for location_name in duplicate_mapped_locations:
        errors.append(
            "Multiple game event keys map to the same AP location: "
            f"{location_name}"
        )

    normal_location_names = {
        location_data.name
        for location_data in LOCATION_TABLE
        if location_data.code is not None
    }

    mapped_location_name_set = set(mapped_location_names)

    unknown_mapped_locations = mapped_location_name_set - normal_location_names

    for location_name in sorted(unknown_mapped_locations):
        errors.append(
            "Game check maps to unknown or non-normal AP location: "
            f"{location_name}"
        )

    missing_game_checks = normal_location_names - mapped_location_name_set

    for location_name in sorted(missing_game_checks):
        errors.append(
            "Normal AP location has no game check mapping: "
            f"{location_name}"
        )

    if len(event_key_to_location_name) != len(GAME_CHECKS):
        errors.append(
            "event_key_to_location_name has fewer entries than GAME_CHECKS. "
            "This usually means duplicate event keys exist."
        )


def validate_item_pool_size(errors: list[str]) -> None:
    normal_location_count = get_normal_location_count()
    required_item_count = get_required_item_count()

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
    validate_game_check_data(errors)
    validate_item_pool_size(errors)

    raise_validation_errors(errors)


def print_validation_summary() -> None:
    print("Pokemon HGSS world data validation passed.")
    print(f"Normal locations: {get_normal_location_count()}")
    print(f"Event locations: {get_event_location_count()}")
    print(f"Required item placements: {get_required_item_count()}")
    print(f"Filler item types: {get_filler_item_count()}")
    print(f"Event item types: {get_event_item_count()}")
    print(f"Game checks: {get_game_check_count()}")
    print(f"Regions: {len(REGION_ORDER)}")
    print(f"Entrances: {len(REGION_CONNECTIONS)}")
    print(f"Location rules: {len(LOCATION_RULES)}")
    print(f"Entrance rules: {len(ENTRANCE_RULES)}")


def main() -> None:
    validate_hgss_data()
    print_validation_summary()


if __name__ == "__main__":
    main()