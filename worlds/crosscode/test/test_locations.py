import typing

from BaseClasses import ItemClassification

from . import CrossCodeTestBase
from ..types.items import CrossCodeItem
from ..types.condition import *
from ..types.locations import CrossCodeLocation

class TestLocationsBase(CrossCodeTestBase):
    def test_has_all_locations_with_metadata_none(self):
        for name, data in self.world_data.locations_dict.items():
            if data.metadata is None:
                self.assertIsNotNone(self.multiworld.get_location(name, self.player))

    def check_location_inclusion_with_metadata(self, key: str, value: typing.Any, included: bool):
        for name, data in self.world_data.locations_dict.items():
            if data.metadata is None:
                continue
            else:
                try:
                    computed_value = data.metadata[key]
                except KeyError:
                    continue

                if computed_value == value:
                    self.assertEqual(
                        self.multiworld.get_location(name, self.player) is not None,
                        included
                    )

class TestQuestRandoLocations(TestLocationsBase):
    options = { "quest_rando": True }

    def test_has_all_quest_rando_locations(self):
        self.check_location_inclusion_with_metadata(
            "quest",
            True,
            True
        )
