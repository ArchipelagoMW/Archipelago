
from BaseClasses import MultiWorld, Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from .Items import item_table, create_itempool, create_item, event_item_pairs, sly_episodes
from .Locations import get_location_names
from .Options import Sly1Options
from .Regions import create_regions
from .Types import EpisodeType, episode_type_to_name, Sly1Item
from .Rules import set_rules

class Sly1Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Sly Cooper and the Thievius Raccoonus for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nep"]
    )]

class Sly1World(World):
    """
    Sly Cooper and the Thievius Raccoonus is a action stealth game.
    Avenge your father and take back the pages from the fiendish five.
    """

    game = "Sly Cooper and the Thievius Raccoonus"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = Sly1Options
    options = Sly1Options
    web = Sly1Web()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        
    def generate_early(self):
        starting_episode = (episode_type_to_name[EpisodeType(self.options.StartingEpisode)])
        self.multiworld.push_precollected(self.create_item(starting_episode))

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

        for event, item in event_item_pairs.items():
            event_item = Sly1Item(item, ItemClassification.progression, None, self.player)
            self.multiworld.get_location(event, self.player).place_locked_item(event_item)

    def set_rules(self):
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)