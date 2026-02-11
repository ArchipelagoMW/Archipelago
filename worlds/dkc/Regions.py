from BaseClasses import MultiWorld, Region, ItemClassification
from .Locations import DKCLocation
from .Items import DKCItem
from .Names import LocationName, RegionName, EventName
from worlds.AutoWorld import World

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKCWorld

def create_regions(world: "DKCWorld", active_locations):
    multiworld = world.multiworld
    player = world.player

    menu = Region('Menu', player, multiworld)

    # Worlds
    dk_isle = Region(RegionName.dk_isle, player, multiworld)
    kongo_jungle = Region(RegionName.kongo_jungle, player, multiworld)
    monkey_mines = Region(RegionName.monkey_mines, player, multiworld)
    vine_valley = Region(RegionName.vine_valley, player, multiworld)
    gorilla_glacier = Region(RegionName.gorilla_glacier, player, multiworld)
    kremkroc_industries = Region(RegionName.kremkroc_industries, player, multiworld)
    chimp_caverns = Region(RegionName.chimp_caverns, player, multiworld)
    gangplank_galleon = Region(RegionName.gangplank_galleon, player, multiworld)

    jungle_hijinxs_map = Region(RegionName.jungle_hijinxs_map, player, multiworld)
    ropey_rampage_map = Region(RegionName.ropey_rampage_map, player, multiworld)
    reptile_rumble_map = Region(RegionName.reptile_rumble_map, player, multiworld)
    coral_capers_map = Region(RegionName.coral_capers_map, player, multiworld)
    barrel_cannon_canyon_map = Region(RegionName.barrel_cannon_canyon_map, player, multiworld)
    very_gnawty_lair_map = Region(RegionName.very_gnawty_lair_map, player, multiworld)
    winky_walkway_map = Region(RegionName.winky_walkway_map, player, multiworld)
    mine_cart_carnage_map = Region(RegionName.mine_cart_carnage_map, player, multiworld)
    bouncy_bonanza_map = Region(RegionName.bouncy_bonanza_map, player, multiworld)
    stop_go_station_map = Region(RegionName.stop_go_station_map, player, multiworld)
    millstone_mayhem_map = Region(RegionName.millstone_mayhem_map, player, multiworld)
    necky_nuts_map = Region(RegionName.necky_nuts_map, player, multiworld)
    vulture_culture_map = Region(RegionName.vulture_culture_map, player, multiworld)
    tree_top_town_map = Region(RegionName.tree_top_town_map, player, multiworld)
    forest_frenzy_map = Region(RegionName.forest_frenzy_map, player, multiworld)
    temple_tempest_map = Region(RegionName.temple_tempest_map, player, multiworld)
    orang_utan_gang_map = Region(RegionName.orang_utan_gang_map, player, multiworld)
    clam_city_map = Region(RegionName.clam_city_map, player, multiworld)
    bumble_b_rumble_map = Region(RegionName.bumble_b_rumble_map, player, multiworld)
    snow_barrel_blast_map = Region(RegionName.snow_barrel_blast_map, player, multiworld)
    slipslide_ride_map = Region(RegionName.slipslide_ride_map, player, multiworld)
    ice_age_alley_map = Region(RegionName.ice_age_alley_map, player, multiworld)
    croctopus_chase_map = Region(RegionName.croctopus_chase_map, player, multiworld)
    torchlight_trouble_map = Region(RegionName.torchlight_trouble_map, player, multiworld)
    rope_bridge_rumble_map = Region(RegionName.rope_bridge_rumble_map, player, multiworld)
    really_gnawty_rampage_map = Region(RegionName.really_gnawty_rampage_map, player, multiworld)
    oil_drum_alley_map = Region(RegionName.oil_drum_alley_map, player, multiworld)
    trick_track_trek_map = Region(RegionName.trick_track_trek_map, player, multiworld)
    elevator_antics_map = Region(RegionName.elevator_antics_map, player, multiworld)
    poison_pond_map = Region(RegionName.poison_pond_map, player, multiworld)
    mine_cart_madness_map = Region(RegionName.mine_cart_madness_map, player, multiworld)
    blackout_basement_map = Region(RegionName.blackout_basement_map, player, multiworld)
    boss_dumb_drum_map = Region(RegionName.boss_dumb_drum_map, player, multiworld)
    tanked_up_trouble_map = Region(RegionName.tanked_up_trouble_map, player, multiworld)
    manic_mincers_map = Region(RegionName.manic_mincers_map, player, multiworld)
    misty_mine_map = Region(RegionName.misty_mine_map, player, multiworld)
    loopy_lights_map = Region(RegionName.loopy_lights_map, player, multiworld)
    platform_perils_map = Region(RegionName.platform_perils_map, player, multiworld)
    necky_revenge_map = Region(RegionName.necky_revenge_map, player, multiworld)

    jungle_hijinxs_level = Region(RegionName.jungle_hijinxs_level, player, multiworld)
    ropey_rampage_level = Region(RegionName.ropey_rampage_level, player, multiworld)
    reptile_rumble_level = Region(RegionName.reptile_rumble_level, player, multiworld)
    coral_capers_level = Region(RegionName.coral_capers_level, player, multiworld)
    barrel_cannon_canyon_level = Region(RegionName.barrel_cannon_canyon_level, player, multiworld)
    very_gnawty_lair_level = Region(RegionName.very_gnawty_lair_level, player, multiworld)
    winky_walkway_level = Region(RegionName.winky_walkway_level, player, multiworld)
    mine_cart_carnage_level = Region(RegionName.mine_cart_carnage_level, player, multiworld)
    bouncy_bonanza_level = Region(RegionName.bouncy_bonanza_level, player, multiworld)
    stop_go_station_level = Region(RegionName.stop_go_station_level, player, multiworld)
    millstone_mayhem_level = Region(RegionName.millstone_mayhem_level, player, multiworld)
    necky_nuts_level = Region(RegionName.necky_nuts_level, player, multiworld)
    vulture_culture_level = Region(RegionName.vulture_culture_level, player, multiworld)
    tree_top_town_level = Region(RegionName.tree_top_town_level, player, multiworld)
    forest_frenzy_level = Region(RegionName.forest_frenzy_level, player, multiworld)
    temple_tempest_level = Region(RegionName.temple_tempest_level, player, multiworld)
    orang_utan_gang_level = Region(RegionName.orang_utan_gang_level, player, multiworld)
    clam_city_level = Region(RegionName.clam_city_level, player, multiworld)
    bumble_b_rumble_level = Region(RegionName.bumble_b_rumble_level, player, multiworld)
    snow_barrel_blast_level = Region(RegionName.snow_barrel_blast_level, player, multiworld)
    slipslide_ride_level = Region(RegionName.slipslide_ride_level, player, multiworld)
    ice_age_alley_level = Region(RegionName.ice_age_alley_level, player, multiworld)
    croctopus_chase_level = Region(RegionName.croctopus_chase_level, player, multiworld)
    torchlight_trouble_level = Region(RegionName.torchlight_trouble_level, player, multiworld)
    rope_bridge_rumble_level = Region(RegionName.rope_bridge_rumble_level, player, multiworld)
    really_gnawty_rampage_level = Region(RegionName.really_gnawty_rampage_level, player, multiworld)
    oil_drum_alley_level = Region(RegionName.oil_drum_alley_level, player, multiworld)
    trick_track_trek_level = Region(RegionName.trick_track_trek_level, player, multiworld)
    elevator_antics_level = Region(RegionName.elevator_antics_level, player, multiworld)
    poison_pond_level = Region(RegionName.poison_pond_level, player, multiworld)
    mine_cart_madness_level = Region(RegionName.mine_cart_madness_level, player, multiworld)
    blackout_basement_level = Region(RegionName.blackout_basement_level, player, multiworld)
    boss_dumb_drum_level = Region(RegionName.boss_dumb_drum_level, player, multiworld)
    tanked_up_trouble_level = Region(RegionName.tanked_up_trouble_level, player, multiworld)
    manic_mincers_level = Region(RegionName.manic_mincers_level, player, multiworld)
    misty_mine_level = Region(RegionName.misty_mine_level, player, multiworld)
    loopy_lights_level = Region(RegionName.loopy_lights_level, player, multiworld)
    platform_perils_level = Region(RegionName.platform_perils_level, player, multiworld)
    necky_revenge_level = Region(RegionName.necky_revenge_level, player, multiworld)

    multiworld.regions += [
        menu,
        dk_isle,
        kongo_jungle,
        monkey_mines,
        vine_valley,
        gorilla_glacier,
        kremkroc_industries,
        chimp_caverns,
        gangplank_galleon,

        jungle_hijinxs_map,
        ropey_rampage_map,
        reptile_rumble_map,
        coral_capers_map,
        barrel_cannon_canyon_map,
        very_gnawty_lair_map,
        winky_walkway_map,
        mine_cart_carnage_map,
        bouncy_bonanza_map,
        stop_go_station_map,
        millstone_mayhem_map,
        necky_nuts_map,
        vulture_culture_map,
        tree_top_town_map,
        forest_frenzy_map,
        temple_tempest_map,
        orang_utan_gang_map,
        clam_city_map,
        bumble_b_rumble_map,
        snow_barrel_blast_map,
        slipslide_ride_map,
        ice_age_alley_map,
        croctopus_chase_map,
        torchlight_trouble_map,
        rope_bridge_rumble_map,
        really_gnawty_rampage_map,
        oil_drum_alley_map,
        trick_track_trek_map,
        elevator_antics_map,
        poison_pond_map,
        mine_cart_madness_map,
        blackout_basement_map,
        boss_dumb_drum_map,
        tanked_up_trouble_map,
        manic_mincers_map,
        misty_mine_map,
        loopy_lights_map,
        platform_perils_map,
        necky_revenge_map,

        jungle_hijinxs_level,
        ropey_rampage_level,
        reptile_rumble_level,
        coral_capers_level,
        barrel_cannon_canyon_level,
        very_gnawty_lair_level,
        winky_walkway_level,
        mine_cart_carnage_level,
        bouncy_bonanza_level,
        stop_go_station_level,
        millstone_mayhem_level,
        necky_nuts_level,
        vulture_culture_level,
        tree_top_town_level,
        forest_frenzy_level,
        temple_tempest_level,
        orang_utan_gang_level,
        clam_city_level,
        bumble_b_rumble_level,
        snow_barrel_blast_level,
        slipslide_ride_level,
        ice_age_alley_level,
        croctopus_chase_level,
        torchlight_trouble_level,
        rope_bridge_rumble_level,
        really_gnawty_rampage_level,
        oil_drum_alley_level,
        trick_track_trek_level,
        elevator_antics_level,
        poison_pond_level,
        mine_cart_madness_level,
        blackout_basement_level,
        boss_dumb_drum_level,
        tanked_up_trouble_level,
        manic_mincers_level,
        misty_mine_level,
        loopy_lights_level,
        platform_perils_level,
        necky_revenge_level,
    ]

    # Level clears
    add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.very_gnawty_lair_level, LocationName.very_gnawty_lair_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.necky_nuts_level, LocationName.necky_nuts_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.clam_city_level, LocationName.clam_city_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.bumble_b_rumble_level, LocationName.bumble_b_rumble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.torchlight_trouble_level, LocationName.torchlight_trouble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.rope_bridge_rumble_level, LocationName.rope_bridge_rumble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.really_gnawty_rampage_level, LocationName.really_gnawty_rampage_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.boss_dumb_drum_level, LocationName.boss_dumb_drum_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.necky_revenge_level, LocationName.necky_revenge_clear)

    add_location_to_region(multiworld, player, active_locations, RegionName.very_gnawty_lair_level, LocationName.defeated_gnawty_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.necky_nuts_level, LocationName.defeated_necky_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.bumble_b_rumble_level, LocationName.defeated_bumble_b)
    add_location_to_region(multiworld, player, active_locations, RegionName.really_gnawty_rampage_level, LocationName.defeated_gnawty_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.boss_dumb_drum_level, LocationName.defeated_boss_dumb_drum)
    add_location_to_region(multiworld, player, active_locations, RegionName.necky_revenge_level, LocationName.defeated_necky_2)

    add_event_to_region(multiworld, player, RegionName.gangplank_galleon, LocationName.k_rool_clear, EventName.k_rool)

    # Level clears (events)
    add_event_to_region(multiworld, player, RegionName.jungle_hijinxs_level, EventName.jungle_hijinxs_clear, EventName.jungle_level)
    add_event_to_region(multiworld, player, RegionName.ropey_rampage_level, EventName.ropey_rampage_clear, EventName.jungle_level)
    add_event_to_region(multiworld, player, RegionName.reptile_rumble_level, EventName.reptile_rumble_clear, EventName.jungle_level)
    add_event_to_region(multiworld, player, RegionName.coral_capers_level, EventName.coral_capers_clear, EventName.jungle_level)
    add_event_to_region(multiworld, player, RegionName.barrel_cannon_canyon_level, EventName.barrel_cannon_canyon_clear, EventName.jungle_level)
    add_event_to_region(multiworld, player, RegionName.winky_walkway_level, EventName.winky_walkway_clear, EventName.mines_level)
    add_event_to_region(multiworld, player, RegionName.mine_cart_carnage_level, EventName.mine_cart_carnage_clear, EventName.mines_level)
    add_event_to_region(multiworld, player, RegionName.bouncy_bonanza_level, EventName.bouncy_bonanza_clear, EventName.mines_level)
    add_event_to_region(multiworld, player, RegionName.stop_go_station_level, EventName.stop_go_station_clear, EventName.mines_level)
    add_event_to_region(multiworld, player, RegionName.millstone_mayhem_level, EventName.millstone_mayhem_clear, EventName.mines_level)
    add_event_to_region(multiworld, player, RegionName.vulture_culture_level, EventName.vulture_culture_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.tree_top_town_level, EventName.tree_top_town_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.forest_frenzy_level, EventName.forest_frenzy_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.temple_tempest_level, EventName.temple_tempest_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.orang_utan_gang_level, EventName.orang_utan_gang_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.clam_city_level, EventName.clam_city_clear, EventName.valley_level)
    add_event_to_region(multiworld, player, RegionName.snow_barrel_blast_level, EventName.snow_barrel_blast_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.slipslide_ride_level, EventName.slipslide_ride_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.ice_age_alley_level, EventName.ice_age_alley_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.croctopus_chase_level, EventName.croctopus_chase_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.torchlight_trouble_level, EventName.torchlight_trouble_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.rope_bridge_rumble_level, EventName.rope_bridge_rumble_clear, EventName.glacier_level)
    add_event_to_region(multiworld, player, RegionName.oil_drum_alley_level, EventName.oil_drum_alley_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.trick_track_trek_level, EventName.trick_track_trek_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.elevator_antics_level, EventName.elevator_antics_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.poison_pond_level, EventName.poison_pond_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.mine_cart_madness_level, EventName.mine_cart_madness_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.blackout_basement_level, EventName.blackout_basement_clear, EventName.industries_level)
    add_event_to_region(multiworld, player, RegionName.tanked_up_trouble_level, EventName.tanked_up_trouble_clear, EventName.caverns_level)
    add_event_to_region(multiworld, player, RegionName.manic_mincers_level, EventName.manic_mincers_clear, EventName.caverns_level)
    add_event_to_region(multiworld, player, RegionName.misty_mine_level, EventName.misty_mine_clear, EventName.caverns_level)
    add_event_to_region(multiworld, player, RegionName.loopy_lights_level, EventName.loopy_lights_clear, EventName.caverns_level)
    add_event_to_region(multiworld, player, RegionName.platform_perils_level, EventName.platform_perils_clear, EventName.caverns_level)

    # Bonuses
    add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bonus_4)
    add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bonus_5)
    add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.torchlight_trouble_level, LocationName.torchlight_trouble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.torchlight_trouble_level, LocationName.torchlight_trouble_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.rope_bridge_rumble_level, LocationName.rope_bridge_rumble_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.rope_bridge_rumble_level, LocationName.rope_bridge_rumble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bonus_4)
    add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_bonus_2)

    if world.options.kong_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.clam_city_level, LocationName.clam_city_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.torchlight_trouble_level, LocationName.torchlight_trouble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.rope_bridge_rumble_level, LocationName.rope_bridge_rumble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_kong)

    if world.options.balloon_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_balloon_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.croctopus_chase_balloon_1)

    if world.options.token_checks:   
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_token_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_token_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.clam_city_level, LocationName.clam_city_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_token_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_token_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_token_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_token_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_token_1)

    if world.options.banana_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_11)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_12)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_13)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_14)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_15)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_16)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_17)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_18)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_hijinxs_level, LocationName.jungle_hijinxs_bunch_19)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_11)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_12)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_13)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_14)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_15)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_16)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_17)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_18)
        add_location_to_region(multiworld, player, active_locations, RegionName.ropey_rampage_level, LocationName.ropey_rampage_bunch_19)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_11)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_12)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_13)
        add_location_to_region(multiworld, player, active_locations, RegionName.reptile_rumble_level, LocationName.reptile_rumble_bunch_14)
        add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.coral_capers_level, LocationName.coral_capers_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_11)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_cannon_canyon_level, LocationName.barrel_cannon_canyon_bunch_12)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.winky_walkway_level, LocationName.winky_walkway_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_carnage_level, LocationName.mine_cart_carnage_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.bouncy_bonanza_level, LocationName.bouncy_bonanza_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.stop_go_station_level, LocationName.stop_go_station_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.millstone_mayhem_level, LocationName.millstone_mayhem_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.vulture_culture_level, LocationName.vulture_culture_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.tree_top_town_level, LocationName.tree_top_town_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.forest_frenzy_level, LocationName.forest_frenzy_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.temple_tempest_level, LocationName.temple_tempest_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.orang_utan_gang_level, LocationName.orang_utan_gang_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.clam_city_level, LocationName.clam_city_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.clam_city_level, LocationName.clam_city_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.snow_barrel_blast_level, LocationName.snow_barrel_blast_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.slipslide_ride_level, LocationName.slipslide_ride_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.ice_age_alley_level, LocationName.ice_age_alley_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.croctopus_chase_level, LocationName.croctopus_chase_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.torchlight_trouble_level, LocationName.torchlight_trouble_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rope_bridge_rumble_level, LocationName.rope_bridge_rumble_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.oil_drum_alley_level, LocationName.oil_drum_alley_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.trick_track_trek_level, LocationName.trick_track_trek_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.elevator_antics_level, LocationName.elevator_antics_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.poison_pond_level, LocationName.poison_pond_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.mine_cart_madness_level, LocationName.mine_cart_madness_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.blackout_basement_level, LocationName.blackout_basement_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.tanked_up_trouble_level, LocationName.tanked_up_trouble_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.manic_mincers_level, LocationName.manic_mincers_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.misty_mine_level, LocationName.misty_mine_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.loopy_lights_level, LocationName.loopy_lights_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.platform_perils_level, LocationName.platform_perils_bunch_1)

