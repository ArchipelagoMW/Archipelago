from typing import List, Optional, Callable, Tuple, Dict, Iterable, ClassVar
from BaseClasses import CollectionState
from .GameLogic import GameLogic, Recipe, Building, PowerInfrastructureLevel, DropPodData
from .StateLogic import StateLogic, EventId, part_event_prefix, building_event_prefix
from .Items import Items
from .Options import SatisfactoryOptions
from math import ceil, floor


class LocationData():
    region: str
    name: str
    event_name: str
    code: Optional[int]
    non_progression: Optional[bool]
    rule: Optional[Callable[[CollectionState], bool]]

    def __init__(self, region: str, name: str, code: Optional[int], event_name: Optional[str] = None,
                 non_progression: Optional[bool] = False, rule: Optional[Callable[[CollectionState], bool]] = None):
        self.region = region
        self.name = name
        self.code = code
        self.rule = rule
        self.non_progression = non_progression
        self.event_name = event_name or name


class Part(LocationData):
    @staticmethod
    def get_parts(state_logic: StateLogic, recipes: Tuple[Recipe, ...], name: str, items: Items) -> List[LocationData]:
        recipes_per_region: Dict[str, List[Recipe]] = {}

        for recipe in recipes:
            recipes_per_region.setdefault(recipe.building or "Overworld", []).append(recipe)

        return [Part(state_logic, region, recipes_for_region, name, items) 
                for region, recipes_for_region in recipes_per_region.items()]

    def __init__(self, state_logic: StateLogic, region: str, recipes: Iterable[Recipe], name: str, items: Items):
        super().__init__(region, part_event_prefix + name + region, EventId, part_event_prefix + name,
            rule = self.can_produce_any_recipe_for_part(state_logic, recipes, name, items))

    def can_produce_any_recipe_for_part(self, state_logic: StateLogic, recipes: Iterable[Recipe], 
                                        name: str, items: Items) -> Callable[[CollectionState], bool]:
        def can_build_by_any_recipe(state: CollectionState) -> bool:
            if name == "Steel Ingot":
                debug = True

            if items.precalculated_progression_recipes and name in items.precalculated_progression_recipes:
                can_produce: bool = state_logic.can_produce_specific_recipe_for_part(
                    state, items.precalculated_progression_recipes[name])
                
                can_produce_anyway: bool
                if can_produce:
                    return can_produce
                else:
                    can_produce_anyway = \
                        any(state_logic.can_produce_specific_recipe_for_part(state, recipe) for recipe in recipes)

                    if can_produce_anyway:
                        debug = True

                    return False # can_produce_anyway
            else:
                return any(state_logic.can_produce_specific_recipe_for_part(state, recipe) for recipe in recipes)

        return can_build_by_any_recipe


class EventBuilding(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, building_name: str, building: Building):
        super().__init__("Overworld", building_event_prefix + building_name, EventId, 
            rule = self.can_create_building(game_logic, state_logic, building))

    def can_create_building(self, game_logic: GameLogic, state_logic: StateLogic, building: Building
            ) -> Callable[[CollectionState], bool]:

        def can_build(state: CollectionState) -> bool:
            if building.name == "Building: Foundry":
                debug = True

            return state_logic.has_recipe(state, building) \
                and state_logic.can_power(state, building.power_requirement) \
                and state_logic.can_produce_all_allowing_handcrafting(state, game_logic, building.inputs)

        return can_build


class PowerInfrastructure(LocationData):
    def __init__(self, game_logic: GameLogic, state_logic: StateLogic, 
                 powerLevel: PowerInfrastructureLevel, recipes: Iterable[Recipe]):
        super().__init__("Overworld", building_event_prefix + powerLevel.to_name(), EventId, 
            rule = self.can_create_power_infrastructure(game_logic, state_logic, powerLevel, recipes))

    def can_create_power_infrastructure(self, game_logic: GameLogic, state_logic: StateLogic, 
                                        powerLevel: PowerInfrastructureLevel, recipes: Iterable[Recipe]
            ) -> Callable[[CollectionState], bool]:

        def can_power(state: CollectionState) -> bool:
            return any(state_logic.can_power(state, level) for level in PowerInfrastructureLevel if level > powerLevel)\
                or any(state_logic.can_build(state, recipe.building) and 
                       state_logic.can_produce_all_allowing_handcrafting(state, game_logic, recipe.inputs) 
                        for recipe in recipes)

        return can_power


