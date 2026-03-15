"""
Ys I Chronicles - Archipelago World

This module defines the Archipelago integration for Ys I Chronicles (PC).
"""

from typing import Dict, List, ClassVar, Any
from BaseClasses import Item, ItemClassification, Location, Region, Tutorial, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

def launch_client():
    """Launch the Ys Chronicles client."""
    from .client import launch
    launch_subprocess(launch, name="YsChroniclesClient")

components.append(Component(
    "Ys I Chronicles Client",
    func=launch_client,
    component_type=Type.CLIENT
))

from .items import (
    YS1_ITEMS,
    YS1_BASE_ID,
    YsItemType,
    item_name_to_id,
    get_item_classification,
    get_filler_items,
)
from .locations import (
    YS1_LOCATIONS,
    YS1_LOCATION_BASE_ID,
    YsLocationType,
    location_name_to_id,
)
from .regions import (
    YS1_REGIONS,
    YS1_CONNECTIONS,
    RULE_FUNCTIONS,
    LOCATION_RULES,
    BOSS_LOCATIONS,
    BOSS_ITEMS,
)
from .options import YsChroniclesOptions


class YsChroniclesItem(Item):
    """An item in Ys I Chronicles."""
    game = "Ys I Chronicles"


class YsChroniclesLocation(Location):
    """A location in Ys I Chronicles."""
    game = "Ys I Chronicles"


class YsChroniclesWebWorld(WebWorld):
    """Web integration for Ys Chronicles."""

    theme = "stone"

    game_info_languages = ["en"]

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Ys I Chronicles for Archipelago multiworld.",
            "English",
            "en_setup_Ys I Chronicles.md",
            "setup/en",
            ["mishy"]
        )
    ]


