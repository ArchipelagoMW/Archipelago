import os
import typing
import settings

from BaseClasses import Item, Region, MultiWorld, Tutorial, ItemClassification
from .items import CV64Item, filler_item_names, get_item_info, get_item_names_to_ids, get_item_counts
from .locations import CV64Location, get_location_info, verify_locations, get_location_names_to_ids, base_id
from .entrances import verify_entrances, get_warp_entrances
from .options import CV64Options
from .stages import get_locations_from_stage, get_normal_stage_exits, vanilla_stage_order, \
    shuffle_stages, generate_warps, get_region_names
from .regions import get_region_info
from .rules import CV64Rules
from .data import iname, rname, ename
from ..AutoWorld import WebWorld, World
from .aesthetics import randomize_lighting, shuffle_sub_weapons, rom_empty_breakables_flags, rom_sub_weapon_flags, \
    randomize_music, get_start_inventory_data, get_location_data, randomize_shop_prices, get_loading_zone_bytes, \
    get_countdown_numbers
from .rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch
from .client import Castlevania64Client


class CV64Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the CV64 US 1.0 rom"""
        copy_to = "Castlevania (USA).z64"
        description = "CV64 (US 1.0) ROM File"
        md5s = [CV64DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CV64Web(WebWorld):
    theme = "stone"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Castlevania 64 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )]


class CV64World(World):
    """
    Castlevania for the Nintendo 64 is the first 3D game in the franchise. As either whip-wielding Belmont descendant
    Reinhardt Schneider or powerful sorceress Carrie Fernandez, brave many terrifying traps and foes as you make your
    way to Dracula's chamber and stop his rule of terror.
    """
    game = "Castlevania 64"
    item_name_groups = {
        "Bomb": {iname.magical_nitro, iname.mandragora},
        "Ingredient": {iname.magical_nitro, iname.mandragora},
    }
    location_name_groups = {stage: set(get_locations_from_stage(stage)) for stage in vanilla_stage_order}
    options_dataclass = CV64Options
    options: CV64Options
    settings: typing.ClassVar[CV64Settings]
    topology_present = True
    data_version = 1

    item_name_to_id = get_item_names_to_ids()
    location_name_to_id = get_location_names_to_ids()

    web = CV64Web()

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        self.active_stage_exits: typing.Dict[str, typing.Dict] = {}
        self.active_stage_list: typing.List[str] = []
        self.active_warp_list: typing.List[str] = []
        self.reinhardt_stages: bool = True
        self.carrie_stages: bool = True
        self.branching_stages: bool = False
        self.starting_stage: str = rname.forest_of_silence

        self.total_s1s: int = 0
        self.s1s_per_warp: int = 0
        self.total_s2s: int = 0
        self.required_s2s: int = 0
        self.drac_condition: int = 0

        super().__init__(multiworld, player)

    @classmethod
    def stage_assert_generate(cls, world) -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        self.total_s1s = self.options.total_special1s.value
        self.s1s_per_warp = self.options.special1s_per_warp.value
        self.total_s2s = self.options.total_special2s.value
        self.required_s2s = int(self.options.percent_special2s_required.value / 100 * self.total_s2s)
        self.drac_condition = self.options.draculas_condition.value

        # If there are more S1s needed to unlock the whole warp menu than there are S1s in total, drop S1s per warp to
        # something manageable.
        while self.s1s_per_warp * 7 > self.total_s1s:
            self.s1s_per_warp -= 1

        # Enable/disable character stages and branching paths accordingly
        if self.options.character_stages.value == self.options.character_stages.option_reinhardt_only:
            self.carrie_stages = False
        elif self.options.character_stages.value == self.options.character_stages.option_carrie_only:
            self.reinhardt_stages = False
        elif self.options.character_stages.value == self.options.character_stages.option_both:
            self.branching_stages = True

        self.active_stage_exits = get_normal_stage_exits(self)

        stage_1_blacklist = []

        # Prevent Clock Tower from being Stage 1 if more than 4 S1s are needed to warp out of it.
        if self.s1s_per_warp > 4 and not self.options.multi_hit_breakables.value:
            stage_1_blacklist.append(rname.clock_tower)

        # Shuffle the stages if the option is on.
        if self.options.stage_shuffle:
            self.active_stage_exits, self.starting_stage, self.active_stage_list = \
                shuffle_stages(self, stage_1_blacklist)
        else:
            self.active_stage_list = [stage for stage in vanilla_stage_order if stage in self.active_stage_exits]

        # Create a list of warps from the active stage list. They are in a random order by default and will never
        # include the starting stage.
        self.active_warp_list = generate_warps(self)

    def create_regions(self) -> None:
        # Create the Menu region.
        active_regions = {"Menu": Region("Menu", self.player, self.multiworld)}

        # Create every stage region by checking to see if that stage is active.
        active_regions.update({name: Region(name, self.player, self.multiworld) for name in
                               get_region_names(self.active_stage_exits)})

        # Add the Renon's shop region if shopsanity is on.
        if self.options.shopsanity.value:
            active_regions.update({rname.renon: Region(rname.renon, self.player, self.multiworld)})

        # Add the Dracula's chamber (the end) region.
        active_regions.update({rname.ck_drac_chamber: Region(rname.ck_drac_chamber, self.player, self.multiworld)})

        # Add the locations to the regions.
        for reg_name in active_regions:
            reg_locs = get_region_info(reg_name, "locations")
            if reg_locs is not None:
                active_regions[reg_name].add_locations(verify_locations(self.options, reg_locs), CV64Location)

        # Set up the regions correctly.
        for region in active_regions:
            self.multiworld.regions.append(active_regions[region])

        # Add the warp Entrances to Menu.
        active_regions["Menu"].add_exits(get_warp_entrances(self.active_warp_list))

        # Add the Entrances to the stage regions.
        for reg_name in active_regions:
            reg_ents = get_region_info(reg_name, "entrances")
            if reg_ents is not None:
                active_regions[reg_name].add_exits(verify_entrances(self.options, reg_ents, self.active_stage_exits))

    def create_item(self, name: str, force_classification=None) -> Item:
        if force_classification is not None:
            classification = getattr(ItemClassification, force_classification)
        else:
            classification = getattr(ItemClassification, get_item_info(name, "default classification"))

        code = get_item_info(name, "code")
        if code is not None:
            code += base_id

        created_item = CV64Item(name, classification, code, self.player)

        return created_item

    def create_items(self) -> None:
        item_counts = get_item_counts(self)

        # Set up the items correctly
        for classification in item_counts:
            for item in item_counts[classification]:
                self.multiworld.itempool += [self.create_item(item, classification)
                                             for _ in range(item_counts[classification][item])]

    def set_rules(self) -> None:
        active_regions = self.multiworld.get_regions(self.player)

        # Set the required Special2s to the number of available bosses or crystal events returned if Special2s
        # are not the goal.
        if self.options.draculas_condition == self.options.draculas_condition.option_crystal:
            self.total_s2s = 1
            self.required_s2s = 1
        elif self.options.draculas_condition != self.options.draculas_condition.option_specials:
            self.total_s2s = 0
            self.required_s2s = 0

        for region in active_regions:
            # Place event items where they should be.
            for loc in region.locations:
                if loc.address is None:
                    event_item = get_location_info(loc.name, "event")
                    loc.place_locked_item(self.create_item(event_item, "progression"))
                    # If we're looking at a boss kill trophy, increment the total S2s and, if we're not already at the
                    # set number of required bosses, the total required number. This way, we can prevent gen failures
                    # should the player set more bosses required than there are total.
                    if event_item == iname.trophy:
                        self.total_s2s += 1
                        if self.required_s2s < self.options.bosses_required.value:
                            self.required_s2s += 1

        # Set up the rules properly.
        CV64Rules(self).set_cv64_rules()

    def pre_fill(self) -> None:
        # If we need more Special1s to warp out of Sphere 1 than there are locations available, then AP's fill
        # algorithm may try placing the Special1s anyway despite placing the stage's single key always being an option.
        # To get around this problem in the fill algorithm, the keys will be forced early in these situations to ensure
        # the algorithm will pick them over the Special1s.
        if self.starting_stage == rname.tower_of_science:
            if self.s1s_per_warp > 3:
                self.multiworld.local_early_items[self.player][iname.science_key2] = 1
        elif self.starting_stage == rname.clock_tower:
            if (self.s1s_per_warp > 2 and self.options.multi_hit_breakables.value is False) or \
                    (self.s1s_per_warp > 8 and self.options.multi_hit_breakables.value is True):
                self.multiworld.local_early_items[self.player][iname.clocktower_key1] = 1
        elif self.starting_stage == rname.castle_wall:
            if self.s1s_per_warp > 5 and self.options.hard_logic.value is False and \
                    self.options.multi_hit_breakables.value is False:
                self.multiworld.local_early_items[self.player][iname.left_tower_key] = 1

    def generate_output(self, output_directory: str) -> None:
        active_locations = self.multiworld.get_locations(self.player)

        # Location data and shop names, descriptions, and colors
        offset_data, shop_name_list, shop_colors_list, shop_desc_list = \
            get_location_data(self, active_locations)
        # Shop prices
        if self.options.shop_prices.value:
            offset_data.update(randomize_shop_prices(self))
        # Map lighting
        if self.options.map_lighting.value:
            offset_data.update(randomize_lighting(self))
        # Sub-weapons
        if self.options.sub_weapon_shuffle.value == self.options.sub_weapon_shuffle.option_own_pool:
            offset_data.update(shuffle_sub_weapons(self))
        elif self.options.sub_weapon_shuffle.value == self.options.sub_weapon_shuffle.option_anywhere:
            offset_data.update(rom_sub_weapon_flags)
        # Empty breakables
        if self.options.empty_breakables.value:
            offset_data.update(rom_empty_breakables_flags)
        # Music
        if self.options.background_music.value:
            offset_data.update(randomize_music(self))
        # Loading zones
        offset_data.update(get_loading_zone_bytes(self.options, self.starting_stage, self.active_stage_exits))
        # Countdown
        if self.options.countdown.value:
            offset_data.update(get_countdown_numbers(self.options, active_locations))
        # Start Inventory
        offset_data.update(get_start_inventory_data(self.player, self.options,
                                                    self.multiworld.precollected_items[self.player]))

        cv64_rom = LocalRom(get_base_rom_path())

        slot_name = self.multiworld.player_name[self.player].encode("utf-8")

        rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.z64")

        patch_rom(self, cv64_rom, offset_data, shop_name_list, shop_desc_list, shop_colors_list, slot_name,
                  active_locations)

        cv64_rom.write_to_file(rompath)

        patch = CV64DeltaPatch(os.path.splitext(rompath)[0] + CV64DeltaPatch.patch_file_ending, player=self.player,
                               player_name=self.multiworld.player_name[self.player], patched_path=rompath)
        patch.write()
        os.unlink(rompath)

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # Write the stage order to the spoiler log
        spoiler_handle.write(f"\nCastlevania 64 stage & warp orders for {self.multiworld.player_name[self.player]}:\n")
        for stage in self.active_stage_list:
            num = str(self.active_stage_exits[stage]["position"]).zfill(2)
            path = self.active_stage_exits[stage]["path"]
            spoiler_handle.writelines(f"Stage {num}{path}:\t{stage}\n")

        # Write the warp order to the spoiler log
        spoiler_handle.writelines(f"\nStart :\t{self.active_stage_list[0]}\n")
        for i in range(1, len(self.active_warp_list)):
            spoiler_handle.writelines(f"Warp {i}:\t{self.active_warp_list[i]}\n")

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {"death_link": self.options.death_link.value,
                "shopsanity": self.options.shopsanity.value}

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        # Attach each location's stage's position to its hint information if Stage Shuffle is on.
        if self.options.stage_shuffle.value:
            stage_pos_data = {}
            for loc in list(self.multiworld.get_locations(self.player)):
                stage = get_region_info(loc.parent_region.name, "stage")
                if stage is not None and loc.address is not None:
                    num = str(self.active_stage_exits[stage]["position"]).zfill(2)
                    path = self.active_stage_exits[stage]["path"]
                    stage_pos_data[loc.address] = f"Stage {num}"
                    if path != " ":
                        stage_pos_data[loc.address] += path
            hint_data[self.player] = stage_pos_data
