import random
from pathlib import Path
from types import SimpleNamespace
from collections import Counter

import pytest

from BaseClasses import ItemClassification

from .. import KirbyAmWorld
from ..data import LocationCategory, data
from ..items import get_item_classification
from ..locations import KirbyAmLocation
from ..options import OneHitMode, RandomizeShards


class _DummyMultiWorld:
    def __init__(self, locations):
        self._locations = locations
        self.itempool = []

    def get_locations(self, player):
        return self._locations

    def get_player_name(self, player):
        return "KirbyAM-Test"


def _build_fill_locations() -> list[KirbyAmLocation]:
    locations: list[KirbyAmLocation] = []
    for key, meta in data.locations.items():
        if meta.category == LocationCategory.GOAL:
            continue
        locations.append(
            KirbyAmLocation(
                1,
                meta.label,
                meta.location_id,
                None,
                key=key,
                default_item_code=meta.default_item,
            )
        )
    return locations


def _build_world_for_create_items(
    shard_mode: int,
    one_hit_mode: int = OneHitMode.option_off,
    start_with_all_maps: int = 0,
    enable_traps: int = 0,
    trap_fill_percentage: int = 25,
) -> tuple[KirbyAmWorld, list[KirbyAmLocation]]:
    locations = _build_fill_locations()
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.player = 1
    world.random = random.Random(7)
    world.multiworld = _DummyMultiWorld(locations)
    world.options = SimpleNamespace(
        shards=SimpleNamespace(value=shard_mode, current_key={
            RandomizeShards.option_vanilla: "vanilla",
            RandomizeShards.option_completely_random: "completely_random",
        }[shard_mode]),
        no_extra_lives=SimpleNamespace(value=False),
        enable_traps=SimpleNamespace(value=enable_traps),
        trap_fill_percentage=SimpleNamespace(value=trap_fill_percentage),
        one_hit_mode=SimpleNamespace(value=one_hit_mode),
        start_with_all_maps=SimpleNamespace(value=start_with_all_maps),
    )
    return world, locations


def test_useful_item_catalog_includes_map_and_vitality() -> None:
    useful_items = [item for item in data.items.values() if item.classification & ItemClassification.useful]

    assert useful_items, "Expected at least one useful item in KirbyAM item data"
    map_items = [item for item in useful_items if "Maps" in item.tags]
    assert map_items, "Expected at least one useful map item"
    assert any("Vitality" in item.tags for item in useful_items), "Expected at least one useful vitality item"
    assert len(map_items) >= 8, "Expected full eight-area map catalog in useful items"


def test_boss_defeat_default_items_are_useful_maps() -> None:
    boss_locations = [loc for loc in data.locations.values() if loc.category == LocationCategory.BOSS_DEFEAT]
    assert boss_locations, "Expected boss defeat locations to exist"

    for location in boss_locations:
        assert location.default_item is not None, f"Expected default_item for {location.name}"
        item = data.items[location.default_item]
        assert item.classification & ItemClassification.useful, (
            f"Expected useful classification for {location.name} default item"
        )
        assert "Maps" in item.tags, f"Expected map default for {location.name}"


def test_vitality_chest_default_items_are_useful_vitality() -> None:
    vitality_locations = [loc for loc in data.locations.values() if loc.category == LocationCategory.VITALITY_CHEST]
    assert len(vitality_locations) == 4

    for location in vitality_locations:
        assert location.default_item is not None, f"Expected default_item for {location.name}"
        item = data.items[location.default_item]
        assert item.classification & ItemClassification.useful, (
            f"Expected useful classification for {location.name} default item"
        )
        assert "Vitality" in item.tags, f"Expected vitality default for {location.name}"


def test_sound_player_chest_default_item_is_useful_sound_player() -> None:
    sound_player_locations = [loc for loc in data.locations.values() if loc.category == LocationCategory.SOUND_PLAYER_CHEST]
    assert len(sound_player_locations) == 1

    location = sound_player_locations[0]
    assert location.default_item is not None, f"Expected default_item for {location.name}"
    item = data.items[location.default_item]
    assert item.classification & ItemClassification.useful
    assert "SoundPlayer" in item.tags


