from typing import Callable, Dict, List, Set, Union
from BaseClasses import MultiWorld, ItemClassification, Item, Location
from .Items import get_full_item_list, spider_mine_sources, second_pass_placeable_items, progressive_if_nco, \
    progressive_if_ext, spear_of_adun_calldowns, spear_of_adun_castable_passives
from .MissionTables import mission_orders, MissionInfo, MissionPools, \
    get_campaign_goal_priority, campaign_final_mission_locations, campaign_alt_final_mission_locations, \
    get_no_build_missions, SC2Campaign, SC2Race, SC2CampaignGoalPriority, SC2Mission, lookup_name_to_mission, \
    campaign_mission_table
from .Options import get_option_value, MissionOrder, \
    get_enabled_campaigns, get_disabled_campaigns, RequiredTactics, kerrigan_unit_available, GrantStoryTech, \
    TakeOverAIAllies, SpearOfAdunPresence, SpearOfAdunAutonomouslyCastAbilityPresence, campaign_depending_orders, \
    ShuffleCampaigns
from .LogicMixin import SC2Logic
from . import ItemNames

# Items with associated upgrades
UPGRADABLE_ITEMS = {item.parent_item for item in get_full_item_list().values() if item.parent_item}

BARRACKS_UNITS = {
    ItemNames.MARINE, ItemNames.MEDIC, ItemNames.FIREBAT, ItemNames.MARAUDER,
    ItemNames.REAPER, ItemNames.GHOST, ItemNames.SPECTRE,
}
FACTORY_UNITS = {
    ItemNames.HELLION, ItemNames.VULTURE, ItemNames.GOLIATH, ItemNames.DIAMONDBACK,
    ItemNames.SIEGE_TANK, ItemNames.THOR, ItemNames.PREDATOR, ItemNames.WIDOW_MINE,
    ItemNames.CYCLONE,
}
STARPORT_UNITS = {
    ItemNames.MEDIVAC, ItemNames.WRAITH, ItemNames.VIKING, ItemNames.BANSHEE,
    ItemNames.BATTLECRUISER, ItemNames.HERCULES, ItemNames.SCIENCE_VESSEL, ItemNames.RAVEN,
    ItemNames.LIBERATOR, ItemNames.VALKYRIE,
}


