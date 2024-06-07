from BaseClasses import Location
import typing

class LocData(typing.NamedTuple):
    id: int
    region: str
    score: int

class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, score: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.yacht_dice_score = score

all_locations = {}
starting_index = 16871244500 #500 more than the starting index for items

#Function that is called when this file is loaded, which loads in ALL possible locations, score 1 to 1000
def all_locations_fun(max_score):
    location_table = {}
    for i in range(max_score+1):
        location_table[f"{i} score"] = LocData(starting_index+i, "Board", i)
    return location_table

#function that loads in all locations necessary for the game, so based on options.
#will make sure that goal_score and max_score are included locations
def ini_locations(goal_score, max_score, num_locs, dif):      
    scaling = 2 #parameter that determines how many low-score location there are.
    #need more low-score locations or lower difficulties:
    if dif == 1:
        scaling = 3 
    elif dif == 2:
        scaling = 2.3

    scores = []
    #the scores follow the function int( 1 + (perc ** scaling) * (max_score-1) )
    #however, this will have many low values, sometimes repeating.
    #to avoid repeating scores, hiscore keeps tracks of the highest score location
    #and the next score will always be at least hiscore + 1
    #note that curscore is at most max_score-1
    hiscore = 0
    for i in range(num_locs - 1):
        perc = (i/num_locs)
        curscore = int(1 + (perc ** scaling) * (max_score-2))
        if curscore <= hiscore:
            curscore = hiscore + 1
        hiscore = curscore
        scores += [curscore]
    
    if goal_score != max_score:
        #if the goal score is not in the list, find the closest one and make it the goal.
        if goal_score not in scores:
            closest_num = min(scores, key=lambda x: abs(x - 500))
            scores[scores.index(closest_num)] = goal_score
        
    scores += [max_score]
    
    location_table = {f"{score} score": LocData(starting_index + score, "Board", score) for score in scores}

    return location_table, scores.index(goal_score)

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in all_locations.items() if data.id}

# we need to run this function to initialize all scores from 1 to 1000, even though not all are used
all_locations = all_locations_fun(1000) 
