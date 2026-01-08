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
from .constants.region_passes import *
from .items import item_table, optional_scholar_abilities, get_random_starting_jobs, filler_items, \
    get_item_names_per_category, progressive_equipment, non_progressive_equipment, get_starting_jobs, \
    set_jobs_at_default_locations, default_starting_job_list, key_rings, dungeon_keys, singleton_keys, \
    display_region_name_to_pass_dict, job_crystal_beginner_dictionary, job_crystal_advanced_dictionary, job_crystal_expert_dictionary
from .locations import get_treasure_and_npc_locations, get_boss_locations, get_shop_locations, get_region_completion_locations, LocationData, get_location_names_per_category, \
    get_location_name_to_id, get_crystal_locations
from .presets import crystal_project_options_presets
from .regions import init_ap_region_to_display_region_dictionary, init_areas, ap_region_to_display_region_dictionary, display_region_subregions_dictionary
from .options import CrystalProjectOptions, IncludedRegions, create_option_groups
from .rules import CrystalProjectLogic
from .mod_helper import ModLocationData, get_modded_items, get_modded_locations, \
    get_modded_shopsanity_locations, get_modded_bosses, build_condition_rule, update_item_classification, ModIncrementedIdData, get_mod_info, get_removed_locations
from typing import List, Set, Dict, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, MultiWorld, CollectionState

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
    options: CrystalProjectOptions
    topology_present = True  # show path to required location checks in spoiler

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
        item_name_to_id[modded_item.name] = modded_item.code
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

    removed_locations = get_removed_locations(mod_info)

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
        self.starting_progressive_levels: int = 1

    def generate_early(self):
        # implement .yaml-less Universal Tracker support
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Crystal Project" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Crystal Project"]
                    self.options.goal.value = slot_data["goal"]
                    self.options.clamshell_goal_quantity.value = slot_data["clamshellGoalQuantity"]
                    self.options.extra_clamshells_in_pool.value = slot_data["extraClamshellsInPool"]
                    self.options.new_world_stone_job_quantity.value = slot_data["jobGoalAmount"]
                    self.options.job_rando.value = slot_data["jobRando"]
                    self.starting_jobs = slot_data["startingJobsForUT"]
                    self.options.starting_job_quantity.value = slot_data["startingJobQuantity"]
                    self.options.kill_bosses_mode.value = slot_data["killBossesMode"]
                    self.options.shopsanity.value = slot_data["shopsanity"]
                    self.options.regionsanity.value = slot_data["regionsanity"]
                    self.options.included_regions.value = slot_data["includedRegionsOption"]
                    self.options.progressive_mount_mode.value = slot_data["progressiveMountMode"]
                    self.options.level_gating.value = slot_data["levelGating"]
                    self.options.level_compared_to_enemies.value = slot_data["levelComparedToEnemies"]
                    self.options.progressive_level_size.value = slot_data["progressiveLevelSize"]
                    self.options.max_level.value = slot_data["maxLevel"]
                    self.options.key_mode.value = slot_data["keyMode"]
                    self.options.obscure_routes.value = slot_data["obscureRoutes"]
                    self.options.include_summon_abilities.value = slot_data["includeSummonAbilities"]
                    self.options.include_scholar_abilities.value = slot_data["includeScholarAbilities"]
                    self.options.use_mods.value = slot_data["useMods"]
                    # self.modded_locations = slot_data["moddedLocationsForUT"]
                    # self.modded_shops = slot_data["moddedShopsForUT"]
                    self.starter_ap_region = slot_data["starterRegion"]
        
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

        if not self.options.level_gating.value == self.options.level_gating.option_none:
            #3 is Spawning Meadows' level
            starting_level_so_you_can_do_anything = 3 + self.options.level_compared_to_enemies.value
            if starting_level_so_you_can_do_anything < 3:
                starting_level_so_you_can_do_anything = 3
            elif starting_level_so_you_can_do_anything > self.options.max_level.value:
                starting_level_so_you_can_do_anything = self.options.max_level.value
            # Players start with at least 1 Progressive Level, but we add more if their Level Compared to Enemies setting is positive
            self.starting_progressive_levels = ((starting_level_so_you_can_do_anything - 1) // self.options.progressive_level_size.value) + 1
            for _ in range(self.starting_progressive_levels):
                self.multiworld.push_precollected(self.create_item(PROGRESSIVE_LEVEL))

    def create_regions(self) -> None:
        init_ap_region_to_display_region_dictionary()

        locations = get_treasure_and_npc_locations(self.player, self.options)
        locations.extend(get_crystal_locations(self.player, self.options))

        if self.options.kill_bosses_mode.value == self.options.kill_bosses_mode.option_true:
            bosses = get_boss_locations(self.player, self.options)
            locations.extend(bosses)

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

        #Regionsanity completion locations need to be added after all other locations so they can be removed if the region is empty (e.g. Neptune Shrine w/o Shopsanity)
        if self.options.regionsanity.value != self.options.regionsanity.option_disabled:
            region_completions = get_region_completion_locations(self.player, self.options)
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

        if (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and self.options.new_world_stone_job_quantity.value > jobs_earnable:
            message = "For player {2}: newWorldStoneJobQuantity was set to {0} but your options only had {1} jobs in pool. Reduced newWorldStoneJobQuantity to {1}."
            logging.getLogger().info(message.format(self.options.new_world_stone_job_quantity.value, jobs_earnable, self.player_name))
            self.options.new_world_stone_job_quantity.value = jobs_earnable

        # pick one display region to give a starting pass to and then save that later
        if self.options.regionsanity.value != self.options.regionsanity.option_disabled:
            starting_passes_list: List[str] = []
            #checking the start inventory for region passes and using the first one to set the starter region, if any
            for item_name in self.options.start_inventory.keys():
                if item_name in self.item_name_groups[PASS]:
                    starting_passes_list.append(item_name)
            for item_name in self.options.start_inventory_from_pool.keys():
                if item_name in self.item_name_groups[PASS]:
                    starting_passes_list.append(item_name)
            if len(starting_passes_list) > 0:
                for display_region_name in display_region_name_to_pass_dict:
                    if display_region_name_to_pass_dict[display_region_name] == starting_passes_list[0]:
                        # The first subregion (AP Region) in a display region will be the starter region if a player puts that display region's pass in their starting inventory
                        self.starter_ap_region = display_region_subregions_dictionary[display_region_name][0]
                        break

            # If this is UT re-gen the value isn't empty and we skip trying to pick a starter_region since we already have one
            if self.starter_ap_region == "":
                initially_reachable_regions = []
                # Generate a collection state that is a copy of the current state but also has all the passes so we can
                # check what regions we can access without just getting told none because we have no passes
                all_passes_state: CollectionState = CollectionState(self.multiworld)
                self.origin_region_name = SPAWNING_MEADOWS_AP_REGION
                for region_pass in self.item_name_groups[PASS]:
                    all_passes_state.collect(self.create_item(region_pass), prevent_sweep=True)
                for ap_region in self.get_regions():
                    #This checks what AP Regions are accessible to the player
                    if ap_region.can_reach(all_passes_state) and ap_region.name != MENU_AP_REGION and ap_region.name != MODDED_ZONE_AP_REGION:
                        if len(ap_region.locations) > 2:
                            initially_reachable_regions.append(ap_region)
                self.starter_ap_region = self.random.choice(initially_reachable_regions).name
                #Until we have a teleport location in every single ap region, for now we take specifically the first ap region in the display regions subregion list
                self.starter_ap_region = display_region_subregions_dictionary[ap_region_to_display_region_dictionary[self.starter_ap_region]][0]
            logging.getLogger().info("Starting region is " + self.starter_ap_region)
            self.origin_region_name = self.starter_ap_region
            #only push if player doesn't already have the pass from their starting inventory
            if len(starting_passes_list) == 0:
                #Converts the AP Region that was picked as the starting region to the Display Region containing that AP Region
                self.multiworld.push_precollected(self.create_item(display_region_name_to_pass_dict[ap_region_to_display_region_dictionary[self.starter_ap_region]]))

    def create_item(self, name: str) -> Item:
        if name in item_table:
            data = item_table[name]
            return Item(name, data.classification, data.code, self.player)
        else:
            matches = [item for (index, item) in enumerate(self.modded_items) if item.name == name]
            return Item(matches[0].name, matches[0].classification, matches[0].code, self.player)

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
                if self.options.clamshell_goal_quantity.value < 2:
                    self.options.clamshell_goal_quantity.value = 2
                self.options.extra_clamshells_in_pool.value = int(max_clamshells - self.options.clamshell_goal_quantity.value)
                if self.options.extra_clamshells_in_pool.value < 0:
                    self.options.extra_clamshells_in_pool.value = 0

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
        # this formula is how we can do ceiling division in Python
        progressive_levels = -(self.options.max_level.value // -self.options.progressive_level_size.value)
        #don't forget to -1
        if progressive_levels > max_progressive_levels:
            potential_progressive_level_size = -(self.options.max_level.value // -max_progressive_levels)
            potential_max_level = self.options.max_level.value

            if potential_progressive_level_size > self.options.progressive_level_size.range_end:
                potential_progressive_level_size = self.options.progressive_level_size.range_end
                potential_max_level = max_progressive_levels * potential_progressive_level_size

            if self.options.max_level.value > potential_max_level:
                raise Exception(f"For player {self.player_name}: yaml settings were too restrictive. Needed at least {-(self.options.max_level.value // -potential_progressive_level_size)} Progressive Levels, but only room for {max_progressive_levels} Progressive Levels in the pool. "
                                f"This is usually caused by mods that add more items than locations. Change settings and regenerate.")
            else:
                message = (f"For player {self.player_name}: yaml settings were too restrictive. Only room for {max_progressive_levels} Progressive Levels in the pool. "
                           f"Increased progressive_level_size to {potential_progressive_level_size}.")
                logging.getLogger().info(message)

                self.options.progressive_level_size.value = potential_progressive_level_size

        progressive_levels = -(self.options.max_level.value // -self.options.progressive_level_size.value)
        return progressive_levels

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

        if self.options.goal.value == self.options.goal.option_astley:
            excluded_items.add(NEW_WORLD_STONE)

        if self.options.goal.value == self.options.goal.option_true_astley:
            excluded_items.add(NEW_WORLD_STONE)
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

        if self.options.use_mods:
            combined_locations: List[ModLocationData] = self.modded_locations
            combined_locations.extend(self.modded_shops)

            for modded_item in self.modded_items:
                update_item_classification(modded_item, [location.rule_condition for location in combined_locations], self)
                item = self.create_item(modded_item.name)
                pool.append(item)

        if not self.options.level_gating.value == self.options.level_gating.option_none:
            #guarantee space for 2 clamshells, one on the following line and one because you start with 1 progressive level already
            max_progressive_levels: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - 1
            #players start with one or more, depending on their Level Compared to Enemies setting
            for _ in range (self.get_total_progressive_levels(max_progressive_levels) - self.starting_progressive_levels):
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
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(THE_NEW_WORLD_AP_REGION, player=self.player)
            self.included_regions.append(THE_NEW_WORLD_DISPLAY_NAME)
        elif self.options.goal == self.options.goal.option_true_astley:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(THE_OLD_WORLD_AP_REGION, player=self.player) and state.can_reach(THE_NEW_WORLD_AP_REGION, player=self.player)
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
        slot_data_removed_locations = []
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

            for location in self.removed_locations:
                slot_data_removed_locations.append({"Id": location.code,
                                            "APRegion": location.ap_region})

        # look into replacing this big chonky return block with self.options.as_dict() and then just adding the extras to the dict after
        return {
            "apworldVersion": self.world_version.as_simple_string(),
            "goal": self.options.goal.value,
            "clamshellGoalQuantity": self.get_goal_clamshells(),
            "extraClamshellsInPool": self.get_extra_clamshells(),
            "jobGoalAmount": self.options.new_world_stone_job_quantity.value,
            "jobRando": self.options.job_rando.value,
            "startingJobsForUT": self.starting_jobs,
            "startingJobQuantity": self.options.starting_job_quantity.value,
            "randomizeStartingJobs": bool(self.options.job_rando.value == self.options.job_rando.option_full),
            "startingJobs": self.get_job_id_list(),
            "killBossesMode" : bool(self.options.kill_bosses_mode.value),
            "shopsanity": self.options.shopsanity.value,
            "regionsanity": self.options.regionsanity.value,
            "includedRegions": self.included_regions,
            "includedRegionsOption": self.options.included_regions.value,
            "progressiveMountMode": self.options.progressive_mount_mode.value,
            "levelGating": self.options.level_gating.value,
            "levelComparedToEnemies": self.options.level_compared_to_enemies.value,
            "progressiveLevelSize": self.options.progressive_level_size.value,
            "maxLevel": self.options.max_level.value,
            "keyMode": self.options.key_mode.value,
            "obscureRoutes": bool(self.options.obscure_routes.value),
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
            "removedLocations": slot_data_removed_locations,
            # "moddedLocationsForUT": self.modded_locations,
            # "moddedShopsForUT": self.modded_shops,
            "starterRegion": self.starter_ap_region, # stored for UT re-gen
            "prefillMap": bool(self.options.fill_full_map.value),
            "disableSparks": bool(self.options.disable_sparks.value),
        }