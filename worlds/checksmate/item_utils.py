from __future__ import annotations

from collections.abc import Mapping
from math import ceil
from typing import Any

from .contract_resource import load_production_contract, mode_item_maxima
from .items import (
    GEOMETRY_ITEMS,
    LEGACY_CHESSMEN_GROUP,
    ItemizationMode,
    item_allowed_in_mode,
    item_name_groups,
    item_table,
    itemization_mode,
)
from .options import piece_limit_options, piece_type_limit_options


def item_maxima(mode: ItemizationMode | str) -> dict[str, int]:
    maxima = dict(mode_item_maxima(ItemizationMode(mode).value))
    for name, data in item_table.items():
        maxima.setdefault(name, data.quantity)
    return maxima


def pocket_item_limit(options: Any) -> int:
    return min(
        options.max_pocket.value,
        options.pocket_limit_by_pocket.value * 3,
    )


def occupied_pockets(pocket_items: int, limit_per_pocket: int) -> int:
    if pocket_items <= 0 or limit_per_pocket <= 0:
        return 0
    return min(3, ceil(pocket_items / limit_per_pocket))


def chessmen_count(
    counts: Mapping[str, int],
    mode: ItemizationMode | str,
    limit_per_pocket: int,
) -> int:
    itemization = ItemizationMode(mode)
    if itemization is ItemizationMode.FUNDAMENTAL:
        chessmen = counts.get("Chessmen", 0)
    else:
        chessmen = sum(
            counts.get(name, 0)
            for name in item_name_groups[LEGACY_CHESSMEN_GROUP]
        )
    return chessmen + occupied_pockets(
        counts.get("Progressive Pocket", 0),
        limit_per_pocket,
    )


def collection_item_maximum(options: Any, item_name: str) -> int:
    mode = itemization_mode(options)
    if (
        item_name not in item_table
        or not item_allowed_in_mode(item_name, mode)
        or (
            item_name in GEOMETRY_ITEMS
            and options.goal.value == options.goal.option_single
        )
    ):
        return 0
    maximum = item_maxima(mode).get(item_name, 0)
    if item_name == "Super-Size Me":
        maximum = 1
    if item_name == "Progressive Pocket":
        maximum = min(maximum, pocket_item_limit(options))
    return max(0, maximum)


def generated_item_maximum(world: Any, item_name: str) -> int:
    options = world.options
    maximum = collection_item_maximum(options, item_name)
    if maximum <= 0:
        return 0

    option_maxima = {
        "Progressive AI Intelligence Malus": options.max_engine_penalties.value,
        "Progressive Pocket": pocket_item_limit(options),
        "Progressive King Promotion": options.fairy_kings.value,
        "Progressive Consul": options.max_kings.value - 1,
    }
    if item_name in option_maxima:
        maximum = min(maximum, option_maxima[item_name])

    if (
        item_name == "Progressive Jack"
        and options.asymmetric_trades.value
        == options.asymmetric_trades.option_disabled
    ):
        return 0

    if item_name in piece_type_limit_options:
        configured_limit = piece_type_limit_options[item_name](options).value
        if configured_limit > 0:
            army_ids = tuple(getattr(world, "army_ids", ()))
            if not army_ids:
                army_ids = tuple(
                    getattr(world, "armies", {}).get(world.player, ())
                )
            type_count = sum(
                world.piece_types_by_army[army_id][item_name]
                for army_id in army_ids
            )
            option_limit = configured_limit * type_count
            if item_name == "Progressive Major Piece":
                queen_maximum = item_maxima(
                    itemization_mode(options)
                )["Progressive Major To Queen"]
                queen_type_limit = piece_type_limit_options[
                    "Progressive Major To Queen"
                ](options).value
                if queen_type_limit > 0:
                    queen_types = sum(
                        world.piece_types_by_army[army_id][
                            "Progressive Major To Queen"
                        ]
                        for army_id in army_ids
                    )
                    queen_maximum = min(
                        queen_maximum,
                        queen_type_limit * queen_types,
                    )
                queen_total_limit = piece_limit_options[
                    "Progressive Major To Queen"
                ](options).value
                if queen_total_limit > 0:
                    queen_maximum = min(
                        queen_maximum,
                        queen_total_limit,
                    )
                option_limit += queen_maximum
            maximum = min(maximum, option_limit)

    if item_name in piece_limit_options:
        configured_limit = piece_limit_options[item_name](options).value
        if configured_limit > 0:
            maximum = min(maximum, configured_limit)

    return max(0, maximum)


def castling_requirement(options: Any) -> int:
    if itemization_mode(options) is ItemizationMode.FUNDAMENTAL:
        return 1
    return load_production_contract().castler.maximum


def required_castler_material_items(castlers: int) -> int:
    contract = load_production_contract()
    return ceil(
        castlers
        * contract.castler.normalized_cost
        / contract.expected_material["material_item"]
    )


def effective_fundamental_castlers(
    castlers: int,
    chessmen: int,
    material_items: int,
    contract=None,
) -> int:
    contract = contract or load_production_contract()
    return min(
        castlers,
        chessmen,
        material_items
        * contract.expected_material["material_item"]
        // contract.castler.normalized_cost,
    )


def get_parents(item_name: str) -> tuple[tuple[str, int], ...]:
    """Return the parent item requirements for an item."""
    return item_table[item_name].parents


def get_children(item_name: str) -> list[str]:
    """Return items that consume the given item as a parent."""
    return [
        child
        for child in item_table
        if any(
            parent_name == item_name
            for parent_name, _ in item_table[child].parents
        )
    ]
