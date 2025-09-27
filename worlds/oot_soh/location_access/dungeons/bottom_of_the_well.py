from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (add_locations, connect_regions, can_pass_enemy, has_explosives, lens_or_skip, can_open_underwater_chest, 
                                         can_cut_shrubs, blast_or_smash, can_break_pots, has_item, take_damage,can_use, small_keys, can_get_enemy_drop, 
                                         can_detonate_upright_bomb_flower, has_fire_source_with_torch, can_kill_enemy)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    "LoweredWaterInsideBotw": SohLocationData(Regions.BOTTOM_OF_THE_WELL_PERIMETER, event_item="Water was lowered in the BotW")
}


def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_rules(world)

def set_rules(world: "SohWorld") -> None:
    player = world.player
    
    ## Bottom of The Well Entryway
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, world, [])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA.value)], # Technically involves an fake wall, but passing it lensless is intended in vanilla and it is well telegraphed
        #[Regions.BOTTOM_OF_THE_WELL_MQ_PERIMETER.value, lambda state: is_child(state, world)],
        [Regions.KAK_WELL.value, lambda state: True]
    ])

    ## Bottom of the Well Perimeter
    # NOT SURE HOW TO ENTER THIS
    #  //Events
    #     EventAccess(&logic->StickPot,               []{return true;}),
    #     EventAccess(&logic->NutPot,                 []{return true;}),
    #     EventAccess(&logic->LoweredWaterInsideBotw, []{return logic->CanUse(RG_ZELDAS_LULLABY);}),
    # },
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_CENTER_BOMBABLE_CHEST.value, lambda state: has_explosives(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_FRONT_CHEST.value, lambda state: state.has(events.get("LoweredWaterInsideBotw").event_item) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_LEFT_CHEST.value, lambda state: state.has(events.get("LoweredWaterInsideBotw").event_item) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_POT.value, lambda state: (can_break_pots(state, world) and state.has(events.get("LoweredWaterInsideBotw").event_item)) or can_use(Items.BOOMERANG.value, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA.value)],
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, lambda state: lens_or_skip(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, lambda state: lens_or_skip(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM.value, lambda state: state.has(events.get("LoweredWaterInsideBotw").event_item) or has_item(Items.BRONZE_SCALE.value, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM.value, lambda state: state.has(events.get("LoweredWaterInsideBotw").event_item) and is_child(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True]
    ])

    ## Bottom of the Well Behind Fake Walls
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_LEFT_FAKE_WALL_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_RIGHT_BOTTOM_FAKE_WALL_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COMPASS_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_CENTER_SKULLTULA_CHEST.value, lambda state: can_pass_enemy(Enemies.BIG_SKULLTULA.value, state, world) or take_damage(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BACK_LEFT_BOMBABLE_CHEST.value, lambda state: has_explosives(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS.value, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM.value, lambda state: lens_or_skip(state, world)]
    ])

    ## Bottom of the Well Southwest Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT3.value, lambda state: can_break_pots(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip(state, world)]
    ])

    ## Bottom of the Well Keese-Beamos Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_CHEST.value, lambda state: lens_or_skip(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_POT1.value, lambda state: can_break_pots(state, world) and lens_or_skip(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world) and lens_or_skip(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip(state, world)]
    ])

    ## Bottom of the Well Like-Like Cage
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        [Locations.BOTTOM_OF_THE_WELL_LIKE_LIKE_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_GS_LIKE_LIKE_CAGE.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, lambda state: True]
    ])

    ## Bottom of the Well Inner Rooms
    # NOT SURE HOW TO ENTER THIS
    #  //Events
    #     EventAccess(&logic->DekuBabaSticks, []{return logic->CanGetDekuBabaSticks();}),
    #     EventAccess(&logic->DekuBabaNuts,   []{return logic->CanGetDekuBabaNuts();}),
    # }, 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        [Locations.BOTTOM_OF_THE_WELL_GS_WEST_INNER_ROOM.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)],
        [Locations.BOTTOM_OF_THE_WELL_GS_EAST_INNER_ROOM.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)]
    ])

    ## Bottom of the Well Coffin Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_FREESTANDING_KEY.value, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_FRONT_LEFT_HEART.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_MIDDLE_RIGHT_HEART.value, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW.value, state, world)]

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: state.has(events.get("LoweredWaterInsideBotw").event_item) or has_item(Items.BRONZE_SCALE.value, state, world)]
    ])

    ## Bottom of the Well Dead Hand Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST.value, lambda state: can_kill_enemy(Enemies.DEAD_HAND.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_INVISIBLE_CHEST.value, lambda state: lens_or_skip(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and can_kill_enemy(Enemies.DEAD_HAND.value, state, world)]
    ])

    ## Bottom of the Well Basement 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST.value, lambda state: blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT3.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT4.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT5.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT6.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT7.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT8.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT9.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT10.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT11.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT12.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_MQ_BASEMENT_SUNS_SONG_FAIRY.value, lambda state: can_use(Items.SUNS_SONG.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS1.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS2.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS3.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS1.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS2.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS3.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS4.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS5.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS6.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS7.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS8.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS9.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, lambda state: is_child(state, world) and can_pass_enemy(Enemies.BIG_SKULLTULA.value, state, world)],
        # False here is for trick ctx->GetTrickOption(RT_BOTW_BASEMENT)
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS.value, lambda state: blast_or_smash(state, world) or can_use(Items.DINS_FIRE.value, state, world) or (can_use(Items.STICKS.value) and False)] # NOT 100% SURE HOW TO TRANSLATE HERE. Has to do with Age: Entrance(RR_BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, []{return Here(RR_BOTTOM_OF_THE_WELL_BASEMENT, []{return logic->BlastOrSmash() || logic->CanUse(RG_DINS_FIRE) || (logic->CanUse(RG_STICKS) && ctx->GetTrickOption(RT_BOTW_BASEMENT));});}),
    ])

    ## Bottom of the Well Useful Bomb Flowers
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST.value, lambda state: has_item(Items.GORONS_BRACELET.value, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: can_detonate_upright_bomb_flower(state, world)]
    ])

    ## Bottom of the Well Basement Platform
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_LEFT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_LEFT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_MIDDLE_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_RIGHT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_RIGHT_RUPEE.value, lambda state: True],
        
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True]
    ])