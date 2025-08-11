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
    tips_pair = create_hint_lookup(self, self.tip_locations, valid_tip_items)
    #Remove any items you've already gotten from being hints from the chicken
    for each_item in tips_pair[0]:
        if each_item in valid_chicken_items:
            valid_chicken_items.remove(each_item)
    #Chicken Hints
    chicken_locations = []
    for each_index in range(7):
        chicken_locations.append("Chicken Hint " + str(each_index + 1))
    chicken_hints = create_hint_lookup(self, chicken_locations, valid_tip_items)[1]
    
    #TODO: Make Balanced Hints actually balanced

    #Apply the hints to the world
    return [tips_pair[1], chicken_hints]

def create_hint_lookup(self, hint_locations : list[str], valid_items : list[Item]):
    hint_lookup : dict[str, Location] = {}
    newly_chosen_items : list[Item] = []
    for each_tip_spot in hint_locations:
        if len(valid_items) > 0:
            next_item : Item = self.random.choice(valid_items)
            valid_items.remove(next_item)
            newly_chosen_items.append(next_item)
            to_scout : Location = next_item.location
            hint_lookup[each_tip_spot] = to_scout
        else:
            break
    return [newly_chosen_items, hint_lookup]

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