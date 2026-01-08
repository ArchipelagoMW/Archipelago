from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    SPIRIT_TEMPLE_BEGINNING_NUT_CRATE = "Spirit Temple Nut Crate"
    SPIRIT_TEMPLE_TWINROVA = "Spirit Temple Twinrova"


def set_region_rules(world: "SohWorld") -> None:
    # Spirit Temple Entryway
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_ENTRYWAY, world, [
        (Regions.SPIRIT_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.DESERT_COLOSSUS_OUTSIDE_TEMPLE, lambda bundle: True)
    ])

    # Spirit Temple Lobby
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_LOBBY, world, [
        (Locations.SPIRIT_TEMPLE_LOBBY_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.SPIRIT_TEMPLE_LOBBY_POT2, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_LOBBY, world, [
        (Regions.SPIRIT_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.SPIRIT_TEMPLE_CHILD, lambda bundle: is_child(bundle)),
        (Regions.SPIRIT_TEMPLE_EARLY_ADULT,
         lambda bundle: can_use(Items.SILVER_GAUNTLETS, bundle))
    ])

    # Spirit Temple Child
    # Events
    add_events(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (EventLocations.SPIRIT_TEMPLE_BEGINNING_NUT_CRATE,
         Events.CAN_FARM_NUTS, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (Locations.SPIRIT_TEMPLE_CHILD_BRIDGE_CHEST, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(
            Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_CHILD_EARLY_TORCHES_CHEST, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle)))) and (can_use_any([Items.STICKS, Items.DINS_FIRE], bundle))),
        (Locations.SPIRIT_TEMPLE_GS_METAL_FENCE, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT1, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT2, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT3, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT4, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (
            has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_BEFORE_CHILD_CLIMB_SMALL_CRATE1,
         lambda bundle: can_break_small_crates(bundle)),
        (Locations.SPIRIT_TEMPLE_BEFORE_CHILD_CLIMB_SMALL_CRATE2,
         lambda bundle: can_break_small_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (Regions.SPIRIT_TEMPLE_CHILD_CLIMB, lambda bundle: small_keys(
            Items.SPIRIT_TEMPLE_SMALL_KEY, 1, bundle))
    ])

    # Spirit Temple Child Climb
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CHILD_CLIMB, world, [
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_NORTH_CHEST, lambda bundle: has_projectile(bundle) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle) and can_use(
            Items.SILVER_GAUNTLETS, bundle) and has_projectile(bundle, Ages.ADULT)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and is_child(bundle) and has_projectile(bundle, Ages.CHILD))),
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_EAST_CHEST, lambda bundle: has_projectile(bundle) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle) and can_use(
            Items.SILVER_GAUNTLETS, bundle) and has_projectile(bundle, Ages.ADULT)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and is_child(bundle) and has_projectile(bundle, Ages.CHILD))),
        (Locations.SPIRIT_TEMPLE_GS_SUN_ON_FLOOR_ROOM, lambda bundle: has_projectile(bundle) or can_use(Items.DINS_FIRE, bundle) or (take_damage(bundle) and (can_jump_slash_except_hammer(bundle) or has_projectile(bundle, Ages.CHILD))) or (is_child(bundle) and small_keys(
            Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_projectile(bundle, Ages.CHILD)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and (has_projectile(bundle, Ages.ADULT) or (take_damage(bundle) and can_jump_slash_except_hammer(bundle))))),
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_POT1,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CHILD_CLIMB, world, [
        (Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, lambda bundle: has_explosives(bundle) or (
            bool(world.options.sunlight_arrows) and can_use(Items.LIGHT_ARROW, bundle)))
    ])

    # Spirit Temple Early Adult
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_EARLY_ADULT, world, [
        (Locations.SPIRIT_TEMPLE_COMPASS_CHEST, lambda bundle: can_use(
            Items.HOOKSHOT, bundle) and can_use(Items.ZELDAS_LULLABY, bundle)),
        (Locations.SPIRIT_TEMPLE_EARLY_ADULT_RIGHT_CHEST, lambda bundle: (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.BOMBCHUS_5], bundle) or (can_use(
            Items.BOMB_BAG, bundle) and is_adult(bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle))) and (can_use(Items.HOVER_BOOTS, bundle) or can_jump_slash_except_hammer(bundle))),
        (Locations.SPIRIT_TEMPLE_FIRST_MIRROR_LEFT_CHEST,
         lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle)),
        (Locations.SPIRIT_TEMPLE_FIRST_MIRROR_RIGHT_CHEST,
         lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle)),
        (Locations.SPIRIT_TEMPLE_GS_BOULDER_ROOM, lambda bundle: can_use(Items.SONG_OF_TIME, bundle) and (can_use_any(
            [Items.FAIRY_BOW, Items.HOOKSHOT, Items.BOMBCHUS_5], bundle) or (can_use(Items.BOMB_BAG, bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle)))),
        (Locations.SPIRIT_TEMPLE_AFTER_BOULDER_ROOM_SUNS_SONG_FAIRY, lambda bundle: can_use(Items.SUNS_SONG, bundle) and (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.BOMBCHUS_5], bundle) or (
            can_use(Items.BOMB_BAG, bundle) and is_adult(bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle))) and (can_use(Items.HOVER_BOOTS, bundle) or can_jump_slash(bundle)))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_EARLY_ADULT, world, [
        (Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, lambda bundle: small_keys(
            Items.SPIRIT_TEMPLE_SMALL_KEY, 1, bundle))
    ])

    # Spirit Temple Central Chamber
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, world, [
        (Locations.SPIRIT_TEMPLE_MAP_CHEST, lambda bundle: ((has_explosives(bundle) or small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)) and (can_use(Items.DINS_FIRE, bundle) or ((can_use(Items.FIRE_ARROW, bundle) or can_do_trick(Tricks.SPIRIT_MAP_CHEST, bundle)) and can_use(Items.FAIRY_BOW, bundle) and can_use(Items.STICKS, bundle)))) or (
            small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_explosives(bundle) and can_use(Items.STICKS, bundle)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle) and (can_use(Items.FIRE_ARROW, bundle) or (can_do_trick(Tricks.SPIRIT_MAP_CHEST, bundle) and can_use(Items.FAIRY_BOW, bundle))) and can_use(Items.SILVER_GAUNTLETS, bundle))),
        (Locations.SPIRIT_TEMPLE_SUN_BLOCK_ROOM_CHEST, lambda bundle: ((has_explosives(bundle) or small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)) and (can_use(Items.DINS_FIRE, bundle) or ((can_use(Items.FIRE_ARROW, bundle) or can_do_trick(Tricks.SPIRIT_SUN_CHEST, bundle)) and can_use(Items.FAIRY_BOW, bundle) and can_use(Items.STICKS, bundle)))) or (
            small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_explosives(bundle) and can_use(Items.STICKS, bundle)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle) and (can_use(Items.FIRE_ARROW, bundle) or (can_do_trick(Tricks.SPIRIT_SUN_CHEST, bundle) and can_use(Items.FAIRY_BOW, bundle))) and can_use(Items.SILVER_GAUNTLETS, bundle))),
        (Locations.SPIRIT_TEMPLE_STATUE_ROOM_HAND_CHEST, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY,
         3, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and can_use(Items.ZELDAS_LULLABY, bundle)),
        (Locations.SPIRIT_TEMPLE_STATUE_ROOM_NORTHEAST_CHEST, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle)
         and can_use(Items.ZELDAS_LULLABY, bundle) and (can_use_any([Items.HOOKSHOT, Items.HOVER_BOOTS], bundle) or can_do_trick(Tricks.SPIRIT_LOBBY_JUMP, bundle))),
        (Locations.SPIRIT_TEMPLE_GS_HALL_AFTER_SUN_BLOCK_ROOM, lambda bundle: (has_explosives(bundle) and can_use(Items.BOOMERANG, bundle) and can_use(Items.HOOKSHOT, bundle)) or (can_use(Items.BOOMERANG, bundle) and small_keys(
            Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_explosives(bundle)) or (can_use(Items.HOOKSHOT, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle))),
        (Locations.SPIRIT_TEMPLE_GS_LOBBY, lambda bundle: ((has_explosives(bundle) or small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)) and can_do_trick(Tricks.SPIRIT_LOBBY_GS, bundle) and can_use(Items.BOOMERANG, bundle) and (can_use(Items.HOOKSHOT, bundle) or can_use(Items.HOVER_BOOTS, bundle) or can_do_trick(Tricks.SPIRIT_LOBBY_JUMP, bundle))) or (can_do_trick(
            Tricks.SPIRIT_LOBBY_GS, bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_explosives(bundle) and can_use(Items.BOOMERANG, bundle)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and (can_use_any([Items.HOOKSHOT, Items.HOVER_BOOTS], bundle) or can_do_trick(Tricks.SPIRIT_LOBBY_JUMP, bundle)))),
        (Locations.SPIRIT_TEMPLE_AFTER_SUN_BLOCK_POT1, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_AFTER_SUN_BLOCK_POT2, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT1, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT2, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT3, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT4, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT5, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT6, lambda bundle: can_break_pots(
            bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, world, [
        (Regions.SPIRIT_TEMPLE_OUTDOOR_HANDS, lambda bundle: can_jump_slash_except_hammer(
            bundle) or has_explosives(bundle)),
        (Regions.SPIRIT_TEMPLE_BEYOND_CENTRAL_LOCKED_DOOR, lambda bundle: small_keys(
            Items.SPIRIT_TEMPLE_SMALL_KEY, 4, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle)),
        (Regions.SPIRIT_TEMPLE_CHILD_CLIMB, lambda bundle: True),
        (Regions.SPIRIT_TEMPLE_INSIDE_STATUE_HEAD, lambda bundle: can_do_trick(
            Tricks.SPIRIT_PLATFORM_HOOKSHOT, bundle) and can_use(Items.HOOKSHOT, bundle))
    ])

    # Spirit Temple Outdoor Hands
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_OUTDOOR_HANDS, world, [
        (Locations.SPIRIT_TEMPLE_SILVER_GAUNTLETS_CHEST, lambda bundle: (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle)
         and can_use(Items.LONGSHOT, bundle) and has_explosives(bundle)) or small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle)),
        (Locations.SPIRIT_TEMPLE_MIRROR_SHIELD_CHEST, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY,
         4, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and has_explosives(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_OUTDOOR_HANDS, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: (is_child(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle)) or (can_use(Items.SILVER_GAUNTLETS,
         bundle) and ((small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3, bundle) and has_explosives(bundle)) or small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle))))
    ])

    # Spirit Temple Beyond Central Locked Door
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_BEYOND_CENTRAL_LOCKED_DOOR, world, [
        (Locations.SPIRIT_TEMPLE_NEAR_FOUR_ARMOS_CHEST, lambda bundle: (can_use(Items.MIRROR_SHIELD, bundle) or (
            bool(world.options.sunlight_arrows) and can_use(Items.LIGHT_ARROW, bundle))) and has_explosives(bundle)),
        (Locations.SPIRIT_TEMPLE_HALLWAY_LEFT_INVISIBLE_CHEST, lambda bundle: (can_do_trick(
            Tricks.LENS_SPIRIT, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)) and has_explosives(bundle)),
        (Locations.SPIRIT_TEMPLE_HALLWAY_RIGHT_INVISIBLE_CHEST, lambda bundle: (can_do_trick(
            Tricks.LENS_SPIRIT, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)) and has_explosives(bundle)),
        (Locations.SPIRIT_TEMPLE_BEAMOS_HALL_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.SPIRIT_TEMPLE_FOUR_ARMOS_ROOM_SUNS_SONG_FAIRY,
         lambda bundle: has_explosives(bundle) and can_use(Items.SUNS_SONG, bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_BEYOND_CENTRAL_LOCKED_DOOR, world, [
        (Regions.SPIRIT_TEMPLE_BEYOND_FINAL_LOCKED_DOOR, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and (can_do_trick(Tricks.SPIRIT_WALL, bundle) or can_use_any(
            [Items.LONGSHOT, Items.BOMBCHUS_5], bundle) or ((can_use_any([Items.BOMB_BAG, Items.NUTS, Items.DINS_FIRE], bundle)) and (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.MEGATON_HAMMER], bundle)))))
    ])

    # Spirit Temple Beyond Final Locked Door
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_BEYOND_FINAL_LOCKED_DOOR, world, [
        (Locations.SPIRIT_TEMPLE_BOSS_KEY_CHEST, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle) and ((take_damage(bundle)
         and can_do_trick(Tricks.FLAMING_CHESTS, bundle)) or (can_use(Items.FAIRY_BOW, bundle) and can_use(Items.HOOKSHOT, bundle)))),
        (Locations.SPIRIT_TEMPLE_TOPMOST_CHEST, lambda bundle: (can_use(Items.MIRROR_SHIELD, bundle) and (can_jump_slash(bundle) or has_explosives(bundle) or (can_do_trick(Tricks.HOOKSHOT_EXTENSION,
         bundle) and (can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.HOOKSHOT], bundle))))) or (bool(world.options.sunlight_arrows) and can_use(Items.LIGHT_ARROW, bundle))),
        (Locations.SPIRIT_TEMPLE_ADULT_CLIMB_LEFT_HEART,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Locations.SPIRIT_TEMPLE_ADULT_CLIMB_RIGHT_HEART,
         lambda bundle: can_use(Items.HOOKSHOT, bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_BEYOND_FINAL_LOCKED_DOOR, world, [
        (Regions.SPIRIT_TEMPLE_INSIDE_STATUE_HEAD, lambda bundle: can_use(
            Items.MIRROR_SHIELD, bundle) and has_explosives(bundle) and can_use(Items.HOOKSHOT, bundle))
    ])

    # Spirit Temple Inside Statue Head
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_INSIDE_STATUE_HEAD, world, [
        (Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, lambda bundle: True),
        (Regions.SPIRIT_TEMPLE_BOSS_ENTRYWAY, lambda bundle: True)
    ])

    # Spirit Temple Boss Entryway
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_BOSS_ENTRYWAY, world, [
        (Regions.SPIRIT_TEMPLE_INSIDE_STATUE_HEAD, lambda bundle: False),
        (Regions.SPIRIT_TEMPLE_BOSS_ROOM, lambda bundle: has_item(
            Items.SPIRIT_TEMPLE_BOSS_KEY, bundle))
    ])

    # Spirit Temple Boss Room
    # Events
    add_events(Regions.SPIRIT_TEMPLE_BOSS_ROOM, world, [
        (EventLocations.SPIRIT_TEMPLE_TWINROVA, Events.SPIRIT_TEMPLE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.TWINROVA))
    ])
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_BOSS_ROOM, world, [
        (Locations.SPIRIT_TEMPLE_TWINROVA_HEART_CONTAINER,
         lambda bundle: has_item(Events.SPIRIT_TEMPLE_COMPLETED, bundle)),
        (Locations.TWINROVA, lambda bundle: has_item(
            Events.SPIRIT_TEMPLE_COMPLETED, bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_BOSS_ROOM, world, [
        (Regions.SPIRIT_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.DESERT_COLOSSUS, lambda bundle: has_item(
            Events.SPIRIT_TEMPLE_COMPLETED, bundle))
    ])
