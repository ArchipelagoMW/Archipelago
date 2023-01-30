from ..items import load_item_csv
from ..locations import load_location_csv


def test_items_integrity():
    items = load_item_csv()

    for item in items:
        assert item.code_without_offset is not None, 'Some item do not have an id. Run the script `update_data.py` to generate them.'


def test_locations_integrity():
    locations = load_location_csv()

    for location in locations:
        assert location.code_without_offset is not None, 'Some location do not have an id. Run the script `update_data.py` to generate them.'
