from .constants.keys import *
from .constants.key_items import *
from .items import item_table, optional_scholar_abilities, get_random_starting_jobs, filler_items, \
    get_item_names_per_category, progressive_equipment, non_progressive_equipment, get_starting_jobs, \
    set_jobs_at_default_locations, default_starting_job_list, job_list
from .locations import get_locations, get_bosses, get_shops
from .regions import init_areas
from .options import CrystalProjectOptions, IncludedRegions
from .rules import CrystalProjectLogic
from typing import List, Set, Dict, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, MultiWorld

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
    #options_presets = MuseDashPresets
    #option_groups = md_option_groups

class CrystalProjectWorld(World):
    """Crystal Project is a mix of old school job based jRPG mixed with a ton of 3D platforming and exploration."""

    game = "Crystal Project"
    options_dataclass = CrystalProjectOptions
    options: CrystalProjectOptions
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(-1, None)}
    boss_name_to_id = {boss.name: boss.code for boss in get_bosses(-1, None)}
    shop_name_to_id = {shop.name: shop.code for shop in get_shops(-1, None)}
    location_name_to_id.update(boss_name_to_id)
    location_name_to_id.update(shop_name_to_id)
    item_name_groups = get_item_names_per_category()
    web = CrystalProjectWeb()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.starting_jobs = []
        self.included_regions: List[str] = []
        self.statically_placed_jobs:int = 0

    def generate_early(self):
        self.multiworld.push_precollected(self.create_item("Item - Home Point Stone"))

        self.starting_jobs = get_starting_jobs(self)
        for job in self.starting_jobs:
            self.multiworld.push_precollected(self.create_item(job.name))

        if self.options.startWithTreasureFinder:
            self.multiworld.push_precollected(self.create_item("Item - Treasure Finder"))

        if self.options.startWithMaps:
            self.multiworld.push_precollected(self.create_item("Item - Spawning Meadows Map"))
            self.multiworld.push_precollected(self.create_item("Item - Delende Map"))
            self.multiworld.push_precollected(self.create_item("Item - Pale Grotto Map"))
            self.multiworld.push_precollected(self.create_item("Item - Seaside Cliffs Map"))
            self.multiworld.push_precollected(self.create_item("Item - Draft Shaft Conduit Map"))
            self.multiworld.push_precollected(self.create_item("Item - Proving Meadows Map"))
            self.multiworld.push_precollected(self.create_item("Item - Soiled Den Map"))
            self.multiworld.push_precollected(self.create_item("Item - Yamagawa M.A. Map"))
            self.multiworld.push_precollected(self.create_item("Item - Skumparadise Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Courtyard Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jojo Sewers Map"))
            self.multiworld.push_precollected(self.create_item("Item - Greenshire Reprise Map"))
            self.multiworld.push_precollected(self.create_item("Item - Mercury Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Boomer Society Map"))
            self.multiworld.push_precollected(self.create_item("Item - Rolling Quintar Fields Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Nest Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Jail Map"))
            self.multiworld.push_precollected(self.create_item("Item - Cobblestone Crag Map"))
            self.multiworld.push_precollected(self.create_item("Item - Okimoto N.S. Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon Pass Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon River Map"))
            self.multiworld.push_precollected(self.create_item("Item - Poseidon Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Poko Poko Desert Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sara Sara Bazaar Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sara Sara Beach Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ancient Reservoir Map"))
            self.multiworld.push_precollected(self.create_item("Item - Shoudu Province Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Undercity Map"))
            self.multiworld.push_precollected(self.create_item("Item - Beaurior Volcano Map"))
            self.multiworld.push_precollected(self.create_item("Item - Beaurior Rock Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Tall Tall Heights Map"))
            self.multiworld.push_precollected(self.create_item("Item - Slip Glide Ride Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ganymede Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Reserve Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Sanctum Map"))
            self.multiworld.push_precollected(self.create_item("Item - Lake Delende Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jidamba Tangle Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jidamba Eaclaneya Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Deep Sea Map"))
            self.multiworld.push_precollected(self.create_item("Item - The New World Map"))
            self.multiworld.push_precollected(self.create_item("Item - Continental Tram Map"))
            self.multiworld.push_precollected(self.create_item("Item - Castle Ramparts Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon Bay Map"))
            self.multiworld.push_precollected(self.create_item("Item - Lands End Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Pipeline Map"))
            self.multiworld.push_precollected(self.create_item("Item - Northern Cave Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Depths Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Open Sea Map"))
            self.multiworld.push_precollected(self.create_item("Item - Dione Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Neptune Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Castle Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ancient Labyrinth Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Mausoleum Map"))
            self.multiworld.push_precollected(self.create_item("Item - Basement Map"))
            self.multiworld.push_precollected(self.create_item("Item - Trial Caves Map"))
            self.multiworld.push_precollected(self.create_item("Item - Overpass Map"))
            self.multiworld.push_precollected(self.create_item("Item - Underpass Map"))
            self.multiworld.push_precollected(self.create_item("Item - River Cats Ego Map"))
            self.multiworld.push_precollected(self.create_item("Item - Northern Stretch Map"))
            self.multiworld.push_precollected(self.create_item("Item - Eastern Chasm Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sequoia Athenaeum Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Chalice of Tar Map"))
            self.multiworld.push_precollected(self.create_item("Item - Flyers Crag Map"))
            self.multiworld.push_precollected(self.create_item("Item - Flyers Lookout Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jade Cavern Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Old World Map"))

    def create_regions(self) -> None:
        locations = get_locations(self.player, self.options)

        if self.options.killBossesMode.value == self.options.killBossesMode.option_true:
            bosses = get_bosses(self.player, self.options)
            locations.extend(bosses)

        if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
            shops = get_shops(self.player, self.options)
            locations.extend(shops)

        init_areas(self, locations, self.options)

        if self.options.jobRando.value == self.options.jobRando.option_none:
            jobs_earnable = set_jobs_at_default_locations(self)
        else:
            jobs_earnable = len(job_list) - len(self.starting_jobs)

        if (self.options.goal.value == self.options.goal.option_astley or self.options.goal.value == self.options.goal.option_true_astley) and self.options.newWorldStoneJobQuantity.value > jobs_earnable:
            message = "For player {2}: newWorldStoneJobQuantity was set to {0} but your options only had {1} jobs in pool. Reduced newWorldStoneJobQuantity to {1}."
            self.logger.info(message.format(self.options.newWorldStoneJobQuantity.value, jobs_earnable, self.player_name))
            self.options.newWorldStoneJobQuantity.value = jobs_earnable

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

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
        excluded_items.add("Item - Home Point Stone")

        for job in self.starting_jobs:
            excluded_items.add(job.name)

        if not self.options.levelGating:
            excluded_items.add("Item - Progressive Level Cap")

        if self.options.startWithTreasureFinder:
            excluded_items.add("Item - Treasure Finder")

        if self.options.startWithMaps:
            excluded_items.add("Item - Spawning Meadows Map")
            excluded_items.add("Item - Delende Map")
            excluded_items.add("Item - Pale Grotto Map")
            excluded_items.add("Item - Seaside Cliffs Map")
            excluded_items.add("Item - Draft Shaft Conduit Map")
            excluded_items.add("Item - Proving Meadows Map")
            excluded_items.add("Item - Soiled Den Map")
            excluded_items.add("Item - Yamagawa M.A. Map")
            excluded_items.add("Item - Skumparadise Map")
            excluded_items.add("Item - Capital Courtyard Map")
            excluded_items.add("Item - Capital Sequoia Map")
            excluded_items.add("Item - Jojo Sewers Map")
            excluded_items.add("Item - Greenshire Reprise Map")
            excluded_items.add("Item - Mercury Shrine Map")
            excluded_items.add("Item - Boomer Society Map")
            excluded_items.add("Item - Rolling Quintar Fields Map")
            excluded_items.add("Item - Quintar Nest Map")
            excluded_items.add("Item - Capital Jail Map")
            excluded_items.add("Item - Cobblestone Crag Map")
            excluded_items.add("Item - Okimoto N.S. Map")
            excluded_items.add("Item - Salmon Pass Map")
            excluded_items.add("Item - Salmon River Map")
            excluded_items.add("Item - Poseidon Shrine Map")
            excluded_items.add("Item - Poko Poko Desert Map")
            excluded_items.add("Item - Sara Sara Bazaar Map")
            excluded_items.add("Item - Sara Sara Beach Map")
            excluded_items.add("Item - Ancient Reservoir Map")
            excluded_items.add("Item - Shoudu Province Map")
            excluded_items.add("Item - The Undercity Map")
            excluded_items.add("Item - Beaurior Volcano Map")
            excluded_items.add("Item - Beaurior Rock Map")
            excluded_items.add("Item - The Sequoia Map")
            excluded_items.add("Item - Tall Tall Heights Map")
            excluded_items.add("Item - Slip Glide Ride Map")
            excluded_items.add("Item - Ganymede Shrine Map")
            excluded_items.add("Item - Quintar Reserve Map")
            excluded_items.add("Item - Quintar Sanctum Map")
            excluded_items.add("Item - Lake Delende Map")
            excluded_items.add("Item - Jidamba Tangle Map")
            excluded_items.add("Item - Jidamba Eaclaneya Map")
            excluded_items.add("Item - The Deep Sea Map")
            excluded_items.add("Item - The New World Map")
            excluded_items.add("Item - Continental Tram Map")
            excluded_items.add("Item - Castle Ramparts Map")
            excluded_items.add("Item - Salmon Bay Map")
            excluded_items.add("Item - Lands End Map")
            excluded_items.add("Item - Capital Pipeline Map")
            excluded_items.add("Item - Northern Cave Map")
            excluded_items.add("Item - The Depths Map")
            excluded_items.add("Item - The Open Sea Map")
            excluded_items.add("Item - Dione Shrine Map")
            excluded_items.add("Item - Neptune Shrine Map")
            excluded_items.add("Item - Castle Sequoia Map")
            excluded_items.add("Item - Ancient Labyrinth Map")
            excluded_items.add("Item - Quintar Mausoleum Map")
            excluded_items.add("Item - Basement Map")
            excluded_items.add("Item - Trial Caves Map")
            excluded_items.add("Item - Overpass Map")
            excluded_items.add("Item - Underpass Map")
            excluded_items.add("Item - River Cats Ego Map")
            excluded_items.add("Item - Northern Stretch Map")
            excluded_items.add("Item - Eastern Chasm Map")
            excluded_items.add("Item - Sequoia Athenaeum Map")
            excluded_items.add("Item - The Chalice of Tar Map")
            excluded_items.add("Item - Flyers Crag Map")
            excluded_items.add("Item - Flyers Lookout Map")
            excluded_items.add("Item - Jade Cavern Map")
            excluded_items.add("Item - The Old World Map")

        if self.options.goal == self.options.goal.option_astley:
            excluded_items.add("Item - New World Stone")

        if self.options.goal == self.options.goal.option_true_astley:
            excluded_items.add("Item - New World Stone")
            excluded_items.add("Item - Old World Stone")

        if self.options.includeSummonAbilities == self.options.includeSummonAbilities.option_false:
            excluded_items.add("Summon - Shaku")
            excluded_items.add("Summon - Pamoa")
            excluded_items.add("Summon - Guaba")
            excluded_items.add("Summon - Niltsi")
            excluded_items.add("Summon - Ioske")
            excluded_items.add("Summon - Coyote")
            excluded_items.add("Summon - Tira")
            excluded_items.add("Summon - Juses")
            excluded_items.add("Summon - Pah")

        if self.options.includeScholarAbilities == self.options.includeScholarAbilities.option_false:
            excluded_items.add("Scholar - Roost")
            excluded_items.add("Scholar - Lucky Dice")
            excluded_items.add("Scholar - Sun Bath")
            excluded_items.add("Scholar - Sleep Aura")
            excluded_items.add("Scholar - Regenerate")
            excluded_items.add("Scholar - Reverse Polarity")
            excluded_items.add("Scholar - Barrier")
            excluded_items.add("Scholar - MP Sickle")
            excluded_items.add("Scholar - Adrenaline")
            excluded_items.add("Scholar - Fire Breath")
            excluded_items.add("Scholar - Explode")
            excluded_items.add("Scholar - Whirlwind")
            excluded_items.add("Scholar - Atmoshear")
            excluded_items.add("Scholar - Build Life")
            excluded_items.add("Scholar - Aero")
            excluded_items.add("Scholar - Insult")
            excluded_items.add("Scholar - Infusion")
            excluded_items.add("Scholar - Overload")
            excluded_items.add("Scholar - Reflection")
            excluded_items.add("Scholar - Lifegiver")

        #Progressive Equipment Mode
        if self.options.progressiveEquipmentMode.value == self.options.progressiveEquipmentMode.option_false:
            [excluded_items.add(progressive_equipment_piece) for progressive_equipment_piece in progressive_equipment]
        else:
            [excluded_items.add(equipment_piece) for equipment_piece in non_progressive_equipment]

        if (self.options.keyMode.value != self.options.keyMode.option_key_ring or 
            self.options.keyMode.value != self.options.keyMode.option_key_ring_skelefree):
            excluded_items.add(PRISON_KEY_RING)
            excluded_items.add(BEAURIOR_KEY_RING)
            excluded_items.add(SLIP_GLIDE_RIDE_KEY_RING)
            excluded_items.add(ICE_PUZZLE_KEY_RING)
            excluded_items.add(JIDAMBA_KEY_RING)

        if (self.options.keyMode.value != self.options.keyMode.option_vanilla or 
            self.options.keyMode.value != self.options.keyMode.option_vanilla_skelefree):
            excluded_items.add(SOUTH_WING_KEY)
            excluded_items.add(EAST_WING_KEY)
            excluded_items.add(WEST_WING_KEY)
            excluded_items.add(DARK_WING_KEY)
            excluded_items.add(CELL_KEY)
            excluded_items.add(SMALL_KEY)
            excluded_items.add(BEAURIOR_BOSS_KEY)
            excluded_items.add(RED_DOOR_KEY)
            excluded_items.add(ICE_CELL_KEY)
            excluded_items.add(FOLIAGE_KEY)
            excluded_items.add(CAVE_KEY)
            excluded_items.add(CANOPY_KEY)

        if (self.options.keyMode.value == self.options.keyMode.option_vanilla_skelefree or 
            self.options.keyMode.value == self.options.keyMode.option_key_ring_skelefree):
            excluded_items.add(SKELETON_KEY)

        if self.options.jobRando.value == self.options.jobRando.option_none:
            excluded_items.add("Job - Fencer")
            excluded_items.add("Job - Shaman")
            excluded_items.add("Job - Scholar")
            excluded_items.add("Job - Aegis")
            excluded_items.add("Job - Hunter")
            excluded_items.add("Job - Chemist")
            excluded_items.add("Job - Reaper")
            excluded_items.add("Job - Ninja")
            excluded_items.add("Job - Nomad")
            excluded_items.add("Job - Dervish")
            excluded_items.add("Job - Beatsmith")
            excluded_items.add("Job - Samurai")
            excluded_items.add("Job - Assassin")
            excluded_items.add("Job - Valkyrie")
            excluded_items.add("Job - Summoner")
            excluded_items.add("Job - Beastmaster")
            excluded_items.add("Job - Weaver")
            excluded_items.add("Job - Mimic")

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                #Check region and add the region amounts; then check Shopsanity and add the shop amounts
                amount:int = data.beginnerAmount
                if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                    amount = amount + data.beginnerShops
                if self.options.includedRegions == self.options.includedRegions.option_advanced:
                    amount = amount + data.advancedAmount
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + data.advancedShops
                elif self.options.includedRegions == self.options.includedRegions.option_expert:
                    amount = amount + data.advancedAmount + data.expertAmount
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + data.expertShops
                elif self.options.includedRegions == self.options.includedRegions.option_all:
                    amount = amount + data.advancedAmount + data.expertAmount + data.endGameAmount
                    #atm there are no end-game specific shopsanity items
                    if self.options.shopsanity.value != self.options.shopsanity.option_disabled:
                        amount = amount + data.endGameShops
                for _ in range(amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        for _ in range (self.options.clamshellsInPool):
            item = self.set_classifications("Item - Clamshell")
            pool.append(item)

        if self.options.levelGating:
            for _ in range (self.options.levelUpsInPool):
                item = self.set_classifications("Item - Progressive Level Cap")
                pool.append(item)

        if self.options.goal.value == self.options.goal.option_true_astley:
            for _ in range(4):
                item = self.set_classifications("Item - Deity Eye")
                pool.append(item)
            item = self.set_classifications("Item - STEM WARD")
            pool.append(item)

        #7 spells randomly chosen from the entire pool (they have Reverse Polarity as default to merc Gran)
        if self.options.includedRegions == self.options.includedRegions.option_beginner:
            for scholar_ability in self.get_optional_scholar_abilities(7):
                item = self.create_item(scholar_ability)
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
        win_condition_item: str
        if self.options.goal == self.options.goal.option_astley:
            win_condition_item = "Item - New World Stone" # todo should this still be here if we auto-hand you the stone?
            self.multiworld.completion_condition[self.player] = lambda state: logic.has_jobs(state, self.options.newWorldStoneJobQuantity.value)
            self.included_regions.append("The New World")
        elif self.options.goal == self.options.goal.option_true_astley:
            win_condition_item = "Item - Old World Stone"
            self.multiworld.completion_condition[self.player] = lambda state: logic.has_jobs(state, self.options.newWorldStoneJobQuantity.value) and logic.old_world_requirements
            self.included_regions.append("The Old World")
        elif self.options.goal == self.options.goal.option_clamshells:
            win_condition_item = "Item - Clamshell"
            self.multiworld.completion_condition[self.player] = lambda state: state.has(win_condition_item, self.player, self.options.clamshellsQuantity.value)

    def get_job_id_list(self) -> List[int]:
        job_ids: List[int] = []
        for job in self.starting_jobs:
            job_ids.append(job.id)

        return job_ids

    # This is data that needs to be readable from within the modded version of the game.
    # Example job rando makes the crystals behave differently, so the game needs to know about it.
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "clamshellsQuantity": self.options.clamshellsQuantity.value,
            "jobGoalAmount": self.options.newWorldStoneJobQuantity.value,
            "startWithMaps": bool(self.options.startWithMaps.value),
            "randomizeStartingJobs": bool(self.options.jobRando.value == self.options.jobRando.option_full),
            "killBossesMode" : bool(self.options.killBossesMode.value),
            "easyLeveling": bool(self.options.easyLeveling.value),
            "randomizeMusic": bool(self.options.randomizeMusic.value),
            "levelGating": bool(self.options.levelGating.value),
            "shopsanity": self.options.shopsanity.value,
            "startingJobs": self.get_job_id_list(),
            "includedRegions": self.included_regions,
        }