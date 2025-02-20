import logging
import os
import pkgutil
from typing import Any, ClassVar, Dict, List, TextIO

import settings
from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial

import Utils
from worlds.AutoWorld import WebWorld, World
from .banlists import banlists
from .boosterpack_chaos import create_chaos_packs
from .boosterpack_contents import get_booster_contents
from .boosterpack_shuffle import create_shuffled_packs
from .boosterpacks_data import booster_card_id_to_name
from .card_data import CardData, cards, empty_card_data, collection_id_to_name
from .card_rules import set_card_rules
from .groups import item_groups, location_groups
from .items import (
    Banlist_Items,
    booster_packs,
    draft_boosters,
    draft_opponents,
    excluded_items,
    item_to_index,
    useful,
    tier_1_opponents,
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
from .logic import yugioh06_difficulty
from .opponents import OpponentData, get_opponent_locations, get_opponents
from .opponents import challenge_opponents as challenge_opponents
from .options import Yugioh06Options
from .rom import MD5America, MD5Europe, YGO06ProcedurePatch, write_tokens
from .rom import get_base_rom_path as get_base_rom_path
from .rom_values import banlist_ids as banlist_ids
from .rom_values import function_addresses as function_addresses
from .rom_values import structure_deck_selection as structure_deck_selection
from .rules import set_rules
from .structure_deck import get_deck_content_locations, worst_deck
from .client_bh import YuGiOh2006Client


class Yugioh06Web(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Yu-Gi-Oh! - Ultimate Masters Edition - World Championship Tournament 2006 "
        "for Archipelago on your computer.",
        "English",
        "docs/setup_en.md",
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

    item_name_groups = item_groups
    location_name_groups = location_groups

    removed_challenges: List[str]
    starting_booster: str
    starting_opponent: str
    campaign_opponents: List[OpponentData]
    starter_deck: Dict[CardData, int]
    structure_deck: Dict[CardData, int]
    is_draft_mode: bool
    progression_cards: Dict[str, List[str]]
    progression_cards_in_booster: List[str]
    progression_cards_in_start: List[str]
    booster_pack_contents: Dict[str, Dict[str, str]]

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def generate_early(self):
        self.starting_opponent = ""
        self.starting_booster = ""
        self.removed_challenges = []
        self.starter_deck = {}
        self.structure_deck = {}
        self.progression_cards = {}
        self.progression_cards_in_booster = []
        self.progression_cards_in_start = []
        self.booster_pack_contents = {}
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Yu-Gi-Oh! 2006" in self.multiworld.re_gen_passthrough:
                # bypassing random yaml settings
                slot_data = self.multiworld.re_gen_passthrough["Yu-Gi-Oh! 2006"]
                self.options.structure_deck.value = slot_data["structure_deck"]
                self.options.banlist.value = slot_data["banlist"]
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
                if "progression_cards" in slot_data:
                    self.progression_cards_in_start = [collection_id_to_name[cid] for cid in
                                                       slot_data["progression_cards_in_start"]]
                    self.progression_cards_in_booster = [collection_id_to_name[cid] for cid in
                                                         slot_data["progression_cards_in_booster"]]
                    for name, v in slot_data["progression_cards"].items():
                        self.progression_cards[name] = [collection_id_to_name[cid] for cid in
                                                        slot_data["progression_cards"][name]]
                    for name, content in slot_data["booster_pack_contents"].items():
                        con = {}
                        for cid in slot_data["booster_pack_contents"][name]:
                            con[collection_id_to_name[cid]] = "Common"
                        self.booster_pack_contents[name] = con

        # set possible starting booster and opponent. Restrict them if you don't start with a standard booster
        if self.options.structure_deck.value > 5:
            self.is_draft_mode = True
            if self.options.randomize_pack_contents == self.options.randomize_pack_contents.option_vanilla:
                boosters = draft_boosters
            else:
                boosters = booster_packs
            if self.options.campaign_opponents_shuffle.value:
                opponents = tier_1_opponents
            else:
                opponents = draft_opponents
        else:
            self.is_draft_mode = False
            boosters = booster_packs
            opponents = tier_1_opponents

        # clone to prevent duplicates
        card_list = list(cards.values())
        # set starter deck
        if self.options.starter_deck.value == self.options.starter_deck.option_random_singles:
            for i in range(0, 40):
                card = self.random.choice(card_list)
                card_list.remove(card)
                self.starter_deck[card] = 1
        elif self.options.starter_deck.value == self.options.starter_deck.option_random_playsets:
            for i in range(0, 13):
                card = self.random.choice(card_list)
                card_list.remove(card)
                self.starter_deck[card] = 3
            self.starter_deck[empty_card_data] = 1
        elif self.options.starter_deck.value == self.options.starter_deck.option_custom:
            total_amount = 0
            for name, amount in self.options.custom_starter_deck.value.items():
                card = cards[name]
                if amount > 3:
                    logging.warning(
                        f"{self.player} has too many {name} in their "
                        f"Custom Starter Deck setting. Setting it to 3")
                    amount = 3
                total_amount += amount
                if total_amount > 40:
                    logging.warning(f"{self.player} Starter Deck cards exceeded the maximum of 40")
                    break
                if amount > 0:
                    self.starter_deck[card] = amount
            if total_amount < 40:
                self.starter_deck[empty_card_data] = 40 - total_amount
        # set structure deck
        banlist = banlists[self.options.banlist.current_key]
        # make sure the structure deck is a legal deck
        card_list = [card for card in card_list if card.card_type != "Fusion" and card.name not in banlist["Forbidden"]]
        if self.options.structure_deck.current_key == "random_deck":
            self.options.structure_deck.value = self.random.randint(0, 5)
        if self.options.structure_deck.value == self.options.structure_deck.option_random_singles:
            for i in range(0, 40):
                card = self.random.choice(card_list)
                card_list.remove(card)
                self.structure_deck[card] = 1
        elif self.options.structure_deck.value == self.options.structure_deck.option_random_playsets:
            amount = 0
            while amount < 40:
                card = self.random.choice(card_list)
                card_list.remove(card)
                if card.name in banlist["Limited"]:
                    self.structure_deck[card] = 1
                    amount += 1
                elif card.name in banlist["Semi-Limited"]:
                    self.structure_deck[card] = 2
                    amount += 2
                else:
                    self.structure_deck[card] = 3
                    amount += 3
        elif self.options.structure_deck.value == self.options.structure_deck.option_worst:
            self.structure_deck = {cards[card_name]: amount for card_name, amount in worst_deck.items()}
        elif self.options.structure_deck.value == self.options.structure_deck.option_custom:
            total_amount = 0
            for name, amount in self.options.custom_structure_deck.value.items():
                card = cards[name]
                if amount > 3:
                    logging.warning(
                        f"{self.player} has too many {name} in their "
                        f"Custom Structure Deck setting. Setting it to 3")
                    amount = 3
                total_amount += amount
                if total_amount > 80:
                    logging.warning(f"{self.player} Structure Deck cards exceeded the maximum of 80")
                    break
                if amount > 0:
                    self.structure_deck[card] = amount
            if total_amount < 40:
                for card_name, w_amount in worst_deck.items():
                    card = cards[card_name]
                    self.structure_deck[card] = w_amount
                    total_amount += min(w_amount, 40 - total_amount)
                    if total_amount >= 40:
                        break
        # set starting booster and opponent
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
                self.options.third_tier_5_campaign_boss_challenges.value,
                self.options.fourth_tier_5_campaign_boss_challenges.value,
                self.options.final_campaign_boss_challenges.value,
                self.options.number_of_challenges.value,
            )

            self.random.shuffle(challenge)
            excluded = self.options.exclude_locations.value.intersection(challenge)
            prio = self.options.priority_locations.value.intersection(challenge)
            normal = [e for e in challenge if e not in excluded and e not in prio]
            total = list(excluded) + normal + list(prio)
            self.removed_challenges = total[:noc]

        self.campaign_opponents = get_opponents(
            self.multiworld, self.player, bool(self.options.campaign_opponents_shuffle.value)
        )

        if not self.progression_cards:
            # set progression_cards
            set_card_rules(self)

        # randomize packs
        if (not self.booster_pack_contents and
                self.options.randomize_pack_contents.value == self.options.randomize_pack_contents.option_shuffle):
            self.booster_pack_contents = create_shuffled_packs(self)
        elif (not self.booster_pack_contents and
                  self.options.randomize_pack_contents.value == self.options.randomize_pack_contents.option_chaos):
            self.booster_pack_contents = create_chaos_packs(self)

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
            self.create_region("Campaign", {**Bonuses, **Campaign_Opponents}),
            self.create_region("Challenges"),
            self.create_region("Card Shop", {**Required_Cards, **collection_events}),
            self.create_region("Structure Deck", get_deck_content_locations(self, structure_deck)),
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
                campaign_amount = 0
                challenge_amount = 0
                if opponent.column == 3:
                    challenge_amount = self.options.third_tier_5_campaign_boss_challenges.value
                    campaign_amount = self.options.third_tier_5_campaign_boss_campaign_opponents.value
                elif opponent.column == 4:
                    challenge_amount = self.options.fourth_tier_5_campaign_boss_challenges.value
                    campaign_amount = self.options.fourth_tier_5_campaign_boss_campaign_opponents.value
                elif opponent.column == 5:
                    challenge_amount = self.options.final_campaign_boss_challenges.value
                    campaign_amount = self.options.final_campaign_boss_campaign_opponents.value
                entrance.access_rule = lambda state, chal_a=challenge_amount, cam_a=campaign_amount, opp=opponent: ((
                    state.has("Challenge Beaten", self.player, chal_a)) and
                    state.has_group("Campaign Boss Beaten", self.player, cam_a) and
                    state.has_all(opp.additional_info, self.player))
            else:
                entrance.access_rule = lambda state, unlock=unlock_item, opp=opponent: (
                        state.has(unlock, self.player) and
                        yugioh06_difficulty(self, state, self.player, opp.difficulty))
            campaign.exits.append(entrance)
            entrance.connect(region)
            self.multiworld.regions.append(region)

        card_shop = self.get_region("Card Shop")
        # Booster Contents
        for booster in booster_packs:
            region = self.create_region(booster, get_booster_contents(booster, self, self.booster_pack_contents))
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
            for location_name, content in get_booster_contents(booster, self, self.booster_pack_contents).items():
                item = Yugioh2006Item(content, ItemClassification.progression, None, self.player)
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(item)

        structure_deck = self.options.structure_deck.current_key
        for location_name, content in get_deck_content_locations(self, structure_deck).items():
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
        if self.options.ocg_arts:
            procedure.insert(1, ("apply_bsdiff4", ["ocg_patch.bsdiff4"]))
            patch.write_file("ocg_patch.bsdiff4", pkgutil.get_data(__name__, "patches/ocg.bsdiff4"))
        patch.procedure = procedure
        write_tokens(self, patch)

        # Write Output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("structure_deck", "banlist",
                                         "final_campaign_boss_challenges",
                                         "fourth_tier_5_campaign_boss_challenges",
                                         "third_tier_5_campaign_boss_challenges",
                                         "final_campaign_boss_campaign_opponents",
                                         "fourth_tier_5_campaign_boss_campaign_opponents",
                                         "third_tier_5_campaign_boss_campaign_opponents",
                                         "number_of_challenges")
        slot_data["removed challenges"] = self.removed_challenges
        slot_data["starting_booster"] = self.starting_booster
        slot_data["starting_opponent"] = self.starting_opponent
        slot_data["progression_cards_in_start"] = [cards[c].id for c in self.progression_cards_in_start]
        slot_data["progression_cards_in_booster"] = [cards[c].id for c in self.progression_cards_in_booster]
        slot_data["all_progression_cards"] = [cards[c].id for c in
                                              self.progression_cards_in_booster + self.progression_cards_in_start]
        slot_data["progression_cards"] = {}
        for k, v in self.progression_cards.items():
            slot_data["progression_cards"][k] = [cards[c].id for c in v]

        slot_data["booster_pack_contents"] = {}
        for name, content in self.booster_pack_contents.items():
            slot_data["booster_pack_contents"][name] = [cards[c].id for c in content.keys()]
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\n\nProgression cards for {self.multiworld.player_name[self.player]}")
        for location, p_cards in self.progression_cards.items():
            spoiler_handle.write(f"\n   {location}: {', '.join(p_cards)}")
        spoiler_handle.write(f"\n\nProgression cards in start for {self.player_name}\n")
        spoiler_handle.write(f" {', '.join(self.progression_cards_in_start)} ")
        spoiler_handle.write(f"\n\nProgression cards in booster for {self.player_name}\n")
        spoiler_handle.write(f" {', '.join(self.progression_cards_in_booster)}")

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data


class Yugioh2006Item(Item):
    game: str = "Yu-Gi-Oh! 2006"


class Yugioh2006Location(Location):
    game: str = "Yu-Gi-Oh! 2006"
