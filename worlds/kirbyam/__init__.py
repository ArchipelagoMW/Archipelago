"""
Archipelago World definition for Kirby & The Amazing Mirror
"""
import base64
import os
import pkgutil
import time
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List

import settings
from BaseClasses import ItemClassification, LocationProgressType, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

from .client import KirbyAmClient  # type: ignore  # Required to register BizHawk client
from .data import LocationCategory
from .data import data as kirby_data
from .generation_logging import (
    generation_stage,
    log_generation_complete,
    log_generation_error,
    log_generation_start,
    log_items_created,
    log_regions_created,
    logger,
)
from .groups import ITEM_GROUPS, LOCATION_GROUPS
from .items import KirbyAmItem, create_item_label_to_code_map, get_item_classification
from .locations import KirbyAmLocation, create_location_label_to_id_map
from .options import OPTION_GROUPS, Goal, KirbyAmOptions, RandomizeShards
from .rom import KirbyAmProcedurePatch, write_tokens

if TYPE_CHECKING:
    from BaseClasses import CollectionState


class KirbyAmWebWorld(WebWorld):
    """
    Webhost info for Kirby & The Amazing Mirror
    """
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Kirby & The Amazing Mirror with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Harrison Sherwin"],
    )

    tutorials = [setup_en]
    option_groups = OPTION_GROUPS


class KirbyAmSettings(settings.Group):
    class KirbyAmRomFile(settings.UserFilePath):
        """File name of your USA Kirby & The Amazing Mirror ROM"""
        description = "Kirby & The Amazing Mirror ROM File"
        copy_to = "Kirby & The Amazing Mirror (USA).gba"

        # Validate the ROM hash
        hash_obj = KirbyAmProcedurePatch.hash
        if hash_obj is None:
            raise RuntimeError("KirbyAmProcedurePatch.hash is missing")
        md5s = [hash_obj]

    rom_file: KirbyAmRomFile = KirbyAmRomFile(KirbyAmRomFile.copy_to)


