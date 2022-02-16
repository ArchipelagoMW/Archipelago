import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestBase(unittest.TestCase):
    def testCreateItem(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            proxy_world = world_type(None, 0)  # this is identical to MultiServer.py creating worlds
            for item_name in world_type.item_name_to_id:
                with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                    item = proxy_world.create_item(item_name)
                    self.assertEqual(item.name, item_name)
