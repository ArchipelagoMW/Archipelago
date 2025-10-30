from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    DMT_BEAN_PLANT_FAIRY = "DMT Bean Plant Fairy"
    DMT_GOSSIP_STONE_SONG_FAIRY = "DMT Gossip Stone Song Fairy"
    DMT_BUG_ROCK = "DMT Bug Rock"
    DMT_STORMS_GROTTO_GOSSIP_STONE_SONG_FAIRY = "DMT Storms Grotto Gossip Stone Song Fairy"
    DMT_STORMS_GROTTO_BUTTERFLY_FAIRY = "DMT Storms Grotto Butterfly Fairy"
    DMT_STORMS_GROTTO_BUG_GRASS = "DMT Storms Grotto Bug Grass"
    DMT_STORMS_GROTTO_PUDDLE_FISH = "DMT Storms Grotto Puddle Fish"
    DMT_BEAN_PATCH = "DMT Bean Patch"
    DMT_DAY_NIGHT_CYCLE_CHILD = "DMT Day Night Cycle Child"
    DMT_DAY_NIGHT_CYCLE_ADULT = "DMT Day Night Cycle Adult"


class LocalEvents(StrEnum):
    DMT_BEAN_PLANTED = "DMT Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    # Death Mountain Trail
    # Events
    add_events(Regions.DEATH_MOUNTAIN_TRAIL, world, [
        (EventLocations.DMT_BEAN_PLANT_FAIRY, Events.CAN_ACCESS_FAIRIES, lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN,
         bundle) and can_use(Items.SONG_OF_STORMS, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (EventLocations.DMT_BEAN_PATCH, LocalEvents.DMT_BEAN_PLANTED, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (EventLocations.DMT_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
        (EventLocations.DMT_DAY_NIGHT_CYCLE_ADULT,
         Events.ADULT_CAN_PASS_TIME, lambda bundle: is_adult(bundle)),
    ])
    # Locations
    add_locations(Regions.DEATH_MOUNTAIN_TRAIL, world, [
        (Locations.DMT_CHEST, lambda bundle: blast_or_smash(bundle) or (can_do_trick(
            Tricks.DMT_BOMBABLE, bundle) and is_child(bundle) and has_item(Items.GORONS_BRACELET, bundle))),
        (Locations.DMT_FREESTANDING_POH, lambda bundle: take_damage(bundle) or can_use(Items.HOVER_BOOTS, bundle) or (is_adult(bundle)
         and has_item(LocalEvents.DMT_BEAN_PLANTED, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.DMT_GS_BEAN_PATCH, lambda bundle: can_spawn_soil_skull(bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle) or (
            can_do_trick(Tricks.DMT_SOIL_GS, bundle) and (take_damage(bundle) or can_use(Items.HOVER_BOOTS, bundle)) and can_use(Items.BOOMERANG, bundle)))),
        (Locations.DMT_GS_NEAR_KAK, lambda bundle: blast_or_smash(bundle)),
        (Locations.DMT_GS_ABOVE_DODONGOS_CAVERN, lambda bundle: is_adult(bundle) and at_night(bundle) and (can_use(Items.MEGATON_HAMMER, bundle) or (can_do_trick(Tricks.DMT_HOOKSHOT_LOWER_GS, bundle) and can_use(Items.HOOKSHOT, bundle)) or (can_do_trick(
            Tricks.DMT_BEAN_LOWER_GS, bundle) and has_item(LocalEvents.DMT_BEAN_PLANTED, bundle)) or (can_do_trick(Tricks.DMT_HOVERS_LOWER_GS, bundle) and can_use(Items.HOVER_BOOTS, bundle)) or can_do_trick(Tricks.DMT_JS_LOWER_GS, bundle)) and can_get_nighttime_gs(bundle)),
        (Locations.DMT_BLUE_RUPEE_UNDER_BOULDER,
         lambda bundle: is_child(bundle) and blast_or_smash(bundle)),
        (Locations.DMT_RED_RUPEE_UNDER_BOULDER,
         lambda bundle: is_child(bundle) and blast_or_smash(bundle)),
        (Locations.DMT_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(
            Items.SONG_OF_STORMS, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (Locations.DMT_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(
            Items.SONG_OF_STORMS, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (Locations.DMT_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle) and can_use(
            Items.SONG_OF_STORMS, bundle) and (has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (Locations.DMT_FLAG_SUNS_SONG_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle))
    ])
    # Connections
    connect_regions(Regions.DEATH_MOUNTAIN_TRAIL, world, [
        (Regions.KAK_BEHIND_GATE, lambda bundle: True),
        (Regions.GORON_CITY, lambda bundle: True),
        (Regions.DEATH_MOUNTAIN_SUMMIT, lambda bundle: blast_or_smash(bundle) or (is_adult(bundle) and ((has_item(LocalEvents.DMT_BEAN_PLANTED, bundle)
         and has_item(Items.GORONS_BRACELET, bundle)) or (can_use(Items.HOVER_BOOTS, bundle) and can_do_trick(Tricks.DMT_CLIMB_HOVERS, bundle))))),
        (Regions.DODONGOS_CAVERN_ENTRYWAY, lambda bundle: has_explosives(
            bundle) or has_item(Items.GORONS_BRACELET, bundle) or is_adult(bundle)),
        (Regions.DMT_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle))
    ])

    # Death Mountain Summit
    # Events
    add_events(Regions.DEATH_MOUNTAIN_SUMMIT, world, [
        (EventLocations.DMT_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.DMT_BUG_ROCK, Events.CAN_ACCESS_BUGS,
         lambda bundle: is_child(bundle))
    ])
    # Locations
    add_locations(Regions.DEATH_MOUNTAIN_SUMMIT, world, [
        (Locations.DMT_TRADE_BROKEN_SWORD, lambda bundle: is_adult(
            bundle) and can_use(Items.BROKEN_GORONS_SWORD, bundle)),
        (Locations.DMT_TRADE_EYEDROPS, lambda bundle: is_adult(
            bundle) and can_use(Items.WORLDS_FINEST_EYEDROPS, bundle)),
        (Locations.DMT_TRADE_CLAIM_CHECK, lambda bundle: is_adult(
            bundle) and can_use(Items.CLAIM_CHECK, bundle)),
        (Locations.DMT_GS_FALLING_ROCKS_PATH, lambda bundle: is_adult(bundle) and at_night(bundle) and (can_use(
            Items.MEGATON_HAMMER, bundle) or can_do_trick(Tricks.DMT_UPPER_GS, bundle)) and can_get_nighttime_gs(bundle)),
        (Locations.DMT_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.DMT_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.DEATH_MOUNTAIN_SUMMIT, world, [
        (Regions.DEATH_MOUNTAIN_TRAIL, lambda bundle: True),
        (Regions.DMC_UPPER_LOCAL, lambda bundle: True),
        (Regions.DMT_OWL_FLIGHT, lambda bundle: is_child(bundle)),
        (Regions.DMT_COW_GROTTO, lambda bundle: blast_or_smash(bundle)),
        (Regions.DMT_GREAT_FAIRY_FOUNTAIN, lambda bundle: blast_or_smash(bundle))
    ])

    # Death Mountain Trail Owl Flight
    # Connections
    connect_regions(Regions.DMT_OWL_FLIGHT, world, [
        (Regions.KAK_IMPAS_ROOFTOP, lambda bundle: True)
    ])

    # Death Mountain Trail Cow Grotto
    # Locations
    add_locations(Regions.DMT_COW_GROTTO, world, [
        (Locations.DMT_COW_GROTTO_COW,
         lambda bundle: can_use(Items.EPONAS_SONG, bundle)),
        (Locations.DMT_COW_GROTTO_BEEHIVE,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.DMT_COW_GROTTO_LEFT_HEART, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_MIDDLE_LEFT_HEART, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_MIDDLE_RIGHT_HEART, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RIGHT_HEART, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE1, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE2, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE3, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE4, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE5, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RUPEE6, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_RED_RUPEE, lambda bundle: True),
        (Locations.DMT_COW_GROTTO_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.DMT_COW_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMT_COW_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DMT_COW_GROTTO, world, [
        (Regions.DEATH_MOUNTAIN_SUMMIT, lambda bundle: True)
    ])

    # Death Mountain Trail Storms Grotto
    # Events
    add_events(Regions.DMT_STORMS_GROTTO, world, [
        (EventLocations.DMT_STORMS_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.DMT_STORMS_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.DMT_STORMS_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.DMT_STORMS_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.DMT_STORMS_GROTTO, world, [
        (Locations.DMT_STORMS_GROTTO_CHEST, lambda bundle: True),
        (Locations.DMT_STORMS_GROTTO_FISH, lambda bundle: has_bottle(bundle)),
        (Locations.DMT_STORMS_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.DMT_STORMS_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.DMT_STORMS_GROTTO_BEEHIVE_LEFT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.DMT_STORMS_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.DMT_STORMS_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMT_STORMS_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMT_STORMS_GROTTO_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DMT_STORMS_GROTTO_GRASS4, lambda bundle: can_cut_shrubs(bundle))
    ])
    # Connections
    connect_regions(Regions.DMT_STORMS_GROTTO, world, [
        (Regions.DEATH_MOUNTAIN_TRAIL, lambda bundle: True)
    ])

    # Death Mountain Trail Great Fairy Fountain
    # Locations
    add_locations(Regions.DMT_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.DMT_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.DMT_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.DEATH_MOUNTAIN_SUMMIT, lambda bundle: True)
    ])