def test_filler_catalog_includes_current_filler_set() -> None:
    filler_items = [item for item in data.items.values() if item.classification == ItemClassification.filler]
    filler_by_label = {item.label: item for item in filler_items}
    filler_labels = set(filler_by_label)

    assert filler_labels == {
        "1 Up",
        "Small Food",
        "Energy Drink",
        "Hunk of Meat",
        "Cell Phone Battery",
        "Max Tomato",
        "Invincibility Candy",
    }
    assert all("Filler" in item.tags for item in filler_items)
    assert "Life" in filler_by_label["1 Up"].tags
    assert "Consumable" in filler_by_label["Small Food"].tags
    assert "Health" in filler_by_label["Small Food"].tags
    assert "Health" in filler_by_label["Energy Drink"].tags
    assert "Health" in filler_by_label["Hunk of Meat"].tags
    assert "Battery" in filler_by_label["Cell Phone Battery"].tags
    assert "Health" in filler_by_label["Max Tomato"].tags
    assert "Invincibility" in filler_by_label["Invincibility Candy"].tags


def test_consumable_filler_item_ids_are_stable() -> None:
    labels_to_ids = {item.label: item.item_id for item in data.items.values()}
    shard_ids = sorted(
        item.item_id
        for item in data.items.values()
        if "Shards" in item.tags
    )

    assert labels_to_ids["1 Up"] == 3860001
    assert shard_ids == list(range(3860002, 3860010))

    assert labels_to_ids["Small Food"] == 3860026
    assert labels_to_ids["Cell Phone Battery"] == 3860027
    assert labels_to_ids["Max Tomato"] == 3860028
    assert labels_to_ids["Invincibility Candy"] == 3860029
    assert labels_to_ids["Energy Drink"] == 3860030
    assert labels_to_ids["Hunk of Meat"] == 3860031
    assert labels_to_ids["Health Down Trap"] == 3860032
    assert labels_to_ids["Life Down Trap"] == 3860033
    assert labels_to_ids["Bomb Trap"] == 3860034
    assert labels_to_ids["Battery Drain Trap"] == 3860035
    assert "2 Up" not in labels_to_ids
    assert "3 Up" not in labels_to_ids


def test_available_trap_item_labels_are_driven_by_traps_json() -> None:
    assert data.available_trap_item_labels == (
        "Health Down Trap",
        "Life Down Trap",
        "Bomb Trap",
        "Battery Drain Trap",
    )


def test_trap_filler_percentage_replaces_eligible_filler_slots() -> None:
    world, _ = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        enable_traps=1,
        trap_fill_percentage=100,
    )

    world.create_items()

    trap_items = [item for item in world.multiworld.itempool if item.trap]
    assert trap_items, "Expected traps in pool when trap_fill_percentage is 100"


def test_active_filler_selection_is_seed_stable() -> None:
    world_a = KirbyAmWorld.__new__(KirbyAmWorld)
    world_a.random = random.Random(41)
    world_a.options = SimpleNamespace(no_extra_lives=SimpleNamespace(value=False))

    world_b = KirbyAmWorld.__new__(KirbyAmWorld)
    world_b.random = random.Random(41)
    world_b.options = SimpleNamespace(no_extra_lives=SimpleNamespace(value=False))

    picks_a = [world_a.get_filler_item_name() for _ in range(64)]
    picks_b = [world_b.get_filler_item_name() for _ in range(64)]

    assert picks_a == picks_b
    assert all(pick in KirbyAmWorld.ACTIVE_FILLER_POOL for pick in picks_a)
    assert len(KirbyAmWorld.ACTIVE_FILLER_POOL) > 1, "Expanded filler pool should contain multiple filler labels"


