"""
Archipelago init file for Pokepark 1
"""
from BaseClasses import ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import components, Component, launch_subprocess
from .items import FRIENDSHIP_ITEMS, PokeparkItem, UNLOCK_ITEMS, BERRIES, ALL_ITEMS_TABLE, PRISM_ITEM, POWERS, \
    REGION_UNLOCK
from .locations import ALL_LOCATIONS_TABLE
from .logic import REGIONS
from .options import PokeparkOptions


class PokeparkWebWorld(WebWorld):
    theme = "jungle"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Pokepark Randomizer software on your computer."
            "This guide covers single-player, multiworld, and related software.",
            "English",
            "pokepark_1_en.md",
            "pokepark_1/en",
            [""]
    )]
    options_presets = {
        "Default": {
            "disable_block_events": True
        }
    }

class PokeparkWorld(World):
    """
    The first Pokepark game featuring 3D Gameplay controlling Pokemon. Lot of Minigames in the mission to save the Pokepark through the collection of Prism Shards.
    """
    game = "PokéPark"

    options_dataclass = PokeparkOptions
    options = PokeparkOptions
    web = PokeparkWebWorld()

    item_name_to_id = ALL_ITEMS_TABLE
    location_name_to_id = ALL_LOCATIONS_TABLE
    location_name_groups = {
        "Friendship Locations": [f"{region.display} - {friendship.name}" for region in REGIONS for friendship in
                                 region.friendship_locations],
        "Unlock Locations": [f"{region.display} - {unlock.name}" for region in REGIONS for unlock in
                             region.unlock_location],
        "Minigame Locations": [f"{region.display} - {minigame.name}" for region in REGIONS for minigame in
                               region.minigame_location],
        "Quest Locations": [f"{region.display} - {ability.name}" for region in REGIONS for ability in
                            region.quest_locations]
    }
    item_name_groups = {
        "Friendship Items": FRIENDSHIP_ITEMS.keys(),
        "Unlock Items": UNLOCK_ITEMS.keys(),
        "Currency Items": BERRIES.keys(),
        "Prisma Items": PRISM_ITEM.keys(),
        "Ability Items": POWERS.keys(),
        "Entrance Items": REGION_UNLOCK.keys()
    }

    data_version = 1
    def create_regions(self):
        from .regions import create_regions
        create_regions(self)

    def create_items(self):
        pool = [self.create_item(name) for name in FRIENDSHIP_ITEMS.keys()]
        pool += [self.create_item(name) for name in UNLOCK_ITEMS.keys()]
        pool += [self.create_item(name) for name in PRISM_ITEM.keys()]
        pool += [self.create_item(name) for name in REGION_UNLOCK.keys()]
        pool += [self.create_item(name) for _ in range(3) for name in POWERS.keys()]

        remaining_slots = len(ALL_LOCATIONS_TABLE) - len(pool)
        berry_items = list(BERRIES.keys())
        for i in range(remaining_slots):
            berry_name = berry_items[i % len(berry_items)]
            pool.append(self.create_item(berry_name))

        self.multiworld.itempool += pool
        if self.options.disable_block_events:
            print(self.options.disable_block_events.display_name)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, name: str):
        if name in FRIENDSHIP_ITEMS or name in UNLOCK_ITEMS or name in PRISM_ITEM or name in REGION_UNLOCK:
            classification = ItemClassification.progression
        elif name in POWERS:
            classification = ItemClassification.useful
        elif name in BERRIES:
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.filler

        return PokeparkItem(name, classification, ALL_ITEMS_TABLE[name], self.player)

def launch_client():
     from .PokeparkClient import main
     launch_subprocess(main, name="Pokepark client")

def add_client_to_launcher() -> None:
    version = "0.2.0"
    found = False
    for c in components:
        if c.display_name == "Pokepark Client":
            found = True
            if getattr(c, "version", 0) < version:
                c.version = version
                c.func = launch_client
                return
    if not found:
        components.append(Component("Pokepark Client", "PokeparkClient",
                                    func=launch_client))


add_client_to_launcher()