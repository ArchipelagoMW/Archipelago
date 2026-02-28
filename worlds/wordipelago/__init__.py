from typing import List

from BaseClasses import LocationProgressType, Region, Tutorial, ItemClassification
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from .items import WordipelagoItem, item_data_table, item_table
from .locations import WordipelagoLocation, location_data_table, get_location_table
from .options import WordipelagoOptions, option_groups
from .regions import region_data_table
from .rules import create_rules
from .logicrules import rule_logic, letter_scores



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
    option_groups = option_groups


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
        location_count = self.options.word_checks + self.options.word_streak_checks + self.options.minimum_point_shop_checks
        

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
        
        item_count = (26 - self.options.starting_letters) + (6 - self.options.starting_guesses) + self.options.additional_guesses
        if not self.options.yellow_unlocked: 
            item_count += 1
        if not self.options.unused_letters_unlocked: 
            item_count += 1

        if(self.multiworld.players == 1):
            
            # if(self.options.green_checks == 0 and self.options.yellow_checks == 0):
            #     raise OptionError('Not enough early game locations')
            # if(self.options.letter_checks == 0 and self.options.yellow_checks == 0):
            #     raise OptionError('Not enough early game locations')
            # if(self.options.green_checks == 0 and self.options.letter_checks == 0):
            #     raise OptionError('Not enough early game locations')
        
        
            checks_needed = max(4 - self.options.starting_guesses, 0) + max(8 - self.options.starting_letters, 0)
            if(not self.options.starting_guesses):
                checks_needed += 1

            can_reach_words = self.options.starting_letters >= 8 and self.options.yellow_unlocked and self.options.starting_guesses >= 4
            yellow_checks_available = self.options.yellow_checks == 1 and (self.options.green_checks.value != 0 or self.options.letter_checks.value != 0)
            enough_checks = self.options.letter_checks >= 2 or self.options.green_checks >= 2
            if(not can_reach_words and not yellow_checks_available and not enough_checks):
                if(not enough_checks):
                    raise OptionError('No way to reach word checks: Not enough locations')

    def fill_slot_data(self):
            """
            make slot data, which consists of options, and some other variables.
            """
            wordipelago_options = self.options.as_dict(
                "win_condition",
                "word_checks",
                "word_streak_checks",
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
                "shop_points_item_size",
                "point_shop_check_price",
                "word_weighting"
            )
            game_rule_logic = dict(rule_logic[self.options.logic_difficulty.value])
            game_rule_logic["pointShop"] = rule_logic[self.options.logic_difficulty.value]["green"][str(self.options.point_shop_logic_level.value)]
            
            return {
                **wordipelago_options,
                "world_version": "1.0.0",
                "rule_logic": game_rule_logic,
                "letter_scores" : letter_scores
            }
            
    def create_item(self, name: str) -> WordipelagoItem:
        return WordipelagoItem(name, item_data_table[name].type, item_data_table[name].code, player=self.player)

    def create_items(self) -> None:
        items = 0
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
        
        for i in range(self.options.starting_guesses.value):
            self.multiworld.push_precollected(self.create_item('Guess'))
        if(self.options.starting_guesses.value < 2):
            self.multiworld.early_items[self.player]["Guess"] = 1 
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
        location_count = self.options.word_checks + self.options.word_streak_checks + self.options.minimum_point_shop_checks
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


        item_count = (26 - self.options.starting_letters) + (6 - self.options.starting_guesses) + self.options.time_reward_count + self.options.additional_guesses
        if not self.options.yellow_unlocked: 
            item_count += 1
        if not self.options.unused_letters_unlocked: 
            item_count += 1
        if(location_count > item_count):
            filler_items = location_count - item_count
            percent_modifier = 1
            total_item_percent = (self.options.bad_guess_trap_percent
                + self.options.random_guess_trap_percent
                + self.options.shop_points_item_reward_percent
                + self.options.extra_time_reward_percent
                + self.options.extra_cooldown_trap_percent)
            if(total_item_percent > 0):
                percent_modifier = 100.00 / total_item_percent
            
            extra_cooldown_trap_count = int((filler_items) * (self.options.extra_cooldown_trap_percent / 100.00) * percent_modifier)
            bad_guess_trap_count = int((filler_items) * (self.options.bad_guess_trap_percent / 100.00) * percent_modifier)
            random_guess_trap_count = int((filler_items) * (self.options.random_guess_trap_percent / 100.00) * percent_modifier)
            shop_points_item_reward_count = int((filler_items) * (self.options.shop_points_item_reward_percent / 100.00) * percent_modifier)
            extra_time_reward_count = int((filler_items) * (self.options.extra_time_reward_percent / 100.00) * percent_modifier)
            
            for i in range(extra_cooldown_trap_count):
                item_pool.append(WordipelagoItem("Extra Cooldown Trap", ItemClassification.trap, 196, self.player))  
            for i in range(bad_guess_trap_count):
                item_pool.append(WordipelagoItem("Bad Guess Trap", ItemClassification.trap, 197, self.player))  
            for i in range(random_guess_trap_count):
                item_pool.append(WordipelagoItem("Random Guess Trap", ItemClassification.trap, 198, self.player))  
            for i in range(shop_points_item_reward_count):
                item_pool.append(WordipelagoItem("Shop Points", ItemClassification.filler, 199, self.player))  
            for i in range(extra_time_reward_count):
                item_pool.append(WordipelagoItem("Cooldown Reduction", ItemClassification.filler, 200, self.player))
            for i in range(location_count - (len(item_pool))):
                item_pool.append(self.create_filler())
                
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Filler Items
        location_count = self.options.word_checks + self.options.word_streak_checks + self.options.minimum_point_shop_checks
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

        item_count = (26 - self.options.starting_letters) + (6 - self.options.starting_guesses) + self.options.time_reward_count + self.options.additional_guesses
        if not self.options.yellow_unlocked: 
            item_count += 1
            # self.multiworld.early_items[self.player]["Yellow Letters"] = 1

        if not self.options.unused_letters_unlocked: 
            item_count += 1

        loc_count_difference = location_count - item_count

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        word_chunk_size = self.options.word_checks // 5 + (self.options.word_checks % 5 > 0)
        word_streak_chunk_size = self.options.word_streak_checks // 5 + (self.options.word_streak_checks % 5 > 0)
        locs = 0
        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            for location_name, location_data in location_data_table.items():
                if location_data.region == region_name and location_data.can_create(self):
                    locs = locs + 1
                    region.add_locations({location_name: location_data.address}, WordipelagoLocation)
            if(region_name == 'Words'):
                for i in range(self.options.word_checks):
                    locs = locs + 1
                    chunk_region = self.get_region('Words Chunk ' + str(min(5, i // word_chunk_size + 1)))
                    name = "Word " + str(i + 1)
                    chunk_region.add_locations({name: 1001 + i})
                    if((i + 1) % word_chunk_size == 0 or i + 1 == self.options.word_checks):
                        event_name = str(i + 1) + " Words"
                        chunk_region.add_locations({event_name: None})
                    
            if(region_name == 'Streaks'):
                for i in range(self.options.word_streak_checks):
                    locs = locs + 1
                    chunk_region = self.get_region('Streaks Chunk ' + str(min(5, i // word_streak_chunk_size + 1)))
                    name = str(i + 1) + " Word Streak"
                    chunk_region.add_locations({name: 2001 + i})
                    
                    if((i + 1) % word_streak_chunk_size == 0 or i + 1 == self.options.word_streak_checks):
                        event_name = str(i + 1) + " Streaks"
                        chunk_region.add_locations({event_name: None})
                        
            if(region_name == 'Point Shop'):
                for i in range(self.options.minimum_point_shop_checks + max(0, -loc_count_difference)):
                    locs = locs + 1
                    name = "Point Shop Purchase " + str(i + 1)
                    region.add_locations({name: 3001 + i})


    
        # Change the victory location to an event and place the Victory item there.
        victory_location_name = "Goal Event Location"
        self.get_region('Menu').add_locations({victory_location_name: None})
        self.get_location(victory_location_name).place_locked_item(
            WordipelagoItem("Word Master", ItemClassification.progression, None, self.player)
        )
        
        for i in range(1, self.options.word_checks + 1):
            if(i != 0 and i % word_chunk_size == 0 or i == self.options.word_checks):
                self.get_location(str(i) + " Words").place_locked_item(
                    WordipelagoItem(str(i) + " Words", ItemClassification.progression, None, self.player)
                )
                
                self.get_location(str(i) + " Words").access_rule = lambda state: (lambda state, self, i: self.get_location("Word " + str(i), self.player) in state.locations_checked)
        
        for i in range(1, self.options.word_streak_checks + 1):
            if(i != 0 and i % word_streak_chunk_size == 0 or i == self.options.word_streak_checks):
                self.get_location(str(i) + " Streaks").place_locked_item(
                    WordipelagoItem(str(i) + " Streaks", ItemClassification.progression, None, self.player)
                )
                
                self.get_location(str(i) + " Streaks").access_rule = lambda state: (lambda state, self, i: self.get_location(str(i) + " Word Streak") in state.locations_checked)

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Suggestion"
