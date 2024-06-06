import math
import logging

from BaseClasses import Region, Entrance, Item, Tutorial
from .Items import YachtDiceItem, item_table, item_groups
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Options import YachtDiceOptions
from .Rules import set_yacht_rules, set_yacht_completion_rules, dice_simulation
from ..AutoWorld import World, WebWorld


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
    and unlockable categories to navigate the depths of the game. 
    Roll your way to victory by reaching the target score!
    """
    game: str = "Yacht Dice"
    options_dataclass = YachtDiceOptions
    
    web = YachtDiceWeb()
 
    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in all_locations.items()}
    
    item_name_groups = item_groups

    ap_world_version = "2.0.2"

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
            
        #number of dice and rolls in the pull
        ind_dice_rolls = self.options.minimal_number_of_dice_and_rolls.value
        
        num_of_dice = [0, 2, 5, 5, 6, 7, 8][ind_dice_rolls]
        num_of_rolls = [0, 2, 3, 5, 4, 3, 2][ind_dice_rolls]

        #amount of dice and roll fragments needed to get a dice or roll
        frags_per_dice = self.options.number_of_dice_fragments_per_dice.value
        frags_per_roll = self.options.number_of_roll_fragments_per_roll.value
            
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
       
        
        #A list of all possible categories.
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
        
        #categories used in this game.
        possible_categories = []

        for index, cats in enumerate(all_categories):
            possible_categories += [cats[categorylist[index]]]
            
            # Add Choice and Inverse choice (or their alts) to the precollected list.
            if index == 0 or index == 1:
                self.precollected += [cats[categorylist[index]]]
            else:
                self.itempool += [cats[categorylist[index]]]
            
        # Also start with one Roll and one Dice
        self.precollected += ["Roll"]
        self.precollected += ["Dice"]

        #if one fragment per dice, just add "Dice" objects
        if frags_per_dice == 1:
            self.itempool += ["Dice"] * (num_of_dice-1) #minus one because one is in start inventory
        else:
            self.itempool += ["Dice"] #always add a full dice to make generation easier (will be early)
            self.itempool += ["Dice Fragment"] * (frags_per_dice * (num_of_dice-2))

        #if one fragment per roll, just add "Roll" objects
        if frags_per_roll == 1:
            self.itempool += ["Roll"] * (num_of_rolls-1) #minus one because one is in start inventory
        else:
            self.itempool += ["Roll"] #always add a full roll to make generation easier (will be early)
            self.itempool += ["Roll Fragment"] * (frags_per_roll * (num_of_rolls-2))
                
        already_items = len(self.itempool) + self.extra_plando_items
        
        #Yacht Dice needs extra filler items so it doesn't get stuck in generation.
        if self.options.minimize_extra_items.value == 2:
            extraPercentage = max(0.1, 0.8 - self.multiworld.players / 10)
        else:
            extraPercentage = 0.7
            
        extra_locations_needed = max(10, math.ceil(already_items * extraPercentage))
                
        self.max_score = self.options.score_for_last_check.value
        self.goal_score = min(self.max_score, self.options.score_for_goal.value)
        
        weights = [
            self.options.weight_of_dice.value,
            self.options.weight_of_roll.value,
            self.options.weight_of_fixed_score_multiplier.value,
            self.options.weight_of_step_score_multiplier.value,
            self.options.weight_of_double_category.value,
            self.options.weight_of_points.value
        ]
        
        #if the player wants extra rolls or dice, fill the pool with fragments until close to an extra roll/dice
        if weights[0] > 0 and frags_per_dice > 1:
            self.itempool += ["Dice Fragment"] * (frags_per_dice - 1)
        if weights[1] > 0 and frags_per_roll > 1:
            self.itempool += ["Roll Fragment"] * (frags_per_roll - 1)
            
        #calibrate the weights, since the impact of each of the items is different
        weights[0] = weights[0] / 5 * frags_per_dice
        weights[1] = weights[1] / 5 * frags_per_roll
            
        extra_points_added = 0
        multipliers_added = 0
        
        while dice_simulation(self.itempool + self.precollected, "state_is_a_list", self.options) < 1000:  
            all_items = self.itempool + self.precollected
            dice_fragments_in_pool = all_items.count("Dice") * frags_per_dice + all_items.count("Dice Fragment")
            if dice_fragments_in_pool + 1 >= 9 * frags_per_dice:
                weights[0] = 0 #cannot have 9 dice
            roll_fragments_in_pool = all_items.count("Roll") * frags_per_roll + all_items.count("Roll Fragment")
            if roll_fragments_in_pool + 1 >= 6 * frags_per_roll:
                weights[1] = 0 # cannot have 6 rolls
                
            if multipliers_added > 50:
                weights[2] = 0
                weights[3] = 0
                
            if extra_points_added > 300:
                weights[5] = 0                
            
            #if all weights are zero, allow to add fixed score multiplier, double category, points.
            if sum(weights) == 0:
                if multipliers_added <= 50:
                    weights[2] = 1 
                weights[4] = 1
                if extra_points_added <= 300:
                    weights[5] = 1
                
            which_item_to_add = self.multiworld.random.choices([0,1,2,3,4,5], weights = weights)[0]
            
            if which_item_to_add == 0:
                if frags_per_dice == 1:
                    self.itempool += ["Dice"]
                else:
                    self.itempool += ["Dice Fragment"]
                weights[0] /= (1 + frags_per_dice)
            elif which_item_to_add == 1:
                if frags_per_roll == 1:
                    self.itempool += ["Roll"]
                else:
                    self.itempool += ["Roll Fragment"]
                weights[1] /= (1 + frags_per_roll)
            elif which_item_to_add == 2:
                self.itempool += ["Fixed Score Multiplier"]
                weights[2] /= 1.05
                multipliers_added += 1
            elif which_item_to_add == 3:
                self.itempool += ["Step Score Multiplier"]
                weights[3] /= 1.1
                multipliers_added += 1
            elif which_item_to_add == 4:
                #increase chances of "free-score categories"
                cat_weights = [2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1] 
                self.itempool += self.multiworld.random.choices(possible_categories, weights = cat_weights)
                weights[4] /= 1.1
            elif which_item_to_add == 5:
                score_dist = self.options.points_size.value
                probs = [1,0,0]
                if score_dist == 1:
                    probs = [0.9,0.08,0]
                if score_dist == 2:
                    probs = [0,1,0]
                if score_dist == 3:
                    probs = [0,0.3,0.7]
                if score_dist == 4:
                    probs = [0.3,0.4,0.3]
                c = self.multiworld.random.choices([0,1,2], weights = probs)[0] 
                if c == 0:
                    self.itempool += ["1 Point"]
                    extra_points_added += 1
                    weights[5] /= 1.01
                elif c==1:
                    self.itempool += ["10 Points"]
                    extra_points_added += 10
                    weights[5] /= 1.1
                elif c==2:
                    self.itempool += ["100 Points"]
                    extra_points_added += 100
                    weights[5] /= 2
                else:
                    raise Exception("Unknown point value (Yacht Dice)")
            else:
                raise Exception("Invalid index when adding new items in Yacht Dice")
                               
        #count the number of locations in the game. extra_plando_items is set in generate_early
        #and counts number of plando items *not* from pool.
        
        already_items = len(self.itempool) + self.extra_plando_items + 1 #+1 because of Victory item
        
        extra_locations_needed += (already_items - 70) // 20
        self.number_of_locations = already_items + extra_locations_needed
        
        # From here, we will count the number of items in the self.itempool, and add items to the pool,
        # making sure not to exceed the number of locations.
        
        #first, we flood the entire pool with extra points (useful), if that setting is chosen.
        if self.options.add_bonus_points.value == 1: #all of the extra points
            already_items = len(self.itempool) + self.extra_plando_items + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 100)
         
        #second, we flood the entire pool with story chapters (filler), if that setting is chosen.   
        if self.options.add_story_chapters.value == 1: #all of the story chapters
            already_items = len(self.itempool) + self.extra_plando_items + 1
            number_of_items = min(self.number_of_locations - already_items, 100)
            number_of_items = (number_of_items // 10) * 10 #story chapters always come in multiples of 10
            self.itempool += ["Story Chapter"] * number_of_items
            
        #add some extra points (useful)
        if self.options.add_bonus_points.value == 2: #add extra points if wanted
            already_items = len(self.itempool) + self.extra_plando_items + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)
            
        #add some story chapters (filler)
        if self.options.add_story_chapters.value == 2: #add extra points if wanted
            already_items = len(self.itempool) + self.extra_plando_items + 1
            if(self.number_of_locations - already_items >= 10):
                self.itempool += ["Story Chapter"] * 10
                
        #add some extra points if there is still room
        if self.options.add_bonus_points.value == 2:
            already_items = len(self.itempool) + self.extra_plando_items + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)
         
        #add some encouragements filler-items if there is still room
        already_items = len(self.itempool) + self.extra_plando_items + 1
        self.itempool += ["Encouragement"] * min(self.number_of_locations - already_items, 5)

        #add some fun facts filler-items if there is still room
        already_items = len(self.itempool) + self.extra_plando_items + 1
        self.itempool += ["Fun Fact"] * min(self.number_of_locations - already_items, 5)
        
        #finally, add some "Good RNG" and "Bad RNG" items to complete the item pool
        #these items are filler and do not do anything.
        
        #probability of Good and Bad rng, based on difficulty for fun :)
        p = 1.1 - 0.25 * self.options.game_difficulty.value
            
        already_items = len(self.itempool) + self.extra_plando_items + 1
        self.itempool += self.multiworld.random.choices(
            ["Good RNG", "Bad RNG"], 
            weights=[p, 1-p], 
            k=self.number_of_locations - already_items
        )

        #we are done adding items. Now because of the last step, number of items should be number of locations
        already_items = len(self.itempool) + self.extra_plando_items + 1
        if already_items != self.number_of_locations:
            raise Exception(f"[Yacht Dice] Number in self.itempool is not number of locations "
                f"{already_items} {self.number_of_locations}.")
        
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

    def create_items(self):
        #convert strings to actual items
        itempoolO = [item for item in map(lambda name: self.create_item(name), self.itempool)]

        #and add them to the itempool
        for item in itempoolO:
            self.multiworld.itempool += [item]    

    def create_regions(self):
        #call the ini_locations function, that generates locations based on the inputs.
        location_table, goal_index = ini_locations(self.goal_score, self.max_score, self.number_of_locations, 
                                                        self.options.game_difficulty.value)

        #simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        #add locations to board, one for every location in the location_table
        board.locations = [YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
                            for loc_name, loc_data in location_table.items() if loc_data.region == board.name]
        
        #which index of all locations should have the Victory item.
        
        # Add the victory item to the correct location. 
        # The website declares that the game is complete when the victory item is obtained.
        board.locations[goal_index].place_locked_item(self.create_item("Victory"))
              
        #these will be slot_data input
        self.goal_score = board.locations[goal_index].yacht_dice_score
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
        
        maxScoreWithItems = dice_simulation(self.multiworld.get_all_state(False), self.player, self.options)
        
        if self.goal_score > maxScoreWithItems:
            raise Exception("In Yacht Dice, with all items in the pool, it is impossible to get to the goal.")
        
    def pre_fill(self):
        #in the pre_fill, make sure one dice and one roll is early, so that you will have 2 dice and 2 rolls soon
        self.multiworld.early_items[self.player]["Dice"] = 1
        self.multiworld.early_items[self.player]["Roll"] = 1
        
    def fill_slot_data(self):
        #make slot data, which consists of yachtdice_data, options, and some other variables.
        
        yacht_dice_data = self._get_yachtdice_data()
        
        yacht_dice_options = self.options.as_dict(
                "game_difficulty",
                "score_for_last_check",
                "score_for_goal",
                "minimal_number_of_dice_and_rolls",
                "number_of_dice_fragments_per_dice",
                "number_of_roll_fragments_per_roll",            
                "alternative_categories",
                "weight_of_dice",
                "weight_of_roll",
                "weight_of_fixed_score_multiplier",
                "weight_of_step_score_multiplier",
                "weight_of_double_category",
                "weight_of_points",
                "points_size",
                "minimize_extra_items",
                "add_bonus_points",
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