from typing import Dict, TYPE_CHECKING

from .Rac2Interface import PLANET_LIST_SIZE, INVENTORY_SIZE, NANOTECH_BOOST_MAX
from .TextManager import get_rich_item_name
from .data import Planets, Locations, Items

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context

PLANET_UNLOCK_TO_LOCATION_ID: Dict[int, int] = {
    Planets.MAKTAR_NEBULA.number: Locations.OOZLA_END_STORE_CUTSCENE.location_id,
    Planets.ENDAKO.number: Locations.MAKTAR_PHOTO_BOOTH.location_id,
    Planets.BARLOW.number: Locations.MAKTAR_DEACTIVATE_JAMMING_ARRAY.location_id,
    Planets.FELTZIN_SYSTEM.number: Locations.BARLOW_HOVERBIKE_RACE_TRANSMISSION.location_id,
    Planets.NOTAK.number: Locations.FELTZIN_DEFEAT_THUG_SHIPS.location_id,
    Planets.SIBERIUS.number: Locations.NOTAK_WORKER_BOTS.location_id,
    Planets.TABORA.number: Locations.SIBERIUS_DEFEAT_THIEF.location_id,
    Planets.DOBBO.number: Locations.TABORA_MEET_ANGELA.location_id,
    Planets.HRUGIS_CLOUD.number: Locations.DOBBO_FACILITY_TERMINAL.location_id,
    Planets.JOBA.number: Locations.DOBBO_DEFEAT_THUG_LEADER.location_id,
    Planets.TODANO.number: Locations.HRUGIS_DESTROY_DEFENSES.location_id,
    Planets.BOLDAN.number: Locations.TODANO_SEARCH_ROCKET_SILO.location_id,
    Planets.ARANOS_PRISON.number: Locations.BOLDAN_FIND_FIZZWIDGET.location_id,
    Planets.GORN.number: Locations.ARANOS_CONTROL_ROOM.location_id,
    Planets.SNIVELAK.number: Locations.GORN_DEFEAT_THUG_FLEET.location_id,
    Planets.SMOLG.number: Locations.SNIVELAK_RESCUE_ANGELA.location_id,
    Planets.DAMOSEL.number: Locations.SMOLG_MUTANT_CRAB.location_id,
    Planets.GRELBIN.number: Locations.SMOLG_BALLOON_TRANSMISSION.location_id,
    Planets.YEEDIL.number: Locations.GRELBIN_FIND_ANGELA.location_id,
    Planets.SHIP_SHACK.number: Locations.NOTAK_TOP_PIER_TELESCREEN.location_id
}

INVENTORY_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    Items.HELI_PACK.offset: Locations.ENDAKO_RESCUE_CLANK_HELI.location_id,
    Items.THRUSTER_PACK.offset: Locations.ENDAKO_RESCUE_CLANK_THRUSTER.location_id,
    Items.MAPPER.offset: Locations.DAMOSEL_DEFEAT_MOTHERSHIP.location_id,
    Items.ARMOR_MAGNETIZER.offset: Locations.TODANO_STUART_ZURGO_TRADE.location_id,
    Items.LEVITATOR.offset: Locations.JOBA_SHADY_SALESMAN.location_id,
    Items.SWINGSHOT.offset: Locations.ENDAKO_CLANK_APARTMENT_SS.location_id,
    Items.GRAVITY_BOOTS.offset: Locations.JOBA_ARENA_BATTLE.location_id,
    Items.GRIND_BOOTS.offset: Locations.ENDAKO_CLANK_APARTMENT_GB.location_id,
    Items.GLIDER.offset: Locations.TABORA_UNDERGROUND_MINES_END.location_id,
    Items.DYNAMO.offset: Locations.OOZLA_OUTSIDE_MEGACORP_STORE.location_id,
    Items.ELECTROLYZER.offset: Locations.MAKTAR_ARENA_CHALLENGE.location_id,
    Items.THERMANATOR.offset: Locations.BARLOW_INVENTOR.location_id,
    Items.TRACTOR_BEAM.offset: Locations.OOZLA_MEGACORP_SCIENTIST.location_id,
    Items.QWARK_STATUETTE.offset: Locations.ARANOS_PLUMBER.location_id,
    Items.BOX_BREAKER.offset: Locations.OOZLA_SWAMP_MONSTER_II.location_id,
    Items.INFILTRATOR.offset: Locations.JOBA_ARENA_CAGE_MATCH.location_id,
    Items.CHARGE_BOOTS.offset: Locations.JOBA_FIRST_HOVERBIKE_RACE.location_id,
    Items.HYPNOMATIC.offset: Locations.DAMOSEL_HYPNOTIST.location_id,
    Items.SHEEPINATOR.offset: Locations.TODANO_FACILITY_INTERIOR.location_id
}

