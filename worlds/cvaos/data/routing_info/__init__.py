from __future__ import annotations

import csv
import re
from enum import IntFlag, auto
from pathlib import Path
from typing import Iterable, Sequence

from pydantic import BaseModel, ConfigDict

__all__ = [
    "AbilityCombo",
    "RoutingInfo",
    "entrance_to_entrance_info_collection",
    "EntranceToPickupRegionInfo",
    "entrance_to_pickup_region_info_collection",
    "DefaultTransdoorConnection",
    "default_transdoor_entrance_connection_collection",
]


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"true", "1", "yes", "y"}


def _canonical_ability_name(name: str) -> str:
    # E.g. make "Panth." (in CSV) just "Panth".
    return name.strip().rstrip(".")


class AbilityCombo(IntFlag):
    """
    Requirement-mask bitflag.
    """

    None_ = 0

    Glide = auto()   # Flying Armor
    """Flying Armor"""
    Slide = auto()   # Skeleton Blaze
    """Skeleton Blaze"""
    DJump = auto()   # Malphas
    """Malphas"""
    HJump = auto()   # Hippogryph
    """Hippogryph"""
    WWalk = auto()   # Undine
    """Undine"""
    Dive = auto()    # Skula
    """Skula"""
    Panth = auto()   # Black Panther
    """Black Panther"""
    Bat = auto()     # Giant Bat
    """Giant Bat"""
    Impossible = auto()
    """Impossible requirement (never satisfied)"""
    BDash = auto()   # Grave Keeper
    """Grave Keeper"""
    Kick = auto()    # Kicker Skeleton
    """Kicker Skeleton"""

    Enemy = auto()   # Presence of an enemy
    """Presence of an enemy"""
    PixPer = auto()  # Pixel-perfect platforming
    """Pixel-perfect platforming"""
    Clip = auto()    # Platform Clip
    """Platform Clip"""
    Ceil = auto()    # Ceiling reachable
    """Ceiling reachable"""
    Vert = auto()    # Vertical room entrance
    """Vertical room entrance"""
    QSave = auto()   # Quick Save Entrance Reset
    """Quick Save Entrance Reset"""
    Tform = auto()   # Transform soul (Devil/Curly/Manticore)
    """Transform soul (Devil/Curly/Manticore)"""

# Canonical enum-key -> bitflag
_ABILITY_BY_NAME: dict[str, AbilityCombo] = {
    "None": AbilityCombo.None_,
    "Glide": AbilityCombo.Glide,
    "Slide": AbilityCombo.Slide,
    "DJump": AbilityCombo.DJump,
    "HJump": AbilityCombo.HJump,
    "WWalk": AbilityCombo.WWalk,
    "Dive": AbilityCombo.Dive,
    "Panth": AbilityCombo.Panth,
    "Bat": AbilityCombo.Bat,
    "Impossible": AbilityCombo.Impossible,
    "BDash": AbilityCombo.BDash,
    "Kick": AbilityCombo.Kick,
    "Enemy": AbilityCombo.Enemy,
    "PixPer": AbilityCombo.PixPer,
    "Clip": AbilityCombo.Clip,
    "Ceil": AbilityCombo.Ceil,
    "Vert": AbilityCombo.Vert,
    "QSave": AbilityCombo.QSave,
    "Tform": AbilityCombo.Tform,
}


def _minimize_req_masks(reqs: Iterable[int]) -> tuple[int, ...]:
    """
    Remove dominated requirement masks. If A \\subseteq B, drop B.
    """
    uniq = sorted(set(int(r) for r in reqs), key=lambda m: (m.bit_count(), m))
    out: list[int] = []
    for r in uniq:
        # dominated by something already kept? (exists o ⊆ r)
        if any((o | r) == r for o in out):
            continue

        # remove anything dominated by r (remove o where r ⊆ o)
        out = [o for o in out if not ((r | o) == o)]
        out.append(r)
    return tuple(out)


