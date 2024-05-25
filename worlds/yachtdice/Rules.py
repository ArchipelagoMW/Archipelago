from ..generic.Rules import set_rule
from BaseClasses import MultiWorld
from .YachtWeights import yacht_weights
import math

category_mappings = {
    "Category Ones": "Ones",
    "Category Twos": "Twos",
    "Category Threes": "Threes",
    "Category Fours": "Fours",
    "Category Fives": "Fives",
    "Category Sixes": "Sixes",
    "Category Choice": "Choice",
    "Category Inverse Choice": "Choice",
    "Category Pair": "Pair",
    "Category Three of a Kind": "ThreeOfAKind",
    "Category Four of a Kind": "FourOfAKind",
    "Category Tiny Straight": "TinyStraight",
    "Category Small Straight": "SmallStraight",
    "Category Large Straight": "LargeStraight",
    "Category Full House": "FullHouse",
    "Category Yacht": "Yacht",
    "Category Distincts": "Distincts",
    "Category Two times Ones": "TwoTimesOnes",
    "Category Half of Sixes": "HalfOfSixes",
    "Category Twos and Threes": "TwosAndThrees",
    "Category Sum of Odds": "SumOfOdds",
    "Category Sum of Evens": "SumOfEvens",
    "Category Double Threes and Fours": "DoubleThreesAndFours",
    "Category Quadruple Ones and Twos": "QuadrupleOnesAndTwos",
    "Category Micro Straight": "MicroStraight",
    "Category Three Odds": "ThreeOdds",
    "Category 1-2-1 Consecutive": "OneTwoOneConsecutive",
    "Category Three Distinct Dice": "ThreeDistinctDice",
    "Category Two Pair": "TwoPair",
    "Category 2-1-2 Consecutive": "TwoOneTwoConsecutive",
    "Category Five Distinct Dice": "FiveDistinctDice",
    "Category 4&5 Full House": "FourAndFiveFullHouse"
}

#This class adds logic to the apworld.
#In short, we ran a simulation for every possible combination of dice and rolls you can have, per category.
#This simulation has a good strategy for locking dice.
#This gives rise to an approximate discrete distribution per category.
#We calculate the distribution of the total score.
#We then pick a correct percentile to reflect the correct score that should be in logic.
#The score is logic is *much* lower than the actual maximum reachable score.



class Category:
    def __init__(self, name, mult = 1):
        self.name = name
        self.multiplicity = mult #how many times you have the category

    #return mean score of a category
    def meanScore(self, nbDice, nbRolls):
        if nbDice == 0 or nbRolls == 0:
            return 0
        meanScore = 0
        for key in yacht_weights[self.name, min(8,nbDice), min(8,nbRolls)]:
            meanScore += key*yacht_weights[self.name, min(8,nbDice), min(8,nbRolls)][key]/100000
        return meanScore



def extractProgression(state, player, options):
    #method to obtain a list of what items the player has.
    #this includes categories, dice, rolls and score multiplier.
    
    number_of_dice = (
        state.count("Dice", player) 
        + state.count("Dice Fragment", player) // options.number_of_dice_fragments_per_dice.value
    )

    number_of_rerolls = (
        state.count("Roll", player) 
        + state.count("Roll Fragment", player) // options.number_of_roll_fragments_per_roll.value
    )

    number_of_mults = state.count("Score Multiplier", player)
    
    
    score_mult = -10000
    if options.score_multiplier_type.value == 1: #fixed
        score_mult = 0.1 * number_of_mults
    if options.score_multiplier_type.value == 2: #step
        score_mult = 0.01 * number_of_mults
   
    categories = []
    
    for category_name, category_value in category_mappings.items():
        if state.count(category_name, player) >= 1:
            categories += [Category(category_value, state.count(category_name, player))] 
  
    extra_points_in_logic = state.count("1 Point", player)
    extra_points_in_logic += state.count("10 Points", player) * 10
    extra_points_in_logic += state.count("100 Points", player) * 100
    

    return [categories, number_of_dice, number_of_rerolls, score_mult, extra_points_in_logic]
    
#We will store the results of this function as it is called often for the same parameters.
yachtdice_cache = {}

