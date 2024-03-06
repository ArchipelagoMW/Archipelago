import unittest

from BaseClasses import MultiWorld
from Options import ItemLinks
from worlds.AutoWorld import AutoWorldRegister


class TestOptions(unittest.TestCase):
    def test_options_have_doc_string(self):
        """Test that submitted options have their own specified docstring"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        self.assertTrue(option.__doc__)

    def test_options_are_not_set_by_world(self):
        """Test that options attribute is not already set"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                self.assertFalse(hasattr(world_type, "options"),
                                 f"Unexpected assignment to {world_type.__name__}.options!")

    def test_item_links_resolve(self):
        """Test item link option resolves correctly."""
        multiworld = MultiWorld(2)
        multiworld.game = {1: "Game 1", 2: "Game 2"}
        multiworld.player_name = {1: "Player 1", 2: "Player 2"}
        multiworld.set_seed()
        item_link_group = [{
            "name": "ItemLinkTest",
            "item_pool": ["Everything"],
            "link_replacement": False,
            "replacement_item": None,
        }]
        item_links = {1: ItemLinks.from_any(item_link_group), 2: ItemLinks.from_any(item_link_group)}
        for link in item_links.values():
            self.assertEqual(link.value[0], item_link_group[0])
