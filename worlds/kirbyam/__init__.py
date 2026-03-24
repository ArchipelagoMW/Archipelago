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
from .ability_randomization import (
    VALID_ENEMY_COPY_ABILITIES,
    build_enemy_copy_ability_policy,
)
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
from .options import (
    OPTION_GROUPS,
    EnemyCopyAbilityRandomization,
    Goal,
    KirbyAmOptions,
    RandomizeShards,
)
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
    _enemy_copy_ability_policy: dict[str, Any]

    # Generation stages
    # Phase 1: Active filler pool for random selection.
    # Contains only "1 Up" for Phase 1 balance; supports future expansion.
    ACTIVE_FILLER_POOL: ClassVar[tuple[str, ...]] = ("1 Up",)
    _SHARD_CHEST_KEY_ORDER: ClassVar[tuple[str, ...]] = (
        "MAJOR_CHEST_MUSTARD_MOUNTAIN",
        "MAJOR_CHEST_MOONLIGHT_MANSION",
        "MAJOR_CHEST_CANDY_CONSTELLATION",
        "MAJOR_CHEST_OLIVE_OCEAN",
        "MAJOR_CHEST_PEPPERMINT_PALACE",
        "MAJOR_CHEST_CABBAGE_CAVERN",
        "MAJOR_CHEST_CARROT_CASTLE",
        "MAJOR_CHEST_RADISH_RUINS",
    )
    # Shard item labels in the same positional order as _SHARD_CHEST_KEY_ORDER.
    # Using labels (stable identifiers from items.json) rather than sorted item IDs
    # keeps the vanilla chest→shard mapping correct even if item IDs are reorganised.
    _SHARD_ITEM_LABEL_ORDER: ClassVar[tuple[str, ...]] = (
        "Mustard Mountain - Mirror Shard",
        "Moonlight Mansion - Mirror Shard",
        "Candy Constellation - Mirror Shard",
        "Olive Ocean - Mirror Shard",
        "Peppermint Palace - Mirror Shard",
        "Cabbage Cavern - Mirror Shard",
        "Carrot Castle - Mirror Shard",
        "Radish Ruins - Mirror Shard",
    )
    _RAINBOW_ROUTE_CHEST_KEY: ClassVar[str] = "MAJOR_CHEST_RAINBOW_ROUTE"

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # If you don't have sanity_check.py yet, comment these out for now.
        from .sanity_check import validate_group_maps, validate_regions
        assert validate_regions()
        assert validate_group_maps()

    # Filler item name
    def get_filler_item_name(self) -> str:
        return self.random.choice(self.ACTIVE_FILLER_POOL)

    # Pre-generation adjustments
    def generate_early(self) -> None:
        # Track generation start
        self._generation_start_time = time.time()
        log_generation_start(self.player, self.player_name, self.options.as_dict("goal", "shards", "death_link"))

        with generation_stage("generate_early", self.player, self.player_name):
            # If shards are shuffled as items, they must be local to the ROM unless you implement remote shard handling.
            if self.options.shards.value == RandomizeShards.option_shuffle:
                self.logger.debug("Shards are shuffled; marking them as local items.")
                self.options.local_items.value.update(self.item_name_groups.get("Shard", set()))
                logger.info(f"[P{self.player}] Shards marked as local items (shuffle mode)")
            else:
                logger.info(f"[P{self.player}] Shards mode: {self.options.shards.current_key}")

            mode = int(self.options.enemy_copy_ability_randomization.value)
            randomize_boss_spawned = bool(self.options.randomize_boss_spawned_ability_grants.value)
            randomize_miniboss = bool(self.options.randomize_miniboss_ability_grants.value)
            self._enemy_copy_ability_policy = build_enemy_copy_ability_policy(
                self.random,
                mode,
                randomize_boss_spawned,
                randomize_miniboss,
            )
            if mode == EnemyCopyAbilityRandomization.option_vanilla:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: vanilla (%s whitelist entries)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                )
            elif mode == EnemyCopyAbilityRandomization.option_shuffled:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: shuffled (%s whitelist entries)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                )
            else:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: completely_random (%s whitelist entries)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                )
                logger.debug(
                    "[P%s] Enemy copy-ability policy: %s",
                    self.player,
                    self._enemy_copy_ability_policy,
                )

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

            # Resolve fillable physical locations by category.
            boss_locations: list[KirbyAmLocation] = []
            major_chest_locations: list[KirbyAmLocation] = []
            vitality_chest_locations: list[KirbyAmLocation] = []
            location_by_key: dict[str, KirbyAmLocation] = {}
            for loc in fill_locations:
                if loc.key is None:
                    continue
                location_by_key[loc.key] = loc
                loc_meta = kirby_data.locations.get(loc.key)
                if loc_meta is None:
                    continue
                if loc_meta.category == LocationCategory.BOSS_DEFEAT:
                    boss_locations.append(loc)
                elif loc_meta.category == LocationCategory.MAJOR_CHEST:
                    major_chest_locations.append(loc)
                elif loc_meta.category == LocationCategory.VITALITY_CHEST:
                    vitality_chest_locations.append(loc)

            boss_locations.sort(key=lambda loc: loc.key or "")
            major_chest_locations.sort(key=lambda loc: loc.key or "")
            vitality_chest_locations.sort(key=lambda loc: loc.key or "")

            locked_shard_count = 0
            randomized_item_codes: list[int] = []
            if boss_locations or major_chest_locations or vitality_chest_locations:
                shard_label_to_code = {
                    item.label: item.item_id
                    for item in kirby_data.items.values()
                    if "Shard" in item.tags
                }
                missing_shard_labels = [
                    label for label in self._SHARD_ITEM_LABEL_ORDER
                    if label not in shard_label_to_code
                ]
                if missing_shard_labels:
                    available_labels = sorted(shard_label_to_code.keys())
                    raise ValueError(
                        "KirbyAM shard item configuration error: missing shard labels in items data: "
                        f"{missing_shard_labels}. "
                        f"Available shard-tagged item labels: {available_labels}"
                    )
                shard_item_codes = [
                    shard_label_to_code[label] for label in self._SHARD_ITEM_LABEL_ORDER
                ]

                shard_chest_locations: list[KirbyAmLocation] = []
                for chest_key in self._SHARD_CHEST_KEY_ORDER:
                    shard_chest = location_by_key.get(chest_key)
                    if shard_chest is None:
                        raise ValueError(f"KirbyAM shard chest location missing from region graph: {chest_key}")
                    shard_chest_locations.append(shard_chest)

                rainbow_route_chest = location_by_key.get(self._RAINBOW_ROUTE_CHEST_KEY)
                if rainbow_route_chest is None:
                    raise ValueError(
                        f"KirbyAM non-shard chest location missing from region graph: {self._RAINBOW_ROUTE_CHEST_KEY}"
                    )

                expected_boss_defeat_count = sum(
                    1 for m in kirby_data.locations.values()
                    if m.category == LocationCategory.BOSS_DEFEAT
                )
                if len(boss_locations) != expected_boss_defeat_count:
                    raise ValueError(
                        f"KirbyAM expected {expected_boss_defeat_count} boss-defeat locations,"
                        f" found {len(boss_locations)}"
                    )

                # Place shards onto major-chest locations in vanilla/shuffle modes.
                if self.options.shards.value in {RandomizeShards.option_vanilla, RandomizeShards.option_shuffle}:
                    if self.options.shards.value == RandomizeShards.option_vanilla:
                        shard_codes_for_chests = shard_item_codes
                    else:
                        shard_codes_for_chests = list(shard_item_codes)
                        self.random.shuffle(shard_codes_for_chests)

                    if len(shard_chest_locations) != len(shard_codes_for_chests):
                        raise ValueError(
                            "KirbyAM shard placement mismatch: %d shard chest locations vs %d shard items"
                            % (len(shard_chest_locations), len(shard_codes_for_chests))
                        )
                    for chest_loc, shard_code in zip(shard_chest_locations, shard_codes_for_chests):
                        chest_loc.place_locked_item(self.create_item_by_code(shard_code))
                        chest_loc.progress_type = LocationProgressType.DEFAULT
                        locked_shard_count += 1

                    logger.info(
                        "[P%s] Locked %s shard items onto major-chest locations (mode=%s)",
                        self.player,
                        locked_shard_count,
                        self.options.shards.current_key,
                    )

                # Build the non-shard pool from boss rewards, vitality chest rewards,
                # and Rainbow Route's big chest reward.
                base_non_shard_codes: list[int] = []
                for loc in boss_locations + vitality_chest_locations + [rainbow_route_chest]:
                    if loc.default_item_code is None:
                        raise ValueError(f"KirbyAM location '{loc.name}' is missing a default item code")
                    base_non_shard_codes.append(loc.default_item_code)

                if self.options.shards.value == RandomizeShards.option_completely_random:
                    randomized_item_codes.extend(shard_item_codes)
                randomized_item_codes.extend(base_non_shard_codes)

                open_physical_locations = [
                    loc for loc in boss_locations + major_chest_locations + vitality_chest_locations
                    if loc.item is None
                ]
                needed_pool_size = len(open_physical_locations)

                if len(randomized_item_codes) != needed_pool_size:
                    raise ValueError(
                        "KirbyAM item pool mismatch: open physical locations=%s randomized item count=%s"
                        % (needed_pool_size, len(randomized_item_codes))
                    )

            if (boss_locations or major_chest_locations or vitality_chest_locations) and not randomized_item_codes:
                raise ValueError(
                    "KirbyAM item pool build failed: no randomized items were produced. "
                    "This likely indicates a problem with boss/major/vitality chest locations or region data."
                )

            itempool: list[KirbyAmItem] = [
                self.create_item_by_code(code) for code in randomized_item_codes
            ]

            # Add to AP pool
            self.multiworld.itempool += itempool

            useful_count = sum(1 for item in itempool if item.useful)
            filler_count = sum(1 for item in itempool if item.filler)
            progression_count = sum(1 for item in itempool if item.advancement)
            pool_shard_count = sum(1 for item in itempool if item.name in self.item_name_groups.get("Shard", set()))
            logger.info(
                "[P%s] Item pool classification summary: useful=%s filler=%s progression=%s",
                self.player,
                useful_count,
                filler_count,
                progression_count,
            )

            goal_event_count = 0
            for loc in self.multiworld.get_locations(self.player):
                if not isinstance(loc, KirbyAmLocation) or loc.key is None:
                    continue
                loc_meta = kirby_data.locations.get(loc.key)
                if loc_meta and loc_meta.category == LocationCategory.GOAL:
                    loc.place_locked_item(self.create_event(loc.name))
                    loc.progress_type = LocationProgressType.DEFAULT
                    # Goal checks are runtime events, not host-fillable AP locations.
                    # Keep address=None so multidata does not serialize a None item
                    # for a numeric location entry (host LocationStore requires ints).
                    loc.address = None
                    goal_event_count += 1

            # Log item creation (randomized pool + fixed shard placements)
            log_items_created(
                self.player,
                len(itempool),
                locked_shard_count + pool_shard_count,
                len(itempool) - pool_shard_count,
            )
            logger.debug(f"[P{self.player}] Converted {goal_event_count} goal locations to locked events")

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
        # Register auth token using the same (team, slot) tuple shape as player names.
        key = base64.b64encode(self.auth).decode("ascii")
        connect_names = multidata["connect_names"]
        connect_names[key] = connect_names[self.player_name]

    # Helper method to fill slot data
    def fill_slot_data(self) -> dict[str, Any]:
        # Slot data needed by client. Keep minimal while you iterate.
        slot_data = self.options.as_dict(
            "goal",
            "shards",
            "death_link",
            "enemy_copy_ability_randomization",
            "randomize_boss_spawned_ability_grants",
            "randomize_miniboss_ability_grants",
            toggles_as_bools=True,
        )
        policy = getattr(self, "_enemy_copy_ability_policy", None)
        assert policy is not None, (
            "Enemy copy ability policy must be initialized before fill_slot_data is called."
        )
        allowed_abilities = policy.get("allowed_abilities", VALID_ENEMY_COPY_ABILITIES)
        slot_data["enemy_copy_ability_whitelist"] = list(allowed_abilities)
        slot_data["enemy_copy_ability_policy"] = dict(policy)
        return slot_data

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