def filter_missions(multiworld: MultiWorld, player: int) -> Dict[MissionPools, List[SC2Mission]]:
    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """

    mission_order_type = get_option_value(multiworld, player, "mission_order")
    shuffle_no_build = get_option_value(multiworld, player, "shuffle_no_build")
    enabled_campaigns = get_enabled_campaigns(multiworld, player)
    disabled_campaigns = get_disabled_campaigns(multiworld, player)
    excluded_mission_names = get_option_value(multiworld, player, "excluded_missions")
    grant_story_tech = get_option_value(multiworld, player, "grant_story_tech") == GrantStoryTech.option_true
    excluded_missions: Set[SC2Mission] = set([lookup_name_to_mission[name] for name in excluded_mission_names])
    mission_pools: Dict[MissionPools, List[SC2Mission]] = {}
    for mission in SC2Mission:
        if not mission_pools.get(mission.pool):
            mission_pools[mission.pool] = list()
        mission_pools[mission.pool].append(mission)
    # A bit of safeguard:
    for mission_pool in MissionPools:
        if not mission_pools.get(mission_pool):
            mission_pools[mission_pool] = []

    if mission_order_type == MissionOrder.option_vanilla:
        # Vanilla uses the entire mission pool
        goal_priorities: Dict[SC2Campaign, SC2CampaignGoalPriority] = {campaign: get_campaign_goal_priority(campaign) for campaign in enabled_campaigns}
        goal_level = max(goal_priorities.values())
        candidate_campaigns = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
        goal_campaign = multiworld.random.choice(candidate_campaigns)
        if campaign_final_mission_locations[goal_campaign] is not None:
            mission_pools[MissionPools.FINAL] = [campaign_final_mission_locations[goal_campaign].mission]
        else:
            mission_pools[MissionPools.FINAL] = [list(campaign_alt_final_mission_locations[goal_campaign].keys())[0]]
        remove_final_mission_from_other_pools(mission_pools)
        return mission_pools
    # Omitting No-Build missions if not shuffling no-build
    if not shuffle_no_build:
        excluded_missions = excluded_missions.union(get_no_build_missions())
    # Omitting missions not in enabled campaigns
    for campaign in disabled_campaigns:
        excluded_missions = excluded_missions.union(campaign_mission_table[campaign])

    # Finding the goal map
    goal_priorities = {campaign: get_campaign_goal_priority(campaign, excluded_missions) for campaign in enabled_campaigns}
    goal_level = max(goal_priorities.values())
    candidate_campaigns = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
    goal_campaign = multiworld.random.choice(candidate_campaigns)
    primary_goal = campaign_final_mission_locations[goal_campaign]
    if primary_goal is None or primary_goal.mission in excluded_missions:
        # No primary goal or its mission is excluded
        candidate_missions = list(campaign_alt_final_mission_locations[goal_campaign].keys())
        candidate_missions = [mission for mission in candidate_missions if mission not in excluded_missions]
        if len(candidate_missions) == 0:
            raise Exception("There are no valid goal missions. Please exclude fewer missions.")
        goal_mission = multiworld.random.choice(candidate_missions)
    else:
        goal_mission = primary_goal.mission

    # Excluding missions
    for difficulty, mission_pool in mission_pools.items():
        mission_pools[difficulty] = [mission for mission in mission_pool if mission not in excluded_missions]
    mission_pools[MissionPools.FINAL] = [goal_mission]

    # Mission pool changes
    adv_tactics = get_option_value(multiworld, player, "required_tactics") != RequiredTactics.option_standard
    def move_mission(mission: SC2Mission, current_pool, new_pool):
        if mission in mission_pools[current_pool]:
            mission_pools[current_pool].remove(mission)
            mission_pools[new_pool].append(mission)
    # WoL
    if not get_option_value(multiworld, player, 'shuffle_no_build'):
        # Replacing No Build missions with Easy missions
        move_mission(SC2Mission.ZERO_HOUR, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.EVACUATION, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.DEVILS_PLAYGROUND, MissionPools.EASY, MissionPools.STARTER)
        # Pushing Outbreak to Normal, as it cannot be placed as the second mission on Build-Only
        move_mission(SC2Mission.OUTBREAK, MissionPools.EASY, MissionPools.MEDIUM)
        # Pushing extra Normal missions to Easy
        move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, MissionPools.MEDIUM, MissionPools.EASY)
        move_mission(SC2Mission.ECHOES_OF_THE_FUTURE, MissionPools.MEDIUM, MissionPools.EASY)
        move_mission(SC2Mission.CUTTHROAT, MissionPools.MEDIUM, MissionPools.EASY)
        # Additional changes on Advanced Tactics
        if adv_tactics:
            move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, MissionPools.EASY, MissionPools.STARTER)
            move_mission(SC2Mission.SMASH_AND_GRAB, MissionPools.EASY, MissionPools.STARTER)
            move_mission(SC2Mission.THE_MOEBIUS_FACTOR, MissionPools.MEDIUM, MissionPools.EASY)
            move_mission(SC2Mission.WELCOME_TO_THE_JUNGLE, MissionPools.MEDIUM, MissionPools.EASY)
            move_mission(SC2Mission.ENGINE_OF_DESTRUCTION, MissionPools.HARD, MissionPools.MEDIUM)
    # Prophecy needs to be adjusted on tiny grid
    if enabled_campaigns == {SC2Campaign.PROPHECY} and mission_order_type == MissionOrder.option_tiny_grid:
        move_mission(SC2Mission.A_SINISTER_TURN, MissionPools.MEDIUM, MissionPools.EASY)
    # Prologue's only valid starter is the goal mission
    if enabled_campaigns == {SC2Campaign.PROLOGUE} \
            or mission_order_type in campaign_depending_orders \
            and get_option_value(multiworld, player, "shuffle_campaigns") == ShuffleCampaigns.option_false:
        move_mission(SC2Mission.DARK_WHISPERS, MissionPools.EASY, MissionPools.STARTER)
    # HotS
    kerriganless = get_option_value(multiworld, player, "kerrigan_presence") not in kerrigan_unit_available
    if adv_tactics:
        # Medium -> Easy
        for mission in (SC2Mission.FIRE_IN_THE_SKY, SC2Mission.WAKING_THE_ANCIENT, SC2Mission.CONVICTION):
            move_mission(mission, MissionPools.MEDIUM, MissionPools.EASY)
        # Hard -> Medium
        move_mission(SC2Mission.PHANTOMS_OF_THE_VOID, MissionPools.HARD, MissionPools.MEDIUM)
        if not kerriganless:
            # Additional starter mission assuming player starts with minimal anti-air
            move_mission(SC2Mission.WAKING_THE_ANCIENT, MissionPools.EASY, MissionPools.STARTER)
    if grant_story_tech:
        # Additional starter mission if player is granted story tech
        move_mission(SC2Mission.ENEMY_WITHIN, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.TEMPLAR_S_RETURN, MissionPools.EASY, MissionPools.STARTER)
    if grant_story_tech or kerriganless:
        # The player has, all the stuff he needs, provided under these settings
        move_mission(SC2Mission.SUPREME, MissionPools.MEDIUM, MissionPools.STARTER)
        move_mission(SC2Mission.THE_INFINITE_CYCLE, MissionPools.MEDIUM, MissionPools.STARTER)
    if get_option_value(multiworld, player, "take_over_ai_allies") == TakeOverAIAllies.option_true:
        move_mission(SC2Mission.HARBINGER_OF_OBLIVION, MissionPools.MEDIUM, MissionPools.STARTER)
    if len(mission_pools[MissionPools.STARTER]) < 2 and not kerriganless or adv_tactics:
        # Conditionally moving Easy missions to Starter
        move_mission(SC2Mission.HARVEST_OF_SCREAMS, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.DOMINATION, MissionPools.EASY, MissionPools.STARTER)
    if len(mission_pools[MissionPools.STARTER]) < 2:
        move_mission(SC2Mission.TEMPLAR_S_RETURN, MissionPools.EASY, MissionPools.STARTER)

    remove_final_mission_from_other_pools(mission_pools)
    return mission_pools


def remove_final_mission_from_other_pools(mission_pools: Dict[MissionPools, List[SC2Mission]]):
    final_missions = mission_pools[MissionPools.FINAL]
    for pool, missions in mission_pools.items():
        if pool == MissionPools.FINAL:
            continue
        for final_mission in final_missions:
            while final_mission in missions:
                missions.remove(final_mission)


def get_item_upgrades(inventory: List[Item], parent_item: Union[Item, str]) -> List[Item]:
    item_name = parent_item.name if isinstance(parent_item, Item) else parent_item
    return [
        inv_item for inv_item in inventory
        if get_full_item_list()[inv_item.name].parent_item == item_name
    ]


def get_item_quantity(item: Item, multiworld: MultiWorld, player: int):
    if (not get_option_value(multiworld, player, "nco_items")) \
            and item.name in progressive_if_nco:
        return 1
    if (not get_option_value(multiworld, player, "ext_items")) \
            and item.name in progressive_if_ext:
        return 1
    return get_full_item_list()[item.name].quantity


def copy_item(item: Item):
    return Item(item.name, item.classification, item.code, item.player)


def num_missions(multiworld: MultiWorld, player: int) -> int:
    mission_order_type = multiworld.mission_order[player]
    if mission_order_type != MissionOrder.option_grid:
        return len(mission_orders[mission_order_type]) - 1
    else:
        mission_pools = filter_missions(multiworld, player)
        return sum(len(pool) for _, pool in mission_pools.items())


class ValidInventory:

    def has(self, item: str, player: int):
        return item in self.logical_inventory

    def has_any(self, items: Set[str], player: int):
        return any(item in self.logical_inventory for item in items)

    def has_all(self, items: Set[str], player: int):
        return all(item in self.logical_inventory for item in items)

    def count(self, item: str, player: int) -> int:
        return len([inventory_item for inventory_item in self.logical_inventory if inventory_item == item])

    def has_units_per_structure(self) -> bool:
        return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(FACTORY_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(STARPORT_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure

    def generate_reduced_inventory(self, inventory_size: int, mission_requirements: List[Callable]) -> List[Item]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory = list(self.item_pool)
        locked_items = list(self.locked_items)
        self.logical_inventory = [
            item.name for item in inventory + locked_items + self.existing_items
            if item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing)
        ]
        requirements = mission_requirements
        parent_items = self.item_children.keys()
        parent_lookup = {child: parent for parent, children in self.item_children.items() for child in children}
        minimum_upgrades = get_option_value(self.multiworld, self.player, "min_number_of_upgrades")
        item_list = get_full_item_list()

        def attempt_removal(item: Item) -> bool:
            inventory.remove(item)
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if not all(requirement(self) for requirement in requirements):
                    # If item cannot be removed, lock or revert
                    self.logical_inventory.append(item.name)
                    for _ in range(get_item_quantity(item, self.multiworld, self.player)):
                        locked_items.append(copy_item(item))
                    return False
            return True

        # Limit the maximum number of upgrades
        maxUpgrad = get_option_value(self.multiworld, self.player,
                            "max_number_of_upgrades")
        if maxUpgrad != -1:
            unit_avail_upgrades = {}
            # Needed to take into account locked/existing items
            unit_nb_upgrades = {}
            for item in inventory:
                cItem = item_list[item.name]
                if cItem.type in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
                    unit_avail_upgrades[item.name] = []
                    unit_nb_upgrades[item.name] = 0
                elif cItem.parent_item is not None:
                    if cItem.parent_item not in unit_avail_upgrades:
                        unit_avail_upgrades[cItem.parent_item] = [item]
                        unit_nb_upgrades[cItem.parent_item] = 1
                    else:
                        unit_avail_upgrades[cItem.parent_item].append(item)
                        unit_nb_upgrades[cItem.parent_item] += 1
            # For those two categories, we count them but dont include them in removal
            for item in locked_items + self.existing_items:
                cItem = item_list[item.name]
                if cItem.type in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
                    unit_avail_upgrades[item.name] = []
                    unit_nb_upgrades[item.name] = 0
                elif cItem.parent_item is not None:
                    if cItem.parent_item not in unit_avail_upgrades:
                        unit_nb_upgrades[cItem.parent_item] = 1
                    else:
                        unit_nb_upgrades[cItem.parent_item] += 1
            # Making sure that the upgrades being removed is random
            # Currently, only for combat shield vs Stabilizer Medpacks...
            shuffled_unit_upgrade_list = list(unit_avail_upgrades.keys())
            self.multiworld.random.shuffle(shuffled_unit_upgrade_list)
            for unit in shuffled_unit_upgrade_list:
                while (unit_nb_upgrades[unit] > maxUpgrad) \
                         and (len(unit_avail_upgrades[unit]) > 0):
                    itemCandidate = self.multiworld.random.choice(unit_avail_upgrades[unit])
                    success = attempt_removal(itemCandidate)
                    # Whatever it succeed to remove the iventory or it fails and thus
                    # lock it, the upgrade is no longer available for removal
                    unit_avail_upgrades[unit].remove(itemCandidate)
                    if success:
                        unit_nb_upgrades[unit] -= 1

        # Locking minimum upgrades for items that have already been locked/placed when minimum required
        if minimum_upgrades > 0:
            known_items = self.existing_items + locked_items
            known_parents = [item for item in known_items if item in parent_items]
            for parent in known_parents:
                child_items = self.item_children[parent]
                removable_upgrades = [item for item in inventory if item in child_items]
                locked_upgrade_count = sum(1 if item in child_items else 0 for item in known_items)
                self.multiworld.random.shuffle(removable_upgrades)
                while len(removable_upgrades) > 0 and locked_upgrade_count < minimum_upgrades:
                    item_to_lock = removable_upgrades.pop()
                    inventory.remove(item_to_lock)
                    locked_items.append(item_to_lock)
                    locked_upgrade_count += 1

        if self.min_units_per_structure > 0 and self.has_units_per_structure():
            requirements.append(lambda state: state.has_units_per_structure())

        # Determining if the full-size inventory can complete campaign
        if not all(requirement(self) for requirement in requirements):
            raise Exception("Too many items excluded - campaign is impossible to complete.")

        # Reserving space for generic items
        generic_item_count = sum(1 if item.name in second_pass_placeable_items else 0 for item in inventory)
        reserved_generic_percent = get_option_value(self.multiworld, self.player, "ensure_generic_items") / 100
        reserved_generic_space = int(generic_item_count * reserved_generic_percent)
        inventory_size -= reserved_generic_space

        # Main cull process
        while len(inventory) + len(locked_items) > inventory_size:
            if len(inventory) == 0:
                # There are more items than locations and all of them are already locked due to YAML or logic.
                # First, transfer reserved space to the inventory
                while reserved_generic_space > 0 and len(locked_items) > inventory_size:
                    reserved_generic_space -= 1
                    inventory_size += 1
                # If there still isn't enough space, push locked items into start inventory
                self.multiworld.random.shuffle(locked_items)
                while len(locked_items) > inventory_size:
                    item: Item = locked_items.pop()
                    self.multiworld.push_precollected(item)
                break
            # Select random item from removable items
            item = self.multiworld.random.choice(inventory)
            # Do not remove item if it would drop upgrades below minimum
            if minimum_upgrades > 0:
                parent_item = parent_lookup.get(item, None)
                if parent_item:
                    count = sum(1 if item in self.item_children[parent_item] else 0 for item in inventory + locked_items)
                    if count <= minimum_upgrades:
                        if parent_item in inventory:
                            # Attempt to remove parent instead, if possible
                            item = parent_item
                        else:
                            # Lock remaining upgrades
                            for item in self.item_children[parent_item]:
                                if item in inventory:
                                    inventory.remove(item)
                                    locked_items.append(item)
                            continue

            # Drop child items when removing a parent
            if item in parent_items:
                items_to_remove = [item for item in self.item_children[item] if item in inventory]
                success = attempt_removal(item)
                if success:
                    while len(items_to_remove) > 0:
                        item_to_remove = items_to_remove.pop()
                        if item_to_remove not in inventory:
                            continue
                        attempt_removal(item_to_remove)
            else:
                attempt_removal(item)

        # Removing extra dependencies
        # WoL
        logical_inventory_set = set(self.logical_inventory)
        if not spider_mine_sources & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Spider Mine)")]
        if not BARRACKS_UNITS & logical_inventory_set:
            inventory = [item for item in inventory if
                         not (item.name.startswith(ItemNames.TERRAN_INFANTRY_UPGRADE_PREFIX) or item.name == ItemNames.ORBITAL_STRIKE)]
        if not FACTORY_UNITS & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.startswith(ItemNames.TERRAN_VEHICLE_UPGRADE_PREFIX)]
        if not STARPORT_UNITS & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.startswith(ItemNames.TERRAN_SHIP_UPGRADE_PREFIX)]
        # HotS
        # Baneling without sources => remove Baneling and upgrades
        if (ItemNames.BANELING in self.logical_inventory
            and ItemNames.ZERGLING not in self.logical_inventory
            and ItemNames.KERRIGAN_SPAWN_BANELINGS not in self.logical_inventory
        ):
            inventory = [item for item in inventory if ItemNames.BANELING not in item.name]
        # Spawn Banelings without Zergling => remove Baneling unit, keep upgrades
        if (ItemNames.BANELING in self.logical_inventory
            and ItemNames.ZERGLING not in self.logical_inventory
            and ItemNames.KERRIGAN_SPAWN_BANELINGS in self.logical_inventory
        ):
            inventory = [item for item in inventory if item.name != ItemNames.BANELING]
        if ItemNames.MUTALISK not in self.logical_inventory:
            inventory = [item for item in inventory if not item.name.startswith(ItemNames.ZERG_FLYER_UPGRADE_PREFIX)]
            locked_items = [item for item in locked_items if not item.name.startswith(ItemNames.ZERG_FLYER_UPGRADE_PREFIX)]

        # Cull finished, adding locked items back into inventory
        inventory += locked_items

        # Replacing empty space with generically useful items
        replacement_items = [item for item in self.item_pool
                             if (item not in inventory
                                 and item not in self.locked_items
                                 and item.name in second_pass_placeable_items)]
        self.multiworld.random.shuffle(replacement_items)
        inventory_size += reserved_generic_space
        while len(inventory) < inventory_size and len(replacement_items) > 0:
            item = replacement_items.pop()
            inventory.append(item)

        return inventory

    def _read_logic(self):
        # General
        self._sc2_cleared_missions = lambda world, player, mission_count: False
        self._sc2_advanced_tactics = lambda world, player: SC2Logic._sc2_advanced_tactics(self, world, player)
        # Terran
        self._sc2wol_has_common_unit = lambda world, player: SC2Logic._sc2wol_has_common_unit(self, world, player)
        self._sc2wol_has_early_tech = lambda world, player: SC2Logic._sc2wol_has_early_tech(self, world, player)
        self._sc2wol_has_air = lambda world, player: SC2Logic._sc2wol_has_air(self, world, player)
        self._sc2wol_has_air_anti_air = lambda world, player: SC2Logic._sc2wol_has_air_anti_air(self, world, player)
        self._sc2wol_has_competent_anti_air = lambda world, player: SC2Logic._sc2wol_has_competent_anti_air(self, world, player)
        self._sc2wol_has_competent_ground_to_air = lambda world, player: SC2Logic._sc2wol_has_competent_ground_to_air(self, world, player)
        self._sc2wol_has_anti_air = lambda world, player: SC2Logic._sc2wol_has_anti_air(self, world, player)
        self._sc2wol_defense_rating = lambda world, player, zerg_enemy, air_enemy=False: SC2Logic._sc2wol_defense_rating(self, world, player, zerg_enemy, air_enemy)
        self._sc2wol_has_competent_comp = lambda world, player: SC2Logic._sc2wol_has_competent_comp(self, world, player)
        self._sc2wol_has_train_killers = lambda world, player: SC2Logic._sc2wol_has_train_killers(self, world, player)
        self._sc2wol_able_to_rescue = lambda world, player: SC2Logic._sc2wol_able_to_rescue(self, world, player)
        self._sc2wol_beats_protoss_deathball = lambda world, player: SC2Logic._sc2wol_beats_protoss_deathball(self, world, player)
        self._sc2wol_survives_rip_field = lambda world, player: SC2Logic._sc2wol_survives_rip_field(self, world, player)
        self._sc2wol_has_sustainable_mech_heal = lambda world, player: SC2Logic._sc2wol_has_sustainable_mech_heal(self, world, player)
        self._sc2wol_has_bio_heal = lambda world, player: SC2Logic._sc2wol_has_bio_heal(self, world, player)
        self._sc2wol_has_competent_base_trasher = lambda world, player: SC2Logic._sc2wol_has_competent_base_trasher(self, world, player)
        self._sc2wol_has_nukes = lambda world, player: SC2Logic._sc2wol_has_nukes(self, world, player)
        self._sc2wol_has_mm_upgrade = lambda world, player: SC2Logic._sc2wol_has_mm_upgrade(self, world, player)
        self._sc2wol_welcome_to_the_jungle_requirement = lambda world, player: SC2Logic._sc2wol_welcome_to_the_jungle_requirement(self, world, player)
        self._sc2wol_can_respond_to_colony_infestations = lambda world, player: SC2Logic._sc2wol_can_respond_to_colony_infestations(self, world, player)
        self._sc2wol_final_mission_requirements = lambda world, player: SC2Logic._sc2wol_final_mission_requirements(self, world, player)
        self._sc2wol_cleared_missions = lambda world, player: SC2Logic._sc2wol_cleared_missions(self, world, player)
        self._sc2wol_essence_of_eternity_comp = lambda world, player: SC2Logic._sc2wol_essence_of_eternity_comp(self, world, player)
        # Zerg
        self._sc2hots_has_common_unit = lambda world, player: SC2Logic._sc2hots_has_common_unit(self, world, player)
        self._sc2hots_has_good_antiair = lambda world, player: SC2Logic._sc2hots_has_good_antiair(self, world, player)
        self._sc2hots_has_minimal_antiair = lambda world, player: SC2Logic._sc2hots_has_minimal_antiair(self, world, player)
        self._sc2hots_has_brood_lord = lambda world, player: SC2Logic._sc2hots_has_brood_lord(self, world, player)
        self._sc2hots_has_viper = lambda world, player: SC2Logic._sc2hots_has_viper(self, world, player)
        self._sc2hots_has_impaler_or_lurker = lambda world, player: SC2Logic._sc2hots_has_impaler_or_lurker(self, world, player)
        self._sc2hots_has_competent_comp = lambda world, player: SC2Logic._sc2hots_has_competent_comp(self, world, player)
        self._sc2hots_can_spread_creep = lambda world, player: SC2Logic._sc2hots_can_spread_creep(self, world, player)
        self._sc2hots_has_competent_defense = lambda world, player: SC2Logic._sc2hots_has_competent_defense(self, world, player)
        self._sc2hots_has_basic_kerrigan = lambda world, player: SC2Logic._sc2hots_has_basic_kerrigan(self, world, player)
        self._sc2hots_has_two_kerrigan_actives = lambda world, player: SC2Logic._sc2hots_has_two_kerrigan_actives(self, world, player)
        self._sc2hots_can_pass_vents = lambda world, player: SC2Logic._sc2hots_can_pass_vents(self, world, player)
        self._sc2hots_can_pass_supreme = lambda world, player: SC2Logic._sc2hots_can_pass_supreme(self, world, player)
        self._sc2hots_final_mission_requirements = lambda world, player: SC2Logic._sc2hots_final_mission_requirements(self, world, player)
        self._sc2hots_amon_s_fall_comp = lambda world, player: SC2Logic._sc2hots_amon_s_fall_comp(self, world, player)
        # Protoss
        self._sc2lotv_has_common_unit = lambda world, player: SC2Logic._sc2lotv_has_common_unit(self, world, player)
        self._sc2lotv_has_competent_anti_air = lambda world, player: SC2Logic._sc2lotv_has_competent_anti_air(self, world, player)
        self._sc2lotv_has_basic_anti_air = lambda world, player: SC2Logic._sc2lotv_has_basic_anti_air(self, world, player)
        self._sc2lotv_has_anti_armor_anti_air = lambda world, player: SC2Logic._sc2lotv_has_anti_armor_anti_air(self, world, player)
        self._sc2lotv_has_anti_light_anti_air = lambda world, player: SC2Logic._sc2lotv_has_anti_light_anti_air(self, world, player)
        self._sc2lotv_can_attack_behind_chasm = lambda world, player: SC2Logic._sc2lotv_can_attack_behind_chasm(self, world, player)
        self._sc2lotv_has_fleet = lambda world, player: SC2Logic._sc2lotv_has_fleet(self, world, player)
        self._sc2lotv_has_templar_return_comp = lambda world, player: SC2Logic._sc2lotv_has_templar_return_comp(self, world, player)
        self._sc2lotv_has_brothers_in_arms_comp = lambda world, player: SC2Logic._sc2lotv_has_brothers_in_arms_comp(self, world, player)
        self._sc2lotv_has_hybrid_counter = lambda world, player: SC2Logic._sc2lotv_has_hybrid_counter(self, world, player)
        self._sc2lotv_the_infinite_cycle_requirements = lambda world, player: SC2Logic._sc2lotv_the_infinite_cycle_requirements(self, world, player)
        self._sc2lotv_has_basic_splash = lambda world, player: SC2Logic._sc2lotv_has_basic_splash(self, world, player)
        self._sc2lotv_has_static_defense = lambda world, player: SC2Logic._sc2lotv_has_static_defense(self, world, player)
        self._sc2lotv_last_stand_requirements = lambda world, player: SC2Logic._sc2lotv_last_stand_requirements(self, world, player)
        self._sc2lotv_harbinger_of_oblivion_requirement = lambda world, player: SC2Logic._sc2lotv_harbinger_of_oblivion_requirement(self, world, player)
        self._sc2lotv_has_competent_comp = lambda world, player: SC2Logic._sc2lotv_has_competent_comp(self, world, player)
        self._sc2lotv_steps_of_the_rite_comp = lambda world, player: SC2Logic._sc2lotv_steps_of_the_rite_comp(self, world, player)
        self._sc2lotv_has_templar_charge_comp = lambda world, player: SC2Logic._sc2lotv_has_templar_charge_comp(self, world, player)
        self._sc2lotv_has_the_host_comp = lambda world, player: SC2Logic._sc2lotv_has_the_host_comp(self, world, player)
        self._sc2lotv_has_heal = lambda world, player: SC2Logic._sc2lotv_has_heal(self, world, player)
        self._sc2lotv_final_mission_requirements = lambda world, player: SC2Logic._sc2lotv_final_mission_requirements(self, world, player)
        self._sc2lotv_into_the_void_comp = lambda world, player: SC2Logic._sc2lotv_into_the_void_comp(self, world, player)

    def __init__(self, multiworld: MultiWorld, player: int,
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item],
                 used_races: Set[SC2Race]):
        self.multiworld = multiworld
        self.player = player
        self.logical_inventory = list()
        self.locked_items = locked_items[:]
        self.existing_items = existing_items
        self._read_logic()
        soa_presence = get_option_value(multiworld, player, "spear_of_adun_presence")
        soa_autocast_presence = get_option_value(multiworld, player, "spear_of_adun_autonomously_cast_ability_presence")
        # Initial filter of item pool
        self.item_pool = []
        item_quantities: dict[str, int] = dict()
        # Inventory restrictiveness based on number of missions with checks
        mission_count = num_missions(multiworld, player)
        self.min_units_per_structure = int(mission_count / 7)
        min_upgrades = 1 if mission_count < 10 else 2
        for item in item_pool:
            item_info = get_full_item_list()[item.name]
            if item_info.race != SC2Race.ANY and item_info.race not in used_races:
                if soa_presence == SpearOfAdunPresence.option_everywhere \
                        and item.name in spear_of_adun_calldowns:
                    # Add SoA powers regardless of used races as it's present everywhere
                    self.item_pool.append(item)
                if soa_autocast_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_everywhere \
                        and item.name in spear_of_adun_castable_passives:
                    self.item_pool.append(item)
                # Drop any item belonging to a race not used in the campaign
                continue
            if item_info.type == "Upgrade":
                # Locking upgrades based on mission duration
                if item.name not in item_quantities:
                    item_quantities[item.name] = 0
                item_quantities[item.name] += 1
                if item_quantities[item.name] <= min_upgrades:
                    self.locked_items.append(item)
                else:
                    self.item_pool.append(item)
            elif item_info.type == "Goal":
                self.locked_items.append(item)
            else:
                self.item_pool.append(item)
        self.item_children: Dict[Item, List[Item]] = dict()
        for item in self.item_pool + locked_items + existing_items:
            if item.name in UPGRADABLE_ITEMS:
                self.item_children[item] = get_item_upgrades(self.item_pool, item)


def filter_items(multiworld: MultiWorld, player: int, mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]], location_cache: List[Location],
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item]) -> List[Item]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    used_races = get_used_races(mission_req_table, multiworld, player)
    mission_requirements = [location.access_rule for location in location_cache]
    valid_inventory = ValidInventory(multiworld, player, item_pool, existing_items, locked_items, used_races)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items


def get_used_races(mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]], multiworld: MultiWorld, player: int) -> Set[SC2Race]:
    grant_story_tech = get_option_value(multiworld, player, "grant_story_tech")
    take_over_ai_allies = get_option_value(multiworld, player, "take_over_ai_allies")
    kerrigan_presence = get_option_value(multiworld, player, "kerrigan_presence")
    missions = missions_in_mission_table(mission_req_table)

    # By missions
    races = set([mission.race for mission in missions])

    # Conditionally logic-less no-builds (They're set to SC2Race.ANY):
    if grant_story_tech == GrantStoryTech.option_false:
        if SC2Mission.ENEMY_WITHIN in missions:
            # Zerg units need to be unlocked
            races.add(SC2Race.ZERG)
        if kerrigan_presence in kerrigan_unit_available \
                and not missions.isdisjoint({SC2Mission.BACK_IN_THE_SADDLE, SC2Mission.SUPREME, SC2Mission.CONVICTION, SC2Mission.THE_INFINITE_CYCLE}):
            # You need some Kerrigan abilities (they're granted if Kerriganless or story tech granted)
            races.add(SC2Race.ZERG)

    # If you take over the AI Ally, you need to have its race stuff
    if take_over_ai_allies == TakeOverAIAllies.option_true \
            and not missions.isdisjoint({SC2Mission.THE_RECKONING}):
        # Jimmy in The Reckoning
        races.add(SC2Race.TERRAN)

    return races


def missions_in_mission_table(mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]]) -> Set[SC2Mission]:
    return set([mission.mission for campaign_missions in mission_req_table.values() for mission in
                campaign_missions.values()])
