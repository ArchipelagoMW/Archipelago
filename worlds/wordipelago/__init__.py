from typing import List

from BaseClasses import Region, Tutorial, ItemClassification
from Options import OptionError
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
    """A brand new take on the world famous word guessing game."""

    game = "Wordipelago"
    web = WordipelagoWebWorld()
    options: WordipelagoOptions
    options_dataclass = WordipelagoOptions
    location_name_to_id = get_location_table()
    item_name_to_id = item_table
    starting_items = []

    def generate_early(self):
        location_count = self.options.words_to_win - 1 # Victory Event
        if(self.options.letter_checks >= 1):
            location_count += 6
        if(self.options.letter_checks >= 2):
            location_count += 13
        if(self.options.letter_checks == 3):
            location_count += 7
        if(self.options.green_checks == 1 or self.options.green_checks == 3):
            location_count += 5
        if(self.options.green_checks == 2 or self.options.green_checks == 3):
            location_count += 31
        if(self.options.yellow_checks == 1):
            location_count += 31
        
        if(self.multiworld.players == 1):
            checks_needed = max(4 - self.options.starting_guesses, 0) + max(8 - self.options.starting_letters, 0)
            if(not self.options.starting_guesses):
                checks_needed += 1

            can_reach_words = self.options.starting_letters >= 8 and self.options.yellow_unlocked and self.options.starting_guesses >= 4
            yellow_checks_available = self.options.yellow_checks == 1 and (self.options.green_checks != 0 or self.options.letter_checks != 0)
            enough_checks = self.options.letter_checks >= 2 or self.options.green_checks >= 2
            if(not can_reach_words and not yellow_checks_available and not enough_checks):
                if(not enough_checks):
                    raise OptionError('No way to reach word checks: Not enough locations')

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
                "start_inventory_from_pool",
                "extra_cooldown_trap_size",
                "clue_item_point_size"
            )
            return {
                **wordipelago_options,
                "world_version": "0.8.5"
            }
            
    def create_item(self, name: str) -> WordipelagoItem:
        return WordipelagoItem(name, item_data_table[name].type, item_data_table[name].code, player=self.player)

    def create_items(self) -> None:
        self.starting_items = []
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
            starting_letters.append('Letter ' + weighted_letter)
            self.starting_items.append(weighted_letter)
            self.multiworld.push_precollected(self.create_item('Letter ' + weighted_letter))
        
        for i in range(self.options.starting_guesses):
            self.multiworld.push_precollected(self.create_item('Guess'))
        if(self.options.yellow_unlocked): 
            self.multiworld.push_precollected(self.create_item('Yellow Letters'))
        if(self.options.unused_letters_unlocked): 
            self.multiworld.push_precollected(self.create_item('Unused Letters'))

        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]

        for key, item in item_data_table.items():
            if item.code and item.can_create(self):
                for i in range(item.count(self)):
                    if(key in exclude):
                        exclude.remove(key)
                    else:
                        item_pool.append(self.create_item(key))
            
        # Filler Items
        location_count = self.options.words_to_win - 1 # Victory Event
        if(self.options.letter_checks >= 1):
            location_count += 6
        if(self.options.letter_checks >= 2):
            location_count += 13
        if(self.options.letter_checks == 3):
            location_count += 7
        if(self.options.green_checks == 1 or self.options.green_checks == 3):
            location_count += 5
        if(self.options.green_checks == 2 or self.options.green_checks == 3):
            location_count += 31
        if(self.options.yellow_checks == 1):
            location_count += 31


        item_count = (26 - self.options.starting_letters) + (6 - self.options.starting_guesses) + self.options.time_reward_count
        if not self.options.yellow_unlocked: 
            item_count += 1
        if not self.options.unused_letters_unlocked: 
            item_count += 1

        if(location_count > item_count):
            filler_items = location_count - item_count
            percent_modifier = 1
            total_item_percent = self.options.bad_guess_trap_percent
            + self.options.clue_item_reward_percent
            + self.options.extra_time_reward_percent
            + self.options.extra_cooldown_trap_percent
            if(total_item_percent > 100):
                percent_modifier = 100.00 / total_item_percent
            
            extra_cooldown_trap_count = int((filler_items) * (self.options.extra_cooldown_trap_percent / 100.00) * percent_modifier)
            bad_guess_trap_count = int((filler_items) * (self.options.bad_guess_trap_percent / 100.00) * percent_modifier)
            clue_item_reward_count = int((filler_items) * (self.options.clue_item_reward_percent / 100.00) * percent_modifier)
            extra_time_reward_count = int((filler_items) * (self.options.extra_time_reward_percent / 100.00) * percent_modifier)
            
            for i in range(extra_cooldown_trap_count):
                item_pool.append(WordipelagoItem("Extra Cooldown Trap", ItemClassification.trap, 197, self.player))  
            for i in range(bad_guess_trap_count):
                item_pool.append(WordipelagoItem("Bad Guess Trap", ItemClassification.trap, 198, self.player))  
            for i in range(clue_item_reward_count):
                item_pool.append(WordipelagoItem("Clue Points", ItemClassification.filler, 199, self.player))  
            for i in range(extra_time_reward_count):
                item_pool.append(WordipelagoItem("Time", ItemClassification.filler, 200, self.player))
            for i in range(location_count - (len(item_pool))):
                item_pool.append(self.create_filler())
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Filler Items
        location_count = self.options.words_to_win - 1
        if(self.options.letter_checks >= 1):
            location_count += 6
        if(self.options.letter_checks >= 2):
            location_count += 13
        if(self.options.letter_checks == 3):
            location_count += 7
        if(self.options.green_checks == 1 or self.options.green_checks == 3):
            location_count += 5
        if(self.options.green_checks == 2 or self.options.green_checks == 3):
            location_count += 31
        if(self.options.yellow_checks == 1):
            location_count += 31

        item_count = (26 - self.options.starting_letters) + (6 - self.options.starting_guesses) + self.options.time_reward_count
        if not self.options.yellow_unlocked: 
            item_count += 1
        if not self.options.unused_letters_unlocked: 
            item_count += 1

        loc_count_difference = location_count - item_count

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
                for i in range(self.options.words_to_win + max(0, -loc_count_difference)):
                    name = "Word " + str(i + 1)
                    region.add_locations({name: 1001 + i})

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"Word {self.options.words_to_win}"
        self.get_location(victory_location_name).place_locked_item(
            WordipelagoItem("Word Master", ItemClassification.progression, 1000, self.player)
        )

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Suggestion"
