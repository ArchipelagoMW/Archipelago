from BaseClasses import Item
import typing
import random
import copy
from .Constants import *
from .Options import *


class OpenRCT2Item(Item):
    game: str = "OpenRCT2"



def set_openRCT2_items(scenario, rules, monopoly_mode, include_gamespeed_items, furry_convention_traps, spam_traps, bathroom_traps, skips, filler, atm, first_aid):
    # print("\nThis is the selected scenario:")
    # print(scenario)
    # print("And these items will be randomized:")
    # print(Scenario_Items[scenario])
    openRCT2_items = copy.deepcopy(Scenario_Items[scenario])
    
    if atm:
        if "Cash Machine" not in openRCT2_items:
            openRCT2_items.append("Cash Machine")

    if first_aid:
        if "First Aid" not in openRCT2_items:
            openRCT2_items.append("First Aid")

    if monopoly_mode:
        count = 0
        while count < 20:
            openRCT2_items.append("Land Discount")
            openRCT2_items.append("Construction Rights Discount")
            count += 1
            
    if include_gamespeed_items:
        count = 0
        while count < 4:
            openRCT2_items.append("Progressive Speed")
            count += 1

    count = 0
    while count < furry_convention_traps:
        openRCT2_items.append("Furry Convention Trap")
        count += 1
    count = 0
    while count < spam_traps:
        openRCT2_items.append("Spam Trap")
        count +=1
    count = 0
    while count < bathroom_traps:
        openRCT2_items.append("Bathroom Trap")
        count +=1
    count = 0
    while count < skips:
        openRCT2_items.append("Skip")
        count +=1

    for number, rule in enumerate(item_info["park_rules"]):#Check every rule type
        if rules[number] == 1:#If it's enabled and can be disabled
            openRCT2_items.append(rule)#Add an item to disable

    filler_count = len(openRCT2_items) * (filler * .01) - 1
    count = 0
    while count < filler_count:
        rarity = random.random()
        if rarity < .6:
            openRCT2_items.append(random.choice(item_info["filler_common"]))
        elif rarity < .9:
            openRCT2_items.append(random.choice(item_info["filler_uncommon"]))
        else:
            openRCT2_items.append(random.choice(item_info["filler_rare"]))
        count += 1

    openRCT2_items.append("Beauty Contest")
    
    item_table = {name: [base_id + count, True] for count, name in enumerate(openRCT2_items)}
    item_frequency = {}
    for ride in openRCT2_items:
        found = False
        for item in item_frequency:
            if ride == item:
                item_frequency[item] += 1
                found = True
                break
        if not found:
            item_frequency[ride] = 1

    # print("Here's the generated item table and frequency table")
    # print(item_table)
    # print("\n\n")
    # print(item_frequency)

    return[item_table,item_frequency]
