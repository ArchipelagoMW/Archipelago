import logging
import os
import threading
import pkgutil
from typing import NamedTuple, Union, Dict, Any

import bsdiff4

import Utils
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import item_to_index, tier_1_opponents, booster_packs, excluded_items, Banlist_Items, core_booster
from .Locations import Bonuses, Limited_Duels, Theme_Duels, Campaign_Opponents, Required_Cards, \
    get_beat_challenge_events, special
from .Opponents import get_opponents, get_opponent_locations
from .Options import ygo06_options
from .Rom import YGO06DeltaPatch, get_base_rom_path
from .Rules import set_rules
from .logic import YuGiOh06Logic
from .BoosterPacks import booster_contents, get_booster_locations
from worlds.generic.Rules import add_rule
from .RomValues import structure_deck_selection, banlist_ids


class Yugioh06Web(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up Yu-Gi-Oh! - Ultimate Masters Edition - World Championship Tournament 2006"
        "for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rensen"]
    )

    tutorials = [setup]


class Yugioh06World(World):
    """

    """
    game = "Yu-Gi-Oh! 2006"
    data_version = 1
    web = Yugioh06Web()
    option_definitions = ygo06_options

    item_name_to_id = {}
    start_id = 5730000
    for k, v in item_to_index.items():
        item_name_to_id[k] = v + start_id

    location_name_to_id = {}
    start_id = 5730000
    for k, v in Bonuses.items():
        location_name_to_id[k] = v + start_id

    for k, v in Limited_Duels.items():
        location_name_to_id[k] = v + start_id

    for k, v in Theme_Duels.items():
        location_name_to_id[k] = v + start_id

    for k, v in Campaign_Opponents.items():
        location_name_to_id[k] = v + start_id

    for k, v in Required_Cards.items():
        location_name_to_id[k] = v + start_id

    for k, v in special.items():
        location_name_to_id[k] = v + start_id

    set_rules = set_rules

    item_name_groups = {
        "Core Booster": core_booster
    }

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
        item_pool = []
        for name in item_to_index:
            if name in excluded_items or name in start_inventory:
                continue
            item = Yugioh2006Item(
                name,
                ItemClassification.progression,
                self.item_name_to_id[name],
                self.player
            )
            item_pool.append(item)

        while len(item_pool) < len(self.location_name_to_id):
            item = Yugioh2006Item(
                "Money",
                ItemClassification.filler,
                self.item_name_to_id["Money"],
                self.player
            )
            item_pool.append(item)

        self.multiworld.itempool += item_pool

        for challenge in get_beat_challenge_events().keys():
            item = Yugioh2006Item(
                "Challenge Beaten",
                ItemClassification.progression,
                None,
                self.player
            )
            location = self.multiworld.get_location(challenge, self.player)
            location.place_locked_item(item)
            location.event = True

        for opponent in get_opponents(self.multiworld, self.player):
            for location_name, event in get_opponent_locations(opponent).items():
                if event is not None:
                    item = Yugioh2006Item(
                        event,
                        ItemClassification.progression,
                        None,
                        self.player
                    )
                    location = self.multiworld.get_location(location_name, self.player)
                    location.place_locked_item(item)
                    location.event = True

        for booster in booster_packs:
            for location_name, content in get_booster_locations(booster).items():
                item = Yugioh2006Item(
                    content,
                    ItemClassification.progression,
                    None,
                    self.player
                )
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(item)
                location.event = True

    def create_regions(self):
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, 'Menu', None, ['to Campaign', 'to Challenges', 'to Card Shop']),
            create_region(self.multiworld, self.player, 'Campaign', Bonuses | Campaign_Opponents),
            create_region(self.multiworld, self.player, 'Challenges'),
            create_region(self.multiworld, self.player, 'Card Shop', Required_Cards)
        ]

        self.multiworld.get_entrance('to Campaign', self.player) \
            .connect(self.multiworld.get_region('Campaign', self.player))
        self.multiworld.get_entrance('to Challenges', self.player) \
            .connect(self.multiworld.get_region('Challenges', self.player))
        self.multiworld.get_entrance('to Card Shop', self.player) \
            .connect(self.multiworld.get_region('Card Shop', self.player))

        campaign = self.multiworld.get_region('Campaign', self.player)
        # Campaign Opponents
        for opponent in get_opponents(self.multiworld, self.player):
            unlock_item = "Campaign Tier " + str(opponent.tier) + " Column " + str(opponent.column)
            region = create_region(self.multiworld, self.player,
                                   opponent.name, get_opponent_locations(opponent))
            entrance = Entrance(self.player, unlock_item, campaign)
            if opponent.tier == 5 and opponent.column == 3:
                entrance.access_rule =\
                    (lambda opp: lambda state:
                     state.has("Challenge Beaten", self.player,
                               self.multiworld.ThirdTier5CampaignBossChallenges[self.player].value) and
                               opp.rule(state))(opponent)
            elif opponent.tier == 5 and opponent.column == 4:
                entrance.access_rule =\
                    (lambda opp: lambda state:
                     state.has("Challenge Beaten", self.player,
                               self.multiworld.FourthTier5CampaignBossChallenges[self.player].value) and
                     opp.rule(state))(opponent)
            elif opponent.tier == 5 and opponent.column == 5:
                entrance.access_rule =\
                    (lambda opp: lambda state: state.has("Challenge Beaten", self.player,
                     self.multiworld.FinalCampaignBossChallenges[self.player].value) and opp.rule(state))(opponent)
            else:
                entrance.access_rule = (lambda unlock, opp: lambda state:
                                        state.has(unlock, self.player) and opp.rule(state))(unlock_item, opponent)
            campaign.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        card_shop = self.multiworld.get_region('Card Shop', self.player)
        # Booster Contents
        for booster in booster_packs:
            region = create_region(self.multiworld, self.player,
                                   booster, get_booster_locations(booster))
            entrance = Entrance(self.player, booster, card_shop)
            entrance.access_rule = (lambda unlock: lambda state: state.has(unlock, self.player))(booster)
            campaign.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        challenges = self.multiworld.get_region('Challenges', self.player)
        # Challenges
        for challenge, lid in (Limited_Duels | Theme_Duels).items():
            region = create_region(self.multiworld, self.player,
                                   challenge, {challenge: lid, challenge + " Complete": None})
            entrance = Entrance(self.player, challenge, card_shop)
            entrance.access_rule = (lambda unlock: lambda state:
                                    state.has(unlock + " Unlock", self.player))(challenge)
            challenges.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

    def generate_early(self):
        starting_opponent = self.multiworld.random.choice(tier_1_opponents)
        self.multiworld.start_inventory[self.player].value[starting_opponent] = 1
        starting_pack = self.multiworld.random.choice(booster_packs)
        self.multiworld.start_inventory[self.player].value[starting_pack] = 1
        banlist = self.multiworld.Banlist[self.player]
        self.multiworld.start_inventory[self.player].value[Banlist_Items.get(banlist)] = 1

    def apply_base_path(self, rom):
        base_patch_location = os.path.dirname(__file__) + "/patch.bsdiff4"
        with open(base_patch_location, "rb") as base_patch:
            rom_data = bsdiff4.patch(rom.read(), base_patch.read())
        rom_data = bytearray(rom_data)
        return rom_data

    def apply_randomizer(self):
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = self.apply_base_path(rom)

        structure_deck = self.multiworld.StructureDeck[self.player]
        structure_deck_data_location = 0x000fd0aa
        rom_data[structure_deck_data_location] = structure_deck_selection.get(structure_deck.value)
        banlist = self.multiworld.Banlist[self.player]
        banlist_data_location = 0xf4496
        rom_data[banlist_data_location] = banlist_ids.get(banlist.value)
        randomizer_data_start = 0x0000f310
        for location in self.multiworld.get_locations():
            item = location.item.name
            if location.item.player != self.player:
                item = "Remote"
            item_id = item_to_index.get(item)
            if item_id is None:
                continue
            location_id = self.location_name_to_id[location.name] - 5730000
            rom_data[randomizer_data_start + location_id] = item_id
        return rom_data

    def generate_output(self, output_directory: str):
        patched_rom = self.apply_randomizer()
        outfilebase = 'AP_' + self.multiworld.seed_name
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.gba')
        self.rom_name_text = f'YGO06{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, 'utf8')[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        patched_rom[0x10:0x30] = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], 'utf8')[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        patched_rom[0x30:0x50] = self.playerName
        patched_filename = os.path.join(output_directory, outputFilename)
        with open(patched_filename, 'wb') as patched_rom_file:
            patched_rom_file.write(patched_rom)
        patch = YGO06DeltaPatch(os.path.splitext(outputFilename)[0] + YGO06DeltaPatch.patch_file_ending,
                                player=self.player,
                                player_name=self.multiworld.player_name[self.player],
                                patched_path=outputFilename)
        patch.write()
        os.unlink(patched_filename)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name, lid in locations.items():
            location = Yugioh2006Location(player, location_name, lid, region)
            if locations[location_name] is None:
                location.event = True
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))
    return region


class Yugioh2006Item(Item):
    game = "Yu-Gi-Oh! 2006"


class Yugioh2006Location(Location):
    game: str = "Yu-Gi-Oh! 2006"
