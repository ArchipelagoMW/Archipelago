from dataclasses import dataclass, field
from typing import Any

from .locations import BoardStage, location_names_for_stage


@dataclass(slots=True)
class PoolAccounting:
    """Mutable item accounting owned by one ChecksMate world."""

    used: dict[str, int] = field(default_factory=dict)
    remaining: dict[str, int] = field(default_factory=dict)

    def reset(self) -> None:
        self.used.clear()
        self.remaining.clear()

    def used_count(self, item_name: str) -> int:
        return self.used.get(item_name, 0)

    def add_used(self, item_name: str, count: int = 1) -> None:
        self.used[item_name] = self.used_count(item_name) + count

    def set_used(self, item_name: str, count: int) -> None:
        self.used[item_name] = count

    def set_remaining(self, item_name: str, count: int) -> None:
        self.remaining[item_name] = count

    def consume(self, item_name: str, quantity: int | None = None) -> None:
        self.add_used(item_name)
        if quantity is not None:
            self.remaining.setdefault(item_name, quantity)
            self.remaining[item_name] -= 1

    def used_player_view(self, player: int) -> dict[int, dict[str, int]]:
        """Return the legacy player-keyed shape while retaining one source of truth."""
        return {player: self.used}

    def remaining_player_view(self, player: int) -> dict[int, dict[str, int]]:
        """Return the legacy player-keyed shape while retaining one source of truth."""
        return {player: self.remaining}


@dataclass(frozen=True, slots=True)
class PoolCapacity:
    """Location capacity available to one world's generated item pool."""

    location_count: int
    reserved_locations: int = 0

    @classmethod
    def for_world(
        cls,
        world: Any,
        super_sized: bool,
        reserved_locations: int = 0,
    ) -> "PoolCapacity":
        stage = BoardStage.Board12x12 if super_sized else BoardStage.Board8x8
        tactics = world.options.enable_tactics
        tactics_mode = (
            "none"
            if tactics.value == tactics.option_none
            else "turns"
            if tactics.value == tactics.option_turns
            else "all"
        )
        location_count = len(location_names_for_stage(stage, tactics_mode))
        return cls(
            location_count=location_count,
            reserved_locations=min(max(0, reserved_locations), location_count),
        )

    @property
    def item_limit(self) -> int:
        return self.location_count - self.reserved_locations

    def available(self, pooled_items: int, committed_items: int = 0) -> int:
        return max(0, self.item_limit - pooled_items - committed_items)
