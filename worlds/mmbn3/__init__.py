import os
import settings
import typing

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, Entrance, \
    LocationProgressType

from worlds.AutoWorld import WebWorld, World

from .Rom import MMBN3DeltaPatch, LocalRom, get_base_rom_path
from .Items import MMBN3Item, ItemData, item_table, all_items, item_frequencies, items_by_id, ItemType, item_groups
from .Locations import Location, MMBN3Location, all_locations, location_table, location_data_table, \
    secret_locations, jobs, location_groups
from .Options import MMBN3Options
from .Regions import regions, RegionName
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName
from worlds.generic.Rules import add_item_rule, add_rule, forbid_item


class MMBN3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MMBN3 Blue US rom"""
        copy_to = "Mega Man Battle Network 3 - Blue Version (USA).gba"
        description = "MMBN3 ROM File"
        md5s = [MMBN3DeltaPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  for operating system default program
        Alternatively, a path to a program to open the .gba file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = True


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
    options_dataclass = MMBN3Options
    options: MMBN3Options
    settings: typing.ClassVar[MMBN3Settings]
    topology_present = False


    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    
    excluded_locations: typing.Set[str]
    item_frequencies: typing.Dict[str, int]

    location_name_groups = location_groups
    item_name_groups = item_groups

    web = MMBN3Web()

    def generate_early(self) -> None:
        """
        called per player before any items or locations are created. You can set properties on your world here.
        Already has access to player options and RNG.
        """
        self.item_frequencies = item_frequencies.copy()
        if self.options.extra_ranks > 0:
            self.item_frequencies[ItemName.Progressive_Undernet_Rank] = 8 + self.options.extra_ranks

        self.excluded_locations = set()
        if not self.options.include_secret:
            self.excluded_locations |= secret_locations
        if not self.options.include_jobs:
            self.excluded_locations |= {job.name for job in jobs}

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

        # Regions which contribute to explore score when accessible.
        explore_score_region_names = (
            RegionName.WWW_Island,
            RegionName.SciLab_Overworld,
            RegionName.SciLab_Cyberworld,
            RegionName.Yoka_Overworld,
            RegionName.Yoka_Cyberworld,
            RegionName.Beach_Overworld,
            RegionName.Beach_Cyberworld,
            RegionName.Undernet,
            RegionName.Deep_Undernet,
            RegionName.Secret_Area,
        )
        explore_score_regions = [self.get_region(region_name) for region_name in explore_score_region_names]

        # Entrances which use explore score in their logic need to register all the explore score regions as indirect
        # conditions.
        def register_explore_score_indirect_conditions(entrance):
            for explore_score_region in explore_score_regions:
                self.multiworld.register_indirect_condition(explore_score_region, entrance)

        for region_info in regions:
            region = name_to_region[region_info.name]
            for connection in region_info.connections:
                entrance = region.connect(name_to_region[connection])

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
                        state.can_reach_region(RegionName.SciLab_Overworld, self.player)
                    self.multiworld.register_indirect_condition(self.get_region(RegionName.SciLab_Overworld), entrance)
                if connection == RegionName.Yoka_Cyberworld:
                    entrance.access_rule = lambda state: \
                        state.has(ItemName.CYokaPas, self.player) or \
                        (
                            state.can_reach_region(RegionName.SciLab_Overworld, self.player) and
                            state.has(ItemName.Press, self.player)
                        )
                    self.multiworld.register_indirect_condition(self.get_region(RegionName.SciLab_Overworld), entrance)
                if connection == RegionName.Beach_Cyberworld:
                    entrance.access_rule = lambda state: state.has(ItemName.CBeacPas, self.player) and\
                        state.can_reach_region(RegionName.Yoka_Overworld, self.player)
                    self.multiworld.register_indirect_condition(self.get_region(RegionName.Yoka_Overworld), entrance)
                if connection == RegionName.Undernet:
                    entrance.access_rule = lambda state: self.explore_score(state) > 8 and\
                        state.has(ItemName.Press, self.player)
                    register_explore_score_indirect_conditions(entrance)
                if connection == RegionName.Secret_Area:
                    entrance.access_rule = lambda state: self.explore_score(state) > 12 and\
                        state.has(ItemName.Hammer, self.player)
                    register_explore_score_indirect_conditions(entrance)
                if connection == RegionName.WWW_Island:
                    entrance.access_rule = lambda state:\
                        state.has(ItemName.Progressive_Undernet_Rank, self.player, 8)

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
            filler_item_name = self.random.choice(filler_items)
            item = self.create_item(filler_item_name)
            self.multiworld.itempool.append(item)
            filler_items.remove(filler_item_name)

    def set_rules(self) -> None:
        """
        called to set access and item rules on locations and entrances.
        """

        # Set WWW ID requirements
        def has_www_id(state): return state.has(ItemName.WWW_ID, self.player)
        add_rule(self.get_location(LocationName.ACDC_1_PMD), has_www_id)
        add_rule(self.get_location(LocationName.SciLab_1_WWW_BMD), has_www_id)
        add_rule(self.get_location(LocationName.Yoka_1_WWW_BMD), has_www_id)
        add_rule(self.get_location(LocationName.Undernet_1_WWW_BMD), has_www_id)

        # Set Press Program requirements
        def has_press(state): return state.has(ItemName.Press, self.player)
        add_rule(self.get_location(LocationName.Yoka_1_PMD), has_press)
        add_rule(self.get_location(LocationName.Yoka_2_Upper_BMD), has_press)
        add_rule(self.get_location(LocationName.Beach_2_East_BMD), has_press)
        add_rule(self.get_location(LocationName.Hades_South_BMD), has_press)
        add_rule(self.get_location(LocationName.Secret_3_BugFrag_BMD), has_press)
        add_rule(self.get_location(LocationName.Secret_3_Island_BMD), has_press)

        # Set Purple Mystery Data Unlocker access
        def can_unlock(state): return state.can_reach_region(RegionName.SciLab_Overworld, self.player) or \
            state.can_reach_region(RegionName.SciLab_Cyberworld, self.player) or \
            state.can_reach_region(RegionName.Yoka_Cyberworld, self.player) or \
            state.has(ItemName.Unlocker, self.player, 8) # There are 8 PMDs that aren't in one of the above areas
        add_rule(self.get_location(LocationName.ACDC_1_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Yoka_1_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Beach_1_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Undernet_7_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Mayls_HP_PMD), can_unlock)
        add_rule(self.get_location(LocationName.SciLab_Dads_Computer_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Zoo_Panda_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Beach_DNN_Security_Panel_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Beach_DNN_Main_Console_PMD), can_unlock)
        add_rule(self.get_location(LocationName.Tamakos_HP_PMD), can_unlock)

        # Set Job additional area access
        self.get_location(LocationName.Please_deliver_this).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player)
        self.get_location(LocationName.My_Navi_is_sick).access_rule =\
            lambda state: \
                state.has(ItemName.Recov30_star, self.player)
        self.get_location(LocationName.Help_me_with_my_son).access_rule =\
            lambda state:\
                state.can_reach_region(RegionName.Yoka_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player)
        self.get_location(LocationName.Transmission_error).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Chip_Prices).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.SciLab_Cyberworld, self.player)
        self.get_location(LocationName.Im_broke).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player) and \
                state.can_reach_region(RegionName.Yoka_Cyberworld, self.player)
        self.get_location(LocationName.Rare_chips_for_cheap).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player)
        self.get_location(LocationName.Be_my_boyfriend).access_rule =\
            lambda state: \
                state.can_reach_region(RegionName.Beach_Cyberworld, self.player)
        self.get_location(LocationName.Will_you_deliver).access_rule=\
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player) and \
                state.can_reach_region(RegionName.Beach_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player)
        self.get_location(LocationName.Somebody_please_help).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player)
        self.get_location(LocationName.Looking_for_condor).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player) and \
                state.can_reach_region(RegionName.Beach_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player)
        self.get_location(LocationName.Help_with_rehab).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Beach_Overworld, self.player)
        self.get_location(LocationName.Help_with_rehab_bonus).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Beach_Overworld, self.player)
        self.get_location(LocationName.Old_Master).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player) and \
                state.can_reach_region(RegionName.Beach_Overworld, self.player)
        self.get_location(LocationName.Catching_gang_members).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Cyberworld, self.player) and \
                state.has(ItemName.Press, self.player)
        self.get_location(LocationName.Please_adopt_a_virus).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.SciLab_Cyberworld, self.player)
        self.get_location(LocationName.Legendary_Tomes).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Beach_Overworld, self.player) and \
                state.can_reach_region(RegionName.Undernet, self.player) and \
                state.can_reach_region(RegionName.Deep_Undernet, self.player) and \
                state.has_all({ItemName.Press, ItemName.Magnum1_A}, self.player)
        self.get_location(LocationName.Legendary_Tomes_Treasure).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player) and \
                state.can_reach_location(LocationName.Legendary_Tomes, self.player)
        self.get_location(LocationName.Hide_and_seek_First_Child).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Hide_and_seek_Second_Child).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Hide_and_seek_Third_Child).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Hide_and_seek_Fourth_Child).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Hide_and_seek_Completion).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player)
        self.get_location(LocationName.Finding_the_blue_Navi).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Undernet, self.player)
        self.get_location(LocationName.Give_your_support).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Beach_Overworld, self.player)
        self.get_location(LocationName.Stamp_collecting).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.Beach_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.SciLab_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.Yoka_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.Beach_Cyberworld, self.player)
        self.get_location(LocationName.Help_with_a_will).access_rule = \
            lambda state: \
                state.can_reach_region(RegionName.ACDC_Overworld, self.player) and \
                state.can_reach_region(RegionName.ACDC_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.Yoka_Overworld, self.player) and \
                state.can_reach_region(RegionName.Yoka_Cyberworld, self.player) and \
                state.can_reach_region(RegionName.Beach_Overworld, self.player) and \
                state.can_reach_region(RegionName.Undernet, self.player)

        # Set Trade quests
        self.get_location(LocationName.ACDC_SonicWav_W_Trade).access_rule =\
            lambda state: state.has(ItemName.SonicWav_W, self.player)
        self.get_location(LocationName.ACDC_Bubbler_C_Trade).access_rule =\
            lambda state: state.has(ItemName.Bubbler_C, self.player)
        self.get_location(LocationName.ACDC_Recov120_S_Trade).access_rule =\
            lambda state: state.has(ItemName.Recov120_S, self.player)
        self.get_location(LocationName.SciLab_Shake1_S_Trade).access_rule =\
            lambda state: state.has(ItemName.Shake1_S, self.player)
        self.get_location(LocationName.Yoka_FireSwrd_P_Trade).access_rule =\
            lambda state: state.has(ItemName.FireSwrd_P, self.player)
        self.get_location(LocationName.Hospital_DynaWav_V_Trade).access_rule =\
            lambda state: state.has(ItemName.DynaWave_V, self.player)
        self.get_location(LocationName.Beach_DNN_WideSwrd_C_Trade).access_rule =\
            lambda state: state.has(ItemName.WideSwrd_C, self.player)
        self.get_location(LocationName.Beach_DNN_HoleMetr_H_Trade).access_rule =\
            lambda state: state.has(ItemName.HoleMetr_H, self.player)
        self.get_location(LocationName.Beach_DNN_Shadow_J_Trade).access_rule =\
            lambda state: state.has(ItemName.Shadow_J, self.player)
        self.get_location(LocationName.Hades_GrabBack_K_Trade).access_rule =\
            lambda state: state.has(ItemName.GrabBack_K, self.player)

        # Set Number Traders

        # The first 8 are considered cheap enough to grind for in ACDC. Protip: Try grinding in the tank
        self.get_location(LocationName.Numberman_Code_09).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_10).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_11).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_12).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_13).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_14).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_15).access_rule = \
            lambda state: self.explore_score(state) > 2
        self.get_location(LocationName.Numberman_Code_16).access_rule = \
            lambda state: self.explore_score(state) > 2

        self.get_location(LocationName.Numberman_Code_17).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_18).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_19).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_20).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_21).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_22).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_23).access_rule =\
            lambda state: self.explore_score(state) > 4
        self.get_location(LocationName.Numberman_Code_24).access_rule =\
            lambda state: self.explore_score(state) > 4

        self.get_location(LocationName.Numberman_Code_25).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.get_location(LocationName.Numberman_Code_26).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.get_location(LocationName.Numberman_Code_27).access_rule =\
            lambda state: self.explore_score(state) > 8
        self.get_location(LocationName.Numberman_Code_28).access_rule =\
            lambda state: self.explore_score(state) > 8

        self.get_location(LocationName.Numberman_Code_29).access_rule =\
            lambda state: self.explore_score(state) > 10
        self.get_location(LocationName.Numberman_Code_30).access_rule =\
            lambda state: self.explore_score(state) > 10
        self.get_location(LocationName.Numberman_Code_31).access_rule =\
            lambda state: self.explore_score(state) > 10

        #miscellaneous locations with extra requirements
        add_rule(self.get_location(LocationName.Comedian),
                 lambda state: state.has(ItemName.Humor, self.player))
        add_rule(self.get_location(LocationName.Villain),
                 lambda state: state.has(ItemName.BlckMnd, self.player))
        forbid_item(self.get_location(LocationName.WWW_1_Central_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_1_East_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_2_East_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_2_Northwest_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_3_East_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_3_North_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_4_Northwest_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_4_Central_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_Wall_BMD),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_Control_Room_1_Screen),
                    ItemName.Progressive_Undernet_Rank, self.player)
        forbid_item(self.get_location(LocationName.WWW_Wilys_Desk),
                    ItemName.Progressive_Undernet_Rank, self.player)

        # I have no fuckin clue why this specific location shits the bed on a progressive undernet rank.
        # If you ever figure it out I will buy you a pizza.
        forbid_item(self.get_location(LocationName.Chocolate_Shop_07),
                    ItemName.Progressive_Undernet_Rank, self.player)

        # place "Victory" at "Final Boss" and set collection as win condition
        self.get_location(LocationName.Alpha_Defeated) \
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
                        if self.options.trade_quest_hinting == 0:
                            item_name_text = "Check"
                        # Partial item hinting
                        elif self.options.trade_quest_hinting == 1:
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
        return self.options.as_dict("extra_ranks", "include_jobs", "trade_quest_hinting")


    def explore_score(self, state):
        """
        Determine roughly how much of the game you can explore to make certain checks not restrict much movement
        """
        score = 0
        if state.can_reach_region(RegionName.WWW_Island, self.player):
            return 999
        if state.can_reach_region(RegionName.SciLab_Overworld, self.player):
            score += 3
        if state.can_reach_region(RegionName.SciLab_Cyberworld, self.player):
            score += 1
        if state.can_reach_region(RegionName.Yoka_Overworld, self.player):
            score += 2
        if state.can_reach_region(RegionName.Yoka_Cyberworld, self.player):
            score += 1
        if state.can_reach_region(RegionName.Beach_Overworld, self.player):
            score += 3
        if state.can_reach_region(RegionName.Beach_Cyberworld, self.player):
            score += 1
        if state.can_reach_region(RegionName.Undernet, self.player):
            score += 2
        if state.can_reach_region(RegionName.Deep_Undernet, self.player):
            score += 1
        if state.can_reach_region(RegionName.Secret_Area, self.player):
            score += 1
        return score