class KirbyAmWorld(World):
    """
    Kirby & The Amazing Mirror is a classic Kirby adventure that emphasizes exploration and nonlinear progression.
    Guide Kirby through a vast, interconnected world within the Mirror Land,
    copy enemy abilities, uncover hidden paths, defeat powerful bosses,
    and restore peace by reuniting the shattered Dimension Mirror.
    """
    game = "Kirby & The Amazing Mirror"
    web = KirbyAmWebWorld()
    topology_present = True

    # IMPORTANT: must match the name your settings system expects for this world.
    settings_key = "kirby_am_settings"
    settings: ClassVar[KirbyAmSettings]

    options_dataclass = KirbyAmOptions
    options: KirbyAmOptions

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()

    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    required_client_version = (0, 4, 6)

    # Per-seed auth token used by BizHawk client connection
    auth: bytes

    # Track generation timing
    _generation_start_time: float

    # Generation stages
    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # If you don't have sanity_check.py yet, comment these out for now.
        from .sanity_check import validate_group_maps, validate_regions
        assert validate_regions()
        assert validate_group_maps()

    # Filler item name
    def get_filler_item_name(self) -> str:
        # Keep simple until you define your filler set.
        return "1 Up"

    # Pre-generation adjustments
    def generate_early(self) -> None:
        # Track generation start
        self._generation_start_time = time.time()
        log_generation_start(self.player, self.player_name, self.options.as_dict("goal", "shards"))

        with generation_stage("generate_early", self.player, self.player_name):
            # If shards are shuffled as items, they must be local to the ROM unless you implement remote shard handling.
            if self.options.shards.value == RandomizeShards.option_shuffle:
                self.logger.debug("Shards are shuffled; marking them as local items.")
                self.options.local_items.value.update(self.item_name_groups.get("Shard", set()))
                logger.info(f"[P{self.player}] Shards marked as local items (shuffle mode)")
            else:
                logger.info(f"[P{self.player}] Shards mode: {self.options.shards.current_key}")

    # Create world regions
    def create_regions(self) -> None:
        with generation_stage("create_regions", self.player, self.player_name):
            from .regions import create_regions as create_regions_impl

            regions_by_name = create_regions_impl(self)

            # Most create_regions implementations already append to multiworld.regions.
            # To avoid double-adding, only add missing ones here.
            existing = {(r.name, r.player) for r in self.multiworld.regions}
            for r in regions_by_name.values():
                if (r.name, r.player) not in existing:
                    self.multiworld.regions.append(r)

            # Log region creation
            fillable_locations = len([
                loc for loc in self.multiworld.get_locations(self.player)
                if isinstance(loc, KirbyAmLocation) and loc.address is not None
            ])
            log_regions_created(self.player, len(regions_by_name), fillable_locations)

    def create_items(self) -> None:
        with generation_stage("create_items", self.player, self.player_name):
            # Create items for all fillable locations (address != None).
            fill_locations: list[KirbyAmLocation] = [
                loc for loc in self.multiworld.get_locations(self.player)
                if isinstance(loc, KirbyAmLocation) and loc.address is not None
            ]

            # Filter categories that should not be randomized into the pool.
            filtered_categories = set()
            if self.options.shards.value in {RandomizeShards.option_vanilla, RandomizeShards.option_shuffle}:
                filtered_categories.add(LocationCategory.SHARD)

            # Build the default item pool from each location's default item.
            itempool: list[KirbyAmItem] = []
            shard_count = 0
            for loc in fill_locations:
                if loc.key is None:
                    continue
                loc_meta = kirby_data.locations.get(loc.key)
                if loc_meta is None:
                    continue

                if loc_meta.category in filtered_categories:
                    if loc_meta.category == LocationCategory.SHARD:
                        shard_count += 1
                    continue

                # During early iteration it's easy to have a location without a default_item.
                # Avoid hard crashes and fall back to the world's configured filler.
                if loc.default_item_code is None:
                    self.logger.warning(
                        "Location '%s' has no default_item; using filler '%s' instead.",
                        loc.name,
                        self.get_filler_item_name(),
                    )
                    itempool.append(self.create_item(self.get_filler_item_name()))
                else:
                    itempool.append(self.create_item_by_code(loc.default_item_code))

            # Add to AP pool
            self.multiworld.itempool += itempool

            # Log item creation (pool size as total; shards counted separately)
            log_items_created(self.player, len(itempool), shard_count, len(itempool))

            # If shards are vanilla, convert shard locations to events so logic can see them without randomization.
            if self.options.shards.value == RandomizeShards.option_vanilla:
                event_count = 0
                for loc in self.multiworld.get_locations(self.player):
                    if not isinstance(loc, KirbyAmLocation) or loc.key is None:
                        continue
                    loc_meta = kirby_data.locations.get(loc.key)
                    if loc_meta and loc_meta.category == LocationCategory.SHARD:
                        if loc.default_item_code is None:
                            self.logger.warning(
                                "Shard location '%s' is missing default_item; leaving it randomized.",
                                loc.name,
                            )
                            continue
                        # Lock the vanilla shard item here as an event.
                        loc.place_locked_item(self.create_event(self.item_id_to_name[loc.default_item_code]))
                        loc.progress_type = LocationProgressType.DEFAULT
                        loc.address = None
                        event_count += 1
                logger.debug(f"[P{self.player}] Converted {event_count} shard locations to events (vanilla mode)")

    # Set world rules
    def set_rules(self) -> None:
        from .rules import set_rules as set_rules_impl
        set_rules_impl(self)

    # Helper methods for generation and output
    def generate_basic(self) -> None:
        # Create auth for client connection.
        self.auth = self.random.randbytes(16)

    def generate_output(self, output_directory: str) -> None:
        try:
            # Load base patch data from package resources
            patch_data = pkgutil.get_data(__name__, "data/base_patch.bsdiff4")
            if patch_data is None:
                raise FileNotFoundError(
                    "Missing resource 'data/base_patch.bsdiff4' in the kirbyam package/apworld. "
                    "Ensure it is included when packaging."
                )

            # Create procedure patch
            patch = KirbyAmProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch.bsdiff4", patch_data)
            write_tokens(self, patch)

            # Write the patch file
            out_file_name = self.multiworld.get_out_file_name_base(self.player)
            patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

            if hasattr(self, "_generation_start_time"):
                elapsed = time.time() - self._generation_start_time
                log_generation_complete(self.player, self.player_name, elapsed)
        except Exception as exc:
            log_generation_error(self.player, self.player_name, str(exc))
            raise

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        # Register auth token -> player name mapping for BizHawk
        key = base64.b64encode(self.auth).decode("ascii")
        connect_names = multidata.setdefault("connect_names", {})
        # connect_names is used as an auth-token to player-name mapping.
        # The player's name should always be the value.
        connect_names[key] = self.player_name

    # Helper method to fill slot data
    def fill_slot_data(self) -> dict[str, Any]:
        # Slot data needed by client. Keep minimal while you iterate.
        return self.options.as_dict(
            "goal",
            "shards",
        )

    # Helper methods to create items and events
    def create_item(self, name: str) -> KirbyAmItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    # Helper method to create item by item code
    def create_item_by_code(self, item_code: int) -> KirbyAmItem:
        return KirbyAmItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player,
        )

    # Helper method to create event item
    def create_event(self, name: str) -> KirbyAmItem:
        return KirbyAmItem(
            name,
            ItemClassification.progression,
            None,
            self.player,
        )
