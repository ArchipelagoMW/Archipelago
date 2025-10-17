from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    SHADOW_TEMPLE_BEGINNING_NUT_POT = "Shadow Temple Beginning Nut Pot"
    SHADOW_TEMPLE_FAIRY_POT = "Shadow Temple Fairy Pot"
    SHADOW_TEMPLE_BONGO_BONGO = "Shadow Temple Bongo Bongo"


def set_region_rules(world: "SohWorld") -> None:
    # Shadow Temple Entryway
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_ENTRYWAY, world, [
        (Regions.SHADOW_TEMPLE_BEGINNING, lambda bundle: (can_do_trick(Tricks.LENS_SHADOW, bundle) or can_use(
            Items.LENS_OF_TRUTH, bundle)) and (can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle))),
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda bundle: True)
    ])

    # Shadow Temple Beginning
    # Events
    add_events(Regions.SHADOW_TEMPLE_BEGINNING, world, [
        (EventLocations.SHADOW_TEMPLE_BEGINNING_NUT_POT,
         Events.CAN_FARM_NUTS, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_BEGINNING, world, [
        (Locations.SHADOW_TEMPLE_MAP_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.SHADOW_TEMPLE_HOVER_BOOTS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.DEAD_HAND)),
        (Locations.SHADOW_TEMPLE_NEAR_DEAD_HAND_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_WHISPERING_WALLS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_WHISPERING_WALLS_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_WHISPERING_WALLS_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_WHISPERING_WALLS_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_WHISPERING_WALLS_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_MAP_CHEST_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_MAP_CHEST_POT2,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_BEGINNING, world, [
        (Regions.SHADOW_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.SHADOW_TEMPLE_FIRST_BEAMOS,
         lambda bundle: can_use(Items.HOVER_BOOTS, bundle)),
    ])

    # Shadow Temple First Beamos
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_FIRST_BEAMOS, world, [
        (Locations.SHADOW_TEMPLE_COMPASS_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.SHADOW_TEMPLE_EARLY_SILVER_RUPEE_CHEST, lambda bundle: can_use(
            Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle)),
        (Locations.SHADOW_TEMPLE_BEAMOS_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_FIRST_BEAMOS, world, [
        (Regions.SHADOW_TEMPLE_HUGE_PIT, lambda bundle: has_explosives(bundle) and is_adult(
            bundle) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 1, bundle)),
        (Regions.SHADOW_TEMPLE_BEYOND_BOAT, lambda bundle: False),
    ])

    # Shadow Temple Huge Pit
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_HUGE_PIT, world, [
        (Locations.SHADOW_TEMPLE_INVISIBLE_BLADES_VISIBLE_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.SHADOW_TEMPLE_INVISIBLE_BLADES_INVISIBLE_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_LOWER_CHEST, lambda bundle: True),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_UPPER_CHEST, lambda bundle: (can_do_trick(Tricks.SHADOW_UMBRELLA_HOVER, bundle) and can_use(
            Items.HOVER_BOOTS, bundle)) or can_do_trick(Tricks.SHADOW_UMBRELLA_CLIP, bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_SWITCH_CHEST, lambda bundle: (can_do_trick(Tricks.SHADOW_UMBRELLA_HOVER, bundle) and can_use(
            Items.HOVER_BOOTS, bundle)) or can_do_trick(Tricks.SHADOW_UMBRELLA_CLIP, bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.SHADOW_TEMPLE_INVISIBLE_SPIKES_CHEST, lambda bundle: small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 2, bundle) and (
            (can_do_trick(Tricks.LENS_SHADOW_PLATFORM, bundle) and can_do_trick(Tricks.LENS_SHADOW, bundle)) or can_use(Items.LENS_OF_TRUTH, bundle))),
        (Locations.SHADOW_TEMPLE_FREESTANDING_KEY, lambda bundle: small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 2, bundle) and ((can_do_trick(Tricks.LENS_SHADOW_PLATFORM, bundle) and can_do_trick(Tricks.LENS_SHADOW, bundle)) or can_use(
            Items.LENS_OF_TRUTH, bundle)) and can_use(Items.HOOKSHOT, bundle) and (can_use(Items.BOMB_BAG, bundle) or has_item(Items.GORONS_BRACELET, bundle) or (can_do_trick(Tricks.SHADOW_FREESTANDING_KEY, bundle) and can_use(Items.BOMBCHUS_5, bundle)))),
        (Locations.SHADOW_TEMPLE_GS_LIKE_LIKE_ROOM,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.SHADOW_TEMPLE_GS_FALLING_SPIKES_ROOM, lambda bundle: can_use(Items.HOOKSHOT, bundle) or (can_do_trick(Tricks.SHADOW_UMBRELLA_GS, bundle) and can_use(
            Items.HOVER_BOOTS, bundle) and can_standing_shield(bundle) and can_use(Items.MASTER_SWORD, bundle)) or (is_adult(bundle) and can_ground_jump(bundle))),
        (Locations.SHADOW_TEMPLE_GS_SINGLE_GIANT_POT, lambda bundle: small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 2, bundle) and ((can_do_trick(
            Tricks.LENS_SHADOW_PLATFORM, bundle) and can_do_trick(Tricks.LENS_SHADOW, bundle)) or can_use(Items.LENS_OF_TRUTH, bundle) and can_use(Items.HOOKSHOT, bundle))),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_POT3, lambda bundle: can_break_pots(bundle) and (can_do_trick(Tricks.SHADOW_UMBRELLA_HOVER, bundle)
         and can_use(Items.HOVER_BOOTS, bundle)) or can_do_trick(Tricks.SHADOW_UMBRELLA_CLIP, bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.SHADOW_TEMPLE_FALLING_SPIKES_POT4, lambda bundle: can_break_pots(bundle) and (can_do_trick(Tricks.SHADOW_UMBRELLA_HOVER, bundle)
         and can_use(Items.HOVER_BOOTS, bundle)) or can_do_trick(Tricks.SHADOW_UMBRELLA_CLIP, bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.SHADOW_TEMPLE_INVISIBLE_BLADES_LEFT_HEART, lambda bundle: (can_use(
            Items.SONG_OF_TIME, bundle) and is_adult(bundle)) or can_use(Items.BOOMERANG, bundle)),
        (Locations.SHADOW_TEMPLE_INVISIBLE_BLADES_RIGHT_HEART, lambda bundle: (can_use(
            Items.SONG_OF_TIME, bundle) and is_adult(bundle)) or can_use(Items.BOOMERANG, bundle)),
        (Locations.SHADOW_TEMPLE_PIT_ROOM_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_HUGE_PIT, world, [
        (Regions.SHADOW_TEMPLE_WIND_TUNNEL, lambda bundle: ((can_do_trick(Tricks.LENS_SHADOW_PLATFORM, bundle) and can_do_trick(Tricks.LENS_SHADOW, bundle)) or can_use(Items.LENS_OF_TRUTH, bundle)) and (
            can_use(Items.HOOKSHOT, bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 3, bundle)),
    ])

    # Shadow Temple Wind Tunnel
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_WIND_TUNNEL, world, [
        (Locations.SHADOW_TEMPLE_WIND_HINT_CHEST, lambda bundle: True),
        (Locations.SHADOW_TEMPLE_AFTER_WIND_ENEMY_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.GIBDO, EnemyDistance.CLOSE, True, 2)),
        (Locations.SHADOW_TEMPLE_AFTER_WIND_HIDDEN_CHEST,
         lambda bundle: has_explosives(bundle)),
        (Locations.SHADOW_TEMPLE_GS_NEAR_SHIP, lambda bundle: can_use(
            Items.LONGSHOT, bundle) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 4, bundle)),
        (Locations.SHADOW_TEMPLE_WIND_HINT_SUNS_SONG_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_WIND_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_WIND_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_SCARECROW_NEAR_SHIP_NORTH_HEART, lambda bundle: can_use(
            Items.DISTANT_SCARECROW, bundle) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 4, bundle)),
        (Locations.SHADOW_TEMPLE_SCARECROW_NEAR_SHIP_SOUTH_HEART, lambda bundle: can_use(
            Items.DISTANT_SCARECROW, bundle) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 4, bundle))

    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_WIND_TUNNEL, world, [
        (Regions.SHADOW_TEMPLE_BEYOND_BOAT, lambda bundle: can_jump_slash_except_hammer(bundle) and can_use(
            Items.ZELDAS_LULLABY, bundle) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 4, bundle)),
    ])

    # Shadow Temple Beyond Boat
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_BEYOND_BOAT, world, [
        (Locations.SHADOW_TEMPLE_SPIKE_WALLS_LEFT_CHEST,
         lambda bundle: can_use(Items.DINS_FIRE, bundle)),
        (Locations.SHADOW_TEMPLE_BOSS_KEY_CHEST,
         lambda bundle: can_use(Items.DINS_FIRE, bundle)),
        (Locations.SHADOW_TEMPLE_INVISIBLE_FLOORMASTER_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.FLOORMASTER)),
        (Locations.SHADOW_TEMPLE_GS_TRIPLE_GIANT_POT,
         lambda bundle: is_adult(bundle) and can_attack(bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_BOAT_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_BOAT_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_BOAT_POT3, lambda bundle: can_break_pots(bundle) and (can_use(Items.FAIRY_BOW, bundle) or can_use(
            Items.DISTANT_SCARECROW, bundle) or (can_do_trick(Tricks.SHADOW_STATUE, bundle) and can_use(Items.BOMBCHUS_5, bundle)))),
        (Locations.SHADOW_TEMPLE_AFTER_BOAT_POT4, lambda bundle: can_break_pots(bundle) and (can_use(Items.FAIRY_BOW, bundle) or can_use(
            Items.DISTANT_SCARECROW, bundle) or (can_do_trick(Tricks.SHADOW_STATUE, bundle) and can_use(Items.BOMBCHUS_5, bundle)))),
        (Locations.SHADOW_TEMPLE_SPIKE_WALLS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_FLOORMASTER_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_FLOORMASTER_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_SHIP_UPPER_LEFT_HEART,
         lambda bundle: can_use(Items.DISTANT_SCARECROW, bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_SHIP_UPPER_RIGHT_HEART,
         lambda bundle: can_use(Items.DISTANT_SCARECROW, bundle)),
        (Locations.SHADOW_TEMPLE_AFTER_SHIP_LOWER_HEART, lambda bundle: (can_use(Items.FAIRY_BOW, bundle) or can_use(Items.DISTANT_SCARECROW, bundle) or (can_do_trick(Tricks.SHADOW_STATUE,
         bundle) and can_use(Items.BOMBCHUS_5, bundle))) and can_use(Items.SONG_OF_TIME, bundle) or (can_use(Items.DISTANT_SCARECROW, bundle) and can_use(Items.HOVER_BOOTS, bundle)))
    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_BEYOND_BOAT, world, [
        (Regions.SHADOW_TEMPLE_BOSS_ENTRYWAY, lambda bundle: (can_use(Items.FAIRY_BOW, bundle) or can_use(Items.DISTANT_SCARECROW, bundle) or (can_do_trick(
            Tricks.SHADOW_STATUE, bundle) and can_use(Items.BOMBCHUS_5, bundle))) and small_keys(Items.SHADOW_TEMPLE_SMALL_KEY, 5, bundle) and can_use(Items.HOVER_BOOTS, bundle)),
    ])

    # Shadow Temple Boss Entryway
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_BOSS_ENTRYWAY, world, [
        (Regions.SHADOW_TEMPLE_BEYOND_BOAT, lambda bundle: False),
        (Regions.SHADOW_TEMPLE_BOSS_ROOM, lambda bundle: has_item(
            Items.SHADOW_TEMPLE_BOSS_KEY, bundle))
    ])

    # Shadow Temple Boss Room
    # Events
    add_events(Regions.SHADOW_TEMPLE_BOSS_ROOM, world, [
        (EventLocations.SHADOW_TEMPLE_BONGO_BONGO, Events.SHADOW_TEMPLE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.BONGO_BONGO))
    ])
    # Locations
    add_locations(Regions.SHADOW_TEMPLE_BOSS_ROOM, world, [
        (Locations.SHADOW_TEMPLE_BONGO_BONGO_HEART_CONTAINER,
         lambda bundle: has_item(Events.SHADOW_TEMPLE_COMPLETED, bundle)),
        (Locations.BONGO_BONGO, lambda bundle: has_item(
            Events.SHADOW_TEMPLE_COMPLETED, bundle))
    ])
    # Connections
    connect_regions(Regions.SHADOW_TEMPLE_BOSS_ROOM, world, [
        (Regions.SHADOW_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda bundle: has_item(
            Events.SHADOW_TEMPLE_COMPLETED, bundle))
    ])
