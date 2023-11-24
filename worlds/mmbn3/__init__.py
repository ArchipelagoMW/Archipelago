import os
import settings
import typing
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, Entrance, \
    LocationProgressType

from worlds.AutoWorld import WebWorld, World
from .Rom import MMBN3DeltaPatch, LocalRom, get_base_rom_path
from .Items import MMBN3Item, ItemData, item_table, all_items, item_frequencies, items_by_id, ItemType
from .Locations import Location, MMBN3Location, all_locations, location_table, location_data_table, \
    always_excluded_locations, jobs
from .Options import MMBN3Options
from .Regions import regions, RegionName
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName
from worlds.generic.Rules import add_item_rule


class MMBN3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MMBN3 Blue US rom"""
        copy_to = "Mega Man Battle Network 3 - Blue Version (USA).gba"
        description = "MMBN3 ROM File"
        md5s = [MMBN3DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class MMBN3Web(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MegaMan Battle Network 3 Randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic"]
    )
    tutorials = [setup_en]


class MMBN3World(World):
    """
    Play as Lan and MegaMan to stop the evil organization WWW led by the nefarious
    Dr. Wily in their plans to take over the Net! Collect BattleChips, Customize your Navi,
    and utilize powerful Style Changes to grow strong enough to take on the greatest
    threat the Internet has ever faced!
    """
    game = "MegaMan Battle Network 3"
    option_definitions = MMBN3Options
    settings: typing.ClassVar[MMBN3Settings]
    topology_present = False

    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    
    excluded_locations: typing.List[str]
    item_frequencies: typing.Dict[str, int]

    web = MMBN3Web()

    def generate_early(self) -> None:
        """
        called per player before any items or locations are created. You can set properties on your world here.
        Already has access to player options and RNG.
        """
        self.item_frequencies = item_frequencies.copy()
        if self.multiworld.extra_ranks[self.player] > 0:
            self.item_frequencies[ItemName.Progressive_Undernet_Rank] = 8 + self.multiworld.extra_ranks[self.player]

        if not self.multiworld.include_jobs[self.player]:
            self.excluded_locations = always_excluded_locations + [job.name for job in jobs]
        else:
            self.excluded_locations = always_excluded_locations

    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """
        name_to_region = {}
        for region_info in regions:
            region = Region(region_info.name, self.player, self.multiworld)
            name_to_region[region_info.name] = region
            for location in region_info.locations:
                loc = MMBN3Location(self.player, location, self.location_name_to_id.get(location, None), region)
                if location in self.excluded_locations:
                    loc.progress_type = LocationProgressType.EXCLUDED
                # Do not place any progression items on WWW Island
                if region_info.name == RegionName.WWW_Island:
                    add_item_rule(loc, lambda item: not item.advancement)
                region.locations.append(loc)
            self.multiworld.regions.append(region)
        for region_info in regions:
            region = name_to_region[region_info.name]
            for connection in region_info.connections:
                connection_region = name_to_region[connection]
                entrance = Entrance(self.player, connection, region)
                entrance.connect(connection_region)

                # ACDC Pending with Start Randomizer
                # if connection == RegionName.ACDC_Overworld:
                #     entrance.access_rule = lambda state: state.has(ItemName.Parasol, self.player)
                if connection == RegionName.SciLab_Overworld:
                    entrance.access_rule = lambda state: state.has(ItemName.SubPET, self.player)
                if connection == RegionName.Yoka_Overworld:
                    entrance.access_rule = lambda state: state.has(ItemName.Needle, self.player)
                if connection == RegionName.Beach_Overworld:
                    entrance.access_rule = lambda state: state.has(ItemName.PETCase, self.player)

                # ACDC Pending with Start Randomizer
                # if connection == RegionName.ACDC_Cyberworld:
                #     entrance.access_rule = lambda state: state.has(ItemName.CACDCPas, self.player)
                if connection == RegionName.SciLab_Cyberworld:
                    entrance.access_rule = lambda state: \
                        state.has(ItemName.CSciPas, self.player) or \
                        state.can_reach(RegionName.SciLab_Overworld, "Region", self.player)
                if connection == RegionName.Yoka_Cyberworld:
                    entrance.access_rule = lambda state: \
                        state.has(ItemName.CYokaPas, self.player) or \
                        (
                            state.can_reach(RegionName.SciLab_Overworld, "Region", self.player) and
                            state.has(ItemName.Press, self.player)
                        )
                if connection == RegionName.Beach_Cyberworld:
                    entrance.access_rule = lambda state: state.has(ItemName.CBeacPas, self.player) and\
                        state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)

                if connection == RegionName.Undernet:
                    entrance.access_rule = lambda state: self.explore_score(state) > 8 and\
                        state.has(ItemName.Press, self.player)
                if connection == RegionName.Secret_Area:
                    entrance.access_rule = lambda state: self.explore_score(state) > 12 and\
                        state.has(ItemName.Hammer, self.player)
                if connection == RegionName.WWW_Island:
                    entrance.access_rule = lambda state:\
                        state.has(ItemName.Progressive_Undernet_Rank, self.player, 8)
                region.exits.append(entrance)

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        for item in all_items:
            if item.progression != ItemClassification.filler:
                freq = self.item_frequencies.get(item.itemName, 1)
                required_items += [item.itemName for _ in range(freq)]

        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        for item in all_items:
            if item.progression == ItemClassification.filler:
                freq = self.item_frequencies.get(item.itemName, 1)
                filler_items += [item.itemName for _ in range(freq)]

        remaining = len(all_locations) - len(required_items)
        for i in range(remaining):
            filler_item_name = self.multiworld.random.choice(filler_items)
            item = self.create_item(filler_item_name)
            self.multiworld.itempool.append(item)
            filler_items.remove(filler_item_name)

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """

        # Set WWW ID requirements
        def has_www_id(state): return state.has(ItemName.WWW_ID, self.player)
        self.multiworld.get_location(LocationName.ACDC_1_PMD, self.player).access_rule = has_www_id
        self.multiworld.get_location(LocationName.SciLab_1_WWW_BMD, self.player).access_rule = has_www_id
        self.multiworld.get_location(LocationName.Yoka_1_WWW_BMD, self.player).access_rule = has_www_id
        self.multiworld.get_location(LocationName.Undernet_1_WWW_BMD, self.player).access_rule = has_www_id

        # Set Press Program requirements
        def has_press(state): return state.has(ItemName.Press, self.player)
        self.multiworld.get_location(LocationName.Yoka_1_PMD, self.player).access_rule = has_press
        self.multiworld.get_location(LocationName.Yoka_2_Upper_BMD, self.player).access_rule = has_press
        self.multiworld.get_location(LocationName.Beach_2_East_BMD, self.player).access_rule = has_press
        self.multiworld.get_location(LocationName.Hades_South_BMD, self.player).access_rule = has_press
        self.multiworld.get_location(LocationName.Secret_3_BugFrag_BMD, self.player).access_rule = has_press
        self.multiworld.get_location(LocationName.Secret_3_Island_BMD, self.player).access_rule = has_press

        # Set Job additional area access
        self.multiworld.get_location(LocationName.Please_deliver_this, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.My_Navi_is_sick, self.player).access_rule =\
            lambda state: \
                state.has(ItemName.Recov30_star, self.player)
        self.multiworld.get_location(LocationName.Help_me_with_my_son, self.player).access_rule =\
            lambda state:\
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Transmission_error, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Chip_Prices, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.SciLab_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Im_broke, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Yoka_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Rare_chips_for_cheap, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Be_my_boyfriend, self.player).access_rule =\
            lambda state: \
                state.can_reach(RegionName.Beach_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Will_you_deliver, self.player).access_rule=\
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Somebody_please_help, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Looking_for_condor, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Help_with_rehab, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Old_Master, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Catching_gang_members, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Cyberworld, "Region", self.player) and \
                state.has(ItemName.Press, self.player)
        self.multiworld.get_location(LocationName.Please_adopt_a_virus, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.SciLab_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Legendary_Tomes, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Undernet, "Region", self.player) and \
                state.can_reach(RegionName.Deep_Undernet, "Region", self.player) and \
                state.has_all({ItemName.Press, ItemName.Magnum1_A}, self.player)
        self.multiworld.get_location(LocationName.Legendary_Tomes_Treasure, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player) and \
                state.can_reach(LocationName.Legendary_Tomes, "Location", self.player)
        self.multiworld.get_location(LocationName.Hide_and_seek_First_Child, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Hide_and_seek_Second_Child, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Hide_and_seek_Third_Child, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Hide_and_seek_Fourth_Child, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Hide_and_seek_Completion, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Finding_the_blue_Navi, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Undernet, "Region", self.player)
        self.multiworld.get_location(LocationName.Give_your_support, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Stamp_collecting, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.SciLab_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.Yoka_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.Beach_Cyberworld, "Region", self.player)
        self.multiworld.get_location(LocationName.Help_with_a_will, self.player).access_rule = \
            lambda state: \
                state.can_reach(RegionName.ACDC_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.ACDC_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.Yoka_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Yoka_Cyberworld, "Region", self.player) and \
                state.can_reach(RegionName.Beach_Overworld, "Region", self.player) and \
                state.can_reach(RegionName.Undernet, "Region", self.player)

        # Set Trade quests
        self.multiworld.get_location(LocationName.ACDC_SonicWav_W_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.SonicWav_W, self.player)
        self.multiworld.get_location(LocationName.ACDC_Bubbler_C_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.Bubbler_C, self.player)
        self.multiworld.get_location(LocationName.ACDC_Recov120_S_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.Recov120_S, self.player)
        self.multiworld.get_location(LocationName.SciLab_Shake1_S_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.Shake1_S, self.player)
        self.multiworld.get_location(LocationName.Yoka_FireSwrd_P_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.FireSwrd_P, self.player)
        self.multiworld.get_location(LocationName.Hospital_DynaWav_V_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.DynaWave_V, self.player)
        self.multiworld.get_location(LocationName.Beach_DNN_WideSwrd_C_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.WideSwrd_C, self.player)
        self.multiworld.get_location(LocationName.Beach_DNN_HoleMetr_H_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.HoleMetr_H, self.player)
        self.multiworld.get_location(LocationName.Beach_DNN_Shadow_J_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.Shadow_J, self.player)
        self.multiworld.get_location(LocationName.Hades_GrabBack_K_Trade, self.player).access_rule =\
            lambda state: state.has(ItemName.GrabBack_K, self.player)

        # Set Number Traders

        # The first 8 are considered cheap enough to grind for in ACDC. Protip: Try grinding in the tank
        self.multiworld.get_location(LocationName.Numberman_Code_09, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_10, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_11, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_12, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_13, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_14, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_15, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.multiworld.get_location(LocationName.Numberman_Code_16, self.player).access_rule = \
            lambda state: self.explore_score(state) > 2

        self.multiworld.get_location(LocationName.Numberman_Code_17, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_18, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_19, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_20, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_21, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_22, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_23, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.multiworld.get_location(LocationName.Numberman_Code_24, self.player).access_rule =\
            lambda state: self.explore_score(state) > 4

        self.multiworld.get_location(LocationName.Numberman_Code_25, self.player).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.multiworld.get_location(LocationName.Numberman_Code_26, self.player).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.multiworld.get_location(LocationName.Numberman_Code_27, self.player).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.multiworld.get_location(LocationName.Numberman_Code_28, self.player).access_rule =\
            lambda state: self.explore_score(state) > 8

        self.multiworld.get_location(LocationName.Numberman_Code_29, self.player).access_rule =\
            lambda state: self.explore_score(state) > 10
        self.multiworld.get_location(LocationName.Numberman_Code_30, self.player).access_rule =\
            lambda state: self.explore_score(state) > 10
        self.multiworld.get_location(LocationName.Numberman_Code_31, self.player).access_rule =\
            lambda state: self.explore_score(state) > 10

        def not_undernet(item): return item.code != item_table[ItemName.Progressive_Undernet_Rank].code or item.player != self.player
        self.multiworld.get_location(LocationName.WWW_1_Central_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_1_East_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_2_East_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_2_Northwest_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_3_East_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_3_North_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_4_Northwest_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_4_Central_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_Wall_BMD, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_Control_Room_1_Screen, self.player).item_rule = not_undernet
        self.multiworld.get_location(LocationName.WWW_Wilys_Desk, self.player).item_rule = not_undernet

        # place "Victory" at "Final Boss" and set collection as win condition
        self.multiworld.get_location(LocationName.Alpha_Defeated, self.player) \
            .place_locked_item(self.create_event(ItemName.Victory))
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_output(self, output_directory: str) -> None:
        rompath: str = ""

        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())

            for location_name in location_table.keys():
                location = world.get_location(location_name, player)
                ap_item = location.item
                item_id = ap_item.code
                if item_id is not None:
                    if ap_item.player != player or item_id not in items_by_id:
                        item = ItemData(item_id, ap_item.name, ap_item.classification, ItemType.External)
                        item = item._replace(recipient=self.multiworld.player_name[ap_item.player])
                    else:
                        item = items_by_id[item_id]

                    location_data = location_data_table[location_name]
                    # print("Placing item "+item.itemName+" at location "+location_data.name)
                    rom.replace_item(location_data, item)
                    if location_data.inject_name:
                        item_name_text = "Item"
                        long_item_text = ""

                        # No item hinting
                        if self.multiworld.trade_quest_hinting[self.player] == 0:
                            item_name_text = "Check"
                        # Partial item hinting
                        elif self.multiworld.trade_quest_hinting[self.player] == 1:
                            if item.progression == ItemClassification.progression \
                                    or item.progression == ItemClassification.progression_skip_balancing:
                                item_name_text = "Progress"
                            elif item.progression == ItemClassification.useful \
                                    or item.progression == ItemClassification.trap:
                                item_name_text = "Item"
                            else:
                                item_name_text = "Garbage"

                            if item.recipient == 'Myself':
                                item_name_text = "Your " + item_name_text
                            else:
                                item_name_text = item.recipient + "'s " + item_name_text
                        # Full item hinting
                        else:
                            owners_name = "Your" if item.recipient == 'Myself' else item.recipient + "'s"
                            long_item_text = f"It's {owners_name} \n\"{item.itemName}\"!!"

                        rom.insert_hint_text(location_data, item_name_text, long_item_text)

            rom.inject_name(world.player_name[player])

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.gba")

            rom.write_changed_rom()
            rom.write_to_file(rompath)

            patch = MMBN3DeltaPatch(os.path.splitext(rompath)[0]+MMBN3DeltaPatch.patch_file_ending, player=player,
                                    player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        return MMBN3Item(item.itemName, item.progression, item.code, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return MMBN3Item(event, ItemClassification.progression, None, self.player)

    def fill_slot_data(self):
        return {name: getattr(self.multiworld, name)[self.player].value for name in self.option_definitions}


    def explore_score(self, state):
        """
        Determine roughly how much of the game you can explore to make certain checks not restrict much movement
        """
        score = 0
        if state.can_reach(RegionName.WWW_Island, "Region", self.player):
            return 999
        if state.can_reach(RegionName.SciLab_Overworld, "Region", self.player):
            score += 3
        if state.can_reach(RegionName.SciLab_Cyberworld, "Region", self.player):
            score += 1
        if state.can_reach(RegionName.Yoka_Overworld, "Region", self.player):
            score += 2
        if state.can_reach(RegionName.Yoka_Cyberworld, "Region", self.player):
            score += 1
        if state.can_reach(RegionName.Beach_Overworld, "Region", self.player):
            score += 3
        if state.can_reach(RegionName.Beach_Cyberworld, "Region", self.player):
            score += 1
        if state.can_reach(RegionName.Undernet, "Region", self.player):
            score += 2
        if state.can_reach(RegionName.Deep_Undernet, "Region", self.player):
            score += 1
        if state.can_reach(RegionName.Secret_Area, "Region", self.player):
            score += 1
        return score
