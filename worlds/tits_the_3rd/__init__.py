"""
This module servies as an entrypoint into the Trails in the Sky the 3rd AP world.
"""
from copy import deepcopy
from typing import ClassVar, Counter, Dict, Set, Any

from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from worlds.tits_the_3rd.names.item_name import ItemName
from worlds.tits_the_3rd.names.location_name import LocationName
from .items import (
    default_item_pool,
    item_data_table,
    item_groups,
    item_table,
    TitsThe3rdItem,
    TitsThe3rdItemData,
    character_table,
    quartz_table,
    filler_items,
    default_chest_pool,
    default_character_quartz_pool,
    default_character_to_location,
    default_craft_pool,
)
from .tables.location_list import craft_locations, location_table, default_sealing_stone_quartz
from .locations import create_locations, location_groups
from .options import CharacterStartingQuartzOptions, ChestItemPoolOptions, SealingStoneCharactersOptions, StartingCharactersOptions, TitsThe3rdOptions, CraftShuffle, CraftPlacement
from .regions import create_regions, connect_regions
from .settings import TitsThe3rdSettings
from .web import TitsThe3rdWeb
from .tables import location_list
from .crafts.craft_randomizer import shuffle_crafts_main
from .spoiler_mapping import scrub_spoiler_data

def launch_client():
    """Launch a Trails in the Sky the 3rd client instance"""
    from worlds.tits_the_3rd.client.client import launch

    launch_subprocess(launch, name="TitsThe3rdClient")


components.append(Component("Trails in the Sky the 3rd Client", "TitsThe3rdClient", func=launch_client, component_type=Type.CLIENT))