def test_filler_selection_respects_active_pool() -> None:
    """Verify that all filler picks are from the configured active filler pool."""
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = random.Random(12345)
    world.options = SimpleNamespace(no_extra_lives=SimpleNamespace(value=False))

    picks = [world.get_filler_item_name() for _ in range(50)]

    # All picks must be from the active pool, regardless of specific pool contents.
    assert all(pick in KirbyAmWorld.ACTIVE_FILLER_POOL for pick in picks), (
        f"Filler picks must be from ACTIVE_FILLER_POOL, got {set(picks)}"
    )


def test_active_filler_pool_contents() -> None:
    """Issue #295: active filler generation includes the shipped consumable set."""
    assert KirbyAmWorld.ACTIVE_FILLER_POOL == (
        "1 Up",
        "Small Food",
        "Energy Drink",
        "Hunk of Meat",
        "Cell Phone Battery",
        "Max Tomato",
        "Invincibility Candy",
    )


def test_no_extra_lives_excludes_1_up_from_active_filler_pool() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.options = SimpleNamespace(
        no_extra_lives=SimpleNamespace(value=True),
        one_hit_mode=SimpleNamespace(value=OneHitMode.option_off),
    )

    assert world._active_filler_pool() == (
        "Small Food",
        "Energy Drink",
        "Hunk of Meat",
        "Cell Phone Battery",
        "Max Tomato",
        "Invincibility Candy",
    )


def test_no_extra_lives_filler_selection_never_picks_1_up() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = random.Random(12345)
    world.options = SimpleNamespace(
        no_extra_lives=SimpleNamespace(value=True),
        one_hit_mode=SimpleNamespace(value=OneHitMode.option_off),
    )

    picks = [world.get_filler_item_name() for _ in range(50)]

    assert "1 Up" not in picks
    assert all(pick in world._active_filler_pool() for pick in picks)


def test_one_hit_mode_exclude_vitality_counters_excludes_food_from_active_filler_pool() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.options = SimpleNamespace(
        no_extra_lives=SimpleNamespace(value=False),
        one_hit_mode=SimpleNamespace(value=OneHitMode.option_exclude_vitality_counters),
    )

    assert world._active_filler_pool() == (
        "1 Up",
        "Cell Phone Battery",
        "Invincibility Candy",
    )


def test_one_hit_mode_exclude_vitality_counters_and_no_extra_lives_stack_filler_exclusions() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.options = SimpleNamespace(
        no_extra_lives=SimpleNamespace(value=True),
        one_hit_mode=SimpleNamespace(value=OneHitMode.option_exclude_vitality_counters),
    )

    assert world._active_filler_pool() == (
        "Cell Phone Battery",
        "Invincibility Candy",
    )


def test_one_hit_mode_exclude_vitality_counters_filler_selection_never_picks_healing_fillers() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = random.Random(12345)
    world.options = SimpleNamespace(
        no_extra_lives=SimpleNamespace(value=False),
        one_hit_mode=SimpleNamespace(value=OneHitMode.option_exclude_vitality_counters),
    )

    picks = [world.get_filler_item_name() for _ in range(50)]

    assert "Small Food" not in picks
    assert "Energy Drink" not in picks
    assert "Hunk of Meat" not in picks
    assert "Max Tomato" not in picks
    assert all(pick in world._active_filler_pool() for pick in picks)


def test_payload_supports_consumable_and_life_fillers() -> None:
    payload_path = Path(__file__).resolve().parents[1] / "kirby_ap_payload" / "ap_payload.c"
    with payload_path.open("r", encoding="utf-8") as payload_file:
        payload = payload_file.read()

    assert "static void ap_grant_lives(uint8_t amount)" in payload
    assert "static void ap_grant_small_food(void)" in payload
    assert "static void ap_grant_energy_drink(void)" in payload
    assert "static void ap_grant_hunk_of_meat(void)" in payload
    assert "static void ap_grant_battery(void)" in payload
    assert "static void ap_grant_max_tomato(void)" in payload
    assert "static void ap_grant_invincibility_candy(void)" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 26u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 27u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 28u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 29u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 30u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 31u" in payload
    assert "KIRBY_GIVE_INVINCIBILITY_FN" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 22u" not in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 23u" not in payload


