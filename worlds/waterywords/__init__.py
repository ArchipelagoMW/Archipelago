import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import YachtDiceItem, item_table, group_table, bonus_item_list
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Rules import set_yacht_completion_rules, set_yacht_rules

from .Options import YachtDiceOptions


class YachtDiceWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Yacht Dice. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class YachtDiceWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago,
    where you cast your dice to chart a course for high scores,
    unlocking valuable treasures along the way.
    Discover more dice, extra rolls, multipliers,
    and unlockable categories to navigate the depths of the game.
    Roll your way to victory by reaching the target score!
    """

    game: str = "Watery Words"
    options_dataclass = YachtDiceOptions

    web = YachtDiceWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in all_locations.items()}
    
    item_name_groups = group_table

    ap_world_version = "0.1.0"

    def _get_yachtdice_data(self):
        return {
            # "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "race": self.multiworld.is_race,
        }

    def generate_early(self):
        """
        In generate early, we fill the item-pool, then determine the number of locations, and add filler items.
        """
        self.itempool = []
        self.precollected = []
        
        WW_letters = (
            ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 +
            ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 +
            ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 +
            ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 +
            ['Y'] * 2 + ['Z'] * 1
        )
        self.max_letters = len(WW_letters)

        possible_start_words = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"];
        
        # Choose a word randomly from possible_start_words
        selected_word = self.random.choice(possible_start_words)
        word_letters = [letter.upper() for letter in selected_word]

        # Remove each letter in the selected word from WW_letters
        for letter in word_letters:
            self.precollected.append(letter)
            WW_letters.remove(letter)  # This removes one occurrence of the letter from WW_letters
        
        self.slotdata_letter_packs = []
        if self.options.merge_items:
            self.itempool += ["5 Letters"] * 19
            self.random.shuffle(WW_letters)
            self.slotdata_letter_packs = [WW_letters[i:i+5] for i in range(0, len(WW_letters), 5)]
        else:
            self.itempool += WW_letters
        
        self.precollected += ["Extra turn"] * 1
        self.itempool += ["Extra turn"] * 10
        self.max_turns = 11
        
        bonus_tiles = []        
        for bonuses in bonus_item_list:
            item = self.random.choices(bonuses, weights=[8, 16, 12, 24])[0]
            if item.split(" ", 1)[1] in ["0,0", "0,14", "14,0", "14,14", "7,1", "2,4", "12,4", "2,10", "12,10", "7,13"]:
                self.precollected.append(item)
            else:
                bonus_tiles.append(item)
                
        self.slotdata_bonus_tiles_packs = []
        if self.options.merge_items:
            self.itempool += ["5 Bonus Tiles"] * 9
            self.random.shuffle(bonus_tiles)
            self.slotdata_bonus_tiles_packs = [bonus_tiles[i:i+5] for i in range(0, len(bonus_tiles), 5)]
        else:
            self.itempool += bonus_tiles       
                
        self.max_bonus_tiles = len(bonus_item_list)
        
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

        # max score is the value of the last check. Goal score is the score needed to 'finish' the game
        self.max_score = self.options.score_for_last_check.value
        self.goal_score = min(self.max_score, self.options.score_for_goal.value)
        
        self.multiworld.early_items[self.player]["Extra turn"] = 1
        
        self.number_of_locations = len(self.itempool) + 1


    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]

    def create_regions(self):
        # call the ini_locations function, that generates locations based on the inputs.
        location_table = ini_locations(
            self.goal_score,
            self.max_score,
            self.number_of_locations,
            self.options.merge_items
        )

        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        # add locations to board, one for every location in the location_table
        board.locations = [
            YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name
        ]

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"{self.goal_score} score"
        self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def get_filler_item_name(self) -> str:
        return "A tile but you can't quite read what letter it is, so you decide to throw it away."

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """

        self.logic_factor = max(1.1 * self.max_score / (min(self.max_letters * 2, self.max_turns * 18) * (1 + 0.025 * self.max_bonus_tiles)), 1)
        
        set_yacht_rules(
            self.multiworld,
            self.player,
            self.logic_factor,
            self.max_letters + self.max_turns + self.max_bonus_tiles
        )
        set_yacht_completion_rules(self.multiworld, self.player)
        
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item


    def fill_slot_data(self):
        slot_data = {}
        slot_data["ap_world_version"] = self.ap_world_version
        slot_data["goal_score"] = self.goal_score
        slot_data["logic_factor"] = self.logic_factor
        slot_data["max_items"] = self.max_letters + self.max_turns + self.max_bonus_tiles
        slot_data["letter_packs"] = self.slotdata_letter_packs
        slot_data["bonus_tiles_packs"] = self.slotdata_bonus_tiles_packs
        
        return slot_data
