import os
from typing import ClassVar, Dict, Any

import bsdiff4
import math
import settings

import Utils
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .utils import openFile
from ..AutoWorld import World, WebWorld
from .Items import item_to_index, tier_1_opponents, booster_packs, excluded_items, Banlist_Items, core_booster, \
    challenges, useful, draft_boosters, draft_opponents
from .Locations import Bonuses, Limited_Duels, Theme_Duels, Campaign_Opponents, Required_Cards, \
    get_beat_challenge_events, special, collection_events
from .Opponents import get_opponents, get_opponent_locations, challenge_opponents
from .Options import Yugioh06Options
from .Rom import YGO06DeltaPatch, get_base_rom_path, MD5Europe, MD5America
from .Rules import set_rules
from .logic import YuGiOh06Logic
from .BoosterPacks import booster_contents, get_booster_locations
from .StructureDeck import get_deck_content_locations
from .RomValues import structure_deck_selection, banlist_ids, function_addresses
from .Client_bh import YuGiOh2006Client


class Yugioh06Web(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up Yu-Gi-Oh! - Ultimate Masters Edition - World Championship Tournament 2006 "
        "for Archipelago on your computer.",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["Rensen"]
    )
    tutorials = [setup]


class Yugioh2006Setting(settings.Group):
    class Yugioh2006RomFile(settings.UserFilePath):
        """File name of your Yu-Gi-Oh 2006 ROM"""
        description = "Yu-Gi-Oh 2006 ROM File"
        copy_to = "YuGiOh06.gba"
        md5s = [MD5Europe, MD5America]

    rom_file: Yugioh2006RomFile = Yugioh2006RomFile(Yugioh2006RomFile.copy_to)


