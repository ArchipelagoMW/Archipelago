from __future__ import annotations

import csv
import re
from enum import IntFlag, auto
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel, ConfigDict

__all__ = [
    "AbilityCombo",
    "RoutingInfo",
    "entrance_to_entrance_info_collection"
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