class YsChroniclesWorld(World):
    """
    Ys I Chronicles is an action RPG remake of the classic Ys games.
    Guide Adol Christin through the ancient land of Esteria to stop
    the forces of darkness and uncover the secrets of ancient Ys.
    """

    game = "Ys I Chronicles"
    web = YsChroniclesWebWorld()

    options_dataclass = YsChroniclesOptions
    options: YsChroniclesOptions

    item_name_to_id: ClassVar[Dict[str, int]] = item_name_to_id
    location_name_to_id: ClassVar[Dict[str, int]] = location_name_to_id

    # Slot data sent to the client
    slot_data: Dict[str, Any]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.slot_data = {}

    # -------------------------------------------------------------------------
    # Item Creation
    # -------------------------------------------------------------------------

    def create_item(self, name: str) -> YsChroniclesItem:
        """Create an item for this world."""
        item_data = YS1_ITEMS.get(name)
        if item_data:
            return YsChroniclesItem(
                name,
                item_data.classification,
                item_data.code,
                self.player
            )
        # Fallback for unknown items
        return YsChroniclesItem(
            name,
            ItemClassification.filler,
            None,
            self.player
        )

    def create_items(self) -> None:
        """Create all items for the item pool."""
        item_pool: List[YsChroniclesItem] = []

        # Track which items to include based on options
        excluded_items: set = set()

        boss_checks_enabled = bool(self.options.boss_checks)

        if not boss_checks_enabled:
            # Boss items stay vanilla — precollect them so logic rules auto-pass
            for item_name in BOSS_ITEMS:
                self.multiworld.push_precollected(self.create_item(item_name))
                excluded_items.add(item_name)
        # When boss checks ARE enabled, boss items go into the pool normally

        # Handle starting weapon
        if self.options.starting_weapon == 1:  # Short Sword
            self.multiworld.push_precollected(self.create_item("Short Sword"))
            excluded_items.add("Short Sword")
        elif self.options.starting_weapon == 2:  # Long Sword
            self.multiworld.push_precollected(self.create_item("Long Sword"))
            excluded_items.add("Long Sword")

        # Create items based on shuffle options
        for item_name, item_data in YS1_ITEMS.items():
            if item_name in excluded_items:
                continue

            # Check shuffle options
            if item_data.item_type in (YsItemType.WEAPON, YsItemType.ARMOR, YsItemType.SHIELD):
                if not self.options.shuffle_equipment:
                    continue
            elif item_data.item_type == YsItemType.RING:
                if not self.options.shuffle_rings:
                    continue
            elif item_data.item_type == YsItemType.KEY:
                if not self.options.shuffle_keys:
                    continue
            elif item_data.item_type in (YsItemType.QUEST, YsItemType.BOOK):
                if not self.options.shuffle_quest_items:
                    continue
            elif item_data.item_type == YsItemType.CONSUMABLE:
                if not self.options.shuffle_consumables:
                    continue

            item_pool.append(self.create_item(item_name))

        # Fill remaining locations with filler
        filler_items = get_filler_items()
        locations_count = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < locations_count:
            import random
            filler_name = random.choice(filler_items)
            item_pool.append(self.create_item(filler_name))

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        """Return filler item name for junk locations."""
        return "Heal Potion"

    # -------------------------------------------------------------------------
    # Region & Location Creation
    # -------------------------------------------------------------------------

    def create_regions(self) -> None:
        """Create all regions and locations."""
        boss_checks_enabled = bool(self.options.boss_checks)

        # Create all regions
        regions: Dict[str, Region] = {}
        for region_name in YS1_REGIONS:
            region = Region(region_name, self.player, self.multiworld)
            regions[region_name] = region
            self.multiworld.regions.append(region)

        shop_checks_enabled = bool(self.options.shuffle_shops)

        # Create locations and add to regions
        for loc_name, loc_data in YS1_LOCATIONS.items():
            # Skip boss locations if boss checks are disabled
            if loc_data.loc_type == YsLocationType.BOSS and not boss_checks_enabled:
                continue
            # Skip shop locations if shop checks are disabled
            if loc_data.loc_type == YsLocationType.SHOP and not shop_checks_enabled:
                continue

            region = regions.get(loc_data.region)
            if region:
                location = YsChroniclesLocation(
                    self.player,
                    loc_name,
                    loc_data.code,
                    region
                )
                region.locations.append(location)

        # Create region connections
        for from_region, to_region, rule_name in YS1_CONNECTIONS:
            if from_region in regions and to_region in regions:
                if rule_name and rule_name in RULE_FUNCTIONS:
                    rule_func = RULE_FUNCTIONS[rule_name]
                    regions[from_region].connect(
                        regions[to_region],
                        rule=lambda state, rf=rule_func: rf(state, self.player)
                    )
                else:
                    regions[from_region].connect(regions[to_region])

    def set_rules(self) -> None:
        """Set access rules for locations."""
        boss_checks_enabled = bool(self.options.boss_checks)

        # Apply location-specific rules
        for loc_name, rule_name in LOCATION_RULES.items():
            # Skip boss location rules if boss checks disabled
            if loc_name in BOSS_LOCATIONS and not boss_checks_enabled:
                continue

            location = self.multiworld.get_location(loc_name, self.player)
            if location and rule_name in RULE_FUNCTIONS:
                rule_func = RULE_FUNCTIONS[rule_name]
                location.access_rule = lambda state, rf=rule_func: rf(state, self.player)

        # Prevent self-locking placements
        shield_ring_loc = self.multiworld.get_location("Shrine F1 - Shield Ring Chest", self.player)
        if shield_ring_loc:
            shield_ring_loc.item_rule = lambda item: item.name != "Treasure Box Key"

        locked_chest_loc = self.multiworld.get_location("Minea Fields - Locked Chest", self.player)
        if locked_chest_loc:
            locked_chest_loc.item_rule = lambda item: item.name != "Treasure Box Key"

        silver_bell_loc = self.multiworld.get_location("Silver Bell Reward", self.player)
        if silver_bell_loc:
            silver_bell_loc.item_rule = lambda item: item.name != "Silver Bell"

        # Set completion condition based on goal
        # Dark Fact is a location in Tower Upper gated by Blue Amulet
        if self.options.goal == 0:  # Dark Fact
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.can_reach_location("Boss: Dark Fact", self.player)
        elif self.options.goal == 1:  # All Books
            from .regions import has_all_books
            self.multiworld.completion_condition[self.player] = \
                lambda state: (
                    has_all_books(state, self.player) and
                    state.can_reach_location("Boss: Dark Fact", self.player)
                )
        elif self.options.goal == 2:  # All Bosses
            self.multiworld.completion_condition[self.player] = \
                lambda state: (
                    state.can_reach_location("Boss: Dark Fact", self.player) and
                    state.can_reach_region("Shrine B3", self.player) and
                    state.can_reach_region("Mine B2", self.player) and
                    state.can_reach_region("Tower F8", self.player) and
                    state.can_reach_region("Tower F14", self.player)
                )

    # -------------------------------------------------------------------------
    # Generation
    # -------------------------------------------------------------------------

    def generate_early(self) -> None:
        """Called before item/location creation."""
        pass

    def generate_basic(self) -> None:
        """Called after item/location creation."""
        pass

    def pre_fill(self) -> None:
        """Called before filling locations with items."""
        pass

    # Items used for tower-internal progression
    TOWER_INTERNAL_ITEMS = {
        "Hammer", "Rod", "Blue Amulet", "Blue Necklace", "Monocle",
        "Idol", "Mask of Eyes",
    }
    TOWER_REGIONS = {
        "Tower Lower", "Tower F8", "Tower Mid", "Tower F14", "Tower Upper",
    }

    def fill_slot_data(self) -> Dict[str, Any]:
        """Data sent to the client."""
        # Find tower-internal items placed in overworld locations.
        # The client uses this to auto-warp the player back if they
        # enter the tower without collecting these.
        tower_items_in_overworld = []
        for loc_name, loc_data in YS1_LOCATIONS.items():
            if loc_data.region in self.TOWER_REGIONS:
                continue
            location = self.multiworld.get_location(loc_name, self.player)
            if (location and location.item and
                    location.item.player == self.player and
                    location.item.name in self.TOWER_INTERNAL_ITEMS):
                game_id = YS1_ITEMS[location.item.name].game_id
                tower_items_in_overworld.append(game_id)

        return {
            "goal": self.options.goal.value,
            "boss_checks": bool(self.options.boss_checks),
            "death_link": self.options.death_link.value,
            "experience_multiplier": self.options.experience_multiplier.value,
            "gold_multiplier": self.options.gold_multiplier.value,
            "tower_items_in_overworld": tower_items_in_overworld,
        }

    # -------------------------------------------------------------------------
    # Output
    # -------------------------------------------------------------------------

    def generate_output(self, output_directory: str) -> None:
        """Generate output files (e.g., patch files)."""
        pass
