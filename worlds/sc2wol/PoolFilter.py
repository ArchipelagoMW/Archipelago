from BaseClasses import MultiWorld, Item, ItemClassification
from .Items import item_table
from .MissionTables import no_build_regions_list, easy_regions_list, medium_regions_list, hard_regions_list, vanilla_mission_req_table, starting_mission_locations
from .Options import get_option_value
from .LogicMixin import SC2WoLLogic

# Items with associated upgrades
UPGRADABLE_ITEMS = [
    "Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre",
    "Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor",
    "Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser",
    "Bunker", "Missile Turret"
]

BARRACKS_UNITS = {"Marine", "Medic", "Firebat", "Marauder", "Reaper", "Ghost", "Spectre"}
FACTORY_UNITS = {"Hellion", "Vulture", "Goliath", "Diamondback", "Siege Tank", "Thor", "Predator"}
STARPORT_UNITS = {"Medivac", "Wraith", "Viking", "Banshee", "Battlecruiser", "Hercules", "Science Vessel", "Raven"}
MIN_UNITS_PER_STRUCTURE = [
    3,   # Vanilla
    3,   # Vanilla Shuffled
    2,   # Mini Shuffle
    0    # Gauntlet
]

PROTOSS_REGIONS = ["A Sinister Turn", "Echoes of the Future", "In Utter Darkness"]

UPGRADES = [
    "Progressive Infantry Weapon", "Progressive Infantry Armor",
    "Progressive Vehicle Weapon", "Progressive Vehicle Armor",
    "Progressive Ship Weapon", "Progressive Ship Armor"
]


def filter_missions(world: MultiWorld, player: int) -> set[str]:
    """
    Returns a semi-randomly pruned set of missions based on yaml configuration
    """
    missions = set(vanilla_mission_req_table.keys())
    mission_order = get_option_value(world, player, "mission_order")
    shuffle_protoss = get_option_value(world, player, "shuffle_protoss")
    relegate_no_build = get_option_value(world, player, "relegate_no_build")

    # Vanilla and Vanilla Shuffled use the entire mission pool
    if mission_order not in (2, 3):
        return missions

    if mission_order == 2:
        mission_count = 15
    else:
        mission_count = 7
    mission_sets = [
        set(no_build_regions_list),
        set(easy_regions_list),
        set(medium_regions_list),
        set(hard_regions_list)
    ]
    # Omitting Protoss missions if not shuffling protoss
    if not shuffle_protoss:
        missions.difference_update(PROTOSS_REGIONS)
        for mission_set in mission_sets:
            mission_set.difference_update(PROTOSS_REGIONS)
    # Omitting No Build missions if relegating no-build
    if relegate_no_build:
        missions.difference_update(no_build_regions_list)
        # The build missions in starting_mission_locations become the new "no build missions"
        mission_sets[0] = set(starting_mission_locations.keys())
        mission_sets[0].difference_update(no_build_regions_list)
        # Future-proofing in case a non-Easy mission is placed in starting_mission_locations
        for mission_set in mission_sets[1:]:
            mission_set.difference_update(mission_sets[0])
    # Removing random missions from each difficulty set in a cycle
    set_cycle = 0
    while len(missions) > mission_count:
        if set_cycle == 4:
            set_cycle = 0
        # Must contain at least one mission per set
        if len(mission_sets[set_cycle]) == 1:
            continue
        removed_mission = world.random.choice(mission_sets[set_cycle])
        mission_sets[set_cycle].remove(removed_mission)
        missions.remove(removed_mission)
        set_cycle += 1
    return missions


