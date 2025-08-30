from .Options import MrHints, ChickenHints
from BaseClasses import Item, ItemClassification, Location

def create_hints(self):
    #Mr. Hints
    tip_catagories = get_catagories(self.options.mr_hints, MrHints)
    valid_tip_items = get_valid_items(self, tip_catagories)
    #Chicken Hints
    chicken_catagories = get_catagories(self.options.chicken_hints, ChickenHints)
    valid_chicken_items = get_valid_items(self, chicken_catagories)

    #Get Mr. Tip Hints First
    tips_pair = create_hint_lookup(self, self.tip_locations, valid_tip_items, tip_catagories, self.options.mr_hints == 2, "Mr. Tip Says:\n")
    #Remove any items you've already gotten from being hints from the chicken
    for each_item in tips_pair[0]:
        if each_item in valid_chicken_items:
            valid_chicken_items.remove(each_item)
    #Chicken Hints
    chicken_locations = []
    for each_index in range(7):
        chicken_locations.append("Chicken Hint " + str(each_index + 1))
    chicken_hints = create_hint_lookup(self, chicken_locations, valid_chicken_items, chicken_catagories, self.options.chicken_hints == 2, "Cheat Chicken Says:\n")[1]
    
    #Apply the hints to the world
    return [tips_pair[1], chicken_hints]

def create_hint_lookup(self, hint_locations : list[str], valid_items : list[Item], valid_catagories : list [ItemClassification], vague_hint : bool, vauge_prefix : str):
    hint_lookup : dict[str, dict[str,int]] = {}
    newly_chosen_items : list[Item] = []
    #If there's multiple valid catagories, we're in balanced mode
    if len(valid_catagories) > 1:
        valid_item_catagories : dict[ItemClassification:list[Item]] = {}
        grabbed_from_catagory : dict[ItemClassification:int] = {}
        for each_classification in valid_catagories:
            valid_item_catagories[each_classification] = get_valid_items(self, [each_classification])
            grabbed_from_catagory[each_classification] = 0
        current_catagory : ItemClassification
        for each_tip_spot in hint_locations:
            #Get the catagory with the lowest value
            lowest_value = 999
            for each_catagory, catagory_value in grabbed_from_catagory.items():
                if catagory_value < lowest_value:
                    lowest_value = catagory_value
                    current_catagory = each_catagory
            if len([valid_item_catagories[current_catagory]]) > 0:
                next_item : Item = self.random.choice(valid_item_catagories[current_catagory])
                valid_item_catagories[current_catagory].remove(next_item)
                newly_chosen_items.append(next_item)
                to_scout : Location = next_item.location
                hint_lookup[location_name_to_address(self, each_tip_spot)] = location_to_hint_info(self, vague_hint, to_scout, next_item, vauge_prefix)
                grabbed_from_catagory[current_catagory] += 1
            else:
                #If this catagory has no more items, remove it
                del grabbed_from_catagory[current_catagory]
                #If no catagories have items, bail
                if len(grabbed_from_catagory) == 0:
                    break
        return [newly_chosen_items, hint_lookup]
    #Otherwise, just grab from the single catagory
    for each_tip_spot in hint_locations:
        if len(valid_items) > 0:
            next_item : Item = self.random.choice(valid_items)
            valid_items.remove(next_item)
            newly_chosen_items.append(next_item)
            to_scout : Location = next_item.location
            hint_lookup[location_name_to_address(self, each_tip_spot)] = location_to_hint_info(self, vague_hint, to_scout, next_item, vauge_prefix)
        else:
            break
    return [newly_chosen_items, hint_lookup]

def location_to_hint_info(self, vague_hint : bool, in_location : Location, in_item : Item, vauge_prefix : str) -> dict[str:str]:
    hint : dict[str:str] = {
        "player_id" : in_location.player,
        "location_id" : in_location.address
    }
    if vague_hint:
        hint_text = in_location.hint_text.removeprefix("at ")
        item_class = " " + str(in_item.classification.value) + " "
        locations_owner = self.multiworld.player_name[in_location.player]
        item_owner = self.multiworld.player_name[in_item.player]
        match in_item.classification.value:
            #Filler
            case 0:
                item_class = " won't do much for "
            #Progression
            case 1:
                item_class = " is important for "
            #Useful
            case 2:
                item_class = " would help "
            #Useful Progression
            case 3:
                item_class = " is critical for "
            #Trap
            case 4:
                item_class = " will hurt "
            #
            case 25:
                item_class = " is good for "
            
            case 9:
                item_class = " is important for "
            
            case 17:
                item_class = " is good for "
        hint["vague_hint"] = vauge_prefix + locations_owner + "'s " + hint_text + item_class + item_owner
    return hint

def location_name_to_address(self, location_name : str) -> str:
    if location_name.startswith("Chicken Hint "):
        return location_name.removeprefix("Chicken Hint ")
    return str(self.multiworld.get_location(location_name, self.player).address)

def get_catagories(set_option, option_origin) -> list[ItemClassification] | None:
    match set_option:
        case option_origin.option_off:
            #No Hints
            return None
        case option_origin.option_catagory_only:
            #Vauge Hints
            return []
        case option_origin.option_chaos:
            #Any items
            return []
        case option_origin.option_balanced:
            #Tries to keep a bit of all types
            return [ItemClassification.trap, ItemClassification.useful, ItemClassification.progression]
        case option_origin.option_traps:
            #Traps
            return [ItemClassification.trap]
        case option_origin.option_useful:
            #Useful
            return [ItemClassification.useful]
        case option_origin.option_progression:
            #Progression
            return [ItemClassification.progression]

def get_valid_items(self, item_classes : list[ItemClassification] | None) -> list[Item]:
    #No items
    if item_classes == None:
        return []
    #All items are valid choices
    if item_classes == []:
        return self.multiworld.itempool.copy()
    #Only items from the catagory are valid choices
    valid_items : list[Item] = []
    for each_item in self.multiworld.itempool:
        if each_item.classification in item_classes:
            valid_items.append(each_item)
    return valid_items