from typing import TextIO, ClassVar, Any
from BaseClasses import Item, ItemClassification, CollectionState
from .GameLogic import GameLogic
from .Items import Items
from .Locations import Locations, LocationData
from .StateLogic import EventId, StateLogic
from .Options import SatisfactoryOptions, Placement
from .Regions import SatisfactoryLocation, create_regions_and_return_locations
from .CriticalPathCalculator import CriticalPathCalculator
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
    web = SatisfactoryWebWorld()
    origin_region_name = "Overworld"
    required_client_version = (0, 6, 0)
    ut_can_gen_without_yaml = True

    game_logic: ClassVar[GameLogic] = GameLogic()

    # These are set in generate_early and thus aren't always available
    state_logic: StateLogic | None = None
    items: Items | None = None
    critical_path: CriticalPathCalculator | None = None
    critical_path_seed: float | None = None
    #

    item_name_to_id = Items.item_names_and_ids
    location_name_to_id = Locations().get_locations_for_data_package()
    item_name_groups = Items.get_item_names_per_category(game_logic)

    def generate_early(self) -> None:
        self.interpret_slot_data(None)

        if self.critical_path_seed == None:
            self.critical_path_seed = self.random.random()

        self.critical_path = CriticalPathCalculator(self.game_logic, self.critical_path_seed, self.options)
        self.critical_path.calculate()

        self.state_logic = StateLogic(self.player, self.options, self.critical_path)
        self.items = Items(self.player, self.game_logic, self.random, self.options, self.critical_path)

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

        starting_inventory: list[str] = self.options.starting_inventory_preset.get_selected_list()
        for item_name in starting_inventory:
            self.push_precollected(item_name)


    def create_regions(self) -> None:
        locations: list[LocationData] = \
            Locations(self.game_logic, self.options, self.state_logic, self.items, self.critical_path).get_locations()
        create_regions_and_return_locations(
            self.multiworld, self.options, self.player, self.game_logic, self.state_logic, self.critical_path,
            locations)


    def create_items(self) -> None:
        self.setup_events()

        number_of_locations: int = len(self.multiworld.get_unfilled_locations(self.player))
        precollected_items: list[Item] = self.multiworld.precollected_items[self.player]
        
        self.multiworld.itempool += \
            self.items.build_item_pool(self.random, precollected_items, number_of_locations)


    def set_rules(self) -> None:
        resource_sink_goal: bool = "AWESOME Sink Points (total)" in self.options.goal_selection \
                                or "AWESOME Sink Points (per minute)" in self.options.goal_selection

        required_parts = set(self.game_logic.space_elevator_tiers[self.options.final_elevator_package.value - 1].keys())

        if resource_sink_goal:
            required_parts.union(self.game_logic.buildings["AWESOME Sink"].inputs)

        self.multiworld.completion_condition[self.player] = \
            lambda state: self.state_logic.can_produce_all(state, required_parts)


    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change and item.name in self.game_logic.indirect_recipes:
            state.prog_items[self.player][self.game_logic.indirect_recipes[item.name]] = 1
        return change


    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change and item.name in self.game_logic.indirect_recipes:
            del state.prog_items[self.player][self.game_logic.indirect_recipes[item.name]]
        return change


    def fill_slot_data(self) -> dict[str, object]:
        slot_hub_layout: list[list[dict[str, int]]] = []

        for tier, milestones in enumerate(self.game_logic.hub_layout, 1):
            slot_hub_layout.append([])
            for milestone, parts in enumerate(milestones, 1):
                 slot_hub_layout[tier - 1].append({})
                 for part, amount in parts.items():
                    multiplied_amount = int(max(amount * (self.options.milestone_cost_multiplier / 100), 1))
                    slot_hub_layout[tier-1][milestone-1][self.item_id_str(part)] = multiplied_amount

        starting_recipes: tuple[int] = tuple(
            self.item_name_to_id[recipe_name] 
            for recipe_name in self.critical_path.tier_0_recipes
        )

        return {
            "Data": {
                "HubLayout": slot_hub_layout,
                "ExplorationCosts": {
                    self.item_id_str("Mercer Sphere"): int(self.options.goal_exploration_collectables_amount.value * 2),
                    self.item_id_str("Somersloop"): self.options.goal_exploration_collectables_amount.value,
                    self.item_id_str("Hard Drive"): int(self.options.goal_exploration_collectables_amount.value / 5),
                    self.item_id_str("Paleberry"): self.options.goal_exploration_collectables_amount.value * 10,
                    self.item_id_str("Beryl Nut"): self.options.goal_exploration_collectables_amount.value * 20,
                    self.item_id_str("Bacon Agaric"): self.options.goal_exploration_collectables_amount.value,
                },
                "Options": {
                    "GoalSelection": self.options.goal_selection.value,
                    "GoalRequirement": self.options.goal_requirement.value,
                    "FinalElevatorTier": self.options.final_elevator_package.value,
                    "FinalResourceSinkPointsTotal": self.options.goal_awesome_sink_points_total.value,
                    "FinalResourceSinkPointsPerMinute": self.options.goal_awesome_sink_points_per_minute.value,
                    "FreeSampleEquipment": self.options.free_sample_equipment.value,
                    "FreeSampleBuildings": self.options.free_sample_buildings.value,
                    "FreeSampleParts": self.options.free_sample_parts.value,
                    "FreeSampleRadioactive": bool(self.options.free_sample_radioactive),
                    "EnergyLink": bool(self.options.energy_link),
                    "StartingRecipies": starting_recipes
                },
                "SlotDataVersion": 1,
                "UT": {
                    "Seed": self.critical_path_seed,
                    "RandomizeTier0": bool(self.options.randomize_starter_recipes)
                }
            },
            "DeathLink": bool(self.options.death_link)
        }


    def interpret_slot_data(self, slot_data: dict[str, Any] | None) -> dict[str, Any] | None:
        """Used by Universal Tracker to correctly rebuild state"""

        if not slot_data \
            and hasattr(self.multiworld, "re_gen_passthrough") \
            and isinstance(self.multiworld.re_gen_passthrough, dict) \
            and "Satisfactory" in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough["Satisfactory"]

        if not slot_data:
            return None
        
        if (slot_data["Data"]["SlotDataVersion"] != 1):
            raise Exception("The slot_data version mismatch, the UT's Satisfactory .apworld is different from the one used during generation")

        self.options.goal_selection.value = slot_data["Data"]["Options"]["GoalSelection"]
        self.options.goal_requirement.value = slot_data["Data"]["Options"]["GoalRequirement"]
        self.options.final_elevator_package.value = slot_data["Data"]["Options"]["FinalElevatorTier"]
        self.options.goal_awesome_sink_points_total.value = slot_data["Data"]["Options"]["FinalResourceSinkPointsTotal"]
        self.options.goal_awesome_sink_points_per_minute.value = \
            slot_data["Data"]["Options"]["FinalResourceSinkPointsPerMinute"]
        self.options.free_sample_equipment.value = slot_data["Data"]["Options"]["FreeSampleEquipment"]
        self.options.free_sample_buildings.value = slot_data["Data"]["Options"]["FreeSampleBuildings"]
        self.options.free_sample_parts.value = slot_data["Data"]["Options"]["FreeSampleParts"]
        self.options.free_sample_radioactive.value = int(slot_data["Data"]["Options"]["FreeSampleRadioactive"])
        self.options.energy_link.value = int(slot_data["Data"]["Options"]["EnergyLink"])

        self.options.milestone_cost_multiplier.value = 100 * \
            (slot_data["Data"]["HubLayout"][0][0][self.item_id_str("Concrete")] 
                / self.game_logic.hub_layout[0][0]["Concrete"])
        self.options.goal_exploration_collectables_amount.value = \
            slot_data["Data"]["ExplorationCosts"][self.item_id_str("Somersloop")]
        
        self.critical_path_seed = slot_data["Data"]["UT"]["Seed"]
        self.options.randomize_starter_recipes.value = slot_data["Data"]["UT"]["RandomizeTier0"]

        return slot_data


    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.randomize_starter_recipes:
            spoiler_handle.write(f'Starter Recipes:                 {sorted(self.critical_path.tier_0_recipes)}\n')


    def setup_events(self) -> None:
        location: SatisfactoryLocation
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item_name = location.event_name

                item = Item(item_name, ItemClassification.progression, EventId, self.player)

                location.place_locked_item(item)
                location.show_in_spoiler = False


    def get_filler_item_name(self) -> str:
        if self.items:
            return self.items.get_filler_item_name(self.random, None)
        else:
            return Items.get_filler_item_name_uninitialized(self.random)


    def create_item(self, name: str) -> Item:
        if self.items:
            return self.items.create_item(name, self.player)
        else:
            return Items.create_item_uninitialized(name, self.player)


    def push_precollected(self, item_name: str) -> None:
        item = self.create_item(item_name)
        self.multiworld.push_precollected(item)


    def item_id_str(self, item_name: str) -> str:
        # ItemIDs of bundles are shared with their component item
        bundled_name = f"Bundle: {item_name}"
        return str(self.item_name_to_id[bundled_name])
