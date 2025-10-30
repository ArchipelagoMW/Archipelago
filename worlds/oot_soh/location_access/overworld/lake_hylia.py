from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    LH_BUG_SHRUB = "LH Bug Shrub"
    LH_BEAN_FAIRY = "LH Bean Fairy"
    LH_GOSSIP_STONE_SONG_FAIRY = "LH Gossip Stone Song Fairy"
    LH_BUTTERFLY_FAIRY = "LH Butterfly Fairy"
    CHILD_SCARECROW = "Child Scarecrow"
    ADULT_SCARECROW = "Adult Scarecrow"
    LH_BEAN_PATCH = "LH Bean Patch"
    LH_DAY_NIGHT_CYCLE_CHILD = "LH Day Night Cycle Child"
    LH_DAY_NIGHT_CYCLE_ADULT = "LH Day Night Cycle Adult"


class LocalEvents(StrEnum):
    LH_BEAN_PLANTED = "Lake Hylia Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # Lake Hylia
    # Events
    add_events(Regions.LAKE_HYLIA, world, [
        (EventLocations.LH_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.LH_BEAN_FAIRY, Events.CAN_ACCESS_FAIRIES, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle) and
         can_use(Items.SONG_OF_STORMS, bundle)),
        (EventLocations.LH_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle)),
        (EventLocations.LH_BUG_SHRUB, Events.CAN_ACCESS_BUGS,
         lambda bundle: can_cut_shrubs(bundle)),
        (EventLocations.CHILD_SCARECROW, Events.CHILD_SCARECROW_UNLOCKED, lambda bundle: is_child(bundle) and
         has_item(Items.FAIRY_OCARINA, bundle) and
         ocarina_button_count(bundle) >= 2),
        (EventLocations.ADULT_SCARECROW, Events.ADULT_SCARECROW_UNLOCKED, lambda bundle: is_adult(bundle) and
         has_item(Items.FAIRY_OCARINA, bundle) and
         ocarina_button_count(bundle) >= 2),
        (EventLocations.LH_BEAN_PATCH, LocalEvents.LH_BEAN_PLANTED, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle)),
        (EventLocations.LH_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
        (EventLocations.LH_DAY_NIGHT_CYCLE_ADULT,
         Events.ADULT_CAN_PASS_TIME, lambda bundle: is_adult(bundle)),
    ])
    # Locations
    add_locations(Regions.LAKE_HYLIA, world, [
        (Locations.LH_UNDERWATER_ITEM, lambda bundle: is_child(bundle) and
         can_use(Items.SILVER_SCALE, bundle)),
        (Locations.LH_SUN, lambda bundle: is_adult(bundle) and
         ((has_item(Events.WATER_TEMPLE_COMPLETED, bundle) and
           has_item(Items.BRONZE_SCALE, bundle)) or
          can_use(Items.DISTANT_SCARECROW, bundle)) and
         can_use(Items.FAIRY_BOW, bundle)),
        (Locations.LH_FREESTANDING_POH, lambda bundle: is_adult(bundle) and
         (can_use(Items.SCARECROW, bundle) or
          has_item(LocalEvents.LH_BEAN_PLANTED, bundle))),
        (Locations.LH_GS_BEAN_PATCH, lambda bundle: can_spawn_soil_skull(bundle) and
         can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA)),
        (Locations.LH_GS_LAB_WALL, lambda bundle: is_child(bundle) and
         (can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)
          or (can_do_trick(Tricks.LH_LAB_WALL_GS, bundle) and
              can_jump_slash_except_hammer(bundle))) and
         can_get_nighttime_gs(bundle)),
        (Locations.LH_GS_SMALL_ISLAND, lambda bundle: is_child(bundle) and
         can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA) and
         can_get_nighttime_gs(bundle) and
         has_item(Items.BRONZE_SCALE, bundle)),
        (Locations.LH_GS_TREE, lambda bundle: is_adult(bundle) and
         can_use(Items.LONGSHOT, bundle) and
         can_get_nighttime_gs(bundle)),
        (Locations.LH_UNDERWATER_FRONT_RUPEE, lambda bundle: is_child(bundle) and
         has_item(Items.BRONZE_SCALE, bundle)),
        (Locations.LH_UNDERWATER_MIDDLE_RUPEE, lambda bundle: is_child(bundle) and
         (has_item(Items.SILVER_SCALE, bundle) or
          can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LH_UNDERWATER_BACK_RUPEE, lambda bundle: is_child(bundle) and
         (has_item(Items.SILVER_SCALE, bundle) or
          can_use(Items.IRON_BOOTS, bundle))),
        (Locations.LH_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle) and
         can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle) and
         can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle) and
         can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_LAB_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.LH_LAB_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_SOUTHEAST_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.LH_SOUTHEAST_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_SOUTHWEST_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.LH_SOUTHWEST_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.LH_ISLAND_SUNS_SONG_FAIRY, lambda bundle: can_use(Items.SUNS_SONG, bundle) and
         ((has_item(Items.BRONZE_SCALE, bundle) and
           (is_child(bundle) or
            has_item(Events.WATER_TEMPLE_COMPLETED, bundle))) or
          can_use(Items.DISTANT_SCARECROW, bundle))),
        (Locations.LH_GRASS_1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_4, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_5, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_6, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_7, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_8, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_9, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_10, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_11, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_12, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_13, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_14, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_15, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_16, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_17, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_18, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_19, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_20, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_21, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_22, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_23, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_24, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_25, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_26, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_27, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_28, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_29, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_30, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_31, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_32, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_33, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_34, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_35, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_GRASS_36, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_CHILD_GRASS_1, lambda bundle: is_child(bundle) and
         can_cut_shrubs(bundle)),
        (Locations.LH_CHILD_GRASS_2, lambda bundle: is_child(bundle) and
         can_cut_shrubs(bundle)),
        (Locations.LH_CHILD_GRASS_3, lambda bundle: is_child(bundle) and
         can_cut_shrubs(bundle)),
        (Locations.LH_CHILD_GRASS_4, lambda bundle: is_child(bundle) and
         can_cut_shrubs(bundle)),
        (Locations.LH_WARP_PAD_GRASS_1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.LH_WARP_PAD_GRASS_2, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.LAKE_HYLIA, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True),
        (Regions.LH_FROM_SHORTCUT, lambda bundle: True),
        (Regions.LH_OWL_FLIGHT, lambda bundle: is_child(bundle)),
        (Regions.LH_FISHING_ISLAND, lambda bundle: ((is_child(bundle)
                                                     or has_item(Events.WATER_TEMPLE_COMPLETED, bundle))
                                                    and has_item(Items.BRONZE_SCALE, bundle))
         or (is_adult(bundle)
             and (can_use(Items.SCARECROW, bundle)
                  or has_item(LocalEvents.LH_BEAN_PLANTED, bundle)))),
        (Regions.LH_LAB, lambda bundle: can_open_overworld_door(
            Items.HYLIA_LAB_KEY, bundle)),
        (Regions.LH_FROM_WATER_TEMPLE, lambda bundle: True),
        (Regions.LH_GROTTO, lambda bundle: True),
    ])

    # LH from Shortcut
    # Connections
    connect_regions(Regions.LH_FROM_SHORTCUT, world, [
        (Regions.LAKE_HYLIA, lambda bundle: (hearts(bundle) > 1) or
         has_item(Items.BOTTLE_WITH_FAIRY, bundle) or
         has_item(Items.BRONZE_SCALE, bundle) or
         can_use(Items.IRON_BOOTS, bundle)),
        (Regions.ZORAS_DOMAIN, lambda bundle: is_child(bundle) and
         (has_item(Items.SILVER_SCALE, bundle) or
          can_use(Items.IRON_BOOTS, bundle))),
    ])

    # LH from Water Temple
    # Connections
    connect_regions(Regions.LH_FROM_WATER_TEMPLE, world, [
        (Regions.LAKE_HYLIA, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or
         has_item(Items.BOTTLE_WITH_FAIRY, bundle) or
         can_use(Items.IRON_BOOTS, bundle)),
        (Regions.WATER_TEMPLE_ENTRYWAY, lambda bundle: can_use(Items.HOOKSHOT, bundle) and
         ((can_use(Items.IRON_BOOTS, bundle) or
           (can_do_trick(Tricks.LH_WATER_HOOKSHOT, bundle) and
            has_item(Items.GOLDEN_SCALE, bundle))) or
          (is_adult(bundle) and
           can_use(Items.LONGSHOT, bundle) and
           has_item(Items.GOLDEN_SCALE, bundle)))),
    ])

    # LH Fishing Island
    # Connections
    connect_regions(Regions.LH_FISHING_ISLAND, world, [
        (Regions.LAKE_HYLIA, lambda bundle: has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.LH_FISHING_HOLE, lambda bundle: can_open_overworld_door(
            Items.FISHING_HOLE_KEY, bundle)),
    ])

    # LH Owl Flight
    # Connections
    connect_regions(Regions.LH_OWL_FLIGHT, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True),
    ])

    # LH Lab
    # Locations
    add_locations(Regions.LH_LAB, world, [
        (Locations.LH_LAB_DIVE, lambda bundle: has_item(Items.GOLDEN_SCALE, bundle) or
         (can_do_trick(Tricks.LH_LAB_DIVING, bundle) and
          can_use(Items.IRON_BOOTS, bundle) and
          has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.LH_LAB_TRADE_EYEBALL_FROG, lambda bundle: is_adult(bundle) and
         can_use(Items.EYEBALL_FROG, bundle)),
        (Locations.LH_GS_LAB_CRATE, lambda bundle: can_use(Items.IRON_BOOTS, bundle) and
         can_use(Items.HOOKSHOT, bundle) and
         can_break_crates(bundle)),
        (Locations.LH_LAB_FRONT_RUPEE, lambda bundle: can_use(Items.IRON_BOOTS, bundle) or
         has_item(Items.GOLDEN_SCALE, bundle)),
        (Locations.LH_LAB_LEFT_RUPEE, lambda bundle: can_use(Items.IRON_BOOTS, bundle) or
         has_item(Items.GOLDEN_SCALE, bundle)),
        (Locations.LH_LAB_RIGHT_RUPEE, lambda bundle: can_use(Items.IRON_BOOTS, bundle) or
         has_item(Items.GOLDEN_SCALE, bundle)),
        (Locations.LH_LAB_CRATE, lambda bundle: can_use(Items.IRON_BOOTS, bundle) and
         can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.LH_LAB, world, [
        (Regions.LAKE_HYLIA, lambda bundle: True),
    ])

    # LH Fishing HOLE
    # Locations
    add_locations(Regions.LH_FISHING_HOLE, world, [
        (Locations.LH_CHILD_FISHING, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        # These locations need to be adjusted to have the option check when we add the option to split child and adult pond fish
        (Locations.LH_CHILD_POND_FISH1, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH2, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH3, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH4, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH5, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH6, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH7, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH8, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH9, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH10, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH11, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH12, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH13, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH14, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_FISH15, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_LOACH1, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_CHILD_POND_LOACH2, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_child(bundle)),
        (Locations.LH_ADULT_FISHING, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH1, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH2, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH3, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH4, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH5, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH6, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH7, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH8, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH9, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH10, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH11, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH12, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH13, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH14, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_FISH15, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_ADULT_POND_LOACH, lambda bundle: can_use(
            Items.FISHING_POLE, bundle) and is_adult(bundle)),
        (Locations.LH_HYRULE_LOACH_REWARD,
         lambda bundle: can_use(Items.FISHING_POLE, bundle)),
    ])
    # Connections
    connect_regions(Regions.LH_FISHING_HOLE, world, [
        (Regions.LH_FISHING_ISLAND, lambda bundle: True),
    ])

    # LH Grotto
    # Locations
    add_locations(Regions.LH_GROTTO, world, [
        (Locations.LH_DEKU_SCRUB_GROTTO_LEFT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LH_DEKU_SCRUB_GROTTO_RIGHT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LH_DEKU_SCRUB_GROTTO_CENTER,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LH_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.LH_GROTTO, world, [
        (Regions.LAKE_HYLIA, lambda bundle: True)
    ])
