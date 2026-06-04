from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReceivedItemTracker:
    item_id_to_name: dict[int, str]
    processed_item_count: int = 0
    received_item_names: list[str] = field(default_factory=list)

    @classmethod
    def from_seed_data(
        cls,
        slot_data: dict[str, Any] | None,
        aphgss_data: dict[str, Any] | None,
    ) -> "ReceivedItemTracker":
        item_name_to_id: dict[str, int] = {}

        if aphgss_data:
            item_name_to_id.update(
                {
                    item_name: int(item_id)
                    for item_name, item_id
                    in aphgss_data.get("item_name_to_id", {}).items()
                }
            )

        if slot_data:
            item_name_to_id.update(
                {
                    item_name: int(item_id)
                    for item_name, item_id
                    in slot_data.get("item_name_to_id", {}).items()
                }
            )

        item_id_to_name = {
            item_id: item_name
            for item_name, item_id in item_name_to_id.items()
        }

        return cls(item_id_to_name=item_id_to_name)

    def update_seed_data(
        self,
        slot_data: dict[str, Any] | None,
        aphgss_data: dict[str, Any] | None,
    ) -> None:
        new_tracker = self.from_seed_data(slot_data, aphgss_data)
        self.item_id_to_name = new_tracker.item_id_to_name

    def get_item_name(self, item_id: int) -> str:
        return self.item_id_to_name.get(
            int(item_id),
            f"Unknown Item {item_id}",
        )

    def get_new_received_items(self, items_received) -> list[str]:
        new_items = items_received[self.processed_item_count:]
        new_item_names: list[str] = []

        for received_item in new_items:
            item_id = int(received_item.item)
            item_name = self.get_item_name(item_id)

            self.received_item_names.append(item_name)
            new_item_names.append(item_name)

        self.processed_item_count = len(items_received)

        return new_item_names