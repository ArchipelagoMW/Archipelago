from typing import Dict

from . import RLTestBase
from ..Items import item_table
from ..Locations import location_table


class UniqueTest(RLTestBase):
    @staticmethod
    def test_item_ids_are_all_unique():
        item_ids: Dict[int, str] = {}
        for name, data in item_table.items():
            assert data.code not in item_ids.keys(), f"'{name}': {data.code}, is not unique. " \
                                                     f"'{item_ids[data.code]}' also has this identifier."
            item_ids[data.code] = name

    @staticmethod
    def test_location_ids_are_all_unique():
        location_ids: Dict[int, str] = {}
        for name, data in location_table.items():
            assert data.code not in location_ids.keys(), f"'{name}': {data.code}, is not unique. " \
                                                         f"'{location_ids[data.code]}' also has this identifier."
            location_ids[data.code] = name
