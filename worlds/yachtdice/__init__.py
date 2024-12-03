import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import YachtDiceItem, item_groups, item_table
from .Locations import YachtDiceLocation, all_locations, ini_locations
from .Options import (
    AddExtraPoints,
    AddStoryChapters,
    GameDifficulty,
    MinimalNumberOfDiceAndRolls,
    MinimizeExtraItems,
    PointsSize,
    YachtDiceOptions,
    yd_option_groups,
)
from .Rules import dice_simulation_fill_pool, set_yacht_completion_rules, set_yacht_rules


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

    option_groups = yd_option_groups


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

    ap_world_version = "2.1.4"

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

        # number of dice and rolls in the pull
        opt_dice_and_rolls = self.options.minimal_number_of_dice_and_rolls

        if opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_5_dice_and_3_rolls:
            num_of_dice = 5
            num_of_rolls = 3
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_5_dice_and_5_rolls:
            num_of_dice = 5
            num_of_rolls = 5
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_6_dice_and_4_rolls:
            num_of_dice = 6
            num_of_rolls = 4
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_7_dice_and_3_rolls:
            num_of_dice = 7
            num_of_rolls = 3
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_8_dice_and_2_rolls:
            num_of_dice = 8
            num_of_rolls = 2
        else:
            raise Exception(f"[Yacht Dice] Unknown MinimalNumberOfDiceAndRolls options {opt_dice_and_rolls}")

        # amount of dice and roll fragments needed to get a dice or roll
        self.frags_per_dice = self.options.number_of_dice_fragments_per_dice.value
        self.frags_per_roll = self.options.number_of_roll_fragments_per_roll.value

        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            self.frags_per_dice = min(self.frags_per_dice, 2)
            self.frags_per_roll = min(self.frags_per_roll, 2)

        # set difficulty
        diff_value = self.options.game_difficulty
        if diff_value == GameDifficulty.option_easy:
            self.difficulty = 1
        elif diff_value == GameDifficulty.option_medium:
            self.difficulty = 2
        elif diff_value == GameDifficulty.option_hard:
            self.difficulty = 3
        elif diff_value == GameDifficulty.option_extreme:
            self.difficulty = 4
        else:
            raise Exception(f"[Yacht Dice] Unknown GameDifficulty options {diff_value}")

        # Create a list with the specified number of 1s
        num_ones = self.options.alternative_categories.value
        categorylist = [1] * num_ones + [0] * (16 - num_ones)

        # Shuffle the list to randomize the order
        self.random.shuffle(categorylist)

        # A list of all possible categories.
        # Every entry in the list has two categories, one 'default' category and one 'alt'.
        # You get either of the two for every entry, so a total of 16 unique categories.
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
            ["Category Yacht", "Category 4&5 Full House"],
        ]

        # categories used in this game.
        self.possible_categories = []

        for index, cats in enumerate(all_categories):
            self.possible_categories.append(cats[categorylist[index]])

            # Add Choice and Inverse choice (or their alts) to the precollected list.
            if index == 0 or index == 1:
                self.precollected.append(cats[categorylist[index]])
            else:
                self.itempool.append(cats[categorylist[index]])

        # Also start with one Roll and one Dice
        self.precollected.append("Dice")
        num_of_dice_to_add = num_of_dice - 1
        self.precollected.append("Roll")
        num_of_rolls_to_add = num_of_rolls - 1

        self.skip_early_locations = False
        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            self.precollected.append("Dice")
            num_of_dice_to_add -= 1
            self.precollected.append("Roll")
            num_of_rolls_to_add -= 1
            self.skip_early_locations = True

        if num_of_dice_to_add > 0:
            self.itempool.append("Dice")
            num_of_dice_to_add -= 1
        if num_of_rolls_to_add > 0:
            self.itempool.append("Roll")
            num_of_rolls_to_add -= 1

        # if one fragment per dice, just add "Dice" objects
        if num_of_dice_to_add > 0:
            if self.frags_per_dice == 1:
                self.itempool += ["Dice"] * num_of_dice_to_add  # minus one because one is in start inventory
            else:
                self.itempool += ["Dice Fragment"] * (self.frags_per_dice * num_of_dice_to_add)

        # if one fragment per roll, just add "Roll" objects
        if num_of_rolls_to_add > 0:
            if self.frags_per_roll == 1:
                self.itempool += ["Roll"] * num_of_rolls_to_add  # minus one because one is in start inventory
            else:
                self.itempool += ["Roll Fragment"] * (self.frags_per_roll * num_of_rolls_to_add)

        already_items = len(self.itempool)

        # Yacht Dice needs extra filler items so it doesn't get stuck in generation.
        # For now, we calculate the number of extra items we'll need later.
        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            extra_percentage = max(0.1, 0.8 - self.multiworld.players / 10)
        elif self.options.minimize_extra_items == MinimizeExtraItems.option_no_dont:
            extra_percentage = 0.72
        else:
            raise Exception(f"[Yacht Dice] Unknown MinimizeExtraItems options {self.options.minimize_extra_items}")
        extra_locations_needed = max(10, math.ceil(already_items * extra_percentage))

        # max score is the value of the last check. Goal score is the score needed to 'finish' the game
        self.max_score = self.options.score_for_last_check.value
        self.goal_score = min(self.max_score, self.options.score_for_goal.value)

        # Yacht Dice adds items into the pool until a score of at least 1000 is reached.
        # the yaml contains weights, which determine how likely it is that specific items get added.
        # If all weights are 0, some of them will be made to be non-zero later.
        weights: Dict[str, float] = {
            "Dice": self.options.weight_of_dice.value,
            "Roll": self.options.weight_of_roll.value,
            "Fixed Score Multiplier": self.options.weight_of_fixed_score_multiplier.value,
            "Step Score Multiplier": self.options.weight_of_step_score_multiplier.value,
            "Double category": self.options.weight_of_double_category.value,
            "Points": self.options.weight_of_points.value,
        }

        # if the player wants extra rolls or dice, fill the pool with fragments until close to an extra roll/dice
        if weights["Dice"] > 0 and self.frags_per_dice > 1:
            self.itempool += ["Dice Fragment"] * (self.frags_per_dice - 1)
        if weights["Roll"] > 0 and self.frags_per_roll > 1:
            self.itempool += ["Roll Fragment"] * (self.frags_per_roll - 1)

        # calibrate the weights, since the impact of each of the items is different
        weights["Dice"] = weights["Dice"] / 5 * self.frags_per_dice
        weights["Roll"] = weights["Roll"] / 5 * self.frags_per_roll

        extra_points_added = [0]  # make it a mutible type so we can change the value in the function
        step_score_multipliers_added = [0]

        def get_item_to_add(weights, extra_points_added, step_score_multipliers_added):
            all_items = self.itempool + self.precollected
            dice_fragments_in_pool = all_items.count("Dice") * self.frags_per_dice + all_items.count("Dice Fragment")
            if dice_fragments_in_pool + 1 >= 9 * self.frags_per_dice:
                weights["Dice"] = 0  # don't allow >=9 dice
            roll_fragments_in_pool = all_items.count("Roll") * self.frags_per_roll + all_items.count("Roll Fragment")
            if roll_fragments_in_pool + 1 >= 6 * self.frags_per_roll:
                weights["Roll"] = 0  # don't allow >= 6 rolls

            # Don't allow too many extra points
            if extra_points_added[0] > 400:
                weights["Points"] = 0

            if step_score_multipliers_added[0] > 10:
                weights["Step Score Multiplier"] = 0

            # if all weights are zero, allow to add fixed score multiplier, double category, points.
            if sum(weights.values()) == 0:
                weights["Fixed Score Multiplier"] = 1
                weights["Double category"] = 1
                if extra_points_added[0] <= 400:
                    weights["Points"] = 1

            # Next, add the appropriate item. We'll slightly alter weights to avoid too many of the same item
            which_item_to_add = self.random.choices(list(weights.keys()), weights=list(weights.values()))[0]

            if which_item_to_add == "Dice":
                weights["Dice"] /= 1 + self.frags_per_dice
                return "Dice" if self.frags_per_dice == 1 else "Dice Fragment"
            elif which_item_to_add == "Roll":
                weights["Roll"] /= 1 + self.frags_per_roll
                return "Roll" if self.frags_per_roll == 1 else "Roll Fragment"
            elif which_item_to_add == "Fixed Score Multiplier":
                weights["Fixed Score Multiplier"] /= 1.05
                return "Fixed Score Multiplier"
            elif which_item_to_add == "Step Score Multiplier":
                weights["Step Score Multiplier"] /= 1.1
                step_score_multipliers_added[0] += 1
                return "Step Score Multiplier"
            elif which_item_to_add == "Double category":
                # Below entries are the weights to add each category.
                # Prefer to add choice or number categories, because the other categories are too "all or nothing",
                # which often don't give any points, until you get overpowered, and then they give all points.
                cat_weights = [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
                weights["Double category"] /= 1.1
                return self.random.choices(self.possible_categories, weights=cat_weights)[0]
            elif which_item_to_add == "Points":
                score_dist = self.options.points_size
                probs = {"1 Point": 1, "10 Points": 0, "100 Points": 0}
                if score_dist == PointsSize.option_small:
                    probs = {"1 Point": 0.9, "10 Points": 0.1, "100 Points": 0}
                elif score_dist == PointsSize.option_medium:
                    probs = {"1 Point": 0, "10 Points": 1, "100 Points": 0}
                elif score_dist == PointsSize.option_large:
                    probs = {"1 Point": 0, "10 Points": 0.3, "100 Points": 0.7}
                elif score_dist == PointsSize.option_mix:
                    probs = {"1 Point": 0.3, "10 Points": 0.4, "100 Points": 0.3}
                else:
                    raise Exception(f"[Yacht Dice] Unknown PointsSize options {score_dist}")
                choice = self.random.choices(list(probs.keys()), weights=list(probs.values()))[0]
                if choice == "1 Point":
                    weights["Points"] /= 1.01
                    extra_points_added[0] += 1
                    return "1 Point"
                elif choice == "10 Points":
                    weights["Points"] /= 1.1
                    extra_points_added[0] += 10
                    return "10 Points"
                elif choice == "100 Points":
                    weights["Points"] /= 2
                    extra_points_added[0] += 100
                    return "100 Points"
                else:
                    raise Exception("Unknown point value (Yacht Dice)")
            else:
                raise Exception(f"Invalid index when adding new items in Yacht Dice: {which_item_to_add}")

        # adding 17 items as a start seems like the smartest way to get close to 1000 points
        for _ in range(17):
            self.itempool.append(get_item_to_add(weights, extra_points_added, step_score_multipliers_added))

        score_in_logic = dice_simulation_fill_pool(
            self.itempool + self.precollected,
            self.frags_per_dice,
            self.frags_per_roll,
            self.possible_categories,
            self.difficulty,
            self.player,
        )

        # if we overshoot, remove items until you get below 1000, then return the last removed item
        if score_in_logic > 1000:
            removed_item = ""
            while score_in_logic > 1000:
                removed_item = self.itempool.pop()
                score_in_logic = dice_simulation_fill_pool(
                    self.itempool + self.precollected,
                    self.frags_per_dice,
                    self.frags_per_roll,
                    self.possible_categories,
                    self.difficulty,
                    self.player,
                )
            self.itempool.append(removed_item)
        else:
            # Keep adding items until a score of 1000 is in logic
            while score_in_logic < 1000:
                item_to_add = get_item_to_add(weights, extra_points_added, step_score_multipliers_added)
                self.itempool.append(item_to_add)
                if item_to_add == "1 Point":
                    score_in_logic += 1
                elif item_to_add == "10 Points":
                    score_in_logic += 10
                elif item_to_add == "100 Points":
                    score_in_logic += 100
                else:
                    score_in_logic = dice_simulation_fill_pool(
                        self.itempool + self.precollected,
                        self.frags_per_dice,
                        self.frags_per_roll,
                        self.possible_categories,
                        self.difficulty,
                        self.player,
                    )

        # count the number of locations in the game.
        already_items = len(self.itempool) + 1  # +1 because of Victory item

        # We need to add more filler/useful items if there are many items in the pool to guarantee successful generation
        extra_locations_needed += (already_items - 45) // 15
        self.number_of_locations = already_items + extra_locations_needed

        # From here, we will count the number of items in the self.itempool, and add useful/filler items to the pool,
        # making sure not to exceed the number of locations.

        # first, we flood the entire pool with extra points (useful), if that setting is chosen.
        if self.options.add_bonus_points == AddExtraPoints.option_all_of_it:  # all of the extra points
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 100)

        # second, we flood the entire pool with story chapters (filler), if that setting is chosen.
        if self.options.add_story_chapters == AddStoryChapters.option_all_of_it:  # all of the story chapters
            already_items = len(self.itempool) + 1
            number_of_items = min(self.number_of_locations - already_items, 100)
            number_of_items = (number_of_items // 10) * 10  # story chapters always come in multiples of 10
            self.itempool += ["Story Chapter"] * number_of_items

        # add some extra points (useful)
        if self.options.add_bonus_points == AddExtraPoints.option_sure:  # add extra points if wanted
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)

        # add some story chapters (filler)
        if self.options.add_story_chapters == AddStoryChapters.option_sure:  # add extra points if wanted
            already_items = len(self.itempool) + 1
            if self.number_of_locations - already_items >= 10:
                self.itempool += ["Story Chapter"] * 10

        # add some more extra points if there is still room
        if self.options.add_bonus_points == AddExtraPoints.option_sure:
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)

        # add some encouragements filler-items if there is still room
        already_items = len(self.itempool) + 1
        self.itempool += ["Encouragement"] * min(self.number_of_locations - already_items, 5)

        # add some fun facts filler-items if there is still room
        already_items = len(self.itempool) + 1
        self.itempool += ["Fun Fact"] * min(self.number_of_locations - already_items, 5)

        # finally, add some "Good RNG" and "Bad RNG" items to complete the item pool
        # these items are filler and do not do anything.

        # probability of Good and Bad rng, based on difficulty for fun :)

        p = 1.1 - 0.25 * self.difficulty
        already_items = len(self.itempool) + 1
        self.itempool += self.random.choices(
            ["Good RNG", "Bad RNG"], weights=[p, 1 - p], k=self.number_of_locations - already_items
        )

        # we are done adding items. Now because of the last step, number of items should be number of locations
        already_items = len(self.itempool) + 1
        if already_items != self.number_of_locations:
            raise Exception(
                f"[Yacht Dice] Number in self.itempool is not number of locations "
                f"{already_items} {self.number_of_locations}."
            )

        # add precollected items using push_precollected. Items in self.itempool get created in create_items
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

        # make sure one dice and one roll is early, so that you will have 2 dice and 2 rolls soon
        self.multiworld.early_items[self.player]["Dice"] = 1
        self.multiworld.early_items[self.player]["Roll"] = 1

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]

    def create_regions(self):
        # call the ini_locations function, that generates locations based on the inputs.
        location_table = ini_locations(
            self.goal_score,
            self.max_score,
            self.number_of_locations,
            self.difficulty,
            self.skip_early_locations,
            self.multiworld.players,
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
        return "Good RNG"

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
        set_yacht_rules(
            self.multiworld,
            self.player,
            self.frags_per_dice,
            self.frags_per_roll,
            self.possible_categories,
            self.difficulty,
        )
        set_yacht_completion_rules(self.multiworld, self.player)

    def fill_slot_data(self):
        """
        make slot data, which consists of yachtdice_data, options, and some other variables.
        """
        yacht_dice_data = self._get_yachtdice_data()
        yacht_dice_options = self.options.as_dict(
            "game_difficulty",
            "score_for_last_check",
            "score_for_goal",
            "number_of_dice_fragments_per_dice",
            "number_of_roll_fragments_per_roll",
            "which_story",
            "allow_manual_input",
        )
        slot_data = {**yacht_dice_data, **yacht_dice_options}  # combine the two
        slot_data["number_of_dice_fragments_per_dice"] = self.frags_per_dice
        slot_data["number_of_roll_fragments_per_roll"] = self.frags_per_roll
        slot_data["goal_score"] = self.goal_score
        slot_data["last_check_score"] = self.max_score
        slot_data["allowed_categories"] = self.possible_categories
        slot_data["ap_world_version"] = self.ap_world_version
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item

    # We overwrite these function to monitor when states have changed. See also dice_simulation in Rules.py
    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            state.prog_items[self.player]["state_is_fresh"] = 0

        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:
            state.prog_items[self.player]["state_is_fresh"] = 0

        return change
