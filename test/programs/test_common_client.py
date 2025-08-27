import unittest

import NetUtils
from CommonClient import CommonContext


class TestCommonContext(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.ctx = CommonContext()
        self.ctx.slot = 1  # Pretend we're player 1 for this.
        self.ctx.slot_info.update({
            1: NetUtils.NetworkSlot("Player 1", "__TestGame1", NetUtils.SlotType.player),
            2: NetUtils.NetworkSlot("Player 2", "__TestGame1", NetUtils.SlotType.player),
            3: NetUtils.NetworkSlot("Player 3", "__TestGame2", NetUtils.SlotType.player),
        })
        self.ctx.consume_players_package([
            NetUtils.NetworkPlayer(1, 1, "Player 1", "Player 1"),
            NetUtils.NetworkPlayer(1, 2, "Player 2", "Player 2"),
            NetUtils.NetworkPlayer(1, 3, "Player 3", "Player 3"),
        ])
        # Using IDs outside the "safe range" for testing purposes only. If this fails unit tests, it's because
        # another world is not following the spec for allowed ID ranges.
        self.ctx.update_data_package({
            "games": {
                "__TestGame1": {
                    "location_name_to_id": {
                        "Test Location 1 - Safe": 2**54 + 1,
                        "Test Location 2 - Duplicate": 2**54 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 1 - Safe": 2**54 + 1,
                        "Test Item 2 - Duplicate": 2**54 + 2,
                    },
                },
                "__TestGame2": {
                    "location_name_to_id": {
                        "Test Location 3 - Duplicate": 2**54 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 3 - Duplicate": 2**54 + 2,
                    },
                },
            },
        })

    async def test_archipelago_datapackage_lookups_exist(self):
        assert "Archipelago" in self.ctx.item_names, "Archipelago item names entry does not exist"
        assert "Archipelago" in self.ctx.location_names, "Archipelago location names entry does not exist"

    async def test_explicit_name_lookups(self):
        # Items
        assert self.ctx.item_names["__TestGame1"][2**54+1] == "Test Item 1 - Safe"
        assert self.ctx.item_names["__TestGame1"][2**54+2] == "Test Item 2 - Duplicate"
        assert self.ctx.item_names["__TestGame1"][2**54+3] == f"Unknown item (ID: {2**54+3})"
        assert self.ctx.item_names["__TestGame1"][-1] == "Nothing"
        assert self.ctx.item_names["__TestGame2"][2**54+1] == f"Unknown item (ID: {2**54+1})"
        assert self.ctx.item_names["__TestGame2"][2**54+2] == "Test Item 3 - Duplicate"
        assert self.ctx.item_names["__TestGame2"][2**54+3] == f"Unknown item (ID: {2**54+3})"
        assert self.ctx.item_names["__TestGame2"][-1] == "Nothing"

        # Locations
        assert self.ctx.location_names["__TestGame1"][2**54+1] == "Test Location 1 - Safe"
        assert self.ctx.location_names["__TestGame1"][2**54+2] == "Test Location 2 - Duplicate"
        assert self.ctx.location_names["__TestGame1"][2**54+3] == f"Unknown location (ID: {2**54+3})"
        assert self.ctx.location_names["__TestGame1"][-1] == "Cheat Console"
        assert self.ctx.location_names["__TestGame2"][2**54+1] == f"Unknown location (ID: {2**54+1})"
        assert self.ctx.location_names["__TestGame2"][2**54+2] == "Test Location 3 - Duplicate"
        assert self.ctx.location_names["__TestGame2"][2**54+3] == f"Unknown location (ID: {2**54+3})"
        assert self.ctx.location_names["__TestGame2"][-1] == "Cheat Console"

    async def test_lookup_helper_functions(self):
        # Checking own slot.
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1) == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2) == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 3) == f"Unknown item (ID: {2 ** 54 + 3})"
        assert self.ctx.item_names.lookup_in_slot(-1) == f"Nothing"

        # Checking others' slots.
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1, 2) == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2, 2) == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 1, 3) == f"Unknown item (ID: {2 ** 54 + 1})"
        assert self.ctx.item_names.lookup_in_slot(2 ** 54 + 2, 3) == "Test Item 3 - Duplicate"

        # Checking by game.
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 1, "__TestGame1") == "Test Item 1 - Safe"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 2, "__TestGame1") == "Test Item 2 - Duplicate"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 3, "__TestGame1") == f"Unknown item (ID: {2 ** 54 + 3})"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 1, "__TestGame2") == f"Unknown item (ID: {2 ** 54 + 1})"
        assert self.ctx.item_names.lookup_in_game(2 ** 54 + 2, "__TestGame2") == "Test Item 3 - Duplicate"

        # Checking with Archipelago ids are valid in any game package.
        assert self.ctx.item_names.lookup_in_slot(-1, 2) == "Nothing"
        assert self.ctx.item_names.lookup_in_slot(-1, 3) == "Nothing"
        assert self.ctx.item_names.lookup_in_game(-1, "__TestGame1") == "Nothing"
        assert self.ctx.item_names.lookup_in_game(-1, "__TestGame2") == "Nothing"