def test_goal_locations_are_converted_to_addressless_events() -> None:
    goal_key, goal_meta = next(
        (key, meta) for key, meta in data.locations.items() if meta.category == LocationCategory.GOAL
    )
    goal_location = KirbyAmLocation(
        1,
        goal_meta.label,
        goal_meta.location_id,
        None,
        key=goal_key,
        default_item_code=goal_meta.default_item,
    )

    class _DummyMultiWorld:
        def __init__(self, locations):
            self._locations = locations
            self.itempool = []

        def get_locations(self, player):
            return self._locations

        def get_player_name(self, player):
            return "KirbyAM-Test"

    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.player = 1
    world.multiworld = _DummyMultiWorld([goal_location])
    world.options = SimpleNamespace(
        shards=SimpleNamespace(value=RandomizeShards.option_completely_random)
    )

    world.create_items()

    assert goal_location.item is not None
    assert goal_location.item.code is None
    assert goal_location.address is None


def test_vanilla_shards_are_locked_to_boss_defeats() -> None:
    world, locations = _build_world_for_create_items(RandomizeShards.option_vanilla)

    world.create_items()

    boss_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.BOSS_DEFEAT]
    chest_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.MAJOR_CHEST]

    key_to_boss_location = {loc.key: loc for loc in boss_locations}
    ordered_boss_locations = [key_to_boss_location[key] for key in KirbyAmWorld._BOSS_DEFEAT_KEY_ORDER]
    locked_boss_shards = [loc.item.name for loc in ordered_boss_locations if loc.item is not None]
    assert len(locked_boss_shards) == 8
    assert all("Mirror Shard" in item_name for item_name in locked_boss_shards)
    assert locked_boss_shards == list(KirbyAmWorld._SHARD_ITEM_LABEL_ORDER)
    assert all(loc.item is None for loc in chest_locations)
    _major_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MAJOR_CHEST)
    _vitality_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.VITALITY_CHEST)
    _sound_player_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.SOUND_PLAYER_CHEST)
    _minor_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MINOR_CHEST)
    _hub_switch_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.HUB_SWITCH)
    _room_sanity_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.ROOM_SANITY)
    _expected_pool_size = (
        _major_chest_count
        + _vitality_chest_count
        + _sound_player_chest_count
        + _minor_chest_count
        + _hub_switch_count
        + _room_sanity_count
    )
    assert len(world.multiworld.itempool) == _expected_pool_size
    assert all("Mirror Shard" not in item.name for item in world.multiworld.itempool)


def test_completely_random_pool_contains_all_shards_but_bosses_are_unlocked() -> None:
    world, locations = _build_world_for_create_items(RandomizeShards.option_completely_random)

    world.create_items()

    boss_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.BOSS_DEFEAT]
    assert all(loc.item is None for loc in boss_locations)

    shard_items = [item for item in world.multiworld.itempool if "Shards" in item.tags]
    _boss_defeat_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.BOSS_DEFEAT)
    _major_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MAJOR_CHEST)
    _vitality_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.VITALITY_CHEST)
    _sound_player_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.SOUND_PLAYER_CHEST)
    _minor_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MINOR_CHEST)
    _hub_switch_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.HUB_SWITCH)
    _room_sanity_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.ROOM_SANITY)
    _shard_item_count = len(KirbyAmWorld._SHARD_ITEM_LABEL_ORDER)
    _open_non_goal_location_count = (
        _boss_defeat_count
        + _major_chest_count
        + _vitality_chest_count
        + _sound_player_chest_count
        + _minor_chest_count
        + _hub_switch_count
        + _room_sanity_count
    )
    _expected_pool_size = _open_non_goal_location_count
    assert len(world.multiworld.itempool) == _expected_pool_size
    assert len(shard_items) == _shard_item_count


