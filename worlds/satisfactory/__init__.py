from typing import Dict, List, Set, TextIO, ClassVar, Tuple
from BaseClasses import Item, MultiWorld, ItemClassification, CollectionState
from .GameLogic import GameLogic
from .Items import Items
from .Locations import Locations, LocationData
from .StateLogic import EventId, StateLogic
from .Options import SatisfactoryOptions, Placement
from .Regions import SatisfactoryLocation, create_regions_and_return_locations
from .Web import SatisfactoryWebWorld
from ..AutoWorld import World


class SatisfactoryWorld(World):
    """
    Satisfactory is a first-person open-world factory building game with a dash of exploration and combat.
    Explore an alien planet, create multi-story factories, and enter conveyor belt heaven!
    """

    game = "Satisfactory"
    options_dataclass = SatisfactoryOptions
    options: SatisfactoryOptions
    topology_present = False
    data_version = 0
    web = SatisfactoryWebWorld()

    item_name_to_id = Items.item_names_and_ids
    location_name_to_id = Locations().get_locations_for_data_package()
    item_name_groups = Items.get_item_names_per_category()

    game_logic: ClassVar[GameLogic] = GameLogic()
    state_logic: StateLogic
    items: Items

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.items = None


    def generate_early(self) -> None:
        self.state_logic = StateLogic(self.player, self.options)
        self.items = Items(self.player, self.game_logic, self.random, self.options)

        if not self.options.goal_selection.value:
            raise Exception("""Satisfactory: player {} needs to choose a goal, the option goal_selection is empty"""
                .format(self.multiworld.player_name[self.player]))

        if self.options.mam_logic_placement.value == Placement.starting_inventory:
            self.push_precollected("Building: MAM")
        if self.options.awesome_logic_placement.value == Placement.starting_inventory:
            self.push_precollected("Building: AWESOME Sink")
            self.push_precollected("Building: AWESOME Shop")
        if self.options.energy_link_logic_placement.value == Placement.starting_inventory:
            self.push_precollected("Building: Power Storage")
        if self.options.splitter_placement == Placement.starting_inventory:
            self.push_precollected("Building: Conveyor Splitter")
            self.push_precollected("Building: Conveyor Merger")

        if not self.options.trap_selection_override.value:
            self.options.trap_selection_override.value = self.options.trap_selection_preset.get_selected_list()

        starting_inventory: List[str] = self.options.starting_inventory_preset.get_selected_list()
        for item_name in starting_inventory:
            self.push_precollected(item_name)


    def create_regions(self) -> None:
        locations: List[LocationData] = \
            Locations(self.game_logic, self.options, self.state_logic, self.items).get_locations()
        create_regions_and_return_locations(
            self.multiworld, self.options, self.player, self.game_logic, self.state_logic, locations)


    def create_items(self) -> None:
        self.setup_events()

        number_of_locations: int = len(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.itempool += \
            self.items.build_item_pool(self.random, self.multiworld, self.options, number_of_locations)


    def set_rules(self) -> None:
        resource_sink_goal: bool = "AWESOME Sink Points" in self.options.goal_selection

        last_elevator_tier: int = \
            len(self.game_logic.space_elevator_tiers) if resource_sink_goal \
                else self.options.final_elevator_package.value
        
        required_parts: Set[str] = set(self.game_logic.space_elevator_tiers[last_elevator_tier - 1].keys())

        if resource_sink_goal:
            required_parts.union(self.game_logic.buildings["AWESOME Sink"].inputs)

        required_parts_tuple: Tuple[str, ...] = tuple(required_parts)

        self.multiworld.completion_condition[self.player] = \
            lambda state: self.state_logic.can_produce_all(state, required_parts_tuple)


    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change and item.name == "Recipe: Quartz Purification":
            state.prog_items[self.player]["Recipe: Distilled Silica"] = 1
        return change


    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change and item.name == "Recipe: Quartz Purification":
            del state.prog_items[self.player]["Recipe: Distilled Silica"]
        return change


    def fill_slot_data(self) -> Dict[str, object]:
        slot_hub_layout: List[List[Dict[str, int]]] = []

        for tier, milestones in enumerate(self.game_logic.hub_layout, 1):
            slot_hub_layout.append([])
            for milestone, parts in enumerate(milestones, 1):
                 slot_hub_layout[tier - 1].append({})
                 for part, amount in parts.items():
                    # ItemIDs of bundles are shared with their component item
                    bundled_name = f"Bundle: {part}"
                    slot_hub_layout[tier - 1][milestone - 1][self.item_name_to_id[bundled_name]] = amount

        return {
            "Data": {
                "HubLayout": slot_hub_layout,
                "SlotsPerMilestone": self.game_logic.slots_per_milestone,
                "Options": {
                    "GoalSelection": self.options.goal_selection.value,
                    "GoalRequirement": self.options.goal_requirement.value,
                    "FinalElevatorTier": self.options.final_elevator_package.value,
                    "FinalResourceSinkPoints": self.options.final_awesome_sink_points.value,
                    "EnableHardDriveGacha": True if self.options.hard_drive_progression_limit else False,
                    "FreeSampleEquipment": self.options.free_sample_equipment.value,
                    "FreeSampleBuildings": self.options.free_sample_buildings.value,
                    "FreeSampleParts": self.options.free_sample_parts.value,
                    "FreeSampleRadioactive": bool(self.options.free_sample_radioactive),
                    "EnergyLink": bool(self.options.energy_link)
                }
            },
            "DeathLink": bool(self.options.death_link)
        }


    def write_spoiler(self, spoiler_handle: TextIO):
        self.items.write_progression_chain(self.multiworld, spoiler_handle)


    def get_filler_item_name(self) -> str:
        return self.items.get_filler_item_name(self.random, self.options)


    def setup_events(self):
        location: SatisfactoryLocation
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item_name = location.event_name

                item = Item(item_name, ItemClassification.progression, EventId, self.player)

                location.place_locked_item(item)
                location.show_in_spoiler = False


    def create_item(self, name: str) -> Item:
        return Items.create_item(self.items, name, self.player)


    def push_precollected(self, item_name: str) -> None:
        item = self.create_item(item_name)
        self.multiworld.push_precollected(item)