class ValidInventory(SC2WoLLogic):

    def has(self, item: str, player: int = 0):
        return item in self.logical_inventory

    def has_any(self, items: set[str], player: int = 0):
        return any([item in self.logical_inventory for item in items])

    # Necessary for Piercing the Shroud
    def _sc2wol_has_mm_upgrade(self, world: MultiWorld, player: int):
        return self.has_any({"Combat Shield (Marine)", "Stabilizer Medpacks (Medic)"}, player)

    # Necessary for Maw of the Void
    def _sc2wol_survives_rip_field(self, world: MultiWorld, player: int):
        return self.has("Battlecruiser", player) or \
           self._sc2wol_has_air(world, player) and \
           self._sc2wol_has_competent_anti_air(world, player) and \
           self.has("Science Vessel", player)

    def _sc2wol_has_units_per_structure(self, world: MultiWorld, player: int):
        return len(BARRACKS_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
               len(FACTORY_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure and \
               len(STARPORT_UNITS.intersection(self.logical_inventory)) > self.min_units_per_structure

    def generate_reduced_inventory(self, number_of_locations: int):
        inventory = set(self.inventory)
        locked_items = list(self.locked_items)
        self.logical_inventory = set(self.progression_items)
        while len(inventory) + len(locked_items) > number_of_locations:
            if len(inventory) == 0:
                raise Exception('Reduced item pool generation failed.')
            # Select random item from removable items
            item = self.world.random.choice(inventory)
            inventory.remove(item)
            # Only run logic checks when removing logic items
            if item in self.logical_inventory:
                self.logical_inventory.remove(item)
                if not all(self.requirements):
                    # If item cannot be removed, move it to locked items
                    self.logical_inventory.add(item)
                    locked_items.add(item)
                else:
                    # If item can be removed and is a unit, remove armory upgrades
                    if item in UPGRADABLE_ITEMS:
                        inventory = [inv_item for inv_item in inventory if not inv_item.endswith('(' + item + ')')]
        return list(inventory) + locked_items

    def __init__(self, world: MultiWorld, player: int, locked_items: list[str]):
        self.world = world
        mission_order = get_option_value(world, player, "mission_order")
        self.min_units_per_structure = MIN_UNITS_PER_STRUCTURE[mission_order]
        self.locked_items = locked_items
        self.inventory = set(item_table.keys())
        protoss_items = set()
        # Scanning item table
        self.logical_inventory = set()
        self.progression_items = set()
        for item_name, item in item_table.items():
            if item.classification == ItemClassification.progression:
                self.progression_items.add(item_name)
            elif item.type in ("Minerals", "Vespene", "Supply"):
                self.inventory.remove(item_name)
            if item.type == "Protoss":
                protoss_items.add(item_name)
        self.requirements = [
            self._sc2wol_has_common_unit,
            self._sc2wol_has_air,
            self._sc2wol_has_competent_anti_air,
            self._sc2wol_has_heavy_defense,
            self._sc2wol_has_competent_comp,
            self._sc2wol_has_train_killers,
            self._sc2wol_able_to_rescue,
            self._sc2wol_beats_protoss_deathball,
            self._sc2wol_survives_rip_field
        ]
        # Only include units per structure requirement if more than 0
        if self.min_units_per_structure > 0:
            self.requirements.append(self._sc2wol_has_units_per_structure)
        # Only include Marine/Medic upgrade requirements if no-build missions are present
        if mission_order in (1, 2) or get_option_value(world, player, "relegate_no_build"):
            self.requirements.append(self._has_mm_upgrade)
        # Only include protoss requirements if protoss missions are present
        if mission_order in (1, 2) or get_option_value(world, player, "shuffle_protoss"):
            self.requirements += [
                self._sc2wol_has_protoss_common_units,
                self._sc2wol_has_protoss_medium_units
            ]
        else:
            # Remove protoss items if protoss missions are not present
            self.locked_items = [item for item in self.locked_items if item not in protoss_items]
            self.inventory = [item for item in self.inventory if item not in protoss_items]
        # 2 tiers of each upgrade are guaranteed
        self.locked_items += 2 * UPGRADES
        self.inventory.difference_update(locked_items)
        # 1 tier of each upgrade can be potentially removed
        self.inventory += UPGRADES


def filter_items(world: MultiWorld, player: int, regions: set[str], locked_items: list[str] = []) -> list[str]:
    """
    Returns a semi-randomly pruned set of items based on number of available locations.
    The returned inventory must be capable of logically accessing every location in the world.
    """
    valid_inventory = ValidInventory(world, player, locked_items)
    number_of_locations = sum([
        info.extra_locations for name, info in vanilla_mission_req_table.items() if name in regions
    ])
    return valid_inventory.generate_reduced_inventory(number_of_locations)