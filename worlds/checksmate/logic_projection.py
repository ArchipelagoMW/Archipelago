"""Monotonic AP logic metrics derived from the APMW v2 semantic projection."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Mapping

from BaseClasses import CollectionState

from .locations import BoardStage, geometry_unlocks_for_stage
from .options import resolve_piece_upgrade_preferences, resolve_piece_upgrade_ratio
from .apmw_contract import ApmwContractV2, GeometryStage
from .contract_resource import load_production_contract, mode_item_maxima
from .semantic_projection import (
    ItemCount,
    ProjectionInput,
    SemanticSeeds,
    UnlockCount,
    UpgradePreference,
    project_exact_active_material,
    project_exact_active_non_primary_count,
)


_FUNDAMENTAL_ENVELOPE_AXES = (
    "Chessmen",
    "Material",
    "Castler",
    "Progressive Consul",
)
_LEGACY_ENVELOPE_AXES = (
    "Progressive Pawn",
    "Progressive Minor Piece",
    "Progressive Major Piece",
    "Progressive Major To Queen",
    "Progressive Jack",
    "Progressive Consul",
)
_MAX_EXACT_ENVELOPE_CELLS = 10_000


@dataclass(frozen=True)
class LogicMetrics:
    material: int
    chessmen: int
    castlers: int


class WorldLogicProjection:
    """Builds cached stage-local suffix envelopes for one generated world.

    Small Fundamental count spaces use the exact semantic projector once per
    cell, followed by a componentwise suffix minimum. Large Fundamental spaces
    and Legacy use a cheaper active-slot floor. Both forms are monotonic and no
    greater than exact material.
    """

    def __init__(
        self,
        options,
        seeds: SemanticSeeds = SemanticSeeds(),
        contract: ApmwContractV2 | None = None,
    ):
        self.options = options
        self.seeds = seeds
        self.contract = contract or load_production_contract()
        self.itemization = (
            "fundamental"
            if options.progression_itemization.value
            == options.progression_itemization.option_fundamental
            else "legacy"
        )
        self.axes = (
            _FUNDAMENTAL_ENVELOPE_AXES
            if self.itemization == "fundamental"
            else _LEGACY_ENVELOPE_AXES
        )
        self.preferences = _upgrade_preferences(options, self.itemization)
        self.maxima = dict(mode_item_maxima(self.itemization))
        self._obtainable = {
            name: self.maxima.get(name, 0)
            for name in self.axes
        }
        self._obtainable_king_promotions = self.maxima[
            "Progressive King Promotion"
        ]
        self._tables: dict[
            tuple[BoardStage, tuple[int, ...]],
            tuple[tuple[int, ...], tuple[int, ...] | None],
        ] = {}
        self._active_count_cache: dict[
            tuple[BoardStage, tuple[int, ...]],
            int,
        ] = {}

    def set_obtainable_counts(self, counts: Mapping[str, int]) -> None:
        self._obtainable = {
            name: min(
                max(0, int(counts.get(name, 0))),
                self.maxima.get(name, 0),
            )
            for name in self.axes
        }
        self._obtainable_king_promotions = min(
            max(0, int(counts.get("Progressive King Promotion", 0))),
            self.maxima["Progressive King Promotion"],
        )
        self._tables.clear()
        self._active_count_cache.clear()

    def metrics(
        self,
        state: CollectionState,
        player: int,
        stage: BoardStage,
    ) -> LogicMetrics:
        counts = {
            name: self._normalized_count(state.count(name, player), name)
            for name in (
                *self.axes,
                "Progressive King Promotion",
            )
        }
        return self.metrics_from_counts(counts, stage)

    def metrics_from_counts(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> LogicMetrics:
        normalized = {
            name: self._normalized_count(counts.get(name, 0), name)
            for name in (
                *self.axes,
                "Progressive King Promotion",
            )
        }
        maxima = tuple(
            max(self._obtainable[name], normalized[name])
            for name in self.axes
        )
        active_chessmen = self._logic_chessmen_floor(normalized, stage)
        dimensions, table = self._envelope(stage, maxima)
        if table is None:
            material = self._slot_floor(active_chessmen)
        else:
            material = table[_flat_index(
                tuple(normalized[name] for name in self.axes),
                dimensions,
            )]
        material += (
            normalized["Progressive King Promotion"]
            * self.contract.expected_material["king_promotion"]
        )

        geometry = self._geometry(stage)
        # Two future consuls still leave at least five home-rank slots on the
        # smallest board, so all normalized locked Castlers remain active.
        safe_castler_slots = max(
            0,
            geometry.files
            - 1
            - self.maxima["Progressive Consul"],
        )
        castlers = 0
        if self.itemization == "fundamental":
            castlers = min(
                normalized["Castler"],
                normalized["Chessmen"],
                normalized["Material"]
                * self.contract.expected_material["material_item"]
                // self.contract.castler.normalized_cost,
                safe_castler_slots,
            )
        return LogicMetrics(material, active_chessmen, castlers)

    def maximum_material(self, stage: BoardStage) -> int:
        counts = dict(self._obtainable)
        counts["Progressive King Promotion"] = (
            self._obtainable_king_promotions
        )
        return self.metrics_from_counts(counts, stage).material

    def exact_active_material(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> int:
        normalized = {
            name: self._normalized_count(count, name)
            for name, count in counts.items()
            if name in self.maxima
        }
        return project_exact_active_material(
            self.contract,
            self._projection_input(normalized, stage),
        )

    def exact_active_non_primary_count(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> int:
        normalized = {
            name: self._normalized_count(counts.get(name, 0), name)
            for name in self.axes
        }
        return self._active_non_primary_count(normalized, stage)

    def _logic_chessmen_floor(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> int:
        if self.itemization == "fundamental":
            # Future Material can turn Pawn slots into non-pawns, whose capacity
            # is the safe lower bound for every reachable future composition.
            owned_slots = (
                counts["Chessmen"]
                + counts["Progressive Consul"]
            )
            return min(
                owned_slots,
                self._geometry(stage).non_pawn_capacity,
            )

        geometry = self._geometry(stage)
        active_non_pawns = min(
            sum(
                counts[name]
                for name in (
                    "Progressive Minor Piece",
                    "Progressive Major Piece",
                    "Progressive Jack",
                    "Progressive Consul",
                )
            ),
            geometry.non_pawn_capacity,
        )
        active_pawn_capacity = (
            geometry.gross_pawn_capacity
            - max(0, active_non_pawns - (geometry.files - 1))
        )
        return active_non_pawns + min(
            counts["Progressive Pawn"],
            active_pawn_capacity,
        )

    def _envelope(
        self,
        stage: BoardStage,
        maxima: tuple[int, ...],
    ) -> tuple[tuple[int, ...], tuple[int, ...] | None]:
        key = stage, maxima
        if key in self._tables:
            return self._tables[key]

        dimensions = tuple(maximum + 1 for maximum in maxima)
        cells = 1
        for dimension in dimensions:
            cells *= dimension
        if (
            self.itemization == "legacy"
            or cells > _MAX_EXACT_ENVELOPE_CELLS
        ):
            # Every active non-primary semantic slot is worth at least one pawn.
            result = dimensions, None
            self._tables[key] = result
            return result

        values = [0] * cells
        for coordinates in product(*(range(dimension) for dimension in dimensions)):
            counts = {
                name: count
                for name, count in zip(self.axes, coordinates)
                if count
            }
            values[_flat_index(coordinates, dimensions)] = (
                project_exact_active_material(
                    self.contract,
                    self._projection_input(counts, stage),
                )
            )

        for axis in range(len(dimensions)):
            reverse_ranges = (
                range(dimension - 1, -1, -1)
                for dimension in dimensions
            )
            for coordinates_value in product(*reverse_ranges):
                coordinates = list(coordinates_value)
                if coordinates[axis] + 1 >= dimensions[axis]:
                    continue
                current_index = _flat_index(tuple(coordinates), dimensions)
                coordinates[axis] += 1
                future_index = _flat_index(tuple(coordinates), dimensions)
                values[current_index] = min(
                    values[current_index],
                    values[future_index],
                )

        result = dimensions, tuple(values)
        self._tables[key] = result
        return result

    def _slot_floor(
        self,
        active_chessmen: int,
    ) -> int:
        return active_chessmen * self.contract.expected_material["pawn"]

    def _active_non_primary_count(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> int:
        normalized = tuple(counts[name] for name in self.axes)
        key = stage, normalized
        if key not in self._active_count_cache:
            projection_counts = {
                name: count
                for name, count in zip(self.axes, normalized)
                if count
            }
            self._active_count_cache[key] = (
                project_exact_active_non_primary_count(
                    self.contract,
                    self._projection_input(projection_counts, stage),
                )
            )
        return self._active_count_cache[key]

    def _projection_input(
        self,
        counts: Mapping[str, int],
        stage: BoardStage,
    ) -> ProjectionInput:
        files, ranks = geometry_unlocks_for_stage(stage)
        return ProjectionInput(
            self.itemization,
            "stable",
            self.seeds,
            tuple(
                ItemCount(name, count)
                for name, count in sorted(counts.items())
                if count
            ),
            (
                UnlockCount("board-file-unlock", files),
                UnlockCount("board-rank-unlock", ranks),
            ),
            self.preferences,
        )

    def _geometry(self, stage: BoardStage) -> GeometryStage:
        stage_id = {
            BoardStage.Board8x8: "8x8",
            BoardStage.Board10x8: "10x8",
            BoardStage.Board10x10: "10x10",
            BoardStage.Board12x10: "12x10",
            BoardStage.Board12x12: "12x12",
        }[stage]
        return next(value for value in self.contract.stages if value.stage_id == stage_id)

    def _normalized_count(self, count: int, name: str) -> int:
        maximum = self.maxima.get(name, 0)
        return min(max(0, int(count)), maximum)

def _upgrade_preferences(
    options,
    itemization: str,
) -> tuple[UpgradePreference, ...]:
    if (
        itemization == "fundamental"
        and not options.piece_upgrade_priority.value
        and options.fairy_chess_pawn_upgrades.value
        != options.fairy_chess_pawn_upgrades.option_configure
    ):
        return ()
    resolved = resolve_piece_upgrade_preferences(
        options.fairy_chess_pawn_upgrades,
        options.piece_upgrade_preferences,
        options.piece_upgrade_priority,
    )
    ratios = resolve_piece_upgrade_ratio(options.piece_upgrade_ratio)
    if isinstance(resolved, dict):
        priorities = resolved
    else:
        priorities = {
            action: len(resolved) - index
            for index, action in enumerate(resolved)
        }
    return tuple(
        UpgradePreference(
            action,
            priority,
            ratios.get(action, 1),
            1,
        )
        for action, priority in priorities.items()
        if priority > 0
    )


def _flat_index(coordinates: tuple[int, ...], dimensions: tuple[int, ...]) -> int:
    index = 0
    for coordinate, dimension in zip(coordinates, dimensions):
        index = index * dimension + coordinate
    return index