class TitsThe3rdWorld(World):
    """
    Trails in the Sky the 3rd is a JRPG from the "Trails of" / "Kiseki" series,
    released in 2007 and developed by Nihon Falcom. Embark on an emotional rollercoaster
    following Father Kevin Graham and Ries Argent during their journey to escape the
    mysterious dimension of Phantasma. It is highly recommended to pick up the first two
    games before playing this one, Trails in the Sky FC / SC.
    """

    game: str = "Trails in the Sky the 3rd"
    options_dataclass = TitsThe3rdOptions
    options: TitsThe3rdOptions
    topology_present: bool = True
    settings: ClassVar[TitsThe3rdSettings]
    web: WebWorld = TitsThe3rdWeb()
    base_id: int = 1954308624560

    item_name_groups: Dict[str, Set[str]] = item_groups
    location_name_groups: Dict[str, Set[str]] = location_groups
    item_name_to_id: Dict[str, int] = item_table
    location_name_to_id: Dict[str, int] = {key: data.flag for key, data in location_table.items()}

    def create_item(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd item for this player"""
        data: TitsThe3rdItemData = item_data_table[name]
        if self.options.name_spoiler_option:
            name = scrub_spoiler_data(name)
        return TitsThe3rdItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd event for this player"""
        return TitsThe3rdItem(name, True, None, self.player)

    def create_regions(self) -> None:
        """Define regions and locations for Trails in the Sky the 3rd AP"""
        create_regions(self.multiworld, self.player)
        connect_regions(self.multiworld, self.player)
        create_locations(self.multiworld, self.player, self.options)

    def setup_characters(self, itempool: Counter[str]) -> Counter[str]:
        # Randomize starting characters here
        character_list = list(character_table.keys())
        if self.options.starting_character_option == StartingCharactersOptions.option_vanilla:
            character_list.remove(ItemName.kevin)
            character_list.remove(ItemName.ries)
            first_starting_character = ItemName.kevin
            second_starting_character = ItemName.ries
            self.multiworld.push_precollected(self.create_item(ItemName.kevin))
            self.multiworld.push_precollected(self.create_item(ItemName.ries))
        elif self.options.starting_character_option == StartingCharactersOptions.option_set:
            first_starting_character = self.options.first_starting_character.current_key.capitalize()
            character_list.remove(first_starting_character)

            second_starting_character = self.options.second_starting_character.current_key.capitalize()
            if second_starting_character == first_starting_character:
                self.multiworld.random.shuffle(character_list)
                second_starting_character = character_list.pop()
            else:
                character_list.remove(second_starting_character)

            self.multiworld.push_precollected(self.create_item(first_starting_character))
            self.multiworld.push_precollected(self.create_item(second_starting_character))
        else:
            self.multiworld.random.shuffle(character_list)
            first_starting_character = character_list.pop()
            second_starting_character = character_list.pop()
            self.multiworld.push_precollected(self.create_item(first_starting_character))
            self.multiworld.push_precollected(self.create_item(second_starting_character))

        # Sealing Stone Characters
        # Charactersanity
        if self.options.sealing_stone_character_options == SealingStoneCharactersOptions.option_charactersanity:
            itempool.update(character_list)
        # Vanilla
        elif self.options.sealing_stone_character_options == SealingStoneCharactersOptions.option_vanilla:
            sealing_stone_locations = deepcopy(LocationName.sealing_stone_locations)
            leftover_characters = list()
            for character in character_list:
                if character in default_character_to_location:
                    location_name = default_character_to_location[character]
                    character_item = self.create_item(character)
                    self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)
                    sealing_stone_locations.remove(location_name)
                else:
                    leftover_characters.append(character)

            for character in leftover_characters:
                location_name = sealing_stone_locations.pop()
                character_item = self.create_item(character)
                self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)
        # Shuffle
        else:
            sealing_stone_locations = deepcopy(LocationName.sealing_stone_locations)
            self.multiworld.random.shuffle(sealing_stone_locations)
            for character in character_list:
                location_name = sealing_stone_locations.pop()
                character_item = self.create_item(character)
                self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)

        return itempool

    def _set_default_craft_locations_for_character(self, location_names: Set[str], item_name: ItemName) -> None:
        """
        Given a set of craft location names, set them to the progressive craft for the given character.

        Args:
            location_names (Set[str]): The set of location names to set the progressive craft for.
            item_name (ItemName): The item name of the progressive craft.

        Returns:
            None
        """
        for location_name in location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(item_name))

    def _set_default_craft_locations(self) -> None:
        """
        Set the craft unlock locations for each character to the default location.

        Returns:
            None
        """
        self._set_default_craft_locations_for_character(location_names=location_groups["Estelle Crafts"], item_name=ItemName.estelle_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Joshua Crafts"], item_name=ItemName.joshua_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Scherazard Crafts"], item_name=ItemName.scherazard_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Olivier Crafts"], item_name=ItemName.olivier_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Kloe Crafts"], item_name=ItemName.kloe_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Agate Crafts"], item_name=ItemName.agate_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Tita Crafts"], item_name=ItemName.tita_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Zin Crafts"], item_name=ItemName.zin_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Kevin Crafts"], item_name=ItemName.kevin_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Anelace Crafts"], item_name=ItemName.anelace_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Josette Crafts"], item_name=ItemName.josette_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Richard Crafts"], item_name=ItemName.richard_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Mueller Crafts"], item_name=ItemName.mueller_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Julia Crafts"], item_name=ItemName.julia_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Ries Crafts"], item_name=ItemName.ries_progressive_craft)
        self._set_default_craft_locations_for_character(location_names=location_groups["Renne Crafts"], item_name=ItemName.renne_progressive_craft)

    def pre_fill(self) -> None:
        # For now hard code beating Bennu as victory
        chapter_1_item = self.create_item(ItemName.bennu_defeat)
        chapter_2_item = self.create_item(ItemName.kloe_rescue)
        # TODO: change victory condition
        self.multiworld.get_location(LocationName.chapter1_boss_defeated, self.player).place_locked_item(chapter_1_item)
        self.multiworld.get_location(LocationName.chapter2_boss_defeated, self.player).place_locked_item(chapter_2_item)
        # Crafts
        if self.options.craft_placement == CraftPlacement.option_default and self.options.craft_shuffle:
            # Crafts are at their default locations, but which craft is given is randomized.
            # (E.g. Estelle may get Dual Strike when she levels up)
            self._set_default_craft_locations()
        elif self.options.craft_placement == CraftPlacement.option_crafts:
            # Crafts are shuffled amongst each other (e.g. levelling up as character X may give a craft for character Y)
            craft_items = []
            for item_name, quantity in default_craft_pool.items():
                for _ in range(quantity):
                    craft_items.append(self.create_item(item_name))
            remaining_craft_locations = list(craft_locations.keys())
            for item in craft_items:
                location_name = self.multiworld.random.choice(remaining_craft_locations)
                self.multiworld.get_location(location_name, self.player).place_locked_item(item)
                remaining_craft_locations.remove(location_name)

    def create_items(self) -> None:
        """Define items for Trails in the Sky the 3rd AP"""
        itempool = deepcopy(default_item_pool)

        # Setup all the playable characters stuffs
        itempool = self.setup_characters(itempool)

        # Handle Sealing Stone Quartz
        # Vanilla Shuffle
        if self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_vanilla_shuffle:
            itempool.update(default_character_quartz_pool)
        # Vanilla
        elif self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_vanilla:
            for location_name, quartz_name in default_sealing_stone_quartz.items():
                quartz_item = self.create_item(quartz_name)
                self.multiworld.get_location(location_name, self.player).place_locked_item(quartz_item)
        # Random Quartz
        elif self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_random_quartz:
            quartz_list = list(quartz_table.keys())
            for location_name in default_sealing_stone_quartz:
                quartz_item = self.create_item(self.multiworld.random.choice(quartz_list))
                self.multiworld.get_location(location_name, self.player).place_locked_item(quartz_item)
        # Else all random (NOP): We just let the filler handler further down handle this

        # Handle Chest Item Pool
        if self.options.chest_itempool_option == ChestItemPoolOptions.option_vanilla_shuffle:
            itempool.update(default_chest_pool)

        # Add craft items to item pool.
        # If crafts are shuffled amongst each other, or placed as their default locations, this was placed in prefill.
        if self.options.craft_placement == CraftPlacement.option_anywhere:
            itempool.update(default_craft_pool)

        # Generate filler here
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        itempool.update([self.get_filler_item_name() for _ in range(total_locations - itempool.total())])

        for item_name, quantity in itempool.items():
            for _ in range(quantity):
                self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        """Set remaining rules."""
        self.multiworld.completion_condition[self.player] = lambda _: True

    def fill_slot_data(self) -> Dict[str, Any]:
        # Note: if craft shuffle is on, event get crafts will be a random progressive craft.
        # If craft shuffle is off, event get crafts will be the default craft.
        #   For these, craft_get_order will be ignored.
        # This behaviour is handled by the client.
        craft_get_order, old_craft_id_to_new_craft_id = shuffle_crafts_main(self.options, self.random)
        return {
            "craft_get_order": craft_get_order,
            "old_craft_id_to_new_craft_id": old_craft_id_to_new_craft_id,
            "default_event_crafts": self.options.craft_placement == CraftPlacement.option_default and not self.options.craft_shuffle,
            "default_crfget": self.options.craft_placement == CraftPlacement.option_default and not self.options.craft_shuffle,
        }

    def get_filler_item_name(self):
        filler_item_name = self.multiworld.random.choice(filler_items)

        # TODO: Maybe add more logic here

        return filler_item_name