def test_completely_random_pool_contains_each_non_filler_item_exactly_once() -> None:
    world, _locations = _build_world_for_create_items(RandomizeShards.option_completely_random)

    world.create_items()

    expected_non_filler_codes = {
        item.item_id
        for item in data.items.values()
        if item.classification not in (ItemClassification.filler, ItemClassification.trap)
    }
    pool_codes = [item.code for item in world.multiworld.itempool if item.code is not None]
    pool_non_filler_codes = [code for code in pool_codes if get_item_classification(code) != ItemClassification.filler]

    assert set(pool_non_filler_codes) == expected_non_filler_codes
    assert len(pool_non_filler_codes) == len(expected_non_filler_codes)
    assert len(pool_codes) >= len(expected_non_filler_codes)


def test_vanilla_pool_contains_each_non_shard_non_filler_item_exactly_once() -> None:
    world, _locations = _build_world_for_create_items(RandomizeShards.option_vanilla)

    world.create_items()

    shard_codes = {
        item.item_id for item in data.items.values() if "Shards" in item.tags
    }
    expected_non_filler_codes = {
        item.item_id
        for item in data.items.values()
        if item.classification not in (ItemClassification.filler, ItemClassification.trap) and item.item_id not in shard_codes
    }
    pool_codes = [item.code for item in world.multiworld.itempool if item.code is not None]
    pool_non_filler_codes = [code for code in pool_codes if get_item_classification(code) != ItemClassification.filler]

    assert set(pool_non_filler_codes) == expected_non_filler_codes
    assert len(pool_non_filler_codes) == len(expected_non_filler_codes)
    assert shard_codes.isdisjoint(set(pool_codes)), "Vanilla shard mode should not randomize shard items"


def test_create_items_fails_when_non_filler_count_exceeds_open_locations() -> None:
    boss_only_locations = [
        KirbyAmLocation(
            1,
            meta.label,
            meta.location_id,
            None,
            key=key,
            default_item_code=meta.default_item,
        )
        for key, meta in data.locations.items()
        if meta.category == LocationCategory.BOSS_DEFEAT
    ]

    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.player = 1
    world.random = random.Random(7)
    world.multiworld = _DummyMultiWorld(boss_only_locations)
    world.options = SimpleNamespace(
        shards=SimpleNamespace(
            value=RandomizeShards.option_completely_random,
            current_key="completely_random",
        )
    )

    with pytest.raises(ValueError, match="non-filler item count"):
        world.create_items()


# ── One-Hit Mode item pool tests ────────────────────────────────────────────


def _vitality_item_codes() -> set[int]:
    return {item.item_id for item in data.items.values() if "Vitality" in item.tags}


def test_one_hit_mode_vanilla_includes_all_vitality_items() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_off,
    )
    world.create_items()

    vitality_codes = _vitality_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert vitality_codes.issubset(pool_codes), (
        "Vanilla one-hit mode should not remove vitality counter items from the pool"
    )


def test_one_hit_mode_include_vitality_counters_includes_all_vitality_items() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_include_vitality_counters,
    )
    world.create_items()

    vitality_codes = _vitality_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert vitality_codes.issubset(pool_codes), (
        "include_vitality_counters mode should keep all vitality counter items in the pool"
    )


def test_vitality_items_appear_exactly_once_in_vanilla_pool() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_off,
    )
    world.create_items()

    vitality_codes = _vitality_item_codes()
    pool_codes = [item.code for item in world.multiworld.itempool if item.code is not None]
    counts = Counter(code for code in pool_codes if code in vitality_codes)

    assert counts, "Expected vitality counters in vanilla pool"
    assert all(count == 1 for count in counts.values()), (
        f"Vitality counter items must be unique in pool, got counts={dict(counts)}"
    )
    assert counts.keys() == vitality_codes, (
        "Vanilla pool must contain each vitality counter exactly once"
    )


def test_vitality_items_appear_exactly_once_in_include_mode_pool() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_include_vitality_counters,
    )
    world.create_items()

    vitality_codes = _vitality_item_codes()
    pool_codes = [item.code for item in world.multiworld.itempool if item.code is not None]
    counts = Counter(code for code in pool_codes if code in vitality_codes)

    assert counts, "Expected vitality counters in include_vitality_counters pool"
    assert all(count == 1 for count in counts.values()), (
        f"Vitality counter items must be unique in pool, got counts={dict(counts)}"
    )
    assert counts.keys() == vitality_codes, (
        "include_vitality_counters pool must contain each vitality counter exactly once"
    )


