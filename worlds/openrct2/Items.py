from BaseClasses import Item
import typing
import copy
from .Constants import item_info, Scenario_Items
from .Options import *


class OpenRCT2Item(Item):
    game: str = "OpenRCT2"



def set_openRCT2_items(world):
    # print("\nThis is the selected scenario:")
    # print(scenario)
    # print("And these items will be randomized:")
    # print(Scenario_Items[scenario])
    openRCT2_items = copy.deepcopy(Scenario_Items[world.options.scenario.value])
    rules = [world.options.difficult_guest_generation.value,
                 world.options.difficult_park_rating.value,
                 world.options.forbid_high_construction.value,
                 world.options.forbid_landscape_changes.value,
                 world.options.forbid_marketing_campaigns.value,
                 world.options.forbid_tree_removal.value]

    if world.options.include_atm:
        if "Cash Machine" not in openRCT2_items:
            openRCT2_items.append("Cash Machine")

    if world.options.include_first_aid:
        if "First Aid" not in openRCT2_items:
            openRCT2_items.append("First Aid")

    if world.options.monopoly_mode.value:
        for each in range(20):
            openRCT2_items.append("Land Discount")
            openRCT2_items.append("Construction Rights Discount")
                      
    if world.options.include_gamespeed_items.value:
        for each in range(4):
            openRCT2_items.append("Progressive Speed")

    for each in range(world.options.furry_convention_traps.value):
        openRCT2_items.append("Furry Convention Trap")

    for each in range(world.options.spam_traps.value):
        openRCT2_items.append("Spam Trap")
    for each in range(world.options.bathroom_traps.value):
        openRCT2_items.append("Bathroom Trap")
    for each in range(world.options.skips.value):
        openRCT2_items.append("Skip")

    for number, rule in enumerate(item_info["park_rules"]):  # Check every rule type
        if rules[number] == 1:  # If it's enabled and can be disabled
            openRCT2_items.append(rule)  # Add an item to disable

    filler = world.options.filler.value

    filler_count = len(openRCT2_items) * (filler * .01) - 1
    count = 0
    while count < filler_count:
        rarity = world.random.random()
        if rarity < .6:
            openRCT2_items.append(world.random.choice(item_info["filler_common"]))
        elif rarity < .9:
            openRCT2_items.append(world.random.choice(item_info["filler_uncommon"]))
        else:
            openRCT2_items.append(world.random.choice(item_info["filler_rare"]))
        count += 1

    openRCT2_items.append("Beauty Contest")
    
    # print(openRCT2_items)

    # handles the starting ride
    found_starter = False
    while not found_starter:
        candidate_list = [item for item in openRCT2_items if item in item_info["rides"] and item not in item_info["non_starters"]]  
        candidate = world.random.choice(candidate_list)  
        starting_ride = candidate
        openRCT2_items.remove(candidate)
        found_starter = True
    
    # print("Here's the starting ride!")
    # print(starting_ride)

    return openRCT2_items, starting_ride
