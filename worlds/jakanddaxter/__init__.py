from BaseClasses import Item, ItemClassification, Tutorial
from .GameID import jak1_id, jak1_name
from .JakAndDaxterOptions import JakAndDaxterOptions
from .Items import JakAndDaxterItem
from .Locations import JakAndDaxterLocation, location_table as item_table
from .locs import CellLocations as Cells, ScoutLocations as Scouts, OrbLocations as Orbs
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld
from ..LauncherComponents import components, Component, launch_subprocess, Type


class JakAndDaxterWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelaGOAL (Archipelago on OpenGOAL).",
        "English",
        "setup_en.md",
        "setup/en",
        ["markustulliuscicero"]
    )

    tutorials = [setup_en]


class JakAndDaxterWorld(World):
    """
    Jak and Daxter: The Precursor Legacy is a 2001 action platformer developed by Naughty Dog
    for the PlayStation 2. The game follows the eponymous protagonists, a young boy named Jak
    and his friend Daxter, who has been transformed into an "ottsel." With the help of Samos
    the Sage of Green Eco and his daughter Keira, the pair travel north in search of a cure for Daxter,
    discovering artifacts created by an ancient race known as the Precursors along the way. When the
    rogue sages Gol and Maia Acheron plan to flood the world with Dark Eco, they must stop their evil plan
    and save the world.
    """
    # ID, name, version
    game = jak1_name
    data_version = 1
    required_client_version = (0, 4, 5)

    # Options
    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    # Web world
    web = JakAndDaxterWebWorld()

    # Items and Locations
    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    # Remember, the game ID and various offsets for each item type have already been calculated.
    item_name_to_id = {item_table[k]: k for k in item_table}
    location_name_to_id = {item_table[k]: k for k in item_table}
    item_name_groups = {
        "Power Cell": {item_table[k]: k for k in item_table
                       if k in range(jak1_id, jak1_id + Scouts.fly_offset)},
        "Scout Fly": {item_table[k]: k for k in item_table
                      if k in range(jak1_id + Scouts.fly_offset, jak1_id + Orbs.orb_offset)}
        # "Precursor Orb": {}  # TODO
    }

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_items(self):
        self.multiworld.itempool += [self.create_item(item_table[k]) for k in item_table]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        if item_id in range(jak1_id, jak1_id + Scouts.fly_offset):
            # Power Cell
            classification = ItemClassification.progression_skip_balancing
        elif item_id in range(jak1_id + Scouts.fly_offset, jak1_id + Orbs.orb_offset):
            # Scout Fly
            classification = ItemClassification.progression_skip_balancing
        elif item_id > jak1_id + Orbs.orb_offset:
            # Precursor Orb
            classification = ItemClassification.filler  # TODO
        else:
            classification = ItemClassification.filler

        item = JakAndDaxterItem(name, classification, item_id, self.player)
        return item


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="JakAndDaxterClient")


components.append(Component("Jak and Daxter Client",
                            "JakAndDaxterClient",
                            func=launch_client,
                            component_type=Type.CLIENT))
