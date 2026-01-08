from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    DEKU_TREE_LOBBY_BABA_STICKS = "Deku Tree Lobby Baba Sticks",
    DEKU_TREE_LOBBY_BABA_NUTS = "Deku Tree Lobby Baba Nuts",
    DEKU_TREE_COMPASS_BABA_STICKS = "Deku Tree Compass Room Baba Sticks",
    DEKU_TREE_COMPASS_BABA_NUTS = "Deku Tree Compass Room Baba Nuts",
    DEKU_TREE_BASEMENT_LOWER_BABA_STICKS = "Deku Tree Basement Lower Baba Sticks",
    DEKU_TREE_BASEMENT_LOWER_BABA_NUTS = "Deku Tree Basement Lower Baba Nuts",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS = "Deku Tree Basement Torch Room Baba Sticks",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS = "Deku Tree Torch Room Baba Nuts",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS = "Deku Tree Basement Back Lobby Baba Sticks",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS = "Deku Tree Basement Back Lobby Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BABA_STICKS = "Deku Tree Basement Upper Baba Sticks",
    DEKU_TREE_BASEMENT_UPPER_BABA_NUTS = "Deku Tree Basement Upper Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BLOCK = "Deku Tree Basement Upper Push Block",
    DEKU_TREE_QUEEN_GOHMA = "Deku Tree Queen Gohma"


class LocalEvents(StrEnum):
    DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED = "Deku Tree Basement Upper Block Pushed"


def set_region_rules(world: "SohWorld") -> None:
    # Deku Tree Entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_ENTRYWAY, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: True)
    ])

    # Deku Lobby
    # Events
    add_events(Regions.DEKU_TREE_LOBBY, world, [
        (EventLocations.DEKU_TREE_LOBBY_BABA_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_LOBBY_BABA_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_LOBBY, world, [
        (Locations.DEKU_TREE_MAP_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_LOBBY_LOWER_HEART, lambda bundle: True),
        (Locations.DEKU_TREE_LOBBY_UPPER_HEART,
         lambda bundle: can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        (Locations.DEKU_TREE_LOBBY_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LOBBY_GRASS5, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_LOBBY, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda bundle: True),
        (Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_COMPASS_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: can_attack(
            bundle) or can_use(Items.NUTS, bundle))
    ])

    # Deku F2 middle room
    # Connections
    connect_regions(Regions.DEKU_TREE_2F_MIDDLE_ROOM, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: can_reflect_nuts(
            bundle) or can_use(Items.MEGATON_HAMMER, bundle)),
        (Regions.DEKU_TREE_SLINGSHOT_ROOM, lambda bundle: can_reflect_nuts(
            bundle) or can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Deku slingshot room
    # Locations
    add_locations(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        (Locations.DEKU_TREE_SLINGSHOT_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS1, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS2, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS3, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle)),
        (Locations.DEKU_TREE_SLINGSHOT_GRASS4, lambda bundle: can_cut_shrubs(
            bundle) and can_reflect_nuts(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        (Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda bundle: can_use(
            Items.FAIRY_SLINGSHOT, bundle) or can_use(Items.HOVER_BOOTS, bundle))
    ])

    # Deku compass room
    # Events
    add_events(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (EventLocations.DEKU_TREE_COMPASS_BABA_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_COMPASS_BABA_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (Locations.DEKU_TREE_COMPASS_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_GS_COMPASS_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOLD_SKULLTULA)),
        (Locations.DEKU_TREE_COMPASS_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_COMPASS_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: has_fire_source_with_torch(bundle))
    ])

    # Deku Basement Lower
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (Locations.DEKU_TREE_BASEMENT_CHEST, lambda bundle: True),
        (Locations.DEKU_TREE_GS_BASEMENT_GATE, lambda bundle: can_kill_enemy(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)),
        (Locations.DEKU_TREE_GS_BASEMENT_VINES, lambda bundle: can_kill_enemy(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)),
        (Locations.DEKU_TREE_BASEMENT_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_BASEMENT_GRASS2,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        (Regions.DEKU_TREE_LOBBY, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: is_adult(bundle) or can_do_trick(Tricks.DEKU_B1_SKIP, bundle)
            or has_item(LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, bundle) or can_ground_jump(bundle))
    ])

    # Deku basement shrub room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_EYE_SWITCH_GRASS4,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT,
         lambda bundle: can_hit_eye_targets(bundle))
    ])

    # Deku basement water room front
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, world, [
        (Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_do_trick(Tricks.DEKU_B1_BACKFLIP_OVER_SPIKED_LOG, bundle)),
    ])

    # Deku basement water room back
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        (Locations.DEKU_TREE_SPIKE_ROLLER_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_SPIKE_ROLLER_GRASS2,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_do_trick(Tricks.DEKU_B1_BACKFLIP_OVER_SPIKED_LOG, bundle)),
        (Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda bundle: True)
    ])

    # Deku tree basement torch room
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (Locations.DEKU_TREE_TORCHES_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_TORCHES_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle))
    ])

    # Deku basement back lobby
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (Locations.DEKU_TREE_LARVAE_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_LARVAE_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        (Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_BACK_ROOM, lambda bundle: (
            has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))),
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: (
            has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))),
    ])

    # Deku basement back room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        (Locations.DEKU_TREE_GS_BASEMENT_BACK_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle)),

    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: True),
    ])

    # Deku basement upper
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
        (EventLocations.DEKU_TREE_BASEMENT_UPPER_BLOCK,
         LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        (Regions.DEKU_TREE_BASEMENT_LOWER, lambda bundle: True),
        (Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda bundle: is_child(bundle)),
        (Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda bundle: has_fire_source_with_torch(bundle) or
         (can_do_trick(Tricks.DEKU_B1_BOW_WEBS, bundle) and is_adult(bundle) and can_use(Items.FAIRY_BOW, bundle)))
    ])

    # Deku outside boss room
    # Locations
    add_locations(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        (Locations.DEKU_TREE_FINAL_ROOM_LEFT_FRONT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_FINAL_ROOM_LEFT_BACK_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_FINAL_ROOM_RIGHT_HEART, lambda bundle: has_item(Items.BRONZE_SCALE,
         bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS1, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS2, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle)),
        (Locations.DEKU_TREE_BEFORE_BOSS_GRASS3, lambda bundle: can_cut_shrubs(
            bundle) and has_fire_source_with_torch(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_BASEMENT_UPPER, lambda bundle: True),
        (Regions.DEKU_TREE_BOSS_ENTRYWAY, lambda bundle: (has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))
            and can_reflect_nuts(bundle))
    ])

    # Skipping master quest for now

    # Deku Boss room entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ENTRYWAY, world, [
        (Regions.DEKU_TREE_BOSS_ROOM, lambda bundle: True)
    ])

    # Deku boss exit
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_EXIT, world, [
        (Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda bundle: True),
        # skipping mq connection
    ])

    # Deku Tree boss room
    # Events
    add_events(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (EventLocations.DEKU_TREE_QUEEN_GOHMA, Events.DEKU_TREE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOHMA))
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Locations.QUEEN_GOHMA, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER,
         lambda bundle: has_item(Events.DEKU_TREE_COMPLETED, bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8,
         lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ROOM, world, [
        (Regions.DEKU_TREE_BOSS_EXIT, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: has_item(
            Events.DEKU_TREE_COMPLETED, bundle))
    ])