PLAT_BOLT_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    Planets.OOZLA.number * 4 + 1: Locations.OOZLA_SWAMP_RUINS_PB.location_id,
    Planets.OOZLA.number * 4 + 2: Locations.OOZLA_TRACTOR_PUZZLE_PB.location_id,
    Planets.MAKTAR_NEBULA.number * 4 + 1: Locations.MAKTAR_CRANE_PB.location_id,
    Planets.JAMMING_ARRAY.number * 4 + 1: Locations.MAKTAR_JAMMING_ARRAY_PB.location_id,
    Planets.ENDAKO.number * 4 + 1: Locations.ENDAKO_CRANE_PB.location_id,
    Planets.ENDAKO.number * 4 + 3: Locations.ENDAKO_LEDGE_PB.location_id,
    Planets.BARLOW.number * 4: Locations.BARLOW_HOUND_CAVE_PB.location_id,
    Planets.BARLOW.number * 4 + 1: Locations.BARLOW_HOVERBIKE_RACE_PB.location_id,
    Planets.FELTZIN_SYSTEM.number * 4: Locations.FELTZIN_RACE_PB.location_id,
    Planets.NOTAK.number * 4: Locations.NOTAK_TIMED_DYNAMO_PB.location_id,
    Planets.NOTAK.number * 4 + 1: Locations.NOTAK_PROMENADE_SIGN_PB.location_id,
    Planets.NOTAK.number * 4 + 2: Locations.NOTAK_BEHIND_BUILDING_PB.location_id,
    Planets.SIBERIUS.number * 4: Locations.SIBERIUS_FLAMEBOT_LEDGE_PB.location_id,
    Planets.SIBERIUS.number * 4 + 1: Locations.SIBERIUS_FENCED_AREA_PB.location_id,
    Planets.TABORA.number * 4: Locations.TABORA_CANYON_GLIDE_PB.location_id,
    Planets.TABORA.number * 4 + 1: Locations.TABORA_NORTHEAST_DESERT_PB.location_id,
    Planets.TABORA.number * 4 + 2: Locations.TABORA_UNDERGROUND_MINES_PB.location_id,
    Planets.DOBBO.number * 4 + 1: Locations.DOBBO_SPIDERBOT_ROOM_PB.location_id,
    Planets.DOBBO.number * 4 + 3: Locations.DOBBO_FACILITY_GLIDE_PB.location_id,
    Planets.HRUGIS_CLOUD.number * 4: Locations.HRUGIS_RACE_PB.location_id,
    Planets.JOBA.number * 4: Locations.JOBA_HIDDEN_CLIFF_PB.location_id,
    Planets.JOBA.number * 4 + 1: Locations.JOBA_LEVITATOR_TOWER_PB.location_id,
    Planets.TODANO.number * 4: Locations.TODANO_SPIDERBOT_CONVEYOR_PB.location_id,
    Planets.TODANO.number * 4 + 1: Locations.TODANO_END_TOUR_PB.location_id,
    Planets.TODANO.number * 4 + 2: Locations.TODANO_NEAR_STUART_ZURGO_PB.location_id,
    Planets.BOLDAN.number * 4: Locations.BOLDAN_FLOATING_PLATFORM_PB.location_id,
    Planets.BOLDAN.number * 4 + 1: Locations.BOLDAN_SPIDERBOT_ALLEY_PB.location_id,
    Planets.BOLDAN.number * 4 + 3: Locations.BOLDAN_UPPER_DOME_PB.location_id,
    Planets.ARANOS_PRISON.number * 4: Locations.ARANOS_UNDER_SHIP_PB.location_id,
    Planets.GORN.number * 4: Locations.GORN_RACE_PB.location_id,
    Planets.SNIVELAK.number * 4: Locations.SNIVELAK_DYNAMO_PLATFORMS_PB.location_id,
    Planets.SMOLG.number * 4 + 1: Locations.SMOLG_WAREHOUSE_PB.location_id,
    Planets.SMOLG.number * 4 + 2: Locations.SMOLG_FLOATING_PLATFORM_PB.location_id,
    Planets.DAMOSEL.number * 4: Locations.DAMOSEL_FROZEN_FOUNTAIN_PB.location_id,
    Planets.DAMOSEL.number * 4 + 1: Locations.DAMOSEL_PYRAMID_PB.location_id,
    Planets.GRELBIN.number * 4 + 1: Locations.GRELBIN_UNDERWATER_TUNNEL_PB.location_id,
    Planets.GRELBIN.number * 4 + 2: Locations.GRELBIN_YETI_CAVE_PB.location_id,
    Planets.GRELBIN.number * 4 + 3: Locations.GRELBIN_ICE_PLAINS_PB.location_id,
    Planets.YEEDIL.number * 4 + 1: Locations.YEEDIL_TRACTOR_PILLAR_PB.location_id,
    Planets.YEEDIL.number * 4 + 2: Locations.YEEDIL_BRIDGE_GRINDRAIL_PB.location_id,
}

