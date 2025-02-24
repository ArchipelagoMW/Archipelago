from typing import List

from BaseClasses import Region, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .items import WordipelagoItem, item_data_table, item_table
from .locations import WordipelagoLocation, location_data_table, get_location_table
from .options import WordipelagoOptions
from .regions import region_data_table
from .rules import create_rules



class WordipelagoWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Wordipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["ProfDeCube"]
    )

    tutorials = [setup_en]


class WordipelagoWorld(World):
    """The greatest game of all time."""

    game = "Wordipelago"
    web = WordipelagoWebWorld()
    options: WordipelagoOptions
    options_dataclass = WordipelagoOptions
    location_name_to_id = get_location_table()
    item_name_to_id = item_table
    starting_items = []

    def fill_slot_data(self):
            """
            make slot data, which consists of options, and some other variables.
            """
            wordipelago_options = self.options.as_dict(
                "words_to_win",
                "green_checks",
                "yellow_checks",
                "letter_checks",
                "starting_letters",
                "starting_guesses",
                "starting_cooldown",
                "time_reward_count",
                "time_reward_seconds",
                "yellow_unlocked",
                "unused_letters_unlocked",
                "shuffle_typing",
                "extra_items_as_time_rewards",
                "start_inventory_from_pool",
            )
            return {
                **wordipelago_options,
                "starting_items": self.starting_items,
                "world_version": "0.8.0"
            }
            
    def create_item(self, name: str) -> WordipelagoItem:
        return WordipelagoItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[WordipelagoItem] = []
        starting_letters: List[str] = []
        
        letter_weights = {
            "A": 979,
            "B": 281,
            "C": 477,
            "D": 393,
            "E": 1233,
            "F": 230,
            "G": 311,
            "H": 389,
            "I": 671,
            "J": 27,
            "K": 210,
            "L": 719,
            "M": 316,
            "N": 575,
            "O": 754,
            "P": 367,
            "Q": 29,
            "R": 899,
            "S": 669,
            "T": 729,
            "U": 467,
            "V": 153,
            "W": 195,
            "X": 37,
            "Y": 425,
            "Z": 40
        }
        all_letters = list(letter_weights.keys())

        for i in range(self.options.starting_letters):
            remaining_letters = [letter for letter in all_letters if letter not in self.starting_items]
            weighted_letter = self.multiworld.random.choices(remaining_letters, weights=list({letter: letter_weights[letter] for letter in remaining_letters}.values()), k=1)[0]
            starting_letters.append('The Letter ' + weighted_letter)
            self.starting_items.append(weighted_letter)
            self.multiworld.push_precollected(self.create_item('The Letter ' + weighted_letter))

        for key, item in item_data_table.items():
            if item.code and item.can_create(self) and key not in starting_letters:
                for i in range(item.count(self)):
                    item_pool.append(self.create_item(key))
        for i in range(self.options.time_reward_count):
            item_pool.append(WordipelagoItem("Time", ItemClassification.filler, 200, self.player))
            
        # Filler Items
        location_count = 26 + 5 + self.options.words_to_win
        item_count = 26 - self.options.starting_letters + 6 - self.options.starting_guesses + self.options.time_reward_count
        if not self.options.yellow_unlocked: 
            item_count += 1
        if not self.options.unused_letters_unlocked: 
            item_count += 1

        if(location_count > item_count):
            for i in range(location_count - item_count):
                if(self.options.extra_items_as_time_rewards):
                    item_pool.append(WordipelagoItem("Time", ItemClassification.filler, 200, self.player))  
                else:
                    item_pool.append(self.create_filler())  

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, WordipelagoLocation)
            if(region_name == 'Words'):
                for i in range(self.options.words_to_win):
                    name = "Word " + str(i + 1)
                    region.add_locations({name: 201 + i})
            region.add_exits(region_data_table[region_name].connecting_regions)

        if(location_data_table["Used J"].can_create(self)):
            self.options.exclude_locations.value.add("Used J")
            self.options.exclude_locations.value.add("Used K")
            self.options.exclude_locations.value.add("Used X")
            self.options.exclude_locations.value.add("Used Z")
            self.options.exclude_locations.value.add("Used Q")

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Not Much"
