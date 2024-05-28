from typing import Callable, Dict, List, Set, Union, Tuple, Optional, TYPE_CHECKING
from BaseClasses import  Item, Location
from .items import (get_full_item_list, spider_mine_sources, second_pass_placeable_items,
    upgrade_item_types,
)
from .mission_tables import (MissionInfo, MissionPools,
    get_campaign_goal_priority, campaign_final_mission_locations, campaign_alt_final_mission_locations,
    SC2Campaign, SC2CampaignGoalPriority, SC2Mission,
)
from .options import (get_option_value, MissionOrder,
    get_enabled_campaigns, RequiredTactics, kerrigan_unit_available, GrantStoryTech,
    TakeOverAIAllies, campaign_depending_orders,
    ShuffleCampaigns, get_excluded_missions, ShuffleNoBuild, ExtraLocations, GrantStoryLevels, EnableMorphling,
    static_mission_orders, dynamic_mission_orders
)
from . import item_groups, item_names

if TYPE_CHECKING:
    from . import SC2World


# Items with associated upgrades
UPGRADABLE_ITEMS = {item.parent_item for item in get_full_item_list().values() if item.parent_item}
BARRACKS_UNITS = set(item_groups.barracks_units)
FACTORY_UNITS = set(item_groups.factory_units)
STARPORT_UNITS = set(item_groups.starport_units)


