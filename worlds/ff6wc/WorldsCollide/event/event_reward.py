import json
import os
import pkgutil
from pathlib import Path
from enum import Flag, unique, auto
from .. import args as args
from ..constants import items
from ..data.characters import Characters
from .. import constants as constants


@unique
class RewardType(Flag):
    NONE = auto()
    CHARACTER = auto()
    ESPER = auto()
    ITEM = auto()
    ARCHIPELAGO = auto()

CHARACTER_ESPER_ONLY_REWARDS = 6
class Reward:
    if args.ap_data:
        file = pkgutil.get_data("worlds.ff6wc", "location_equivalences.json").decode('utf-8')
        location_equivalencies = json.loads(file)

    def __init__(self, event, possible_types, ap_name="", ap_index=""):
        self.id = None
        self.type = None
        self.event = event
        self.possible_types = possible_types
        self.ap_name = ap_name
        self.ap_index = ap_index

    def single_possible_type(self):
        return self.possible_types in RewardType

    def __str__(self):
        result = f"{self.id} {self.type} {self.event.name()}"

        possible_strings = []
        if self.possible_types & RewardType.CHARACTER:
            possible_strings.append("Character")
        if self.possible_types & RewardType.ESPER:
            possible_strings.append("Esper")
        if self.possible_types & RewardType.ITEM:
            possible_strings.append("Item")

        return result + " (" + ', '.join(possible_strings) + ")"


def choose_reward(possible_types: RewardType, characters: Characters, espers, items, ap_reward: Reward = None):
    import random

    all_types = [flag for flag in RewardType]
    random.shuffle(all_types)

    item_possible = False
    for reward_type in all_types:
        if reward_type & possible_types:
            if reward_type == RewardType.CHARACTER and characters.get_available_count():
                return (characters.get_random_available(), reward_type)
            elif reward_type == RewardType.ESPER and espers.available():
                return (espers.get_random_esper(), reward_type)
            elif reward_type == RewardType.ITEM:
                item_possible = True
            elif reward_type == RewardType.ARCHIPELAGO:
                reward = args.ap_data[ap_reward.ap_name]
                if reward == "Archipelago Item":
                    return (constants.items.name_id["ArchplgoItem"], RewardType.ITEM)
                if reward == "Ragnarok Sword":
                    return (constants.items.name_id["Ragnarok"], RewardType.ITEM)
                if reward == "Ragnarok Esper":
                    return (espers.get_specific_esper("Ragnarok"), RewardType.ESPER)
                if str.upper(reward) in Characters.DEFAULT_NAME:
                    return (characters.get_specific_character(reward), RewardType.CHARACTER)
                elif reward in constants.items.good_items:
                    return (constants.items.name_id[reward], RewardType.ITEM)
                elif reward in constants.items.name_id.keys():
                    return (constants.items.name_id[reward], RewardType.ITEM)
                else:
                    return (espers.get_specific_esper(reward), RewardType.ESPER)

    # tried all possible_rewards and none were available
    # probably running out of chars and espers and need to make item rewards possible for more events
    assert(item_possible)
    return (items.get_good_random(), RewardType.ITEM)

# weight reward slots based on how long they have been in the reward pool (longer means lower odds)
# the first events unlocked will have more chances to be picked, this balances it somewhat by lowering their odds each time they aren't picked
# specifically, when an event is added to the pool it is twice as likely to be picked as an event added in the previous iteration
# e.g. 4 slots in pool, a has been in for 2 picks, b has been in for 1 pick and c,d have been in for 0 picks
# a should have half the weight of b which should have half the weight of c and d
# a + b + c + d = 1.0
# a + 2a + 4a + 4a = 1.0        11a = 1.0   a = 0.0909
# 0.5b + b + 2b + 2b = 1.0     5.5b = 1.0   b = 0.1818
# 0.25c + 0.5c + c + c = 1.0  2.75c = 1.0   c = 0.3636 # and same for d
def reward_slot_weight(slot_iterations, slot, iteration):
    csum = 0
    cmod = 2**(iteration - slot_iterations[slot])
    for s in slot_iterations:
        csum += 2**(iteration - s) / cmod
    return 1 / csum

# generate weights for each slot based on its number of iterations
def reward_slot_weights(slot_iterations, iteration):
    slot_weights = []
    for x in range(len(slot_iterations)):
        slot_weights.append(reward_slot_weight(slot_iterations, x, iteration))
    return slot_weights

# return index of randomly chosen (biased) slots
# https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_reward_choice(slot_iterations, iteration):
    weights = reward_slot_weights(slot_iterations, iteration)

    from ..ff6wcutils.weighted_random import weighted_random
    return weighted_random(weights)
