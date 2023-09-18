from BaseClasses import Item
import typing
import random
from .Constants import *
from .Options import *


class OpenRCT2Item(Item):
    game: str = "OpenRCT2"



def set_openRCT2_items(monopoly_mode, furry_convention_traps, spam_traps, bathroom_traps, park_rules, filler):
    openRCT2_items = ForestFrontiers
    
    if monopoly_mode:
        count = 0
        while count < 20:
            openRCT2_items.append("Land Discount")
            openRCT2_items.append("Construction Rights Discount")
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

    if park_rules:
        for rule in item_info["park_rules"]:
            openRCT2_items.append(rule)

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

    print("Here's the generated item table and frequency table")
    print(item_table)
    print("\n\n")
    print(item_frequency)

    return[item_table,item_frequency]