class ElevatorTier(LocationData):
    def __init__(self, tier: int, state_logic: StateLogic, game_logic: GameLogic):
        super().__init__("Overworld", f"Elevator Tier {tier + 1}", EventId,
            rule = lambda state: state_logic.can_build(state, "Space Elevator") and \
                                 state_logic.can_produce_all(state, game_logic.space_elevator_tiers[tier].keys()))


class HubSlot(LocationData):
    def __init__(self, tier: int, milestone: int, slot: int, locationId: int):
        super().__init__(f"Hub {tier}-{milestone}", f"Hub {tier}-{milestone}, item {slot}", locationId)


class MamSlot(LocationData):
    def __init__(self, tree: str, nodeName: str, locationId: int):
        super().__init__(f"{tree}: {nodeName}", f"{tree}: {nodeName}", locationId)


class ShopSlot(LocationData):
    def __init__(self, state_logic: Optional[StateLogic], slot: int, cost: int, locationId: int):
        super().__init__("AWESOME Shop", f"AWESOME Shop purchase {slot}", locationId,
            rule = self.can_purchase_from_shop(state_logic, cost))
        
    def can_purchase_from_shop(self, state_logic: Optional[StateLogic], cost) -> Callable[[CollectionState], bool]:
        def can_purchase(state: CollectionState) -> bool:
            if not state_logic or cost < 20:
                return True
            elif (cost >= 20 and cost < 50):
                return state_logic.is_game_phase(state, 1)
            elif (cost >= 50 and cost < 100):
                return state_logic.is_game_phase(state, 2)
            else:
                return state_logic.is_game_phase(state, 3)
            
        return can_purchase


class DropPod(LocationData):
    def __init__(self, data: DropPodData, state_logic: Optional[StateLogic],
            locationId: int, tier: int, can_hold_progression: bool):

        # drop pod locations are unlocked by hard drives, there is currently no direct mapping between location and hard drive
        # we currently do not know how many hdd require gas or radioactive protection
        # coordinates are for us to reference them, there is no real link between coordinate and check
        def get_region(gassed: Optional[bool], radioactive: Optional[bool]) -> str:
            #if radioactive:
            #    return "Radioactive Area"
            #elif gassed:
            #    return "Gas Area"
            #else:
            #    return "Overworld"
            return f"Hub Tier {tier}"

        def get_rule(unlocked_by: Optional[str], power_needed: int) -> Callable[[CollectionState], bool]:
            # Power is kept out of logic. with energy link its simple, 
            # without you just going to have to figure it your yourself

            def logic_rule(state: CollectionState):
                return state_logic.can_build(state, "MAM") and (
                    (not unlocked_by) or (state_logic and state_logic.can_produce(state, unlocked_by)))

            return logic_rule

        super().__init__(
            get_region(data.gassed, data.radioactive), f"Hard drive random check {locationId - 1338600}", locationId,
                non_progression = not can_hold_progression, rule = get_rule(data.item, data.power))


