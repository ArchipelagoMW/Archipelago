import random
from pathlib import Path
from types import SimpleNamespace

from BaseClasses import ItemClassification

from .. import KirbyAmWorld
from ..data import LocationCategory, data
from ..locations import KirbyAmLocation
from ..options import RandomizeShards


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


def _build_world_for_create_items(shard_mode: int) -> tuple[KirbyAmWorld, list[KirbyAmLocation]]:
    locations = _build_fill_locations()
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.player = 1
    world.random = random.Random(7)
    world.multiworld = _DummyMultiWorld(locations)
    world.options = SimpleNamespace(
        shards=SimpleNamespace(value=shard_mode, current_key={
            RandomizeShards.option_vanilla: "vanilla",
            RandomizeShards.option_shuffle: "shuffle",
            RandomizeShards.option_completely_random: "completely_random",
        }[shard_mode])
    )
    return world, locations


def test_useful_item_catalog_includes_map_and_vitality() -> None:
    useful_items = [item for item in data.items.values() if item.classification & ItemClassification.useful]

    assert useful_items, "Expected at least one useful item in KirbyAM item data"
    map_items = [item for item in useful_items if "Map" in item.tags]
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
        assert "Map" in item.tags, f"Expected map default for {location.name}"


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


def test_filler_catalog_includes_multiple_life_items() -> None:
    filler_items = [item for item in data.items.values() if item.classification == ItemClassification.filler]
    filler_labels = {item.label for item in filler_items}

    assert {"1 Up", "2 Up", "3 Up"}.issubset(filler_labels)
    assert all("Filler" in item.tags for item in filler_items)
    assert all("Life" in item.tags for item in filler_items)


def test_active_filler_selection_is_seed_stable() -> None:
    world_a = KirbyAmWorld.__new__(KirbyAmWorld)
    world_a.random = random.Random(41)

    world_b = KirbyAmWorld.__new__(KirbyAmWorld)
    world_b.random = random.Random(41)

    picks_a = [world_a.get_filler_item_name() for _ in range(16)]
    picks_b = [world_b.get_filler_item_name() for _ in range(16)]

    assert picks_a == picks_b
    assert set(picks_a) == {"1 Up"}, "Phase 1 active filler pool contains only 1 Up"
    assert all(pick == "1 Up" for pick in picks_a), "All filler picks should be 1 Up in Phase 1"


def test_filler_selection_respects_active_pool() -> None:
    """Verify that all filler picks are from the configured active filler pool."""
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = random.Random(12345)

    picks = [world.get_filler_item_name() for _ in range(50)]

    # All picks must be from the active pool, regardless of specific pool contents.
    assert all(pick in KirbyAmWorld.ACTIVE_FILLER_POOL for pick in picks), (
        f"Filler picks must be from ACTIVE_FILLER_POOL, got {set(picks)}"
    )


def test_phase1_active_filler_pool_contents() -> None:
    """Phase 1: active filler generation is intentionally limited to 1 Up."""
    assert KirbyAmWorld.ACTIVE_FILLER_POOL == ("1 Up",)


def test_payload_supports_weighted_life_fillers() -> None:
    payload_path = Path(__file__).resolve().parents[1] / "kirby_ap_payload" / "ap_payload.c"
    with payload_path.open("r", encoding="utf-8") as payload_file:
        payload = payload_file.read()

    assert "static void ap_grant_lives(uint8_t amount)" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 22u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 23u" in payload
    assert "ap_grant_lives(2u)" in payload
    assert "ap_grant_lives(3u)" in payload


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


def test_vanilla_shards_are_locked_to_major_chests_not_boss_defeats() -> None:
    world, locations = _build_world_for_create_items(RandomizeShards.option_vanilla)

    world.create_items()

    boss_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.BOSS_DEFEAT]
    chest_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.MAJOR_CHEST]

    assert all(loc.item is None for loc in boss_locations)
    locked_chest_shards = [loc.item.name for loc in chest_locations if loc.item is not None]
    assert len(locked_chest_shards) == 8
    assert all("Mirror Shard" in item_name for item_name in locked_chest_shards)
    _boss_defeat_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.BOSS_DEFEAT)
    _shard_chest_count = len(KirbyAmWorld._SHARD_CHEST_KEY_ORDER)
    _major_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MAJOR_CHEST)
    _vitality_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.VITALITY_CHEST)
    _expected_pool_size = _boss_defeat_count + _vitality_chest_count + (_major_chest_count - _shard_chest_count)
    assert len(world.multiworld.itempool) == _expected_pool_size
    assert all("Mirror Shard" not in item.name for item in world.multiworld.itempool)


def test_completely_random_pool_contains_all_shards_but_bosses_are_unlocked() -> None:
    world, locations = _build_world_for_create_items(RandomizeShards.option_completely_random)

    world.create_items()

    boss_locations = [loc for loc in locations if data.locations[loc.key].category == LocationCategory.BOSS_DEFEAT]
    assert all(loc.item is None for loc in boss_locations)

    shard_items = [item for item in world.multiworld.itempool if "Shard" in item.tags]
    _boss_defeat_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.BOSS_DEFEAT)
    _shard_chest_count = len(KirbyAmWorld._SHARD_CHEST_KEY_ORDER)
    _major_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.MAJOR_CHEST)
    _vitality_chest_count = sum(1 for m in data.locations.values() if m.category == LocationCategory.VITALITY_CHEST)
    _shard_item_count = len(KirbyAmWorld._SHARD_ITEM_LABEL_ORDER)
    _expected_pool_size = _boss_defeat_count + _vitality_chest_count + (_major_chest_count - _shard_chest_count) + _shard_item_count
    assert len(world.multiworld.itempool) == _expected_pool_size
    assert len(shard_items) == _shard_item_count
