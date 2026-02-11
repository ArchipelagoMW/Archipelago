from typing import Dict, Any

from worlds.generic.Rules import set_rule

from . import GatoRobotoWorld
from .Names import RegionName, ItemName, LocationName


def set_rules(world: GatoRobotoWorld):
    player = world.player

    # Location logic dictionary
    location_logic: Dict[str, Any] = {

        # LANDING SITE

        # West Healthkit
        # LocationName.loc_healthkit_landing_site_west: lambda state: True,

        # East Healthkit
        LocationName.loc_healthkit_landing_site_east:
            lambda state: state.has(ItemName.module_missile, player),

        # Bark Cartridge
        LocationName.loc_cartridge_bark:
            lambda state: state.has(ItemName.module_missile, player),

        # Nicotine Cartridge
        LocationName.loc_cartridge_nicotine:
            lambda state: state.has_all([ItemName.module_missile,
                                         ItemName.module_spinjump], player) or
                          (world.options.rocket_jumps and
                           state.has(ItemName.module_missile, player)),

        # Missile Module
        # LocationName.loc_module_missile: lambda state: True,

        # Decoder Module
        LocationName.loc_module_decoder:
            lambda state: (state.has_all(ItemName.ProgressiveAqueducts, player) and
                            state.has_all(ItemName.ProgressiveHeaterCore, player) and
                            state.has_all(ItemName.ProgressiveVentilation, player) and
                            state.has(ItemName.module_spinjump, player)) or
                          (world.options.precise_tricks and
                           world.options.rocket_jumps and
                           state.has(ItemName.module_spinjump, player) and
                           state.has(ItemName.module_missile, player)),

        # NEXUS

        # Nexus West Healthkit
        LocationName.loc_healthkit_nexus_west:
            lambda state: state.has_all([ItemName.module_spinjump,
                                         ItemName.module_phase], player) or
                          (world.options.rocket_jumps and
                           world.options.precise_tricks and
                           state.has(ItemName.module_coolant, player)) or
                          (world.options.rocket_jumps and
                           state.has(ItemName.module_spinjump, player)),

        # Nexus East Healthkit
        LocationName.loc_healthkit_nexus_east:
            lambda state: state.has(ItemName.module_spinjump, player) or
                          world.options.rocket_jumps,

        # Coffee Stain Cartridge
        LocationName.loc_cartridge_coffee_stain:
            lambda state: state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) or
                          world.options.water_mech,

        # Urine Cartridge
        LocationName.loc_cartridge_urine:
            lambda state: state.has(ItemName.module_spinjump, player) or
                          (state.has(ItemName.module_coolant, player) and
                           world.options.rocket_jumps) or
                          world.options.precise_tricks,

        # Swamp Matcha Cartridge
        LocationName.loc_cartridge_swamp_matcha:
            lambda state: state.has_all(ItemName.ProgressiveVentilation, player) or
                           world.options.precise_tricks,

        # Repeater Module
        LocationName.loc_module_repeater:
            lambda state: state.has_from_list(ItemName.Cartridges, player, 7),

        # Hopper Module
        LocationName.loc_module_hopper:
            lambda state: state.has_from_list(ItemName.Cartridges, player, 14),

        # AQUEDUCTS

        # Aqueducts West Healthkit
        LocationName.loc_healthkit_aqueducts_west:
            lambda state: state.has_any(ItemName.ProgressiveAqueducts, player) or
                          world.options.water_mech,

        # Aqueducts East Healthkit
        LocationName.loc_healthkit_aqueducts_east:
            lambda state: (state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) and
                           state.has(ItemName.module_spinjump, player)) or
                          (state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) and
                           world.options.rocket_jumps) or
                          (world.options.rocket_jumps and
                           world.options.water_mech),

        # Port Cartridge
        LocationName.loc_cartridge_port:
            lambda state: state.has_all(ItemName.ProgressiveAqueducts, player) and
                          state.has(ItemName.module_spinjump, player),

        # Goop Cartridge
        LocationName.loc_cartridge_goop:
            lambda state: state.has_all(ItemName.ProgressiveAqueducts, player) and
                          state.has(ItemName.module_spinjump, player),

        # Starboard Cartridge
        LocationName.loc_cartridge_starboard:
            lambda state: (state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) and
                           state.has(ItemName.module_spinjump, player)) or
                          (state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) and
                           world.options.rocket_jumps) or
                          (world.options.rocket_jumps and
                           world.options.water_mech),

        # Spin Jump Module
        LocationName.loc_module_spinjump:
            lambda state: state.has_all(ItemName.ProgressiveAqueducts, player),

        # Progressive Aqueducts 1
        LocationName.loc_progressive_aqueducts_1:
            lambda state: state.count_from_list(ItemName.ProgressiveAqueducts, player) == 0 or
                          (state.has_any(ItemName.ProgressiveAqueducts, player) and
                           (state.has(ItemName.module_spinjump, player) or
                            world.options.rocket_jumps)),

        # Progressive Aqueducts 2
        LocationName.loc_progressive_aqueducts_2:
            lambda state: state.has_any(ItemName.ProgressiveAqueducts, player) or
                          (world.options.rocket_jumps and
                           world.options.water_mech),

        # Progressive Aqueducts 3
        LocationName.loc_progressive_aqueducts_3:
            lambda state: state.count_from_list(ItemName.ProgressiveAqueducts, player) == 2 or
                          (state.has_from_list(ItemName.ProgressiveAqueducts, player, 2) and
                           (state.has(ItemName.module_spinjump, player) or
                            world.options.rocket_jumps)),

        # HEATER CORE

        # Heater Core West Healthkit
        LocationName.loc_healthkit_heater_core_west:
            lambda state: state.has_all(ItemName.ProgressiveHeaterCore, player),

        # Heater Core East Healthkit
        LocationName.loc_healthkit_heater_core_east:
            lambda state: state.has_all(ItemName.ProgressiveHeaterCore, player),

        # Virtual Cat Cartridge
        LocationName.loc_cartridge_virtual_cat:
            lambda state: state.has_all(ItemName.ProgressiveHeaterCore, player),

        # Meowtrix Cartridge
        LocationName.loc_cartridge_meowtrix:
            lambda state: state.has_all(ItemName.ProgressiveHeaterCore, player),

        # Chewed Gum Cartridge
        LocationName.loc_cartridge_chewed_gum:
            lambda state: state.has_all(ItemName.ProgressiveHeaterCore, player),

        # Phase Module
        LocationName.loc_module_phase:
            lambda state: state.has_from_list(ItemName.ProgressiveHeaterCore, player, 2) or
                          state.has(ItemName.module_phase, player),

        # Coolant Module
        LocationName.loc_module_coolant:
            lambda state: (state.has_from_list(ItemName.ProgressiveHeaterCore, player, 2) and
                           state.has(ItemName.module_phase, player)) or
                          (state.has_any(ItemName.ProgressiveHeaterCore, player) and
                           state.has(ItemName.module_phase, player) and
                           world.options.rocket_jumps and
                           world.options.small_mech) or
                          state.has(ItemName.module_phase, player),

        # Progressive Heater Core 1
        # LocationName.loc_progressive_heater_core_1: lambda state: True,

        # Progressive Heater Core 2
        LocationName.loc_progressive_heater_core_2:
            lambda state: state.has_any(ItemName.ProgressiveHeaterCore, player) or
                          state.has(ItemName.module_phase, player),

        # Progressive Heater Core 3
        LocationName.loc_progressive_heater_core_3:
            lambda state: (state.has_from_list(ItemName.ProgressiveHeaterCore, player, 2) and
                           state.has(ItemName.module_phase, player)) or
                          (state.has_any(ItemName.ProgressiveHeaterCore, player) and
                           state.has(ItemName.module_phase, player) and
                           world.options.rocket_jumps and
                           world.options.small_mech) or
                          state.has(ItemName.module_phase, player),

        # VENTILATION

        # Ventilation Healthkit
        LocationName.loc_healthkit_ventilation:
            lambda state: state.has_any(ItemName.ProgressiveVentilation, player),

        # Gris Cartridge
        LocationName.loc_cartridge_gris:
            lambda state: state.has_all(ItemName.ProgressiveVentilation, player),

        # Grape Cartridge
        LocationName.loc_cartridge_grape:
            lambda state: state.has_all(ItemName.ProgressiveVentilation, player),

        # Bigshot Module
        LocationName.loc_module_bigshot:
            lambda state: state.has_any(ItemName.ProgressiveVentilation, player),

        # Progressive Ventilation 1
        # LocationName.loc_progressive_ventilation_1: lambda state: True,

        # Progressive Ventilation 2
        LocationName.loc_progressive_ventilation_2:
            lambda state: state.has_any(ItemName.ProgressiveVentilation, player),

        # Progressive Ventilation 3
        LocationName.loc_progressive_ventilation_3:
            lambda state: state.has_from_list(ItemName.ProgressiveVentilation, player, 2),

        # INCUBATOR

        # Incubator Healthkit
        LocationName.loc_healthkit_incubator:
            lambda state: state.has_all([ItemName.module_spinjump,
                                         ItemName.module_hopper,
                                         ItemName.module_phase], player)

        # Tamagato Cartridge
        # LocationName.loc_cartridge_tamagato: lambda state: True

    }

    region_logic: Dict[str, Any] = {
        RegionName.region_nexus:
            lambda state: state.has(ItemName.module_missile, player),
        RegionName.region_heater_core:
            lambda state: state.has(ItemName.module_spinjump, player) or
                          world.options.rocket_jumps,
        RegionName.region_ventilation:
            lambda state: state.has_from_list(ItemName.ProgressiveHeaterCore, player, 2) and
                          (state.has(ItemName.module_spinjump, player) or
                           world.options.rocket_jumps),
        RegionName.region_incubator:
            lambda state: state.has_all(ItemName.ProgressiveAqueducts, player) and
                          state.has_all(ItemName.ProgressiveHeaterCore, player) and
                          state.has_all(ItemName.ProgressiveVentilation, player) and
                          state.has(ItemName.module_decoder, player)
    }

    for location in location_logic:
        set_rule(world.get_location(location), location_logic[location])

    for region in region_logic:
        set_rule(world.get_region(region).entrances[0], region_logic[region])
