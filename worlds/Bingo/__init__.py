from typing import List, Dict, Any

from BaseClasses import Region, Item, ItemClassification, Entrance, Tutorial, MultiWorld
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Items import BingoItem, item_data_table, item_table
from .Locations import BingoLocation, location_data_table, location_table
from .Options import BingoOptions, BingoStartHints
from .Regions import region_data_table
from .Rules import get_bingo_rule, special_rule, can_goal


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="APBingoClient")


components.append(Component(
    "APBingo Client",
    "APBingoClient",
    func=launch_client,
    component_type=Type.CLIENT
))


class BingoWorld(World):
    """Randomized Bingo!"""

    game = "APBingo"
    options: BingoOptions
    options_dataclass = BingoOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    board_locations = []
    board_size = 0
    required_bingos = 22

    def create_item(self, name: str) -> BingoItem:
        return BingoItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[BingoItem] = []

        squares = self.get_available_items()

        for name, item in item_data_table.items():
            if name in squares:
                item_pool.append(self.create_item(name))
        self.options.non_local_items.value = set(squares)
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)

            available_locs = self.get_available_locations(True)

            filtered_locations = {
                location: data.address
                for location, data in location_data_table.items()
                if location in available_locs and data.region == region_name
            }
            region.add_locations(filtered_locations, BingoLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

    def set_rules(self) -> None:

        bingo_names = self.get_available_locations(False)

        for bingo in bingo_names:
            self.get_location(bingo).access_rule = get_bingo_rule(bingo, self)
            self.get_location(bingo).item_rule = lambda item: item.game != "APBingo"

        all_keys = self.get_available_items()
        self.get_location("Bingo (ALL)").access_rule = special_rule(self, all_keys)
        self.get_location("Bingo (ALL)").item_rule = lambda item: item.game != "APBingo"

        # Don't allow incorrect values for required bingos
        self.required_bingos = self.options.required_bingos.value
        max_possible_bingos = (2 * self.board_size + 2)
        if self.required_bingos > max_possible_bingos:
            self.required_bingos = max_possible_bingos

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: can_goal(state, self.player, self.required_bingos, self.board_size)

    def pre_fill(self) -> None:
        if self.options.bingo_balance == 0:
            return

        num_items:int = len(self.get_available_items())*self.options.bingo_balance//100
        items_to_distribute = self.get_available_items()
        self.random.shuffle(items_to_distribute)
        items_to_distribute = items_to_distribute[:num_items]
        players = [i for i in self.multiworld.player_ids if self.multiworld.game[i] != self.game]

        player_locations = [self.multiworld.get_unfilled_locations(p) for p in players]
        for locations in player_locations:
            self.random.shuffle(locations)

        while len(items_to_distribute) > 0:
            #Round robin placement
            for candidates in player_locations:
                item = self.create_item(items_to_distribute[-1])
                for location in reversed(candidates):
                    if location.address is not None and location.item is None and location.can_fill(self.multiworld.state,item,check_access=False):
                        self.multiworld.push_item(location,item,False)
                        location.locked = True
                        candidates.remove(location)
                        self.multiworld.itempool.remove(item)
                        items_to_distribute.pop()
                        break
                else:
                    #Couldn't place at a single location, this game can't accept any more items from us
                    candidates.clear()
                if len(items_to_distribute) == 0:
                    # Placed all items, break out
                    break
            player_locations = list(filter(lambda l: len(l) > 0,player_locations))
            if len(player_locations) == 0:
                # No more locations left, need to abort the loop
                break

    def get_available_items(self):
        return [f"{chr(row)}{col}" for row in range(ord('A'), ord('A') + self.options.board_size.value) for col in range(1, self.options.board_size.value + 1)]

    def get_available_locations(self, include_all):

        # Define the board size
        self.board_size = self.options.board_size.value  # Change this to any integer for different board sizes

        bingo_names = []

        # Required locations should match the board size
        required_locations = (self.board_size * self.board_size) - 1

        suffix = 0  # Start with suffix 0
        while len(bingo_names) < required_locations:
            # Generate horizontal Bingo names for the current suffix
            for row in range(ord('A'), ord('A') + self.board_size):
                if len(bingo_names) < required_locations:  # Check before appending
                    bingo_names.append(f"Bingo ({chr(row)}1-{chr(row)}{self.board_size})-{suffix}")

            # Generate vertical Bingo names for the current suffix
            for col in range(1, self.board_size + 1):
                if len(bingo_names) < required_locations:  # Check before appending
                    bingo_names.append(f"Bingo (A{col}-{chr(ord('A') + self.board_size - 1)}{col})-{suffix}")

            # Generate diagonal Bingo names for the current suffix
            if len(bingo_names) < required_locations:  # Check before appending
                bingo_names.append(f"Bingo (A1-{chr(ord('A') + self.board_size - 1)}{self.board_size})-{suffix}")
            if len(bingo_names) < required_locations:  # Check before appending
                bingo_names.append(f"Bingo ({chr(ord('A') + self.board_size - 1)}1-A{self.board_size})-{suffix}")

            suffix += 1  # Increment suffix for the next round

        # Include the ALL bingo if specified and we haven't filled the required locations
        if include_all:
            bingo_names.append("Bingo (ALL)")

        return bingo_names

    def find_locations(self):

        self.board_locations = []
        squares = self.get_available_items()

        for square in squares:
            board_location = self.multiworld.find_item(square, self.player)
            self.board_locations.append(str(board_location))

    def fill_slot_data(self) -> Dict[str, Any]:

        self.find_locations()
        if bool(self.options.auto_hints):
            self.options.start_hints = BingoStartHints(self.get_available_items())

        return {
            "requiredBingoCount": self.required_bingos,
            "boardLocations": self.board_locations,
            "boardSize": self.options.board_size.value,
            "customBoard": str(self.options.board_color.value),
            "customSquare": str(self.options.square_color.value),
            "customHLSquare": str(self.options.hl_square_color.value),
            "customText": str(self.options.text_color.value),
        }
