import logging
from .constants.mounts import *
from .constants.jobs import *
from .constants.keys import *
from .constants.key_items import *
from .constants.regions import *
from .constants.teleport_stones import *
from .constants.item_groups import *
from .constants.region_passes import *
from .items import item_table, optional_scholar_abilities, get_random_starting_jobs, filler_items, \
    get_item_names_per_category, progressive_equipment, non_progressive_equipment, get_starting_jobs, \
    set_jobs_at_default_locations, default_starting_job_list, key_rings, dungeon_keys, singleton_keys, \
    region_name_to_pass_dict
from .locations import get_locations, get_bosses, get_shops
from .presets import crystal_project_options_presets
from .regions import init_areas
from .options import CrystalProjectOptions, IncludedRegions, create_option_groups
from .rules import CrystalProjectLogic
from .mod_helper import get_modded_items, get_modded_locations, get_mod_guids
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
    apworld_version = "0.6.0"
    game = "Crystal Project"
    options_dataclass = CrystalProjectOptions
    options: CrystalProjectOptions
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(-1, options)}
    boss_name_to_id = {boss.name: boss.code for boss in get_bosses(-1, options)}
    shop_name_to_id = {shop.name: shop.code for shop in get_shops(-1, options)}
    location_name_to_id.update(boss_name_to_id)
    location_name_to_id.update(shop_name_to_id)
    item_name_groups = get_item_names_per_category()
    modded_items = mod_helper.get_modded_items(-1, options)

    for modded_item in modded_items:
        item_name_to_id[modded_item.name] = modded_item.code
        item_name_groups.setdefault('MOD', set()).add(modded_item.name)

    modded_locations = mod_helper.get_modded_locations(-1, World, options)

    for modded_location in modded_locations:
        location_name_to_id[modded_location.name] = modded_location.code

    modded_shops = mod_helper.get_modded_shopsanity_locations(-1, World, options)

    for modded_shop in modded_shops:
        location_name_to_id[modded_shop.name] = modded_shop.code

    web = CrystalProjectWeb()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.starter_region: str = ""
        self.starting_jobs: List[str] = []
        self.included_regions: List[str] = []
        self.statically_placed_jobs:int = 0

    def generate_early(self):
        self.multiworld.push_precollected(self.create_item(HOME_POINT_STONE))

        self.starting_jobs = get_starting_jobs(self)
        for job in self.starting_jobs:
            self.multiworld.push_precollected(self.create_item(job))

        if self.options.startWithTreasureFinder.value:
            self.multiworld.push_precollected(self.create_item(TREASURE_FINDER))

        if self.options.startWithMaps.value:
            for map_name in self.item_name_groups[MAP]:
                self.multiworld.push_precollected(self.create_item(map_name))

        if not self.options.levelGating.value == self.options.levelGating.option_none:
            self.multiworld.push_precollected(self.create_item(PROGRESSIVE_LEVEL))

    def create_regions(self) -> None:
        locations = get_locations(self.player, self.options)

        if self.options.killBossesMode.value == self.options.killBossesMode.option_true:
            bosses = get_bosses(self.player, self.options)
            locations.extend(bosses)

        if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
            shops = get_shops(self.player, self.options)
            locations.extend(shops)

        if self.options.useMods:
            modded_locations = mod_helper.get_modded_locations(self.player, self, self.options)
            locations.extend(modded_locations)

        if self.options.useMods and self.options.shopsanity.value != self.options.shopsanity.option_disabled:
            modded_shops = mod_helper.get_modded_shopsanity_locations(self.player, self, self.options)
            locations.extend(modded_shops)

        init_areas(self, locations, self.options)

        if self.options.jobRando.value == self.options.jobRando.option_none:
            jobs_earnable = set_jobs_at_default_locations(self)
        else:
            jobs_earnable = len(self.item_name_groups[JOB]) - len(self.starting_jobs)

        if (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and self.options.newWorldStoneJobQuantity.value > jobs_earnable:
            message = "For player {2}: newWorldStoneJobQuantity was set to {0} but your options only had {1} jobs in pool. Reduced newWorldStoneJobQuantity to {1}."
            logging.getLogger().info(message.format(self.options.newWorldStoneJobQuantity.value, jobs_earnable, self.player_name))
            self.options.newWorldStoneJobQuantity.value = jobs_earnable

        # pick one region to give a starting pass to and then save that later
        if self.options.regionsanity.value == self.options.regionsanity.option_true:
            initially_reachable_regions = []
            # Generate a collection state that is a copy of the current state but also has all the passes so we can
            # check what regions we can access without just getting told none because we have no passes
            all_passes_state: CollectionState = CollectionState(self.multiworld)
            for region_pass in self.item_name_groups[PASS]:
                all_passes_state.collect(self.create_item(region_pass))
            for region in self.get_regions():
                if region.can_reach(all_passes_state) and region.name != MENU:
                    if len(region.locations) > 2:
                        initially_reachable_regions.append(region)
            self.starter_region = self.random.choice(initially_reachable_regions).name
            # logging.getLogger().info("Starting region is " + self.starter_region)
            self.origin_region_name = self.starter_region
            self.multiworld.push_precollected(self.create_item(region_name_to_pass_dict[self.starter_region]))
            self.multiworld.get_region(self.starter_region, self.player).add_exits([MENU])

    def create_item(self, name: str) -> Item:
        if name in item_table:
            data = item_table[name]
            return Item(name, data.classification, data.code, self.player)

        return Item(name, ItemClassification.filler, None, self.player)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

    def get_goal_clamshells(self) -> int:
        goal_clamshell_quantity = 2
        if self.options.goal.value == self.options.goal.option_clamshells:
            goal_clamshell_quantity = self.options.clamshellGoalQuantity.value
        return goal_clamshell_quantity

    def get_total_clamshells(self, max_clamshells: int) -> int:
        total_clamshell_quantity = 3
        if self.options.goal.value == self.options.goal.option_clamshells:
            total_clamshell_quantity = self.options.clamshellGoalQuantity.value + self.options.extraClamshellsInPool.value
            # If the player's options ask to put more clamshells in the pool than there is room, reduce their options proportionally so they fit
            if total_clamshell_quantity > max_clamshells:
                percent_goal_clamshells = self.options.clamshellGoalQuantity.value / total_clamshell_quantity
                self.options.clamshellGoalQuantity.value = int(percent_goal_clamshells * max_clamshells)
                if self.options.clamshellGoalQuantity.value < 1:
                    self.options.clamshellGoalQuantity.value = 1
                self.options.extraClamshellsInPool.value = int(max_clamshells - self.options.clamshellGoalQuantity.value)

                # Log the change to player settings
                message = ("For player {2}: total_clamshells was {0} but there was only room for {1} clamshells in the pool. "
                           "Reduced clamshellGoalQuantity to {3} and extraClamshellsInPool to {4}.")
                logging.getLogger().info(message.format(total_clamshell_quantity, max_clamshells, self.player_name,
                                                self.options.clamshellGoalQuantity.value, self.options.extraClamshellsInPool.value))

                total_clamshell_quantity = self.options.clamshellGoalQuantity.value + self.options.extraClamshellsInPool.value
        return total_clamshell_quantity

    #making randomized scholar ability pool
    def get_optional_scholar_abilities(self, count: int):
        return self.random.sample(optional_scholar_abilities, count)

    def get_filler_item_name(self) -> str:
        # traps go here if we have any
        # trap_chance: int = self.options.trap_chance.value
        # enabled_traps: List[str] = self.options.traps.value

        # if self.random.random() < (trap_chance / 100) and enabled_traps:
        #     return self.random.choice(enabled_traps)
        # else:
        #     return self.random.choice(filler_items) 
        return self.random.choice(filler_items)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(HOME_POINT_STONE)

        for job in self.starting_jobs:
            excluded_items.add(job)

        if self.options.progressiveMountMode.value == self.options.progressiveMountMode.option_true:
            for mount in self.item_name_groups[MOUNT]:
               if mount != PROGRESSIVE_MOUNT:
                   excluded_items.add(mount)
        else:
            excluded_items.add(PROGRESSIVE_MOUNT)

        if self.options.levelGating.value == self.options.levelGating.option_none:
            excluded_items.add(PROGRESSIVE_LEVEL)

        if self.options.startWithTreasureFinder:
            excluded_items.add(TREASURE_FINDER)

        if self.options.startWithMaps:
            for map_name in self.item_name_groups[MAP]:
                excluded_items.add(map_name)

        if self.options.goal == self.options.goal.option_astley:
            excluded_items.add(NEW_WORLD_STONE)

        if self.options.goal == self.options.goal.option_true_astley:
            excluded_items.add(NEW_WORLD_STONE)
            excluded_items.add(OLD_WORLD_STONE)

        if self.options.includeSummonAbilities == self.options.includeSummonAbilities.option_false:
            for summon in self.item_name_groups[SUMMON]:
                excluded_items.add(summon)

        if self.options.includeScholarAbilities == self.options.includeScholarAbilities.option_false:
            for scholar_ability in self.item_name_groups[SCHOLAR_ABILITY]:
                excluded_items.add(scholar_ability)

        #Progressive Equipment Mode
        if self.options.progressiveEquipmentMode.value == self.options.progressiveEquipmentMode.option_false:
            for progressive_equipment_piece in progressive_equipment:
                excluded_items.add(progressive_equipment_piece)
        else:
            for equipment_piece in non_progressive_equipment:
                excluded_items.add(equipment_piece)

        #For non-keyring modes
        if (self.options.keyMode.value != self.options.keyMode.option_key_ring and
            self.options.keyMode.value != self.options.keyMode.option_key_ring_skelefree):
            for keyring in key_rings:
                excluded_items.add(keyring)

        #For non-vanilla key modes
        if (self.options.keyMode.value != self.options.keyMode.option_vanilla and
            self.options.keyMode.value != self.options.keyMode.option_vanilla_skelefree):
            for key in dungeon_keys:
                excluded_items.add(key)

        #For skeleton key mode
        if self.options.keyMode.value == self.options.keyMode.option_skeleton:
            for key in singleton_keys:
                excluded_items.add(key)

        if (self.options.keyMode.value == self.options.keyMode.option_vanilla_skelefree or 
            self.options.keyMode.value == self.options.keyMode.option_key_ring_skelefree):
            excluded_items.add(SKELETON_KEY)

        if self.options.jobRando.value == self.options.jobRando.option_none:
            excluded_items.add(FENCER_JOB)
            excluded_items.add(SHAMAN_JOB)
            excluded_items.add(SCHOLAR_JOB)
            excluded_items.add(AEGIS_JOB)
            excluded_items.add(HUNTER_JOB)
            excluded_items.add(CHEMIST_JOB)
            excluded_items.add(REAPER_JOB)
            excluded_items.add(NINJA_JOB)
            excluded_items.add(NOMAD_JOB)
            excluded_items.add(DERVISH_JOB)
            excluded_items.add(BEATSMITH_JOB)
            excluded_items.add(SAMURAI_JOB)
            excluded_items.add(ASSASSIN_JOB)
            excluded_items.add(VALKYRIE_JOB)
            excluded_items.add(SUMMONER_JOB)
            excluded_items.add(BEASTMASTER_JOB)
            excluded_items.add(WEAVER_JOB)
            excluded_items.add(MIMIC_JOB)

        #regionsanity items
        if self.options.regionsanity.value == self.options.regionsanity.option_false:
            for region_pass in self.item_name_groups[PASS]:
                excluded_items.add(region_pass)
        else:
            excluded_items.add(region_name_to_pass_dict[self.starter_region])

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                #Check region and add the region amounts; then check Shopsanity and add the shop amounts
                amount:int = int(data.beginnerAmount or 0)
                if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                    amount = amount + int(data.beginnerShops or 0)
                if self.options.includedRegions == self.options.includedRegions.option_advanced:
                    amount = amount + int(data.advancedAmount or 0)
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.advancedShops or 0)
                elif self.options.includedRegions == self.options.includedRegions.option_expert:
                    amount = amount + int(data.advancedAmount or 0) + int(data.expertAmount or 0)
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.expertShops or 0)
                elif self.options.includedRegions == self.options.includedRegions.option_all:
                    amount = amount + int(data.advancedAmount or 0) + int(data.expertAmount or 0) + int(data.endGameAmount or 0)
                    #atm there are no end-game specific shopsanity items
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + int(data.endGameShops or 0)

                # Make sure new world pass is included if region sanity of on and its required for the goal
                if (self.options.regionsanity.value == self.options.regionsanity.option_true and
                        (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and
                        name == THE_NEW_WORLD_PASS):
                    amount = 1
                # Same goes for old world pass
                elif (self.options.regionsanity.value == self.options.regionsanity.option_true and
                        self.options.goal.value == self.options.goal.option_true_astley and
                        name == THE_OLD_WORLD_PASS):
                    amount = 1

                for _ in range(amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        if not self.options.levelGating.value == self.options.levelGating.option_none:
            #this formula is how we can do ceiling division in Python
            progressive_levels_in_pool = -(self.options.maxLevel.value // -self.options.progressiveLevelSize.value)
            #players start with one
            for _ in range (progressive_levels_in_pool - 1):
                item = self.set_classifications(PROGRESSIVE_LEVEL)
                pool.append(item)

        if self.options.goal.value == self.options.goal.option_true_astley:
            for _ in range(4):
                item = self.set_classifications(DEITY_EYE)
                pool.append(item)
            item = self.set_classifications(STEM_WARD)
            pool.append(item)

        #7 spells randomly chosen from the entire pool (they have Reverse Polarity as default to merc Gran)
        if self.options.includedRegions == self.options.includedRegions.option_beginner:
            for scholar_ability in self.get_optional_scholar_abilities(7):
                item = self.create_item(scholar_ability)
                pool.append(item)

        max_clamshells: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        for _ in range(self.get_total_clamshells(max_clamshells)):
            item = self.set_classifications(CLAMSHELL)
            pool.append(item)

        if self.options.useMods:
            modded_items = mod_helper.get_modded_items(self.player, self.options)

            for modded_item in modded_items:
                pool.append(modded_item)

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
        win_condition_item: str
        if self.options.goal == self.options.goal.option_astley:
            win_condition_item = NEW_WORLD_STONE # todo should this still be here if we auto-hand you the stone?
            self.multiworld.completion_condition[self.player] = lambda state: logic.has_jobs(state, self.options.newWorldStoneJobQuantity.value)
            self.included_regions.append(THE_NEW_WORLD)
        elif self.options.goal == self.options.goal.option_true_astley:
            win_condition_item = OLD_WORLD_STONE
            self.multiworld.completion_condition[self.player] = lambda state: logic.has_jobs(state, self.options.newWorldStoneJobQuantity.value) and logic.old_world_requirements(state)
            self.included_regions.append(THE_OLD_WORLD)
        elif self.options.goal == self.options.goal.option_clamshells:
            win_condition_item = CLAMSHELL
            self.multiworld.completion_condition[self.player] = lambda state: state.has(win_condition_item, self.player, self.options.clamshellGoalQuantity.value)

    def get_job_id_list(self) -> List[int]:
        job_ids: List[int] = []
        for job in self.starting_jobs:
            job_ids.append(self.item_name_to_id[job])

        return job_ids

    # This is data that needs to be readable from within the modded version of the game.
    # Example job rando makes the crystals behave differently, so the game needs to know about it.
    def fill_slot_data(self) -> Dict[str, Any]:
        mod_guids = None
        if options.UseMods:
            mod_guids = mod_helper.get_mod_guids()

        # look into replacing this big chonky return block with self.options.as_dict() and then just adding the extras to the dict after

        return {
            "apworld_version": self.apworld_version,
            "goal": self.options.goal.value,
            "clamshellGoalQuantity": self.get_goal_clamshells(),
            "jobGoalAmount": self.options.newWorldStoneJobQuantity.value,
            "startWithMaps": bool(self.options.startWithMaps.value),
            "randomizeStartingJobs": bool(self.options.jobRando.value == self.options.jobRando.option_full),
            "killBossesMode" : bool(self.options.killBossesMode.value),
            "easyLeveling": bool(self.options.easyLeveling.value),
            "obscureRoutes": bool(self.options.obscureRoutes.value),
            "randomizeMusic": bool(self.options.randomizeMusic.value),
            "levelGating": self.options.levelGating.value,
            "progressiveLevelSize": self.options.progressiveLevelSize.value,
            "maxLevel": self.options.maxLevel.value,
            "shopsanity": self.options.shopsanity.value,
            "regionsanity": bool(self.options.regionsanity.value),
            "startingJobs": self.get_job_id_list(),
            "includedRegions": self.included_regions,
            "modGuids": mod_guids,
        }