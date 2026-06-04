from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LocationTracker:
    location_name_to_id: dict[str, int]
    checked_location_ids: set[int] = field(default_factory=set)

    @classmethod
    def from_seed_data(
        cls,
        slot_data: dict[str, Any] | None,
        aphgss_data: dict[str, Any] | None,
    ) -> "LocationTracker":
        location_name_to_id: dict[str, int] = {}

        if aphgss_data:
            location_name_to_id.update(
                {
                    location_name: int(location_id)
                    for location_name, location_id
                    in aphgss_data.get("location_name_to_id", {}).items()
                }
            )

        if slot_data:
            location_name_to_id.update(
                {
                    location_name: int(location_id)
                    for location_name, location_id
                    in slot_data.get("location_name_to_id", {}).items()
                }
            )

        return cls(location_name_to_id=location_name_to_id)

    def update_checked_locations(self, location_ids) -> None:
        for location_id in location_ids:
            self.checked_location_ids.add(int(location_id))

    def get_location_id(self, location_name: str) -> int | None:
        return self.location_name_to_id.get(location_name)

    def has_checked_location_id(self, location_id: int) -> bool:
        return int(location_id) in self.checked_location_ids

    def has_checked_location_name(self, location_name: str) -> bool:
        location_id = self.get_location_id(location_name)

        if location_id is None:
            return False

        return self.has_checked_location_id(location_id)

    def mark_location_checked(self, location_name: str) -> tuple[int | None, bool]:
        location_id = self.get_location_id(location_name)

        if location_id is None:
            return None, False

        if self.has_checked_location_id(location_id):
            return location_id, False

        self.checked_location_ids.add(location_id)

        return location_id, True