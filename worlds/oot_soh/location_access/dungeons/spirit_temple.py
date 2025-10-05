from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld

class EventLocations(str, Enum):
    SPIRIT_TEMPLE_BEGINNING_NUT_CRATE = "Spirit Temple Nut Crate"
    SPIRIT_TEMPLE_BOSS_TWINROVA = "Spirit Temple Boss Twinrova"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    ## Spirit Temple Entryway
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_ENTRYWAY, world, [
        (Regions.SPIRIT_TEMPLE_LOBBY, lambda bundle: True), 
        (Regions.DESERT_COLOSSUS_FROM_SPIRIT_ENTRYWAY, lambda bundle: True)
    ])

    ## Spirit Temple Lobby
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_LOBBY, world, [
        (Locations.SPIRIT_TEMPLE_LOBBY_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.SPIRIT_TEMPLE_LOBBY_POT2, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_LOBBY, world, [
        (Regions.SPIRIT_TEMPLE_ENTRYWAY, lambda bundle: True), 
        (Regions.SPIRIT_TEMPLE_CHILD, lambda bundle: is_child(bundle)),
        (Regions.SPIRIT_TEMPLE_EARLY_ADULT, lambda bundle: can_use(Items.SILVER_GAUNTLETS, bundle)) 
    ])

    ## Spirit Temple Child
    # Events
    add_events(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (EventLocations.SPIRIT_TEMPLE_BEGINNING_NUT_CRATE, Events.CAN_FARM_NUTS, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (Locations.SPIRIT_TEMPLE_CHILD_BRIDGE_CHEST, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_CHILD_EARLY_TORCHES_CHEST, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle)))) and (can_use_any([Items.STICKS, Items.DINS_FIRE], bundle))),
        (Locations.SPIRIT_TEMPLE_GS_METAL_FENCE, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT1, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT2, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT3, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_ANUBIS_POT4, lambda bundle: (can_use_any([Items.BOOMERANG, Items.FAIRY_SLINGSHOT], bundle) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.SPIRIT_CHILD_CHU, bundle))) and (has_explosives(bundle) or ((can_use_any([Items.NUTS, Items.BOOMERANG], bundle)) and (can_use_any([Items.STICKS, Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle))))),
        (Locations.SPIRIT_TEMPLE_BEFORE_CHILD_CLIMB_SMALL_CRATE1, lambda bundle: can_break_small_crates(bundle)),
        (Locations.SPIRIT_TEMPLE_BEFORE_CHILD_CLIMB_SMALL_CRATE2, lambda bundle: can_break_small_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CHILD, world, [
        (Regions.SPIRIT_TEMPLE_CHILD_CLIMB, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 1, bundle))
    ])

    ## Spirit Temple Child Climb
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CHILD_CLIMB, world, [
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_NORTH_CHEST, lambda bundle: has_projectile(bundle, Ages.BOTH) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and has_projectile(bundle, Ages.ADULT)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and is_child(bundle) and has_projectile(bundle, Ages.CHILD))),
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_EAST_CHEST, lambda bundle: has_projectile(bundle, Ages.BOTH) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and has_projectile(bundle, Ages.ADULT)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and is_child(bundle) and has_projectile(bundle, Ages.CHILD))),
        (Locations.SPIRIT_TEMPLE_GS_SUN_ON_FLOOR_ROOM, lambda bundle: has_projectile(bundle, Ages.BOTH) or can_use(Items.DINS_FIRE, bundle) or (take_damage(bundle) and (can_jump_slash_except_hammer(bundle) or has_projectile(bundle, Ages.CHILD))) or (is_child(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 5, bundle) and has_projectile(bundle, Ages.CHILD)) or (small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle) and (has_projectile(bundle, Ages.ADULT) or (take_damage(bundle) and can_jump_slash_except_hammer(bundle))))),
        (Locations.SPIRIT_TEMPLE_CHILD_CLIMB_POT1, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CHILD_CLIMB, world, [
        (Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, lambda bundle: has_explosives(bundle) or (world.options.sunlight_arrows.value and can_use(Items.LIGHT_ARROW, bundle)))
    ])

    ## Spirit Temple Early Adult
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_EARLY_ADULT, world, [
        (Locations.SPIRIT_TEMPLE_COMPASS_CHEST, lambda bundle: can_use(Items.HOOKSHOT, bundle) and can_use(Items.ZELDAS_LULLABY, bundle)),
        (Locations.SPIRIT_TEMPLE_EARLY_ADULT_RIGHT_CHEST, lambda bundle: (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.BOMBCHUS_5], bundle) or (can_use(Items.BOMB_BAG, bundle) and is_adult(bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle))) and (can_use(Items.HOVER_BOOTS, bundle) or can_jump_slash_except_hammer(bundle))),
        (Locations.SPIRIT_TEMPLE_FIRST_MIRROR_LEFT_CHEST, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3)),
        (Locations.SPIRIT_TEMPLE_FIRST_MIRROR_RIGHT_CHEST, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 3)),
        (Locations.SPIRIT_TEMPLE_GS_BOULDER_ROOM, lambda bundle: can_use(Items.SONG_OF_TIME, bundle) and (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.BOMBCHUS_5], bundle) or (can_use(Items.BOMB_BAG, bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle)))),
        (Locations.SPIRIT_TEMPLE_AFTER_BOULDER_ROOM_SUNS_SONG_FAIRY, lambda bundle: can_use(Items.SUNS_SONG, bundle) and (can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.BOMBCHUS_5], bundle) or (can_use(Items.BOMB_BAG, bundle) and is_adult(bundle) and can_do_trick(Tricks.SPIRIT_LOWER_ADULT_SWITCH, bundle))) and (can_use(Items.HOVER_BOOTS, bundle) or can_jump_slash(bundle)))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_EARLY_ADULT, world, [
        (Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 1, bundle))
    ])

    ## Spirit Temple Central Chamber
    # Locations
    add_locations(Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, world, [
        (Locations.SPIRIT_TEMPLE_MAP_CHEST, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_SUN_BLOCK_ROOM_CHEST, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_STATUE_ROOM_HAND_CHEST, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_STATUE_ROOM_NORTHEAST_CHEST, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_GS_HALL_AFTER_SUN_BLOCK_ROOM, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_GS_LOBBY, lambda bundle: True),
        (Locations.SPIRIT_TEMPLE_AFTER_SUN_BLOCK_POT1, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_AFTER_SUN_BLOCK_POT2, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT1, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT2, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT3, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT4, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT5, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle)),
        (Locations.SPIRIT_TEMPLE_CENTRAL_CHAMBER_POT6, lambda bundle: can_break_pots(bundle) and small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 2, bundle))
    ])
    # Connections
    connect_regions(Regions.SPIRIT_TEMPLE_CENTRAL_CHAMBER, world, [
        (Regions.SPIRIT_TEMPLE_OUTDOOR_HANDS, lambda bundle: can_jump_slash_except_hammer(bundle) or has_explosives(bundle)),
        (Regions.SPIRIT_TEMPLE_BEYOND_CENTRAL_LOCKED_DOOR, lambda bundle: small_keys(Items.SPIRIT_TEMPLE_SMALL_KEY, 4, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle)),
        (Regions.SPIRIT_TEMPLE_CHILD_CLIMB, lambda bundle: True),
        (Regions.SPIRIT_TEMPLE_INSIDE_STATUE_HEAD, lambda bundle: can_do_trick(Tricks.SPIRIT_PLATFORM_HOOKSHOT, bundle) and can_use(Items.HOOKSHOT, bundle))
    ])