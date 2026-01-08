
from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import item_table, item_groups, TwistyCubeItem as TwistyCubeItem
from .Locations import TwistyCubeLocation, location_table
from .Options import TwistyCubeOptions
from .Puzzle import CubePuzzle


from worlds.LauncherComponents import (
    Component,
    components,
    Type as component_type,
)


class TwistyCubeWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Rubik's Cube. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class TwistyCubeWorld(World):

    game: str = "Twisty Cube"
    options_dataclass = TwistyCubeOptions

    web = TwistyCubeWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}
        
    item_name_groups = item_groups

    side_permutation: dict[str, str]

    puzzle: CubePuzzle
    
    ap_world_version = "0.0.2"

    def _get_twistycube_data(self):
        return {
            "seed_name": self.multiworld.seed,
            "color_permutation": self.color_permutation,
            "ap_world_version": self.ap_world_version
        }

    def generate_early(self):
        self.puzzle = CubePuzzle(self.options.size_of_cube.value, self.random)

    def create_items(self):
        self.pool_contents = []
        for item in self.puzzle.get_items():
            self.pool_contents.append(item)

        for _ in range(self.options.starting_stickers.value):
            name = self.random.choice(self.pool_contents)
            self.multiworld.push_precollected(self.create_item(name))
            self.pool_contents.remove(name)
        self.multiworld.itempool += [self.create_item(name) for name in self.pool_contents]
                

    def create_regions(self):        
        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)
        
        self.color_permutation = self.puzzle.get_color_permutation(bool(self.options.randomize_color_layout.value))
        
        all_locations = []
        for location, requirements in self.puzzle.get_location_table(self.options.starting_stickers.value).items():
            all_locations.append(
                TwistyCubeLocation(self.player, location, location_table[location].id, requirements, board)
            )

        board.locations = all_locations
        
        for loc in board.locations:
            loc.access_rule = lambda state, count=loc.reqs: state.has("stickers", self.player, count)

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = self.puzzle.get_goal_location()
        self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        

    def get_filler_item_name(self) -> str:
        return "filler"

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = TwistyCubeItem(name, item_data.classification, item_data.code, self.player)
        return item
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and "Sticker" in item.name:
            state.prog_items[item.player]["stickers"] += 1
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and "Sticker" in item.name:
            state.prog_items[item.player]["stickers"] -= 1
        return change

    def fill_slot_data(self):
        """
        make slot data, which consists of twistycube_data, options, and some other variables.
        """
        slot_data = self._get_twistycube_data()
        twistycube_options = self.options.as_dict(
            "size_of_cube",
        )
        slot_data = {**slot_data, **twistycube_options}  # combine the two
        return slot_data

    def open_page(url):
        import webbrowser
        import urllib.parse

        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme != "archipelago":
            raise ValueError("URL must be an Archipelago URL")

        query_parameters = {
            "hostport": f"{parsed_url.hostname}:{parsed_url.port}",
            "name": parsed_url.username
        }
        if parsed_url.password is not None:
            query_parameters["password"] = parsed_url.password
        
        target_url = f"http://cube-ap.netlify.app/?{urllib.parse.urlencode(query_parameters)}"
        webbrowser.open(target_url)

    components.append(
        Component(
            "Twisty Cube AutoLaunch",
            func=open_page,
            component_type=component_type.HIDDEN,
            supports_uri=True,
            game_name="Twisty Cube"
        )
    )