class Yugioh06World(World):
    """
    Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006 is the definitive Yu-Gi-Oh
    simulator on the GBA. Featuring over 2000 cards and over 90 Challenges.
    """
    game = "Yu-Gi-Oh! 2006"
    data_version = 1
    web = Yugioh06Web()
    options: Yugioh06Options
    options_dataclass = Yugioh06Options
    settings_key = "yugioh06_settings"
    settings: ClassVar[Yugioh2006Setting]

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

    item_name_to_id = {}
    start_id = 5730000
    for k, v in item_to_index.items():
        item_name_to_id[k] = v + start_id

    location_name_to_id = {}
    for k, v in Bonuses.items():
        location_name_to_id[k] = v + start_id

    for k, v in Limited_Duels.items():
        location_name_to_id[k] = v + start_id

    for k, v in Theme_Duels.items():
        location_name_to_id[k] = v + start_id

    for k, v in Campaign_Opponents.items():
        location_name_to_id[k] = v + start_id

    for k, v in special.items():
        location_name_to_id[k] = v + start_id

    for k, v in Required_Cards.items():
        location_name_to_id[k] = v + start_id

    set_rules = set_rules

    item_name_groups = {
        "Core Booster": core_booster,
        "Campaign Boss Beaten": ["Tier 1 Beaten", "Tier 2 Beaten", "Tier 3 Beaten", "Tier 4 Beaten", "Tier 5 Beaten"]
    }

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.removed_challenges = None
        self.starting_booster = None
        self.starting_opponent = None
        self.campaign_opponents = None

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        start_inventory = self.options.start_inventory.value.copy()
        item_pool = []
        items = item_to_index.copy()
        starting_list = Banlist_Items.get(self.options.banlist.value)
        if not self.options.add_empty_banList.value and starting_list != "No Banlist":
            items.pop("No Banlist")
        for rc in self.removed_challenges:
            items.pop(rc + " Unlock")
        items.pop(self.starting_opponent)
        items.pop(self.starting_booster)
        items.pop(starting_list)
        for name in items:
            if name in excluded_items or name in start_inventory:
                continue
            item = Yugioh2006Item(
                name,
                ItemClassification.useful if name in useful else ItemClassification.progression,
                self.item_name_to_id[name],
                self.player
            )
            item_pool.append(item)

        while len(item_pool) < len([l for l in self.location_name_to_id if l not in self.removed_challenges]):
            item = Yugioh2006Item(
                "5000DP",
                ItemClassification.filler,
                self.item_name_to_id["5000DP"],
                self.player
            )
            item_pool.append(item)

        self.multiworld.itempool += item_pool

        for challenge in get_beat_challenge_events(self).keys():
            item = Yugioh2006Item(
                "Challenge Beaten",
                ItemClassification.progression,
                None,
                self.player
            )
            location = self.multiworld.get_location(challenge, self.player)
            location.place_locked_item(item)
            location.event = True

        for opponent in self.campaign_opponents:
            for location_name, event in get_opponent_locations(opponent).items():
                if event is not None and not isinstance(event, int):
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

        structure_deck = self.options.structure_deck.current_key
        for location_name, content in get_deck_content_locations(structure_deck).items():
            item = Yugioh2006Item(
                content,
                ItemClassification.progression,
                None,
                self.player
            )
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(item)
            location.event = True
        for event in collection_events:
            item = Yugioh2006Item(
                event,
                ItemClassification.progression,
                None,
                self.player
            )
            location = self.multiworld.get_location(event, self.player)
            location.place_locked_item(item)
            location.event = True

    def create_regions(self):
        structure_deck = self.options.structure_deck.current_key
        self.multiworld.regions += [
            create_region(self, 'Menu', None, ['to Deck Edit', 'to Campaign', 'to Challenges', 'to Card Shop']),
            create_region(self, 'Campaign', Bonuses | Campaign_Opponents),
            create_region(self, 'Challenges'),
            create_region(self, 'Card Shop', Required_Cards | collection_events),
            create_region(self, 'Structure Deck', get_deck_content_locations(structure_deck))
        ]

        self.multiworld.get_entrance('to Campaign', self.player) \
            .connect(self.multiworld.get_region('Campaign', self.player))
        self.multiworld.get_entrance('to Challenges', self.player) \
            .connect(self.multiworld.get_region('Challenges', self.player))
        self.multiworld.get_entrance('to Card Shop', self.player) \
            .connect(self.multiworld.get_region('Card Shop', self.player))
        self.multiworld.get_entrance('to Deck Edit', self.player) \
            .connect(self.multiworld.get_region('Structure Deck', self.player))

        campaign = self.multiworld.get_region('Campaign', self.player)
        # Campaign Opponents
        for opponent in self.campaign_opponents:
            unlock_item = "Campaign Tier " + str(opponent.tier) + " Column " + str(opponent.column)
            region = create_region(self,
                                   opponent.name, get_opponent_locations(opponent))
            entrance = Entrance(self.player, unlock_item, campaign)
            if opponent.tier == 5 and opponent.column > 2:
                unlock_amount = 0
                is_challenge = True
                if opponent.column == 3:
                    if self.options.third_tier_5_campaign_boss_unlock_condition.value == 1:
                        unlock_item = "Challenge Beaten"
                        unlock_amount = self.options.third_tier_5_campaign_boss_challenges.value
                        is_challenge = True
                    else:
                        unlock_item = "Campaign Boss Beaten"
                        unlock_amount = self.options.third_tier_5_campaign_boss_campaign_opponents.value
                        is_challenge = False
                if opponent.column == 4:
                    if self.options.fourth_tier_5_campaign_boss_unlock_condition.value == 1:
                        unlock_item = "Challenge Beaten"
                        unlock_amount = self.options.fourth_tier_5_campaign_boss_challenges.value
                        is_challenge = True
                    else:
                        unlock_item = "Campaign Boss Beaten"
                        unlock_amount = self.options.fourth_tier_5_campaign_boss_campaign_opponents.value
                        is_challenge = False
                if opponent.column == 5:
                    if self.options.final_campaign_boss_unlock_condition.value == 1:
                        unlock_item = "Challenge Beaten"
                        unlock_amount = self.options.final_campaign_boss_challenges.value
                        is_challenge = True
                    else:
                        unlock_item = "Campaign Boss Beaten"
                        unlock_amount = self.options.final_campaign_boss_campaign_opponents.value
                        is_challenge = False
                if is_challenge:
                    entrance.access_rule = \
                        (lambda opp, item, amount: lambda state: state.has(item, self.player, amount) and
                                                                 state.yugioh06_difficulty(self.player, opp.difficulty)
                                                                 and state.has_all(opp.additional_info, self.player))\
                                                                (opponent, unlock_item, unlock_amount)

                else:
                    entrance.access_rule = \
                        (lambda opp, item, amount: lambda state: state.has_group(item, self.player, amount) and
                                                                 state.yugioh06_difficulty(self.player, opp.difficulty)
                                                                 and state.has_all(opp.additional_info, self.player))\
                                                                 (opponent, unlock_item, unlock_amount)
            else:
                entrance.access_rule = (lambda unlock, opp: lambda state:
                state.has(unlock, self.player) and state.yugioh06_difficulty(self.player, opp.difficulty))(unlock_item, opponent)
            campaign.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        card_shop = self.multiworld.get_region('Card Shop', self.player)
        # Booster Contents
        for booster in booster_packs:
            region = create_region(self,
                                   booster, get_booster_locations(booster))
            entrance = Entrance(self.player, booster, card_shop)
            entrance.access_rule = (lambda unlock: lambda state: state.has(unlock, self.player))(booster)
            card_shop.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        challenge_region = self.multiworld.get_region('Challenges', self.player)
        # Challenges
        for challenge, lid in (Limited_Duels | Theme_Duels).items():
            if challenge in self.removed_challenges:
                continue
            region = create_region(self,
                                   challenge, {challenge: lid, challenge + " Complete": None})
            entrance = Entrance(self.player, challenge, challenge_region)
            entrance.access_rule = (lambda unlock: lambda state: state.has(unlock + " Unlock", self.player))(challenge)
            challenge_region.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

    def generate_early(self):
        if self.options.structure_deck.current_key == "none":
            boosters = draft_boosters
            if self.options.campaign_opponents_shuffle.value:
                opponents = tier_1_opponents
            else:
                opponents = draft_opponents
        else:
            boosters = booster_packs
            opponents = tier_1_opponents

        if self.options.structure_deck.current_key == "random_deck":
            self.options.structure_deck.value = self.random.choice([0, 1, 2, 3, 4, 5])
        for item in self.options.start_inventory:
            if item in opponents:
                self.starting_opponent = item
            if item in boosters:
                self.starting_booster = item
        if not self.starting_opponent:
            self.starting_opponent = self.wolrd.random.choice(opponents)
        self.multiworld.push_precollected(self.create_item(self.starting_opponent))
        if not self.starting_booster:
            self.starting_booster = self.world.random.choice(boosters)
        self.multiworld.push_precollected(self.create_item(self.starting_booster))
        banlist = self.options.banlist.value
        self.multiworld.push_precollected(self.create_item(Banlist_Items.get(banlist)))
        challenge = list((Limited_Duels | Theme_Duels).keys())
        noc = len(challenge) - max(self.options.third_tier_5_campaign_boss_challenges.value
                                   if self.options.third_tier_5_campaign_boss_unlock_condition == "challenges" else 0,
                                   self.options.fourth_tier_5_campaign_boss_challenges.value
                                   if self.options.fourth_tier_5_campaign_boss_unlock_condition == "challenges" else 0,
                                   self.options.final_campaign_boss_challenges.value
                                   if self.options.final_campaign_boss_unlock_condition == "challenges" else 0,
                                   self.options.number_of_challenges.value,
                                   91 if hasattr(self.multiworld, "generation_is_fake") else 0)

        self.random.shuffle(challenge)
        excluded = self.options.exclude_locations.value.intersection(challenge)
        prio = self.options.priority_locations.value.intersection(challenge)
        normal = [e for e in challenge if e not in excluded and e not in prio]
        total = list(excluded) + normal + list(prio)
        self.removed_challenges = total[:noc]
        self.campaign_opponents = get_opponents(self.multiworld, self.player,
                                                self.options.campaign_opponents_shuffle.value)

    def apply_base_patch(self, rom):
        base_patch_location = "/".join((os.path.dirname(self.__file__), "patch.bsdiff4"))
        with openFile(base_patch_location, "rb") as base_patch:
            rom_data = bsdiff4.patch(rom.read(), base_patch.read())
        if self.options.ocg_arts:
            ocg_patch_location = "/".join((os.path.dirname(self.__file__), "patches/ocg.bsdiff4"))
            with openFile(ocg_patch_location, "rb") as ocg_patch:
                rom_data = bsdiff4.patch(rom_data, ocg_patch.read())
        structure_deck = self.options.structure_deck
        if structure_deck.current_key == 'none':
            draft_patch_location = "/".join((os.path.dirname(self.__file__), "patches/draft.bsdiff4"))
            with openFile(draft_patch_location, "rb") as draft_patch:
                rom_data = bsdiff4.patch(rom_data, draft_patch.read())
        rom_data = bytearray(rom_data)
        return rom_data

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "structure_deck": self.options.structure_deck.value,
            "banlist": self.options.banlist.value,
            "final_campaign_boss_unlock_condition": self.options.final_campaign_boss_unlock_condition.value,
            "fourth_tier_5_campaign_boss_unlock_condition": self.options.fourth_tier_5_campaign_boss_unlock_condition.value,
            "third_tier_5_campaign_boss_unlock_condition": self.options.third_tier_5_campaign_boss_unlock_condition.value,
            "final_campaign_boss_challenges": self.options.final_campaign_boss_challenges.value,
            "fourth_tier_5_campaign_boss_challenges": self.options.fourth_tier_5_campaign_boss_challenges.value,
            "third_tier_5_campaign_boss_challenges": self.options.third_tier_5_campaign_boss_campaign_opponents.value,
            "final_campaign_boss_campaign_opponents": self.options.final_campaign_boss_campaign_opponents.value,
            "fourth_tier_5_campaign_boss_campaign_opponents": self.options.fourth_tier_5_campaign_boss_unlock_condition.value,
            "third_tier_5_campaign_boss_campaign_opponents": self.options.third_tier_5_campaign_boss_campaign_opponents.value,
            "number_of_challenges": self.options.number_of_challenges.value,
        }

        slot_data["removed challenges"] = self.removed_challenges
        slot_data["starting_booster"] = self.starting_booster
        slot_data["starting_opponent"] = self.starting_opponent
        return slot_data

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> None:
        # bypassing random yaml settings
        self.options.structure_deck.value = slot_data["structure_deck"]
        self.options.banlist.value = slot_data["banlist"]
        self.options.final_campaign_boss_unlock_condition.value = slot_data["final_campaign_boss_unlock_condition"]
        self.options.fourth_tier_5_campaign_boss_unlock_condition.value = \
            slot_data["fourth_tier_5_campaign_boss_unlock_condition"]
        self.options.third_tier_5_campaign_boss_unlock_condition.value = \
            slot_data["third_tier_5_campaign_boss_unlock_condition"]
        self.options.final_campaign_boss_challenges.value = \
            slot_data["final_campaign_boss_challenges"]
        self.options.fourth_tier_5_campaign_boss_challenges.value = \
            slot_data["fourth_tier_5_campaign_boss_challenges"]
        self.options.third_tier_5_campaign_boss_challenges.value = \
            slot_data["third_tier_5_campaign_boss_challenges"]
        self.options.final_campaign_boss_campaign_opponents.value = \
            slot_data["final_campaign_boss_campaign_opponents"]
        self.options.fourth_tier_5_campaign_boss_campaign_opponents.value = \
            slot_data["fourth_tier_5_campaign_boss_campaign_opponents"]
        self.options.third_tier_5_campaign_boss_campaign_opponents.value = \
            slot_data["third_tier_5_campaign_boss_campaign_opponents"]
        self.options.number_of_challenges.value = \
            slot_data["number_of_challenges"]
        self.removed_challenges = slot_data["removed challenges"]
        self.starting_booster = slot_data["starting_booster"]
        self.starting_opponent = slot_data["starting_opponent"]
        all_state = self.multiworld.get_all_state(False)

    def apply_randomizer(self):
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = self.apply_base_patch(rom)

        structure_deck = self.options.structure_deck
        # set structure deck
        structure_deck_data_location = 0x000fd0aa
        rom_data[structure_deck_data_location] = structure_deck_selection.get(structure_deck.value)
        # set banlist
        banlist = self.options.banlist
        banlist_data_location = 0xf4496
        rom_data[banlist_data_location] = banlist_ids.get(banlist.value)
        # set items to locations map
        randomizer_data_start = 0x0000f310
        for location in self.multiworld.get_locations(self.player):
            item = location.item.name
            if location.item.player != self.player:
                item = "Remote"
            item_id = item_to_index.get(item)
            if item_id is None:
                continue
            location_id = self.location_name_to_id[location.name] - 5730000
            rom_data[randomizer_data_start + location_id] = item_id
        # set starting inventory
        inventory_map = [0 for i in range(32)]
        starting_inventory = list(map(lambda i: i.name, self.multiworld.precollected_items[self.player]))
        starting_inventory += self.options.start_inventory.value
        for start_inventory in starting_inventory:
            item_id = self.item_name_to_id[start_inventory] - 5730001
            index = math.floor(item_id / 8)
            bit = item_id % 8
            inventory_map[index] = inventory_map[index] | (1 << bit)

        rom_data[0xe9dc:0xe9fc] = inventory_map
        # set unlock conditions for the last 3 campaign opponents
        rom_data[0xeefa] = self.options.third_tier_5_campaign_boss_challenges.value \
            if self.options.third_tier_5_campaign_boss_unlock_condition.value == 1 \
            else self.options.third_tier_5_campaign_boss_campaign_opponents.value
        rom_data[0xef10] = self.options.fourth_tier_5_campaign_boss_challenges.value \
            if self.options.fourth_tier_5_campaign_boss_unlock_condition.value == 1 \
            else self.options.fourth_tier_5_campaign_boss_campaign_opponents.value
        rom_data[0xef22] = self.options.final_campaign_boss_challenges.value \
            if self.options.final_campaign_boss_unlock_condition.value == 1 \
            else self.options.final_campaign_boss_campaign_opponents.value
        rom_data[0xeef8] = \
            int((function_addresses.get(self.options.third_tier_5_campaign_boss_unlock_condition.value) - 0xeefa) / 2)
        rom_data[0xef0e] = \
            int((function_addresses.get(self.options.fourth_tier_5_campaign_boss_unlock_condition.value) - 0xef10) / 2)
        rom_data[0xef20] = \
            int((function_addresses.get(self.options.final_campaign_boss_unlock_condition.value) - 0xef22) / 2)
        # set starting money
        rom_data[0xf4734:0xf4738] = self.options.starting_money.value.to_bytes(4, 'little')
        rom_data[0xe70c] = self.options.money_reward_multiplier.value
        rom_data[0xe6e4] = self.options.money_reward_multiplier.value
        # normalize booster packs if option is set
        if self.options.normalize_boosters_packs.value:
            booster_pack_price = self.options.booster_pack_prices.value.to_bytes(2, 'little')
            for booster in range(51):
                space = booster * 16
                rom_data[0x1e5e2e8 + space] = booster_pack_price[0]
                rom_data[0x1e5e2e9 + space] = booster_pack_price[1]
                rom_data[0x1e5e2ea + space] = 5
        # set shuffled campaign opponents if option is set
        if self.options.campaign_opponents_shuffle.value:
            i = 0
            for opp in self.campaign_opponents:
                space = i * 32
                rom_data[0x000f3ba + i] = opp.id
                rom_data[0x1e58d0e + space:0x1e58d10 + space] = opp.card_id.to_bytes(2, 'little')
                rom_data[0x1e58d10 + space:0x1e58d12 + space] = opp.deck_name_id.to_bytes(2, 'little')
                rom_data[0x1e58d12 + space:0x1e58d28 + space] = opp.deck_file.encode('ascii')
                i = i+1
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


def create_region(self, name: str, locations=None, exits=None):
    region = Region(name, self.player, self.multiworld)
    if locations:
        for location_name, lid in locations.items():
            if lid is not None and isinstance(lid, int):
                lid = self.location_name_to_id[location_name]
            else:
                lid = None
            location = Yugioh2006Location(self.player, location_name, lid, region)
            if lid is None:
                location.event = True
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(self.player, _exit, region))
    return region


class Yugioh2006Item(Item):
    game = "Yu-Gi-Oh! 2006"


class Yugioh2006Location(Location):
    game: str = "Yu-Gi-Oh! 2006"
