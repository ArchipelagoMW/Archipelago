from BaseClasses import Region, Entrance, Item, Tutorial
from .Items import YachtDiceItem, item_table, ITEM_GROUPS
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Options import YachtDiceOptions
from .Rules import set_yacht_rules, set_yacht_completion_rules, calculateScoreInLogic, diceSimulation
from ..AutoWorld import World, WebWorld
import math
import logging

class YachtDiceWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yacht Dice. This guide covers "
        "single-player, multiworld, and website.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Spineraks"]
    )]

class YachtDiceWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago, 
    where you cast your dice to chart a course for high scores, 
    unlocking valuable treasures along the way. 
    Discover more dice, extra rolls, multipliers, 
    and unlockable categories to navigate the game's depths. 
    Roll your way to victory by reaching the target score!
    """
    game: str = "Yacht Dice"
    options_dataclass = YachtDiceOptions
    
    web = YachtDiceWeb()
 
    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in all_locations.items()}
    
    item_name_groups = ITEM_GROUPS

    ap_world_version = "1.1.1"

    def _get_yachtdice_data(self):
        return {
            # "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "race": self.multiworld.is_race,
        }
        
    def generate_early(self):
        self.itempool = []
        self.precollected = []
        
        #calculate the maximum score goal:
        game_difficulty = self.options.game_difficulty.value            
            
        #number of dice and rolls in the pull
        numDice = self.options.number_of_dice_and_rolls.value # either 5, 6, 7 or 8
        numRolls = 10 - numDice # either 5, 4, 3 en 2

        #amount of dice and roll fragments needed to get a dice or roll
        amDiceF = self.options.number_of_dice_fragments_per_dice.value
        amRollsF = self.options.number_of_roll_fragments_per_roll.value
        
        #number of extra dice and roll fragments in the pool, 
        #so that you don't have to wait for that one last fragment
        #capped to be one less than number of fragments needed to complete a new dice/roll.
        exDiceF = max(0, min(amDiceF - 1, self.options.number_of_extra_dice_fragments.value) )
        exRollsF = max(0, min(amRollsF - 1, self.options.number_of_extra_roll_fragments.value) )
            
        #count number of plando items not from pool, we need extra locations for them
        self.extra_plando_items = 0
        
        for plando_setting in self.multiworld.plando_items[self.player]:
            if plando_setting.get("from_pool", False) is False:
                self.extra_plando_items += sum(value for value in plando_setting["items"].values())
                

        
        # Create a list with the specified number of 1s
        num_ones = self.options.alternative_categories.value
        categorylist = [1] * num_ones + [0] * (16 - num_ones)
        
        # Shuffle the list to randomize the order
        self.multiworld.random.shuffle(categorylist)                       
       
        
        #add all categories. Note: not "choice" and "inverse choice", they are obtained at the start
        all_categories = [
            ["Category Choice", "Category Double Threes and Fours"],
            ["Category Inverse Choice", "Category Quadruple Ones and Twos"],
            ["Category Ones", "Category Distincts"],
            ["Category Twos", "Category Two times Ones"],
            ["Category Threes", "Category Half of Sixes"],
            ["Category Fours", "Category Twos and Threes"],
            ["Category Fives", "Category Sum of Odds"],
            ["Category Sixes", "Category Sum of Evens"],
            ["Category Pair", "Category Micro Straight"],
            ["Category Three of a Kind", "Category Three Odds"],
            ["Category Four of a Kind", "Category 1-2-1 Consecutive"],
            ["Category Tiny Straight", "Category Three Distinct Dice"],
            ["Category Small Straight", "Category Two Pair"],
            ["Category Large Straight", "Category 2-1-2 Consecutive"],
            ["Category Full House", "Category Five Distinct Dice"],
            ["Category Yacht", "Category 4&5 Full House"]
        ]
        
        possible_categories = []

        for index, cats in enumerate(all_categories):
            possible_categories += [cats[categorylist[index]]]
            if index == 0 or index == 1:
                self.precollected += [cats[categorylist[index]]]
            else:
                self.itempool += [cats[categorylist[index]]]
            
            
        self.precollected += ["Roll"]
        self.precollected += ["Dice"]

         #if one fragment per dice, just add "Dice" objects
        if amDiceF == 1:
            self.itempool += ["Dice"] * (numDice-1) #minus one because one is in start inventory
        else:
            self.itempool += ["Dice"] #always add a full dice to make generation easier
            #add dice fragments, note the -2 because one is added in the previous line, one is in start inventory
            self.itempool += ["Dice Fragment"] * (amDiceF * (numDice-2) + exDiceF)

        #if one fragment per roll, just add "Roll" objects
        if amRollsF == 1:
            self.itempool += ["Roll"] * (numRolls-1) #minus one because one is in start inventory
        else:
            self.itempool += ["Roll"] #always add a full roll to make generation easier
            #add roll fragments, note the -2 because one is added in the previous line, one is in start inventory
            self.itempool += ["Roll Fragment"] * (amRollsF * (numRolls-2) + exRollsF)
            
        #always add exactly 10 score multipliers
        self.itempool += ["Score Multiplier"] * 10
        
        #At this point, the itempool has all basic items.
        scoreInLogic = calculateScoreInLogic(self.itempool+self.precollected, self.options)
        
        already_items = len(self.itempool) + self.extra_plando_items
        
        if self.options.minimize_extra_items.value == 2:
            extraPercentage = max(0.1, 0.5 - self.multiworld.players / 10)
        else:
            extraPercentage = 0.7
            
        extraLocationsNeeded = max(10, math.ceil(already_items * extraPercentage))
                
        if self.options.game_mode.value == 1:
            self.max_score = scoreInLogic
            #print(f"Max score: {self.max_score}, difficulty {game_difficulty}")
        
        if self.options.game_mode.value == 2:
            self.max_score = 1000
            self.extra_points_for_game_mode = self.max_score - scoreInLogic
            
            if(self.options.points_game_mode.value >= 4):
                while self.extra_points_for_game_mode >= 89: #rather have 100 points than lot of smaller items
                    self.itempool += ["100 Points"]
                    self.extra_points_for_game_mode -= 100
                    
            if(self.options.points_game_mode.value >= 3):
                while self.extra_points_for_game_mode >= 7: #rather have 10 points that lot of 1 points.
                    self.itempool += ["10 Points"]
                    self.extra_points_for_game_mode -= 10
            
            if(self.options.points_game_mode.value >= 2 and self.extra_points_for_game_mode > 0):        
                self.itempool += ["1 Point"] * self.extra_points_for_game_mode
               
        if self.options.game_mode.value == 3: 
            self.max_score = 1000
            while calculateScoreInLogic(self.itempool+self.precollected, self.options) < 1000:
                self.itempool += [self.multiworld.random.choice(possible_categories)]
            
        
        
        
        #count the number of locations in the game. extra_plando_items is set in generate_early
        #and counts number of plando items *not* from pool.
        
        already_items = len(self.itempool) + self.extra_plando_items
        self.number_of_locations = already_items + extraLocationsNeeded
        
        # From here, we'll count the number of items in the self.itempool, and add items to the pool,
        # making sure not to exceed the number of locations.
        
        #first, we flood the entire pool with extra points (useful), if that setting is chosen.
        if self.options.add_extra_points.value == 1: #all of the extra points
            already_items = len(self.itempool) + self.extra_plando_items
            self.itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 100)
         
        #second, we flood the entire pool with story chapters (filler), if that setting is chosen.   
        if self.options.add_story_chapters.value == 1: #all of the story chapters
            already_items = len(self.itempool) + self.extra_plando_items
            number_of_items = min(self.number_of_locations - already_items, 100)
            number_of_items = (number_of_items // 10) * 10 #story chapters always come in multiples of 10
            self.itempool += ["Story Chapter"] * number_of_items
            
        #add some extra points (useful)
        if self.options.add_extra_points.value == 2: #add extra points if wanted
            already_items = len(self.itempool) + self.extra_plando_items
            self.itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 10)
            
        #add some story chapters (filler)
        if self.options.add_story_chapters.value == 2: #add extra points if wanted
            already_items = len(self.itempool) + self.extra_plando_items
            if(self.number_of_locations - already_items >= 10):
                self.itempool += ["Story Chapter"] * 10
                
        #add some extra points if there is still room
        if self.options.add_extra_points.value == 2:
            already_items = len(self.itempool) + self.extra_plando_items
            self.itempool += ["Extra Point"] * min(self.number_of_locations - already_items, 10)
         
        #add some encouragements filler-items if there is still room
        already_items = len(self.itempool) + self.extra_plando_items
        self.itempool += ["Encouragement"] * min(self.number_of_locations - already_items, 5)

        #add some fun facts filler-items if there is still room
        already_items = len(self.itempool) + self.extra_plando_items
        self.itempool += ["Fun Fact"] * min(self.number_of_locations - already_items, 5)
        
        #finally, add some "Good RNG" and "Bad RNG" items to complete the item pool
        #these items are filler and don't do anything.
        
        #probability of Good and Bad rng, based on difficulty for fun :)
        p = 0.5
        if self.options.game_difficulty.value == 1:
            p = 0.9
        elif self.options.game_difficulty.value == 2:
            p = 0.7
        elif self.options.game_difficulty.value == 3:
            p = 0.5
        elif self.options.game_difficulty.value == 4:
            p = 0.1
            
        already_items = len(self.itempool) + self.extra_plando_items
        self.itempool += self.multiworld.random.choices(
            ["Good RNG", "Bad RNG"], 
            weights=[p, 1-p], 
            k=self.number_of_locations - already_items
        )

        #we're done adding items. Now because of the last step, number of items should be number of locations
        already_items = len(self.itempool) + self.extra_plando_items
        if len(self.itempool) != self.number_of_locations:
            raise Exception(f"Number in self.itempool is not number of locations {len(self.itempool)} {self.number_of_locations}.")
        
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

    def create_items(self):
        #convert strings to actual items
        itempoolO = [item for item in map(lambda name: self.create_item(name), self.itempool)]

        #and add them to the itempool
        for item in itempoolO:
            self.multiworld.itempool += [item]    

    def create_regions(self):
        #we have no complicated regions, just one rule per location.
        
        game_difficulty = self.options.game_difficulty.value        

        #call the ini_locations function, that generations locations based on the inputs.
        location_table = ini_locations(self.max_score, self.number_of_locations, game_difficulty)

        #simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        #add locations to board, one for every location in the location_table
        board.locations = [YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
                            for loc_name, loc_data in location_table.items() if loc_data.region == board.name]

        #parameter to see where the final check should be
        goal_percentage_location = self.options.goal_location_percentage.value
        
        #which index of all locations should have the Victory item.
        victory_id = int(goal_percentage_location / 100 * len(board.locations))-1
        
        # Add the victory item to the correct location. 
        # The website declares that the game is complete when the victory item is obtained.
        board.locations[victory_id].place_locked_item(self.create_item("Victory"))
              
        #these will be slot_data input
        self.goal_score = board.locations[victory_id].yacht_dice_score
        self.max_score = board.locations[-1].yacht_dice_score
        
        #add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        
    def set_rules(self):
        #set rules per location, and add the rule for beating the game
        set_yacht_rules(self.multiworld, self.player, self.options)
        set_yacht_completion_rules(self.multiworld, self.player)
        
        maxScoreWithItems = diceSimulation(self.multiworld.get_all_state(False), self.player, self.options)
        
        if self.goal_score > maxScoreWithItems:
            raise Exception("In Yacht Dice, with all items in the pool, it is impossible to get to the goal.")
        
    def pre_fill(self):
        #in the pre_fill, make sure one dice and one roll is early, so that you'll have 2 dice and 2 rolls soon
        self.multiworld.early_items[self.player]["Dice"] = 1
        self.multiworld.early_items[self.player]["Roll"] = 1
                
        #put more items early since we want less extra items.
        if self.options.minimize_extra_items.value == 2:
            self.multiworld.early_items[self.player]["Category Pair"] = 1
            self.multiworld.early_items[self.player]["Category Fives"] = 1
            self.multiworld.early_items[self.player]["Category Sixes"] = 1
        
    def fill_slot_data(self):
        #make slot data, which consists of yachtdice_data, options, and some other variables.
        
        yacht_dice_data = self._get_yachtdice_data()
        
        yacht_dice_options = self.options.as_dict(
            "number_of_dice_and_rolls", 
            "number_of_dice_fragments_per_dice", 
            "number_of_roll_fragments_per_roll", 
            "number_of_extra_roll_fragments",
            "game_difficulty",
            "goal_location_percentage", 
            "alternative_categories",
            "score_multiplier_type", 
            "game_mode",
            "minimize_extra_items",
            "add_extra_points", 
            "add_story_chapters", 
            "which_story"
        )
        
        slot_data = {**yacht_dice_data, **yacht_dice_options} #combine the two
                          
        slot_data["goal_score"] = self.goal_score
        slot_data["last_check_score"] = self.max_score
        slot_data["ap_world_version"] = self.ap_world_version
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item