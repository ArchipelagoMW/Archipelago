from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_FORMAT_VERSION = 1


def load_aphgss_file(file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find .aphgss file: {file_path}")

    if file_path.suffix != ".aphgss":
        raise ValueError(
            f"Expected a .aphgss file, but got: {file_path.name}"
        )

    with file_path.open("r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    return data


def validate_aphgss_data(data: dict[str, Any]) -> None:
    format_version = data.get("format_version")

    if format_version != EXPECTED_FORMAT_VERSION:
        raise ValueError(
            "Unsupported .aphgss format version. "
            f"Expected {EXPECTED_FORMAT_VERSION}, got {format_version}."
        )

    required_fields = (
        "game",
        "player",
        "player_name",
        "options",
        "item_name_to_id",
        "location_name_to_id",
        "location_item_data",
    )

    missing_fields = [
        field_name
        for field_name in required_fields
        if field_name not in data
    ]

    if missing_fields:
        raise ValueError(
            "The .aphgss file is missing required fields: "
            f"{', '.join(missing_fields)}"
        )


def print_aphgss_summary(data: dict[str, Any]) -> None:
    location_item_data = data["location_item_data"]
    options = data["options"]

    normal_locations = [
        location_data
        for location_data in location_item_data
        if location_data["location_id"] is not None
    ]

    event_locations = [
        location_data
        for location_data in location_item_data
        if location_data["location_id"] is None
    ]

    print("Pokemon HGSS .aphgss file loaded successfully.")
    print(f"Game: {data['game']}")
    print(f"Player number: {data['player']}")
    print(f"Player name: {data['player_name']}")
    print(f"Goal option: {options['goal']}")
    print(
        "HM badge requirements: "
        f"{options['hm_badge_requirements']}"
    )
    print(f"Item IDs: {len(data['item_name_to_id'])}")
    print(f"Location IDs: {len(data['location_name_to_id'])}")
    print(f"Normal locations in output: {len(normal_locations)}")
    print(f"Event locations in output: {len(event_locations)}")

    print()
    print("First 5 location placements:")

    for location_data in location_item_data[:5]:
        print(
            "- "
            f"{location_data['location_name']} -> "
            f"{location_data['item_name']}"
        )


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:")
        print("  py -3.13 -m worlds.pokemon_hgss.Client path\\to\\file.aphgss")
        raise SystemExit(1)

    file_path = Path(sys.argv[1])

    data = load_aphgss_file(file_path)
    validate_aphgss_data(data)
    print_aphgss_summary(data)


if __name__ == "__main__":
    main()