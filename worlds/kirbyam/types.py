"""Typing helpers for KirbyAM BizHawk client integration."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from worlds._bizhawk import BizHawkContext


@runtime_checkable
class KirbyAmNetworkItem(Protocol):
    """Minimal AP network item shape consumed by KirbyAM item delivery logic."""

    item: int
    player: int


@runtime_checkable
class KirbyAmBizHawkClientContext(Protocol):
    """Typed subset of BizHawkClientContext required by KirbyAM client methods."""

    bizhawk_ctx: BizHawkContext
    server: Any
    slot_data: dict[str, Any] | None
    checked_locations: set[int]
    locations_checked: set[int]
    items_received: list[KirbyAmNetworkItem]

    auth: str | None
    game: str
    items_handling: int
    want_slot_data: bool
    watcher_timeout: float

    async def send_msgs(self, msgs: list[dict[str, Any]]) -> None:
        ...
