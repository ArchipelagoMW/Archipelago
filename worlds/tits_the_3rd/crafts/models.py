"""
This module contains the classes and logic for the craft randomization.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class CraftCategory(Enum):
    """
    For randomization, only crafts within the same category can be randomized with each other.
    Potentially, we could change this in the future as an option.

    Upgradable: Crafts have 2 levels of progression (e.g. Dragon Dive vs Dragon Dive 2).
    Normal craft: non scraft and non chain craft.
    """
    FIXED_NORMAL_CRAFT = 1
    UPGRADABLE_NORMAL_CRAFT = 2
    FIXED_SCRAFT = 3
    UPGRADABLE_SCRAFT = 4
    CHAIN_CRAFT = 5


@dataclass
class Craft:
    """Represents a craft that can be randomized."""
    base_craft_name: str
    base_craft_id: int
    base_craft_level_acquired: int
    category: CraftCategory
    animation_size_bytes: int
    base_as_function_name: Optional[str] = None
    upgraded_craft_name: Optional[str] = None
    upgraded_craft_id: Optional[int] = None
    upgraded_craft_level_acquired: Optional[int] = None

    def __post_init__(self):
        if not self.base_as_function_name and self.category != CraftCategory.CHAIN_CRAFT:
            raise ValueError("base_as_function_name must be populated for non chain craft.")
        is_upgradable = self.category in [CraftCategory.UPGRADABLE_NORMAL_CRAFT, CraftCategory.UPGRADABLE_SCRAFT]
        if is_upgradable:
            if not (self.upgraded_craft_name and self.upgraded_craft_id and self.upgraded_craft_level_acquired):
                raise ValueError("All upgradable categories must be populated for upgradable craft")
        else:
            if self.upgraded_craft_name or self.upgraded_craft_id or self.upgraded_craft_level_acquired:
                raise ValueError("All upgradable categories must not be populated for non upgradable craft")


@dataclass
class Character:
    """Represents a character who can have their crafts randomized."""
    name: str
    char_id: int
    animation_buffer_size_bytes: int # Max size of animations we can put on this character (combined)
    fixed_normal_crafts: List[Craft]
    upgradable_normal_crafts: List[Craft]
    fixed_scrafts: List[Craft]
    upgradable_scrafts: List[Craft]
    chain_crafts: List[Craft]

    def get_craft_list_by_category(self, category: CraftCategory) -> List[Craft]:
        """Returns all the crafts for this character in the given category."""
        if category == CraftCategory.FIXED_NORMAL_CRAFT:
            return self.fixed_normal_crafts
        elif category == CraftCategory.UPGRADABLE_NORMAL_CRAFT:
            return self.upgradable_normal_crafts
        elif category == CraftCategory.FIXED_SCRAFT:
            return self.fixed_scrafts
        elif category == CraftCategory.UPGRADABLE_SCRAFT:
            return self.upgradable_scrafts
        elif category == CraftCategory.CHAIN_CRAFT:
            return self.chain_crafts
        else:
            raise ValueError(f"Invalid category: {category}")

    @property
    def crafts(self) -> List[Craft]:
        """Returns all the crafts for this character."""
        return self.fixed_normal_crafts + self.upgradable_normal_crafts + self.fixed_scrafts + self.upgradable_scrafts + self.chain_crafts

    @property
    def swappable_crafts(self) -> List[Craft]:
        """Returns all the crafts that can be swapped with other characters."""
        return self.fixed_normal_crafts + self.upgradable_normal_crafts + self.fixed_scrafts + self.upgradable_scrafts

    @property
    def total_animation_size_bytes(self) -> int:
        """Returns the total size in bytes of all the craft animations."""
        size = sum(craft.animation_size_bytes for craft in self.crafts)
        return size

    @property
    def remaining_buffer_size_bytes(self) -> int:
        """Returns the remaining animation buffer size in bytes. This can return negative if the animation is too big."""
        return self.animation_buffer_size_bytes - self.total_animation_size_bytes
