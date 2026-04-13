"""Regression tests for KirbyAM user-facing item and location naming."""

from ..data import data


def test_map_items_use_area_then_map_naming() -> None:
    expected = {
        "Rainbow Route - Map",
        "Mustard Mountain - Map",
        "Moonlight Mansion - Map",
        "Candy Constellation - Map",
        "Olive Ocean - Map",
        "Peppermint Palace - Map",
        "Cabbage Cavern - Map",
        "Carrot Castle - Map",
        "Radish Ruins - Map",
    }
    actual = {
        item.label
        for item in data.items.values()
        if "Maps" in item.tags
    }
    assert actual == expected


def test_vitality_items_use_area_specific_names() -> None:
    expected = {
        "Carrot Castle - Vitality Counter",
        "Olive Ocean - Vitality Counter",
        "Radish Ruins - Vitality Counter",
        "Candy Constellation - Vitality Counter",
    }
    actual = {
        item.label
        for item in data.items.values()
        if "Vitality" in item.tags
    }
    assert actual == expected


def test_physical_big_chest_locations_hide_contents_in_labels() -> None:
    expected = {
        "Rainbow Route Map - Big Chest",
        "Moonlight Mansion Map - Big Chest",
        "Cabbage Cavern Map - Big Chest",
        "Mustard Mountain Map - Big Chest",
        "Carrot Castle Map - Big Chest",
        "Olive Ocean Map - Big Chest",
        "Peppermint Palace Map - Big Chest",
        "Radish Ruins Map - Big Chest",
        "Candy Constellation Map - Big Chest",
        "Carrot Castle Vitality - Big Chest",
        "Olive Ocean Vitality - Big Chest",
        "Radish Ruins Vitality - Big Chest",
        "Candy Constellation Vitality - Big Chest",
        "Candy Constellation Sound Player - Big Chest",
    }
    actual = {
        location.label
        for location in data.locations.values()
        if location.category.name in {"MAJOR_CHEST", "VITALITY_CHEST", "SOUND_PLAYER_CHEST"}
    }
    assert actual == expected