def test_one_hit_mode_exclude_vitality_counters_removes_vitality_items() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_exclude_vitality_counters,
    )
    world.create_items()

    vitality_codes = _vitality_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert vitality_codes.isdisjoint(pool_codes), (
        "exclude_vitality_counters mode should have no vitality counter items in the pool"
    )


def test_one_hit_mode_exclude_vitality_counters_pool_size_unchanged() -> None:
    """Total pool size should not change; filler fills the slots vacated by vitality items."""
    world_vanilla, _locs_v = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_off,
    )
    world_vanilla.create_items()

    world_exclude, _locs_e = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_exclude_vitality_counters,
    )
    world_exclude.create_items()

    assert len(world_exclude.multiworld.itempool) == len(world_vanilla.multiworld.itempool), (
        "Pool size should be the same in exclude_vitality_counters mode as in vanilla"
    )


def test_one_hit_mode_exclude_vitality_counters_vitality_chest_locations_exist() -> None:
    """Vitality Chest locations remain in the pool; pool has enough items to fill them (with filler)."""
    world, locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        one_hit_mode=OneHitMode.option_exclude_vitality_counters,
    )
    world.create_items()

    vitality_locs = [
        loc for loc in locations
        if data.locations[loc.key].category == LocationCategory.VITALITY_CHEST
    ]
    assert len(vitality_locs) == 4, "Expected 4 vitality chest locations"

    # All vitality chest locations are open (no locked item); the pool covers them with filler.
    for loc in vitality_locs:
        assert loc.item is None, (
            f"Vitality chest location {loc.name} should be open (no locked item) in exclude mode"
        )

    # The pool size equals the number of open locations, confirming filler fills the vitality slots.
    open_count = sum(
        1 for loc in locations
        if data.locations.get(loc.key) is not None
        and data.locations[loc.key].category != LocationCategory.GOAL
        and loc.item is None
    )
    assert len(world.multiworld.itempool) == open_count, (
        "Pool size should equal the number of open non-goal locations"
    )


# ── Start-With-All-Maps item pool tests ─────────────────────────────────────


def _map_item_codes() -> set[int]:
    return {item.item_id for item in data.items.values() if "Maps" in item.tags}


def test_start_with_all_maps_excludes_map_items_from_pool() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        start_with_all_maps=1,
    )
    world.create_items()

    map_codes = _map_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert map_codes.isdisjoint(pool_codes), (
        "start_with_all_maps mode should have no map items in the randomized pool"
    )


def test_start_with_all_maps_pool_size_unchanged() -> None:
    """Total pool size should not change; filler fills the slots vacated by map items."""
    world_baseline, _locs_b = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        start_with_all_maps=0,
    )
    world_baseline.create_items()

    world_maps, _locs_m = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        start_with_all_maps=1,
    )
    world_maps.create_items()

    assert len(world_maps.multiworld.itempool) == len(world_baseline.multiworld.itempool), (
        "Pool size should be the same with start_with_all_maps enabled as without"
    )


def test_start_with_all_maps_vanilla_shards_excludes_map_items_from_pool() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_vanilla,
        start_with_all_maps=1,
    )
    world.create_items()

    map_codes = _map_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert map_codes.isdisjoint(pool_codes), (
        "start_with_all_maps mode should have no map items in the pool (vanilla shard mode)"
    )


def test_start_with_all_maps_off_includes_all_map_items_in_pool() -> None:
    world, _locations = _build_world_for_create_items(
        RandomizeShards.option_completely_random,
        start_with_all_maps=0,
    )
    world.create_items()

    map_codes = _map_item_codes()
    pool_codes = {item.code for item in world.multiworld.itempool if item.code is not None}
    assert map_codes.issubset(pool_codes), (
        "When start_with_all_maps is off, all map items should remain in the pool"
    )

