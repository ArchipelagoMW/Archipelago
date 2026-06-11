from __future__ import annotations

import logging
import re
from enum import IntFlag, auto
from typing import Iterable

from ..._pydantic_compat import BaseModel
from .._csv_resources import open_csv, open_csv_if_exists

__all__ = [
    "AbilityCombo",
    "RoutingInfo",
    "entrance_to_entrance_info_collection",
    "EntranceToPickupRegionInfo",
    "entrance_to_pickup_region_info_collection",
    "lookup_pickup_region_requirement",
    "EntranceToEnemyRegionInfo",
    "entrance_to_enemy_region_info_collection",
    "by_enemy_name_for_enemy_regions",
    "by_enemy_number_for_enemy_regions",
    "enemy_meta_by_number",
    "resolve_enemy_number",
    "TransdoorConnection",
    "transdoor_connection_collection",
    "by_from_entrance_for_transdoor",
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
    Tform = auto()   # Devil/Curly/Manticore
    """Devil/Curly/Manticore"""

    Enemy = auto()   # Presence of a kickable enemy
    """Presence of a kickable enemy"""
    PixPer = auto()  # Pixel-perfect platforming
    """Pixel-perfect platforming"""
    Clip = auto()    # Platform Clip
    """Platform Clip"""
    Floor = auto()   # Floor reachable and hittable
    """Floor reachable and hittable"""
    Ceil = auto()    # Ceiling reachable and hittable
    """Ceiling reachable and hittable"""
    Vert = auto()    # Vertical room entrance
    """Vertical room entrance"""
    QSave = auto()   # Quick Save entrance reset
    """Quick Save entrance reset"""

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
    "Tform": AbilityCombo.Tform,
    "Enemy": AbilityCombo.Enemy,
    "PixPer": AbilityCombo.PixPer,
    "Clip": AbilityCombo.Clip,
    "Floor": AbilityCombo.Floor,
    "Ceil": AbilityCombo.Ceil,
    "Vert": AbilityCombo.Vert,
    "QSave": AbilityCombo.QSave,
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


def _ability_and_combo_headers(fieldnames: Iterable[str]) -> tuple[list[str], list[str]]:
    names = list(fieldnames or [])
    try:
        start = names.index("None")
        end = None
        for i, name in enumerate(names[start:], start):
            if name.strip().startswith("Misc. combo") or name.strip() == "<alt 2>":
                end = i
                break
        if end is None:
            end = len(names)
        ability_headers = names[start:end]
    except ValueError:
        ability_headers = []
    combo_headers = [h for h in names if h.strip().startswith("Misc. combo")]
    return ability_headers, combo_headers


def _extract_abilities_and_combo_texts(
    row: dict,
    ability_headers: Iterable[str],
    combo_headers: Iterable[str],
) -> tuple[frozenset[str], tuple[str, ...]]:
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


class TransdoorConnection(BaseModel):
    """
    Maps one side of a physical door to the entrance node on the other side.

    :param from_entrance: Entrance node on one side of the door.
    :param to_entrance: Entrance node on the opposite side of the same door.
    """

    class Config:
        frozen = True

    from_entrance: str
    to_entrance: str


def _load_transdoor_connections() -> tuple[TransdoorConnection, ...]:
    out: list[TransdoorConnection] = []
    for row in open_csv(__name__, "default_transdoor_entrance_connections.csv"):
        if not any((v or "").strip() for v in row.values()):
            continue
        out.append(TransdoorConnection(
            from_entrance=row["from_entrance"].strip(),
            to_entrance=row["to_entrance"].strip(),
        ))

    # Apply overrides: rows with does_exist=FALSE are removed, rows with
    # is_override=TRUE are added in their place.
    override_reader = open_csv_if_exists(__name__, "override_transdoor_entrance_connections.csv")
    if override_reader is not None:
        removals: set[tuple[str, str]] = set()
        additions: list[TransdoorConnection] = []
        for row in override_reader:
            if not any((v or "").strip() for v in row.values()):
                continue
            from_e = row["from_entrance"].strip()
            to_e = row["to_entrance"].strip()
            if not _truthy(row.get("does_exist")):
                removals.add((from_e, to_e))
            if _truthy(row.get("is_override")):
                additions.append(TransdoorConnection(from_entrance=from_e, to_entrance=to_e))
        out = [c for c in out if (c.from_entrance, c.to_entrance) not in removals]
        out.extend(additions)

    return tuple(out)


def _entrance_identifiers_from_cell(room_id: str, cell: str | None) -> set[str]:
    """
    Interpret the dest_room_identifier column and return the set of entrance identifiers
    for arrivals in room_id.

    For "Any", returns all entrance nodes that arrive in room_id according to
    by_from_entrance_for_transdoor. For a specific neighbor room (or comma-separated list),
    constructs f"{neighbor}:{room_id}" and includes it only if it exists in
    by_from_entrance_for_transdoor. This means removing a door from
    default_transdoor_entrance_connections.csv automatically excludes it here.
    """
    if cell is None:
        return set()

    text = cell.strip()
    if not text:
        return set()

    if text.lower() == "any":
        return set(_arrivals_by_room.get(room_id, set()))

    identifiers: set[str] = set()
    for neighbor in (part.strip() for part in text.split(",") if part.strip()):
        entrance = f"{neighbor}:{room_id}"
        if entrance in by_from_entrance_for_transdoor:
            identifiers.add(entrance)
    return identifiers


def _requirement_bitmasks_from(
    abilities: Iterable[str],
    combo_texts: Iterable[str],
    *,
    include_combos: bool = True,
    minimize: bool = True,
    strict_combo_tokens: bool = True,
) -> tuple[int, ...]:
    masks: list[int] = []

    for ability in abilities:
        if ability == "None":
            masks.append(0)
            continue
        flag = _ABILITY_BY_NAME.get(ability)
        if flag is None:
            if strict_combo_tokens:
                raise ValueError(f"Unknown ability column/token: {ability!r}")
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


class RoutingInfo(BaseModel):
    class Config:
        extra = "allow"
        frozen = True

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
        abilities, combo_texts = _extract_abilities_and_combo_texts(
            row, ability_headers, combo_headers
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
        return _requirement_bitmasks_from(
            self.abilities,
            self.combo_texts,
            include_combos=include_combos,
            minimize=minimize,
            strict_combo_tokens=strict_combo_tokens,
        )


def _load() -> tuple[RoutingInfo, ...]:
    reader = open_csv(__name__, "entrance_to_entrance_requirements.csv")
    ability_headers, combo_headers = _ability_and_combo_headers(reader.fieldnames or [])

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


class EntranceToPickupRegionInfo(BaseModel):
    """
    Requirements for reaching a pickup region from a specific entrance.

    These requirements are symmetric: they apply both to reaching the pickup region
    and returning from it.
    """

    class Config:
        extra = "allow"
        frozen = True

    pickup_number: int
    pickup_room: str
    item_name: str
    variant: int | None
    entrance_identifier: str

    abilities: frozenset[str]
    combo_texts: tuple[str, ...] = ()

    @classmethod
    def from_row(
        cls,
        row: dict,
        ability_headers: Iterable[str],
        combo_headers: Iterable[str],
        entrance_identifier: str,
    ) -> "EntranceToPickupRegionInfo":
        abilities, combo_texts = _extract_abilities_and_combo_texts(
            row, ability_headers, combo_headers
        )

        return cls(
            pickup_number=int(row["pickup_number"]),
            pickup_room=row["Room"],
            item_name=row["Item Name"],
            variant=int(row[""]) if row.get("") else None,
            entrance_identifier=entrance_identifier,
            abilities=abilities,
            combo_texts=combo_texts,
            **{k: v for k, v in row.items() if k not in {"pickup_number", "Room", "Item Name", "", "dest_room_identifier", *ability_headers, *combo_headers}},
        )

    @property
    def key(self) -> tuple[str, int]:
        return (self.entrance_identifier, self.pickup_number)

    @property
    def pickup_region_identifier(self) -> int:
        return self.pickup_number

    def get_requirement_bitmasks(
        self,
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
    ) -> tuple[int, ...]:
        return _requirement_bitmasks_from(
            self.abilities,
            self.combo_texts,
            include_combos=include_combos,
            minimize=minimize,
            strict_combo_tokens=strict_combo_tokens,
        )


def _load_pickup_region_requirements() -> tuple[EntranceToPickupRegionInfo, ...]:
    reader = open_csv(__name__, "symmetric_entrance_to_pickup_region_requirements.csv")
    ability_headers, combo_headers = _ability_and_combo_headers(reader.fieldnames or [])

    seen_keys: set[tuple[str, int]] = set()
    out: list[EntranceToPickupRegionInfo] = []
    for row in reader:
        if not any((v or "").strip() for v in row.values()):
            continue

        room_id = row.get("Room", "").strip()
        entrances = _entrance_identifiers_from_cell(room_id, row.get("dest_room_identifier"))
        if not entrances:
            raise ValueError(f"No entrance identifiers resolved for pickup_number {row.get('pickup_number')} in room {room_id!r}")

        for entrance_identifier in sorted(entrances):
            key = (entrance_identifier, int(row["pickup_number"]))
            if key in seen_keys:
                continue
            seen_keys.add(key)
            out.append(
                EntranceToPickupRegionInfo.from_row(
                    row, ability_headers, combo_headers, entrance_identifier
                )
            )

    return tuple(out)


# Transdoor connections must be loaded before pickup region requirements, because
# _entrance_identifiers_from_cell (called during pickup region loading) relies on
# by_from_entrance_for_transdoor and _arrivals_by_room.
transdoor_connection_rows: tuple[TransdoorConnection, ...] = _load_transdoor_connections()
transdoor_connection_collection: list[TransdoorConnection] = list(transdoor_connection_rows)
by_from_entrance_for_transdoor: dict[str, TransdoorConnection] = {
    r.from_entrance: r for r in transdoor_connection_rows
}
_arrivals_by_room: dict[str, set[str]] = {}
for _r in transdoor_connection_rows:
    _, _dest_room = _r.from_entrance.split(":", 1)
    _arrivals_by_room.setdefault(_dest_room, set()).add(_r.from_entrance)

pickup_region_rows: tuple[EntranceToPickupRegionInfo, ...] = _load_pickup_region_requirements()
by_pickup_number_for_pickup_regions: dict[int, list[EntranceToPickupRegionInfo]] = {}
by_entrance_identifier_for_pickup_regions: dict[str, list[EntranceToPickupRegionInfo]] = {}
by_entrance_and_pickup: dict[tuple[str, int], EntranceToPickupRegionInfo] = {}

for row in pickup_region_rows:
    by_pickup_number_for_pickup_regions.setdefault(row.pickup_number, []).append(row)
    by_entrance_identifier_for_pickup_regions.setdefault(row.entrance_identifier, []).append(row)
    by_entrance_and_pickup[(row.entrance_identifier, row.pickup_number)] = row

entrance_to_pickup_region_info_collection = list(pickup_region_rows)


def lookup_pickup_region_requirement(entrance_identifier: str, pickup_number: int) -> EntranceToPickupRegionInfo:
    return by_entrance_and_pickup[(entrance_identifier, pickup_number)]


class EntranceToEnemyRegionInfo(BaseModel):
    """
    Requirements for reaching an enemy *instance* from a specific entrance.

    Mirrors :class:`EntranceToPickupRegionInfo`, but for enemy regions — used to put
    enemy-drop souls (e.g. Flame Demon, Succubus) into logic, since those souls are not
    ground pickups and never enter the item pool. Requirements are symmetric (they apply
    both to reaching the enemy and returning).

    ``enemy_number`` is globally unique (one per CSV instance). ``enemy_name`` +
    ``specifier`` is unique only *within a room* (e.g. "Succubus_a" exists in both room
    90D and 90E), so use ``enemy_number`` to identify a single instance.
    """

    class Config:
        extra = "allow"
        frozen = True

    enemy_number: int
    enemy_room: str
    enemy_name: str
    specifier: str
    entrance_identifier: str

    abilities: frozenset[str]
    combo_texts: tuple[str, ...] = ()

    @classmethod
    def from_row(
        cls,
        row: dict,
        ability_headers: Iterable[str],
        combo_headers: Iterable[str],
        entrance_identifier: str,
    ) -> "EntranceToEnemyRegionInfo":
        abilities, combo_texts = _extract_abilities_and_combo_texts(
            row, ability_headers, combo_headers
        )
        return cls(
            enemy_number=int(row["enemy_number"]),
            enemy_room=(row.get("room_id") or "").strip(),
            enemy_name=(row.get("Enemy Name") or "").strip(),
            specifier=(row.get("Specifier") or "").strip(),
            entrance_identifier=entrance_identifier,
            abilities=abilities,
            combo_texts=combo_texts,
        )

    @property
    def key(self) -> tuple[str, int]:
        return (self.entrance_identifier, self.enemy_number)

    @property
    def identifier_key(self) -> str:
        """Human-readable enemy id, e.g. "Succubus_a". NOT globally unique across rooms."""
        return f"{self.enemy_name}{self.specifier}"

    def get_requirement_bitmasks(
        self,
        *,
        include_combos: bool = True,
        minimize: bool = True,
        strict_combo_tokens: bool = True,
    ) -> tuple[int, ...]:
        return _requirement_bitmasks_from(
            self.abilities,
            self.combo_texts,
            include_combos=include_combos,
            minimize=minimize,
            strict_combo_tokens=strict_combo_tokens,
        )


def _load_enemy_region_requirements() -> tuple[EntranceToEnemyRegionInfo, ...]:
    skipped_unresolved = 0
    reader = open_csv(__name__, "symmetric_entrance_to_enemy_region_requirements.csv")
    ability_headers, combo_headers = _ability_and_combo_headers(reader.fieldnames or [])

    seen_keys: set[tuple[str, int]] = set()
    out: list[EntranceToEnemyRegionInfo] = []
    for row in reader:
        if not any((v or "").strip() for v in row.values()):
            continue

        room_id = (row.get("room_id") or "").strip()
        entrances = _entrance_identifiers_from_cell(room_id, row.get("dest_room_identifier"))
        if not entrances:
            # Unlike pickups (which raise), enemy rows are bulk data; a blank or
            # unresolved dest_room_identifier just means we can't place this instance
            # in the region graph, so skip it.
            skipped_unresolved += 1
            continue

        for entrance_identifier in sorted(entrances):
            key = (entrance_identifier, int(row["enemy_number"]))
            if key in seen_keys:
                continue
            seen_keys.add(key)
            out.append(
                EntranceToEnemyRegionInfo.from_row(
                    row, ability_headers, combo_headers, entrance_identifier
                )
            )

    if skipped_unresolved:
        logging.info(
            "cvaos: skipped %d enemy routing rows with unresolved dest_room_identifier",
            skipped_unresolved,
        )
    return tuple(out)


enemy_region_rows: tuple[EntranceToEnemyRegionInfo, ...] = _load_enemy_region_requirements()
entrance_to_enemy_region_info_collection = list(enemy_region_rows)

# enemy_number -> its per-entrance routing rows
by_enemy_number_for_enemy_regions: dict[int, list[EntranceToEnemyRegionInfo]] = {}
# enemy_name -> set of enemy_numbers of that type (drives "reach ANY instance")
by_enemy_name_for_enemy_regions: dict[str, set[int]] = {}
# enemy_number -> (enemy_name, specifier, room) for region naming / reverse lookup
enemy_meta_by_number: dict[int, tuple[str, str, str]] = {}
# (room, enemy_name, specifier) -> enemy_number (unique within a room)
_enemy_number_by_room_name_spec: dict[tuple[str, str, str], int] = {}

for _enemy_row in enemy_region_rows:
    by_enemy_number_for_enemy_regions.setdefault(_enemy_row.enemy_number, []).append(_enemy_row)
    by_enemy_name_for_enemy_regions.setdefault(_enemy_row.enemy_name, set()).add(_enemy_row.enemy_number)
    enemy_meta_by_number[_enemy_row.enemy_number] = (
        _enemy_row.enemy_name, _enemy_row.specifier, _enemy_row.enemy_room,
    )
    _enemy_number_by_room_name_spec[
        (_enemy_row.enemy_room, _enemy_row.enemy_name, _enemy_row.specifier)
    ] = _enemy_row.enemy_number


def resolve_enemy_number(room_id: str, enemy_name: str, specifier: str = "") -> int:
    """Map the human form ``(room, name, specifier)`` to the unique ``enemy_number``."""
    return _enemy_number_by_room_name_spec[(room_id, enemy_name, specifier)]
