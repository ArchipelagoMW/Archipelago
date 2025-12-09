from worlds import network_data_package
from worlds.AutoWorld import WebWorld, World


class TestWebWorld(WebWorld):
    tutorials = []


class TestWorld(World):
    game = "Test Game"
    item_name_to_id = {}
    location_name_to_id = {}
    hidden = True
    web = TestWebWorld()


# add our test world to the data package, so we can test it later
network_data_package["games"][TestWorld.game] = TestWorld.get_data_package_data()