#Function that returns the feasible score in logic based on items obtained.
def diceSimulationStrings(categories, nbDice, nbRolls, multiplier, diff, scoremulttype):
    tup = tuple([tuple(sorted([c.name+str(c.multiplicity) for c in categories])), nbDice, nbRolls, multiplier]) #identifier
    
    #if already computed, return the result
    if tup in yachtdice_cache.keys():
        return yachtdice_cache[tup]
    
    #sort categories because for the step multiplier, you will want low-scorig categories first
    categories.sort(key=lambda category: category.meanScore(nbDice, nbRolls))

    #function to add two discrete distribution.
    def add_distributions(dist1, dist2, mult):
        combined_dist = {}
        for val1, prob1 in dist1.items():
            for val2, prob2 in dist2.items():
                if int(val1 + val2 * mult) in combined_dist.keys():
                    combined_dist[int(val1 + val2 * mult)] += prob1 * prob2
                else:
                    combined_dist[int(val1 + val2 * mult)] = prob1 * prob2
        return combined_dist
    
    #function to take the maximum of 'times' i.i.d. dist1.
    def max_dist(dist1, times):
        new_dist = {0: 1}
        for _ in range(times):
            c = new_dist.copy()
            new_dist = {}
            for val1, prob1 in c.items():
                for val2, prob2 in dist1.items():
                    new_val = max(val1, val2)
                    new_prob = prob1 * prob2
                    
                    # Update the probability for the new value
                    if new_val in new_dist:
                        new_dist[new_val] += new_prob
                    else:
                        new_dist[new_val] = new_prob
            
        return new_dist

    #Returns percentile value of a distribution.
    def percentile_distribution(dist, percentile):
        sorted_values = sorted(dist.keys())
        cumulative_prob = 0
        prev_val = None
        
        for val in sorted_values:
            prev_val = val
            cumulative_prob += dist[val]
            if cumulative_prob >= percentile:
                return prev_val  # Return the value before reaching the desired percentile
            
        # Return the first value if percentile is lower than all probabilities
        return prev_val if prev_val is not None else sorted_values[0]  
            
    #calculate total distribution
    total_dist = {0: 1}
    for j in range(len(categories)):
        if nbDice == 0 or nbRolls == 0:
            dist = {0: 100000}
        else:
            dist = yacht_weights[categories[j].name, min(8,nbDice), min(8,nbRolls)].copy()
        
        for key in dist.keys():
            dist[key] /= 100000
            
            
        #for higher difficulties, the simulation gets multiple tries for categories.
        dist = max_dist(dist, max(1, len(categories) // (10 - 2*diff)))
        
        cur_mult = -100
        if scoremulttype == 1: #fixed
            cur_mult = multiplier
        if scoremulttype == 2: #step
            cur_mult = j * multiplier
        total_dist = add_distributions(total_dist, dist, (1 + cur_mult) * ( 2 ** (categories[j].multiplicity-1) ))
    
    #save result into the cache, then return it
    yachtdice_cache[tup] = math.floor(percentile_distribution(total_dist, .20 + diff/10))
    return yachtdice_cache[tup]

# Returns the feasible score that one can reach with the current state, options and difficulty.
def diceSimulation(state, player, options):
    categories, nbDice, nbRolls, multiplier, expoints = extractProgression(state, player, options)
    return diceSimulationStrings(categories, nbDice, nbRolls, multiplier, 
                                 options.game_difficulty.value, options.score_multiplier_type.value) + expoints
    
def calculateScoreInLogic(state, options):
    number_of_dice = (
        state.count("Dice") 
        + state.count("Dice Fragment") // options.number_of_dice_fragments_per_dice.value
    )

    number_of_rerolls = (
        state.count("Roll") 
        + state.count("Roll Fragment") // options.number_of_roll_fragments_per_roll.value
    )

    number_of_mults = state.count("Score Multiplier")
    
    
    score_mult = -10000
    if options.score_multiplier_type.value == 1: #fixed
        score_mult = 0.1 * number_of_mults
    if options.score_multiplier_type.value == 2: #step
        score_mult = 0.01 * number_of_mults
   
    categories = []

    for category_name, category_value in category_mappings.items():
        if state.count(category_name) >= 1:
            categories += [Category(category_value, state.count(category_name))]
    
    extra_points_in_logic = state.count("1 Point")
    extra_points_in_logic += state.count("10 Points") * 10
    extra_points_in_logic += state.count("100 Points") * 100
    
    return diceSimulationStrings(categories, number_of_dice, number_of_rerolls, score_mult, 
                                 options.game_difficulty.value, options.score_multiplier_type.value) + extra_points_in_logic

# Sets rules on entrances and advancements that are always applied
def set_yacht_rules(world: MultiWorld, player: int, options):
    for l in world.get_locations(player):
        set_rule(l, 
                    lambda state, 
                    curscore=l.yacht_dice_score, 
                    player=player: 
                    diceSimulation(state, player, options) >= curscore)

# Sets rules on completion condition
def set_yacht_completion_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: state.has("Victory", player)