def connect_regions(world: "DKCWorld"):
    connect(world, "Menu", RegionName.dk_isle)

    connect(world, RegionName.dk_isle, RegionName.kongo_jungle)
    connect(world, RegionName.dk_isle, RegionName.monkey_mines)
    connect(world, RegionName.dk_isle, RegionName.vine_valley)
    connect(world, RegionName.dk_isle, RegionName.gorilla_glacier)
    connect(world, RegionName.dk_isle, RegionName.kremkroc_industries)
    connect(world, RegionName.dk_isle, RegionName.chimp_caverns)
    connect(world, RegionName.dk_isle, RegionName.gangplank_galleon)

    connect(world, RegionName.kongo_jungle, RegionName.jungle_hijinxs_map)
    connect(world, RegionName.kongo_jungle, RegionName.ropey_rampage_map)
    connect(world, RegionName.kongo_jungle, RegionName.reptile_rumble_map)
    connect(world, RegionName.kongo_jungle, RegionName.coral_capers_map)
    connect(world, RegionName.kongo_jungle, RegionName.barrel_cannon_canyon_map)
    connect(world, RegionName.kongo_jungle, RegionName.very_gnawty_lair_map)

    connect(world, RegionName.monkey_mines, RegionName.winky_walkway_map)
    connect(world, RegionName.monkey_mines, RegionName.mine_cart_carnage_map)
    connect(world, RegionName.monkey_mines, RegionName.bouncy_bonanza_map)
    connect(world, RegionName.monkey_mines, RegionName.stop_go_station_map)
    connect(world, RegionName.monkey_mines, RegionName.millstone_mayhem_map)
    connect(world, RegionName.monkey_mines, RegionName.necky_nuts_map)

    connect(world, RegionName.vine_valley, RegionName.vulture_culture_map)
    connect(world, RegionName.vine_valley, RegionName.tree_top_town_map)
    connect(world, RegionName.vine_valley, RegionName.forest_frenzy_map)
    connect(world, RegionName.vine_valley, RegionName.temple_tempest_map)
    connect(world, RegionName.vine_valley, RegionName.orang_utan_gang_map)
    connect(world, RegionName.vine_valley, RegionName.clam_city_map)
    connect(world, RegionName.vine_valley, RegionName.bumble_b_rumble_map)

    connect(world, RegionName.gorilla_glacier, RegionName.snow_barrel_blast_map)
    connect(world, RegionName.gorilla_glacier, RegionName.slipslide_ride_map)
    connect(world, RegionName.gorilla_glacier, RegionName.ice_age_alley_map)
    connect(world, RegionName.gorilla_glacier, RegionName.croctopus_chase_map)
    connect(world, RegionName.gorilla_glacier, RegionName.torchlight_trouble_map)
    connect(world, RegionName.gorilla_glacier, RegionName.rope_bridge_rumble_map)
    connect(world, RegionName.gorilla_glacier, RegionName.really_gnawty_rampage_map)

    connect(world, RegionName.kremkroc_industries, RegionName.oil_drum_alley_map)
    connect(world, RegionName.kremkroc_industries, RegionName.trick_track_trek_map)
    connect(world, RegionName.kremkroc_industries, RegionName.elevator_antics_map)
    connect(world, RegionName.kremkroc_industries, RegionName.poison_pond_map)
    connect(world, RegionName.kremkroc_industries, RegionName.mine_cart_madness_map)
    connect(world, RegionName.kremkroc_industries, RegionName.blackout_basement_map)
    connect(world, RegionName.kremkroc_industries, RegionName.boss_dumb_drum_map)

    connect(world, RegionName.chimp_caverns, RegionName.tanked_up_trouble_map)
    connect(world, RegionName.chimp_caverns, RegionName.manic_mincers_map)
    connect(world, RegionName.chimp_caverns, RegionName.misty_mine_map)
    connect(world, RegionName.chimp_caverns, RegionName.loopy_lights_map)
    connect(world, RegionName.chimp_caverns, RegionName.platform_perils_map)
    connect(world, RegionName.chimp_caverns, RegionName.necky_revenge_map)

    for map_level, level in world.level_connections.items():
        connect(world, map_level, level)


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None):
    region = multiworld.get_region(region_name, player)
    event = DKCLocation(player, event_name, None, region)
    if event_item:
        event.place_locked_item(DKCItem(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(DKCItem(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = DKCLocation(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: World, source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