NANOTECH_OFFSET_TO_LOCATION_ID: Dict[int, int] = {
    0: Locations.NOTAK_PROMENADE_END_NT.location_id,
    1: Locations.ENDAKO_CRANE_NT.location_id,
    2: Locations.TABORA_CANYON_GLIDE_PILLAR_NT.location_id,
    3: Locations.JOBA_TIMED_DYNAMO_NT.location_id,
    4: Locations.JOBA_HOVERBIKE_RACE_SHORTCUT_NT.location_id,
    5: Locations.SNIVELAK_SWINGSHOT_TOWER_NT.location_id,
    6: Locations.FELTZIN_CARGO_BAY_NT.location_id,
    7: Locations.TODANO_ROCKET_SILO_NT.location_id,
    8: Locations.BOLDAN_FOUNTAIN_NT.location_id,
    9: Locations.DOBBO_FACILITY_GLIDE_NT.location_id,
}


async def handle_checked_location(ctx: 'Rac2Context'):
    cleared_locations = set()
    if ctx.current_planet == -1:
        return

    # check planet unlocks table to see which coordinate locations have been checked.
    planet_table_start = ctx.game_interface.addresses.unlocked_planets
    for i, address in enumerate(range(planet_table_start, planet_table_start + PLANET_LIST_SIZE)):
        if i in PLANET_UNLOCK_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(PLANET_UNLOCK_TO_LOCATION_ID[i])

    # check secondary inventory table to see which equipment locations have been checked.
    inventory_start = ctx.game_interface.addresses.secondary_inventory
    for i, address in enumerate(range(inventory_start, inventory_start + INVENTORY_SIZE)):
        if i in INVENTORY_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(INVENTORY_OFFSET_TO_LOCATION_ID[i])

    # check platinum bolts table to see which platinum bolts locations have been checked.
    plat_bolt_table_start = ctx.game_interface.addresses.platinum_bolt_table
    for i, address in enumerate(range(plat_bolt_table_start, plat_bolt_table_start + 0x70)):
        if i in PLAT_BOLT_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(PLAT_BOLT_OFFSET_TO_LOCATION_ID[i])

    # check nanotech boosts table to see which boost locations have been checked.
    nanotech_table_start = ctx.game_interface.addresses.nanotech_boost_table
    for i, address in enumerate(range(nanotech_table_start, nanotech_table_start + NANOTECH_BOOST_MAX)):
        if i in NANOTECH_OFFSET_TO_LOCATION_ID and ctx.game_interface.pcsx2_interface.read_int8(address) == 1:
            cleared_locations.add(NANOTECH_OFFSET_TO_LOCATION_ID[i])

    # Check all location flags defined on locations
    all_active_locations = Planets.get_all_active_locations(ctx.slot_data)
    for location in all_active_locations:
        if location.checked_flag_address is not None:
            addr = location.checked_flag_address(ctx.game_interface.addresses)
            if ctx.game_interface.pcsx2_interface.read_int8(addr) != 0:
                cleared_locations.add(location.location_id)

    cleared_locations = cleared_locations.difference(ctx.checked_locations)
    item_was_bought = False
    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared_locations}])
    for location_id in cleared_locations:
        location = next(loc for loc in all_active_locations if loc.location_id == location_id)
        ctx.game_interface.logger.info(f"Location checked: {location.name}")
        if location.is_vendor:
            ctx.game_interface.vendor.notify_item_bought(location_id)
            item_was_bought = True

        net_item = ctx.locations_info.get(location_id, None)
        if net_item is not None and net_item.player != ctx.slot:
            item_to_player_names = get_rich_item_name(ctx, net_item, True)
            ctx.notification_manager.queue_notification(f"Sent {item_to_player_names}")

    if item_was_bought:
        ctx.game_interface.vendor.refresh(ctx)
