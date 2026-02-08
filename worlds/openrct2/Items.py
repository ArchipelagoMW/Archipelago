from BaseClasses import Item
import copy
from .Constants import Scenario_Items
from .data.item_info import item_info
from .Options import *
from random import Random
from typing import Tuple


class OpenRCT2Item(Item):
    game: str = "OpenRCT2"


def set_openRCT2_items(options: openRCT2Options, random: Random) -> tuple[list[str],str]:
    # print("\nThis is the selected scenario:")
    # print(scenario)
    # print("And these items will be randomized:")
    # print(Scenario_Items[scenario])
    if(options.all_rides_and_scenery_expansion):
        openRCT2_items = copy.deepcopy(Scenario_Items[152]) # Archipelago Madness has every ride in the game. We can go off that
    elif(options.all_rides_and_scenery_base):
        openRCT2_items = copy.deepcopy(Scenario_Items[151]) # Archipelago Madness, but without the expansion stuff
    else:
        openRCT2_items = copy.deepcopy(Scenario_Items[options.scenario.value])
    rules = [options.difficult_guest_generation.value,
                 options.difficult_park_rating.value,
                 options.forbid_high_construction.value,
                 options.forbid_landscape_changes.value,
                 options.forbid_marketing_campaigns.value,
                 options.forbid_tree_removal.value]

    locked = 2 # For clarity in the next if statement

    if options.forbid_high_construction == locked:
        for item in openRCT2_items:
            if item in item_info["requires_height"]:
                openRCT2_items.remove(item)

    if options.include_atm:
        if "Cash Machine" not in openRCT2_items:
            openRCT2_items.append("Cash Machine")

    if options.include_first_aid:
        if "First Aid" not in openRCT2_items:
            openRCT2_items.append("First Aid")

    if ("Log Flume" not in openRCT2_items): # Necessary to not break the Best Water Rides location
        openRCT2_items.append("Log Flume")

    if ("Merry Go Round" not in openRCT2_items): # Necessary to not break the Best Gentle Rides location
        openRCT2_items.append("Merry Go Round")

    if options.monopoly_mode.value:
        for each in range(20):
            openRCT2_items.append("Land Discount")
            openRCT2_items.append("Construction Rights Discount")
                      
    if options.include_gamespeed_items.value:
        for each in range(4):
            openRCT2_items.append("Progressive Speed")

    for each in range(options.furry_convention_traps.value):
        openRCT2_items.append("Furry Convention Trap")

    for each in range(options.spam_traps.value):
        openRCT2_items.append("Spam Trap")

    for each in range(options.bathroom_traps.value):
        openRCT2_items.append("Bathroom Trap")

    for each in range(options.loan_shark_traps.value):
        openRCT2_items.append("Loan Shark Trap")

    for each in range(options.food_poisioning_traps.value):
        openRCT2_items.append("Food Poisioning Trap")

    for each in range(options.skips.value):
        openRCT2_items.append("Skip")

    unlockable = 1 # For clairity in the next loop

    for number, rule in enumerate(item_info["park_rules"]):  # Check every rule type
        if rules[number] == unlockable:  # If it's enabled and can be disabled
            openRCT2_items.append(rule)  # Add an item to disable

    # Adds some useful filler items. 15 is the absolute minimum to not break generation.
    count = 0
    while count < 15:
        openRCT2_items.append(random.choice(item_info["useful_filler_items"]))
        count += 1

    # Add extra traps if there's not enough for the negative awards.
    if options.awards == 0: # 0: all awards
        #Add extra traps if there's fewer than 5.
        if(sum(1 for item in openRCT2_items if item in item_info["trap_items"]) < 5):
            openRCT2_items.append("Bathroom Trap")
            openRCT2_items.append("Furry Convention Trap")
            openRCT2_items.append("Food Poisioning Trap")
            openRCT2_items.append("Spam Trap")
            openRCT2_items.append("Loan Shark Trap")

    filler = options.filler.value

    filler_count = len(openRCT2_items) * (filler * .01) - 1
    for _ in range(int(filler_count)):
        rarity = random.random()
        if rarity < .6:
            openRCT2_items.append(random.choice(item_info["filler_common"]))
        elif rarity < .9:
            openRCT2_items.append(random.choice(item_info["filler_uncommon"]))
        else:
            openRCT2_items.append(random.choice(item_info["filler_rare"]))

    openRCT2_items.append("Beauty Contest") #Every park has a beauty contest award. You are beautiful!
    
    # print(openRCT2_items)

    # handles the starting ride
    candidate_list = [item for item in openRCT2_items if item in item_info["Rides"] and item not in item_info["non_starters"]]  
    candidate = random.choice(candidate_list)
    starting_ride: str = candidate
    openRCT2_items.remove(candidate)
    
    # print("Here's the starting ride!")
    # print(starting_ride)

    return openRCT2_items, starting_ride