def filter_missions(world: 'SC2World') -> Dict[MissionPools, List[SC2Mission]]:

    """
    Returns a semi-randomly pruned tuple of no-build, easy, medium, and hard mission sets
    """
    mission_order_type = get_option_value(world, "mission_order")
    shuffle_no_build = get_option_value(world, "shuffle_no_build")
    enabled_campaigns = get_enabled_campaigns(world)
    grant_story_tech = get_option_value(world, "grant_story_tech") == GrantStoryTech.option_true
    grant_story_levels = get_option_value(world, "grant_story_levels") != GrantStoryLevels.option_disabled
    extra_locations = get_option_value(world, "extra_locations")
    excluded_missions: Set[SC2Mission] = get_excluded_missions(world)
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
        candidate_campaigns: List[SC2Campaign] = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
        candidate_campaigns.sort(key=lambda it: it.id)
        goal_campaign = world.random.choice(candidate_campaigns)
        if campaign_final_mission_locations[goal_campaign] is not None:
            mission_pools[MissionPools.FINAL] = [campaign_final_mission_locations[goal_campaign].mission]
        else:
            mission_pools[MissionPools.FINAL] = [list(campaign_alt_final_mission_locations[goal_campaign].keys())[0]]
        remove_final_mission_from_other_pools(mission_pools)
        return mission_pools

    # Finding the goal map
    goal_mission: Optional[SC2Mission] = None
    if mission_order_type in campaign_depending_orders:
        # Prefer long campaigns over shorter ones and harder missions over easier ones
        goal_priorities = {campaign: get_campaign_goal_priority(campaign, excluded_missions) for campaign in enabled_campaigns}
        goal_level = max(goal_priorities.values())
        candidate_campaigns: List[SC2Campaign] = [campaign for campaign, goal_priority in goal_priorities.items() if goal_priority == goal_level]
        candidate_campaigns.sort(key=lambda it: it.id)

        goal_campaign = world.random.choice(candidate_campaigns)
        primary_goal = campaign_final_mission_locations[goal_campaign]
        if primary_goal is None or primary_goal.mission in excluded_missions:
            # No primary goal or its mission is excluded
            candidate_missions = list(campaign_alt_final_mission_locations[goal_campaign].keys())
            candidate_missions = [mission for mission in candidate_missions if mission not in excluded_missions]
            if len(candidate_missions) == 0:
                raise Exception("There are no valid goal missions. Please exclude fewer missions.")
            goal_mission = world.random.choice(candidate_missions)
        else:
            goal_mission = primary_goal.mission
    else:
        # Find one of the missions with the hardest difficulty
        available_missions: List[SC2Mission] = \
            [mission for mission in SC2Mission
             if (mission not in excluded_missions and mission.campaign in enabled_campaigns)]
        available_missions.sort(key=lambda it: it.id)
        # Loop over pools, from hardest to easiest
        for mission_pool in range(MissionPools.VERY_HARD, MissionPools.STARTER - 1, -1):
            pool_missions: List[SC2Mission] = [mission for mission in available_missions if mission.pool == mission_pool]
            if pool_missions:
                goal_mission = world.random.choice(pool_missions)
                break
    if goal_mission is None:
        raise Exception("There are no valid goal missions. Please exclude fewer missions.")

    # Excluding missions
    for difficulty, mission_pool in mission_pools.items():
        mission_pools[difficulty] = [mission for mission in mission_pool if mission not in excluded_missions]
    mission_pools[MissionPools.FINAL] = [goal_mission]

    # Mission pool changes
    adv_tactics = get_option_value(world, "required_tactics") != RequiredTactics.option_standard

    def move_mission(mission: SC2Mission, current_pool, new_pool):
        if mission in mission_pools[current_pool]:
            mission_pools[current_pool].remove(mission)
            mission_pools[new_pool].append(mission)
    # WoL
    if shuffle_no_build == ShuffleNoBuild.option_false or adv_tactics:
        # Replacing No Build missions with Easy missions
        # WoL
        move_mission(SC2Mission.ZERO_HOUR, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.EVACUATION, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.DEVILS_PLAYGROUND, MissionPools.EASY, MissionPools.STARTER)
        # LotV
        move_mission(SC2Mission.THE_GROWING_SHADOW, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.THE_SPEAR_OF_ADUN, MissionPools.EASY, MissionPools.STARTER)
        if extra_locations == ExtraLocations.option_enabled:
            move_mission(SC2Mission.SKY_SHIELD, MissionPools.EASY, MissionPools.STARTER)
        # Pushing this to Easy
        move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, MissionPools.MEDIUM, MissionPools.EASY)
        if shuffle_no_build == ShuffleNoBuild.option_false:
            # Pushing Outbreak to Normal, as it cannot be placed as the second mission on Build-Only
            move_mission(SC2Mission.OUTBREAK, MissionPools.EASY, MissionPools.MEDIUM)
            # Pushing extra Normal missions to Easy
            move_mission(SC2Mission.ECHOES_OF_THE_FUTURE, MissionPools.MEDIUM, MissionPools.EASY)
            move_mission(SC2Mission.CUTTHROAT, MissionPools.MEDIUM, MissionPools.EASY)
        # Additional changes on Advanced Tactics
        if adv_tactics:
            # WoL
            move_mission(SC2Mission.THE_GREAT_TRAIN_ROBBERY, MissionPools.EASY, MissionPools.STARTER)
            move_mission(SC2Mission.SMASH_AND_GRAB, MissionPools.EASY, MissionPools.STARTER)
            move_mission(SC2Mission.THE_MOEBIUS_FACTOR, MissionPools.MEDIUM, MissionPools.EASY)
            move_mission(SC2Mission.WELCOME_TO_THE_JUNGLE, MissionPools.MEDIUM, MissionPools.EASY)
            move_mission(SC2Mission.ENGINE_OF_DESTRUCTION, MissionPools.HARD, MissionPools.MEDIUM)
            # LotV
            move_mission(SC2Mission.AMON_S_REACH, MissionPools.EASY, MissionPools.STARTER)
    # Prophecy needs to be adjusted on tiny grid
    if enabled_campaigns == {SC2Campaign.PROPHECY} and mission_order_type == MissionOrder.option_tiny_grid:
        move_mission(SC2Mission.A_SINISTER_TURN, MissionPools.MEDIUM, MissionPools.EASY)
    # Prologue's only valid starter is the goal mission
    if enabled_campaigns == {SC2Campaign.PROLOGUE} \
            or mission_order_type in campaign_depending_orders \
            and get_option_value(world, "shuffle_campaigns") == ShuffleCampaigns.option_false:
        move_mission(SC2Mission.DARK_WHISPERS, MissionPools.EASY, MissionPools.STARTER)
    # HotS
    kerriganless = get_option_value(world, "kerrigan_presence") not in kerrigan_unit_available \
        or SC2Campaign.HOTS not in enabled_campaigns
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
        move_mission(SC2Mission.THE_ESCAPE, MissionPools.MEDIUM, MissionPools.STARTER)
        move_mission(SC2Mission.IN_THE_ENEMY_S_SHADOW, MissionPools.MEDIUM, MissionPools.STARTER)
    if (grant_story_tech and grant_story_levels) or kerriganless:
        # The player has, all the stuff he needs, provided under these settings
        move_mission(SC2Mission.SUPREME, MissionPools.MEDIUM, MissionPools.STARTER)
        move_mission(SC2Mission.THE_INFINITE_CYCLE, MissionPools.HARD, MissionPools.STARTER)
    if get_option_value(world, "take_over_ai_allies") == TakeOverAIAllies.option_true:
        move_mission(SC2Mission.HARBINGER_OF_OBLIVION, MissionPools.MEDIUM, MissionPools.STARTER)
    if len(mission_pools[MissionPools.STARTER]) < 2 and not kerriganless or adv_tactics:
        # Conditionally moving Easy missions to Starter
        move_mission(SC2Mission.HARVEST_OF_SCREAMS, MissionPools.EASY, MissionPools.STARTER)
        move_mission(SC2Mission.DOMINATION, MissionPools.EASY, MissionPools.STARTER)
    if len(mission_pools[MissionPools.STARTER]) < 2:
        move_mission(SC2Mission.TEMPLAR_S_RETURN, MissionPools.EASY, MissionPools.STARTER)
    if len(mission_pools[MissionPools.STARTER]) + len(mission_pools[MissionPools.EASY]) < 2:
        # Flashpoint needs just a few items at start but competent comp at the end
        move_mission(SC2Mission.FLASHPOINT, MissionPools.HARD, MissionPools.EASY)

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


