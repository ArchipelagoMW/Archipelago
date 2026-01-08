from BaseClasses import Region, MultiWorld, Entrance, ItemClassification
from .Items import MindustryItem
from .Options import MindustryOptions
from .Locations import MindustryLocations, MindustryLocation
from typing import Optional, Dict
from worlds.generic.Rules import set_rule, add_rule
from .Rules import *


class MindustryRegions():
    """
    Class used to create region for Mindustry
    """
    menu: Region
    all_campaign_victory: Region

    serpulo: Region
    node_serpulo_victory: Region
    node_core_shard: Region
    node_conveyor: Region
    node_junction: Region
    node_router: Region
    node_launch_pad: Region
    node_distributor: Region
    node_sorter: Region
    node_inverted_sorter: Region
    node_overflow_gate: Region
    node_underflow_gate: Region
    node_container: Region
    node_unloader: Region
    node_vault: Region
    node_bridge_conveyor: Region
    node_titanium_conveyor: Region
    node_phase_conveyor: Region
    node_mass_driver: Region
    node_payload_conveyor: Region
    node_payload_router: Region
    node_armored_conveyor: Region
    node_plastanium_conveyor: Region
    node_core_foundation: Region
    node_core_nucleus: Region
    node_mechanical_drill: Region
    node_mechanical_pump: Region
    node_conduit: Region
    node_liquid_junction: Region
    node_liquid_router: Region
    node_liquid_container: Region
    node_liquid_tank: Region
    node_bridge_conduit: Region
    node_pulse_conduit: Region
    node_phase_conduit: Region
    node_plated_conduit: Region
    node_rotary_pump: Region
    node_impulse_pump: Region
    node_graphite_press: Region
    node_pneumatic_drill: Region
    node_cultivator: Region
    node_laser_drill: Region
    node_airblast_drill: Region
    node_water_extractor: Region
    node_oil_extractor: Region
    node_pyratite_mixer: Region
    node_blast_mixer: Region
    node_silicon_smelter: Region
    node_spore_press: Region
    node_coal_centrifuge: Region
    node_multi_press: Region
    node_silicon_crucible: Region
    node_plastanium_compressor: Region
    node_phase_weaver: Region
    node_kiln: Region
    node_pulveriser: Region
    node_incinerator: Region
    node_melter: Region
    node_surge_smelter: Region
    node_separator: Region
    node_disassembler: Region
    node_cryofluid_mixer: Region
    node_micro_processor: Region
    node_switch: Region
    node_message: Region
    node_logic_display: Region
    node_large_logic_display: Region
    node_memory_cell: Region
    node_memory_bank: Region
    node_logic_processor: Region
    node_hyper_processor: Region
    node_illuminator: Region
    node_combustion_generator: Region
    node_power_node: Region
    node_large_power_node: Region
    node_battery_diode: Region
    node_surge_tower: Region
    node_battery: Region
    node_large_battery: Region
    node_mender: Region
    node_mend_projector: Region
    node_force_projector: Region
    node_overdrive_projector: Region
    node_overdrive_dome: Region
    node_repair_point: Region
    node_repair_turret: Region
    node_steam_generator: Region
    node_thermal_generator: Region
    node_differential_generator: Region
    node_thorium_reactor: Region
    node_impact_reactor: Region
    node_rtg_generator: Region
    node_solar_panel: Region
    node_large_solar_panel: Region
    node_duo: Region
    node_copper_wall: Region
    node_large_copper_wall: Region
    node_titanium_wall: Region
    node_large_titanium_wall: Region
    node_door: Region
    node_large_door: Region
    node_plastanium_wall: Region
    node_large_plastanium_wall: Region
    node_thorium_wall: Region
    node_large_thorium_wall: Region
    node_surge_wall: Region
    node_large_surge_wall: Region
    node_phase_wall: Region
    node_large_phase_wall: Region
    node_scatter: Region
    node_hail: Region
    node_salvo: Region
    node_swarmer: Region
    node_cyclone: Region
    node_spectre: Region
    node_ripple: Region
    node_fuse: Region
    node_scorch: Region
    node_arc: Region
    node_wave: Region
    node_parallax: Region
    node_segment: Region
    node_tsunami: Region
    node_lancer: Region
    node_meltdown: Region
    node_foreshadow: Region
    node_shock_mine: Region
    node_ground_factory: Region
    node_dagger: Region
    node_mace: Region
    node_fortress: Region
    node_scepter: Region
    node_reign: Region
    node_nova: Region
    node_pulsar: Region
    node_quasar: Region
    node_vela: Region
    node_corvus: Region
    node_crawler: Region
    node_atrax: Region
    node_spiroct: Region
    node_arkyid: Region
    node_toxopid: Region
    node_air_factory: Region
    node_flare: Region
    node_horizon: Region
    node_zenith: Region
    node_antumbra: Region
    node_eclipse: Region
    node_mono: Region
    node_poly: Region
    node_mega: Region
    node_quad: Region
    node_oct: Region
    node_naval_factory: Region
    node_risso: Region
    node_minke: Region
    node_bryde: Region
    node_sei: Region
    node_omura: Region
    node_retusa: Region
    node_oxynoe: Region
    node_cyerce: Region
    node_aegires: Region
    node_navanax: Region
    node_additive_reconstructor: Region
    node_multiplicative_reconstructor: Region
    node_exponential_reconstructor: Region
    node_tetrative_reconstructor: Region

    node_ground_zero: Region
    node_frozen_forest: Region
    node_the_craters: Region
    node_ruinous_shores: Region
    node_windswept_islands: Region
    node_tar_fields: Region
    node_impact_0078: Region
    node_desolate_rift: Region
    node_planetary_launch_terminal: Region
    node_extraction_outpost: Region
    node_salt_flats: Region
    node_coastline: Region
    node_naval_fortress: Region
    node_overgrowth: Region
    node_biomass_synthesis_facility: Region
    node_stained_mountains: Region
    node_fungal_pass: Region
    node_nuclear_production_complex: Region

    node_copper: Region
    node_water_serpulo: Region
    node_sand_serpulo: Region
    node_lead: Region
    node_titanium: Region
    node_cryofluid: Region
    node_thorium_serpulo: Region
    node_surge_alloy_serpulo: Region
    node_phase_fabric_serpulo: Region
    node_metaglass: Region
    node_scrap: Region
    node_slag_serpulo: Region
    node_coal: Region
    node_graphite_serpulo: Region
    node_silicon_serpulo: Region
    node_pyratite: Region
    node_blast_compound: Region
    node_spore_pod: Region
    node_oil: Region
    node_plastanium: Region


    erekir: Region
    node_erekir_victory: Region
    node_core_bastion: Region
    node_duct: Region
    node_duct_router: Region
    node_duct_bridge: Region
    node_armored_duct: Region
    node_surge_conveyor: Region
    node_surge_router: Region
    node_unit_cargo_loader : Region
    node_unit_cargo_unload_point: Region
    node_overflow_duct: Region
    node_underflow_duct: Region
    node_reinforced_container: Region
    node_duct_unloader: Region
    node_reinforced_vault: Region
    node_reinforced_message: Region
    node_canvas: Region
    node_reinforced_payload_conveyor: Region
    node_payload_mass_driver: Region
    node_payload_loader: Region
    node_payload_unloader: Region
    node_large_payload_mass_driver: Region
    node_constructor: Region
    node_deconstructor: Region
    node_large_constructor: Region
    node_large_deconstructor: Region
    node_reinforced_payload_router: Region
    node_plasma_bore: Region
    node_impact_drill: Region
    node_large_plasma_bore: Region
    node_eruption_drill: Region
    node_turbine_condenser: Region
    node_beam_node: Region
    node_vent_condenser: Region
    node_chemical_combustion_chamber: Region
    node_pyrolysis_generator: Region
    node_flux_reactor: Region
    node_neoplasia_reactor: Region
    node_beam_tower: Region
    node_regen_projector: Region
    node_build_tower: Region
    node_shockwave_tower: Region
    node_reinforced_conduit: Region
    node_reinforced_pump: Region
    node_reinforced_liquid_junction: Region
    node_reinforced_bridge_conduit: Region
    node_reinforced_liquid_router: Region
    node_reinforced_liquid_container: Region
    node_reinforced_liquid_tank: Region
    node_cliff_crusher: Region
    node_silicon_arc_furnace: Region
    node_electrolyzer: Region
    node_oxidation_chamber: Region
    node_surge_crucible: Region
    node_heat_redirector: Region
    node_electric_heater: Region
    node_slag_heater: Region
    node_atmospheric_concentrator: Region
    node_cyanogen_synthesizer: Region
    node_carbide_crucible: Region
    node_phase_synthesizer: Region
    node_phase_heater: Region
    node_heat_router: Region
    node_slag_incinerator: Region
    node_breach: Region
    node_beryllium_wall: Region
    node_large_beryllium_wall: Region
    node_tungsten_wall: Region
    node_large_tungsten_wall: Region
    node_blast_door: Region
    node_reinforced_surge_wall: Region
    node_large_reinforced_surge_wall: Region
    node_shielded_wall: Region
    node_carbide_wall: Region
    node_large_carbide_wall: Region
    node_diffuse: Region
    node_sublimate: Region
    node_afflict: Region
    node_titan: Region
    node_lustre: Region
    node_smite: Region
    node_disperse: Region
    node_scathe: Region
    node_malign: Region
    node_radar: Region
    node_core_citadel: Region
    node_core_acropolis: Region
    node_tank_fabricator: Region
    node_stell: Region
    node_unit_repair_tower: Region
    node_ship_fabricator: Region
    node_elude: Region
    node_mech_fabricator: Region
    node_merui: Region
    node_tank_refabricator: Region
    node_locus: Region
    node_mech_refabricator: Region
    node_cleroi: Region
    node_ship_refabricator: Region
    node_avert: Region
    node_prime_refabricator: Region
    node_precept: Region
    node_anthicus: Region
    node_obviate: Region
    node_tank_assembler: Region
    node_vanquish: Region
    node_conquer: Region
    node_ship_assembler: Region
    node_quell: Region
    node_disrupt: Region
    node_mech_assembler: Region
    node_tecta: Region
    node_collaris: Region
    node_basic_assembler_module: Region

    node_the_onset : Region
    node_aegis: Region
    node_lake: Region
    node_intersect: Region
    node_atlas: Region
    node_split: Region
    node_basin: Region
    node_marsh: Region
    node_ravine: Region
    node_caldera: Region
    node_stronghold: Region
    node_crevice: Region
    node_siege: Region
    node_crossroads: Region
    node_karst: Region
    node_origin: Region
    node_peaks: Region

    node_beryllium: Region
    node_sand_erekir: Region
    node_silicon_erekir: Region
    node_oxide: Region
    node_water_erekir: Region
    node_ozone: Region
    node_hydrogen: Region
    node_nitrogen: Region
    node_cyanogen: Region
    node_neoplasm: Region
    node_graphite_erekir: Region
    node_tungsten: Region
    node_slag_erekir: Region
    node_arkycite: Region
    node_carbide: Region
    node_thorium_erekir: Region
    node_surge_alloy_erekir: Region
    node_phase_fabric_erekir: Region


    multiworld: MultiWorld
    """
    Current Multiworld game
    """

    player: int
    """
    Player Id
    """


    def connect_regions(self, options: MindustryOptions) -> None:
        """
        Connect regions based on user options.
        """
        if options.campaign_choice.value == 0:
            self.__connect_serpulo_campaign(options)
        elif options.campaign_choice.value == 1:
            self.__connect_erekir_campaign(options)
        elif options.campaign_choice.value == 2:
            self.__connect_all_campaign(options)

    def add_regions_to_world(self) -> None:
        """
        Add every region to the `world`
        """
        pass

    def add_event_locations(self, options: MindustryOptions) -> None:
        """
        Add events based on user options.
        """
        if options.campaign_choice.value == 0:
            self.__add_serpulo_events()
        elif options.campaign_choice.value == 1:
            self.__add_erekir_events()
        elif options.campaign_choice.value == 2:
            self.__add_all_events()

    def initialise_rules(self, options: MindustryOptions) -> None:
        """Initialise rules based on user options"""
        if options.campaign_choice.value == 0: #Serpulo
            self.__initialise_serpulo_rules()
            if options.military_level_tracking:
                self.__apply_serpulo_military_level_rules()
        elif options.campaign_choice.value == 1: #Erekir
            self.__initialise_erekir_rules()
            if options.military_level_tracking:
                self.__apply_erekir_military_level_rules()
        elif options.campaign_choice.value == 2: #All
            self.__initialise_all_rules()
            if options.military_level_tracking:
                self.__apply_serpulo_military_level_rules()
                self.__apply_erekir_military_level_rules()

    def create_campaign(self, options: MindustryOptions) -> None:
        """
        Create region for selected campaign
        """
        self.menu = self.__add_region("Menu", None)

        if options.campaign_choice.value == 0:
            self.__create_serpulo_campaign()
        elif options.campaign_choice.value == 1:
            self.__create_erekir_campaign()
        elif options.campaign_choice.value == 2:
            self.__create_all_campaign()


    def __init__(self, multiworld: MultiWorld, player: int):
        """
        Initialisation of the regions
        """
        super().__init__()
        self.multiworld = multiworld
        self.player = player


    def __add_event_location(self, region: Region, name: str, event_name: str) -> None:
        """
        Add an event to the `region` with the name `name` and the item
        `event_name`
        """
        location: MindustryLocation = MindustryLocation(
            self.player, name, None, region
        )
        region.locations.append(location)
        location.place_locked_item(MindustryItem(event_name, ItemClassification.progression, None, self.player))

    def __create_serpulo_campaign(self):
        """
        Create region related to the serpulo campaign.
        """
        self.serpulo: Region = self.__add_region("Serpulo", None)
        self.node_serpulo_victory = self.__add_region("Victory Serpulo", None)

        self.node_core_shard = self.__add_region("Core: Shard", None)

        self.node_conveyor = self.__add_region("Conveyor", None)
        self.node_junction = self.__add_region("AP-S-01-02", MindustryLocations.serpulo_junction)
        self.node_router = self.__add_region("AP-S-01-03", MindustryLocations.serpulo_router)
        self.node_launch_pad = self.__add_region("AP-S-01-04", MindustryLocations.serpulo_launch_pad)
        self.node_distributor = self.__add_region("AP-S-01-05", MindustryLocations.serpulo_distributor)
        self.node_sorter = self.__add_region("AP-S-01-06", MindustryLocations.serpulo_sorter)
        self.node_inverted_sorter = self.__add_region("AP-S-01-07", MindustryLocations.serpulo_inverted_sorter)
        self.node_overflow_gate = self.__add_region("AP-S-01-08", MindustryLocations.serpulo_overflow_gate)
        self.node_underflow_gate = self.__add_region("AP-S-01-09", MindustryLocations.serpulo_underflow_gate)
        self.node_container = self.__add_region("AP-S-01-10", MindustryLocations.serpulo_container)
        self.node_unloader = self.__add_region("AP-S-01-11", MindustryLocations.serpulo_unloader)
        self.node_vault = self.__add_region("AP-S-01-12", MindustryLocations.serpulo_vault)
        self.node_bridge_conveyor = self.__add_region("AP-S-01-13", MindustryLocations.serpulo_bridge_conveyor)
        self.node_titanium_conveyor = self.__add_region("AP-S-01-14", MindustryLocations.serpulo_titanium_conveyor)
        self.node_phase_conveyor = self.__add_region("AP-S-01-15", MindustryLocations.serpulo_phase_conveyor)
        self.node_mass_driver = self.__add_region("AP-S-01-16", MindustryLocations.serpulo_mass_driver)
        self.node_payload_conveyor = self.__add_region("AP-S-01-17", MindustryLocations.serpulo_payload_conveyor)
        self.node_payload_router = self.__add_region("AP-S-01-18", MindustryLocations.serpulo_payload_router)
        self.node_armored_conveyor = self.__add_region("AP-S-01-19", MindustryLocations.serpulo_armored_conveyor)
        self.node_plastanium_conveyor = self.__add_region("AP-S-01-20", MindustryLocations.serpulo_plastanium_conveyor)

        self.node_core_foundation = self.__add_region("AP-S-02-01", MindustryLocations.serpulo_core_foundation)
        self.node_core_nucleus = self.__add_region("AP-S-02-02", MindustryLocations.serpulo_core_nucleus)

        self.node_mechanical_drill = self.__add_region("Mechanical Drill", None)
        self.node_mechanical_pump = self.__add_region("AP-S-03-02", MindustryLocations.serpulo_mechanical_pump)
        self.node_conduit = self.__add_region("AP-S-03-03", MindustryLocations.serpulo_conduit)
        self.node_liquid_junction = self.__add_region("AP-S-03-04", MindustryLocations.serpulo_liquid_junction)
        self.node_liquid_router = self.__add_region("AP-S-03-05", MindustryLocations.serpulo_liquid_router)
        self.node_liquid_container = self.__add_region("AP-S-03-06", MindustryLocations.serpulo_liquid_container)
        self.node_liquid_tank = self.__add_region("AP-S-03-07", MindustryLocations.serpulo_liquid_tank)
        self.node_bridge_conduit = self.__add_region("AP-S-03-08", MindustryLocations.serpulo_bridge_conduit)
        self.node_pulse_conduit = self.__add_region("AP-S-03-09", MindustryLocations.serpulo_pulse_conduit)
        self.node_phase_conduit = self.__add_region("AP-S-03-10", MindustryLocations.serpulo_phase_conduit)
        self.node_plated_conduit = self.__add_region("AP-S-03-11", MindustryLocations.serpulo_plated_conduit)
        self.node_rotary_pump = self.__add_region("AP-S-03-12", MindustryLocations.serpulo_rotary_pump)
        self.node_impulse_pump = self.__add_region("AP-S-03-13", MindustryLocations.serpulo_impulse_pump)
        self.node_graphite_press = self.__add_region("AP-S-03-14", MindustryLocations.serpulo_graphite_press)
        self.node_pneumatic_drill = self.__add_region("AP-S-03-15", MindustryLocations.serpulo_pneumatic_drill)
        self.node_cultivator = self.__add_region("AP-S-03-16", MindustryLocations.serpulo_cultivator)
        self.node_laser_drill = self.__add_region("AP-S-03-17", MindustryLocations.serpulo_laser_drill)
        self.node_airblast_drill = self.__add_region("AP-S-03-18", MindustryLocations.serpulo_airblast_drill)
        self.node_water_extractor = self.__add_region("AP-S-03-19", MindustryLocations.serpulo_water_extractor)
        self.node_oil_extractor = self.__add_region("AP-S-03-20", MindustryLocations.serpulo_oil_extractor)
        self.node_pyratite_mixer = self.__add_region("AP-S-03-21", MindustryLocations.serpulo_pyratite_mixer)
        self.node_blast_mixer = self.__add_region("AP-S-03-22", MindustryLocations.serpulo_blast_mixer)
        self.node_silicon_smelter = self.__add_region("AP-S-03-23", MindustryLocations.serpulo_silicon_smelter)
        self.node_spore_press = self.__add_region("AP-S-03-24", MindustryLocations.serpulo_spore_press)
        self.node_coal_centrifuge = self.__add_region("AP-S-03-25", MindustryLocations.serpulo_coal_centrifuge)
        self.node_multi_press = self.__add_region("AP-S-03-26", MindustryLocations.serpulo_multi_press)
        self.node_silicon_crucible = self.__add_region("AP-S-03-27", MindustryLocations.serpulo_silicon_crucible)
        self.node_plastanium_compressor = self.__add_region("AP-S-03-28", MindustryLocations.serpulo_plastanium_compressor)
        self.node_phase_weaver = self.__add_region("AP-S-03-29", MindustryLocations.serpulo_phase_weaver)
        self.node_kiln = self.__add_region("AP-S-03-30", MindustryLocations.serpulo_kiln)
        self.node_pulveriser = self.__add_region("AP-S-03-31", MindustryLocations.serpulo_pulveriser)
        self.node_incinerator = self.__add_region("AP-S-03-32", MindustryLocations.serpulo_incinerator)
        self.node_melter = self.__add_region("AP-S-03-33", MindustryLocations.serpulo_melter)
        self.node_surge_smelter = self.__add_region("AP-S-03-34", MindustryLocations.serpulo_surge_smelter)
        self.node_separator = self.__add_region("AP-S-03-35", MindustryLocations.serpulo_separator)
        self.node_disassembler = self.__add_region("AP-S-03-36", MindustryLocations.serpulo_disassembler)
        self.node_cryofluid_mixer = self.__add_region("AP-S-03-37", MindustryLocations.serpulo_cryofluid_mixer)
        self.node_micro_processor = self.__add_region("AP-S-03-38", MindustryLocations.serpulo_micro_processor)
        self.node_switch = self.__add_region("AP-S-03-39", MindustryLocations.serpulo_switch)
        self.node_message = self.__add_region("AP-S-03-40", MindustryLocations.serpulo_message)
        self.node_logic_display = self.__add_region("AP-S-03-41", MindustryLocations.serpulo_logic_display)
        self.node_large_logic_display = self.__add_region("AP-S-03-42", MindustryLocations.serpulo_large_logic_display)
        self.node_memory_cell = self.__add_region("AP-S-03-43", MindustryLocations.serpulo_memory_cell)
        self.node_memory_bank = self.__add_region("AP-S-03-44", MindustryLocations.serpulo_memory_bank)
        self.node_logic_processor = self.__add_region("AP-S-03-45", MindustryLocations.serpulo_logic_processor)
        self.node_hyper_processor = self.__add_region("AP-S-03-46", MindustryLocations.serpulo_hyper_processor)
        self.node_illuminator = self.__add_region("AP-S-03-47", MindustryLocations.serpulo_illuminator)
        self.node_combustion_generator = self.__add_region("AP-S-03-48", MindustryLocations.serpulo_combustion_generator)
        self.node_power_node = self.__add_region("AP-S-03-49", MindustryLocations.serpulo_power_node)
        self.node_large_power_node = self.__add_region("AP-S-03-50", MindustryLocations.serpulo_large_power_node)
        self.node_battery_diode = self.__add_region("AP-S-03-51", MindustryLocations.serpulo_battery_diode)
        self.node_surge_tower = self.__add_region("AP-S-03-52", MindustryLocations.serpulo_surge_tower)
        self.node_battery = self.__add_region("AP-S-03-53", MindustryLocations.serpulo_battery)
        self.node_large_battery = self.__add_region("AP-S-03-54", MindustryLocations.serpulo_large_battery)
        self.node_mender = self.__add_region("AP-S-03-55", MindustryLocations.serpulo_mender)
        self.node_mend_projector = self.__add_region("AP-S-03-56", MindustryLocations.serpulo_mend_projector)
        self.node_force_projector = self.__add_region("AP-S-03-57", MindustryLocations.serpulo_force_projector)
        self.node_overdrive_projector = self.__add_region("AP-S-03-58", MindustryLocations.serpulo_overdrive_projector)
        self.node_overdrive_dome = self.__add_region("AP-S-03-59", MindustryLocations.serpulo_overdrive_dome)
        self.node_repair_point = self.__add_region("AP-S-03-60", MindustryLocations.serpulo_repair_point)
        self.node_repair_turret = self.__add_region("AP-S-03-61", MindustryLocations.serpulo_repair_turret)
        self.node_steam_generator = self.__add_region("AP-S-03-62", MindustryLocations.serpulo_steam_generator)
        self.node_thermal_generator = self.__add_region("AP-S-03-63", MindustryLocations.serpulo_thermal_generator)
        self.node_differential_generator = self.__add_region("AP-S-03-64", MindustryLocations.serpulo_differential_generator)
        self.node_thorium_reactor = self.__add_region("AP-S-03-65", MindustryLocations.serpulo_thorium_reactor)
        self.node_impact_reactor = self.__add_region("AP-S-03-66", MindustryLocations.serpulo_impact_reactor)
        self.node_rtg_generator = self.__add_region("AP-S-03-67", MindustryLocations.serpulo_rtg_generator)
        self.node_solar_panel = self.__add_region("AP-S-03-68", MindustryLocations.serpulo_solar_panel)
        self.node_large_solar_panel = self.__add_region("AP-S-03-69", MindustryLocations.serpulo_large_solar_panel)

        self.node_duo = self.__add_region("Duo", None)
        self.node_copper_wall = self.__add_region("Copper Wall", None)
        self.node_large_copper_wall = self.__add_region("AP-S-04-03", MindustryLocations.serpulo_large_copper_wall)
        self.node_titanium_wall = self.__add_region("AP-S-04-04", MindustryLocations.serpulo_titanium_wall)
        self.node_large_titanium_wall = self.__add_region("AP-S-04-05", MindustryLocations.serpulo_large_titanium_wall)
        self.node_door = self.__add_region("AP-S-04-06", MindustryLocations.serpulo_door)
        self.node_large_door = self.__add_region("AP-S-04-07", MindustryLocations.serpulo_large_door)
        self.node_plastanium_wall = self.__add_region("AP-S-04-08", MindustryLocations.serpulo_plastanium_wall)
        self.node_large_plastanium_wall = self.__add_region("AP-S-04-09", MindustryLocations.serpulo_large_plastanium_wall)
        self.node_thorium_wall = self.__add_region("AP-S-04-10", MindustryLocations.serpulo_thorium_wall)
        self.node_large_thorium_wall = self.__add_region("AP-S-04-11", MindustryLocations.serpulo_large_thorium_wall)
        self.node_surge_wall = self.__add_region("AP-S-04-12", MindustryLocations.serpulo_surge_wall)
        self.node_large_surge_wall = self.__add_region("AP-S-04-13", MindustryLocations.serpulo_large_surge_wall)
        self.node_phase_wall = self.__add_region("AP-S-04-14", MindustryLocations.serpulo_phase_wall)
        self.node_large_phase_wall = self.__add_region("AP-S-04-15", MindustryLocations.serpulo_large_phase_wall)
        self.node_scatter = self.__add_region("Scatter", None)
        self.node_hail = self.__add_region("AP-S-04-17", MindustryLocations.serpulo_hail)
        self.node_salvo = self.__add_region("AP-S-04-18", MindustryLocations.serpulo_salvo)
        self.node_swarmer = self.__add_region("AP-S-04-19", MindustryLocations.serpulo_swarmer)
        self.node_cyclone = self.__add_region("AP-S-04-20", MindustryLocations.serpulo_cyclone)
        self.node_spectre = self.__add_region("AP-S-04-21", MindustryLocations.serpulo_spectre)
        self.node_ripple = self.__add_region("AP-S-04-22", MindustryLocations.serpulo_ripple)
        self.node_fuse = self.__add_region("AP-S-04-23", MindustryLocations.serpulo_fuse)
        self.node_scorch = self.__add_region("AP-S-04-24", MindustryLocations.serpulo_scorch)
        self.node_arc = self.__add_region("AP-S-04-25", MindustryLocations.serpulo_arc)
        self.node_wave = self.__add_region("AP-S-04-26", MindustryLocations.serpulo_wave)
        self.node_parallax = self.__add_region("AP-S-04-27", MindustryLocations.serpulo_parallax)
        self.node_segment = self.__add_region("AP-S-04-28", MindustryLocations.serpulo_segment)
        self.node_tsunami = self.__add_region("AP-S-04-29", MindustryLocations.serpulo_tsunami)
        self.node_lancer = self.__add_region("AP-S-04-30", MindustryLocations.serpulo_lancer)
        self.node_meltdown = self.__add_region("AP-S-04-31", MindustryLocations.serpulo_meltdown)
        self.node_foreshadow = self.__add_region("AP-S-04-32", MindustryLocations.serpulo_foreshadow)
        self.node_shock_mine = self.__add_region("AP-S-04-33", MindustryLocations.serpulo_shock_mine)

        self.node_ground_factory = self.__add_region("AP-S-05-01", MindustryLocations.serpulo_ground_factory)
        self.node_dagger = self.__add_region("AP-S-05-02", MindustryLocations.serpulo_dagger)
        self.node_mace = self.__add_region("AP-S-05-03", MindustryLocations.serpulo_mace)
        self.node_fortress = self.__add_region("AP-S-05-04", MindustryLocations.serpulo_fortress)
        self.node_scepter = self.__add_region("AP-S-05-05", MindustryLocations.serpulo_scepter)
        self.node_reign = self.__add_region("AP-S-05-06", MindustryLocations.serpulo_reign)
        self.node_nova = self.__add_region("AP-S-05-07", MindustryLocations.serpulo_nova)
        self.node_pulsar = self.__add_region("AP-S-05-08", MindustryLocations.serpulo_pulsar)
        self.node_quasar = self.__add_region("AP-S-05-09", MindustryLocations.serpulo_quasar)
        self.node_vela = self.__add_region("AP-S-05-10", MindustryLocations.serpulo_vela)
        self.node_corvus = self.__add_region("AP-S-05-11", MindustryLocations.serpulo_corvus)
        self.node_crawler = self.__add_region("AP-S-05-12", MindustryLocations.serpulo_crawler)
        self.node_atrax = self.__add_region("AP-S-05-13", MindustryLocations.serpulo_atrax)
        self.node_spiroct = self.__add_region("AP-S-05-14", MindustryLocations.serpulo_spiroct)
        self.node_arkyid = self.__add_region("AP-S-05-15", MindustryLocations.serpulo_arkyid)
        self.node_toxopid = self.__add_region("AP-S-05-16", MindustryLocations.serpulo_toxopid)
        self.node_air_factory = self.__add_region("AP-S-05-17", MindustryLocations.serpulo_air_factory)
        self.node_flare = self.__add_region("AP-S-05-18", MindustryLocations.serpulo_flare)
        self.node_horizon = self.__add_region("AP-S-05-19", MindustryLocations.serpulo_horizon)
        self.node_zenith = self.__add_region("AP-S-05-20", MindustryLocations.serpulo_zenith)
        self.node_antumbra = self.__add_region("AP-S-05-21", MindustryLocations.serpulo_antumbra)
        self.node_eclipse = self.__add_region("AP-S-05-22", MindustryLocations.serpulo_eclipse)
        self.node_mono = self.__add_region("AP-S-05-23", MindustryLocations.serpulo_mono)
        self.node_poly = self.__add_region("AP-S-05-24", MindustryLocations.serpulo_poly)
        self.node_mega = self.__add_region("AP-S-05-25", MindustryLocations.serpulo_mega)
        self.node_quad = self.__add_region("AP-S-05-26", MindustryLocations.serpulo_quad)
        self.node_oct = self.__add_region("AP-S-05-27", MindustryLocations.serpulo_oct)
        self.node_naval_factory = self.__add_region("AP-S-05-28", MindustryLocations.serpulo_naval_factory)
        self.node_risso = self.__add_region("AP-S-05-29", MindustryLocations.serpulo_risso)
        self.node_minke = self.__add_region("AP-S-05-30", MindustryLocations.serpulo_minke)
        self.node_bryde = self.__add_region("AP-S-05-31", MindustryLocations.serpulo_bryde)
        self.node_sei = self.__add_region("AP-S-05-32", MindustryLocations.serpulo_sei)
        self.node_omura = self.__add_region("AP-S-05-33", MindustryLocations.serpulo_omura)
        self.node_retusa = self.__add_region("AP-S-05-34", MindustryLocations.serpulo_retusa)
        self.node_oxynoe = self.__add_region("AP-S-05-35", MindustryLocations.serpulo_oxynoe)
        self.node_cyerce = self.__add_region("AP-S-05-36", MindustryLocations.serpulo_cyerce)
        self.node_aegires = self.__add_region("AP-S-05-37", MindustryLocations.serpulo_aegires)
        self.node_navanax = self.__add_region("AP-S-05-38", MindustryLocations.serpulo_navanax)
        self.node_additive_reconstructor = self.__add_region("AP-S-05-39", MindustryLocations.serpulo_additive_reconstructor)
        self.node_multiplicative_reconstructor = self.__add_region("AP-S-05-40", MindustryLocations.serpulo_multiplicative_reconstructor)
        self.node_exponential_reconstructor = self.__add_region("AP-S-05-41", MindustryLocations.serpulo_exponential_reconstructor)
        self.node_tetrative_reconstructor = self.__add_region("AP-S-05-42", MindustryLocations.serpulo_tetrative_reconstructor)

        self.node_ground_zero = self.__add_region("Ground Zero", None)
        self.node_frozen_forest = self.__add_region("Frozen Forest", None)
        self.node_the_craters = self.__add_region("The Craters", None)
        self.node_ruinous_shores = self.__add_region("Ruinous Shores", None)
        self.node_windswept_islands = self.__add_region("Windswept Islands", None)
        self.node_tar_fields = self.__add_region("Tar Fields", None)
        self.node_impact_0078 = self.__add_region("Impact 0078", None)
        self.node_desolate_rift = self.__add_region("Desolate Rift", None)
        self.node_planetary_launch_terminal = self.__add_region("Planetary Launch Terminal", None)
        self.node_extraction_outpost = self.__add_region("Extraction Outpost", None)
        self.node_salt_flats = self.__add_region("Salt Flats", None)
        self.node_coastline = self.__add_region("Coastline", None)
        self.node_naval_fortress = self.__add_region("Naval Fortress", None)
        self.node_overgrowth = self.__add_region("Overgrowth", None)
        self.node_biomass_synthesis_facility = self.__add_region("Biomass Synthesis Facility", None)
        self.node_stained_mountains = self.__add_region("Stained Mountains", None)
        self.node_fungal_pass = self.__add_region("Fungal Pass", None)
        self.node_nuclear_production_complex = self.__add_region("Nuclear Production Complex", None)

        self.node_copper = self.__add_region("Copper", None)
        self.node_water_serpulo = self.__add_region("Water Serpulo", None)
        self.node_sand_serpulo = self.__add_region("Sand Serpulo", None)
        self.node_lead = self.__add_region("Lead", None)
        self.node_titanium = self.__add_region("Titanium", None)
        self.node_cryofluid = self.__add_region("Cryofluid", None)
        self.node_thorium_serpulo = self.__add_region("Thorium Serpulo", None)
        self.node_surge_alloy_serpulo = self.__add_region("Surge Alloy Serpulo", None)
        self.node_phase_fabric_serpulo = self.__add_region("Phase Fabric Serpulo", None)
        self.node_metaglass = self.__add_region("Metaglass", None)
        self.node_scrap = self.__add_region("Scrap", None)
        self.node_slag_serpulo = self.__add_region("Slag Serpulo", None)
        self.node_coal = self.__add_region("Coal", None)
        self.node_graphite_serpulo = self.__add_region("Graphite Serpulo", None)
        self.node_silicon_serpulo = self.__add_region("Silicon Serpulo", None)
        self.node_pyratite = self.__add_region("Pyratite", None)
        self.node_blast_compound = self.__add_region("Blast Compound", None)
        self.node_spore_pod = self.__add_region("Spore Pod", None)
        self.node_oil = self.__add_region("Oil", None)
        self.node_plastanium = self.__add_region("Plastanium", None)


    def __connect_serpulo_campaign(self, options: MindustryOptions):
        """
        Connect region related to Serpulo's campaign
        """
        self.__connect_regions(self.menu, self.serpulo)
        if options.goal == 0: #resources
            self.__connect_serpulo_resources_goal()
        elif options.goal == 1: #conquest
            self.__connect_serpulo_conquest_goal()
        else:
            self.__connect_serpulo_resources_goal() # default to resources for now

        self.__connect_regions(self.serpulo, self.node_core_shard)

        self.__connect_regions(self.node_core_shard, self.node_conveyor)
        self.__connect_regions(self.node_conveyor, self.node_junction)
        self.__connect_regions(self.node_junction, self.node_router)

        self.__connect_regions(self.node_router, self.node_launch_pad,
                               lambda state: has_extraction_outpost(state, self.player) and
                                             has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))

        self.__connect_regions(self.node_router, self.node_distributor)

        self.__connect_regions(self.node_router, self.node_sorter)
        self.__connect_regions(self.node_sorter, self.node_inverted_sorter)
        self.__connect_regions(self.node_sorter, self.node_overflow_gate)
        self.__connect_regions(self.node_overflow_gate, self.node_underflow_gate)

        self.__connect_regions(self.node_router, self.node_container,
                               lambda state: has_biomass_synthesis_facility(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_container, self.node_unloader,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_container, self.node_vault,
                               lambda state: has_stained_mountains(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_router, self.node_bridge_conveyor)
        self.__connect_regions(self.node_bridge_conveyor, self.node_titanium_conveyor,
                               lambda state: has_the_craters(state, self.player) and
                                             has_titanium(state, self.player))

        self.__connect_regions(self.node_titanium_conveyor, self.node_phase_conveyor,
                               lambda state: has_graphite_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player) and
                                             has_phase_fabric_serpulo(state, self.player))
        self.__connect_regions(self.node_phase_conveyor, self.node_mass_driver,
                               lambda state: has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_titanium_conveyor, self.node_payload_conveyor,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_payload_conveyor, self.node_payload_router)

        self.__connect_regions(self.node_titanium_conveyor, self.node_armored_conveyor,
                               lambda state: has_plastanium(state, self.player) and
                                             has_thorium_serpulo(state, self.player) and
                                             has_metaglass(state, self.player))
        self.__connect_regions(self.node_armored_conveyor, self.node_plastanium_conveyor,
                               lambda state: has_graphite_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_core_shard, self.node_core_foundation,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_core_foundation, self.node_core_nucleus,
                               lambda state: has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_core_shard, self.node_mechanical_drill)
        self.__connect_regions(self.node_mechanical_drill, self.node_mechanical_pump,
                               lambda state: has_metaglass(state, self.player))

        self.__connect_regions(self.node_mechanical_pump, self.node_conduit)
        self.__connect_regions(self.node_conduit, self.node_liquid_junction,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_liquid_junction, self.node_liquid_router)

        self.__connect_regions(self.node_liquid_router, self.node_liquid_container,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_liquid_container, self.node_liquid_tank)

        self.__connect_regions(self.node_liquid_router, self.node_bridge_conduit)

        self.__connect_regions(self.node_liquid_router, self.node_pulse_conduit,
                               lambda state: has_windswept_islands(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_pulse_conduit, self.node_phase_conduit,
                               lambda state: has_phase_fabric_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_pulse_conduit, self.node_plated_conduit,
                               lambda state: has_thorium_serpulo(state, self.player) and
                                             has_plastanium(state, self.player))

        self.__connect_regions(self.node_pulse_conduit, self.node_rotary_pump,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_rotary_pump, self.node_impulse_pump,
                               lambda state: has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_mechanical_drill, self.node_graphite_press)

        self.__connect_regions(self.node_graphite_press, self.node_pneumatic_drill,
                               lambda state: has_frozen_forest(state, self.player) and
                                             has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_pneumatic_drill, self.node_cultivator,
                               lambda state: has_biomass_synthesis_facility(state, self.player) and
                                             has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_pneumatic_drill, self.node_laser_drill,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_laser_drill, self.node_airblast_drill,
                               lambda state: has_thorium_serpulo(state, self.player) and
                                             has_nuclear_production_complex(state, self.player))

        self.__connect_regions(self.node_laser_drill, self.node_water_extractor,
                               lambda state: has_salt_flats(state, self.player) and
                                             has_metaglass(state, self.player))
        self.__connect_regions(self.node_water_extractor, self.node_oil_extractor,
                               lambda state: has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_graphite_press, self.node_pyratite_mixer)
        self.__connect_regions(self.node_pyratite_mixer, self.node_blast_mixer,
                               lambda state: has_titanium(state, self.player))

        self.__connect_regions(self.node_graphite_press, self.node_silicon_smelter)

        self.__connect_regions(self.node_silicon_smelter, self.node_spore_press,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_spore_press, self.node_coal_centrifuge,
                               lambda state: has_titanium(state, self.player) and
                                             has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_coal_centrifuge, self.node_multi_press)
        self.__connect_regions(self.node_multi_press, self.node_silicon_crucible,
                               lambda state: has_metaglass(state, self.player) and
                                            has_plastanium(state, self.player))

        self.__connect_regions(self.node_spore_press, self.node_plastanium_compressor,
                               lambda state: has_windswept_islands(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_plastanium_compressor, self.node_phase_weaver,
                               lambda state: has_tar_fields(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_silicon_smelter, self.node_kiln,
                               lambda state: has_the_craters(state, self.player) and
                                             has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_kiln, self.node_pulveriser)
        self.__connect_regions(self.node_pulveriser, self.node_incinerator)
        self.__connect_regions(self.node_incinerator, self.node_melter)
        self.__connect_regions(self.node_melter, self.node_surge_smelter,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_melter, self.node_separator,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_separator, self.node_disassembler,
                               lambda state: has_plastanium(state, self.player) and
                                             has_silicon_serpulo(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_melter, self.node_cryofluid_mixer,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))

        self.__connect_regions(self.node_silicon_smelter, self.node_micro_processor,
                               lambda state: has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_micro_processor, self.node_switch,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_switch, self.node_message)
        self.__connect_regions(self.node_message, self.node_logic_display,
                               lambda state: has_metaglass(state, self.player))
        self.__connect_regions(self.node_logic_display, self.node_large_logic_display,
                               lambda state: has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_message, self.node_memory_cell)
        self.__connect_regions(self.node_memory_cell, self.node_memory_bank,
                               lambda state: has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_switch, self.node_logic_processor,
                               lambda state: has_thorium_serpulo(state, self.player))
        self.__connect_regions(self.node_logic_processor, self.node_hyper_processor,
                               lambda state: has_surge_alloy_serpulo(state, self.player))

        self.__connect_regions(self.node_silicon_smelter, self.node_illuminator,
                               lambda state: has_graphite_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_mechanical_drill, self.node_combustion_generator)
        self.__connect_regions(self.node_combustion_generator, self.node_power_node)
        self.__connect_regions(self.node_power_node, self.node_large_power_node,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_large_power_node, self.node_battery_diode,
                               lambda state: has_plastanium(state, self.player) and
                                            has_metaglass(state, self.player))
        self.__connect_regions(self.node_battery_diode, self.node_surge_tower,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_titanium(state, self.player))

        self.__connect_regions(self.node_power_node, self.node_battery)
        self.__connect_regions(self.node_battery, self.node_large_battery,
                               lambda state: has_titanium(state, self.player) and
                                             has_silicon_serpulo(state, self.player))

        self.__connect_regions(self.node_power_node, self.node_mender)
        self.__connect_regions(self.node_mender, self.node_mend_projector,
                               lambda state: has_titanium(state, self.player) and
                                             has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_mend_projector, self.node_force_projector,
                                lambda state: has_impact_0078(state, self.player))
        self.__connect_regions(self.node_force_projector, self.node_overdrive_projector,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_overdrive_projector, self.node_overdrive_dome,
                               lambda state: has_surge_alloy_serpulo(state, self.player))

        self.__connect_regions(self.node_mend_projector, self.node_repair_point)
        self.__connect_regions(self.node_repair_point, self.node_repair_turret,
                               lambda state: has_thorium_serpulo(state, self.player) and
                                             has_plastanium(state, self.player))

        self.__connect_regions(self.node_power_node, self.node_steam_generator,
                               lambda state: has_the_craters(state, self.player) and
                                             has_graphite_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_steam_generator, self.node_thermal_generator,
                               lambda state: has_metaglass(state, self.player))
        self.__connect_regions(self.node_thermal_generator, self.node_differential_generator,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_differential_generator, self.node_thorium_reactor,
                               lambda state: has_thorium_serpulo(state, self.player))
        self.__connect_regions(self.node_thorium_reactor, self.node_impact_reactor,
                               lambda state: has_surge_alloy_serpulo(state, self.player))

        self.__connect_regions(self.node_thorium_reactor, self.node_rtg_generator,
                               lambda state: has_phase_fabric_serpulo(state, self.player) and
                                            has_plastanium(state, self.player))

        self.__connect_regions(self.node_power_node, self.node_solar_panel,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_solar_panel, self.node_large_solar_panel,
                               lambda state: has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_core_shard, self.node_duo)
        self.__connect_regions(self.node_duo, self.node_copper_wall)
        self.__connect_regions(self.node_copper_wall, self.node_large_copper_wall)
        self.__connect_regions(self.node_large_copper_wall, self.node_titanium_wall,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_titanium_wall, self.node_large_titanium_wall)
        self.__connect_regions(self.node_titanium_wall, self.node_door,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_door, self.node_large_door)
        self.__connect_regions(self.node_titanium_wall, self.node_plastanium_wall,
                               lambda state: has_metaglass(state, self.player) and
                                            has_plastanium(state, self.player))
        self.__connect_regions(self.node_plastanium_wall, self.node_large_plastanium_wall)
        self.__connect_regions(self.node_titanium_wall, self.node_thorium_wall,
                               lambda state: has_thorium_serpulo(state, self.player))
        self.__connect_regions(self.node_thorium_wall, self.node_large_thorium_wall)

        self.__connect_regions(self.node_thorium_wall, self.node_surge_wall,
                               lambda state: has_surge_alloy_serpulo(state, self.player))
        self.__connect_regions(self.node_surge_wall, self.node_large_surge_wall)
        self.__connect_regions(self.node_surge_wall, self.node_phase_wall,
                               lambda state: has_phase_fabric_serpulo(state, self.player))
        self.__connect_regions(self.node_phase_wall, self.node_large_phase_wall)

        self.__connect_regions(self.node_duo, self.node_scatter)
        self.__connect_regions(self.node_scatter, self.node_hail,
                               lambda state: has_graphite_serpulo(state, self.player) and
                                             has_the_craters(state, self.player))
        self.__connect_regions(self.node_hail, self.node_salvo,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_salvo, self.node_swarmer,
                               lambda state: has_plastanium(state, self.player) and
                                             has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_swarmer, self.node_cyclone)
        self.__connect_regions(self.node_cyclone, self.node_spectre,
                               lambda state: has_nuclear_production_complex(state, self.player) and
                                             has_surge_alloy_serpulo(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_salvo, self.node_ripple)
        self.__connect_regions(self.node_ripple, self.node_fuse,
                               lambda state: has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_duo, self.node_scorch,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_scorch, self.node_arc)
        self.__connect_regions(self.node_arc, self.node_wave,
                               lambda state: has_metaglass(state, self.player))
        self.__connect_regions(self.node_wave, self.node_parallax,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_parallax, self.node_segment,
                               lambda state: has_thorium_serpulo(state, self.player) and
                                             has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_wave, self.node_tsunami,
                               lambda state: has_titanium(state, self.player) and
                                             has_thorium_serpulo(state, self.player))

        self.__connect_regions(self.node_arc, self.node_lancer,
                               lambda state: has_silicon_serpulo(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_lancer, self.node_meltdown,
                               lambda state: has_surge_alloy_serpulo(state, self.player))
        self.__connect_regions(self.node_meltdown, self.node_foreshadow,
                               lambda state: has_metaglass(state, self.player) and
                                            has_plastanium(state, self.player))

        self.__connect_regions(self.node_lancer, self.node_shock_mine)

        self.__connect_regions(self.node_core_shard, self.node_ground_factory,
                               lambda state: has_silicon_serpulo(state, self.player))
        self.__connect_regions(self.node_ground_factory, self.node_dagger)
        self.__connect_regions(self.node_dagger, self.node_mace,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_mace, self.node_fortress,
                               lambda state: has_metaglass(state, self.player) and
                                            has_titanium(state, self.player))
        self.__connect_regions(self.node_fortress, self.node_scepter,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_scepter, self.node_reign,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_dagger, self.node_nova,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_nova, self.node_pulsar,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_pulsar, self.node_quasar,
                               lambda state: has_metaglass(state, self.player))
        self.__connect_regions(self.node_quasar, self.node_vela,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_vela, self.node_corvus,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_dagger, self.node_crawler)
        self.__connect_regions(self.node_crawler, self.node_atrax,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_atrax, self.node_spiroct,
                               lambda state: has_titanium(state, self.player) and
                                            has_metaglass(state, self.player))
        self.__connect_regions(self.node_spiroct, self.node_arkyid,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_arkyid, self.node_toxopid,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_ground_factory, self.node_air_factory)
        self.__connect_regions(self.node_air_factory, self.node_flare)
        self.__connect_regions(self.node_flare, self.node_horizon,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_horizon, self.node_zenith,
                               lambda state: has_titanium(state, self.player) and
                                            has_metaglass(state, self.player))
        self.__connect_regions(self.node_zenith, self.node_antumbra,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_antumbra, self.node_eclipse,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_flare, self.node_mono)
        self.__connect_regions(self.node_mono, self.node_poly,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_poly, self.node_mega,
                               lambda state: has_titanium(state, self.player) and
                                            has_metaglass(state, self.player))
        self.__connect_regions(self.node_mega, self.node_quad,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_quad, self.node_oct,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_air_factory, self.node_naval_factory,
                               lambda state: has_ruinous_shores(state, self.player) and
                                             has_metaglass(state, self.player))
        self.__connect_regions(self.node_naval_factory, self.node_risso)
        self.__connect_regions(self.node_risso, self.node_minke,
                               lambda state: has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_minke, self.node_bryde,
                               lambda state: has_titanium(state, self.player))
        self.__connect_regions(self.node_bryde, self.node_sei,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_sei, self.node_omura,
                               lambda state: has_surge_alloy_serpulo(state, self.player) and
                                            has_phase_fabric_serpulo(state, self.player))

        self.__connect_regions(self.node_risso, self.node_retusa,
                               lambda state: has_windswept_islands(state, self.player) and
                                             has_titanium(state, self.player))
        self.__connect_regions(self.node_retusa, self.node_oxynoe,
                               lambda state: has_coastline(state, self.player) and
                                             has_graphite_serpulo(state, self.player))
        self.__connect_regions(self.node_oxynoe, self.node_cyerce)
        self.__connect_regions(self.node_cyerce, self.node_aegires,
                               lambda state: has_plastanium(state, self.player))
        self.__connect_regions(self.node_aegires, self.node_navanax,
                               lambda state: has_phase_fabric_serpulo(state, self.player) and
                                             has_surge_alloy_serpulo(state, self.player) and
                                             has_naval_fortress(state, self.player))

        self.__connect_regions(self.node_ground_factory, self.node_additive_reconstructor,
                                lambda state: has_biomass_synthesis_facility(state, self.player))
        self.__connect_regions(self.node_additive_reconstructor, self.node_multiplicative_reconstructor,
                               lambda state: has_titanium(state, self.player) and
                                             has_thorium_serpulo(state, self.player))
        self.__connect_regions(self.node_multiplicative_reconstructor, self.node_exponential_reconstructor,
                               lambda state: has_overgrowth(state, self.player) and
                                             has_plastanium(state, self.player) and
                                             has_phase_fabric_serpulo(state, self.player))
        self.__connect_regions(self.node_exponential_reconstructor, self.node_tetrative_reconstructor,
                               lambda state: has_surge_alloy_serpulo(state, self.player))

        self.__connect_regions(self.node_core_shard, self.node_ground_zero)
        self.__connect_regions(self.node_ground_zero, self.node_frozen_forest)
        self.__connect_regions(self.node_frozen_forest, self.node_the_craters,
                               lambda state: has_frozen_forest(state, self.player))
        self.__connect_regions(self.node_the_craters, self.node_ruinous_shores,
                               lambda state: has_the_craters(state, self.player))
        self.__connect_regions(self.node_ruinous_shores, self.node_windswept_islands,
                               lambda state: has_ruinous_shores(state, self.player))
        self.__connect_regions(self.node_windswept_islands, self.node_tar_fields,
                               lambda state: has_windswept_islands(state, self.player))
        self.__connect_regions(self.node_tar_fields, self.node_impact_0078,
                               lambda state: has_tar_fields(state, self.player))
        self.__connect_regions(self.node_impact_0078, self.node_desolate_rift,
                               lambda state: has_impact_0078(state, self.player))
        self.__connect_regions(self.node_desolate_rift, self.node_planetary_launch_terminal,
                               lambda state: has_desolate_rift(state, self.player))
        self.__connect_regions(self.node_windswept_islands, self.node_extraction_outpost,
                                lambda state: has_ground_factory(state, self.player) and
                                            can_produce_ground_unit(state, self.player) and
                                            has_windswept_islands(state, self.player))
        self.__connect_regions(self.node_windswept_islands, self.node_salt_flats,
                                lambda state: has_ground_factory(state, self.player) and
                                            can_produce_ground_unit(state, self.player) and
                                            has_windswept_islands(state, self.player))
        self.__connect_regions(self.node_salt_flats, self.node_coastline,
                               lambda state: has_salt_flats(state, self.player))
        self.__connect_regions(self.node_coastline, self.node_naval_fortress,
                                lambda state: has_naval_factory(state, self.player) and
                                            can_produce_naval_unit(state, self.player) and
                                            has_coastline(state, self.player))
        self.__connect_regions(self.node_the_craters, self.node_overgrowth,
                               lambda state: has_the_craters(state, self.player))
        self.__connect_regions(self.node_frozen_forest, self.node_biomass_synthesis_facility,
                               lambda state: has_frozen_forest(state, self.player))
        self.__connect_regions(self.node_biomass_synthesis_facility, self.node_stained_mountains,
                               lambda state: has_biomass_synthesis_facility(state, self.player))
        self.__connect_regions(self.node_stained_mountains, self.node_fungal_pass,
                                lambda state: has_ground_factory(state, self.player) and
                                              can_produce_ground_unit(state, self.player) and
                                                has_stained_mountains(state, self.player))
        self.__connect_regions(self.node_fungal_pass, self.node_nuclear_production_complex,
                               lambda state: has_fungal_pass(state, self.player))
        self.__connect_regions(self.node_core_shard, self.node_copper)
        self.__connect_regions(self.node_copper, self.node_water_serpulo)
        self.__connect_regions(self.node_copper, self.node_lead)
        self.__connect_regions(self.node_lead, self.node_titanium,
                               lambda state: has_pneumatic_drill(state, self.player))
        self.__connect_regions(self.node_titanium, self.node_cryofluid,
                               lambda state: has_cryofluid_mixer(state, self.player))
        self.__connect_regions(self.node_titanium, self.node_thorium_serpulo,
                               lambda state: has_laser_drill(state, self.player))
        self.__connect_regions(self.node_thorium_serpulo, self.node_surge_alloy_serpulo,
                               lambda state: has_surge_smelter(state, self.player))
        self.__connect_regions(self.node_thorium_serpulo, self.node_phase_fabric_serpulo,
                               lambda state: has_phase_weaver(state, self.player))
        self.__connect_regions(self.node_lead, self.node_metaglass,
                               lambda state: has_kiln(state, self.player))
        self.__connect_regions(self.node_copper, self.node_sand_serpulo)
        self.__connect_regions(self.node_sand_serpulo, self.node_scrap)
        self.__connect_regions(self.node_scrap, self.node_slag_serpulo,
                               lambda state: has_melter(state, self.player))
        self.__connect_regions(self.node_sand_serpulo, self.node_coal)
        self.__connect_regions(self.node_coal, self.node_graphite_serpulo,
                               lambda state: has_graphite_press(state, self.player))
        self.__connect_regions(self.node_coal, self.node_silicon_serpulo,
                               lambda state: has_silicon_smelter(state, self.player))
        self.__connect_regions(self.node_coal, self.node_pyratite,
                               lambda state: has_pyratite_mixer(state, self.player))
        self.__connect_regions(self.node_pyratite, self.node_blast_compound,
                               lambda state: has_blast_mixer(state, self.player))
        self.__connect_regions(self.node_coal, self.node_spore_pod,
                               lambda state: has_cultivator(state, self.player))
        self.__connect_regions(self.node_coal, self.node_oil,
                               lambda state: has_mechanical_pump(state, self.player))
        self.__connect_regions(self.node_oil, self.node_plastanium,
                               lambda state: has_plastanium_compressor(state, self.player))

    def __connect_serpulo_resources_goal(self):
        """
        Connect Victory node with resources goal requirement for Serpulo campaign.
        """
        self.__connect_regions(self.menu, self.node_serpulo_victory,
                               lambda state: has_titanium(state, self.player) and
                                             has_thorium_serpulo(state, self.player) and
                                             has_surge_alloy_serpulo(state, self.player) and
                                             has_phase_fabric_serpulo(state, self.player) and
                                             has_metaglass(state, self.player) and
                                             has_graphite_serpulo(state, self.player) and
                                             has_silicon_serpulo(state, self.player) and
                                             has_pyratite(state, self.player) and
                                             has_blast_compound(state, self.player) and
                                             has_spore_pod(state, self.player) and
                                             has_plastanium(state, self.player))

    def __connect_serpulo_conquest_goal(self):
        """
        Connect Victory node with conquest goal requirement for serpulo.
        """
        self.__connect_regions(self.menu, self.node_serpulo_victory,
                               lambda state: has_frozen_forest(state, self.player) and
                                             has_the_craters(state, self.player) and
                                             has_biomass_synthesis_facility(state, self.player) and
                                             has_ruinous_shores(state, self.player) and
                                             has_stained_mountains(state, self.player) and
                                             has_windswept_islands(state, self.player) and
                                             has_fungal_pass(state, self.player) and
                                             has_overgrowth(state, self.player) and
                                             has_tar_fields(state, self.player) and
                                             has_extraction_outpost(state, self.player) and
                                             has_salt_flats(state, self.player) and
                                             has_coastline(state, self.player) and
                                             has_nuclear_production_complex(state, self.player) and
                                             has_impact_0078(state, self.player) and
                                             has_naval_fortress(state, self.player) and
                                             has_desolate_rift(state, self.player) and
                                             has_planetary_launch_terminal(state, self.player))

    def __create_erekir_campaign(self):
        """
        Create region related to the Erekir campaign.
        """
        self.erekir: Region = self.__add_region("Erekir", None)
        self.node_erekir_victory = self.__add_region("Victory Erekir", None)

        self.node_core_bastion = self.__add_region("Core: Bastion", None)

        self.node_duct = self.__add_region("Duct", None)
        self.node_duct_router = self.__add_region("AP-E-01-02", MindustryLocations.erekir_duct_router)
        self.node_duct_bridge = self.__add_region("AP-E-01-03", MindustryLocations.erekir_duct_bridge)
        self.node_armored_duct = self.__add_region("AP-E-01-04", MindustryLocations.erekir_armored_duct)
        self.node_surge_conveyor = self.__add_region("AP-E-01-05", MindustryLocations.erekir_surge_conveyor)
        self.node_surge_router = self.__add_region("AP-E-01-06", MindustryLocations.erekir_surge_router)
        self.node_unit_cargo_loader = self.__add_region("AP-E-01-07", MindustryLocations.erekir_unit_cargo_loader)
        self.node_unit_cargo_unload_point = self.__add_region("AP-E-01-08", MindustryLocations.erekir_unit_cargo_unload_point)
        self.node_overflow_duct = self.__add_region("AP-E-01-09", MindustryLocations.erekir_overflow_duct)
        self.node_underflow_duct = self.__add_region("AP-E-01-10", MindustryLocations.erekir_underflow_duct)
        self.node_reinforced_container = self.__add_region("AP-E-01-11", MindustryLocations.erekir_reinforced_container)
        self.node_duct_unloader = self.__add_region("AP-E-01-12", MindustryLocations.erekir_duct_unloader)
        self.node_reinforced_vault = self.__add_region("AP-E-01-13", MindustryLocations.erekir_reinforced_vault)
        self.node_reinforced_message = self.__add_region("AP-E-01-14", MindustryLocations.erekir_reinforced_message)
        self.node_canvas = self.__add_region("AP-E-01-15", MindustryLocations.erekir_canvas)
        self.node_reinforced_payload_conveyor = self.__add_region("AP-E-01-16", MindustryLocations.erekir_reinforced_payload_conveyor)
        self.node_payload_mass_driver = self.__add_region("AP-E-01-17", MindustryLocations.erekir_payload_mass_driver)
        self.node_payload_loader = self.__add_region("AP-E-01-18", MindustryLocations.erekir_payload_loader)
        self.node_payload_unloader = self.__add_region("AP-E-01-19", MindustryLocations.erekir_payload_unloader)
        self.node_large_payload_mass_driver = self.__add_region("AP-E-01-20", MindustryLocations.erekir_large_payload_mass_driver)
        self.node_constructor = self.__add_region("AP-E-01-21", MindustryLocations.erekir_constructor)
        self.node_deconstructor = self.__add_region("AP-E-01-22", MindustryLocations.erekir_deconstructor)
        self.node_large_constructor = self.__add_region("AP-E-01-23", MindustryLocations.erekir_large_constructor)
        self.node_large_deconstructor = self.__add_region("AP-E-01-24", MindustryLocations.erekir_large_deconstructor)
        self.node_reinforced_payload_router = self.__add_region("AP-E-01-25", MindustryLocations.erekir_reinforced_payload_router)

        self.node_plasma_bore = self.__add_region("Plasma Bore", None)
        self.node_impact_drill = self.__add_region("AP-E-02-02", MindustryLocations.erekir_impact_drill)
        self.node_large_plasma_bore = self.__add_region("AP-E-02-03", MindustryLocations.erekir_large_plasma_bore)
        self.node_eruption_drill = self.__add_region("AP-E-02-04", MindustryLocations.erekir_eruption_drill)

        self.node_turbine_condenser = self.__add_region("Turbine Condenser", None)
        self.node_beam_node = self.__add_region("Beam Node", None)
        self.node_vent_condenser = self.__add_region("AP-E-03-03", MindustryLocations.erekir_vent_condenser)
        self.node_chemical_combustion_chamber = self.__add_region("AP-E-03-04", MindustryLocations.erekir_chemical_combustion_chamber)
        self.node_pyrolysis_generator = self.__add_region("AP-E-03-05", MindustryLocations.erekir_pyrolysis_generator)
        self.node_flux_reactor = self.__add_region("AP-E-03-06", MindustryLocations.erekir_flux_reactor)
        self.node_neoplasia_reactor = self.__add_region("AP-E-03-07", MindustryLocations.erekir_neoplasia_reactor)
        self.node_beam_tower = self.__add_region("AP-E-03-08", MindustryLocations.erekir_beam_tower)
        self.node_regen_projector = self.__add_region("AP-E-03-09", MindustryLocations.erekir_regen_projector)
        self.node_build_tower = self.__add_region("AP-E-03-10", MindustryLocations.erekir_build_tower)
        self.node_shockwave_tower = self.__add_region("AP-E-03-11", MindustryLocations.erekir_shockwave_tower)
        self.node_reinforced_conduit = self.__add_region("AP-E-03-12", MindustryLocations.erekir_reinforced_conduit)
        self.node_reinforced_pump = self.__add_region("AP-E-03-13", MindustryLocations.erekir_reinforced_pump)
        self.node_reinforced_liquid_junction = self.__add_region("AP-E-03-14", MindustryLocations.erekir_reinforced_liquid_junction)
        self.node_reinforced_bridge_conduit = self.__add_region("AP-E-03-15", MindustryLocations.erekir_reinforced_bridge_conduit)
        self.node_reinforced_liquid_router = self.__add_region("AP-E-03-16", MindustryLocations.erekir_reinforced_liquid_router)
        self.node_reinforced_liquid_container = self.__add_region("AP-E-03-17", MindustryLocations.erekir_reinforced_liquid_container)
        self.node_reinforced_liquid_tank = self.__add_region("AP-E-03-18", MindustryLocations.erekir_reinforced_liquid_tank)
        self.node_cliff_crusher = self.__add_region("Cliff Crusher", None)
        self.node_silicon_arc_furnace = self.__add_region("Silicon Arc Furnace", None)
        self.node_electrolyzer = self.__add_region("AP-E-03-21", MindustryLocations.erekir_electrolyzer)
        self.node_oxidation_chamber = self.__add_region("AP-E-03-22", MindustryLocations.erekir_oxidation_chamber)
        self.node_surge_crucible = self.__add_region("AP-E-03-23", MindustryLocations.erekir_surge_crucible)
        self.node_heat_redirector = self.__add_region("AP-E-03-24", MindustryLocations.erekir_heat_redirector)
        self.node_electric_heater = self.__add_region("AP-E-03-25", MindustryLocations.erekir_electric_heater)
        self.node_slag_heater = self.__add_region("AP-E-03-26", MindustryLocations.erekir_slag_heater)
        self.node_atmospheric_concentrator = self.__add_region("AP-E-03-27", MindustryLocations.erekir_atmospheric_concentrator)
        self.node_cyanogen_synthesizer = self.__add_region("AP-E-03-28", MindustryLocations.erekir_cyanogen_synthesizer)
        self.node_carbide_crucible = self.__add_region("AP-E-03-29", MindustryLocations.erekir_carbide_crucible)
        self.node_phase_synthesizer = self.__add_region("AP-E-03-30", MindustryLocations.erekir_phase_synthesizer)
        self.node_phase_heater = self.__add_region("AP-E-03-31", MindustryLocations.erekir_phase_heater)
        self.node_heat_router = self.__add_region("AP-E-03-32", MindustryLocations.erekir_heat_router)
        self.node_slag_incinerator = self.__add_region("AP-E-03-33", MindustryLocations.erekir_slag_incinerator)

        self.node_breach = self.__add_region("Breach", None)
        self.node_beryllium_wall = self.__add_region("Beryllium Wall", None)
        self.node_large_beryllium_wall = self.__add_region("AP-E-04-03", MindustryLocations.erekir_large_beryllium_wall)
        self.node_tungsten_wall = self.__add_region("AP-E-04-04", MindustryLocations.erekir_tungsten_wall)
        self.node_large_tungsten_wall = self.__add_region("AP-E-04-05", MindustryLocations.erekir_large_tungsten_wall)
        self.node_blast_door = self.__add_region("AP-E-04-06", MindustryLocations.erekir_blast_door)
        self.node_reinforced_surge_wall = self.__add_region("AP-E-04-07", MindustryLocations.erekir_reinforced_surge_wall)
        self.node_large_reinforced_surge_wall = self.__add_region("AP-E-04-08", MindustryLocations.erekir_large_reinforced_surge_wall)
        self.node_shielded_wall = self.__add_region("AP-E-04-09", MindustryLocations.erekir_shielded_wall)
        self.node_carbide_wall = self.__add_region("AP-E-04-10", MindustryLocations.erekir_carbide_wall)
        self.node_large_carbide_wall = self.__add_region("AP-E-04-11", MindustryLocations.erekir_large_carbide_wall)
        self.node_diffuse = self.__add_region("AP-E-04-12", MindustryLocations.erekir_diffuse)
        self.node_sublimate = self.__add_region("AP-E-04-13", MindustryLocations.erekir_sublimate)
        self.node_afflict = self.__add_region("AP-E-04-14", MindustryLocations.erekir_afflict)
        self.node_titan = self.__add_region("AP-E-04-15", MindustryLocations.erekir_titan)
        self.node_lustre = self.__add_region("AP-E-04-16", MindustryLocations.erekir_lustre)
        self.node_smite = self.__add_region("AP-E-04-17", MindustryLocations.erekir_smite)
        self.node_disperse = self.__add_region("AP-E-04-18", MindustryLocations.erekir_disperse)
        self.node_scathe = self.__add_region("AP-E-04-19", MindustryLocations.erekir_scathe)
        self.node_malign = self.__add_region("AP-E-04-20", MindustryLocations.erekir_malign)
        self.node_radar = self.__add_region("AP-E-04-21", MindustryLocations.erekir_radar)

        self.node_core_citadel = self.__add_region("AP-E-05-01", MindustryLocations.erekir_core_citadel)
        self.node_core_acropolis = self.__add_region("AP-E-05-02", MindustryLocations.erekir_core_acropolis)


        self.node_tank_fabricator = self.__add_region("Tank Fabricator", None)
        self.node_stell = self.__add_region("Stell", None)
        self.node_unit_repair_tower = self.__add_region("AP-E-06-03", MindustryLocations.erekir_unit_repair_tower)
        self.node_ship_fabricator = self.__add_region("AP-E-06-04", MindustryLocations.erekir_ship_fabricator)
        self.node_elude = self.__add_region("AP-E-06-05", MindustryLocations.erekir_elude)
        self.node_mech_fabricator = self.__add_region("AP-E-06-06", MindustryLocations.erekir_mech_fabricator)
        self.node_merui = self.__add_region("AP-E-06-07", MindustryLocations.erekir_merui)
        self.node_tank_refabricator = self.__add_region("AP-E-06-08", MindustryLocations.erekir_tank_refabricator)
        self.node_locus = self.__add_region("AP-E-06-09", MindustryLocations.erekir_locus)
        self.node_mech_refabricator = self.__add_region("AP-E-06-10", MindustryLocations.erekir_mech_refrabricator)
        self.node_cleroi = self.__add_region("AP-E-06-11", MindustryLocations.erekir_cleroi)
        self.node_ship_refabricator = self.__add_region("AP-E-06-12", MindustryLocations.erekir_ship_refabricator)
        self.node_avert = self.__add_region("AP-E-06-13", MindustryLocations.erekir_avert)
        self.node_prime_refabricator = self.__add_region("AP-E-06-14", MindustryLocations.erekir_prime_refabricator)
        self.node_precept = self.__add_region("AP-E-06-15", MindustryLocations.erekir_precept)
        self.node_anthicus = self.__add_region("AP-E-06-16", MindustryLocations.erekir_anthicus)
        self.node_obviate = self.__add_region("AP-E-06-17", MindustryLocations.erekir_obviate)
        self.node_tank_assembler = self.__add_region("AP-E-06-18", MindustryLocations.erekir_tank_assembler)
        self.node_vanquish = self.__add_region("AP-E-06-19", MindustryLocations.erekir_vanquish)
        self.node_conquer = self.__add_region("AP-E-06-20", MindustryLocations.erekir_conquer)
        self.node_ship_assembler = self.__add_region("AP-E-06-21", MindustryLocations.erekir_ship_assembler)
        self.node_quell = self.__add_region("AP-E-06-22", MindustryLocations.erekir_quell)
        self.node_disrupt = self.__add_region("AP-E-06-23", MindustryLocations.erekir_disrupt)
        self.node_mech_assembler = self.__add_region("AP-E-06-24", MindustryLocations.erekir_mech_assembler)
        self.node_tecta = self.__add_region("AP-E-06-25", MindustryLocations.erekir_tecta)
        self.node_collaris = self.__add_region("AP-E-06-26", MindustryLocations.erekir_collaris)
        self.node_basic_assembler_module = self.__add_region("AP-E-06-27", MindustryLocations.erekir_basic_assembler_module)

        self.node_the_onset = self.__add_region("The Onset", None)
        self.node_aegis = self.__add_region("Aegis", None)
        self.node_lake = self.__add_region("Lake", None)
        self.node_intersect = self.__add_region("Intersect", None)
        self.node_atlas = self.__add_region("Atlas", None)
        self.node_split = self.__add_region("Split", None)
        self.node_basin = self.__add_region("Basin", None)
        self.node_marsh = self.__add_region("Marsh", None)
        self.node_ravine = self.__add_region("Ravine", None)
        self.node_caldera = self.__add_region("Caldera", None)
        self.node_stronghold = self.__add_region("Stronghold", None)
        self.node_crevice = self.__add_region("Crevice", None)
        self.node_siege = self.__add_region("Siege", None)
        self.node_crossroads = self.__add_region("Crossroads", None)
        self.node_karst = self.__add_region("Karst", None)
        self.node_origin = self.__add_region("Origin", None)
        self.node_peaks = self.__add_region("Peaks", None)

        self.node_beryllium = self.__add_region("Beryllium", None)
        self.node_sand_erekir = self.__add_region("Sand Erekir", None)
        self.node_silicon_erekir = self.__add_region("Silicon Erekir", None)
        self.node_oxide = self.__add_region("Oxide", None)
        self.node_water_erekir = self.__add_region("Water Erekir", None)
        self.node_ozone = self.__add_region("Ozone", None)
        self.node_hydrogen = self.__add_region("Hydrogen", None)
        self.node_nitrogen = self.__add_region("Nitrogen", None)
        self.node_cyanogen = self.__add_region("Cyanogen", None)
        self.node_neoplasm = self.__add_region("Neoplasm", None)
        self.node_graphite_erekir = self.__add_region("Graphite Erekir", None)
        self.node_tungsten = self.__add_region("Tungsten", None)
        self.node_slag_erekir = self.__add_region("Slag Erekir", None)
        self.node_arkycite = self.__add_region("Arkycite", None)
        self.node_thorium_erekir = self.__add_region("Thorium Erekir", None)
        self.node_carbide = self.__add_region("Carbide", None)
        self.node_surge_alloy_erekir = self.__add_region("Surge Alloy Erekir", None)
        self.node_phase_fabric_erekir = self.__add_region("Phase Fabric Erekir", None)

    def __connect_erekir_campaign(self, options: MindustryOptions):
        """
        Connect region related to Erekir's campaign
        """
        self.__connect_regions(self.menu, self.erekir)
        if options.goal == 0: # Resources
            self.__connect_erekir_resources_goal()
        elif options.goal == 1: # Conquest
            self.__connect_erekir_conquest_goal()
        else:
            self.__connect_erekir_resources_goal()# default to resources for now

        self.__connect_regions(self.erekir, self.node_core_bastion)

        self.__connect_regions(self.node_core_bastion, self.node_duct)
        self.__connect_regions(self.node_duct, self.node_duct_router)
        self.__connect_regions(self.node_duct_router, self.node_duct_bridge)
        self.__connect_regions(self.node_duct_bridge, self.node_armored_duct,
                               lambda state: has_tungsten(state, self.player))
        self.__connect_regions(self.node_armored_duct, self.node_surge_conveyor,
                               lambda state: has_surge_alloy_erekir(state, self.player))
        self.__connect_regions(self.node_surge_conveyor, self.node_surge_router)
        self.__connect_regions(self.node_duct_bridge, self.node_unit_cargo_loader,
                               lambda state: has_surge_alloy_erekir(state, self.player) and
                                            has_oxide(state, self.player))
        self.__connect_regions(self.node_unit_cargo_loader, self.node_unit_cargo_unload_point)
        self.__connect_regions(self.node_duct_router, self.node_overflow_duct)
        self.__connect_regions(self.node_overflow_duct, self.node_underflow_duct)
        self.__connect_regions(self.node_overflow_duct, self.node_reinforced_container,
                               lambda state: has_tungsten(state, self.player))
        self.__connect_regions(self.node_reinforced_container, self.node_duct_unloader)
        self.__connect_regions(self.node_reinforced_container, self.node_reinforced_vault,
                               lambda state: has_thorium_erekir(state, self.player))
        self.__connect_regions(self.node_duct_router, self.node_reinforced_message)
        self.__connect_regions(self.node_reinforced_message, self.node_canvas)
        self.__connect_regions(self.node_duct, self.node_reinforced_payload_conveyor,
                               lambda state: has_tungsten(state, self.player) and
                                            has_intersect(state, self.player))
        self.__connect_regions(self.node_reinforced_payload_conveyor, self.node_payload_mass_driver,
                               lambda state: has_atlas(state, self.player))
        self.__connect_regions(self.node_payload_mass_driver, self.node_payload_loader)
        self.__connect_regions(self.node_payload_loader, self.node_payload_unloader)
        self.__connect_regions(self.node_payload_unloader, self.node_large_payload_mass_driver,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_oxide(state, self.player))
        self.__connect_regions(self.node_payload_mass_driver, self.node_constructor)
        self.__connect_regions(self.node_constructor, self.node_deconstructor,
                               lambda state: has_oxide(state, self.player) and
                                            has_peaks_launch(state, self.player))
        self.__connect_regions(self.node_deconstructor, self.node_large_constructor,
                               lambda state: has_phase_fabric_erekir(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_deconstructor, self.node_large_deconstructor,
                               lambda state: has_carbide(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_reinforced_payload_conveyor, self.node_reinforced_payload_router)

        self.__connect_regions(self.node_core_bastion, self.node_plasma_bore)
        self.__connect_regions(self.node_plasma_bore, self.node_impact_drill)
        self.__connect_regions(self.node_impact_drill, self.node_large_plasma_bore,
                               lambda state: has_tungsten(state, self.player) and
                                            has_oxide(state, self.player) and
                                            has_caldera_launch(state, self.player))
        self.__connect_regions(self.node_large_plasma_bore, self.node_eruption_drill,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_caldera(state, self.player))

        self.__connect_regions(self.node_core_bastion, self.node_turbine_condenser)
        self.__connect_regions(self.node_turbine_condenser, self.node_beam_node)
        self.__connect_regions(self.node_beam_node, self.node_vent_condenser)
        self.__connect_regions(self.node_vent_condenser, self.node_chemical_combustion_chamber,
                               lambda state: has_oxide(state, self.player) and
                                            has_tungsten(state, self.player) and
                                            has_atlas(state, self.player))
        self.__connect_regions(self.node_chemical_combustion_chamber, self.node_pyrolysis_generator,
                               lambda state: has_carbide(state, self.player) and
                                            has_stronghold(state, self.player))
        self.__connect_regions(self.node_pyrolysis_generator, self.node_flux_reactor,
                               lambda state: has_surge_alloy_erekir(state, self.player) and
                                            has_siege(state, self.player))
        self.__connect_regions(self.node_flux_reactor, self.node_neoplasia_reactor,
                               lambda state: has_phase_fabric_erekir(state, self.player) and
                                            has_crossroads(state, self.player))
        self.__connect_regions(self.node_beam_node, self.node_beam_tower,
                                lambda state: has_oxide(state, self.player) and
                                            has_peaks_launch(state, self.player))
        self.__connect_regions(self.node_beam_node, self.node_regen_projector,
                               lambda state: has_oxide(state, self.player) and
                                            has_tungsten(state, self.player) and
                                            has_peaks_launch(state, self.player))
        self.__connect_regions(self.node_regen_projector, self.node_build_tower,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_caldera(state, self.player))
        self.__connect_regions(self.node_build_tower, self.node_shockwave_tower,
                               lambda state: has_surge_alloy_erekir(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_turbine_condenser, self.node_reinforced_conduit)
        self.__connect_regions(self.node_reinforced_conduit, self.node_reinforced_pump,
                               lambda state: has_tungsten(state, self.player) and
                                            has_atlas(state, self.player))
        self.__connect_regions(self.node_reinforced_conduit, self.node_reinforced_liquid_junction)
        self.__connect_regions(self.node_reinforced_liquid_junction, self.node_reinforced_bridge_conduit)
        self.__connect_regions(self.node_reinforced_liquid_junction, self.node_reinforced_liquid_router)
        self.__connect_regions(self.node_reinforced_liquid_router, self.node_reinforced_liquid_container,
                               lambda state: has_tungsten(state, self.player))
        self.__connect_regions(self.node_reinforced_liquid_container, self.node_reinforced_liquid_tank,
                               lambda state: has_intersect(state, self.player))
        self.__connect_regions(self.node_turbine_condenser, self.node_cliff_crusher)
        self.__connect_regions(self.node_cliff_crusher, self.node_silicon_arc_furnace)
        self.__connect_regions(self.node_silicon_arc_furnace, self.node_electrolyzer,
                               lambda state: has_tungsten(state, self.player) and
                                            has_intersect(state, self.player))
        self.__connect_regions(self.node_electrolyzer, self.node_oxidation_chamber,
                               lambda state: has_basin(state, self.player))
        self.__connect_regions(self.node_oxidation_chamber, self.node_surge_crucible,
                               lambda state: has_oxide(state, self.player) and
                                            has_marsh(state, self.player))
        self.__connect_regions(self.node_oxidation_chamber, self.node_heat_redirector,
                               lambda state: has_marsh(state, self.player))
        self.__connect_regions(self.node_heat_redirector, self.node_electric_heater,
                                lambda state: has_oxide(state, self.player) and
                                            has_marsh(state, self.player))
        self.__connect_regions(self.node_electric_heater, self.node_slag_heater,
                               lambda state: has_caldera_launch(state, self.player))
        self.__connect_regions(self.node_electric_heater, self.node_atmospheric_concentrator,
                               lambda state: has_caldera_launch(state, self.player))
        self.__connect_regions(self.node_atmospheric_concentrator, self.node_cyanogen_synthesizer,
                               lambda state: has_carbide(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_electric_heater, self.node_carbide_crucible,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_stronghold(state, self.player))
        self.__connect_regions(self.node_carbide_crucible, self.node_phase_synthesizer,
                               lambda state: has_crossroads(state, self.player))
        self.__connect_regions(self.node_phase_synthesizer, self.node_phase_heater)
        self.__connect_regions(self.node_electric_heater, self.node_heat_router)
        self.__connect_regions(self.node_electrolyzer, self.node_slag_incinerator,
                               lambda state: has_atlas(state, self.player))

        self.__connect_regions(self.node_core_bastion, self.node_breach)
        self.__connect_regions(self.node_breach, self.node_beryllium_wall)
        self.__connect_regions(self.node_beryllium_wall, self.node_large_beryllium_wall)
        self.__connect_regions(self.node_beryllium_wall, self.node_tungsten_wall,
                                lambda state: has_tungsten(state, self.player))
        self.__connect_regions(self.node_tungsten_wall, self.node_large_tungsten_wall)
        self.__connect_regions(self.node_large_tungsten_wall, self.node_blast_door)
        self.__connect_regions(self.node_tungsten_wall, self.node_reinforced_surge_wall,
                               lambda state: has_surge_alloy_erekir(state, self.player))
        self.__connect_regions(self.node_reinforced_surge_wall, self.node_large_reinforced_surge_wall)
        self.__connect_regions(self.node_large_reinforced_surge_wall, self.node_shielded_wall,
                               lambda state: has_phase_fabric_erekir(state, self.player))
        self.__connect_regions(self.node_tungsten_wall, self.node_carbide_wall,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_carbide(state, self.player))
        self.__connect_regions(self.node_carbide_wall, self.node_large_carbide_wall)
        self.__connect_regions(self.node_breach, self.node_diffuse,
                               lambda state: has_tungsten(state, self.player) and
                                            has_aegis(state, self.player))
        self.__connect_regions(self.node_diffuse, self.node_sublimate,
                               lambda state: has_oxide(state, self.player) and
                                            has_basin(state, self.player))
        self.__connect_regions(self.node_sublimate, self.node_afflict,
                               lambda state: has_surge_alloy_erekir(state, self.player) and
                                            has_marsh(state, self.player))
        self.__connect_regions(self.node_afflict, self.node_titan,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_caldera(state, self.player))
        self.__connect_regions(self.node_titan, self.node_lustre,
                               lambda state: has_carbide(state, self.player) and
                                            has_stronghold(state, self.player))
        self.__connect_regions(self.node_lustre, self.node_smite,
                               lambda state: has_phase_fabric_erekir(state, self.player) and
                                            has_crossroads(state, self.player))
        self.__connect_regions(self.node_diffuse, self.node_disperse,
                               lambda state: has_oxide(state, self.player) and
                                            has_thorium_erekir(state, self.player) and
                                            has_caldera(state, self.player))
        self.__connect_regions(self.node_disperse, self.node_scathe,
                               lambda state: has_carbide(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_scathe, self.node_malign,
                               lambda state: has_phase_fabric_erekir(state, self.player) and
                                            has_karst(state, self.player))
        self.__connect_regions(self.node_breach, self.node_radar)

        self.__connect_regions(self.node_core_bastion, self.node_core_citadel,
                               lambda state: has_oxide(state, self.player) and
                                            has_tungsten(state, self.player) and
                                            has_peaks(state, self.player))
        self.__connect_regions(self.node_core_citadel, self.node_core_acropolis,
                               lambda state: has_carbide(state, self.player) and
                                            has_siege(state, self.player))

        self.__connect_regions(self.node_core_bastion, self.node_tank_fabricator)
        self.__connect_regions(self.node_tank_fabricator, self.node_stell)
        self.__connect_regions(self.node_tank_fabricator, self.node_unit_repair_tower,
                               lambda state: has_tungsten(state, self.player) and
                                            has_marsh(state, self.player))
        self.__connect_regions(self.node_tank_fabricator, self.node_ship_fabricator,
                               lambda state: has_aegis(state, self.player))
        self.__connect_regions(self.node_ship_fabricator, self.node_elude)
        self.__connect_regions(self.node_ship_fabricator, self.node_mech_fabricator,
                               lambda state: has_tungsten(state, self.player) and
                                            has_lake(state, self.player))
        self.__connect_regions(self.node_mech_fabricator, self.node_merui)
        self.__connect_regions(self.node_mech_fabricator, self.node_tank_refabricator,
                               lambda state: has_intersect(state, self.player))
        self.__connect_regions(self.node_tank_refabricator, self.node_locus)
        self.__connect_regions(self.node_tank_refabricator, self.node_mech_refabricator,
                               lambda state: has_atlas(state, self.player))
        self.__connect_regions(self.node_mech_refabricator, self.node_cleroi)
        self.__connect_regions(self.node_mech_refabricator, self.node_ship_refabricator,
                               lambda state: has_oxide(state, self.player) and
                                            has_peaks_launch(state, self.player))
        self.__connect_regions(self.node_ship_refabricator, self.node_avert)
        self.__connect_regions(self.node_ship_refabricator, self.node_prime_refabricator,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_caldera(state, self.player))
        self.__connect_regions(self.node_prime_refabricator, self.node_precept)
        self.__connect_regions(self.node_prime_refabricator, self.node_anthicus)
        self.__connect_regions(self.node_prime_refabricator, self.node_obviate)
        self.__connect_regions(self.node_ship_refabricator, self.node_tank_assembler,
                               lambda state: has_thorium_erekir(state, self.player) and
                                            has_carbide(state, self.player) and
                                            has_crevice(state, self.player))
        self.__connect_regions(self.node_tank_assembler, self.node_vanquish)
        self.__connect_regions(self.node_vanquish, self.node_conquer,
                               lambda state: has_crossroads(state, self.player))
        self.__connect_regions(self.node_tank_assembler, self.node_ship_assembler,
                               lambda state: has_siege(state, self.player))
        self.__connect_regions(self.node_ship_assembler, self.node_quell)
        self.__connect_regions(self.node_quell, self.node_disrupt,
                               lambda state: has_crossroads(state, self.player))
        self.__connect_regions(self.node_tank_assembler, self.node_mech_assembler,
                               lambda state: has_siege(state, self.player))
        self.__connect_regions(self.node_mech_assembler, self.node_tecta)
        self.__connect_regions(self.node_tecta, self.node_collaris,
                               lambda state: has_crossroads(state, self.player))
        self.__connect_regions(self.node_tank_assembler, self.node_basic_assembler_module,
                               lambda state: has_phase_fabric_erekir(state, self.player) and
                                            has_karst(state, self.player))

        self.__connect_regions(self.node_core_bastion, self.node_the_onset)
        self.__connect_regions(self.node_the_onset, self.node_aegis,
                               lambda state: has_aegis_requirements(state, self.player))
        self.__connect_regions(self.node_aegis, self.node_lake,
                               lambda state: has_aegis(state, self.player) and
                                            has_lake_requirements(state, self.player))
        self.__connect_regions(self.node_lake, self.node_intersect,
                               lambda state: has_lake(state, self.player) and
                                            has_intersect_requirements(state, self.player))
        self.__connect_regions(self.node_intersect, self.node_atlas,
                               lambda state: has_intersect(state, self.player))
        self.__connect_regions(self.node_atlas, self.node_split,
                               lambda state: has_atlas(state, self.player) and
                                            has_split_requirements(state, self.player))
        self.__connect_regions(self.node_atlas, self.node_basin,
                               lambda state: has_atlas(state, self.player))
        self.__connect_regions(self.node_basin, self.node_marsh,
                               lambda state: has_basin(state, self.player) and
                                            has_marsh_requirement(state, self.player))
        self.__connect_regions(self.node_marsh, self.node_peaks,
                               lambda state: has_peaks_launch(state, self.player) and
                                            has_peaks_requirement(state, self.player))
        self.__connect_regions(self.node_marsh, self.node_ravine,
                               lambda state: has_marsh(state, self.player))
        self.__connect_regions(self.node_ravine, self.node_caldera,
                               lambda state: has_caldera_launch(state, self.player) and
                                            has_caldera_requirement(state, self.player))
        self.__connect_regions(self.node_caldera, self.node_stronghold,
                               lambda state: has_caldera(state, self.player))
        self.__connect_regions(self.node_stronghold, self.node_crevice,
                               lambda state: has_stronghold(state, self.player))
        self.__connect_regions(self.node_crevice, self.node_siege,
                               lambda state: has_crevice(state, self.player))
        self.__connect_regions(self.node_siege, self.node_crossroads,
                               lambda state: has_siege(state, self.player))
        self.__connect_regions(self.node_crossroads, self.node_karst,
                               lambda state: has_crossroads(state, self.player))
        self.__connect_regions(self.node_karst, self.node_origin,
                               lambda state: has_karst(state, self.player))

        self.__connect_regions(self.node_core_bastion, self.node_beryllium)
        self.__connect_regions(self.node_beryllium, self.node_sand_erekir)
        self.__connect_regions(self.node_sand_erekir, self.node_silicon_erekir)
        self.__connect_regions(self.node_silicon_erekir, self.node_oxide,
                               lambda state: has_oxidation_chamber(state, self.player))
        self.__connect_regions(self.node_beryllium, self.node_water_erekir)
        self.__connect_regions(self.node_water_erekir, self.node_ozone,
                               lambda state: has_electrolyzer(state, self.player))
        self.__connect_regions(self.node_ozone, self.node_hydrogen,
                               lambda state: has_electrolyzer(state, self.player))
        self.__connect_regions(self.node_hydrogen, self.node_nitrogen,
                               lambda state: has_atmospheric_concentrator(state, self.player))
        self.__connect_regions(self.node_hydrogen, self.node_cyanogen,
                               lambda state: has_cyanogen_synthesizer(state, self.player))
        self.__connect_regions(self.node_cyanogen, self.node_neoplasm)
        self.__connect_regions(self.node_beryllium, self.node_graphite_erekir)
        self.__connect_regions(self.node_graphite_erekir, self.node_tungsten,
                               lambda state: has_impact_drill(state, self.player))
        self.__connect_regions(self.node_tungsten, self.node_slag_erekir,
                               lambda state: has_reinforced_pump(state, self.player))
        self.__connect_regions(self.node_tungsten, self.node_arkycite,
                               lambda state: has_reinforced_pump(state, self.player))
        self.__connect_regions(self.node_tungsten, self.node_thorium_erekir,
                               lambda state: has_large_plasma_bore(state, self.player) and
                                            has_caldera(state, self.player))
        self.__connect_regions(self.node_thorium_erekir, self.node_carbide,
                               lambda state: has_carbide_crucible(state, self.player))
        self.__connect_regions(self.node_tungsten, self.node_surge_alloy_erekir,
                               lambda state: has_surge_crucible(state, self.player) and
                                            has_reinforced_pump(state, self.player))
        self.__connect_regions(self.node_surge_alloy_erekir, self.node_phase_fabric_erekir,
                               lambda state: has_phase_synthesizer(state, self.player))

    def __connect_erekir_conquest_goal(self):
        self.__connect_regions(self.menu, self.node_erekir_victory,
                               lambda state: has_aegis(state, self.player) and
                                             has_lake(state, self.player) and
                                             has_intersect(state, self.player) and
                                             has_atlas(state, self.player) and
                                             has_split(state, self.player) and
                                             has_basin(state, self.player) and
                                             has_marsh(state, self.player) and
                                             has_peaks(state, self.player) and
                                             has_ravine(state, self.player) and
                                             has_caldera(state, self.player) and
                                             has_stronghold(state, self.player) and
                                             has_crevice(state, self.player) and
                                             has_siege(state, self.player) and
                                             has_crossroads(state, self.player) and
                                             has_karst(state, self.player) and
                                             has_origin(state, self.player))

    def __connect_erekir_resources_goal(self):
        self.__connect_regions(self.menu, self.node_erekir_victory,
                               lambda state: has_oxide(state, self.player) and
                                             has_tungsten(state, self.player) and
                                             has_thorium_erekir(state, self.player) and
                                             has_carbide(state, self.player) and
                                             has_surge_alloy_erekir(state, self.player) and
                                             has_phase_fabric_erekir(state, self.player))

    def __create_all_campaign(self):
        """
        Create region related to the all campaigns.
        """
        self.all_campaign_victory = self.__add_region("All campaign victory", None)
        self.__create_serpulo_campaign()
        self.__create_erekir_campaign()


    def __connect_all_campaign(self, options:MindustryOptions):
        """
        Connect region related to all campaigns.
        """
        self.__connect_regions(self.menu, self.all_campaign_victory,
                               lambda state: has_serpulo_victory(state, self.player) and
                                             has_erekir_victory(state, self.player))
        self.__connect_serpulo_campaign(options)
        self.__connect_erekir_campaign(options)

    def __add_region(self, hint: str,
                     locations: Optional[Dict[str, Optional[int]]]) -> Region:
        """Create a new region."""
        region: Region = Region(hint, self.player, self.multiworld, hint)
        if locations is not None:
            region.add_locations(locations, MindustryLocation)
        self.multiworld.regions.append(region)
        return region

    def __initialise_serpulo_rules(self):
        """Initialise rules for Serpulo location"""
        self.multiworld.completion_condition[self.player] = lambda \
                state: state.has("Victory archived on Serpulo", self.player)



    def __connect_regions(self, source_region: Region, target_region: Region, rule = None) -> None:
        """
        Connect regions between themselves
        """
        entrance = Entrance(source_region.player, source_region.name + " to " + target_region.name, source_region)
        source_region.exits.append(entrance)
        entrance.connect(target_region)
        if rule is not None:
            set_rule(entrance, rule)



    def __add_serpulo_events(self):
        self.__add_event_location(self.node_serpulo_victory, "Victory Serpulo", "Victory archived on Serpulo")
        self.__add_event_location(self.node_frozen_forest, "Capture Frozen Forest", "Frozen Forest captured")
        self.__add_event_location(self.node_the_craters, "Capture The Craters", "The Craters captured")
        self.__add_event_location(self.node_ruinous_shores, "Capture Ruinous Shores", "Ruinous Shores captured")
        self.__add_event_location(self.node_windswept_islands, "Capture Windswept Islands", "Windswept Islands captured")
        self.__add_event_location(self.node_tar_fields, "Capture Tar Fields", "Tar Fields captured")
        self.__add_event_location(self.node_impact_0078, "Capture Impact 0078", "Impact 0078 captured")
        self.__add_event_location(self.node_desolate_rift, "Capture Desolate Rift", "Desolate Rift captured")
        self.__add_event_location(self.node_planetary_launch_terminal, "Capture Planetary Launch Terminal", "Planetary Launch Terminal captured")
        self.__add_event_location(self.node_extraction_outpost, "Capture Extraction Outpost", "Extraction Outpost captured")
        self.__add_event_location(self.node_salt_flats, "Capture Salt Flats", "Salt Flats captured")
        self.__add_event_location(self.node_coastline, "Capture Coastline", "Coastline captured")
        self.__add_event_location(self.node_naval_fortress, "Capture Naval Fortress", "Naval Fortress captured")
        self.__add_event_location(self.node_overgrowth, "Capture Overgrowth", "Overgrowth captured")
        self.__add_event_location(self.node_biomass_synthesis_facility, "Capture Biomass Synthesis Facility", "Biomass Synthesis Facility captured")
        self.__add_event_location(self.node_stained_mountains, "Capture Stained Mountains", "Stained Mountains captured")
        self.__add_event_location(self.node_fungal_pass, "Capture Fungal Pass", "Fungal Pass captured")
        self.__add_event_location(self.node_nuclear_production_complex, "Capture Nuclear Production Complex", "Nuclear Production Complex captured")

        self.__add_event_location(self.node_titanium, "Produce Titanium on Serpulo", "Titanium produced on Serpulo")
        self.__add_event_location(self.node_cryofluid, "Produce Cryofluid on Serpulo", "Cryofluid produced on Serpulo")
        self.__add_event_location(self.node_thorium_serpulo, "Produce Thorium on Serpulo", "Thorium produced on Serpulo")
        self.__add_event_location(self.node_surge_alloy_serpulo, "Produce Surge Alloy on Serpulo", "Surge Alloy produced on Serpulo")
        self.__add_event_location(self.node_phase_fabric_serpulo, "Produce Phase Fabric on Serpulo", "Phase Fabric produced on Serpulo")
        self.__add_event_location(self.node_slag_serpulo, "Produce Slag on Serpulo", "Slag produced on Serpulo")
        self.__add_event_location(self.node_metaglass, "Produce Metaglass on Serpulo", "Metaglass produced on Serpulo")
        self.__add_event_location(self.node_graphite_serpulo, "Produce Graphite on Serpulo", "Graphite produced on Serpulo")
        self.__add_event_location(self.node_silicon_serpulo, "Produce Silicon on Serpulo", "Silicon produced on Serpulo")
        self.__add_event_location(self.node_pyratite, "Produce Pyratite on Serpulo", "Pyratite produced on Serpulo")
        self.__add_event_location(self.node_blast_compound, "Produce Blast Compound on Serpulo", "Blast Compound produced on Serpulo")
        self.__add_event_location(self.node_spore_pod, "Produce Spore Pod on Serpulo", "Spore Pod produced on Serpulo")
        self.__add_event_location(self.node_oil, "Produce Oil on Serpulo", "Oil produced on Serpulo")
        self.__add_event_location(self.node_plastanium, "Produce Plastanium on Serpulo", "Plastanium produced on Serpulo")

    def __initialise_erekir_rules(self):
        self.multiworld.completion_condition[self.player] = lambda \
                state: state.has("Victory archived on Erekir", self.player)

    def __add_erekir_events(self):
        self.__add_event_location(self.node_erekir_victory, "Victory Erekir", "Victory archived on Erekir")
        self.__add_event_location(self.node_aegis, "Capture Aegis", "Aegis captured")
        self.__add_event_location(self.node_lake, "Capture Lake", "Lake captured")
        self.__add_event_location(self.node_intersect, "Capture Intersect", "Intersect captured")
        self.__add_event_location(self.node_atlas, "Capture Atlas", "Atlas captured")
        self.__add_event_location(self.node_split, "Capture Split", "Split captured")
        self.__add_event_location(self.node_basin, "Capture Basin", "Basin captured")
        self.__add_event_location(self.node_marsh, "Capture Marsh", "Marsh captured")
        self.__add_event_location(self.node_ravine, "Capture Ravine", "Ravine captured")
        self.__add_event_location(self.node_caldera, "Capture Caldera", "Caldera captured")
        self.__add_event_location(self.node_stronghold, "Capture Stronghold", "Stronghold captured")
        self.__add_event_location(self.node_crevice, "Capture Crevice", "Crevice captured")
        self.__add_event_location(self.node_siege, "Capture Siege", "Siege captured")
        self.__add_event_location(self.node_crossroads, "Capture Crossroads", "Crossroads captured")
        self.__add_event_location(self.node_karst, "Capture Karst", "Karst captured")
        self.__add_event_location(self.node_origin, "Capture Origin", "Origin captured")
        self.__add_event_location(self.node_peaks, "Capture Peaks", "Peaks captured")

        self.__add_event_location(self.node_oxide, "Produce Oxide on Erekir", "Oxide produced on Erekir")
        self.__add_event_location(self.node_ozone, "Produce Ozone on Erekir", "Ozone produced on Erekir")
        self.__add_event_location(self.node_hydrogen, "Produce Hydrogen on Erekir", "Hydrogen produced on Erekir")
        self.__add_event_location(self.node_nitrogen, "Produce Nitrogen on Erekir", "Nitrogen produced on Erekir")
        self.__add_event_location(self.node_cyanogen, "Produce Cyanogen on Erekir", "Cyanogen produced on Erekir")
        self.__add_event_location(self.node_neoplasm, "Produce Neoplasm on Erekir", "Neoplasm produced on Erekir")
        self.__add_event_location(self.node_tungsten, "Produce Tungsten on Erekir", "Tungsten produced on Erekir")
        self.__add_event_location(self.node_arkycite, "Produce Arkycite on Erekir", "Arkycite produced on Erekir")
        self.__add_event_location(self.node_thorium_erekir, "Produce Thorium on Erekir", "Thorium produced on Erekir")
        self.__add_event_location(self.node_carbide, "Produce Carbide on Erekir", "Carbide produced on Erekir")
        self.__add_event_location(self.node_surge_alloy_erekir, "Produce Surge Alloy on Erekir", "Surge Alloy produced on Erekir")
        self.__add_event_location(self.node_phase_fabric_erekir, "Produce Phase Fabric on Erekir", "Phase Fabric produced on Erekir")
        self.__add_event_location(self.node_slag_erekir, "Produce Slag on Erekir", "Slag produced on Erekir")

    def __add_all_events(self):
        self.__add_event_location(self.all_campaign_victory, "All campaign victory", "Victory archived on all campaign")
        self.__add_serpulo_events()
        self.__add_erekir_events()

    def __initialise_all_rules(self):
        self.multiworld.completion_condition[self.player] = lambda \
                state: state.has("Victory archived on all campaign", self.player)

    def __apply_serpulo_military_level_rules(self):
        add_rule(self.multiworld.get_location("Capture Ruinous Shores", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 5)
        add_rule(self.multiworld.get_location("Capture Windswept Islands", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 6)
        add_rule(self.multiworld.get_location("Capture Tar Fields", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 10)
        add_rule(self.multiworld.get_location("Capture Impact 0078", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 12)
        add_rule(self.multiworld.get_location("Capture Desolate Rift", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 30)
        add_rule(self.multiworld.get_location("Capture Planetary Launch Terminal", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 55)
        add_rule(self.multiworld.get_location("Capture Extraction Outpost", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 10)
        add_rule(self.multiworld.get_location("Capture Salt Flats", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 10)
        add_rule(self.multiworld.get_location("Capture Coastline", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 10)
        add_rule(self.multiworld.get_location("Capture Naval Fortress", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 30)
        add_rule(self.multiworld.get_location("Capture Overgrowth", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 10)
        add_rule(self.multiworld.get_location("Capture Biomass Synthesis Facility", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 6)
        add_rule(self.multiworld.get_location("Capture Stained Mountains", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 7)
        add_rule(self.multiworld.get_location("Capture Fungal Pass", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 8)
        add_rule(self.multiworld.get_location("Capture Nuclear Production Complex", self.player),
                 lambda state: get_military_score_serpulo(state, self.player) >= 12)

    def __apply_erekir_military_level_rules(self):
        add_rule(self.multiworld.get_location("Capture Ravine", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 3)
        add_rule(self.multiworld.get_location("Capture Caldera", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 3 and
                            get_unit_military_score_erekir(state, self.player) >= 4)
        add_rule(self.multiworld.get_location("Capture Stronghold", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 6 and
                               get_unit_military_score_erekir(state, self.player) >= 8)
        add_rule(self.multiworld.get_location("Capture Crevice", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 10 and
                               get_unit_military_score_erekir(state, self.player) >= 8)
        add_rule(self.multiworld.get_location("Capture Siege", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 10 and
                               get_unit_military_score_erekir(state, self.player) >= 15)
        add_rule(self.multiworld.get_location("Capture Crossroads", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 15 and
                               get_unit_military_score_erekir(state, self.player) >= 20)
        add_rule(self.multiworld.get_location("Capture Karst", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 40 and
                               get_unit_military_score_erekir(state, self.player) >= 25)
        add_rule(self.multiworld.get_location("Capture Origin", self.player),
                 lambda state: get_defense_military_score_erekir(state, self.player) >= 50 and
                               get_unit_military_score_erekir(state, self.player) >= 35)
