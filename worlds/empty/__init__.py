from BaseClasses import Region, ItemClassification
from worlds.AutoWorld import World


class EmptyWorld(World):
    """A minimal world with no locations or items, used for fuzzer testing."""
    game = "Empty"
    topology_present = False
    item_name_to_id: dict = {}
    location_name_to_id: dict = {}

    def create_regions(self):
        self.multiworld.regions.append(Region("Menu", self.player, self.multiworld))

    def create_items(self):
        pass

    def set_rules(self):
        pass
