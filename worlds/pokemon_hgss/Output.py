from __future__ import annotations

import json
from pathlib import Path
from typing import Any


APHGSS_FORMAT_VERSION = 1


def build_location_item_data(world) -> list[dict[str, Any]]:
    location_item_data: list[dict[str, Any]] = []

    for location in world.multiworld.get_locations(world.player):
        item = location.item

        location_item_data.append(
            {
                "location_name": location.name,
                "location_id": location.address,
                "item_name": item.name if item else None,
                "item_id": item.code if item else None,
                "item_player": item.player if item else None,
                "locked": bool(getattr(location, "locked", False)),
            }
        )

    return location_item_data


def build_output_data(world) -> dict[str, Any]:
    return {
        "format_version": APHGSS_FORMAT_VERSION,
        "game": world.game,
        "player": world.player,
        "player_name": world.multiworld.player_name[world.player],
        "options": {
            "goal": int(world.options.goal.value),
            "hm_badge_requirements": bool(
                world.options.hm_badge_requirements.value
            ),
        },
        "item_name_to_id": world.item_name_to_id,
        "location_name_to_id": world.location_name_to_id,
        "location_item_data": build_location_item_data(world),
    }


def write_hgss_output(world, output_directory: str) -> None:
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)

    file_name = f"PokemonHGSS_Player{world.player}.aphgss"
    file_path = output_path / file_name

    output_data = build_output_data(world)

    with file_path.open("w", encoding="utf-8") as output_file:
        json.dump(output_data, output_file, indent=2)