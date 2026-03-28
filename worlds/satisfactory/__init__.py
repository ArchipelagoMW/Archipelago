from typing import TextIO, ClassVar, Any
from collections.abc import Iterable
from BaseClasses import Item, ItemClassification, CollectionState
from NetUtils import Hint
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
        self.process_universal_tracker_slot_data_if_available()

        if not self.critical_path_seed:
            self.critical_path_seed = self.random.random()

        if self.options.mam_logic_placement.value == Placement.starting_inventory:
            self.push_precollected_by_name("Building: MAM")
        if self.options.awesome_logic_placement.value == Placement.starting_inventory:
            self.push_precollected_by_name("Building: AWESOME Sink")
            self.push_precollected_by_name("Building: AWESOME Shop")
        if self.options.energy_link_logic_placement.value == Placement.starting_inventory:
            self.push_precollected_by_name("Building: Power Storage")
        if self.options.splitter_placement == Placement.starting_inventory:
            self.push_precollected_by_name("Building: Conveyor Splitter")
            self.push_precollected_by_name("Building: Conveyor Merger")

        if not self.options.trap_selection_override.value:
            self.options.trap_selection_override.value = set(self.options.trap_selection_preset.get_selected_list())

        self.critical_path = CriticalPathCalculator(self.game_logic, self.critical_path_seed, self.options)
        self.critical_path.calculate()

        self.state_logic = StateLogic(self.player, self.options, self.critical_path)
        self.items = Items(self.player, self.game_logic, self.random, self.options, self.critical_path)

        starting_inventory: list[str] = self.options.starting_inventory_preset.get_selected_list()
        for item_name in starting_inventory:
            self.push_precollected_by_name(item_name)

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
        required_parts = set(self.game_logic.space_elevator_phases[self.options.final_elevator_phase.value - 1].keys())
        required_buildings = set()
        required_items = set()

        if "Space Elevator Phase" in self.options.goal_selection:
            required_buildings.add("Space Elevator")

        if "AWESOME Sink Points (total)" in self.options.goal_selection \
                or "AWESOME Sink Points (per minute)" in self.options.goal_selection:
            required_buildings.add("AWESOME Sink")

        if "Erect a FICSMAS Tree" in self.options.goal_selection:
            required_parts.add("FICSMAS Wonder Star")
            required_buildings.add("MAM")
            required_items.update(
                ("FICSMAS Data Cartridge Day 4", "FICSMAS Data Cartridge Day 8", "FICSMAS Data Cartridge Day 14"))            

        self.multiworld.completion_condition[self.player] = \
            lambda state: self.state_logic.can_produce_all(state, required_parts) \
                and self.state_logic.can_build_all(state, required_buildings) \
                and self.state_logic.has_obtained_all(state, required_items)

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change and item.name in self.game_logic.indirect_recipes:
            state.prog_items[self.player][self.game_logic.indirect_recipes[item.name]] += 1
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change and item.name in self.game_logic.indirect_recipes:
            state.prog_items[self.player][self.game_logic.indirect_recipes[item.name]] -= 1
        return change

    def fill_slot_data(self) -> dict[str, object]:
        slot_hub_layout: list[list[dict[str, int]]] = []

        for tier, milestones in enumerate(self.game_logic.hub_layout, 1):
            slot_hub_layout.append([])
            for milestone, parts in enumerate(milestones, 1):
                slot_hub_layout[tier - 1].append({})
                for part, amount in parts.items():
                    multiplied_amount = int(max(amount * (self.options.milestone_cost_multiplier / 100), 1))
                    slot_hub_layout[tier - 1][milestone - 1][self.item_id_str(part)] = multiplied_amount

        starting_recipes: tuple[int, ...] = tuple(
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
                    "FinalElevatorPhase": self.options.final_elevator_phase.value,
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

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any] | None) -> dict[str, Any] | None:
        """Used by Universal Tracker, return value is passed to self.multiworld.re_gen_passthrough["Satisfactory"]"""
        return slot_data

    def process_universal_tracker_slot_data_if_available(self) -> None:
        """Used by Universal Tracker to correctly rebuild state"""

        slot_data: dict[str, Any] | None = None
        if (hasattr(self.multiworld, "re_gen_passthrough")
                and isinstance(self.multiworld.re_gen_passthrough, dict)
                and "Satisfactory" in self.multiworld.re_gen_passthrough):
            slot_data = self.multiworld.re_gen_passthrough["Satisfactory"]

        if not slot_data:
            return

        if slot_data["Data"]["SlotDataVersion"] != 1:
            raise Exception("The slot_data version mismatch, the UT's Satisfactory .apworld is different from the one "
                            "used during generation")

        self.options.goal_selection.value = slot_data["Data"]["Options"]["GoalSelection"]
        self.options.goal_requirement.value = slot_data["Data"]["Options"]["GoalRequirement"]
        self.options.final_elevator_phase.value = slot_data["Data"]["Options"]["FinalElevatorPhase"]
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

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.randomize_starter_recipes:
            spoiler_handle.write(f'Starter Recipes:                 {sorted(self.critical_path.tier_0_recipes)}\n')

    def setup_events(self) -> None:
        location: SatisfactoryLocation
        for location in self.get_locations():
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

    def extend_hint_information(self, _: dict[int, dict[int, str]]):
        """
        Normally used for adding entrance information, 
        but in this case we want to create hints for locations that hold usefull items.
        Since we only know item placements after generation is completed it was either this 
            or fill_slot_data or modify_multidata, and this method seemed the best fit
        """

        locations_visible_from_start: set[int] = set(range(1338000, 1338099))  # ids of Hub 1-1,1 to 2-5,10

        if "Building: AWESOME Shop" in self.options.start_inventory \
                or "Building: AWESOME Shop" in self.options.start_inventory_from_pool \
                or self.options.awesome_logic_placement.value == Placement.starting_inventory:
            locations_visible_from_start.update(range(1338700, 1338709))  # ids of shop locations 1 to 10

            location_names_with_useful_items: Iterable[str] = [
                location.name
                for location in self.get_locations()
                if location.address in locations_visible_from_start and location.item \
                        and location.item.flags & (ItemClassification.progression | ItemClassification.useful) > 0
            ]

            self.options.start_location_hints.value.update(location_names_with_useful_items)

    def push_precollected_by_name(self, item_name: str) -> None:
        item = self.create_item(item_name)
        self.push_precollected(item)

    def item_id_str(self, item_name: str) -> str:
        # ItemIDs of bundles are shared with their component item
        bundled_name = f"Bundle: {item_name}"
        return str(self.item_name_to_id[bundled_name])
