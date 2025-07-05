"""
This module contains the classes and logic for the craft randomization.
"""
from enum import Enum
from typing import Optional, List

import attrs

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

@attrs.define
class Craft:
    """Represents a craft that can be randomized."""
    base_craft_name: str
    base_craft_id: int
    base_craft_level_acquired: int
    category: CraftCategory
    animation_size_bytes: int

    upgraded_craft_name: Optional[str] = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            attrs.validators.instance_of(str)
        )
    )
    upgraded_craft_id: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            attrs.validators.instance_of(int)
        )
    )
    upgraded_craft_level_acquired: Optional[int] = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            attrs.validators.instance_of(int)
        )
    )

    def _validate_upgraded_field(self, field_name: str, value):
        """
        Shared validator for upgraded fields.
        If the craft is upgradable, the field must be populated.
        If the craft is not upgradable, the field must not be populated.
        """
        is_upgradable = self.category in [CraftCategory.UPGRADABLE_NORMAL_CRAFT, CraftCategory.UPGRADABLE_SCRAFT]

        if is_upgradable and value is None:
            raise ValueError(f"{field_name} must be populated for upgradable category {self.category}")
        elif not is_upgradable and value is not None:
            raise ValueError(f"{field_name} must not be populated for non-upgradable category {self.category}")

    @upgraded_craft_name.validator
    def validate_upgraded_craft_name(self, _, value):
        """Validate that upgraded_craft_name is populated for upgradable crafts and not populated for non-upgradable crafts."""
        self._validate_upgraded_field("upgraded_craft_name", value)

    @upgraded_craft_id.validator
    def validate_upgraded_craft_id(self, _, value):
        """Validate that upgraded_craft_id is populated for upgradable crafts and not populated for non-upgradable crafts."""
        self._validate_upgraded_field("upgraded_craft_id", value)

    @upgraded_craft_level_acquired.validator
    def validate_upgraded_craft_level_acquired(self, _, value):
        """Validate that upgraded_craft_level_acquired is populated for upgradable crafts and not populated for non-upgradable crafts."""
        self._validate_upgraded_field("upgraded_craft_level_acquired", value)

@attrs.define
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
