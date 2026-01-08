from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    GRAVEYARD_BUTTERFLY_FAIRY = "Graveyard Butterfly Fairy"
    GRAVEYARD_BEAN_PLANT_FAIRY = "Graveyard Bean Plant Fairy"
    GRAVEYARD_BUG_ROCK = "Graveyard Bug Rock"
    GRAVEYARD_SOLD_SPOOKY_MASK = "Graveyard Sold Spooky Mask"
    GRAVEYARD_DAMPES_GRAVE_NUT_POT = "Graveyard Dampes Grave Nut Pot"
    GRAVEYARD_DAMPES_WINDMILL_ACCESS = "Graveyard Dampes Windmill Access"
    GRAVEYARD_GOSSIP_STONE_SONG_FAIRY = "Graveyard Gossip Stone Song Fairy"
    GRAVEYARD_BEAN_PATCH = "Graveyard Bean Patch"


class LocalEvents(StrEnum):
    ACCESS_TO_WINDMILL_FROM_DAMPES_GRAVE = "Access to Windmill From Dampes Grave"
    GRAVEYARD_BEAN_PLANTED = "Graveyard Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # The Graveyard
    # Events
    add_events(Regions.THE_GRAVEYARD, world, [
        (EventLocations.GRAVEYARD_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle) and at_day(bundle)),
        (EventLocations.GRAVEYARD_BEAN_PLANT_FAIRY, Events.CAN_ACCESS_FAIRIES, lambda bundle: is_child(
            bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (EventLocations.GRAVEYARD_BUG_ROCK,
         Events.CAN_ACCESS_BUGS, lambda bundle: True),
        (EventLocations.GRAVEYARD_SOLD_SPOOKY_MASK, Events.SOLD_SPOOKY_MASK, lambda bundle: is_child(bundle) and at_day(
            bundle) and has_item(Events.CAN_BORROW_SPOOKY_MASK, bundle) and has_item(Items.CHILD_WALLET, bundle)),
        (EventLocations.GRAVEYARD_BEAN_PATCH, LocalEvents.GRAVEYARD_BEAN_PLANTED,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle)),
    ])
    # Locations
    add_locations(Regions.THE_GRAVEYARD, world, [
        (Locations.GRAVEYARD_FREESTANDING_POH, lambda bundle: (((is_adult(bundle) and has_item(LocalEvents.GRAVEYARD_BEAN_PLANTED, bundle)) or can_use(
            Items.LONGSHOT, bundle)) and can_break_crates(bundle)) or (can_do_trick(Tricks.GY_POH, bundle) and can_use(Items.BOOMERANG, bundle))),
        (Locations.GRAVEYARD_DAMPE_GRAVEDIGGING_TOUR, lambda bundle: has_item(
            Items.CHILD_WALLET, bundle) and is_child(bundle) and at_night(bundle)),
        (Locations.GRAVEYARD_GS_WALL, lambda bundle: is_child(bundle) and hookshot_or_boomerang(
            bundle) and at_night(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.GRAVEYARD_GS_BEAN_PATCH,
         lambda bundle: can_spawn_soil_skull(bundle) and can_attack(bundle)),
        (Locations.GRAVEYARD_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GRAVEYARD_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GRAVEYARD_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GRAVEYARD_GRASS_1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_5, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_6, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_7, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_8, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_9, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_10, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_11, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_GRASS_12, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.GRAVEYARD_FREESTANDING_POH_CRATE, lambda bundle: (is_adult(bundle) and has_item(
            LocalEvents.GRAVEYARD_BEAN_PLANTED, bundle)) or can_use(Items.LONGSHOT, bundle) and can_break_crates(bundle))

    ])
    # Connections
    connect_regions(Regions.THE_GRAVEYARD, world, [
        (Regions.GRAVEYARD_SHIELD_GRAVE,
         lambda bundle: is_adult(bundle) or at_night(bundle)),
        (Regions.GRAVEYARD_COMPOSERS_GRAVE,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle)),
        (Regions.GRAVEYARD_HEART_PIECE_GRAVE,
         lambda bundle: is_adult(bundle) or at_night(bundle)),
        (Regions.GRAVEYARD_DAMPES_GRAVE, lambda bundle: is_adult(bundle)),
        (Regions.GRAVEYARD_DAMPES_HOUSE, lambda bundle: is_adult(bundle)
         and can_open_overworld_door(Items.DAMPES_HUT_KEY, bundle)),
        (Regions.KAKARIKO_VILLAGE, lambda bundle: True),
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda bundle: False)
    ])

    # The Graveyard Shield Grave
    # Locations
    add_locations(Regions.GRAVEYARD_SHIELD_GRAVE, world, [
        (Locations.GRAVEYARD_SHIELD_GRAVE_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_SHIELD_GRAVE, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True),
        (Regions.GRAVEYARD_SHIELD_GRAVE_BACK,
         lambda bundle: can_break_mud_walls(bundle))
    ])

    # The Graveyard Shield Grave Back
    # Locations
    add_locations(Regions.GRAVEYARD_SHIELD_GRAVE_BACK, world, [
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY1, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY2, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY3, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY4, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY5, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY6, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY7, lambda bundle: True),
        (Locations.GRAVEYARD_SHIELD_GRAVE_FAIRY8, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_SHIELD_GRAVE_BACK, world, [
        (Regions.GRAVEYARD_SHIELD_GRAVE, lambda bundle: True)
    ])

    # The Graveyard Heart Piece Grave
    # Locations
    add_locations(Regions.GRAVEYARD_HEART_PIECE_GRAVE, world, [
        (Locations.GRAVEYARD_HEART_PIECE_GRAVE_CHEST,
         lambda bundle: can_use(Items.SUNS_SONG, bundle))
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_HEART_PIECE_GRAVE, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True)
    ])

    # The Graveyard Composers Grave
    # Locations
    add_locations(Regions.GRAVEYARD_COMPOSERS_GRAVE, world, [
        (Locations.GRAVEYARD_ROYAL_FAMILYS_TOMB_CHEST,
         lambda bundle: has_fire_source(bundle)),
        (Locations.SONG_FROM_ROYAL_FAMILYS_TOMB,
         lambda bundle: can_use_projectile(bundle) or can_jump_slash(bundle)),
        (Locations.GRAVEYARD_ROYAL_FAMILYS_TOMB_SUNS_SONG_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle))
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_COMPOSERS_GRAVE, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True)
    ])

    # The Graveyard Dampes Grave
    # Events
    add_events(Regions.GRAVEYARD_DAMPES_GRAVE, world, [
        (EventLocations.GRAVEYARD_DAMPES_GRAVE_NUT_POT,
         Events.CAN_FARM_NUTS, lambda bundle: True),
        (EventLocations.GRAVEYARD_DAMPES_WINDMILL_ACCESS, Events.DAMPES_WINDMILL_ACCESS,
         lambda bundle: is_adult(bundle) and can_use(Items.SONG_OF_TIME, bundle))
    ])
    # Locations
    add_locations(Regions.GRAVEYARD_DAMPES_GRAVE, world, [
        (Locations.GRAVEYARD_HOOKSHOT_CHEST, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPE_RACE_FREESTANDING_POH, lambda bundle: is_adult(
            bundle) or can_do_trick(Tricks.GY_CHILD_DAMPE_RACE_POH, bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_POT6,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE1, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE2, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE3, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE4, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE5, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE6, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE7, lambda bundle: True),
        (Locations.GRAVEYARD_DAMPES_GRAVE_RUPEE8, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_DAMPES_GRAVE, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True),
        (Regions.KAK_WINDMILL, lambda bundle: (is_adult(bundle) and can_use(
            Items.SONG_OF_TIME, bundle)) or (is_child(bundle) and can_ground_jump(bundle)))
    ])

    # The Graveyard Dampes House
    # Connections
    connect_regions(Regions.GRAVEYARD_DAMPES_HOUSE, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True)
    ])

    # The Graveyard Warp Pad Region
    # Events
    add_events(Regions.GRAVEYARD_WARP_PAD_REGION, world, [
        (EventLocations.GRAVEYARD_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle))
    ])
    # Locations
    add_locations(Regions.GRAVEYARD_WARP_PAD_REGION, world, [
        (Locations.GRAVEYARD_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.GRAVEYARD_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.GRAVEYARD_WARP_PAD_REGION, world, [
        (Regions.THE_GRAVEYARD, lambda bundle: True),
        (Regions.SHADOW_TEMPLE_ENTRYWAY, lambda bundle: can_use(Items.DINS_FIRE, bundle) or (can_do_trick(
            Tricks.GY_SHADOW_FIRE_ARROWS, bundle) and is_adult(bundle) and can_use(Items.FIRE_ARROW, bundle)))
    ])
