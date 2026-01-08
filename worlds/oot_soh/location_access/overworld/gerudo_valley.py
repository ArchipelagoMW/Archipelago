from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    GV_BUG_ROCK = "GV Bug Rock"
    GV_GOSSIP_STONE_SONG_FAIRY = "GV Gossip Stone Song Fairy"
    GV_BEAN_SOIL = "GV Bean Soil"
    GV_BEAN_PATCH = "GV Bean Patch"
    GV_DAY_NIGHT_CYCLE_CHILD = "GV Day Night Cycle Child"
    GV_DAY_NIGHT_CYCLE_ADULT = "GV Day Night Cycle Adult"


class LocalEvents(StrEnum):
    GV_BEAN_PLANTED = "GV Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # Gerudo Valley
    # Events
    add_events(Regions.GERUDO_VALLEY, world, [
        (EventLocations.GV_BUG_ROCK, Events.CAN_ACCESS_BUGS,
         lambda bundle: is_child(bundle)),
        (EventLocations.GV_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
        (EventLocations.GV_DAY_NIGHT_CYCLE_ADULT,
         Events.ADULT_CAN_PASS_TIME, lambda bundle: is_adult(bundle)),
    ])
    # Locations
    add_locations(Regions.GERUDO_VALLEY, world, [
        (Locations.GV_GS_SMALL_BRIDGE,
         lambda bundle: is_child(bundle) and can_use(Items.BOOMERANG, bundle) and can_get_nighttime_gs(bundle)),
    ])
    # Connection
    connect_regions(Regions.GERUDO_VALLEY, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True),
        (Regions.GV_UPPER_STREAM,
         lambda bundle: is_child(bundle) or has_item(Items.BRONZE_SCALE, bundle) or take_damage(bundle)),
        (Regions.GV_CRATE_LEDGE, lambda bundle: is_child(
            bundle) or can_use(Items.LONGSHOT, bundle)),
        (Regions.GV_GROTTO_LEDGE, lambda bundle: True),
        (Regions.GV_FORTRESS_SIDE, lambda bundle: (is_adult(bundle) and (
            can_use(Items.EPONA, bundle) or can_use(Items.LONGSHOT,
                                                    bundle) or world.options.fortress_carpenters.value == 2 or has_item(
                Events.RESCUED_ALL_CARPENTERS, bundle))) or (is_child(bundle) and can_use(Items.HOOKSHOT, bundle))),
        (Regions.GV_LOWER_STREAM, lambda bundle: is_child(bundle))
    ])

    # GV Upper Stream
    # Events
    add_events(Regions.GV_UPPER_STREAM, world, [
        (EventLocations.GV_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.GV_BEAN_SOIL, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (EventLocations.GV_BEAN_PATCH, LocalEvents.GV_BEAN_PLANTED,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle)),
    ])
    # Locations
    add_locations(Regions.GV_UPPER_STREAM, world, [
        (Locations.GV_WATERFALL_FREESTANDING_POH, lambda bundle: is_child(
            bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (Locations.GV_GS_BEAN_PATCH, lambda bundle: can_spawn_soil_skull(
            bundle) and can_attack(bundle)),
        (Locations.GV_COW, lambda bundle: is_child(
            bundle) and can_use(Items.EPONAS_SONG, bundle)),
        (Locations.GV_BEAN_SPROUT_FAIRY1,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.GV_BEAN_SPROUT_FAIRY2,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.GV_BEAN_SPROUT_FAIRY3,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS,
                                                                                           bundle)),
        (Locations.GV_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.GV_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GV_NEAR_COW_CRATE, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.GV_UPPER_STREAM, world, [
        (Regions.GV_LOWER_STREAM,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle)),
    ])

    # GV Lower Stream
    # Connections
    connect_regions(Regions.GV_LOWER_STREAM, world, [
        (Regions.LAKE_HYLIA, lambda bundle: True)
    ])

    # GV Grotto Ledge
    # Connections
    connect_regions(Regions.GV_GROTTO_LEDGE, world, [
        (Regions.GV_UPPER_STREAM,
         lambda bundle: can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle)),
        (Regions.GV_LOWER_STREAM,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle)),
        (Regions.GV_OCTOROK_GROTTO, lambda bundle: can_use(
            Items.SILVER_GAUNTLETS, bundle)),
        (Regions.GV_CRATE_LEDGE, lambda bundle: can_use(Items.LONGSHOT, bundle))
    ])

    # GV Crate Ledge
    # Locations
    add_locations(Regions.GV_CRATE_LEDGE, world, [
        (Locations.GV_CRATE_FREESTANDING_POH,
         lambda bundle: can_break_crates(bundle)),
        (Locations.GV_FREESTANDING_POH_CRATE,
         lambda bundle: can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.GV_CRATE_LEDGE, world, [
        (Regions.GV_UPPER_STREAM,
         lambda bundle: can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle)),
        (Regions.GV_LOWER_STREAM,
         lambda bundle: can_use(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle)),
    ])

    # GV Fortress Side
    # Locations
    add_locations(Regions.GV_FORTRESS_SIDE, world, [
        (Locations.GV_CHEST, lambda bundle: is_adult(bundle)
         and can_use(Items.MEGATON_HAMMER, bundle)),
        (Locations.GV_TRADE_SAW, lambda bundle: is_adult(
            bundle) and can_use(Items.POACHERS_SAW, bundle)),
        (Locations.GV_GS_BEHIND_TENT,
         lambda bundle: is_adult(bundle) and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.GV_GS_PILLAR,
         lambda bundle: is_adult(bundle) and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.GV_NEAR_BRIDGE_CRATE1, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
        (Locations.GV_NEAR_BRIDGE_CRATE2, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
        (Locations.GV_NEAR_BRIDGE_CRATE3, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
        (Locations.GV_NEAR_BRIDGE_CRATE4, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.GV_FORTRESS_SIDE, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True),
        (Regions.GV_UPPER_STREAM, lambda bundle: True),
        (Regions.GERUDO_VALLEY,
         lambda bundle: is_child(bundle) or can_use(Items.EPONA, bundle) or can_use(Items.LONGSHOT,
                                                                                    bundle) or world.options.fortress_carpenters.value == 2 or has_item(
             Events.RESCUED_ALL_CARPENTERS, bundle)),
        (Regions.GV_CARPENTER_TENT, lambda bundle: is_adult(bundle)),
        (Regions.GV_STORMS_GROTTO, lambda bundle: is_adult(
            bundle) and can_open_storms_grotto(bundle)),
        (Regions.GV_CRATE_LEDGE,
         lambda bundle: can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle)),
    ])

    # GV Carpenter Tent
    # Connections
    connect_regions(Regions.GV_CARPENTER_TENT, world, [
        (Regions.GV_FORTRESS_SIDE, lambda bundle: True),
    ])

    # GV Octorok Grotto
    # Locations
    add_locations(Regions.GV_OCTOROK_GROTTO, world, [
        (Locations.GV_OCTOROK_GROTTO_FRONT_LEFT_BLUE_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_FRONT_RIGHT_BLUE_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV__OCTOROK_GROTTO_BACK_BLUE_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_FRONT_LEFT_GREEN_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_FRONT_RIGHT_GREEN_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_BACK_LEFT_GREEN_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_BACK_RIGHT_GREEN_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
        (Locations.GV_OCTOROK_GROTTO_RED_RUPEE,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle) or can_use(
             Items.BOOMERANG, bundle)),
    ])
    # Connections
    connect_regions(Regions.GV_OCTOROK_GROTTO, world, [
        (Regions.GV_GROTTO_LEDGE, lambda bundle: True),
    ])

    # GV Storms Grotto
    # Locations
    add_locations(Regions.GV_STORMS_GROTTO, world, [
        (Locations.GV_DEKU_SCRUB_GROTTO_REAR,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.GV_DEKU_SCRUB_GROTTO_FRONT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.GV_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.GV_STORMS_GROTTO, world, [
        (Regions.GV_FORTRESS_SIDE, lambda bundle: True),
    ])
