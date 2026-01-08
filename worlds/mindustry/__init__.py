from typing import ClassVar, Dict, List, Any

from BaseClasses import MultiWorld, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.mindustry.Shared import MINDUSTRY_BASE_ID
from worlds.mindustry.Items import item_table, MindustryItem, ItemType, ItemGroup
from worlds.mindustry.Locations import location_table
from worlds.mindustry.Options import MindustryOptions
from worlds.mindustry.Regions import MindustryRegions
from worlds.mindustry.Items import ItemPlanet

class MindustryWeb(WebWorld):
    """Mindustry web page for Archipelago"""
    theme = "stone"

class MindustryWorld(World):
    """
    In Mindustry, you control a small ship that defends a structure called the Core,
    your job is to build production lines and defenses to survive, maintain and conquer.
    There are a total of eight different categories of structures to build, varying from
    drills and factories to extract and refine resources, to turrets and walls to defend your assets.
    There are many more buildings that help to take back Serpulo and other planets. the two current
    planets are; Serpulo and Erikir, Serpulo is the home planet of your faction; the Sharded,
    brought to defend the planet from the formidable enemy; the Crux. The second planet of Erikir
    has a far different and far more deadly enemy of Malis, and their strategies reflect such.
    Source: https://en.wikipedia.org/wiki/Draft:Mindustry
    """
    game: str = "Mindustry"
    """Name of the game"""

    topology_present = True
    "show path to required location checks in spoiler"

    item_name_to_id: ClassVar[Dict[str, int]] =\
        {name: data.id for name, data in item_table.items()}
    "The name and associated ID of each item of the world"

    location_name_to_id = location_table
    "The name and associated ID of each location of the world"

    base_id = MINDUSTRY_BASE_ID
    "The starting ID of the items and locations of the world"

    options_dataclass = MindustryOptions
    "Used to manage world options"

    options: MindustryOptions
    "Every options of the world"

    regions: MindustryRegions
    "Used to manage Regions"

    exclude: List[str]

    def create_regions(self) -> None:
        """
        Create every Region in `regions`
        """
        self.regions.create_campaign(self.options)
        self.regions.connect_regions(self.options)
        self.regions.add_event_locations(self.options)

    def create_item(self, name: str) -> MindustryItem:
        """
        Create an MindustryItem using `name` as item name.
        """
        result: MindustryItem
        try:
            data = item_table[name]
            classification: ItemClassification = ItemClassification.useful
            if data.group == ItemGroup.FILLER:
                classification = ItemClassification.filler
            if data.type == ItemType.NECESSARY:
                classification = ItemClassification.progression
            result = MindustryItem(name, classification, data.id, self.player)
        except BaseException:
            raise Exception('The item ' + name + ' is not valid.')

        return result

    def __pre_fill_item(self, item_name: str, location_name: str, precollected) -> None:
        """Pre-assign an item to a location"""
        if item_name not in precollected:
            self.exclude.append(item_name)
            data = item_table[item_name]
            item = MindustryItem(item_name, data.id, ItemClassification.useful, self.player)
            self.multiworld.get_location(location_name, self.player).place_locked_item(item)

    def create_items(self) -> None:
        """Create every item in the world"""
        campaign = self.options.campaign_choice.value
        self.__exclude_items(self.options)
        world_item_count = 0
        for name, data in item_table.items():
            if self.__from_selected_campaign(data, campaign):
                if name not in self.exclude:
                    item_count = item_table.get(name).count
                    for i in range(item_count):
                        item = self.create_item(name)
                        self.multiworld.itempool.append(item)
                        world_item_count += 1
        #Check how many location are empty and fill them with FILLERS
        remaining = len(self.multiworld.get_unfilled_locations(self.player)) - world_item_count
        while remaining > 0:
            self.__create_filler_item(campaign)
            remaining -= 1

    def generate_early(self) -> None:
        """Change item classification based on options."""
        campaign = self.options.campaign_choice.value
        if self.options.military_level_tracking:
            if campaign == 0: #Serpulo
                self.__apply_serpulo_military_item_classification()
            elif campaign == 1: #Erekir
                self.__apply_erekir_military_item_classification()
            elif campaign == 2: #All
                self.__apply_serpulo_military_item_classification()
                self.__apply_erekir_military_item_classification()

        if self.options.make_early_roadblocks_local:
            if campaign == 0: #Serpulo
                self.__apply_serpulo_local_roadblocks()
            elif campaign == 1: #Erekir
                self.__apply_erekir_local_roadblocks()
            elif campaign == 2: #All
                self.__apply_serpulo_local_roadblocks()
                self.__apply_erekir_local_roadblocks()

        if self.options.logistic_distribution == 1: #Early logistics
            if campaign == 0: #Serpulo
                self.__apply_serpulo_early_logistics()
            elif campaign == 1: #Erekir
                self.__apply_erekir_early_logistics()
            elif campaign == 2: #All
                self.__apply_serpulo_early_logistics()
                self.__apply_erekir_early_logistics()
        if self.options.logistic_distribution == 2: #Local early logistics
            if campaign == 0:
                self.__apply_serpulo_local_early_logistics()
            elif campaign == 1:
                self.__apply_erekir_local_early_logistics()
            elif campaign == 2:
                self.__apply_serpulo_local_early_logistics()
                self.__apply_erekir_local_early_logistics()

    def __apply_serpulo_local_roadblocks(self):
        """Add some Serpulo research to the local early items list"""
        self.multiworld.local_early_items[self.player]["Graphite Press"] = 1
        self.multiworld.local_early_items[self.player]["Silicon Smelter"] = 1
        self.multiworld.local_early_items[self.player]["Combustion Generator"] = 1

    def __apply_erekir_local_roadblocks(self):
        """Add some Erekir research to the local early items list"""
        self.multiworld.local_early_items[self.player]["Impact Drill"] = 1
        self.multiworld.local_early_items[self.player]["Reinforced Conduit"] = 1
        self.multiworld.local_early_items[self.player]["Ship Fabricator"] = 1
        self.multiworld.local_early_items[self.player]["Progressive Ships"] = 1

    def __apply_serpulo_early_logistics(self):
        """Add Serpulo's logistics items to the early items list."""
        self.multiworld.early_items[self.player]["Conduit"] = 1
        self.multiworld.early_items[self.player]["Liquid Junction"] = 1
        self.multiworld.early_items[self.player]["Liquid Router"] = 1
        self.multiworld.early_items[self.player]["Bridge Conduit"] = 1
        self.multiworld.early_items[self.player]["Junction"] = 1
        self.multiworld.early_items[self.player]["Router"] = 1
        self.multiworld.early_items[self.player]["Bridge Conveyor"] = 1
        self.multiworld.early_items[self.player]["Power Node"] = 1

    def __apply_serpulo_local_early_logistics(self):
        """Add Serpulo's logistics items to the local early items list."""
        self.multiworld.local_early_items[self.player]["Conduit"] = 1
        self.multiworld.local_early_items[self.player]["Liquid Junction"] = 1
        self.multiworld.local_early_items[self.player]["Liquid Router"] = 1
        self.multiworld.local_early_items[self.player]["Bridge Conduit"] = 1
        self.multiworld.local_early_items[self.player]["Junction"] = 1
        self.multiworld.local_early_items[self.player]["Router"] = 1
        self.multiworld.local_early_items[self.player]["Bridge Conveyor"] = 1
        self.multiworld.local_early_items[self.player]["Power Node"] = 1

    def __apply_erekir_early_logistics(self):
        """Add Erekir's logistics items to the early items list."""
        self.multiworld.early_items[self.player]["Duct Router"] = 1
        self.multiworld.early_items[self.player]["Duct Bridge"] = 1
        if not self.options.make_early_roadblocks_local: #Item was already added previously.
            self.multiworld.early_items[self.player]["Reinforced Conduit"] = 1
        self.multiworld.early_items[self.player]["Reinforced Liquid Junction"] = 1
        self.multiworld.early_items[self.player]["Reinforced Bridge Conduit"] = 1
        self.multiworld.early_items[self.player]["Reinforced Liquid Router"] = 1

    def __apply_erekir_local_early_logistics(self):
        """Add Erekir's logistics items to the local early items list."""
        self.multiworld.local_early_items[self.player]["Duct Router"] = 1
        self.multiworld.local_early_items[self.player]["Duct Bridge"] = 1
        if not self.options.make_early_roadblocks_local:  # Item was already added previously.
            self.multiworld.early_items[self.player]["Reinforced Conduit"] = 1
        self.multiworld.local_early_items[self.player]["Reinforced Liquid Junction"] = 1
        self.multiworld.local_early_items[self.player]["Reinforced Bridge Conduit"] = 1
        self.multiworld.local_early_items[self.player]["Reinforced Liquid Router"] = 1

    def __apply_erekir_military_item_classification(self):
        """Apply the NECESSARY item classification for Erekir military items."""
        item_table["Diffuse"].type = ItemType.NECESSARY
        item_table["Sublimate"].type = ItemType.NECESSARY
        item_table["Disperse"].type = ItemType.NECESSARY
        item_table["Afflict"].type = ItemType.NECESSARY
        item_table["Scathe"].type = ItemType.NECESSARY
        item_table["Titan"].type = ItemType.NECESSARY
        item_table["Malign"].type = ItemType.NECESSARY
        item_table["Electric Heater"].type = ItemType.NECESSARY
        item_table["Slag Heater"].type = ItemType.NECESSARY
        item_table["Phase Heater"].type = ItemType.NECESSARY
        item_table["Heat Redirector"].type = ItemType.NECESSARY
        item_table["Heat Router"].type = ItemType.NECESSARY
        item_table["Neoplasia Reactor"].type = ItemType.NECESSARY
        item_table["Lustre"].type = ItemType.NECESSARY
        item_table["Smite"].type = ItemType.NECESSARY
        item_table["Tungsten Wall"].type = ItemType.NECESSARY
        item_table["Large Tungsten Wall"].type = ItemType.NECESSARY
        item_table["Reinforced Surge Wall"].type = ItemType.NECESSARY
        item_table["Large Reinforced Surge Wall"].type = ItemType.NECESSARY
        item_table["Carbide Wall"].type = ItemType.NECESSARY
        item_table["Large Carbide Wall"].type = ItemType.NECESSARY
        item_table["Shielded Wall"].type = ItemType.NECESSARY
        item_table["Regen Projector"].type = ItemType.NECESSARY
        item_table["Build Tower"].type = ItemType.NECESSARY
        item_table["Shockwave Tower"].type = ItemType.NECESSARY
        item_table["Prime Refabricator"].type = ItemType.NECESSARY
        item_table["Large Beryllium Wall"].type = ItemType.NECESSARY
        item_table["Constructor"].type = ItemType.NECESSARY
        item_table["Tank Assembler"].type = ItemType.NECESSARY
        item_table["Ship Assembler"].type = ItemType.NECESSARY
        item_table["Mech Assembler"].type = ItemType.NECESSARY
        item_table["Basic Assembler Module"].type = ItemType.NECESSARY

    def __apply_serpulo_military_item_classification(self):
        """Apply the NECESSARY item classification for Serpulo military items."""
        item_table["Hail"].type = ItemType.NECESSARY
        item_table["Arc"].type = ItemType.NECESSARY
        item_table["Scorch"].type = ItemType.NECESSARY
        item_table["Parallax"].type = ItemType.NECESSARY
        item_table["Wave"].type = ItemType.NECESSARY
        item_table["Lancer"].type = ItemType.NECESSARY
        item_table["Salvo"].type = ItemType.NECESSARY
        item_table["Swarmer"].type = ItemType.NECESSARY
        item_table["Ripple"].type = ItemType.NECESSARY
        item_table["Tsunami"].type = ItemType.NECESSARY
        item_table["Fuse"].type = ItemType.NECESSARY
        item_table["Meltdown"].type = ItemType.NECESSARY
        item_table["Foreshadow"].type = ItemType.NECESSARY
        item_table["Cyclone"].type = ItemType.NECESSARY
        item_table["Spectre"].type = ItemType.NECESSARY
        item_table["Segment"].type = ItemType.NECESSARY
        item_table["Mender"].type = ItemType.NECESSARY
        item_table["Mend Projector"].type = ItemType.NECESSARY
        item_table["Shock Mine"].type = ItemType.NECESSARY

    def __create_filler_item(self, campaign):
        """
        Create a filler item from the selected campaign
        """
        self.multiworld.itempool.append(self.create_item("A fistful of nothing..."))

    def __from_selected_campaign(self, data, campaign: int) -> bool:
        """
        Return if an item is from the selected campaign.
        """
        valid = False
        if data.group != ItemGroup.FILLER: #We dont want filler items to get thrown in yet.
            if campaign == 0:
                if data.item_planet == ItemPlanet.SERPULO:
                    valid = True
            elif campaign == 1:
                if data.item_planet == ItemPlanet.EREKIR:
                    valid = True
            elif campaign == 2:
                valid = True
            else:
                valid = False
        return valid

    def set_rules(self) -> None:
        """
        Launched when the Multiworld generator is ready to generate rules
        """
        self.regions.initialise_rules(self.options)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(["A fistful of nothing..."])

    def __init__(self, multiworld: MultiWorld, player: int):
        """Initialise the Mindustry World"""
        super(MindustryWorld, self).__init__(multiworld, player)
        self.regions = MindustryRegions(multiworld, player)
        self.exclude = []

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "tutorial_skip": bool(self.options.tutorial_skip.value),
            "campaign_choice": self.options.campaign_choice.value,
            "goal": self.options.goal.value,
            "disable_invasions": bool(self.options.disable_invasions.value),
            "faster_production": bool(self.options.faster_production.value),
            "faster_conveyor": bool(self.options.faster_conveyor.value),
            "death_link": bool(self.options.death_link.value),
            "death_link_mode": self.options.death_link_mode.value,
            "military_level_tracking": bool(self.options.military_level_tracking.value),
            "randomize_core_units_weapon": bool(self.options.randomize_core_units_weapon.value),
            "logistic_distribution": self.options.logistic_distribution.value,
            "progressive_drills": bool(self.options.progressive_drills),
            "progressive_generators": bool(self.options.progressive_generators),
            "make_early_roadblocks_local": bool(self.options.make_early_roadblocks_local),
            "amount_of_resources_required": self.options.amount_of_resources_required.value,
            "core_russian_roulette_chambers": self.options.core_russian_roulette_chambers.value
        }

    def __exclude_items(self, options: MindustryOptions) -> None:
        """Exclude items from the item pools depending on player options"""
        campaign = options.campaign_choice.value
        progressive_drills = bool(options.progressive_drills)
        progressive_generators = bool(options.progressive_generators)

        if campaign == 0: #Serpulo
            if self.options.logistic_distribution == 3:  # Starter logistics
                self.__starter_serpulo_logistics()
            if progressive_drills:
                self.__exclude_serpulo_drills()
            else:
                self.__exclude_serpulo_progressive_drills()
            if progressive_generators:
                self.__exclude_serpulo_generators()
            else:
                self.__exclude_serpulo_progressive_generators()
        if campaign == 1: #Erekir
            if self.options.logistic_distribution == 3:  # Starter logistics
                self.__starter_erekir_logistics()
            if progressive_drills:
                self.__exclude_erekir_drills()
            else:
                self.__exclude_erekir_progressive_drills()
            if progressive_generators:
                self.__exclude_erekir_generators()
            else:
                self.__exclude_erekir_progressive_generators()
        if campaign == 2: #All
            if self.options.logistic_distribution == 3:  # Starter logistics
                self.__starter_serpulo_logistics()
                self.__starter_erekir_logistics()
            if progressive_drills:
                self.__exclude_serpulo_drills()
                self.__exclude_erekir_drills()
            else:
                self.__exclude_serpulo_progressive_drills()
                self.__exclude_erekir_progressive_drills()
            if progressive_generators:
                self.__exclude_serpulo_generators()
                self.__exclude_erekir_generators()
            else:
                self.__exclude_serpulo_progressive_generators()
                self.__exclude_erekir_progressive_generators()

    def __exclude_serpulo_progressive_drills(self) -> None:
        """Exclude Serpulo progressive drills from the item pool"""
        for x in range(3):
            self.exclude.append("Progressive Drills Serpulo")

    def __exclude_serpulo_progressive_generators(self) -> None:
        """Exclude Serpulo progressive generators from the item pool"""
        for x in range(7):
            self.exclude.append("Progressive Generators Serpulo")

    def __exclude_erekir_progressive_drills(self) -> None:
        """Exclude Erekir progressive drills from the item pool"""
        for x in range(3):
            self.exclude.append("Progressive Drills Erekir")

    def __exclude_erekir_progressive_generators(self) -> None:
        """Exclude Erekir progressive generators from the item pool"""
        for x in range(4):
            self.exclude.append("Progressive Generators Erekir")

    def __starter_serpulo_logistics(self) -> None:
        """Exclude Serpulo logistics items from the item pool for the Starter logistics options"""
        self.multiworld.push_precollected(self.create_item("Conduit"))
        self.exclude.append("Conduit")

        self.multiworld.push_precollected(self.create_item("Liquid Junction"))
        self.exclude.append("Liquid Junction")

        self.multiworld.push_precollected(self.create_item("Liquid Router"))
        self.exclude.append("Liquid Router")

        self.multiworld.push_precollected(self.create_item("Bridge Conduit"))
        self.exclude.append("Bridge Conduit")

        self.multiworld.push_precollected(self.create_item("Junction"))
        self.exclude.append("Junction")

        self.multiworld.push_precollected(self.create_item("Router"))
        self.exclude.append("Router")

        self.multiworld.push_precollected(self.create_item("Bridge Conveyor"))
        self.exclude.append("Bridge Conveyor")

        self.multiworld.push_precollected(self.create_item("Power Node"))
        self.exclude.append("Power Node")

    def __starter_erekir_logistics(self) -> None:
        """Exclude Erekir logistics items from the item pool for the Starter logistics options"""
        self.multiworld.push_precollected(self.create_item("Duct Router"))
        self.exclude.append("Duct Router")

        self.multiworld.push_precollected(self.create_item("Duct Bridge"))
        self.exclude.append("Duct Bridge")

        self.multiworld.push_precollected(self.create_item("Reinforced Conduit"))
        self.exclude.append("Reinforced Conduit")

        self.multiworld.push_precollected(self.create_item("Reinforced Liquid Junction"))
        self.exclude.append("Reinforced Liquid Junction")

        self.multiworld.push_precollected(self.create_item("Reinforced Bridge Conduit"))
        self.exclude.append("Reinforced Bridge Conduit")

        self.multiworld.push_precollected(self.create_item("Reinforced Liquid Router"))
        self.exclude.append("Reinforced Liquid Router")

    def __exclude_serpulo_drills(self):
        self.exclude.append("Pneumatic Drill")
        self.exclude.append("Laser Drill")
        self.exclude.append("Airblast Drill")

    def __exclude_serpulo_generators(self):
        self.exclude.append("Combustion Generator")
        self.exclude.append("Steam Generator")
        self.exclude.append("Thermal Generator")
        self.exclude.append("Differential Generator")
        self.exclude.append("Thorium Reactor")
        self.exclude.append("Impact Reactor")
        self.exclude.append("RTG Generator")


    def __exclude_erekir_drills(self):
        self.exclude.append("Impact Drill")
        self.exclude.append("Large Plasma Bore")
        self.exclude.append("Eruption Drill")

    def __exclude_erekir_generators(self):
        self.exclude.append("Chemical Combustion Chamber")
        self.exclude.append("Pyrolysis Generator")
        self.exclude.append("Flux Reactor")
        self.exclude.append("Neoplasia Reactor")
