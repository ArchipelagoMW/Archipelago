import logging
from .constants.mounts import *
from .constants.jobs import *
from .constants.keys import *
from .constants.key_items import *
from .constants.maps import *
from .constants.ap_regions import *
from .constants.display_regions import *
from .constants.teleport_stones import *
from .constants.item_groups import *
from .constants.location_groups import *
from .constants.region_passes import *
from .home_point_locations import get_home_points
from .items import item_table, optional_scholar_abilities, filler_items, \
    get_item_names_per_category, progressive_equipment, non_progressive_equipment, get_starting_jobs, \
    set_jobs_at_default_locations, key_rings, dungeon_keys, singleton_keys, \
    display_region_name_to_pass_dict, job_crystal_beginner_dictionary, job_crystal_advanced_dictionary, job_crystal_expert_dictionary, home_point_item_index_offset, ItemData
from .locations import get_treasure_and_npc_locations, get_boss_locations, get_shop_locations, get_region_completion_locations, LocationData, get_location_names_per_category, \
    get_location_name_to_id, get_crystal_locations, home_point_location_index_offset
from .presets import crystal_project_options_presets
from .regions import init_ap_region_to_display_region_dictionary, init_areas, ap_region_to_display_region_dictionary, display_region_subregions_dictionary, \
    display_region_levels_dictionary
from .options import CrystalProjectOptions, create_option_groups
from .rules import CrystalProjectLogic
from .mod_helper import ModLocationData, get_modded_items, get_modded_locations, get_modded_home_points, \
    get_modded_shopsanity_locations, get_modded_bosses, build_condition_rule, update_item_classification, get_mod_info, get_removed_locations, get_removed_home_points
from typing import List, Set, Dict, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, MultiWorld, CollectionState, ItemClassification

class CrystalProjectWeb(WebWorld):
    theme = "jungle"
    bug_report_page = "https://github.com/Emerassi/CrystalProjectAPWorld/issues"
    setup_en = Tutorial(
        "Mod Setup and Use Guide",
        "A guide to setting up the Crystal Project Archipelago Mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["dragons but also rabbits"]
    )

    tutorials = [setup_en]
    option_groups = create_option_groups()
    options_presets = crystal_project_options_presets

