from BaseClasses import ItemClassification

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
