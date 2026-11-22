from __future__ import annotations
import json
from importlib import resources
from typing import TYPE_CHECKING, Dict, List, Optional
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification

from .challenges import UNLOCK_ITEMS

FILLER_ITEM_NAME = "Madstone"

class DOTA2Item(Item):
    game = "DOTA 2"

    @property
    def excludable(self) -> bool:  # type: ignore[override]
        # Treat madstones as excludable items
        if self.name == FILLER_ITEM_NAME:
            return True
        return super().excludable
    
@dataclass(frozen=True)
class ItemDef:
    name: str
    classification: ItemClassification
    copies: int
    include_in_filler: bool

def _parse_classification(value: str) -> ItemClassification:
    v = (value or "").strip().lower()
    match v:
        case "progression":
            return ItemClassification.progression
        case "useful":
            return ItemClassification.useful
        case "trap":
            return ItemClassification.trap
        case "filler":
            return ItemClassification.filler
        case _:
            # Default to filler if unknown, but better to be strict for dev:
            raise ValueError(f"Unknown item classification '{value}'")

def load_hero_unlock_items(self:DOTA2World) -> List[ItemDef]:
    # Works in source and in zipped apworld due to importlib.resources.
    items: List[ItemDef] = []

    name = "Progressive Group Unlock"
    classification = _parse_classification("progression")
    copies = len(self.hero_groups)
    include_in_filler = False
    items.append(ItemDef(name=name, classification=classification, copies=copies, include_in_filler=include_in_filler))

    items.append(ItemDef(
        name="Primordial Fragment",
        classification=_parse_classification("progression"),
        copies=self.options.primordial_fragments_to_win.value + 10,
        include_in_filler=False
    ))

    return items

def load_shop_unlock_items() -> List[ItemDef]:
    # Works in source and in zipped apworld due to importlib.resources.
    items: List[ItemDef] = []

    with resources.files(__package__).joinpath("data/unlockDotaShopItems.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
        
        for item in data['unlock_shop_items']:
            name = item['name']
            classification = _parse_classification("progression")
            copies = 1
            include_in_filler = False
            items.append(ItemDef(name=name, classification=classification, copies=copies, include_in_filler=include_in_filler))

    return items

def load_minigame_unlock_items() -> List[ItemDef]:
    # Works in source and in zipped apworld due to importlib.resources.
    items: List[ItemDef] = []

    with resources.files(__package__).joinpath("data/minigameItems.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
        
        for item in data['minigame_items']:
            name = item['name']
            classification = _parse_classification("progression")
            copies = 1
            include_in_filler = False
            items.append(ItemDef(name=name, classification=classification, copies=copies, include_in_filler=include_in_filler))

    return items

# Internal filler item used to pad itempool to location count when needed.
FILLER_ITEM_NAME = "Madstone"

def build_item_name_to_id(base_id: int, item_defs: list[ItemDef]) -> dict[str, int]:
    names = [d.name for d in item_defs]

    if FILLER_ITEM_NAME not in names:
        names.append(FILLER_ITEM_NAME)


    return {name: i for i, name in enumerate(names, base_id)}

def load_item_defs() -> list[ItemDef]:
    items: List[ItemDef] = []
    items.append(ItemDef(
            name="Progressive Group Unlock",
            classification=ItemClassification.progression,
            copies=0,
            include_in_filler=False))
    items.append(ItemDef(
            name="Primordial Fragment",
            classification=ItemClassification.progression,
            copies=0,
            include_in_filler=False,
        ))
    items.append(ItemDef(
            name=FILLER_ITEM_NAME,
            classification=ItemClassification.filler,
            copies=0,
            include_in_filler=True,
        ))
    items.extend(load_shop_unlock_items())
    items.extend(load_minigame_unlock_items())
    # Stat, quest and challenge unlocks go last, so the ids of older items don't move
    items.extend(ItemDef(name=name, classification=ItemClassification.progression, copies=0, include_in_filler=False)
                 for name in UNLOCK_ITEMS)

    return items
