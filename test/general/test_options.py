import unittest

from BaseClasses import PlandoOptions
from Options import Choice, ItemLinks, PlandoConnections, PlandoItems, PlandoTexts
from Utils import restricted_dumps
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

    def test_duplicate_options(self) -> None:
        """Tests that a world doesn't reuse the same option class."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=game_name):
                seen_options = set()
                for option in world_type.options_dataclass.type_hints.values():
                    if not option.visibility:
                        continue
                    self.assertFalse(option in seen_options, f"{option} found in assigned options multiple times.")
                    seen_options.add(option)

    def test_item_links_name_groups(self):
        """Tests that item links successfully unfold item_name_groups"""
        item_link_groups = [
            [{
                "name": "ItemLinkGroup",
                "item_pool": ["Everything"],
                "link_replacement": False,
                "replacement_item": None,
            }],
            [{
                "name": "ItemLinkGroup",
                "item_pool": ["Hammer", "Bow"],
                "link_replacement": False,
                "replacement_item": None,
            }]
        ]
        # we really need some sort of test world but generic doesn't have enough items for this
        world = AutoWorldRegister.world_types["A Link to the Past"]
        plando_options = PlandoOptions.from_option_string("bosses")
        item_links = [ItemLinks.from_any(item_link_groups[0]), ItemLinks.from_any(item_link_groups[1])]
        for link in item_links:
            link.verify(world, "tester", plando_options)
            self.assertIn("Hammer", link.value[0]["item_pool"])
            self.assertIn("Bow", link.value[0]["item_pool"])
        
        # TODO test that the group created using these options has the items

    def test_item_links_resolve(self):
        """Test item link option resolves correctly."""
        item_link_group = [{
            "name": "ItemLinkTest",
            "item_pool": ["Everything"],
            "link_replacement": False,
            "replacement_item": None,
        }]
        item_links = {1: ItemLinks.from_any(item_link_group), 2: ItemLinks.from_any(item_link_group)}
        for link in item_links.values():
            self.assertEqual(link.value[0], item_link_group[0])

    def test_pickle_dumps_default(self):
        """Test that default option values can be pickled into database for WebHost generation"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        restricted_dumps(option.from_any(option.default))
                        if issubclass(option, Choice) and option.default in option.name_lookup:
                            restricted_dumps(option.from_text(option.name_lookup[option.default]))
    
    def test_pickle_dumps_plando(self):
        """Test that plando options using containers of a custom type can be pickled"""
        # The base PlandoConnections class can't be instantiated directly, create a subclass and then cast it
        class TestPlandoConnections(PlandoConnections):
            entrances = {"An Entrance"}
            exits = {"An Exit"}
        plando_connection_value = PlandoConnections(
            TestPlandoConnections.from_any([{"entrance": "An Entrance", "exit": "An Exit"}])
        )

        plando_values = {
            "PlandoConnections": plando_connection_value,
            "PlandoItems": PlandoItems.from_any([{"item": "Something", "location": "Somewhere"}]),
            "PlandoTexts": PlandoTexts.from_any([{"text": "Some text.", "at": "text_box"}]),
        }

        for option_key, value in plando_values.items():
            with self.subTest(option=option_key):
                restricted_dumps(value)
