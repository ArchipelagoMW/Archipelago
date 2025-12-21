import os
import pkgutil
from typing import Any, ClassVar, Dict, List, Set

import settings
from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial

import Utils
from worlds.AutoWorld import WebWorld, World

from .boosterpacks import booster_contents as booster_contents
from .boosterpacks import get_booster_locations
from .items import (
    Banlist_Items,
    booster_packs,
    draft_boosters,
    draft_opponents,
    excluded_items,
    item_to_index,
    useful,
    tier_1_opponents,
    tier_2_opponents,
    tier_3_opponents,
    tier_4_opponents,
    tier_5_opponents,
)
from .items import challenges as challenges
from .locations import (
    Bonuses,
    Campaign_Opponents,
    Limited_Duels,
    Required_Cards,
    Theme_Duels,
    collection_events,
    get_beat_challenge_events,
    special,
)
from .logic import core_booster, yugioh06_difficulty
from .opponents import OpponentData, get_opponent_condition, get_opponent_locations, get_opponents
from .opponents import challenge_opponents as challenge_opponents
from .options import Yugioh06Options
from .rom import MD5America, MD5Europe, YGO06ProcedurePatch, write_tokens
from .rom import get_base_rom_path as get_base_rom_path
from .rom_values import banlist_ids as banlist_ids
from .rom_values import function_addresses as function_addresses
from .rom_values import structure_deck_selection as structure_deck_selection
from .rules import set_rules
from .structure_deck import get_deck_content_locations
from .client_bh import YuGiOh2006Client


