from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    GC_GOSSIP_STONE_SONG_FAIRY = "GC Gossip Stone Song Fairy"
    GC_STICK_POT = "GC Stick Pot"
    GC_BUG_ROCK = "GC Bug Rock"
    GC_DARUNIAS_CHAMBER_TORCH = "GC Darunias Chamber Torch"
    GC_FIRE_AROUND_POT = "GC Fire Around Pot"
    GC_WOODS_WARP = "GC Woods Warp"
    GC_WOODS_WARP_FROM_WOODS = "GC Woods Warp From Woods"
    GC_DARUNIAS_DOOR_AS_CHILD = "GC Darunias Door as Child"
    GC_STOP_ROLLING_GORON_AS_ADULT = "GC Stop Rolling Goron as Adult"


class LocalEvents(StrEnum):
    GC_CHILD_FIRE_LIT = "GC Child Fire Lit"
    GC_WOODS_WARP_OPEN = "GC Woods Warp Open"
    GC_DARUNIAS_DOOR_OPENED_AS_CHILD = "GC Darunias Door Opened as Child"
    GC_STOP_ROLLING_GORON_AS_ADULT = "GC Stop Rolling Goron As Adult"


def set_region_rules(world: "SohWorld") -> None:
    # Goron City
    # Events
    add_events(Regions.GORON_CITY, world, [
        (EventLocations.GC_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (EventLocations.GC_STICK_POT, Events.CAN_FARM_STICKS,
         lambda bundle: is_child(bundle)),
        (EventLocations.GC_BUG_ROCK, Events.CAN_ACCESS_BUGS, lambda bundle: blast_or_smash(
            bundle) or can_use(Items.SILVER_GAUNTLETS, bundle)),
        (EventLocations.GC_FIRE_AROUND_POT, LocalEvents.GC_CHILD_FIRE_LIT,
         lambda bundle: is_child(bundle) and can_use(Items.DINS_FIRE, bundle)),
        (EventLocations.GC_WOODS_WARP, LocalEvents.GC_WOODS_WARP_OPEN, lambda bundle: can_detonate_upright_bomb_flower(
            bundle) or can_use(Items.MEGATON_HAMMER, bundle) or has_item(LocalEvents.GC_CHILD_FIRE_LIT, bundle)),
        (EventLocations.GC_DARUNIAS_DOOR_AS_CHILD, LocalEvents.GC_DARUNIAS_DOOR_OPENED_AS_CHILD,
         lambda bundle: is_child(bundle) and can_use(Items.ZELDAS_LULLABY, bundle)),
        (EventLocations.GC_STOP_ROLLING_GORON_AS_ADULT, LocalEvents.GC_STOP_ROLLING_GORON_AS_ADULT, lambda bundle: is_adult(bundle) and (has_item(Items.GORONS_BRACELET, bundle) or has_explosives(bundle) or can_use(
            Items.FAIRY_BOW, bundle) or (can_do_trick(Tricks.GC_LINK_GORON_DINS, bundle) and (can_use(Items.DINS_FIRE, bundle) or (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle) and can_use(Items.BOTTLE_WITH_BLUE_FIRE, bundle))))))
    ])
    # Locations
    add_locations(Regions.GORON_CITY, world, [
        (Locations.GC_MAZE_LEFT_CHEST, lambda bundle: can_use_any([Items.MEGATON_HAMMER, Items.SILVER_GAUNTLETS], bundle) or (
            can_do_trick(Tricks.GC_LEFTMOST, bundle) and has_explosives(bundle) and can_use(Items.HOVER_BOOTS, bundle))),
        (Locations.GC_MAZE_CENTER_CHEST, lambda bundle: blast_or_smash(
            bundle) or can_use(Items.SILVER_GAUNTLETS, bundle)),
        (Locations.GC_MAZE_RIGHT_CHEST, lambda bundle: blast_or_smash(
            bundle) or can_use(Items.SILVER_GAUNTLETS, bundle)),
        (Locations.GC_POT_FREESTANDING_POH, lambda bundle: is_child(bundle) and has_item(LocalEvents.GC_CHILD_FIRE_LIT, bundle) and (can_use(Items.BOMB_BAG, bundle) or (
            has_item(Items.GORONS_BRACELET, bundle) and can_do_trick(Tricks.GC_POT_STRENGTH, bundle)) or (can_use(Items.BOMBCHUS_5, bundle) and can_do_trick(Tricks.GC_POT, bundle)))),
        (Locations.GC_ROLLING_GORON_AS_CHILD, lambda bundle: is_child(bundle) and (has_explosives(bundle) or (
            has_item(Items.GORONS_BRACELET, bundle) and can_do_trick(Tricks.GC_ROLLING_STRENGTH, bundle)))),
        (Locations.GC_ROLLING_GORON_AS_ADULT, lambda bundle: has_item(
            LocalEvents.GC_STOP_ROLLING_GORON_AS_ADULT, bundle)),
        (Locations.GC_GS_BOULDER_MAZE, lambda bundle: is_child(
            bundle) and blast_or_smash(bundle)),
        (Locations.GC_GS_CENTER_PLATFORM, lambda bundle: is_adult(
            bundle) and can_attack(bundle)),
        (Locations.GC_MEDIGORON, lambda bundle: is_adult(bundle) and has_item(Items.ADULT_WALLET,
         bundle) and (can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle))),
        (Locations.GC_MAZE_GOSSIP_STONE_FAIRY, lambda bundle: (blast_or_smash(bundle) or can_use(
            Items.SILVER_GAUNTLETS, bundle)) and call_gossip_fairy_except_suns(bundle)),
        (Locations.GC_MAZE_GOSSIP_STONE_BIG_FAIRY, lambda bundle: (blast_or_smash(bundle) or can_use(
            Items.SILVER_GAUNTLETS, bundle)) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GC_LOWER_STAIRCASE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_LOWER_STAIRCASE_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_UPPER_STAIRCASE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_UPPER_STAIRCASE_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_UPPER_STAIRCASE_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_MAZE_CRATE, lambda bundle: blast_or_smash(bundle) or (
            can_use(Items.SILVER_GAUNTLETS, bundle) and can_break_crates(bundle)))
    ])
    # Connections
    connect_regions(Regions.GORON_CITY, world, [
        (Regions.DEATH_MOUNTAIN_TRAIL, lambda bundle: True),
        (Regions.GC_MEDIGORON, lambda bundle: can_break_mud_walls(
            bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Regions.GC_WOODS_WARP, lambda bundle: has_item(
            LocalEvents.GC_WOODS_WARP_OPEN, bundle)),
        (Regions.GC_SHOP, lambda bundle: (is_adult(bundle) and has_item(LocalEvents.GC_STOP_ROLLING_GORON_AS_ADULT, bundle)) or (is_child(bundle) and (
            blast_or_smash(bundle) or has_item(Items.GORONS_BRACELET, bundle) or has_item(LocalEvents.GC_CHILD_FIRE_LIT, bundle) or can_use(Items.FAIRY_BOW, bundle)))),
        (Regions.GC_DARUNIAS_CHAMBER, lambda bundle: (is_adult(bundle) and has_item(LocalEvents.GC_STOP_ROLLING_GORON_AS_ADULT,
         bundle)) or (is_child(bundle) and has_item(LocalEvents.GC_DARUNIAS_DOOR_OPENED_AS_CHILD, bundle))),
        (Regions.GC_GROTTO_PLATFORM, lambda bundle: is_adult(bundle) and ((can_use(Items.SONG_OF_TIME, bundle) and ((effective_health(bundle) > 2) or can_use(Items.GORON_TUNIC, bundle) or can_use(Items.LONGSHOT, bundle) or can_use(Items.NAYRUS_LOVE, bundle))) or (effective_health(
            bundle) > 1 and can_use(Items.GORON_TUNIC, bundle) and can_use(Items.HOOKSHOT, bundle)) or (can_use(Items.NAYRUS_LOVE, bundle) and can_use(Items.HOOKSHOT, bundle)) or (effective_health(bundle) > 2 and can_use(Items.HOOKSHOT, bundle) and can_do_trick(Tricks.GC_GROTTO, bundle)))),
    ])

    # Goron City Medigoron
    # Locations
    add_locations(Regions.GC_MEDIGORON, world, [
        (Locations.GC_MEDIGORON_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.GC_MEDIGORON_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GC_MEDIGORON_POT1, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.GC_MEDIGORON, world, [
        (Regions.GORON_CITY, lambda bundle: True)
    ])

    # Goron City Woods Warp
    # Events
    add_events(Regions.GC_WOODS_WARP, world, [
        (EventLocations.GC_WOODS_WARP_FROM_WOODS, LocalEvents.GC_WOODS_WARP_OPEN,
         lambda bundle: blast_or_smash(bundle) or can_use(Items.DINS_FIRE, bundle))
    ])
    # Connections
    connect_regions(Regions.GC_WOODS_WARP, world, [
        (Regions.GORON_CITY, lambda bundle: has_item(
            LocalEvents.GC_WOODS_WARP_OPEN, bundle)),
        (Regions.LOST_WOODS, lambda bundle: True)
    ])

    # Goron City Darunias Chamber
    # Events
    add_events(Regions.GC_DARUNIAS_CHAMBER, world, [
        (EventLocations.GC_DARUNIAS_CHAMBER_TORCH, LocalEvents.GC_CHILD_FIRE_LIT,
         lambda bundle: is_child(bundle) and can_use(Items.STICKS, bundle))
    ])
    # Locations
    add_locations(Regions.GC_DARUNIAS_CHAMBER, world, [
        (Locations.GC_DARUNIAS_JOY, lambda bundle: is_child(
            bundle) and can_use(Items.SARIAS_SONG, bundle)),
        (Locations.GC_DARUNIA_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_DARUNIA_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.GC_DARUNIA_POT3, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.GC_DARUNIAS_CHAMBER, world, [
        (Regions.GORON_CITY, lambda bundle: True),
        (Regions.DMC_LOWER_LOCAL, lambda bundle: is_adult(bundle))
    ])

    # Goron City Grotto Platform
    # Connections
    connect_regions(Regions.GC_GROTTO_PLATFORM, world, [
        (Regions.GC_GROTTO, lambda bundle: True),
        (Regions.GORON_CITY, lambda bundle: effective_health(bundle) > 2 or can_use_any([Items.GORON_TUNIC, Items.NAYRUS_LOVE], bundle) or (
            (is_child(bundle) or can_use(Items.SONG_OF_TIME, bundle)) and can_use(Items.LONGSHOT, bundle)))
    ])

    # Goron City Shop
    # Locations
    add_locations(Regions.GC_SHOP, world, [
        (Locations.GC_SHOP_ITEM1, lambda bundle: True),
        (Locations.GC_SHOP_ITEM2, lambda bundle: True),
        (Locations.GC_SHOP_ITEM3, lambda bundle: True),
        (Locations.GC_SHOP_ITEM4, lambda bundle: True),
        (Locations.GC_SHOP_ITEM5, lambda bundle: True),
        (Locations.GC_SHOP_ITEM6, lambda bundle: True),
        (Locations.GC_SHOP_ITEM7, lambda bundle: True),
        (Locations.GC_SHOP_ITEM8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.GC_SHOP, world, [
        (Regions.GORON_CITY, lambda bundle: True)
    ])

    # Goron City Grotto
    # Locations
    add_locations(Regions.GC_GROTTO, world, [
        (Locations.GC_DEKU_SCRUB_GROTTO_LEFT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.GC_DEKU_SCRUB_GROTTO_RIGHT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.GC_DEKU_SCRUB_GROTTO_CENTER,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.GC_GROTTO_BEEHIVE, lambda bundle: can_break_upper_beehives(bundle))
    ])
    # Connections
    connect_regions(Regions.GC_GROTTO, world, [
        (Regions.GC_GROTTO_PLATFORM, lambda bundle: True)
    ])
