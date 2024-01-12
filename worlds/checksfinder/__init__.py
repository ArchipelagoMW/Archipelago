from BaseClasses import Region, Entrance, Item, Tutorial, ItemClassification
from .Items import ChecksFinderItem, item_table, required_items
from .Locations import ChecksFinderAdvancement, advancement_table, exclusion_table
from .Options import checksfinder_options
from .Rules import set_rules, set_completion_rules
from ..AutoWorld import World, WebWorld

client_version = 7


class ChecksFinderWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago ChecksFinder software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mewlif"]
    )]


class ChecksFinderWorld(World):
    """
    ChecksFinder is a game where you avoid mines and find checks inside the board
    with the mines! You win when you get all your items and beat the board!
    """
    game: str = "ChecksFinder"
    option_definitions = checksfinder_options
    topology_present = True
    web = ChecksFinderWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_checksfinder_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.multiworld.is_race,
        }

    def create_items(self):

        # Generate item pool
        itempool = []
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        # Add the map width and height stuff
        itempool += ["Map Width"] * (10-5)
        itempool += ["Map Height"] * (10-5)
        # Add the map bombs
        itempool += ["Map Bombs"] * (20-5)
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self.multiworld, self.player)
        set_completion_rules(self.multiworld, self.player)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)
        board.locations += [ChecksFinderAdvancement(self.player, loc_name, loc_data.id, board)
                            for loc_name, loc_data in advancement_table.items() if loc_data.region == board.name]

        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def fill_slot_data(self):
        slot_data = self._get_checksfinder_data()
        for option_name in checksfinder_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = ChecksFinderItem(name,
                                ItemClassification.progression if item_data.progression else ItemClassification.filler,
                                item_data.code, self.player)
        return item
