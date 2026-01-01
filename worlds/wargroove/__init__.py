import settings
import string
import typing

from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification
from .Items import item_table, faction_table
from .Locations import location_table
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
from .Options import WargrooveOptions, wargroove_option_groups
from worlds.LauncherComponents import Component, components, Type, launch as launch_component


def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="WargrooveClient", args=args)


components.append(Component("Wargroove Client", game_name="Wargroove", func=launch_client, component_type=Type.CLIENT))


class WargrooveSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Locates the Wargroove root directory on your system.
        This is used by the Wargroove client, so it knows where to send communication files to.
        """
        description = "Wargroove root directory"

    class SaveDirectory(settings.UserFolderPath):
        """
        Locates the Wargroove save file directory on your system.
        This is used by the Wargroove client, so it knows where to send mod and save files to.
        """
        description = "Wargroove save file/appdata directory"

        def browse(self, **kwargs):
            from Utils import messagebox
            messagebox("AppData folder not found",
                       "WargrooveClient couldn't detect a path to the AppData folder.\n"
                       "Please select the folder containing the \"/Chucklefish/Wargroove/\" directories.")
            super().browse(**kwargs)

    root_directory: RootDirectory = RootDirectory("C:/Program Files (x86)/Steam/steamapps/common/Wargroove")
    save_directory: SaveDirectory = SaveDirectory("%APPDATA%")


class WargrooveWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Wargroove for Archipelago.",
        "English",
        "wargroove_en.md",
        "wargroove/en",
        ["Fly Sniper"]
    )]

    option_groups = wargroove_option_groups


class WargrooveWorld(World):
    """
    Command an army, in this retro style turn based strategy game!
    """

    options: WargrooveOptions
    options_dataclass = WargrooveOptions
    settings: typing.ClassVar[WargrooveSettings]
    game = "Wargroove"
    topology_present = True
    web = WargrooveWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            'seed': "".join(self.random.choice(string.ascii_letters) for i in range(16)),
            'income_boost': self.options.income_boost.value,
            'commander_defense_boost': self.options.commander_defense_boost.value,
            'can_choose_commander': self.options.commander_choice.value != 0,
            'commander_choice': self.options.commander_choice.value,
            'player_sacrifice_limit': self.options.player_sacrifice_limit.value,
            'player_summon_limit': self.options.player_summon_limit.value,
            'ai_sacrifice_limit': self.options.ai_sacrifice_limit.value,
            'ai_summon_limit': self.options.ai_summon_limit.value,
            'death_link': self.options.death_link.value,
            'starting_groove_multiplier': 20  # Backwards compatibility in case this ever becomes an option
        }

    def generate_early(self):
        # Selecting a random starting faction
        if self.options.commander_choice.value == 2:
            factions = [faction for faction in faction_table.keys() if faction != "Starter"]
            starting_faction = WargrooveItem(self.multiworld.random.choice(factions) + ' Commanders', self.player)
            self.multiworld.push_precollected(starting_faction)

    def create_items(self):
        # Fill out our pool with our items from the item table
        pool = []
        precollected_item_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        ignore_faction_items = self.options.commander_choice.value == 0
        for name, data in item_table.items():
            if data.code is not None and name not in precollected_item_names and not data.classification == ItemClassification.filler:
                if name.endswith(' Commanders') and ignore_faction_items:
                    continue
                item = WargrooveItem(name, self.player)
                pool.append(item)

        # Matching number of unfilled locations with filler items
        locations_remaining = len(location_table) - 1 - len(pool)
        while locations_remaining > 0:
            # Filling the pool equally with both types of filler items
            pool.append(WargrooveItem("Commander Defense Boost", self.player))
            locations_remaining -= 1
            if locations_remaining > 0:
                pool.append(WargrooveItem("Income Boost", self.player))
                locations_remaining -= 1

        self.multiworld.itempool += pool

        # Placing victory event at final location
        victory = WargrooveItem("Wargroove Victory", self.player)
        self.multiworld.get_location("Wargroove Finale: Victory", self.player).place_locked_item(victory)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Wargroove Victory", self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return WargrooveItem(name, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        return slot_data

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(["Commander Defense Boost", "Income Boost"])


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = WargrooveLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class WargrooveLocation(Location):
    game: str = "Wargroove"


class WargrooveItem(Item):
    game = "Wargroove"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(WargrooveItem, self).__init__(
            name,
            item_data.classification,
            item_data.code,
            player
        )
