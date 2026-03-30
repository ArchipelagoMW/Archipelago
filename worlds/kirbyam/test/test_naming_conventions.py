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
        "Rainbow Route 1-9 - Big Chest",
        "Moonlight Mansion 2-1 - Big Chest",
        "Cabbage Cavern 3-7 - Big Chest",
        "Mustard Mountain 4-25 - Big Chest",
        "Carrot Castle 5-15 - Big Chest",
        "Olive Ocean 6-15 - Big Chest",
        "Peppermint Palace 7-4 - Big Chest",
        "Radish Ruins 8-29 - Big Chest",
        "Candy Constellation 9-18 - Big Chest",
        "Carrot Castle 5-23 - Big Chest",
        "Olive Ocean 6-21 - Big Chest",
        "Radish Ruins 8-4 - Big Chest",
        "Candy Constellation 9-8 - Big Chest",
        "Candy Constellation 9-4 - Big Chest",
    }
    actual = {
        location.label
        for location in data.locations.values()
        if location.category.name == "MAJOR_CHEST"
    }
    assert actual == expected