_PAREN_RE = re.compile(r"\(([^)]+)\)")


def _parse_combo_text_to_mask(text: str, *, strict: bool) -> int | None:
    """
    Parse a combo cell by extracting enum keys inside parentheses only.

    Example:
      "Malphas (DJump), ..." -> DJump | ...

    """
    if not text or not text.strip():
        return None

    mask = 0
    for inside in _PAREN_RE.findall(text):
        key = inside.strip()
        flag = _ABILITY_BY_NAME.get(key)
        if flag is None:
            if strict:
                raise ValueError(f"Unknown combo token: ({key}) in {text!r}")
            continue
        if flag != AbilityCombo.None_:
            mask |= int(flag)

    return mask or None


class RoutingInfo(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    connection_number: int
    room_id: str
    from_room: str
    to_room: str
    variant: int | None

    # Base TRUE/FALSE ability columns (treated as singleton requirement options)
    abilities: frozenset[str]

    # Raw text from Misc. combo N columns
    combo_texts: tuple[str, ...] = ()

    @classmethod
    def from_row(
        cls,
        row: dict,
        ability_headers: Iterable[str],
        combo_headers: Iterable[str],
    ) -> "RoutingInfo":
        abilities = frozenset(
            _canonical_ability_name(header)
            for header in ability_headers
            if _truthy(row.get(header))
        )

        combo_texts = tuple(
            (row.get(h) or "").strip()
            for h in combo_headers
            if (row.get(h) or "").strip()
        )

        ignore_keys = {
            "entrance_connection_number",
            "RoomID",
            "From",
            "To",
            "",
            *ability_headers,
            *combo_headers,
        }

        return cls(
            connection_number=int(row["entrance_connection_number"]),
            room_id=row["RoomID"],
            from_room=row["From"],
            to_room=row["To"],
            variant=int(row[""]) if row.get("") else None,
            abilities=abilities,
            combo_texts=combo_texts,
            **{k: v for k, v in row.items() if k not in ignore_keys},
        )

    def requires(self, ability: str) -> bool:
        return _canonical_ability_name(ability) in self.abilities

    @property
    def key(self) -> int:
        return self.connection_number

    @classmethod
    def lookup(cls, key: int | tuple[str, str]) -> "RoutingInfo":
        return lookup(key)

    def get_requirement_bitmasks(
        self,
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
    ) -> tuple[int, ...]:
        """
        Return requirement masks (each mask is one conjunctive option).

        Interpretation:
          - Each TRUE base ability column creates a singleton option mask.
          - "None" set to true generates the empty requirement option mask=0.
          - Each Misc. combo cell is parsed as a conjunction mask from parenthetical tokens.
        """
        masks: list[int] = []

        # Based singletons ( ; ) )
        for a in self.abilities:
            if a == "None":
                masks.append(0)
                continue
            flag = _ABILITY_BY_NAME.get(a)
            if flag is None:
                if strict_combo_tokens:
                    raise ValueError(f"Unknown ability column/token: {a!r}")
                continue
            if flag != AbilityCombo.None_:
                masks.append(int(flag))

        # Misc combos
        if include_combos:
            for text in self.combo_texts:
                m = _parse_combo_text_to_mask(text, strict=strict_combo_tokens)
                if m is not None:
                    masks.append(m)

        if not masks:
            return tuple()

        return _minimize_req_masks(masks) if minimize else tuple(int(m) for m in masks)


def _load() -> tuple[RoutingInfo, ...]:
    csv_path = Path(__file__).with_name("entrance_to_entrance_requirements.csv")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []

        # Ability headers run from "None" through "Kick", inclusive
        try:
            start = fieldnames.index("None")
            end = fieldnames.index("Kick")
            ability_headers = fieldnames[start : end + 1]
        except ValueError:
            ability_headers = []

        # All "Misc. combo N" columns
        combo_headers = [h for h in fieldnames if h.strip().startswith("Misc. combo")]

        out: list[RoutingInfo] = []
        for row in reader:
            if not any((v or "").strip() for v in row.values()):
                continue
            out.append(RoutingInfo.from_row(row, ability_headers, combo_headers))

    return tuple(out)


rows: tuple[RoutingInfo, ...] = _load()
by_connection_number: dict[int, RoutingInfo] = {r.connection_number: r for r in rows}
by_from_to: dict[tuple[str, str], RoutingInfo] = {(r.from_room, r.to_room): r for r in rows}
entrance_to_entrance_info_collection = list(rows)

def lookup(key: int | tuple[str, str]) -> RoutingInfo:
    if isinstance(key, int):
        return by_connection_number[key]
    return by_from_to[key]


# ---------------------------------------------------------------------------
# EntranceToPickupRegionInfo - routing from entrances to pickup regions
# ---------------------------------------------------------------------------

def _ability_and_combo_headers(
    fieldnames: Sequence[str],
) -> tuple[list[str], list[str]]:
    """Extract ability headers (None..Kick) and combo headers from fieldnames."""
    try:
        start = fieldnames.index("None")
        # Find the last ability column before combo columns
        # Look for "<alt 2>" or first "Misc. combo" as end marker
        end = None
        for i, name in enumerate(fieldnames[start:], start):
            if name.strip().startswith("Misc. combo") or name.strip() == "<alt 2>":
                end = i
                break
        if end is None:
            end = len(fieldnames)
        ability_headers = list(fieldnames[start:end])
    except ValueError:
        ability_headers = []

    combo_headers = [h for h in fieldnames if h.strip().startswith("Misc. combo")]
    return ability_headers, combo_headers


def _extract_abilities_and_combo_texts(
    row: dict,
    ability_headers: list[str],
    combo_headers: list[str],
) -> tuple[frozenset[str], tuple[str, ...]]:
    """Extract abilities and combo texts from a row."""
    abilities = frozenset(
        _canonical_ability_name(header)
        for header in ability_headers
        if _truthy(row.get(header))
    )

    combo_texts = tuple(
        (row.get(h) or "").strip()
        for h in combo_headers
        if (row.get(h) or "").strip()
    )

    return abilities, combo_texts


def _requirement_bitmasks_from(
    abilities: frozenset[str],
    combo_texts: tuple[str, ...],
    *,
    include_combos: bool = True,
    minimize: bool = True,
    strict_combo_tokens: bool = True,
) -> tuple[int, ...]:
    """Compute requirement bitmasks from abilities and combo texts."""
    masks: list[int] = []

    for a in abilities:
        if a == "None":
            masks.append(0)
            continue
        flag = _ABILITY_BY_NAME.get(a)
        if flag is None:
            if strict_combo_tokens:
                raise ValueError(f"Unknown ability column/token: {a!r}")
            continue
        if flag != AbilityCombo.None_:
            masks.append(int(flag))

    if include_combos:
        for text in combo_texts:
            m = _parse_combo_text_to_mask(text, strict=strict_combo_tokens)
            if m is not None:
                masks.append(m)

    if not masks:
        return tuple()

    return _minimize_req_masks(masks) if minimize else tuple(int(m) for m in masks)


def _entrance_identifiers_from_cell(
    cell: str,
    room_identifier: str,
) -> list[str]:
    """
    Parse the 'dest_room_identifier' cell value to entrance identifiers.

    - "Any" means all doors in the room (caller must resolve)
    - "006, 00A" means specific doors -> "009:006", "009:00A" etc.
    """
    cell = cell.strip()
    if cell.lower() == "any":
        return ["Any"]  # Special marker, caller resolves with doors_for_room

    # Parse comma-separated door IDs
    result = []
    for part in cell.split(","):
        part = part.strip()
        if part:
            # Convert to full door identifier format
            result.append(f"{room_identifier}:{part}")
    return result


class EntranceToPickupRegionInfo(BaseModel):
    """Routing info for reaching a pickup from an entrance."""
    model_config = ConfigDict(extra="allow", frozen=True)

    pickup_number: int
    pickup_room: str
    item_name: str
    variant: int | None
    entrance_identifier: str  # door_identifier (may need unique lookup)

    abilities: frozenset[str]
    combo_texts: tuple[str, ...] = ()

    @property
    def key(self) -> tuple[int, str]:
        return (self.pickup_number, self.entrance_identifier)

    def get_requirement_bitmasks(
        self,
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
    ) -> tuple[int, ...]:
        """Return requirement masks for this entrance-to-pickup route."""
        return _requirement_bitmasks_from(
            self.abilities,
            self.combo_texts,
            include_combos=include_combos,
            minimize=minimize,
            strict_combo_tokens=strict_combo_tokens,
        )


def _load_pickup_region_requirements() -> tuple[EntranceToPickupRegionInfo, ...]:
    """Load entrance-to-pickup routing from CSV."""
    # Import here to avoid circular import
    from ..entrance_info import doors_for_room

    csv_path = Path(__file__).with_name("symmetric_entrance_to_pickup_region_requirements.csv")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []

        ability_headers, combo_headers = _ability_and_combo_headers(fieldnames)

        # Track seen (entrance_identifier, pickup_number) pairs to avoid duplicates
        seen_keys: set[tuple[str, int]] = set()
        out: list[EntranceToPickupRegionInfo] = []
        for row in reader:
            if not any((v or "").strip() for v in row.values()):
                continue

            pickup_number = int(row["pickup_number"])
            pickup_room = row["Room"]
            item_name = row["Item Name"]
            variant_str = row.get("", "").strip()
            variant = int(variant_str) if variant_str else None
            entr_cell = row.get("dest_room_identifier", "").strip()

            abilities, combo_texts = _extract_abilities_and_combo_texts(
                row, ability_headers, combo_headers
            )

            # Parse entrance identifiers
            entrance_ids = _entrance_identifiers_from_cell(entr_cell, pickup_room)

            # Expand "Any" to all doors in the room
            if entrance_ids == ["Any"]:
                entrance_ids = list(doors_for_room(pickup_room))

            # Create one entry per entrance (skip duplicates)
            for ent_id in entrance_ids:
                key = (ent_id, pickup_number)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                out.append(EntranceToPickupRegionInfo(
                    pickup_number=pickup_number,
                    pickup_room=pickup_room,
                    item_name=item_name,
                    variant=variant,
                    entrance_identifier=ent_id,
                    abilities=abilities,
                    combo_texts=combo_texts,
                ))

    return tuple(out)


pickup_region_rows: tuple[EntranceToPickupRegionInfo, ...] = _load_pickup_region_requirements()
entrance_to_pickup_region_info_collection = list(pickup_region_rows)


class DefaultTransdoorConnection(BaseModel):
    """A zero-cost transition across a physical doorway."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    connection_number: int
    from_entrance: str
    to_entrance: str

    @property
    def key(self) -> tuple[str, str, int]:
        return (self.from_entrance, self.to_entrance, self.connection_number)


def _load_default_transdoor_connections(
    *,
    starting_connection_number: int,
) -> tuple[DefaultTransdoorConnection, ...]:
    csv_path = Path(__file__).with_name("default_transdoor_entrance_connections.csv")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        out: list[DefaultTransdoorConnection] = []
        next_connection_number = starting_connection_number

        for row in reader:
            if not any((value or "").strip() for value in row.values()):
                continue

            out.append(DefaultTransdoorConnection(
                connection_number=next_connection_number,
                from_entrance=(row.get("from_entrance") or "").strip(),
                to_entrance=(row.get("to_entrance") or "").strip(),
            ))
            next_connection_number += 1

    return tuple(out)


default_transdoor_rows: tuple[DefaultTransdoorConnection, ...] = _load_default_transdoor_connections(
    starting_connection_number=(max(by_connection_number, default=0) + 1),
)
default_transdoor_entrance_connection_collection = list(default_transdoor_rows)
