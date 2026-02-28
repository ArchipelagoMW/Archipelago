"""
Mystical Ninja Starring Goemon (MN64) for Archipelago Multi-World Randomizer
"""

import logging
from typing import Any, Dict

from BaseClasses import Entrance, Item, ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from .Enemies import get_enemy_pool, randomize_all_enemies
from .Hints import CompileMNSGHints
from .Items import MN64Item, all_item_table, get_event_item_names, get_item_name_to_id, get_vanilla_item_names, populate_item_metadata
from .Locations import get_location_name_to_id
from .Logic.mn64_logic_classes import MN64Items
from .Options import MN64Options
from .Regions import (
    connect_regions,
    create_game_regions,
    import_region_logic,
    setup_starting_region,
    update_location_metadata,
)
from .Rules import set_rules

logger = logging.getLogger("Mystical Ninja 64")


class MN64Location(Location):
    """Location class for MN64."""

    game: str = "Mystical Ninja Starring Goemon"


class MN64Web(WebWorld):
    """Web world configuration for MN64."""

    theme = "partyTime"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Mystical Ninja Starring Goemon for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Killklli", "littlecube_hax", "klorfmorf", "abyssonym", "Umed"],
        )
    ]


class MN64World(World):
    """
    Mystical Ninja Starring Goemon is a 3D action-adventure game for the Nintendo 64.
    Play as Goemon and his friends as they travel across Japan to stop the evil Mangamore Corps
    from turning Japan into a giant stage. Explore towns, dungeons, and pilot giant robots!
    """

    game = "Mystical Ninja Starring Goemon"
    is_experimental = True
    web = MN64Web()
    options_dataclass = MN64Options
    options: MN64Options
    topology_present = False

    data_version = 1

    # Item and location mappings
    item_name_to_id = get_item_name_to_id()
    location_name_to_id = get_location_name_to_id()

    # Required client version
    required_client_version = (0, 5, 0)

    # Store location metadata for client
    location_metadata: Dict[str, Dict[str, Any]]
    item_metadata: Dict[str, Dict[str, Any]]

    def generate_early(self) -> None:
        """Read re_gen_passthrough data from Universal Tracker if present."""
        self.using_ut = False
        self.passthrough = {}
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Mystical Ninja Starring Goemon" in self.multiworld.re_gen_passthrough:
                self.using_ut = True
                self.passthrough = self.multiworld.re_gen_passthrough["Mystical Ninja Starring Goemon"]

    def create_regions(self) -> None:
        """Create all regions for MN64."""
        # Create menu region
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Import region logic and create all game regions
        self.all_regions = import_region_logic()

        # Initialize metadata storage
        self.location_metadata = {}
        self.item_metadata = {}
        populate_item_metadata(self)

        # Initialize hint storage for dynamic hints
        self.dynamic_hints = {}

        # Create all game regions and their locations
        create_game_regions(self, self.all_regions, self.location_name_to_id)

        # Connect regions with entrances
        connect_regions(self, self.all_regions, logger)

        # Setup starting region connection from menu
        setup_starting_region(self, self.all_regions, logger)

    def create_items(self) -> None:
        """Create all items for the multiworld."""
        pool = []

        # Get items that are placed at vanilla locations (not randomized)
        vanilla_item_names = get_vanilla_item_names(self.options.randomize_health.value, self.options.randomize_ryo.value, self.options.pot_rando.value)

        # Characters that can start the game
        character_names = ["Goemon", "Ebisumaru", "Yae", "Sasuke"]

        # Restore starting character from passthrough during UT regen, otherwise pick randomly
        if self.using_ut and self.passthrough.get("starting_characters"):
            starting_character = next(
                (name for name in character_names if self.passthrough["starting_characters"].get(name.lower(), False)),
                self.random.choice(character_names),
            )
        else:
            starting_character = self.random.choice(character_names)

        # Build list of available filler items for dynamic filling
        filler_items = []
        for item_name, item_data in all_item_table.items():
            if item_data.classification == ItemClassification.filler and item_data.id is not None:
                # Skip vanilla items
                if item_name not in vanilla_item_names:
                    filler_items.append(item_name)

        # Create progression/useful items based on Items.py definitions
        for item_name, item_data in all_item_table.items():
            # Skip event items - they don't go in the item pool
            if item_data.id is None:
                continue

            # Skip vanilla items - they are placed at vanilla locations during region creation
            if item_name in vanilla_item_names:
                continue

            # Skip the starting character - they'll be added to the precollected pool
            if item_name == starting_character:
                continue

            # Triton Horn is forced start currently
            if item_name == MN64Items.TRITON_HORN.value:
                continue

            # Skip filler items - we'll add them dynamically later
            if item_data.classification == ItemClassification.filler:
                continue

            # Create qty number of this item
            for _ in range(item_data.qty):
                pool.append(self.create_item(item_name))

        # Calculate how many locations are available for items
        # Count non-event, non-vanilla locations
        event_item_names = get_event_item_names()
        location_count = sum(1 for region in self.all_regions.values() for loc in region.locations if loc.item_type.value not in event_item_names and loc.item_type.value not in vanilla_item_names)

        # Fill remaining slots with filler items
        filler_needed = location_count - len(pool)
        for _ in range(filler_needed):
            filler_item = self.random.choice(filler_items)
            pool.append(self.create_item(filler_item))

        # Add items to the multiworld
        self.multiworld.itempool += pool

        # Add the starting character to precollected items
        self.multiworld.push_precollected(self.create_item(starting_character))
        self.multiworld.push_precollected(self.create_item(MN64Items.TRITON_HORN.value))

    def create_item(self, name: str) -> Item:
        """Create an item by name."""
        item_data = all_item_table.get(name)
        if item_data is None:
            raise ValueError(f"Item {name} is not a valid MN64 item")

        return MN64Item(name, item_data.classification, item_data.id, self.player)

    def set_rules(self) -> None:
        """Set access rules for regions and locations."""
        set_rules(self)

        # Set completion condition - player must defeat all bosses
        self.multiworld.completion_condition[self.player] = lambda state: (
            # state.has("Beat Congo", self.player) and
            # state.has("Beat Dharumanyo", self.player) and
            # state.has("Beat Tsurami", self.player) and
            # state.has("Beat Thaisambda", self.player) and
            state.has("Beat Game Die Hard Fans", self.player)
        )

    def post_fill(self):
        """Post-fill operations: update location metadata, randomize enemies, and manage memory."""
        # Update location metadata with the actual items placed at each location
        update_location_metadata(self)

        # Get enemy configuration
        all_enemies = get_enemy_pool(self.options.enemy_rando.value)
        RESTRICTED_ENEMIES = {0x106, 0x10C, 0x133, 0x13A, 0x13C, 0x13D, 0x13E, 0x144}
        RESTRICTED_ENEMY_ROOMS = {0, 0x87}

        # Initialize enemy data storage for slot data
        self.randomized_enemy_data = {}

        # Randomize enemies in each room with memory constraints
        randomize_all_enemies(self, self.all_regions, all_enemies, RESTRICTED_ENEMIES, RESTRICTED_ENEMY_ROOMS)

        # Update room default definitions for rooms without enemies
        from .file_memory_sizes import update_room_default_definitions_post_fill

        self.room_file_data = update_room_default_definitions_post_fill(
            self.all_regions,
            self.multiworld.get_locations(self.player),
            self.randomized_enemy_data,
            all_item_table,
            all_enemies,
            RESTRICTED_ENEMIES,
            RESTRICTED_ENEMY_ROOMS,
            self.random,
        )

        # Generate hints after all items have been placed
        # Only generate if hint counts are greater than 0
        if self.options.major_hint_count.value > 0 or self.options.location_hint_count.value > 0:
            CompileMNSGHints(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        """Fill slot data to be sent to the client."""
        # Convert enemy data integer keys to strings for JSON serialization consistency
        enemy_data_with_string_keys = {}
        for room_id, room_enemies in getattr(self, "randomized_enemy_data", {}).items():
            room_key = str(room_id)
            enemy_data_with_string_keys[room_key] = {}
            for instance_id, enemy_id in room_enemies.items():
                instance_key = str(instance_id)
                enemy_data_with_string_keys[room_key][instance_key] = enemy_id
        # print(self.room_file_data)
        # import time
        # time.sleep(10)
        # Determine starting characters
        character_names = ["Goemon", "Yae", "Ebisumaru", "Sasuke"]
        starting_characters = {}

        # Check which characters are precollected (starting inventory)
        precollected_character_names = {item.name for item in self.multiworld.precollected_items[self.player] if item.name in character_names}
        # print("Precollected characters:", precollected_character_names) case sensitivity

        # Mark each character as available or not at start
        for character in character_names:
            starting_characters[character.lower()] = character in precollected_character_names

        # Collect all starting/precollected items
        starting_items = []
        for item in self.multiworld.precollected_items[self.player]:
            item_info = {"name": item.name, "ap_id": item.code if hasattr(item, "code") else None}
            # Add additional metadata if available in item_metadata
            if hasattr(item, "code") and item.code and item.code in self.item_metadata:
                item_meta = self.item_metadata[item.code]
                if "save_id" in item_meta:
                    item_info["save_id"] = item_meta["save_id"]
                if "entity_id" in item_meta:
                    item_info["entity_id"] = item_meta["entity_id"]
                if "qty" in item_meta:
                    item_info["qty"] = item_meta["qty"]
            starting_items.append(item_info)

        room_data = getattr(self, "room_file_data", {})
        # Recreate it so its just a dict of the id and then the list of files
        room_data_simple = {room_id: data["files"] for room_id, data in room_data.items() if room_id is not None}

        # Create flag_id to ap_location_id mapping
        flag_id_to_ap_location_id = {}
        for room_id, location_list in self.location_metadata.items():
            for location_data in location_list:
                if "flag_id" in location_data and "ap_location_id" in location_data:
                    flag_id = location_data["flag_id"]
                    ap_location_id = location_data["ap_location_id"]
                    # Convert flag_id hex to decimal string
                    flag_id_str = str(flag_id)
                    flag_id_to_ap_location_id[flag_id_str] = ap_location_id

        # Get dynamic hints if they were generated
        dynamic_hints = getattr(self, "dynamic_hints", {})
        major_hints = [hint_data["text"] for hint_data in dynamic_hints.values() if hint_data["type"] == "major"]
        location_hints = [hint_data["text"] for hint_data in dynamic_hints.values() if hint_data["type"] == "location"]
        slot_data = {
            "seed": self.multiworld.seed,
            "location_metadata": self.location_metadata,
            "item_metadata": self.item_metadata,
            "enemy_data": getattr(self, "randomized_enemy_data", {}),
            "room_file_data": room_data_simple,
            "starting_room": getattr(self, "starting_room_id", None),
            "starting_region_name": getattr(self, "starting_region_name", "GoemonsHouse"),
            "starting_spawn_data": getattr(self, "starting_spawn_data", {}),
            "starting_characters": starting_characters,
            "starting_items": starting_items,
            "flag_id_to_ap_location_id": flag_id_to_ap_location_id,
            "major_hints": major_hints,
            "location_hints": location_hints,
            "enemy_rando": self.options.enemy_rando.value,
            "increase_pot_ryo": self.options.increase_pot_ryo.value,
            "pot_rando": self.options.pot_rando.value,
            "randomize_health": self.options.randomize_health.value,
            "randomize_ryo": self.options.randomize_ryo.value,
            "prevent_oneway_softlocks": self.options.prevent_oneway_softlocks.value,
            "chugoku_door_unlocked": self.options.chugoku_door_unlocked.value,
            "pre_unlocked_warps": self.options.pre_unlocked_warps.value,
            "music_rando": self.options.music_rando.value,
            "fast_text": self.options.fast_text.value,
            "keep_intro_cutscene": self.options.keep_intro_cutscene.value,
            "death_link": self.options.death_link.value,
        }

        return slot_data

    def write_spoiler(self, spoiler_handle):
        """Write spoiler information to the spoiler log."""
        spoiler_handle.write("\n")
        spoiler_handle.write(f"Mystical Ninja Starring Goemon Settings for {self.player_name}:\n")
        spoiler_handle.write("\n")

        # Write option settings
        spoiler_handle.write(f"Enemy Randomization: {'Enabled' if self.options.enemy_rando.value else 'Disabled'}\n")
        spoiler_handle.write(f"Starting Room Randomization: {'Enabled' if self.options.starting_room_rando.value else 'Disabled'}\n")
        spoiler_handle.write(f"Increased Pot Ryo: {'Enabled' if self.options.increase_pot_ryo.value else 'Disabled'}\n")
        spoiler_handle.write(f"Pot Randomization: {'Enabled' if self.options.pot_rando.value else 'Disabled'}\n")
        spoiler_handle.write(f"Health in Pool: {'Enabled' if self.options.randomize_health.value else 'Disabled'}\n")
        spoiler_handle.write(f"Ryo in Pool: {'Enabled' if self.options.randomize_ryo.value else 'Disabled'}\n")
        spoiler_handle.write(f"Prevent One-Way Softlocks: {'Enabled' if self.options.prevent_oneway_softlocks.value else 'Disabled'}\n")
        spoiler_handle.write(f"Chugoku Door Unlocked: {'Enabled' if self.options.chugoku_door_unlocked.value else 'Disabled'}\n")
        spoiler_handle.write(f"Pre-Unlocked Warps: {'Enabled' if self.options.pre_unlocked_warps.value else 'Disabled'}\n")
        spoiler_handle.write(f"Death Link: {'Enabled' if self.options.death_link.value else 'Disabled'}\n")

        # Write hint settings and hints
        if self.options.major_hint_count.value > 0 or self.options.location_hint_count.value > 0:
            spoiler_handle.write("\n")
            spoiler_handle.write("=== Hints ===\n")
            spoiler_handle.write(f"Major Item Hints: {self.options.major_hint_count.value}\n")
            spoiler_handle.write(f"Location Hints: {self.options.location_hint_count.value}\n")
            spoiler_handle.write("\n")

            dynamic_hints = getattr(self, "dynamic_hints", {})
            if dynamic_hints:
                # Sort hints by type and then by location name
                major_hints = []
                location_hints = []

                for location_id, hint_data in dynamic_hints.items():
                    if hint_data["type"] == "major":
                        major_hints.append(hint_data)
                    else:
                        location_hints.append(hint_data)

                # Sort by location name
                major_hints.sort(key=lambda h: h["location_name"])
                location_hints.sort(key=lambda h: h["location_name"])

                if major_hints:
                    spoiler_handle.write("Major Item Hints:\n")
                    for hint in major_hints:
                        spoiler_handle.write(f"  {hint['text']}\n")
                    spoiler_handle.write("\n")

                if location_hints:
                    spoiler_handle.write("Location Hints:\n")
                    for hint in location_hints:
                        spoiler_handle.write(f"  {hint['text']}\n")
                    spoiler_handle.write("\n")

        spoiler_handle.write("\n")

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data