def copy_item(item: Item):
    return Item(item.name, item.classification, item.code, item.player)


class ValidInventory:

    def has(self, item: str, player: int):
        return item in self.logical_inventory

    def has_any(self, items: Set[str], player: int):
        return any(item in self.logical_inventory for item in items)

    def has_all(self, items: Set[str], player: int):
        return all(item in self.logical_inventory for item in items)

    def has_group(self, item_group: str, player: int, count: int = 1):
        return False  # Deliberately fails here, as item pooling is not aware about mission layout

    def count_group(self, item_name_group: str, player: int) -> int:
        return 0  # For item filtering assume no missions are beaten

    def count(self, item: str, player: int) -> int:
        return len([inventory_item for inventory_item in self.logical_inventory if inventory_item == item])

    def has_units_per_structure(self) -> bool:
        return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(FACTORY_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
            len(STARPORT_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure

    def generate_reduced_inventory(self, inventory_size: int, mission_requirements: List[Tuple[str, Callable]]) -> List[Item]:
        """Attempts to generate a reduced inventory that can fulfill the mission requirements."""
        inventory: List[Item] = list(self.item_pool)
        locked_items: List[Item] = list(self.locked_items)
        enable_morphling = self.world.options.enable_morphling == EnableMorphling.option_true
        item_list = get_full_item_list()
        self.logical_inventory = [
            item.name for item in inventory + locked_items + self.existing_items
            if item_list[item.name].is_important_for_filtering()  # Track all Progression items and those with complex rules for filtering
        ]
        requirements = mission_requirements
        parent_items = self.item_children.keys()
        parent_lookup = {child: parent for parent, children in self.item_children.items() for child in children}
        minimum_upgrades = get_option_value(self.world, "min_number_of_upgrades")

        def attempt_removal(item: Item) -> bool:
            removed_item = inventory.pop(inventory.index(item))
            # Only run logic checks when removing logic items
            if item.name in self.logical_inventory:
                self.logical_inventory.remove(item.name)
                if not all(requirement(self) for (_, requirement) in mission_requirements):
                    # If item cannot be removed, lock or revert
                    self.logical_inventory.append(item.name)
                    # Note(mm): Be sure to re-add the _exact_ item we removed.
                    # Removing from `inventory` searches based on == checks, but AutoWorld.py
                    # checks using `is` to make sure there are no duplicate item objects in the pool.
                    # Hence, appending `item` could cause sporadic generation failures.
                    locked_items.append(removed_item)
                    return False
            return True

        # Limit the maximum number of upgrades
        maxNbUpgrade = get_option_value(self.world, "max_number_of_upgrades")
        if maxNbUpgrade != -1:
            unit_avail_upgrades = {}
            # Needed to take into account locked/existing items
            unit_nb_upgrades = {}
            for item in inventory:
                cItem = item_list[item.name]
                if item.name in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
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
                if item.name in UPGRADABLE_ITEMS and item.name not in unit_avail_upgrades:
                    unit_avail_upgrades[item.name] = []
                    unit_nb_upgrades[item.name] = 0
                elif cItem.parent_item is not None:
                    if cItem.parent_item not in unit_avail_upgrades:
                        unit_nb_upgrades[cItem.parent_item] = 1
                    else:
                        unit_nb_upgrades[cItem.parent_item] += 1
            # Making sure that the upgrades being removed is random
            shuffled_unit_upgrade_list = list(unit_avail_upgrades.keys())
            self.world.random.shuffle(shuffled_unit_upgrade_list)
            for unit in shuffled_unit_upgrade_list:
                while (unit_nb_upgrades[unit] > maxNbUpgrade) \
                         and (len(unit_avail_upgrades[unit]) > 0):
                    itemCandidate = self.world.random.choice(unit_avail_upgrades[unit])
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
                self.world.random.shuffle(removable_upgrades)
                while len(removable_upgrades) > 0 and locked_upgrade_count < minimum_upgrades:
                    item_to_lock = removable_upgrades.pop()
                    inventory.remove(item_to_lock)
                    locked_items.append(copy_item(item_to_lock))
                    locked_upgrade_count += 1

        if self.min_units_per_structure > 0 and self.has_units_per_structure():
            requirements.append(("Minimum units per structure", lambda state: state.has_units_per_structure()))

        # Determining if the full-size inventory can complete campaign
        failed_locations: List[str] = [location for (location, requirement) in requirements if not requirement(self)]
        if len(failed_locations) > 0:
            raise Exception(f"Too many items excluded - couldn't satisfy access rules for the following locations:\n{failed_locations}")

        # Optionally locking generic items
        generic_items = [item for item in inventory if item.name in second_pass_placeable_items]
        reserved_generic_percent = get_option_value(self.world, "ensure_generic_items") / 100
        reserved_generic_amount = int(len(generic_items) * reserved_generic_percent)
        removable_generic_items = []
        self.world.random.shuffle(generic_items)
        for item in generic_items[:reserved_generic_amount]:
            locked_items.append(copy_item(item))
            inventory.remove(item)
            if item.name not in self.logical_inventory and item.name not in self.locked_items:
                removable_generic_items.append(item)

        # Main cull process
        unused_items: List[str] = []  # Reusable items for the second pass
        while len(inventory) + len(locked_items) > inventory_size:
            if len(inventory) == 0:
                # There are more items than locations and all of them are already locked due to YAML or logic.
                # First, drop non-logic generic items to free up space
                while len(removable_generic_items) > 0 and len(locked_items) > inventory_size:
                    removed_item = removable_generic_items.pop()
                    locked_items.remove(removed_item)
                # If there still isn't enough space, push locked items into start inventory
                self.world.random.shuffle(locked_items)
                while len(locked_items) > inventory_size:
                    item: Item = locked_items.pop()
                    self.multiworld.push_precollected(item)
                break
            # Select random item from removable items
            item = self.world.random.choice(inventory)
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
                                    locked_items.append(copy_item(item))
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
                # Unimportant upgrades may be added again in the second pass
                if attempt_removal(item):
                    unused_items.append(item.name)

        pool_items: List[str] = [item.name for item in (inventory + locked_items + self.existing_items)]
        unused_items = [
            unused_item for unused_item in unused_items
            if item_list[unused_item].parent_item is None
               or item_list[unused_item].parent_item in pool_items
        ]

        # Removing extra dependencies
        # WoL
        logical_inventory_set = set(self.logical_inventory)
        if not spider_mine_sources & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Spider Mine)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Spider Mine)")]
        if not BARRACKS_UNITS & logical_inventory_set:
            inventory = [
                item for item in inventory
                if not (item.name.startswith(item_names.TERRAN_INFANTRY_UPGRADE_PREFIX)
                        or item.name == item_names.ORBITAL_STRIKE)]
            unused_items = [
                item_name for item_name in unused_items
                if not (item_name.startswith(
                    item_names.TERRAN_INFANTRY_UPGRADE_PREFIX)
                        or item_name == item_names.ORBITAL_STRIKE)]
        if not FACTORY_UNITS & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.startswith(item_names.TERRAN_VEHICLE_UPGRADE_PREFIX)]
            unused_items = [item_name for item_name in unused_items if not item_name.startswith(item_names.TERRAN_VEHICLE_UPGRADE_PREFIX)]
        if not STARPORT_UNITS & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.startswith(item_names.TERRAN_SHIP_UPGRADE_PREFIX)]
            unused_items = [item_name for item_name in unused_items if not item_name.startswith(item_names.TERRAN_SHIP_UPGRADE_PREFIX)]
        # HotS
        # Baneling without sources => remove Baneling and upgrades
        if (item_names.ZERGLING_BANELING_ASPECT in self.logical_inventory
                and item_names.ZERGLING not in self.logical_inventory
                and item_names.KERRIGAN_SPAWN_BANELINGS not in self.logical_inventory
                and not enable_morphling
        ):
            inventory = [item for item in inventory if item.name != item_names.ZERGLING_BANELING_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.ZERGLING_BANELING_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.ZERGLING_BANELING_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.ZERGLING_BANELING_ASPECT]
        # Spawn Banelings without Zergling/Morphling => remove Baneling unit, keep upgrades except macro ones
        if (item_names.ZERGLING_BANELING_ASPECT in self.logical_inventory
            and item_names.ZERGLING not in self.logical_inventory
            and item_names.KERRIGAN_SPAWN_BANELINGS in self.logical_inventory
            and not enable_morphling
        ):
            inventory = [item for item in inventory if item.name != item_names.ZERGLING_BANELING_ASPECT]
            inventory = [item for item in inventory if item.name != item_names.BANELING_RAPID_METAMORPH]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.ZERGLING_BANELING_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.BANELING_RAPID_METAMORPH]
        if not {item_names.MUTALISK, item_names.CORRUPTOR, item_names.SCOURGE} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.startswith(item_names.ZERG_FLYER_UPGRADE_PREFIX)]
            locked_items = [item for item in locked_items if not item.name.startswith(item_names.ZERG_FLYER_UPGRADE_PREFIX)]
            unused_items = [item_name for item_name in unused_items if not item_name.startswith(item_names.ZERG_FLYER_UPGRADE_PREFIX)]
        # T3 items removal rules - remove morph and its upgrades if the basic unit isn't in and morphling is unavailable
        if not {item_names.MUTALISK, item_names.CORRUPTOR} & logical_inventory_set and not enable_morphling:
            inventory = [item for item in inventory if not item.name.endswith("(Mutalisk/Corruptor)")]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Mutalisk/Corruptor)")]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT]
        if item_names.ROACH not in logical_inventory_set and not enable_morphling:
            inventory = [item for item in inventory if item.name != item_names.ROACH_RAVAGER_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.ROACH_RAVAGER_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.ROACH_RAVAGER_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.ROACH_RAVAGER_ASPECT]
        if item_names.HYDRALISK not in logical_inventory_set and not enable_morphling:
            inventory = [item for item in inventory if not item.name.endswith("(Hydralisk)")]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.HYDRALISK_LURKER_ASPECT]
            inventory = [item for item in inventory if item_list[item.name].parent_item != item_names.HYDRALISK_IMPALER_ASPECT]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Hydralisk)")]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.HYDRALISK_LURKER_ASPECT]
            unused_items = [item_name for item_name in unused_items if item_list[item_name].parent_item != item_names.HYDRALISK_IMPALER_ASPECT]
        # LotV
        # Shared unit upgrades between several units
        if not {item_names.STALKER, item_names.INSTIGATOR, item_names.SLAYER} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Stalker/Instigator/Slayer)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Stalker/Instigator/Slayer)")]
        if not {item_names.PHOENIX, item_names.MIRAGE} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Phoenix/Mirage)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Phoenix/Mirage)")]
        if not {item_names.VOID_RAY, item_names.DESTROYER} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Void Ray/Destroyer)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Void Ray/Destroyer)")]
        if not {item_names.IMMORTAL, item_names.ANNIHILATOR} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Immortal/Annihilator)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Immortal/Annihilator)")]
        if not {item_names.DARK_TEMPLAR, item_names.AVENGER, item_names.BLOOD_HUNTER} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Dark Templar/Avenger/Blood Hunter)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Dark Templar/Avenger/Blood Hunter)")]
        if not {item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT, item_names.DARK_TEMPLAR} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Archon)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Archon)")]
            logical_inventory_set.difference_update([item_name for item_name in logical_inventory_set if item_name.endswith("(Archon)")])
        if not {item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ARCHON_HIGH_ARCHON} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(High Templar/Signifier)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(High Templar/Signifier)")]
        if item_names.SUPPLICANT not in logical_inventory_set:
            inventory = [item for item in inventory if item.name != item_names.ASCENDANT_POWER_OVERWHELMING]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.ASCENDANT_POWER_OVERWHELMING]
        if not {item_names.DARK_ARCHON, item_names.DARK_TEMPLAR_DARK_ARCHON_MELD} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Dark Archon)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Dark Archon)")]
        if not {item_names.SENTRY, item_names.ENERGIZER, item_names.HAVOC} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Sentry/Energizer/Havoc)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Sentry/Energizer/Havoc)")]
        if not {item_names.SENTRY, item_names.ENERGIZER, item_names.HAVOC, item_names.SHIELD_BATTERY} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Sentry/Energizer/Havoc/Shield Battery)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Sentry/Energizer/Havoc/Shield Battery)")]
        if not {item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL} & logical_inventory_set:
            inventory = [item for item in inventory if not item.name.endswith("(Zealot/Sentinel/Centurion)")]
            unused_items = [item_name for item_name in unused_items if not item_name.endswith("(Zealot/Sentinel/Centurion)")]
        # Static defense upgrades only if static defense present
        if not {item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH, item_names.NEXUS_OVERCHARGE, item_names.SHIELD_BATTERY} & logical_inventory_set:
            inventory = [item for item in inventory if item.name != item_names.ENHANCED_TARGETING]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.ENHANCED_TARGETING]
        if not {item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH, item_names.NEXUS_OVERCHARGE} & logical_inventory_set:
            inventory = [item for item in inventory if item.name != item_names.OPTIMIZED_ORDNANCE]
            unused_items = [item_name for item_name in unused_items if item_name != item_names.OPTIMIZED_ORDNANCE]

        # Cull finished, adding locked items back into inventory
        inventory += locked_items

        # Replacing empty space with generically useful items
        replacement_items = [item for item in self.item_pool
                             if (item not in inventory
                                 and item not in self.locked_items
                                 and (
                                     item.name in second_pass_placeable_items
                                     or item.name in unused_items))]
        self.world.random.shuffle(replacement_items)
        while len(inventory) < inventory_size and len(replacement_items) > 0:
            item = replacement_items.pop()
            inventory.append(item)

        return inventory

    def __init__(self, world: 'SC2World',
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item],
    ):
        self.multiworld = world.multiworld
        self.player = world.player
        self.world: 'SC2World' = world
        self.logical_inventory = list()
        self.locked_items = locked_items[:]
        self.existing_items = existing_items
        # Initial filter of item pool
        self.item_pool = []
        item_quantities: dict[str, int] = dict()
        # Inventory restrictiveness based on number of missions with checks
        # mission_count = sum(len(campaign) for campaign in world.mission_req_table.values())
        mission_count = len(world.custom_mission_order.get_used_missions())
        self.min_units_per_structure = int(mission_count / 7)
        min_upgrades = 1 if mission_count < 10 else 2
        for item in item_pool:
            item_info = get_full_item_list()[item.name]
            if item_info.type in upgrade_item_types:
                # Locking upgrades based on mission duration
                if item.name not in item_quantities:
                    item_quantities[item.name] = 0
                item_quantities[item.name] += 1
                if item_quantities[item.name] <= min_upgrades:
                    self.locked_items.append(item)
                else:
                    self.item_pool.append(item)
            else:
                self.item_pool.append(item)
        self.item_children: Dict[Item, List[Item]] = dict()
        for item in self.item_pool + locked_items + existing_items:
            if item.name in UPGRADABLE_ITEMS:
                self.item_children[item] = get_item_upgrades(self.item_pool, item)


def filter_items(world: 'SC2World', location_cache: List[Location],
                 item_pool: List[Item], existing_items: List[Item], locked_items: List[Item]) -> List[Item]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    open_locations = [location for location in location_cache if location.item is None]
    inventory_size = len(open_locations)
    mission_requirements = [(location.name, location.access_rule) for location in location_cache]
    valid_inventory = ValidInventory(world, item_pool, existing_items, locked_items)

    valid_items = valid_inventory.generate_reduced_inventory(inventory_size, mission_requirements)
    return valid_items


def missions_in_mission_table(mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]]) -> Set[SC2Mission]:
    return set([mission.mission for campaign_missions in mission_req_table.values() for mission in
                campaign_missions.values()])