class CrystalProjectWorld(World):
    """Crystal Project is a mix of old school job based jRPG mixed with a ton of 3D platforming and exploration."""
    game = "Crystal Project"
    options_dataclass = CrystalProjectOptions
    options: CrystalProjectOptions  # pyright: ignore [reportIncompatibleVariableOverride]
    topology_present = True  # show path to required location checks in spoiler

    # Add the home points to the item_table so they don't require any special code after this
    home_points = get_home_points()
    for home_point in home_points:
        item_table[home_point.name] = ItemData(HOME_POINT, home_point.code + home_point_item_index_offset, ItemClassification.progression)

    init_ap_region_to_display_region_dictionary()

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = get_location_name_to_id()

    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    base_game_jobs: set[str] = item_name_groups[JOB].copy()

    mod_info = get_mod_info()
    modded_items = get_modded_items(mod_info)
    modded_job_count: int = 0

    for modded_item in modded_items:
        if modded_item.name in item_name_to_id and item_name_to_id[modded_item.name] != modded_item.code:
            raise Exception(f"A modded item({modded_item.name}) with id {modded_item.code} tried to change the code of item_name_to_id and it can never change!")
        item_name_to_id[modded_item.name] = modded_item.code  # pyright: ignore [reportArgumentType]
        if 'Job' in modded_item.name:
            item_name_groups.setdefault(JOB, set()).add(modded_item.name)
            modded_job_count += 1
        else:
            item_name_groups.setdefault(MOD, set()).add(modded_item.name)

    modded_locations = get_modded_locations(mod_info)

    for modded_location in modded_locations:
        location_name_to_id[modded_location.name] = modded_location.code

    modded_shops = get_modded_shopsanity_locations(mod_info)

    for modded_shop in modded_shops:
        location_name_to_id[modded_shop.name] = modded_shop.code

    modded_bosses = get_modded_bosses(mod_info)

    for modded_boss in modded_bosses:
        location_name_to_id[modded_boss.name] = modded_boss.code

    modded_home_points = get_modded_home_points(mod_info)

    for modded_home_point in modded_home_points:
        location_name_to_id[modded_home_point.name] = modded_home_point.code + home_point_location_index_offset
        if modded_home_point.name in item_name_to_id and item_name_to_id[modded_home_point.name] != modded_home_point.code:
            raise Exception(f"A modded item({modded_home_point.name}) with id {modded_home_point.code} tried to change the code of item_name_to_id and it can never change!")
        item_name_to_id[modded_home_point.name] = modded_home_point.code + home_point_item_index_offset
        item_name_groups.setdefault(MOD, set()).add(modded_home_point.name)

    removed_locations = get_removed_locations(mod_info)
    removed_home_points = get_removed_home_points(mod_info)

    web = CrystalProjectWeb()

    # This is how we tell the Universal Tracker we want to use re_gen_passthrough
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    # and this is how we tell Universal Tracker we don't need the yaml
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.starter_ap_region: str = ""
        self.starting_jobs: List[str] = []
        self.jobs_not_to_exclude: List[str] = []
        self.included_regions: List[str] = []
        self.statically_placed_jobs: int = 0

    def generate_early(self):
        # implement .yaml-less Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Crystal Project" in self.multiworld.re_gen_passthrough:  # pyright: ignore [reportAttributeAccessIssue]
                    slot_data = self.multiworld.re_gen_passthrough["Crystal Project"]  # pyright: ignore [reportAttributeAccessIssue]
                    self.options.goal.value = slot_data["goal"]
                    self.options.clamshell_goal_quantity.value = slot_data["clamshellGoalQuantity"]
                    self.options.extra_clamshells_in_pool.value = slot_data["extraClamshellsInPool"]
                    self.options.astley_job_quantity.value = slot_data["jobGoalAmount"]
                    self.options.job_rando.value = slot_data["jobRando"]
                    self.starting_jobs = slot_data["startingJobsForUT"]
                    self.options.starting_job_quantity.value = slot_data["startingJobQuantity"]
                    self.options.kill_bosses_mode.value = slot_data["killBossesMode"]
                    self.options.shopsanity.value = slot_data["shopsanity"]
                    self.options.regionsanity.value = slot_data["regionsanity"]
                    self.starter_ap_region = slot_data["starterRegion"]
                    self.options.included_regions.value = slot_data["includedRegionsOption"]
                    self.options.progressive_mount_mode.value = slot_data["progressiveMountMode"]
                    self.options.starting_level.value = slot_data["startingLevel"]
                    self.options.level_gating.value = slot_data["levelGating"]
                    self.options.level_compared_to_enemies.value = slot_data["levelComparedToEnemies"]
                    self.options.progressive_level_size.value = slot_data["progressiveLevelSize"]
                    self.options.max_level.value = slot_data["maxLevel"]
                    self.options.key_mode.value = slot_data["keyMode"]
                    self.options.obscure_routes.value = slot_data["obscureRoutes"]
                    self.options.hop_to_it.value = slot_data["hopToIt"]
                    self.options.include_summon_abilities.value = slot_data["includeSummonAbilities"]
                    self.options.include_scholar_abilities.value = slot_data["includeScholarAbilities"]
                    self.options.use_mods.value = slot_data["useMods"]
                    # self.modded_locations = slot_data["moddedLocationsForUT"]
                    # self.modded_shops = slot_data["moddedShopsForUT"]

        if self.options.prioritize_crystals.value == self.options.prioritize_crystals.option_true:
            self.options.priority_locations.value = self.options.priority_locations.value.union(get_location_names_per_category()["Crystals"])

        self.multiworld.push_precollected(self.create_item(HOME_POINT_STONE))
        self.multiworld.push_precollected(self.create_item(ARCHIPELAGO_STONE))

        # Checks if starting jobs is empty and if so fills it.  If this is UT re-gen it won't be empty
        if not self.starting_jobs:
            self.starting_jobs = get_starting_jobs(self)
        for job in self.starting_jobs:
            self.multiworld.push_precollected(self.create_item(job))

        if self.options.start_with_treasure_finder.value:
            self.multiworld.push_precollected(self.create_item(TREASURE_FINDER))

        if self.options.start_with_maps.value == self.options.start_with_maps.option_true:
            for map_name in self.item_name_groups[MAP]:
                self.multiworld.push_precollected(self.create_item(map_name))

    def create_regions(self) -> None:
        locations = get_treasure_and_npc_locations(self.player, self.options)
        locations.extend(get_crystal_locations(self.player, self.options))

        if self.options.kill_bosses_mode.value == self.options.kill_bosses_mode.option_true:
            bosses = get_boss_locations(self.player, self.options)
            locations.extend(bosses)
        else:
            #Can't just do "for location in locations" because when a location is removed, then the number of things inside the list changes, and the code will skip the next location
            i = 0
            while i < len(locations):
                location = locations[i]
                if location.tags is not None:
                    if BOSS_LOCATION_GROUP in location.tags:
                        locations.remove(location)
                        i -= 1
                i += 1

        if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
            shops = get_shop_locations(self.player, self.options)
            locations.extend(shops)

        if self.options.use_mods.value == self.options.use_mods.option_true:
            for modded_location in self.modded_locations:
                location = LocationData(display_region_subregions_dictionary[modded_location.display_region][0],
                                        modded_location.name,
                                        modded_location.code,
                                        build_condition_rule(modded_location.display_region, modded_location.rule_condition, self))
                locations.append(location)

        if self.options.use_mods.value == self.options.use_mods.option_true and self.options.shopsanity.value != self.options.shopsanity.option_disabled:
            for shop in self.modded_shops:
                location = LocationData(display_region_subregions_dictionary[shop.display_region][0],
                                        shop.name,
                                        shop.code,
                                        build_condition_rule(shop.display_region, shop.rule_condition, self))
                locations.append(location)

        if self.options.use_mods.value == self.options.use_mods.option_true and self.options.kill_bosses_mode.value == self.options.kill_bosses_mode.option_true:
            for modded_location in self.modded_bosses:
                location = LocationData(display_region_subregions_dictionary[modded_location.display_region][0],
                                        modded_location.name,
                                        modded_location.code,
                                        build_condition_rule(modded_location.display_region, modded_location.rule_condition, self))
                locations.append(location)

        if self.options.use_mods.value == self.options.use_mods.option_true:
            for removed_location in self.removed_locations:
                for location in locations:
                    if location.name == removed_location.name:
                        locations.remove(location)

        if self.options.home_point_hustle.value != self.options.home_point_hustle.option_disabled:
            home_points = get_home_points()
            removed_code_list = [home_point.code for home_point in self.removed_home_points]

            for home_point in home_points:
                should_add = True
                if self.options.use_mods.value == self.options.use_mods.option_true:
                    should_add = home_point.code not in removed_code_list

                if should_add:
                    home_point_location = LocationData(home_point.ap_region, home_point.name, (home_point.code + home_point_location_index_offset), home_point.rule)
                    locations.append(home_point_location)

            if self.options.use_mods.value == self.options.use_mods.option_true:
                for modded_home_point in self.modded_home_points:
                    location = LocationData(display_region_subregions_dictionary[modded_home_point.display_region][0],
                                            modded_home_point.name,
                                            modded_home_point.code + home_point_location_index_offset,
                                            build_condition_rule(modded_home_point.display_region,
                                                                 modded_home_point.rule_condition, self))
                    locations.append(location)

        #Regionsanity completion locations need to be added after all other locations so they can be removed if the region is empty (e.g. Neptune Shrine w/o Shopsanity)
        if self.options.regionsanity.value != self.options.regionsanity.option_disabled:
            region_completions = get_region_completion_locations()
            for completion in region_completions:
                display_region_empty = True
                for location in locations:
                    if ap_region_to_display_region_dictionary[completion.ap_region] == ap_region_to_display_region_dictionary[location.ap_region]:
                        display_region_empty = False
                        break
                if display_region_empty:
                    region_completions.remove(completion)
            locations.extend(region_completions)

        init_areas(self, locations, self.options)

        if self.options.job_rando.value == self.options.job_rando.option_none:
            jobs_earnable, self.jobs_not_to_exclude = set_jobs_at_default_locations(self, self.player_name)
            if self.options.use_mods.value == self.options.use_mods.option_true:
                jobs_earnable += self.modded_job_count
        else:
            jobs_earnable = len(self.item_name_groups[JOB]) - len(self.starting_jobs)
            if self.options.use_mods.value == self.options.use_mods.option_false:
                jobs_earnable -= self.modded_job_count

        if (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and self.options.astley_job_quantity.value > jobs_earnable:
            message = "For player {2}: newWorldStoneJobQuantity was set to {0} but your options only had {1} jobs in pool. Reduced newWorldStoneJobQuantity to {1}."
            logging.getLogger().info(message.format(self.options.astley_job_quantity.value, jobs_earnable, self.player_name))
            self.options.astley_job_quantity.value = jobs_earnable

        if self.options.regionsanity.value == self.options.regionsanity.option_disabled:
            self.starter_ap_region = SPAWNING_MEADOWS_AP_REGION
        # pick one display region to give a starting pass to and then save that later
        else:
            starting_passes_list: List[str] = []
            #checking the start inventory for region passes and using the first one to set the starter region, if any
            for item_name in self.options.start_inventory.keys():
                if item_name in self.item_name_groups[PASS]:
                    is_inv_pass_for_included_region: bool = False
                    for display_region in self.included_regions:
                        is_inv_pass_for_included_region = False
                        if (display_region != MENU_DISPLAY_NAME and display_region != MODDED_ZONE_DISPLAY_NAME
                                and display_region_name_to_pass_dict[display_region] == item_name):
                                is_inv_pass_for_included_region = True
                                starting_passes_list.append(item_name)
                                break
                    if not is_inv_pass_for_included_region:
                        raise Exception(f"For player {self.player_name}: YAML settings were contradictory. Starting inventory contains {item_name}, "
                                        f"but that region is not in {self.options.included_regions}. Change settings and regenerate.")

            for item_name in self.options.start_inventory_from_pool.keys():
                if item_name in self.item_name_groups[PASS]:
                    is_inv_pool_pass_for_included_region: bool = False
                    for display_region in self.included_regions:
                        is_inv_pool_pass_for_included_region = False
                        if (display_region != MENU_DISPLAY_NAME and display_region != MODDED_ZONE_DISPLAY_NAME
                                and display_region_name_to_pass_dict[display_region] == item_name):
                            is_inv_pool_pass_for_included_region = True
                            starting_passes_list.append(item_name)
                            break
                    if not is_inv_pool_pass_for_included_region:
                        raise Exception(f"For player {self.player_name}: YAML settings were contradictory. Starting inventory from pool contains {item_name}, "
                                        f"but that region is not in {self.options.included_regions}. Change settings and regenerate.")

            if len(starting_passes_list) > 0:
                for display_region_name in display_region_name_to_pass_dict:
                    if display_region_name_to_pass_dict[display_region_name] == starting_passes_list[0]:
                        # The first subregion (AP Region) in a display region will be the starter region if a player puts that display region's pass in their starting inventory
                        self.starter_ap_region = display_region_subregions_dictionary[display_region_name][0]
                        break

            display_regions_desperate_for_a_salmon: list[str] = [THE_OPEN_SEA_DISPLAY_NAME, THE_DEEP_SEA_DISPLAY_NAME, THE_DEPTHS_DISPLAY_NAME]

            # If this is UT re-gen the value isn't empty and we skip trying to pick a starter_region since we already have one
            if self.starter_ap_region == "":
                valid_starting_regions = []
                display_regions_forbidden_from_being_starters: list[str] = [MENU_DISPLAY_NAME, THE_OLD_WORLD_DISPLAY_NAME, MODDED_ZONE_DISPLAY_NAME]
                actual_starting_level_value = self.options.starting_level.value

                if self.options.regionsanity_starter_region_max_level.value < self.options.regionsanity_starter_region_min_level.value:
                    raise Exception(f"For player {self.player_name}: YAML settings were contradictory. Regionsanity Starter Level Min Value {self.options.regionsanity_starter_region_min_level.value} "
                                    f"is higher than Regionsanity Starter Level Max Value {self.options.regionsanity_starter_region_max_level.value}. Change settings and regenerate.")

                for ap_region in self.get_regions():
                    #ap regions are only valid starter regions if they are the first ap region inside the display region (for now)
                    if (len(ap_region.locations) >= 2 and ap_region.name not in display_regions_forbidden_from_being_starters
                            and display_region_subregions_dictionary[ap_region_to_display_region_dictionary[ap_region.name]][0] == ap_region.name
                            and self.options.regionsanity_starter_region_min_level.value <= display_region_levels_dictionary[ap_region_to_display_region_dictionary[ap_region.name]][0] <= self.options.regionsanity_starter_region_max_level.value):
                        reachable_locations_in_region: int = 0
                        #Getting the state into the right place: match the starter region to the currently selected region, give the pass for that region, and give the levels if necessary
                        current_state: CollectionState = CollectionState(self.multiworld)
                        self.origin_region_name = ap_region.name
                        current_state.collect(self.create_item(display_region_name_to_pass_dict[ap_region_to_display_region_dictionary[ap_region.name]]), prevent_sweep=True)

                        if ap_region_to_display_region_dictionary[ap_region.name] in display_regions_desperate_for_a_salmon:
                            current_state.collect(self.create_item(PROGRESSIVE_SALMON_VIOLA), prevent_sweep=True)

                        if not self.options.level_gating.value == self.options.level_gating.option_none:
                            #Temporarily changing starting level value to what it would be if this AP Region were picked, so we know what locations are actually available for the player in that situation
                            self.options.starting_level.value = max(actual_starting_level_value, display_region_levels_dictionary[ap_region_to_display_region_dictionary[ap_region.name]][0] + self.options.level_compared_to_enemies.value)

                        #Checking all locations in current AP Region and the other AP Regions inside the same Display Region
                        for ap_region_name_in_same_display_region in display_region_subregions_dictionary[ap_region_to_display_region_dictionary[ap_region.name]]:
                            ap_region_in_same_display_region = self.get_region(ap_region_name_in_same_display_region)

                            for possible_reachable_location in ap_region_in_same_display_region.locations:
                                if current_state.can_reach(possible_reachable_location):
                                    reachable_locations_in_region += 1

                        if reachable_locations_in_region >= 2:
                            valid_starting_regions.append(ap_region)
                            #logging.getLogger().info(ap_region.name + " is a valid starter region.")

                #Returning starting level to the player's setting
                self.options.starting_level.value = actual_starting_level_value

                if len(valid_starting_regions) == 0:
                    raise Exception(f"For player {self.player_name}: YAML settings were too restrictive. No valid regions are between Regionsanity Starter Level Min Value {self.options.regionsanity_starter_region_min_level.value} "
                                    f"and Regionsanity Starter Level Max Value {self.options.regionsanity_starter_region_max_level.value}. Change settings and regenerate.")

                self.starter_ap_region = self.random.choice(valid_starting_regions).name
                #Until we have a teleport location in every single ap region, for now we take specifically the first ap region in the display regions subregion list
                self.starter_ap_region = display_region_subregions_dictionary[ap_region_to_display_region_dictionary[self.starter_ap_region]][0]

            #only push if player doesn't already have the pass from their starting inventory
            if len(starting_passes_list) == 0:
                #Converts the AP Region that was picked as the starting region to the Display Region containing that AP Region
                self.multiworld.push_precollected(self.create_item(display_region_name_to_pass_dict[ap_region_to_display_region_dictionary[self.starter_ap_region]]))

            #Giving players who start in a swimming-required region a salmon to start
            if self.starter_ap_region in display_regions_desperate_for_a_salmon:
                self.multiworld.push_precollected(self.create_item(PROGRESSIVE_SALMON_VIOLA))
            #Decided it would be cute to start players in the Salmon Room with the Salmon Violin in its chest for The Deep Sea
            if self.starter_ap_region == THE_DEEP_SEA_AP_REGION:
                self.multiworld.push_precollected(self.create_item(JIDAMBA_EACLANEYA_PASS))
                self.get_location(JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Claim the prize of the Timer Fishes").place_locked_item(self.create_item(PROGRESSIVE_SALMON_VIOLA))

        self.origin_region_name = self.starter_ap_region
        logging.getLogger().info("Starting region for " + self.player_name + " is " + ap_region_to_display_region_dictionary[self.starter_ap_region])

        # now that we know your starter region, we know your starting level and how many progressive levels you need to start with
        starter_region_level = display_region_levels_dictionary[ap_region_to_display_region_dictionary[self.starter_ap_region]][0]
        #We take whichever is greater: the player's Starting Level option number or the starter region's level
        self.options.starting_level.value = max(self.options.starting_level.value, starter_region_level + self.options.level_compared_to_enemies.value)
        if self.options.starting_level.value < 3:
            self.options.starting_level.value = 3
        if self.options.starting_level.value > self.options.max_level.value:
            self.options.starting_level.value = self.options.max_level.value
        message = "Starting level for {0} is {1}."
        logging.getLogger().info(message.format(self.player_name, self.options.starting_level.value))

    def create_item(self, name: str) -> Item:
        if name in item_table:
            data = item_table[name]
            return Item(name, data.classification, data.code, self.player)
        else:
            matches_mod = [item for (index, item) in enumerate(self.modded_items) if item.name == name]
            matches_mod_home_point = [item for (index, item) in enumerate(self.modded_home_points) if item.name == name]

            if len(matches_mod) > 0:
                return Item(matches_mod[0].name, matches_mod[0].classification, matches_mod[0].code, self.player)
            elif len(matches_mod_home_point) > 0:
                return Item(matches_mod_home_point[0].name, ItemClassification.progression, matches_mod_home_point[0].code + home_point_item_index_offset, self.player)
            else:
                raise Exception(f"No matches found for name {name}")

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

    NON_CLAM_GOAL_CLAMSHELLS_GOAL = 2
    NON_CLAM_GOAL_CLAMSHELLS_TOTAL = 3

    def get_goal_clamshells(self) -> int:
        goal_clamshell_quantity = self.NON_CLAM_GOAL_CLAMSHELLS_GOAL
        if self.options.goal.value == self.options.goal.option_clamshells:
            goal_clamshell_quantity = self.options.clamshell_goal_quantity.value
        return goal_clamshell_quantity

    def get_extra_clamshells(self) -> int:
        extra_clamshells = self.NON_CLAM_GOAL_CLAMSHELLS_TOTAL
        if self.options.goal.value == self.options.goal.option_clamshells:
            extra_clamshells = self.options.extra_clamshells_in_pool.value
        return extra_clamshells

    def get_total_clamshells(self, max_clamshells: int) -> int:
        total_clamshell_quantity = self.NON_CLAM_GOAL_CLAMSHELLS_TOTAL
        if self.options.goal.value == self.options.goal.option_clamshells:
            total_clamshell_quantity = self.options.clamshell_goal_quantity.value + self.options.extra_clamshells_in_pool.value
            # If the player's options ask to put more clamshells in the pool than there is room, reduce their options proportionally so they fit
            if total_clamshell_quantity > max_clamshells:
                percent_goal_clamshells = self.options.clamshell_goal_quantity.value / total_clamshell_quantity
                self.options.clamshell_goal_quantity.value = int(percent_goal_clamshells * max_clamshells)
                if self.options.clamshell_goal_quantity.value < self.options.clamshell_goal_quantity.range_start:
                    self.options.clamshell_goal_quantity.value = self.options.clamshell_goal_quantity.range_start
                self.options.extra_clamshells_in_pool.value = int(max_clamshells - self.options.clamshell_goal_quantity.value)
                if self.options.extra_clamshells_in_pool.value < self.options.extra_clamshells_in_pool.range_start:
                    self.options.extra_clamshells_in_pool.value = self.options.extra_clamshells_in_pool.range_start

                # Log the change to player settings
                message = ("For player {2}: total_clamshells was {0} but there was only room for {1} clamshells in the pool. "
                           "Reduced clamshellGoalQuantity to {3} and extraClamshellsInPool to {4}.")
                logging.getLogger().info(message.format(total_clamshell_quantity, max_clamshells, self.player_name,
                                                        self.options.clamshell_goal_quantity.value, self.options.extra_clamshells_in_pool.value))

                total_clamshell_quantity = self.options.clamshell_goal_quantity.value + self.options.extra_clamshells_in_pool.value
        return total_clamshell_quantity

    def get_total_progressive_levels(self, max_progressive_levels: int) -> int:
        if max_progressive_levels < 1:
            max_progressive_levels = 1

        level_up_amount = self.options.max_level.value - self.options.starting_level.value

        # this formula is how we can do ceiling division in Python
        progressive_levels = -(level_up_amount // -self.options.progressive_level_size.value)
        #don't forget to -1
        if progressive_levels > max_progressive_levels:
            potential_progressive_level_size = -(level_up_amount // -max_progressive_levels)
            potential_max_level = self.options.max_level.value

            if potential_progressive_level_size > self.options.progressive_level_size.range_end:
                potential_progressive_level_size = self.options.progressive_level_size.range_end
                potential_max_level = max_progressive_levels * potential_progressive_level_size

            if self.options.max_level.value > potential_max_level:
                raise Exception(f"For player {self.player_name}: yaml settings were too restrictive. Needed at least {-(level_up_amount // -potential_progressive_level_size)} Progressive Levels, but only room for {max_progressive_levels} Progressive Levels in the pool. "
                                f"This is usually caused by mods that add more items than locations. Change settings and regenerate.")
            else:
                message = (f"For player {self.player_name}: yaml settings were too restrictive. Only room for {max_progressive_levels} Progressive Levels in the pool. "
                           f"Increased progressive_level_size to {potential_progressive_level_size}.")
                logging.getLogger().info(message)

                self.options.progressive_level_size.value = potential_progressive_level_size

        progressive_levels = -(level_up_amount // -self.options.progressive_level_size.value)
        return progressive_levels

    @staticmethod
    def get_total_passive_point_boosts(max_passive_point_cap: int, starting_passive_point_cap: int, cap_increase: int) -> int:
        return round((max_passive_point_cap - starting_passive_point_cap) / cap_increase)

    #making randomized scholar ability pool
    def get_optional_scholar_abilities(self, count: int):
        return self.random.sample(optional_scholar_abilities, count)

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.options.trap_likelihood.value

        if trap_chance > 0 and self.random.random() < (trap_chance / 100):
             return self.random.choice(list(self.item_name_groups[TRAP]))
        else:
            return self.random.choice(filler_items)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(HOME_POINT_STONE)
        excluded_items.add(ARCHIPELAGO_STONE)

        for job in self.starting_jobs:
            excluded_items.add(job)

        if self.options.progressive_mount_mode.value == self.options.progressive_mount_mode.option_true:
            for mount in self.item_name_groups[MOUNT]:
               if mount != PROGRESSIVE_MOUNT:
                   excluded_items.add(mount)
        else:
            excluded_items.add(PROGRESSIVE_MOUNT)

        if self.options.level_gating.value == self.options.level_gating.option_none:
            excluded_items.add(PROGRESSIVE_LEVEL)

        if self.options.start_with_treasure_finder.value == self.options.start_with_treasure_finder.option_true:
            excluded_items.add(TREASURE_FINDER)

        if self.options.start_with_maps.value == self.options.start_with_maps.option_true:
            for map_name in self.item_name_groups[MAP]:
                excluded_items.add(map_name)

        if self.options.goal.value == self.options.goal.option_true_astley:
            excluded_items.add(OLD_WORLD_STONE)

        if self.options.include_summon_abilities.value == self.options.include_summon_abilities.option_false:
            for summon in self.item_name_groups[SUMMON]:
                excluded_items.add(summon)

        if self.options.include_scholar_abilities.value == self.options.include_scholar_abilities.option_false:
            for scholar_ability in self.item_name_groups[SCHOLAR_ABILITY]:
                excluded_items.add(scholar_ability)

        #Progressive Equipment Mode
        if self.options.progressive_equipment_mode.value == self.options.progressive_equipment_mode.option_false:
            for progressive_equipment_piece in progressive_equipment:
                excluded_items.add(progressive_equipment_piece)
        else:
            for equipment_piece in non_progressive_equipment:
                excluded_items.add(equipment_piece)

        #For non-keyring modes
        if (self.options.key_mode.value != self.options.key_mode.option_key_ring and
            self.options.key_mode.value != self.options.key_mode.option_key_ring_skelefree):
            for keyring in key_rings:
                excluded_items.add(keyring)

        #For non-vanilla key modes
        if (self.options.key_mode.value != self.options.key_mode.option_vanilla and
            self.options.key_mode.value != self.options.key_mode.option_vanilla_skelefree):
            for key in dungeon_keys:
                excluded_items.add(key)

        #For skeleton key mode
        if self.options.key_mode.value == self.options.key_mode.option_skeleton:
            for key in singleton_keys:
                excluded_items.add(key)

        if (self.options.key_mode.value == self.options.key_mode.option_vanilla_skelefree or
            self.options.key_mode.value == self.options.key_mode.option_key_ring_skelefree):
            excluded_items.add(SKELETON_KEY)

        if self.options.job_rando.value == self.options.job_rando.option_none:
            # Summoner job needs to be available if kill bosses mode is on.
            #   If job rando is off and regions are beginner or advanced, then the summoner crystal would be missing.  Do not exclude in this context.
            if (SUMMONER_JOB not in self.jobs_not_to_exclude and
                    ((self.options.included_regions.value == self.options.included_regions.option_beginner or
                    self.options.included_regions.value == self.options.included_regions.option_advanced) and
                    self.options.kill_bosses_mode.value == self.options.kill_bosses_mode.option_true)):
                self.jobs_not_to_exclude.append(SUMMONER_JOB)

            job_crystal_dictionary: Dict[str, str] = job_crystal_beginner_dictionary.copy()
            job_crystal_dictionary.update(job_crystal_advanced_dictionary)
            job_crystal_dictionary.update(job_crystal_expert_dictionary)

            for job_name in job_crystal_dictionary.keys():
                if job_name not in self.jobs_not_to_exclude:
                    excluded_items.add(job_name)

        #regionsanity items
        if self.options.regionsanity.value == self.options.regionsanity.option_disabled:
            for region_pass in self.item_name_groups[PASS]:
                excluded_items.add(region_pass)
        else:
            excluded_items.add(display_region_name_to_pass_dict[ap_region_to_display_region_dictionary[self.starter_ap_region]])

        if self.options.home_point_hustle.value == self.options.home_point_hustle.option_disabled:
            for home_point_item in self.item_name_groups[HOME_POINT]:
                excluded_items.add(home_point_item)
        else:
            all_home_point_locations = get_home_points()

            for home_point_item in self.item_name_groups[HOME_POINT]:
                is_in_included_region: bool = False
                for location in all_home_point_locations:
                    if home_point_item == location.name:
                        if ap_region_to_display_region_dictionary[location.ap_region] in self.included_regions:
                            is_in_included_region = True
                            break
                        elif (ap_region_to_display_region_dictionary[location.ap_region] == THE_NEW_WORLD_DISPLAY_NAME
                              and (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley)):
                            is_in_included_region = True
                            break
                if not is_in_included_region:
                    excluded_items.add(home_point_item)

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                #Check region type and add the region-type amounts; then check Shopsanity and add the shop amounts
                amount:int = int(data.beginnerAmount or 0)
                if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                    amount = amount + int(data.beginnerShops or 0)
                if self.options.included_regions == self.options.included_regions.option_advanced:
                    amount = amount + int(data.advancedAmount or 0)
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.advancedShops or 0)
                elif self.options.included_regions == self.options.included_regions.option_expert:
                    amount = amount + int(data.advancedAmount or 0) + int(data.expertAmount or 0)
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.expertShops or 0)
                elif self.options.included_regions == self.options.included_regions.option_all:
                    amount = amount + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)
                    #atm there are no end-game specific shopsanity items
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.endGameShops or 0)

                # Make sure new world pass is included if regionsanity is on and its required for the goal
                if (self.options.regionsanity.value != self.options.regionsanity.option_disabled and
                        (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and
                        name == THE_NEW_WORLD_PASS):
                    amount = int(data.beginnerAmount or 0) + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)
                # Same goes for old world pass, the depths pass, the deep sea pass, and the open sea pass (so you can get to Gabriel)
                elif (self.options.regionsanity.value != self.options.regionsanity.option_disabled and
                        self.options.goal.value == self.options.goal.option_true_astley and
                        (name == THE_OLD_WORLD_PASS or name == THE_DEPTHS_PASS or name == THE_DEEP_SEA_PASS or name == THE_OPEN_SEA_PASS)):
                    amount = int(data.beginnerAmount or 0) + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)
                # adds Astley goal required item if it doesn't already exist (aka the map!)
                if self.options.goal.value == self.options.goal.option_astley and name == THE_NEW_WORLD_MAP:
                    amount = int(data.beginnerAmount or 0) + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)
                # adds true Astley goal required items if they don't already exist (including maps!)
                if self.options.goal.value == self.options.goal.option_true_astley and (name == STEM_WARD or name == DEITY_EYE or name == THE_OLD_WORLD_MAP or name == THE_NEW_WORLD_MAP):
                    amount = int(data.beginnerAmount or 0) + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)

                for _ in range(amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        #7 spells randomly chosen from the entire pool (they have Reverse Polarity as default to merc Gran)
        if self.options.included_regions == self.options.included_regions.option_beginner:
            for scholar_ability in self.get_optional_scholar_abilities(7):
                item = self.create_item(scholar_ability)
                pool.append(item)

        #for any Astley goal, make sure new world stone is in the pool
        if self.options.goal.value != self.options.goal.option_clamshells:
            item = self.set_classifications(NEW_WORLD_STONE)
            if item not in pool:
                pool.append(item)

        if self.options.maximum_passive_points > self.options.starting_passive_points:
            passive_point_boosts_to_add_to_pool = self.get_total_passive_point_boosts(self.options.maximum_passive_points.value, self.options.starting_passive_points.value, self.options.passive_point_boost_size.value)
            if passive_point_boosts_to_add_to_pool > 0:
                for _ in range(passive_point_boosts_to_add_to_pool):
                    item = self.set_classifications(PASSIVE_POINT_BOOST)
                    pool.append(item)

        if self.options.use_mods:
            combined_locations: List[ModLocationData] = self.modded_locations.copy()
            combined_locations.extend(self.modded_shops)

            for modded_item in self.modded_items:
                update_item_classification(modded_item, [location.rule_condition for location in combined_locations], self)
                item = self.create_item(modded_item.name)
                pool.append(item)

            if self.options.home_point_hustle != self.options.home_point_hustle.option_disabled:
                for modded_home_point in self.modded_home_points:
                    item = self.create_item(modded_home_point.name)
                    update_item_classification(item, [location.rule_condition for location in combined_locations], self)
                    pool.append(item)

        if not self.options.level_gating.value == self.options.level_gating.option_none:
            #guarantee space for 2 clamshells
            min_clamshells = 2
            #any starting progressive levels you have increase the number of max progressive levels you could have
            max_progressive_levels: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - min_clamshells
            #players start with zero or more
            progressive_levels_to_add_to_pool = self.get_total_progressive_levels(max_progressive_levels)
            if progressive_levels_to_add_to_pool > 0:
                for _ in range (progressive_levels_to_add_to_pool):
                    item = self.set_classifications(PROGRESSIVE_LEVEL)
                    pool.append(item)

        max_clamshells: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        for _ in range(self.get_total_clamshells(max_clamshells)):
            item = self.set_classifications(CLAMSHELL)
            pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

        return pool

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        return item

    def set_rules(self) -> None:
        logic = CrystalProjectLogic(self.player, self.options)
        if self.options.goal == self.options.goal.option_astley:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(THE_NEW_WORLD_AP_REGION, player=self.player) and logic.has_jobs(state, self.options.astley_job_quantity.value)
            if THE_NEW_WORLD_DISPLAY_NAME not in self.included_regions:
                self.included_regions.append(THE_NEW_WORLD_DISPLAY_NAME)
        elif self.options.goal == self.options.goal.option_true_astley:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(THE_OLD_WORLD_AP_REGION, player=self.player) and state.can_reach(THE_NEW_WORLD_AP_REGION, player=self.player)
            if THE_OLD_WORLD_DISPLAY_NAME not in self.included_regions:
                self.included_regions.append(THE_OLD_WORLD_DISPLAY_NAME)
        elif self.options.goal == self.options.goal.option_clamshells:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(CLAMSHELL, self.player, self.options.clamshell_goal_quantity.value) and state.can_reach(SEASIDE_CLIFFS_AP_REGION, player=self.player)

    def get_job_id_list(self) -> List[int]:
        job_ids: List[int] = []
        for job in self.starting_jobs:
            job_ids.append(self.item_name_to_id[job])

        return job_ids

    # This is data that needs to be readable from within the modded version of the game.
    # Example job rando makes the crystals behave differently, so the game needs to know about it.
    def fill_slot_data(self) -> Dict[str, Any]:
        mod_info = []
        slot_data_locations = []
        slot_data_home_points = []
        slot_data_removed_locations = []
        slot_data_removed_home_points = []

        if self.options.use_mods:
            for mod in self.mod_info:
                mod_info.append({ "Id": mod.mod_id, "Name": mod.mod_name, "LoadOrder": mod.load_order })

            for modded_location in self.modded_locations:
                slot_data_locations.append({"Id": modded_location.offsetless_code,
                                            "APRegion": display_region_subregions_dictionary[modded_location.display_region][0],
                                            "Name": modded_location.name,
                                            "Coordinates": modded_location.coordinates,
                                            "biomeId": modded_location.biomeId,
                                            "Rule": None })
            if self.options.shopsanity != self.options.shopsanity.option_disabled:
                for shop in self.modded_shops:
                    slot_data_locations.append({ "Id": shop.offsetless_code,
                                                 "APRegion": display_region_subregions_dictionary[shop.display_region][0],
                                                 "Name": shop.name,
                                                 "Coordinates": shop.coordinates,
                                                 "BiomeId": shop.biomeId,
                                                 "Rule": None })

            if self.options.kill_bosses_mode == self.options.kill_bosses_mode.option_true:
                for boss in self.modded_bosses:
                    slot_data_locations.append({ "Id": boss.offsetless_code,
                                                 "APRegion": display_region_subregions_dictionary[boss.display_region][0],
                                                 "Name": boss.name,
                                                 "Coordinates": boss.coordinates,
                                                 "BiomeId": boss.biomeId,
                                                 "Rule": None })

            if self.options.home_point_hustle != self.options.home_point_hustle.option_disabled:
                for home_point in self.modded_home_points:
                    slot_data_home_points.append({ "Id": home_point.offsetless_code,
                                                 "APRegion": display_region_subregions_dictionary[home_point.display_region][0],
                                                 "Name": home_point.name,
                                                 "Coordinates": home_point.coordinates,
                                                 "BiomeId": home_point.biomeId,
                                                 "Rule": None })

            for location in self.removed_locations:
                slot_data_removed_locations.append({"Id": location.code,
                                            "APRegion": location.ap_region})

            for home_point in self.removed_home_points:
                slot_data_removed_home_points.append({"Id": home_point.code,
                                            "APRegion": location.ap_region})

            #TODO removed home points

        # look into replacing this big chonky return block with self.options.as_dict() and then just adding the extras to the dict after
        return {
            "apworldVersion": self.world_version.as_simple_string(),
            "goal": self.options.goal.value,
            "clamshellGoalQuantity": self.get_goal_clamshells(),
            "extraClamshellsInPool": self.get_extra_clamshells(),
            "jobGoalAmount": self.options.astley_job_quantity.value,
            "jobRando": self.options.job_rando.value,
            "startingJobsForUT": self.starting_jobs,
            "startingJobQuantity": self.options.starting_job_quantity.value,
            "randomizeStartingJobs": bool(self.options.job_rando.value == self.options.job_rando.option_full),
            "startingJobs": self.get_job_id_list(),
            "killBossesMode" : bool(self.options.kill_bosses_mode.value),
            "shopsanity": self.options.shopsanity.value,
            "regionsanity": self.options.regionsanity.value,
            "starterRegion": self.starter_ap_region,
            "includedRegions": self.included_regions,
            "includedRegionsOption": self.options.included_regions.value,
            "progressiveMountMode": self.options.progressive_mount_mode.value,
            "startingLevel": self.options.starting_level.value,
            "levelGating": self.options.level_gating.value,
            "levelComparedToEnemies": self.options.level_compared_to_enemies.value,
            "progressiveLevelSize": self.options.progressive_level_size.value,
            "maxLevel": self.options.max_level.value,
            "keyMode": self.options.key_mode.value,
            "obscureRoutes": bool(self.options.obscure_routes.value),
            "hopToIt": self.options.hop_to_it.value,
            "autoSpendLP": bool(self.options.auto_spend_lp.value),
            "autoEquipPassives": bool(self.options.auto_equip_passives.value),
            "easyLeveling": bool(self.options.easy_leveling.value),
            "startWithMaps": bool(self.options.start_with_maps.value),
            "includeSummonAbilities": self.options.include_summon_abilities.value,
            "includeScholarAbilities": self.options.include_scholar_abilities.value,
            "itemInfoMode": self.options.item_info_mode.value,
            "randomizeMusic": bool(self.options.randomize_music.value),
            "useMods": self.options.use_mods.value,
            "modInfo": mod_info,
            "moddedLocations": slot_data_locations,
            "moddedHomePoints": slot_data_home_points,
            "removedLocations": slot_data_removed_locations,
            "removedHomePoints": slot_data_removed_home_points,
            # "moddedLocationsForUT": self.modded_locations,
            # "moddedShopsForUT": self.modded_shops,
            "prefillMap": bool(self.options.fill_full_map.value),
            "disableSparks": bool(self.options.disable_sparks.value),
            "homePointHustle": self.options.home_point_hustle.value,
            "maximumPassivePoints": self.options.maximum_passive_points.value,
            "startingPassivePoints": self.options.starting_passive_points.value,
            "passivePointBoostSize": self.options.passive_point_boost_size.value,
        }