"""
This module servies as an entrypoint into the Trails in the Sky the 3rd AP world.
"""
from copy import deepcopy
from typing import ClassVar, Counter, Dict, Set

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
)
from .locations import create_locations, location_groups, location_table, default_sealing_stone_quartz
from .options import CharacterStartingQuartzOptions, ChestItemPoolOptions, SealingStoneCharactersOptions, StartingCharactersOptions, TitsThe3rdOptions
from .regions import create_regions, connect_regions
from .settings import TitsThe3rdSettings
from .web import TitsThe3rdWeb


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
    location_name_to_id: Dict[str, int] = location_table

    def create_item(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd item for this player"""
        data: TitsThe3rdItemData = item_data_table[name]
        return TitsThe3rdItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd event for this player"""
        return TitsThe3rdItem(name, True, None, self.player)

    def create_regions(self) -> None:
        """Define regions and locations for Trails in the Sky the 3rd AP"""
        create_regions(self.multiworld, self.player)
        connect_regions(self.multiworld, self.player)
        create_locations(self.multiworld, self.player, self.options.name_spoiler_option)

    def setup_characters(self, itempool: Counter[str]) -> Counter[str]:
        # Randomize starting characters here
        character_list = list(character_table.keys())
        if self.options.starting_character_option == StartingCharactersOptions.option_vanilla:
            character_list.remove(ItemName.kevin)
            character_list.remove(ItemName.ries)
            first_starting_character = ItemName.kevin
            second_starting_character = ItemName.ries
            if self.options.name_spoiler_option:
                self.multiworld.push_precollected(self.create_item(ItemName.original_to_spoiler_mapping[ItemName.kevin]))
                self.multiworld.push_precollected(self.create_item(ItemName.original_to_spoiler_mapping[ItemName.ries]))
            else:
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

            if self.options.name_spoiler_option:
                self.multiworld.push_precollected(self.create_item(ItemName.original_to_spoiler_mapping[first_starting_character]))
                self.multiworld.push_precollected(self.create_item(ItemName.original_to_spoiler_mapping[second_starting_character]))
            else:
                self.multiworld.push_precollected(self.create_item(first_starting_character))
                self.multiworld.push_precollected(self.create_item(second_starting_character))
        else:
            self.multiworld.random.shuffle(character_list)
            first_starting_character = character_list.pop()
            second_starting_character = character_list.pop()
            if self.options.name_spoiler_option:
                first_character_item = self.create_item(ItemName.original_to_spoiler_mapping[first_starting_character])
                second_character_item = self.create_item(ItemName.original_to_spoiler_mapping[second_starting_character])
            else:
                first_character_item = self.create_item(first_starting_character)
                second_character_item = self.create_item(second_starting_character)
            self.multiworld.push_precollected(first_character_item)
            self.multiworld.push_precollected(second_character_item)

        # Sealing Stone Characters
        # Charactersanity
        if self.options.sealing_stone_character_options == SealingStoneCharactersOptions.option_charactersanity:
            if self.options.name_spoiler_option:
                character_list = [ItemName.original_to_spoiler_mapping[character] for character in character_list]
            itempool.update(character_list)
        # Vanilla
        elif self.options.sealing_stone_character_options == SealingStoneCharactersOptions.option_vanilla:
            sealing_stone_locations = deepcopy(LocationName.sealing_stone_locations)
            leftover_characters = list()
            for character in character_list:
                if character in default_character_to_location:
                    location_name = default_character_to_location[character]
                    if self.options.name_spoiler_option:
                        character_item = self.create_item(ItemName.original_to_spoiler_mapping[character])
                        self.multiworld.get_location(LocationName.original_to_spoiler_mapping[location_name], self.player).place_locked_item(character_item)
                    else:
                        character_item = self.create_item(character)
                        self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)
                    sealing_stone_locations.remove(location_name)
                else:
                    leftover_characters.append(character)

            for character in leftover_characters:
                location_name = sealing_stone_locations.pop()
                if self.options.name_spoiler_option:
                    character_item = self.create_item(ItemName.original_to_spoiler_mapping[character])
                    self.multiworld.get_location(LocationName.original_to_spoiler_mapping[location_name], self.player).place_locked_item(character_item)
                else:
                    character_item = self.create_item(character)
                    self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)
        # Shuffle
        else:
            sealing_stone_locations = deepcopy(LocationName.sealing_stone_locations)
            self.multiworld.random.shuffle(sealing_stone_locations)
            for character in character_list:
                location_name = sealing_stone_locations.pop()
                if self.options.name_spoiler_option:
                    character_item = self.create_item(ItemName.original_to_spoiler_mapping[character])
                    self.multiworld.get_location(LocationName.original_to_spoiler_mapping[location_name], self.player).place_locked_item(character_item)
                else:
                    character_item = self.create_item(character)
                    self.multiworld.get_location(location_name, self.player).place_locked_item(character_item)

        return itempool

    def create_items(self) -> None:
        itempool = deepcopy(default_item_pool)
        """Define items for Trails in the Sky the 3rd AP"""
        # Handle Sealing Stone Quartz
        # Vanilla Shuffle
        if self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_vanilla_shuffle:
            itempool.update(default_character_quartz_pool)
        # Vanilla
        elif self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_vanilla:
            for location_name, quartz_name in default_sealing_stone_quartz.items():
                quartz_item = self.create_item(quartz_name)
                if self.options.name_spoiler_option:
                    self.multiworld.get_location(LocationName.original_to_spoiler_mapping[location_name], self.player).place_locked_item(quartz_item)
                else:
                    self.multiworld.get_location(location_name, self.player).place_locked_item(quartz_item)
        # Random Quartz
        elif self.options.character_starting_quartz_options == CharacterStartingQuartzOptions.option_random_quartz:
            quartz_list = list(quartz_table.keys())
            for location_name in default_sealing_stone_quartz:
                quartz_item = self.create_item(self.multiworld.random.choice(quartz_list))
                if self.options.name_spoiler_option:
                    self.multiworld.get_location(LocationName.original_to_spoiler_mapping[location_name], self.player).place_locked_item(quartz_item)
                else:
                    self.multiworld.get_location(location_name, self.player).place_locked_item(quartz_item)
        # All Random: We just let the filler handler further down handle this
        else:
            ...

        # Handle Chest Item Pool
        if self.options.chest_itempool_option == ChestItemPoolOptions.option_vanilla_shuffle:
            itempool.update(default_chest_pool)

        # For now hard code beating Bennu as victory
        victory_item = self.create_item(ItemName.bennu_defeat)
        self.multiworld.get_location(LocationName.chapter1_boss_defeated, self.player).place_locked_item(victory_item)

        # Setup all the playable characters stuffs
        itempool = self.setup_characters(itempool)
        # Generate filler here
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        itempool.update([self.get_filler_item_name() for _ in range(total_locations - itempool.total())])

        for item_name, quantity in itempool.items():
            for _ in range(quantity):
                self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        """Set remaining rules."""
        self.multiworld.completion_condition[self.player] = lambda _: True

    def get_filler_item_name(self):
        filler_item_name = self.multiworld.random.choice(filler_items)

        # TODO: Maybe add more logic here

        return filler_item_name