class Locations():
    game_logic: Optional[GameLogic]
    options: Optional[SatisfactoryOptions]
    state_logic: Optional[StateLogic]
    items: Optional[Items]

    hub_location_start: ClassVar[int] = 1338000
    max_tiers: ClassVar[int] = 10
    max_milestones: ClassVar[int] = 5
    max_slots: ClassVar[int] = 10
    drop_pod_location_id_start: ClassVar[int] = 1338600
    drop_pod_location_id_end: ClassVar[int] = 1338699

    def __init__(self, game_logic: Optional[GameLogic] = None, options: Optional[SatisfactoryOptions] = None,
                 state_logic: Optional[StateLogic] = None, items: Optional[Items] = None):
        self.game_logic = game_logic
        self.options = options
        self.state_logic = state_logic
        self.items = items

    def get_base_location_table(self) -> List[LocationData]:
        return [
            MamSlot("Alien Organisms", "Inflated Pocket Dimension", 1338500),
            MamSlot("Alien Organisms", "Hostile Organism Detection", 1338501),
            MamSlot("Alien Organisms", "Expanded Toolbelt", 1338502),
            MamSlot("Alien Organisms", "Bio-Organic Properties", 1338503),
            MamSlot("Alien Organisms", "Stinger Research", 1338504),
            MamSlot("Alien Organisms", "Hatcher Research", 1338505),
            MamSlot("Alien Organisms", "Hog Research", 1338506),
            MamSlot("Alien Organisms", "Spitter Research", 1338507),
            MamSlot("Alien Organisms", "Structural Analysis", 1338508),
            MamSlot("Alien Organisms", "Protein Inhaler", 1338509),
            MamSlot("Alien Organisms", "The Rebar Gun", 1338510),
            MamSlot("Caterium", "Caterium Electronics", 1338511),
            MamSlot("Caterium", "Bullet Guidance System", 1338512),
            MamSlot("Caterium", "High-Speed Connector", 1338513),
            MamSlot("Caterium", "Caterium", 1338514),
            MamSlot("Caterium", "Caterium Ingots", 1338515),
            MamSlot("Caterium", "Quickwire", 1338516),
            MamSlot("Caterium", "Power Switch", 1338517),
            MamSlot("Caterium", "Power Poles Mk.2", 1338518),
            MamSlot("Caterium", "AI Limiter", 1338519),
            MamSlot("Caterium", "Smart Splitter", 1338520),
            MamSlot("Caterium", "Programmable Splitter", 1338521),
            MamSlot("Mycelia", "Gas Mask", 1338522), # 1.0
            MamSlot("Caterium", "Zipline", 1338523),
            MamSlot("Caterium", "Geothermal Generator", 1338524),
            MamSlot("Caterium", "Priority Power Switch", 1338525),
            MamSlot("Caterium", "Stun Rebar", 1338526),
            MamSlot("Caterium", "Power Poles Mk.3", 1338527),
            MamSlot("Mycelia", "Therapeutic Inhaler", 1338528),
            MamSlot("Mycelia", "Expanded Toolbelt", 1338529),
            MamSlot("Mycelia", "Mycelia", 1338530),
            MamSlot("Mycelia", "Fabric", 1338531),
            MamSlot("Mycelia", "Medical Properties", 1338532),
            MamSlot("Mycelia", "Toxic Cellular Modification", 1338533),
            MamSlot("Mycelia", "Vitamin Inhaler", 1338534),
            MamSlot("Mycelia", "Parachute", 1338535),
            MamSlot("Mycelia", "Synthethic Polyester Fabric", 1338536),
            MamSlot("Nutrients", "Bacon Agaric", 1338537),
            MamSlot("Nutrients", "Beryl Nut", 1338538),
            MamSlot("Nutrients", "Paleberry", 1338539),
            MamSlot("Nutrients", "Nutritional Processor", 1338540),
            MamSlot("Nutrients", "Nutritional Inhaler", 1338541),
            MamSlot("Power Slugs", "Slug Scanning", 1338542),
            MamSlot("Power Slugs", "Blue Power Slugs", 1338543),
            MamSlot("Power Slugs", "Yellow Power Shards", 1338544),
            MamSlot("Power Slugs", "Purple Power Shards", 1338545),
            MamSlot("Power Slugs", "Overclock Production", 1338546),
            MamSlot("Quartz", "Crystal Oscillator", 1338547),
            MamSlot("Quartz", "Quartz Crystals", 1338548),
            MamSlot("Quartz", "Quartz", 1338549),
            MamSlot("Quartz", "Shatter Rebar", 1338550),
            MamSlot("Quartz", "Silica", 1338551),
            MamSlot("Quartz", "Explosive Resonance Application", 1338552),
            MamSlot("Quartz", "Blade Runners", 1338553),
            MamSlot("Quartz", "The Explorer", 1338554),
            MamSlot("Quartz", "Radio Signal Scanning", 1338555),
            MamSlot("Quartz", "Inflated Pocket Dimension", 1338556),
            MamSlot("Quartz", "Radar Technology", 1338557),
            MamSlot("Sulfur", "The Nobelisk Detonator", 1338558),
            MamSlot("Sulfur", "Smokeless Powder", 1338559),
            MamSlot("Sulfur", "Sulfur", 1338560),
            MamSlot("Sulfur", "Inflated Pocket Dimension", 1338561),
            MamSlot("Sulfur", "The Rifle", 1338562),
            MamSlot("Sulfur", "Compacted Coal", 1338563),
            MamSlot("Sulfur", "Black Powder", 1338564),
            MamSlot("Sulfur", "Explosive Rebar", 1338565),
            MamSlot("Sulfur", "Cluster Nobelisk", 1338566),
            MamSlot("Sulfur", "Experimental Power Generation", 1338567),
            MamSlot("Sulfur", "Turbo Rifle Ammo", 1338568),
            MamSlot("Sulfur", "Turbo Fuel", 1338569),
            MamSlot("Sulfur", "Expanded Toolbelt", 1338570),
            MamSlot("Sulfur", "Nuclear Deterrent Development", 1338571),

            # 1.0
            MamSlot("Power Slugs", "Synthetic Power Shards", 1338572),
            MamSlot("Sulfur", "Rocket Fuel", 1338573),
            MamSlot("Sulfur", "Ionized Fuel", 1338574),
            MamSlot("Alien Technology", "SAM Analysis", 1338575),
            MamSlot("Alien Technology", "SAM Reanimation", 1338576),
            MamSlot("Alien Technology", "SAM Fluctuator", 1338577),
            MamSlot("Alien Technology", "Mercer Sphere Analysis", 1338578),
            MamSlot("Alien Technology", "Dimensional Depot", 1338579),
            MamSlot("Alien Technology", "Manual Depot Uploader", 1338580),
            MamSlot("Alien Technology", "Depot Expansion (200%)", 1338581),
            MamSlot("Alien Technology", "Depot Expansion (300%)", 1338582),
            MamSlot("Alien Technology", "Depot Expansion (400%)", 1338583),
            MamSlot("Alien Technology", "Depot Expansion (500%)", 1338584),
            MamSlot("Alien Technology", "Upload Upgrade: 30/min", 1338585),
            MamSlot("Alien Technology", "Upload Upgrade: 60/min", 1338586),
            MamSlot("Alien Technology", "Upload Upgrade: 120/min", 1338587),
            MamSlot("Alien Technology", "Upload Upgrade: 240/min", 1338588),
            MamSlot("Alien Technology", "Somersloop Analysis", 1338589),
            MamSlot("Alien Technology", "Alien Energy Harvesting", 1338590),
            MamSlot("Alien Technology", "Production Amplifier", 1338591),
            MamSlot("Alien Technology", "Power Augmenter", 1338592),
            MamSlot("Alien Technology", "Alien Power Matrix", 1338593),
            # 1.0

            # 1338600 - 1338699 - Harddrives - Harddrives

            ShopSlot(self.state_logic, 1, 3, 1338700),
            ShopSlot(self.state_logic, 2, 3, 1338701),
            ShopSlot(self.state_logic, 3, 5, 1338702),
            ShopSlot(self.state_logic, 4, 5, 1338703),
            ShopSlot(self.state_logic, 5, 10, 1338704),
            ShopSlot(self.state_logic, 6, 10, 1338705),
            ShopSlot(self.state_logic, 7, 20, 1338706),
            ShopSlot(self.state_logic, 8, 20, 1338707),
            ShopSlot(self.state_logic, 9, 50, 1338708),
            ShopSlot(self.state_logic, 10, 50, 1338709)
        ]

    def get_locations_for_data_package(self) -> Dict[str, int]:
        "Must include all possible location names and their id's"

        location_table = self.get_base_location_table()
        location_table.extend(self.get_hub_locations())
        location_table.extend(self.get_drop_pod_locations())
        location_table.append(LocationData("Overworld", "UpperBound", 1338999))

        return {location.name: location.code for location in location_table}

    def get_locations(self) -> List[LocationData]:
        "Only return location used in this game based on settings"

        if not self.game_logic or not self.options or not self.state_logic or not self.items:
            raise Exception("Locations need to be initialized with logic, options and items before using this method")

        location_table = self.get_base_location_table()
        location_table.extend(self.get_hub_locations())
        location_table.extend(self.get_drop_pod_locations())
        location_table.extend(self.get_logical_event_locations())

        return location_table

    def get_hub_locations(self) -> List[LocationData]:
        location_table: List[LocationData] = []

        hub_location_id = self.hub_location_start
        for tier in range(1, self.max_tiers + 1):
            for milestone in range(1, self.max_milestones + 1):
                for slot in range(1, self.max_slots + 1):
                    if not self.game_logic:
                        location_table.append(HubSlot(tier, milestone, slot, hub_location_id))
                    else:
                        if tier <= len(self.game_logic.hub_layout) \
                                and milestone <= len(self.game_logic.hub_layout[tier - 1]) \
                                and slot <= self.game_logic.slots_per_milestone:
                            location_table.append(HubSlot(tier, milestone, slot, hub_location_id))

                    hub_location_id += 1
                
        return location_table

    def get_logical_event_locations(self) -> List[LocationData]:
        location_table: List[LocationData] = []

        # for performance plan is to upfront calculated everything we need
        # and than create one massive state.has_all for each logical gate (hub tiers, elevator tiers)

        location_table.extend(
            ElevatorTier(index, self.state_logic, self.game_logic) 
            for index, parts in enumerate(self.game_logic.space_elevator_tiers))
        location_table.extend(
            part 
            for part_name, recipes in self.game_logic.recipes.items() 
            for part in Part.get_parts(self.state_logic, recipes, part_name, self.items))
        location_table.extend(
            EventBuilding(self.game_logic, self.state_logic, name, building) 
            for name, building in self.game_logic.buildings.items())
        location_table.extend(
            PowerInfrastructure(self.game_logic, self.state_logic, power_level, recipes) 
            for power_level, recipes in self.game_logic.requirement_per_powerlevel.items())

        return location_table
    
    def get_drop_pod_locations(self) -> List[LocationData]:
        drop_pod_locations: List[DropPod] = []

        bucket_size: int = 0
        drop_pod_data: List[DropPodData] = []

        if self.game_logic:
            bucket_size = floor(
                (self.drop_pod_location_id_end - self.drop_pod_location_id_start) / len(self.game_logic.hub_layout))

            drop_pod_data = self.game_logic.drop_pods
            # sort, easily obtainable first, should be deterministic
            drop_pod_data.sort(key = lambda data: ("!" if data.item == None else data.item) + str(data.x - data.z))

        for location_id in range(self.drop_pod_location_id_start, self.drop_pod_location_id_end + 1):
            if not self.game_logic or not self.state_logic or not self.options:
                drop_pod_locations.append(DropPod(DropPodData(0, 0, 0, None, 0), None, location_id, 1, False))
            else:
                location_id_normalized: int = location_id - self.drop_pod_location_id_start
                data: DropPodData = drop_pod_data[location_id_normalized]
                can_hold_progression: bool = location_id_normalized < self.options.hard_drive_progression_limit.value
                tier = min(ceil((location_id_normalized + 1) / bucket_size), len(self.game_logic.hub_layout))

                drop_pod_locations.append(DropPod(data, self.state_logic, location_id, tier, can_hold_progression))

        return drop_pod_locations