class Yugioh06Web(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yu-Gi-Oh! - Ultimate Masters Edition - World Championship Tournament 2006 "
        "for Archipelago on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Rensen"],
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
    web = Yugioh06Web()
    options: Yugioh06Options
    options_dataclass = Yugioh06Options
    settings_key = "yugioh06_settings"
    settings: ClassVar[Yugioh2006Setting]

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

    item_name_groups: Dict[str, Set[str]] = {
        "Core Booster": set(core_booster),
        "Campaign Boss Beaten": {"Tier 1 Beaten", "Tier 2 Beaten", "Tier 3 Beaten", "Tier 4 Beaten", "Tier 5 Beaten"},
        "Challenge": set(challenges),
        "Tier 1 Opponent": set(tier_1_opponents),
        "Tier 2 Opponent": set(tier_2_opponents),
        "Tier 3 Opponent": set(tier_3_opponents),
        "Tier 4 Opponent": set(tier_4_opponents),
        "Tier 5 Opponent": set(tier_5_opponents),
        "Campaign Opponent": set(tier_1_opponents + tier_2_opponents + tier_3_opponents +
                             tier_4_opponents + tier_5_opponents)
    }

    removed_challenges: List[str]
    starting_booster: str
    starting_opponent: str
    campaign_opponents: List[OpponentData]
    is_draft_mode: bool

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def generate_early(self):
        self.starting_opponent = ""
        self.starting_booster = ""
        self.removed_challenges = []
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Yu-Gi-Oh! 2006" in self.multiworld.re_gen_passthrough:
                # bypassing random yaml settings
                slot_data = self.multiworld.re_gen_passthrough["Yu-Gi-Oh! 2006"]
                self.options.structure_deck.value = slot_data["structure_deck"]
                self.options.banlist.value = slot_data["banlist"]
                self.options.final_campaign_boss_unlock_condition.value = slot_data[
                    "final_campaign_boss_unlock_condition"
                ]
                self.options.fourth_tier_5_campaign_boss_unlock_condition.value = slot_data[
                    "fourth_tier_5_campaign_boss_unlock_condition"
                ]
                self.options.third_tier_5_campaign_boss_unlock_condition.value = slot_data[
                    "third_tier_5_campaign_boss_unlock_condition"
                ]
                self.options.final_campaign_boss_challenges.value = slot_data["final_campaign_boss_challenges"]
                self.options.fourth_tier_5_campaign_boss_challenges.value = slot_data[
                    "fourth_tier_5_campaign_boss_challenges"
                ]
                self.options.third_tier_5_campaign_boss_challenges.value = slot_data[
                    "third_tier_5_campaign_boss_challenges"
                ]
                self.options.final_campaign_boss_campaign_opponents.value = slot_data[
                    "final_campaign_boss_campaign_opponents"
                ]
                self.options.fourth_tier_5_campaign_boss_campaign_opponents.value = slot_data[
                    "fourth_tier_5_campaign_boss_campaign_opponents"
                ]
                self.options.third_tier_5_campaign_boss_campaign_opponents.value = slot_data[
                    "third_tier_5_campaign_boss_campaign_opponents"
                ]
                self.options.number_of_challenges.value = slot_data["number_of_challenges"]
                self.removed_challenges = slot_data["removed challenges"]
                self.starting_booster = slot_data["starting_booster"]
                self.starting_opponent = slot_data["starting_opponent"]

        if self.options.structure_deck.current_key == "none":
            self.is_draft_mode = True
            boosters = draft_boosters
            if self.options.campaign_opponents_shuffle.value:
                opponents = tier_1_opponents
            else:
                opponents = draft_opponents
        else:
            self.is_draft_mode = False
            boosters = booster_packs
            opponents = tier_1_opponents

        if self.options.structure_deck.current_key == "random_deck":
            self.options.structure_deck.value = self.random.randint(0, 5)
        for item in self.options.start_inventory:
            if item in opponents:
                self.starting_opponent = item
            if item in boosters:
                self.starting_booster = item
        if not self.starting_opponent:
            self.starting_opponent = self.random.choice(opponents)
            self.multiworld.push_precollected(self.create_item(self.starting_opponent))
        if not self.starting_booster:
            self.starting_booster = self.random.choice(boosters)
            self.multiworld.push_precollected(self.create_item(self.starting_booster))
        banlist = self.options.banlist.value
        self.multiworld.push_precollected(self.create_item(Banlist_Items[banlist]))

        if not self.removed_challenges:
            challenge = list(({**Limited_Duels, **Theme_Duels}).keys())
            noc = len(challenge) - max(
                self.options.third_tier_5_campaign_boss_challenges.value
                if self.options.third_tier_5_campaign_boss_unlock_condition == "challenges"
                else 0,
                self.options.fourth_tier_5_campaign_boss_challenges.value
                if self.options.fourth_tier_5_campaign_boss_unlock_condition == "challenges"
                else 0,
                self.options.final_campaign_boss_challenges.value
                if self.options.final_campaign_boss_unlock_condition == "challenges"
                else 0,
                self.options.number_of_challenges.value,
            )

            self.random.shuffle(challenge)
            excluded = self.options.exclude_locations.value.intersection(challenge)
            prio = self.options.priority_locations.value.intersection(challenge)
            normal = [e for e in challenge if e not in excluded and e not in prio]
            total = list(excluded) + normal + list(prio)
            self.removed_challenges = total[:noc]

        self.campaign_opponents = get_opponents(
            self.multiworld, self.player, self.options.campaign_opponents_shuffle.value
        )

    def create_region(self, name: str, locations=None, exits=None):
        region = Region(name, self.player, self.multiworld)
        if locations:
            for location_name, lid in locations.items():
                if lid is not None and isinstance(lid, int):
                    lid = self.location_name_to_id[location_name]
                else:
                    lid = None
                location = Yugioh2006Location(self.player, location_name, lid, region)
                region.locations.append(location)

        if exits:
            for _exit in exits:
                region.exits.append(Entrance(self.player, _exit, region))
        return region

    def create_regions(self):
        structure_deck = self.options.structure_deck.current_key
        self.multiworld.regions += [
            self.create_region("Menu", None, ["to Deck Edit", "to Campaign", "to Challenges", "to Card Shop"]),
            self.create_region("Campaign", {**Bonuses,  **Campaign_Opponents}),
            self.create_region("Challenges"),
            self.create_region("Card Shop", {**Required_Cards, **collection_events}),
            self.create_region("Structure Deck", get_deck_content_locations(structure_deck)),
        ]

        self.get_entrance("to Campaign").connect(self.get_region("Campaign"))
        self.get_entrance("to Challenges").connect(self.get_region("Challenges"))
        self.get_entrance("to Card Shop").connect(self.get_region("Card Shop"))
        self.get_entrance("to Deck Edit").connect(self.get_region("Structure Deck"))

        campaign = self.get_region("Campaign")
        # Campaign Opponents
        for opponent in self.campaign_opponents:
            unlock_item = "Campaign Tier " + str(opponent.tier) + " Column " + str(opponent.column)
            region = self.create_region(opponent.name, get_opponent_locations(opponent))
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
                entrance.access_rule = get_opponent_condition(
                    opponent, unlock_item, unlock_amount, self.player, is_challenge
                )
            else:
                entrance.access_rule = lambda state, unlock=unlock_item, opp=opponent: state.has(
                    unlock, self.player
                ) and yugioh06_difficulty(state, self.player, opp.difficulty)
            campaign.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        card_shop = self.get_region("Card Shop")
        # Booster Contents
        for booster in booster_packs:
            region = self.create_region(booster, get_booster_locations(booster))
            entrance = Entrance(self.player, booster, card_shop)
            entrance.access_rule = lambda state, unlock=booster: state.has(unlock, self.player)
            card_shop.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        challenge_region = self.get_region("Challenges")
        # Challenges
        for challenge, lid in ({**Limited_Duels, **Theme_Duels}).items():
            if challenge in self.removed_challenges:
                continue
            region = self.create_region(challenge, {challenge: lid, challenge + " Complete": None})
            entrance = Entrance(self.player, challenge, challenge_region)
            entrance.access_rule = lambda state, unlock=challenge: state.has(unlock + " Unlock", self.player)
            challenge_region.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

    def create_item(self, name: str) -> Item:
        classification: ItemClassification = ItemClassification.progression
        if name == "5000DP":
            classification = ItemClassification.filler
        if name in useful:
            classification = ItemClassification.useful
        return Item(name, classification, self.item_name_to_id[name], self.player)

    def create_filler(self) -> Item:
        return self.create_item("5000DP")

    def get_filler_item_name(self) -> str:
        return "5000DP"

    def create_items(self):
        start_inventory = self.options.start_inventory.value.copy()
        item_pool = []
        items = item_to_index.copy()
        starting_list = Banlist_Items[self.options.banlist.value]
        if not self.options.add_empty_banlist.value and starting_list != "No Banlist":
            items.pop("No Banlist")
        for rc in self.removed_challenges:
            items.pop(rc + " Unlock")
        items.pop(self.starting_opponent)
        items.pop(self.starting_booster)
        items.pop(starting_list)
        for name in items:
            if name in excluded_items or name in start_inventory:
                continue
            item = self.create_item(name)
            item_pool.append(item)

        needed_item_pool_size = sum(loc not in self.removed_challenges for loc in self.location_name_to_id)
        needed_filler_amount = needed_item_pool_size - len(item_pool)
        item_pool += [self.create_item("5000DP") for _ in range(needed_filler_amount)]

        self.multiworld.itempool += item_pool

        for challenge in get_beat_challenge_events(self):
            item = Yugioh2006Item("Challenge Beaten", ItemClassification.progression, None, self.player)
            location = self.multiworld.get_location(challenge, self.player)
            location.place_locked_item(item)

        for opponent in self.campaign_opponents:
            for location_name, event in get_opponent_locations(opponent).items():
                if event is not None and not isinstance(event, int):
                    item = Yugioh2006Item(event, ItemClassification.progression, None, self.player)
                    location = self.multiworld.get_location(location_name, self.player)
                    location.place_locked_item(item)

        for booster in booster_packs:
            for location_name, content in get_booster_locations(booster).items():
                item = Yugioh2006Item(content, ItemClassification.progression, None, self.player)
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(item)

        structure_deck = self.options.structure_deck.current_key
        for location_name, content in get_deck_content_locations(structure_deck).items():
            item = Yugioh2006Item(content, ItemClassification.progression, None, self.player)
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(item)

        for event in collection_events:
            item = Yugioh2006Item(event, ItemClassification.progression, None, self.player)
            location = self.multiworld.get_location(event, self.player)
            location.place_locked_item(item)

    def set_rules(self):
        set_rules(self)

    def generate_output(self, output_directory: str):
        outfilepname = f"_P{self.player}"
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        self.rom_name_text = f'YGO06{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, "utf8")[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], "utf8")[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        patch = YGO06ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "patch.bsdiff4"))
        procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]
        if self.is_draft_mode:
            procedure.insert(1, ("apply_bsdiff4", ["draft_patch.bsdiff4"]))
            patch.write_file("draft_patch.bsdiff4", pkgutil.get_data(__name__, "patches/draft.bsdiff4"))
        if self.options.ocg_arts:
            procedure.insert(1, ("apply_bsdiff4", ["ocg_patch.bsdiff4"]))
            patch.write_file("ocg_patch.bsdiff4", pkgutil.get_data(__name__, "patches/ocg.bsdiff4"))
        patch.procedure = procedure
        write_tokens(self, patch)

        # Write Output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "structure_deck": self.options.structure_deck.value,
            "banlist": self.options.banlist.value,
            "final_campaign_boss_unlock_condition": self.options.final_campaign_boss_unlock_condition.value,
            "fourth_tier_5_campaign_boss_unlock_condition":
                self.options.fourth_tier_5_campaign_boss_unlock_condition.value,
            "third_tier_5_campaign_boss_unlock_condition":
                self.options.third_tier_5_campaign_boss_unlock_condition.value,
            "final_campaign_boss_challenges": self.options.final_campaign_boss_challenges.value,
            "fourth_tier_5_campaign_boss_challenges":
                self.options.fourth_tier_5_campaign_boss_challenges.value,
            "third_tier_5_campaign_boss_challenges":
                self.options.third_tier_5_campaign_boss_campaign_opponents.value,
            "final_campaign_boss_campaign_opponents":
                self.options.final_campaign_boss_campaign_opponents.value,
            "fourth_tier_5_campaign_boss_campaign_opponents":
                self.options.fourth_tier_5_campaign_boss_campaign_opponents.value,
            "third_tier_5_campaign_boss_campaign_opponents":
                self.options.third_tier_5_campaign_boss_campaign_opponents.value,
            "number_of_challenges": self.options.number_of_challenges.value,
        }

        slot_data["removed challenges"] = self.removed_challenges
        slot_data["starting_booster"] = self.starting_booster
        slot_data["starting_opponent"] = self.starting_opponent
        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data


class Yugioh2006Item(Item):
    game: str = "Yu-Gi-Oh! 2006"


class Yugioh2006Location(Location):
    game: str = "Yu-Gi-Oh! 2006"
