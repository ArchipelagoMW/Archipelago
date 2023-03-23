"""
Archipelago World definition for Pokemon Emerald Version
"""
import hashlib
import os
from typing import List

from BaseClasses import ItemClassification, Tutorial, MultiWorld
from Fill import fill_restrictive
from Options import Toggle
from worlds.AutoWorld import World, WebWorld

from . import rules
from .items import PokemonEmeraldItem, create_item_label_to_code_map, get_item_classification
from .locations import PokemonEmeraldLocation, create_location_label_to_id_map, create_locations_with_tags
from .options import RandomizeBadges, RandomizeHms, ItemPoolType, options, get_option_value
from .regions import create_regions
from .rom import PokemonEmeraldDeltaPatch, generate_output, get_base_rom_path
from .sanity_check import sanity_check


class PokemonEmeraldWebWorld(WebWorld):
    """
    Webhost info for Pokemon Emerald
    """
    theme = "ocean"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Emerald with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Zunawe"]
    )

    tutorials = [setup_en]


class PokemonEmeraldWorld(World):
    """
    Pokémon Emerald is the definitive gen 3 Pokémon game and one of the most beloved in the franchise.
    Catch, train, and battle Pokémon, explore the Hoenn region, and thwart the plots
    of Team Magma and Team Aqua, challenge gyms, and become the Pokémon champion!
    """
    game = "Pokemon Emerald"
    web = PokemonEmeraldWebWorld()
    option_definitions = options
    topology_present = True

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()

    data_version = 0

    def _get_pokemon_emerald_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'race': self.multiworld.is_race,
        }


    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_path = get_base_rom_path()
        if not os.path.exists(rom_path):
            raise FileNotFoundError(rom_path)

        with open(rom_path, "rb") as infile:
            local_hash = hashlib.md5()
            local_hash.update(bytes(infile.read()))

            if local_hash.hexdigest() != PokemonEmeraldDeltaPatch.hash:
                raise AssertionError("Base ROM for Pokemon Emerald does not match expected hash. Please get Pokemon Emerald Version (USA, Europe) and dump it.")

        if sanity_check() is False:
            raise AssertionError("Pokemon Emerald sanity check failed. See log for details.")


    def create_regions(self):
        overworld_items_option = get_option_value(self.multiworld, self.player, "overworld_items")
        hidden_items_option = get_option_value(self.multiworld, self.player, "hidden_items")
        npc_gifts_option = get_option_value(self.multiworld, self.player, "npc_gifts")
        enable_ferry_option = get_option_value(self.multiworld, self.player, "enable_ferry")

        tags = set(["Badge", "HM", "KeyItem", "Rod", "Bike"])
        if overworld_items_option == Toggle.option_true:
            tags.add("OverworldItem")
        if hidden_items_option == Toggle.option_true:
            tags.add("HiddenItem")
        if npc_gifts_option == Toggle.option_true:
            tags.add("NpcGift")
        if enable_ferry_option == Toggle.option_true:
            tags.add("Ferry")

        create_regions(self.multiworld, self.player)
        create_locations_with_tags(self.multiworld, self.player, tags)


    def create_items(self):
        badges_option = get_option_value(self.multiworld, self.player, "badges")
        hms_option = get_option_value(self.multiworld, self.player, "hms")
        key_items_option = get_option_value(self.multiworld, self.player, "key_items")
        rods_option = get_option_value(self.multiworld, self.player, "rods")
        bikes_option = get_option_value(self.multiworld, self.player, "bikes")
        item_pool_type_option = get_option_value(self.multiworld, self.player, "item_pool_type")

        item_locations: List[PokemonEmeraldLocation] = []
        for region in self.multiworld.regions:
            if region.player == self.player:
                # Filter events
                item_locations += [location for location in region.locations if location.address is not None]

                # Filter out items that aren't randomized
                if badges_option == RandomizeBadges.option_vanilla:
                    item_locations = [location for location in item_locations if "Badge" not in location.tags]
                if hms_option == RandomizeHms.option_vanilla:
                    item_locations = [location for location in item_locations if "HM" not in location.tags]
                if key_items_option == Toggle.option_false:
                    item_locations = [location for location in item_locations if "KeyItem" not in location.tags]
                if rods_option == Toggle.option_false:
                    item_locations = [location for location in item_locations if "Rod" not in location.tags]
                if bikes_option == Toggle.option_false:
                    item_locations = [location for location in item_locations if "Bike" not in location.tags]

        if item_pool_type_option == ItemPoolType.option_shuffled:
            self.multiworld.itempool += [self.create_item_by_code(location.default_item_code) for location in item_locations]
        elif item_pool_type_option == ItemPoolType.option_shuffled:
            raise NotImplementedError()


    def set_rules(self):
        rules.set_default_rules(self.multiworld, self.player)

        if get_option_value(self.multiworld, self.player, "overworld_items") == Toggle.option_true:
            rules.set_overworld_item_rules(self.multiworld, self.player)
        if get_option_value(self.multiworld, self.player, "hidden_items") == Toggle.option_true:
            rules.set_hidden_item_rules(self.multiworld, self.player)
        if get_option_value(self.multiworld, self.player, "npc_gifts") == Toggle.option_true:
            rules.set_npc_gift_rules(self.multiworld, self.player)
        if get_option_value(self.multiworld, self.player, "enable_ferry") == Toggle.option_true:
            rules.set_enable_ferry_rules(self.multiworld, self.player)

        if get_option_value(self.multiworld, self.player, "require_itemfinder") == Toggle.option_true:
            rules.add_hidden_item_itemfinder_rules(self.multiworld, self.player)

        if get_option_value(self.multiworld, self.player, "require_flash") == Toggle.option_true:
            rules.add_flash_rules(self.multiworld, self.player)


    def pre_fill(self):
        locations: List[PokemonEmeraldLocation] = self.multiworld.get_locations(self.player)

        badges_option = get_option_value(self.multiworld, self.player, "badges")
        if badges_option == RandomizeBadges.option_shuffle:
            badge_locations = [location for location in locations if location.tags is not None and "Badge" in location.tags]
            badge_items = [item for item in self.multiworld.itempool if item.player == self.player and item.tags is not None and "Badge" in item.tags]

            for item in badge_items:
                self.multiworld.itempool.remove(item)

            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), badge_locations, badge_items, True, True, True)

        hms_option = get_option_value(self.multiworld, self.player, "hms")
        if hms_option == RandomizeBadges.option_shuffle:
            hm_locations = [location for location in locations if location.tags is not None and "HM" in location.tags]
            hm_items = [item for item in self.multiworld.itempool if item.player == self.player and item.tags is not None and "HM" in item.tags]

            for item in hm_items:
                self.multiworld.itempool.remove(item)

            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), hm_locations, hm_items, True, True, True)


    def generate_basic(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        locations: List[PokemonEmeraldLocation] = self.multiworld.get_locations(self.player)

        def convert_unrandomized_items_to_events(tag: str):
            for location in locations:
                if location.tags is not None and tag in location.tags:
                    location.place_locked_item(self.create_event(self.item_id_to_name[location.default_item_code]))
                    location.address = None
                    location.is_event = True

        if get_option_value(self.multiworld, self.player, "badges") == RandomizeBadges.option_vanilla:
            convert_unrandomized_items_to_events("Badge")
        if get_option_value(self.multiworld, self.player, "hms") == RandomizeHms.option_vanilla:
            convert_unrandomized_items_to_events("HM")
        if get_option_value(self.multiworld, self.player, "rods") == Toggle.option_false:
            convert_unrandomized_items_to_events("Rod")
        if get_option_value(self.multiworld, self.player, "bikes") == Toggle.option_false:
            convert_unrandomized_items_to_events("Bike")
        if get_option_value(self.multiworld, self.player, "key_items") == Toggle.option_false:
            convert_unrandomized_items_to_events("KeyItem")


    def generate_output(self, output_directory: str):
        generate_output(self.multiworld, self.player, output_directory)


    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> PokemonEmeraldItem:
        item_code = self.item_name_to_id[name]
        return PokemonEmeraldItem(
            name,
            get_item_classification(item_code),
            item_code,
            self.player
        )

    def create_item_by_code(self, item_code: int) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )

    def create_event(self, name: str) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            name,
            ItemClassification.progression,
            None,
            self.player
        )
