from typing import List

from BaseClasses import Region, Tutorial, ItemClassification
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from .items import WordSearchItem, item_data_table, item_table
from .locations import WordSearchLocation, location_data_table, get_location_table
from .options import WordSearchOptions
from .regions import region_data_table
from .rules import create_rules



class WordSearchWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing WordSearch.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["ProfDeCube"]
    )

    tutorials = [setup_en]


class WordSearchWorld(World):
    """A brand new take on the classic 'find a word' game."""

    game = "WordSearch"
    web = WordSearchWebWorld()
    options: WordSearchOptions
    options_dataclass = WordSearchOptions
    location_name_to_id = get_location_table()
    item_name_to_id = item_table
    starting_items = []

    def generate_early(self):
        # Locations check
        # location_count = self.options.total_word_count - 1
        # item_count = 2 * self.options.total_word_count - (self.options.starting_word_count + self.options.starting_loop_count)
        # if(location_count < item_count):
        #     raise OptionError('Not enough locations, increase total words or starting words/loops')

        # Grid size check
        if(self.options.grid_size * self.options.grid_size < self.options.total_word_count * 6):
            raise OptionError('Word search too dense, too many words in too small of a grid')
        # Word List check
        words = self.options.custom_word_list.value.replace(' ', '').split(',')
        if(self.options.exclusively_custom_words):
            for word in words:
                if len(word) > self.options.grid_size:
                    raise OptionError('Custom word list contains words larger than grid size')
            if len(words) < self.options.total_word_count :
                raise OptionError('Not enough words in custom word list to populate word search')

        if(self.multiworld.players == 1):
            if(self.options.starting_loop_count + self.options.starting_word_count < 6):
                raise OptionError('Single player start too restrictive, increase starting words or loops')
            

    def fill_slot_data(self):
            """
            make slot data, which consists of options, and some other variables.
            """
            word_search_options = self.options.as_dict(
                "grid_size",
                "total_word_count",
                "starting_word_count",
                "out_of_logic_words",
                "starting_loop_count",
                "diagonal_words",
                "backwards_words",
                "exclusively_custom_words"
            )
            return {
                **word_search_options,
                "world_version": "0.1.0",
                "custom_word_list": self.options.custom_word_list.value.replace(' ', '').split(',')
            }
            
    def create_item(self, name: str) -> WordSearchItem:
        return WordSearchItem(name, item_data_table[name].type, item_data_table[name].code, player=self.player)

    def create_items(self) -> None:
        item_pool: List[WordSearchItem] = []

        location_count = self.options.total_word_count - 1
        item_count = 2 * self.options.total_word_count - (self.options.starting_word_count + self.options.starting_loop_count)
        item_count_difference = item_count - location_count
        print(item_count, location_count, item_count_difference)
        print("")
        item_count_map = {
            'Word': self.options.total_word_count - self.options.starting_word_count - 2,
            '2 Words': 1,
            '3 Words': 1,
            'Word and Loop': 0, 
            'Loop': self.options.total_word_count - self.options.starting_loop_count - 2,
            '2 Loops': 1,
            '3 Loops': 1,
        }
        
        while(item_count_difference > -2):
            if item_count_map['Word'] == 0 and item_count_map['Loop'] == 0:
                break
            print(item_count_difference)
            choice = self.multiworld.random.choice(['Word', 'Loop'])
            if item_count_map[choice] == 0:
                continue
            
            if choice == 'Word' :
                if item_count_difference == 1 or item_count_map["Word"] == 1:
                    item_count_map["Word"] -= 2
                    item_count_map["2 Words"] += 1
                    item_count_difference -= 1
                else:
                    word_count_choice = self.multiworld.random.choice(['2 Words', '3 Words', '3 Words', '3 Words', '3 Words'])
                    if word_count_choice == '2 Words':
                        item_count_map["Word"] -= 2
                        item_count_map["2 Words"] += 1
                        item_count_difference -= 1
                    else:
                        item_count_map["Word"] -= 3
                        item_count_map["3 Words"] += 1
                        item_count_difference -= 2
            else:
                if item_count_difference == 1 or item_count_map["Loop"] == 1:
                    item_count_map["Loop"] -= 2
                    item_count_map["2 Loops"] += 1
                    item_count_difference -= 1
                else:
                    Loop_count_choice = self.multiworld.random.choice(['2 Loops', '3 Loops', '3 Loops', '3 Loops', '3 Loops'])
                    if Loop_count_choice == '2 Loops':
                        item_count_map["Loop"] -= 2
                        item_count_map["2 Loops"] += 1
                        item_count_difference -= 1
                    else:
                        item_count_map["Loop"] -= 3
                        item_count_map["3 Loops"] += 1
                        item_count_difference -= 2
                        
        print(item_count_difference, item_count_map)

        for key, item in item_data_table.items():
            if item.code and item.can_create(self):
                for i in range(item_count_map[key]):
                    item_pool.append(self.create_item(key))

        print(item_pool)
        print("")
        if(location_count > len(item_pool)):
            filler_items = location_count - len(item_pool)
            for i in range(filler_items):
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
            }, WordSearchLocation)
            
            if(region_name == 'Words'):
                first_check_name = "1 Word Found"
                region.add_locations({first_check_name: 101})
                for i in range(self.options.total_word_count - 1):
                    name =  str(i + 2) + " Words Found"
                    region.add_locations({name: 102 + i})

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"{self.options.total_word_count} Words Found"
        self.get_location(victory_location_name).place_locked_item(
            WordSearchItem("Word Master", ItemClassification.progression, 1000, self.player)
        )

    def set_rules(self):
        create_rules(self)

    def get_filler_item_name(self) -> str:
        return "Filler"
