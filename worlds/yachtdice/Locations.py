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
        self.event = not address

all_locations = {}
starting_index = 16871244500 #500 more than the startin index for items

#Function that is called when this file is loaded, which loads in ALL possible locations, score 1 to 1000
def all_locations_fun(max_score):
    location_table = {}
    for i in range(max_score+1):
        location_table[f"{i} score"] = LocData(starting_index+i, "Board", i)
    return location_table

#function that loads in all locations necessary for the game, so based on options.
def ini_locations(max_score, num_locs, dif):    
    location_table = {}
    
    scaling = 2 #parameter that determines how many low-score location there are.
    #need more low-score locations or lower difficulties:
    if dif == 1:
        scaling = 3 
    elif dif == 2:
        scaling = 2.2

    #the scores follow the function int( 1 + (perc ** scaling) * (max_score-1) )
    #however, this will have many low values, sometimes repeating.
    #to avoid repeating scores, hiscore keeps tracks of the highest score location
    #and the next score will always be at least hiscore + 1
    #note that curscore is at most max_score-1
    hiscore = 0
    for i in range(num_locs):
        perc = (i/num_locs)
        curscore = int( 1 + (perc ** scaling) * (max_score-2) )
        if(curscore <= hiscore):
            curscore = hiscore + 1
        hiscore = curscore
        location_table[f"{curscore} score"] = LocData(starting_index + curscore, "Board", curscore)
        
    #Finally, add a check for the actual max_score. 
    #This is *not* counted in num_locs, since the victory items is not as well.
    location_table[f"{max_score} score"] = LocData(starting_index + max_score, "Board", max_score)

    return location_table

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in all_locations.items() if data.id}

# we need to run this function to initialize all scores from 1 to 1000, even though not all are used
# this in order to make sure no other worlds use any ids that are similar to Yacht Dice
all_locations = all_locations_fun(1000) 
