import random
from pathlib import Path

from BaseClasses import ItemClassification

from .. import KirbyAmWorld
from ..data import LocationCategory, data


def test_useful_item_catalog_includes_map_and_vitality() -> None:
    useful_items = [item for item in data.items.values() if item.classification & ItemClassification.useful]

    assert useful_items, "Expected at least one useful item in KirbyAM item data"
    map_items = [item for item in useful_items if "Map" in item.tags]
    assert map_items, "Expected at least one useful map item"
    assert any("Vitality" in item.tags for item in useful_items), "Expected at least one useful vitality item"
    assert len(map_items) >= 8, "Expected full eight-area map catalog in useful items"


def test_boss_defeat_default_items_use_useful_mix() -> None:
    boss_locations = [loc for loc in data.locations.values() if loc.category == LocationCategory.BOSS_DEFEAT]
    assert boss_locations, "Expected boss defeat locations to exist"

    assigned_items = []
    for location in boss_locations:
        assert location.default_item is not None, f"Expected default_item for {location.name}"
        item = data.items[location.default_item]
        assigned_items.append(item)
        assert item.classification & ItemClassification.useful, (
            f"Expected useful classification for {location.name} default item"
        )

    assert any("Map" in item.tags for item in assigned_items), "Expected map useful items in boss default pool"
    assert any("Vitality" in item.tags for item in assigned_items), "Expected vitality useful items in boss default pool"


def test_filler_catalog_includes_multiple_life_items() -> None:
    filler_items = [item for item in data.items.values() if item.classification == ItemClassification.filler]
    filler_labels = {item.label for item in filler_items}

    assert {"1 Up", "2 Up", "3 Up"}.issubset(filler_labels)
    assert all("Filler" in item.tags for item in filler_items)
    assert all("Life" in item.tags for item in filler_items)


def test_weighted_filler_selection_is_seed_stable() -> None:
    world_a = KirbyAmWorld.__new__(KirbyAmWorld)
    world_a.random = random.Random(41)

    world_b = KirbyAmWorld.__new__(KirbyAmWorld)
    world_b.random = random.Random(41)

    picks_a = [world_a.get_filler_item_name() for _ in range(16)]
    picks_b = [world_b.get_filler_item_name() for _ in range(16)]

    assert picks_a == picks_b
    assert set(picks_a).issubset({"1 Up", "2 Up", "3 Up"})
    assert len(set(picks_a)) >= 2, "Expected weighted filler pool to produce more than one filler item"


def test_payload_supports_weighted_life_fillers() -> None:
    payload_path = Path(__file__).resolve().parents[1] / "kirby_ap_payload" / "ap_payload.c"
    with payload_path.open("r", encoding="utf-8") as payload_file:
        payload = payload_file.read()

    assert "static void ap_grant_lives(uint8_t amount)" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 22u" in payload
    assert "KIRBY_ITEM_ID_BASE_OFFSET + 23u" in payload
    assert "ap_grant_lives(2u)" in payload
    assert "ap_grant_lives(3u)" in payload
