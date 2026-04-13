"""
Archipelago World definition for Kirby & The Amazing Mirror
"""
import base64
import os
import pkgutil
import random
import time
from collections import Counter
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, TextIO

import settings
from BaseClasses import ItemClassification, LocationProgressType, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

from .client import KirbyAmClient  # type: ignore  # Required to register BizHawk client
from .ability_randomization import (
    VALID_ENEMY_COPY_ABILITIES,
    build_enemy_copy_ability_policy,
)
from .colors import STARTING_KIRBY_COLOR_RANDOM_OPTION, resolve_kirby_color
from .data import LocationCategory, load_json_data, data as kirby_data
from .enemy_ability_runtime_patch import build_enemy_copy_spoiler_rows
from .generation_logging import (
    generation_stage,
    log_generation_complete,
    log_generation_error,
    log_generation_start,
    log_items_created,
    log_regions_created,
    logger,
)
from .groups import ITEM_GROUPS, LOCATION_GROUPS, resolve_item_group
from .items import KirbyAmItem, create_item_label_to_code_map, get_item_classification
from .locations import KirbyAmLocation, create_location_label_to_id_map
from .options import (
    OPTION_GROUPS,
    AbilityRandomizationMode,
    Goal,
    KirbyAmOptions,
    OneHitMode,
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
        ["Harrison Sherwin, BlameMateo"],
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
    _resolved_starting_kirby_color_id: int
    _resolved_starting_kirby_color_name: str

    # Generation stages
    # Active filler pool for random selection.
    # Issue #295 ships the life-up plus consumable filler set as uniform choices.
    ACTIVE_FILLER_POOL: ClassVar[tuple[str, ...]] = (
        "1 Up",
        "Small Food",
        "Cell Phone Battery",
        "Max Tomato",
        "Invincibility Candy",
    )
    ACTIVE_FILLER_POOL_NO_FOOD: ClassVar[tuple[str, ...]] = tuple(
        item_name for item_name in ACTIVE_FILLER_POOL if item_name not in {"Small Food", "Max Tomato"}
    )
    ACTIVE_FILLER_POOL_NO_1UP: ClassVar[tuple[str, ...]] = tuple(
        item_name for item_name in ACTIVE_FILLER_POOL if item_name != "1 Up"
    )
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
    _BOSS_DEFEAT_KEY_ORDER: ClassVar[tuple[str, ...]] = (
        "BOSS_DEFEAT_1",
        "BOSS_DEFEAT_2",
        "BOSS_DEFEAT_3",
        "BOSS_DEFEAT_4",
        "BOSS_DEFEAT_5",
        "BOSS_DEFEAT_6",
        "BOSS_DEFEAT_7",
        "BOSS_DEFEAT_8",
    )
    # Shard item labels in the same positional order as _BOSS_DEFEAT_KEY_ORDER.
    # Vanilla placement follows boss-defeat index -> shard label. This order also
    # matches the legacy shard-chest ordering, but boss-defeat ordering is the
    # authoritative mapping for the current contract.
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
    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # If you don't have sanity_check.py yet, comment these out for now.
        from .sanity_check import validate_group_maps, validate_regions
        assert validate_regions()
        assert validate_group_maps()

    def _no_extra_lives_enabled(self) -> bool:
        option = getattr(getattr(self, "options", None), "no_extra_lives", None)
        value = getattr(option, "value", option)
        return bool(value)

    def _one_hit_mode_value(self) -> int:
        option = getattr(getattr(self, "options", None), "one_hit_mode", None)
        value = getattr(option, "value", option)
        return int(value) if value is not None else 0

    def _start_with_all_maps_enabled(self) -> bool:
        option = getattr(getattr(self, "options", None), "start_with_all_maps", None)
        value = getattr(option, "value", option)
        return bool(value)

    def _get_resolved_starting_kirby_color(self) -> tuple[int, str]:
        resolved_id = getattr(self, "_resolved_starting_kirby_color_id", None)
        resolved_name = getattr(self, "_resolved_starting_kirby_color_name", None)
        if isinstance(resolved_id, int) and isinstance(resolved_name, str) and resolved_name:
            return resolved_id, resolved_name

        option = getattr(getattr(self, "options", None), "starting_kirby_color", None)
        option_value = getattr(option, "value", option)
        try:
            choice_value = int(option_value) if option_value is not None else 0
        except (TypeError, ValueError):
            choice_value = 0
        rng = getattr(self, "random", None)
        if choice_value == STARTING_KIRBY_COLOR_RANDOM_OPTION and not isinstance(rng, random.Random):
            raise RuntimeError(
                "KirbyAM starting Kirby color could not be resolved from the world RNG. "
                "Expected a valid seeded random.Random on self.random or a cached resolved color."
            )
        color = resolve_kirby_color(choice_value, rng)
        self._resolved_starting_kirby_color_id = color.color_id
        self._resolved_starting_kirby_color_name = color.display_name
        return self._resolved_starting_kirby_color_id, self._resolved_starting_kirby_color_name

    def _active_filler_pool(self) -> tuple[str, ...]:
        pool = self.ACTIVE_FILLER_POOL
        if self._one_hit_mode_value() == OneHitMode.option_exclude_vitality_counters:
            pool = self.ACTIVE_FILLER_POOL_NO_FOOD
        if self._no_extra_lives_enabled():
            pool = tuple(item_name for item_name in pool if item_name != "1 Up")
        return pool

    # Filler item name
    def get_filler_item_name(self) -> str:
        return self.random.choice(self._active_filler_pool())

    def _ordered_boss_defeat_locations(self, boss_locations: list[KirbyAmLocation]) -> list[KirbyAmLocation]:
        boss_locations_by_key = {
            loc.key: loc for loc in boss_locations if loc.key is not None
        }
        ordered_boss_locations: list[KirbyAmLocation] = []
        for boss_key in self._BOSS_DEFEAT_KEY_ORDER:
            boss_loc = boss_locations_by_key.get(boss_key)
            if boss_loc is None:
                raise ValueError(f"KirbyAM boss-defeat location missing from region graph: {boss_key}")
            ordered_boss_locations.append(boss_loc)
        return ordered_boss_locations

    # Pre-generation adjustments
    def generate_early(self) -> None:
        # Track generation start
        self._generation_start_time = time.time()
        log_generation_start(self.player, self.player_name, self.options.as_dict("goal", "shards", "death_link"))

        with generation_stage("generate_early", self.player, self.player_name):
            logger.info(f"[P{self.player}] Shards mode: {self.options.shards.current_key}")
            chosen_color_key = self.options.starting_kirby_color.current_key
            resolved_color = resolve_kirby_color(int(self.options.starting_kirby_color.value), self.random)
            self._resolved_starting_kirby_color_id = resolved_color.color_id
            self._resolved_starting_kirby_color_name = resolved_color.display_name
            logger.info(
                "[P%s] Starting Kirby color option: %s -> %s (%s)",
                self.player,
                chosen_color_key,
                resolved_color.display_name,
                resolved_color.color_id,
            )

            mode = int(self.options.ability_randomization_mode.value)
            randomize_boss_spawned = bool(self.options.ability_randomization_boss_spawns.value)
            randomize_miniboss = bool(self.options.ability_randomization_minibosses.value)
            randomize_minny = bool(self.options.ability_randomization_minny.value)
            randomize_non_ability = bool(self.options.ability_randomization_passive_enemies.value)
            no_ability_weight = int(self.options.ability_randomization_no_ability_weight.value)
            self._enemy_copy_ability_policy = build_enemy_copy_ability_policy(
                self.random,
                mode,
                randomize_boss_spawned,
                randomize_miniboss,
                include_minny=randomize_minny,
                include_passive_enemies=randomize_non_ability,
                no_ability_weight=no_ability_weight,
            )
            if mode == AbilityRandomizationMode.option_off:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: off (%s whitelist entries, minny=%s, no_ability_weight=%s)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                    randomize_minny,
                    no_ability_weight,
                )
            elif mode == AbilityRandomizationMode.option_shuffled:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: shuffled "
                    "(%s whitelist entries, minny=%s, passive_enemies=%s, no_ability_weight=%s)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                    randomize_minny,
                    randomize_non_ability,
                    no_ability_weight,
                )
                spoiler_rows = build_enemy_copy_spoiler_rows(self._enemy_copy_ability_policy)
                if spoiler_rows:
                    logger.info(
                        "[P%s] Enemy copy-ability shuffled assignments (kind | source -> ability):",
                        self.player,
                    )
                    for source_kind, source_key, ability_name in spoiler_rows:
                        logger.info(
                            "[P%s]   %s | %s -> %s",
                            self.player,
                            source_kind,
                            source_key,
                            ability_name,
                        )
            else:
                logger.info(
                    "[P%s] Enemy copy-ability randomization: completely_random "
                    "(%s whitelist entries, minny=%s, passive_enemies=%s, no_ability_weight=%s)",
                    self.player,
                    len(VALID_ENEMY_COPY_ABILITIES),
                    randomize_minny,
                    randomize_non_ability,
                    no_ability_weight,
                )
                logger.debug(
                    "[P%s] Enemy copy-ability policy: %s",
                    self.player,
                    self._enemy_copy_ability_policy,
                )

            if self._start_with_all_maps_enabled():
                map_items = [
                    item for item in kirby_data.items.values()
                    if "Maps" in item.tags
                ]
                for map_item in map_items:
                    self.push_precollected(self.create_item(map_item.label))
                logger.info(
                    "[P%s] start_with_all_maps: precollected %s map item(s)",
                    self.player,
                    len(map_items),
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
            sound_player_chest_locations: list[KirbyAmLocation] = []
            hub_switch_locations: list[KirbyAmLocation] = []
            room_sanity_locations: list[KirbyAmLocation] = []
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
                elif loc_meta.category == LocationCategory.SOUND_PLAYER_CHEST:
                    sound_player_chest_locations.append(loc)
                elif loc_meta.category == LocationCategory.HUB_SWITCH:
                    hub_switch_locations.append(loc)
                elif loc_meta.category == LocationCategory.ROOM_SANITY:
                    room_sanity_locations.append(loc)

            boss_locations.sort(key=lambda loc: loc.key or "")
            major_chest_locations.sort(key=lambda loc: loc.key or "")
            vitality_chest_locations.sort(key=lambda loc: loc.key or "")
            sound_player_chest_locations.sort(key=lambda loc: loc.key or "")
            hub_switch_locations.sort(key=lambda loc: loc.key or "")
            room_sanity_locations.sort(key=lambda loc: loc.key or "")

            locked_shard_count = 0
            randomized_item_codes: list[int] = []
            if boss_locations or major_chest_locations or vitality_chest_locations or sound_player_chest_locations or hub_switch_locations or room_sanity_locations:
                shard_label_to_code = {
                    item.label: item.item_id
                    for item in kirby_data.items.values()
                    if "Shards" in item.tags
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

                expected_boss_defeat_count = sum(
                    1 for m in kirby_data.locations.values()
                    if m.category == LocationCategory.BOSS_DEFEAT
                )
                if len(boss_locations) != expected_boss_defeat_count:
                    raise ValueError(
                        f"KirbyAM expected {expected_boss_defeat_count} boss-defeat locations,"
                        f" found {len(boss_locations)}"
                    )

                # In vanilla shard mode, each area's boss defeat location awards
                # that area's matching shard (fixed AP placement).
                if self.options.shards.value == RandomizeShards.option_vanilla:
                    ordered_boss_locations = self._ordered_boss_defeat_locations(boss_locations)

                    if len(ordered_boss_locations) != len(shard_item_codes):
                        raise ValueError(
                            "KirbyAM shard placement mismatch: %d ordered boss locations vs %d shard items"
                            % (len(ordered_boss_locations), len(shard_item_codes))
                        )
                    for boss_loc, shard_code in zip(ordered_boss_locations, shard_item_codes):
                        boss_loc.place_locked_item(self.create_item_by_code(shard_code))
                        boss_loc.progress_type = LocationProgressType.DEFAULT
                        locked_shard_count += 1

                    logger.info(
                        "[P%s] Locked %s shard items onto boss-defeat locations (mode=%s)",
                        self.player,
                        locked_shard_count,
                        self.options.shards.current_key,
                    )

                open_physical_locations = [
                    loc for loc in boss_locations + major_chest_locations + vitality_chest_locations + sound_player_chest_locations + hub_switch_locations + room_sanity_locations
                    if loc.item is None
                ]
                needed_pool_size = len(open_physical_locations)

                non_filler_item_codes = [
                    item.item_id
                    for item in kirby_data.items.values()
                    if item.classification != ItemClassification.filler
                ]
                vitality_item_codes = getattr(self, "_vitality_item_codes", None)
                if vitality_item_codes is None:
                    vitality_item_codes = {
                        item.item_id
                        for item in kirby_data.items.values()
                        if "Vitality" in item.tags
                    }
                    self._vitality_item_codes = vitality_item_codes
                map_item_codes = getattr(self, "_map_item_codes", None)
                if map_item_codes is None:
                    map_item_codes = {
                        item.item_id
                        for item in kirby_data.items.values()
                        if "Maps" in item.tags
                    }
                    self._map_item_codes = map_item_codes
                if self.options.shards.value == RandomizeShards.option_vanilla:
                    shard_code_set = set(shard_item_codes)
                    non_filler_item_codes = [
                        code for code in non_filler_item_codes if code not in shard_code_set
                    ]

                if self._one_hit_mode_value() == OneHitMode.option_exclude_vitality_counters:
                    excluded_vitality_count = sum(
                        1 for code in non_filler_item_codes if code in vitality_item_codes
                    )
                    non_filler_item_codes = [
                        code for code in non_filler_item_codes if code not in vitality_item_codes
                    ]
                    logger.info(
                        "[P%s] One-hit mode (exclude_vitality_counters): removed %s vitality counter item(s) from non-filler pool",
                        self.player,
                        excluded_vitality_count,
                    )

                if self._start_with_all_maps_enabled():
                    excluded_map_count = sum(
                        1 for code in non_filler_item_codes if code in map_item_codes
                    )
                    non_filler_item_codes = [
                        code for code in non_filler_item_codes if code not in map_item_codes
                    ]
                    logger.info(
                        "[P%s] start_with_all_maps: removed %s map item(s) from non-filler pool",
                        self.player,
                        excluded_map_count,
                    )

                if len(non_filler_item_codes) > needed_pool_size:
                    raise ValueError(
                        "KirbyAM item pool mismatch: non-filler item count %d exceeds open physical locations %d"
                        % (len(non_filler_item_codes), needed_pool_size)
                    )

                filler_needed = needed_pool_size - len(non_filler_item_codes)
                randomized_item_codes.extend(non_filler_item_codes)
                randomized_item_codes.extend(
                    self.item_name_to_id[self.get_filler_item_name()]
                    for _ in range(filler_needed)
                )
                self.random.shuffle(randomized_item_codes)

                non_filler_pool_codes = [
                    code
                    for code in randomized_item_codes
                    if get_item_classification(code) != ItemClassification.filler
                ]
                if sorted(non_filler_pool_codes) != sorted(non_filler_item_codes):
                    raise ValueError(
                        "KirbyAM item pool invariant failed: randomized non-filler item set does not match expected set"
                    )

                if len(randomized_item_codes) != needed_pool_size:
                    raise ValueError(
                        "KirbyAM item pool mismatch: open physical locations=%s randomized item count=%s"
                        % (needed_pool_size, len(randomized_item_codes))
                    )

                vitality_code_counts = Counter(
                    code for code in randomized_item_codes if code in vitality_item_codes
                )
                if self._one_hit_mode_value() == OneHitMode.option_exclude_vitality_counters:
                    if vitality_code_counts:
                        raise ValueError(
                            "KirbyAM vitality pool invariant failed in exclude_vitality_counters mode: "
                            f"expected zero vitality items, got counts={dict(vitality_code_counts)}"
                        )
                else:
                    missing_vitality_codes = sorted(
                        code for code in vitality_item_codes if vitality_code_counts.get(code, 0) == 0
                    )
                    duplicate_vitality_codes = {
                        code: count
                        for code, count in vitality_code_counts.items()
                        if count > 1
                    }
                    if missing_vitality_codes or duplicate_vitality_codes:
                        raise ValueError(
                            "KirbyAM vitality pool invariant failed: each vitality counter must appear exactly once. "
                            f"missing={missing_vitality_codes} duplicates={duplicate_vitality_codes}"
                        )
                logger.info(
                    "[P%s] Vitality counter pool multiplicity: %s",
                    self.player,
                    dict(sorted(vitality_code_counts.items())),
                )

                if self._start_with_all_maps_enabled():
                    map_code_counts = Counter(
                        code for code in randomized_item_codes if code in map_item_codes
                    )
                    if map_code_counts:
                        raise ValueError(
                            "KirbyAM map pool invariant failed in start_with_all_maps mode: "
                            f"expected zero map items in pool, got counts={dict(map_code_counts)}"
                        )
                    logger.info(
                        "[P%s] start_with_all_maps: confirmed no map items in randomized pool",
                        self.player,
                    )

            if (boss_locations or major_chest_locations or vitality_chest_locations or sound_player_chest_locations or hub_switch_locations or room_sanity_locations) and not randomized_item_codes:
                raise ValueError(
                    "KirbyAM item pool build failed: no randomized items were produced. "
                    "This likely indicates a problem with boss/major/vitality/sound-player/hub-switch locations, "
                    "room-sanity locations, or region/location data."
                )

            itempool: list[KirbyAmItem] = [
                self.create_item_by_code(code) for code in randomized_item_codes
            ]

            # Add to AP pool
            self.multiworld.itempool += itempool

            useful_count = sum(1 for item in itempool if item.useful)
            filler_count = sum(1 for item in itempool if item.filler)
            progression_count = sum(1 for item in itempool if item.advancement)
            shard_group = resolve_item_group(
                self.item_name_groups,
                "Shards",
                default=self._SHARD_ITEM_LABEL_ORDER,
            )
            pool_shard_count = sum(1 for item in itempool if item.name in shard_group)
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

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        mode = int(self.options.ability_randomization_mode.value)
        if mode != AbilityRandomizationMode.option_shuffled:
            return

        policy = getattr(self, "_enemy_copy_ability_policy", None)
        if not isinstance(policy, dict):
            return

        spoiler_rows = build_enemy_copy_spoiler_rows(policy)
        if not spoiler_rows:
            return

        spoiler_handle.write(f"\n\n{self.player_name}'s Enemy Copy Ability Shuffle:\n\n")
        for source_kind, source_key, ability_name in spoiler_rows:
            spoiler_handle.write(f"{source_kind:12s} | {source_key:28s} -> {ability_name}\n")

    # Helper method to fill slot data
    def fill_slot_data(self) -> dict[str, Any]:
        # Slot data needed by client.
        # Pre-v0.1.0 policy: emit only canonical ability_randomization_* keys.
        # Legacy key aliases are intentionally not emitted before first public release.
        slot_data = self.options.as_dict(
            "goal",
            "shards",
            "start_with_all_maps",
            "starting_kirby_color",
            "no_extra_lives",
            "one_hit_mode",
            "death_link",
            "ability_randomization_mode",
            "ability_randomization_boss_spawns",
            "ability_randomization_minibosses",
            "ability_randomization_minny",
            "ability_randomization_passive_enemies",
            "ability_randomization_no_ability_weight",
            "room_sanity",
            "enable_debug_logging",
            toggles_as_bools=True,
        )
        resolved_color_id, resolved_color_name = self._get_resolved_starting_kirby_color()
        slot_data["starting_kirby_color"] = resolved_color_id
        slot_data["starting_kirby_color_name"] = resolved_color_name
        policy = getattr(self, "_enemy_copy_ability_policy", None)
        assert policy is not None, (
            "Enemy copy ability policy must be initialized before fill_slot_data is called."
        )
        allowed_abilities = policy.get("allowed_abilities", VALID_ENEMY_COPY_ABILITIES)
        slot_data["enemy_copy_ability_whitelist"] = list(allowed_abilities)
        slot_data["enemy_copy_ability_policy"] = dict(policy)

        # Tracker surface integration (Issue #114)
        # Expose all locations and rooms for tracker display
        slot_data["locations"] = {
            loc_key: {
                "label": loc_data.label,
                "location_id": loc_data.location_id,
                "category": loc_data.category.name,
                "tags": sorted(loc_data.tags),
            }
            for loc_key, loc_data in kirby_data.locations.items()
        }

        # All rooms (visited and unvisited), including those not in Room Sanity
        rooms_payload = load_json_data("regions/rooms.json")
        rooms = rooms_payload if isinstance(rooms_payload, dict) else {}
        slot_data["rooms"] = {
            room_key: {
                "label": room_data.get("label", room_key),
                "exits": room_data.get("exits", []),
                "parent_region": room_key.split("/")[0] if "/" in room_key else "",
                "room_sanity_location_id": room_data.get("room_sanity", {}).get("location_id"),
            }
            for room_key, room_data in rooms.items()
        }

        # Unique items for tracker display (items tagged as "Unique").
        # Emit in stable deduplicated order for tracker/cache determinism.
        slot_data["unique_items"] = sorted(
            {
                item_data.label
                for item_data in kirby_data.items.values()
                if "Unique" in item_data.tags
            }
        )

        # Debug settings are grouped under one key to keep slot_data extensible.
        slot_data["debug"] = {
            "logging": bool(self.options.enable_debug_logging.value),
        }
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
