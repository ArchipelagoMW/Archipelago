import json
import os
import pkgutil
from pathlib import Path

from .. import args as args
from ..memory.space import Bank, Space, Reserve, Allocate, Free, Write, Read
from ..data import direction as direction

from ..data import event_bit as event_bit
from ..data import event_word as event_word
from ..data import npc_bit as npc_bit
from ..data import battle_bit as battle_bit

from ..instruction import asm as asm
from ..instruction import field as field
from ..instruction.field import entity as field_entity
from ..instruction import world as world
from ..instruction import vehicle as vehicle

from ..instruction.event import EVENT_CODE_START
from ..event.event_reward import RewardType, Reward

class Event():
    if args.ap_data:
        file = pkgutil.get_data("worlds.ff6wc", "location_equivalences.json").decode('utf-8')
        location_equivalencies = json.loads(file)

    def __init__(self, events, rom, args, dialogs, characters, items, maps, enemies, espers, shops):
        self.events = events
        self.rom = rom
        self.args = args
        self.dialogs = dialogs
        self.characters = characters
        self.items = items
        self.maps = maps
        self.enemies = enemies
        self.espers = espers
        self.shops = shops
        self.rewards = []

        self.rewards_log = []
        self.changes_log = []
        self.aliases = []
        self.planned_reward_index = 0

    def name(self):
        raise NotImplementedError(self.__class__.__name__ + " event name")

    def character_gate(self):
        return None

    def characters_required(self):
        return 1

    def add_reward(self, possible_types):
        if args.ap_data and self.name() in Event.location_equivalencies.keys():
            ap_name = Event.location_equivalencies[self.name()][self.planned_reward_index]
            ap_index = self.planned_reward_index
            self.planned_reward_index += 1
            new_reward = Reward(self, RewardType.ARCHIPELAGO, ap_name, ap_index)
        else:
            new_reward = Reward(self, possible_types)
        self.rewards.append(new_reward)
        return new_reward

    def init_rewards(self):
        pass

    def init_event_bits(self, space):
        pass

    def get_boss(self, original_boss_name, log_change = True):
        pack_id = self.enemies.get_event_boss(original_boss_name)

        if (self.args.boss_battles_shuffle or self.args.boss_battles_random) and log_change:
            boss_name = self.enemies.packs.get_name(pack_id)
            self.log_change(original_boss_name, boss_name)
        return pack_id

    # return the boss in place of the given boss_name
    # example
    # get_replacement_formation("Goddess")
    # if you fight Ultros in the Goddess location, return Ultros
    def get_replacement_formation(self, boss_name):
        from ..data.bosses import pack_name
        replacement = self.get_boss(boss_name, False)
        location_boss = pack_name[replacement]
        formation_id = self.enemies.formations.get_id(location_boss)
        return self.enemies.formations.formations[formation_id]

    def log_reward(self, reward, prefix = "", suffix = ""):
        reward_string = prefix
        if reward.type == RewardType.CHARACTER:
            reward_string += self.characters.get_name(reward.id)
        elif reward.type == RewardType.ESPER:
            reward_string += self.espers.get_name(reward.id)
        elif reward.type == RewardType.ITEM:
            reward_string += self.items.get_name(reward.id)
        self.rewards_log.append(reward_string + suffix)

    def log_change(self, original, new):
        self.changes_log.append(f"    {original:<14} -> {new}")

    def log_string(self):
        log_string = f"{self.name():<30}"
        if self.rewards_log:
            log_string += f" {', '.join(self.rewards_log)}"
        if self.changes_log:
            log_string += '\n' + '\n'.join(self.changes_log)
        return log_string

    def mod(self):
        raise NotImplementedError(self.__class__.__name__ + " event must implement mod")
