import logging
import os
import threading
from typing import ClassVar, Dict, Optional

from . import names
from .items import DWItem, item_table, filler_table, lookup_name_to_id, item_names
from .locations import create_locations, all_locations, location_names
from .regions import create_regions, connect_regions
import settings
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from .rom import DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH, DWPatch
from .options import DWOptions, DWOptionGroups
from .client import DragonWarriorClient

class DWSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Dragon Warrior ROM"""
        description = "Dragon Warrior ROM File"
        copy_to: Optional[str] = "Dragon Warrior (USA) (Rev A).nes"
        md5s = [DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH]
    
    rom_file: RomFile = RomFile(RomFile.copy_to)

class DWWebWorld(WebWorld):
    theme = "grassFlowers"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Dragon Warrior randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serp"]
        )
    ]

    option_groups = DWOptionGroups


class DragonWarriorWorld(World):
    """
    The peace of fair Alefgard has been shattered by the appearance of the nefarious master of the night known as
    the Dragonlord, and the Sphere of Light, which for so long kept the forces of darkness in check, has been stolen!
    It is time for you, a young warrior through whose veins flows the blood of the legendary hero Erdrick, to set out
    on a quest to vanquish the Dragonlord, and save the land from darkness!
    """
    game = "Dragon Warrior"
    authors = ["Serp"]
    settings_key = "dw_options"
    settings: ClassVar[DWSettings]
    options_dataclass = DWOptions
    options: DWOptions
    item_name_to_id = lookup_name_to_id
    item_name_groups = item_names
    location_name_to_id = all_locations
    location_name_groups = location_names
    web = DWWebWorld()
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        levels = 0
        if self.options.levelsanity:
            levels = self.options.levelsanity_range
        tup = create_locations(levels)
        level_locations, high_level_locations = tup[0], tup[1]
        create_regions(self, level_locations, high_level_locations)
        connect_regions(self)

        self.multiworld.get_location(names.rainbow_drop_location, self.player).place_locked_item(self.create_item(names.rainbow_drop))
        self.multiworld.get_location(names.ball_of_light_location, self.player).place_locked_item(self.create_item(names.ball_of_light))

        itempool = []

        # Get the accurate location count between sanity options
        total_locations = 33 + len(level_locations) + len(high_level_locations) + \
            (self.options.searchsanity * 3) + (self.options.shopsanity * 15) + \
            (self.options.monstersanity * 40)

        # The following items always get placed
        itempool += [self.create_item(names.silver_harp),
                     self.create_item(names.staff_of_rain),     
                     self.create_item(names.stones_of_sunlight),
                     self.create_item(names.magic_key),
                     self.create_item(names.death_necklace),
                     self.create_item(names.cursed_belt),
                     self.create_item(names.fighters_ring),
                     self.create_item(names.gwaelins_love),
                     self.create_item(names.high_gold),
                     self.create_item(names.high_gold),
                     self.create_item(names.high_gold)]
        
        
        # The following items are conditional
        if self.options.searchsanity:
            itempool += [
                    self.create_item(names.erdricks_token),
                    self.create_item(names.fairy_flute)
                    ]
            if not self.options.shopsanity:
                itempool.append(self.create_item(names.erdricks_armor))
        
        if self.options.shopsanity:
            itempool += [
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_weapon),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_armor),
                self.create_item(names.progressive_shield),
                self.create_item(names.progressive_shield),
                self.create_item(names.progressive_shield),
            ]
        else:
            itempool.append(self.create_item(names.erdricks_sword))

        if self.options.monstersanity:  # Throw a few more of these in
            itempool += [
                self.create_item(names.high_gold),
                self.create_item(names.high_gold),
                self.create_item(names.high_gold),
            ]

        while len(itempool) < total_locations:
            itempool += [self.create_item(self.get_filler_item_name())]

        self.multiworld.itempool += itempool

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(names.ball_of_light, self.player)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = DWItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(filler_table.keys()))

    def generate_output(self, output_directory: str) -> None:
        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nes")

            patch = DWPatch(os.path.splitext(rompath)[0] + ".apdw",
                            self.player, 
                            self.multiworld.player_name[self.player],
                            flags=self.determine_flags(),
                            searchsanity=self.options.searchsanity,
                            shopsanity=self.options.shopsanity,
                            deathlink=self.options.death_link)
            patch.write()

        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def fill_slot_data(self) -> Dict[str, any]:
        return {
            "searchsanity": self.options.searchsanity.value,
            "levelsanity": self.options.levelsanity.value,
            "shopsanity": self.options.shopsanity.value,
            "monstersanity": self.options.monstersanity.value,
            "death_link": self.options.death_link.value
        }

    def determine_flags(self) -> str:
        ops = self.options
        default_flags = "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAQAAAAAA"
        flag_list = []
        for flag in default_flags:
            flag_list.append(ord(flag))

        # If false, 0 * flag value, otherwise 1 * flag value
        flag_list[1] += int(ops.random_spell_learning) * 1     # B 
        flag_list[1] += int(ops.random_map) * 4                # E
        flag_list[1] += int(ops.random_growth) * 16            # Q
        flag_list[2] += int(ops.random_weapon_prices) * 2      # C
        flag_list[8] += int(ops.random_monster_abilities) * 8  # I
        flag_list[3] += int(ops.heal_hurt_before_more) * 4
        flag_list[3] += int(ops.random_xp_requirements) * 16
        flag_list[2] += int(ops.random_weapon_shops) * 8 * int(not ops.shopsanity)  # Disable random shops when shopsanity is on
        flag_list[8] += int(ops.random_monster_zones) * 2 * int(not ops.monstersanity) # Disable random monsters when monstersanity is on
        flag_list[9] += int(ops.random_monster_stats) * 16
        flag_list[9] += int(ops.random_monster_xp) * 4
        flag_list[9] += int(ops.make_random_stats_consistent) * 1

        flag_list[10] += int(ops.scared_metal_slimes) * 8
        flag_list[10] += int(ops.scaled_metal_slime_xp) * 2
        flag_list[10] += int(ops.scared_metal_slimes) * 8
        flag_list[14] += int(ops.no_hurtmore) * 2
        flag_list[25] += int(ops.only_healmore) * 2
        flag_list[15] += int(ops.no_numbers) * 16
        flag_list[15] += int(ops.invisible_hero) * 4
        flag_list[15] += int(ops.invisible_npcs) * 1

        flag_list[5] += int(ops.enable_menu_wrapping) * 16
        flag_list[5] += int(ops.enable_death_necklace) * 4
        flag_list[5] += int(ops.enable_battle_torches) * 1
        flag_list[6] += int(ops.repel_in_dungeons) * 2
        flag_list[7] += int(ops.permanent_repel) * 16
        flag_list[7] += int(ops.permanent_torch) * 4
        flag_list[11] += int(ops.fast_text) * 4
        flag_list[11] += int(ops.speed_hacks) * 1
        flag_list[21] += int(ops.summer_sale) * 1
        flag_list[21] += int(ops.levelling_speed) * 4   # I think this just works???
        flag_list[30] += int(ops.level_1_radiant) * 8
        flag_list[35] += int(ops.level_1_repel) * 4
        flag_list[16] += int(ops.easy_charlock) * 8
        flag_list[17] += int(ops.modern_spell_names) * 1
        flag_list[23] += int(ops.skip_original_credits) * 4
        flag_list[30] += int(ops.return_escapes) * 4
        flag_list[30] += int(ops.return_to_town) * 2
        flag_list[30] += int(ops.warp_whistle) * 1
        flag_list[31] += int(ops.levelup_refill) * 8
        flag_list[33] += int(ops.ascetic_king) * 4
        flag_list[24] += int(ops.charlock_inn) * 8
        flag_list[28] += int(ops.dl1_crits) * 8
        flag_list[28] += int(ops.dl2_crits) * 2

        flag_list[22] += int(ops.shuffle_music) * 4
        flag_list[22] += int(ops.disable_music) * 2
        flag_list[23] += int(ops.show_death_counter) * 16
        flag_list[22] += int(ops.disable_spell_flashing) * 1
        flag_list[27] += int(ops.disable_red_flashes) * 8
        flag_list[18] += int(ops.noir_mode) * 8
        flag_list[27] += int(ops.magic_herbs) * 16
        flag_list[35] += int(ops.normal_flute_speed) * 2

        # Multiple-choice options
        # Random Map Size
        if ops.random_map_size == 2:
            flag_list[20] += 1
        else:
            flag_list[21] += ops.random_map_size * 16

        # Run Mechanics
        if ops.run_mechanics == 1:
            flag_list[33] += 1
            flag_list[34] += 16
        elif ops.run_mechanics == 2:
            flag_list[34] += 16
        elif ops.run_mechanics == 3:
            flag_list[33] += 1

        # Bonk Damage
        match ops.bonk_damage:
            case 0:
                pass
            case 1:
                flag_list[29] += 8
            case 2:
                flag_list[29] += 16
            case 3:
                flag_list[29] += 24
            case 4:
                flag_list[28] += 1
            case 5:
                flag_list[28] += 1
                flag_list[29] += 8
            case 6:
                flag_list[28] += 1
                flag_list[29] += 16

        final_flags = ""
        for flag in flag_list:
            final_flags += chr(flag)
        
        return final_flags


        
