from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    HC_GOSSIP_STONE_SONG_FAIRY = "HC Gossip Stone Song Fairy"
    HC_BUTTERFLY_FAIRY = "HC Butterfly Fairy"
    HC_BUG_ROCK = "HC Bug Rock"
    HC_STORMS_GROTTO_BEHIND_WALLS_NUT_POT = "HC Storms Grotto Behind Walls Nut Pot"
    HC_STORMS_GROTTO_BEHIND_WALLS_GOSSIP_STONE_SONG_FAIRY = "HC Storms Grotto Behind Walls Gossip Stone Song Fairy"
    HC_STORMS_GROTTO_BEHIND_WALLS_WANDERING_BUGS = "HC Storms Grotto Behind Walls Wandering Bugs"
    HC_OGC_RAINBOW_BRIDGE = "HC OGC Rainbow Bridge"
    HC_DAY_NIGHT_CYCLE_CHILD = "HC Day Night Cycle Child"


class LocalEvents(StrEnum):
    HC_OGC_RAINBOW_BRIDGE_BUILT = "HC OGC Rainbow Bridge Built"


def set_region_rules(world: "SohWorld") -> None:
    # Castle Grounds
    # Connections
    connect_regions(Regions.CASTLE_GROUNDS, world, [
        (Regions.MARKET, lambda bundle: True),
        (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: is_child(bundle)),
        (Regions.GANONS_CASTLE_GROUNDS, lambda bundle: is_adult(bundle))
    ])

    # Hyrule Castle Grounds
    # Events
    add_events(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (EventLocations.HC_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.HC_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle)),
        (EventLocations.HC_BUG_ROCK, Events.CAN_ACCESS_BUGS, lambda bundle: True),
        (EventLocations.HC_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
    ])
    # Locations
    add_locations(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (Locations.HC_MALON_EGG, lambda bundle: True),
        (Locations.HC_GS_TREE,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.CLOSE) and can_bonk_trees(bundle)),
        (Locations.HC_MALON_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_MALON_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_ROCK_WALL_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_ROCK_WALL_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_NEAR_STORMS_GROTTO_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.HC_NEAR_STORMS_GROTTO_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.HC_GROTTO_TREE, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_SKULLTULA_TREE, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_1, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_2, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_3, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_4, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_5, lambda bundle: can_bonk_trees(bundle)),
        (Locations.HC_NEAR_GUARDS_TREE_6, lambda bundle: can_bonk_trees(bundle)),
    ])
    # Connections
    connect_regions(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.HC_GREAT_FAIRY_FOUNTAIN, lambda bundle: blast_or_smash(bundle)),
        (Regions.HC_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle))
    ])
    if not world.options.skip_child_zelda:
        connect_regions(Regions.HYRULE_CASTLE_GROUNDS, world, [
            (Regions.HC_GARDEN,
             lambda bundle: can_use(Items.WEIRD_EGG, bundle) or
             (can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle) and can_jump_slash(bundle)))
        ])

    # Hyrule Castle Garden
    # Locations
    if not world.options.skip_child_zelda:
        add_locations(Regions.HC_GARDEN, world, [
            (Locations.HC_ZELDAS_LETTER, lambda bundle: True)
        ])
        # Connections
        connect_regions(Regions.HC_GARDEN, world, [
            (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: True),
            (Regions.HC_GARDEN_SONG_FROM_IMPA, lambda bundle: True)
        ])

    # Hyrule Castle Garden Song From Impa
    add_locations(Regions.HC_GARDEN_SONG_FROM_IMPA, world, [
        (Locations.SONG_FROM_IMPA, lambda bundle: True)
    ])

    # Hyrule Castle Great Fairy Fountain
    # Locations
    add_locations(Regions.HC_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.HC_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.HC_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True)
    ])

    # Hyrule Castle Storms Grotto
    # Connections
    connect_regions(Regions.HC_STORMS_GROTTO, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.HC_STORMS_GROTTO_BEHIND_WALLS,
         lambda bundle: can_break_mud_walls(bundle)),
        (Regions.HC_STORMS_SKULLTULA, lambda bundle: can_use(
            Items.BOOMERANG, bundle) and can_do_trick(Tricks.HC_STORMS_GS, bundle))
    ])

    # Hyrule Castle Storms Grotto Behind Walls
    # Events
    add_events(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (EventLocations.HC_STORMS_GROTTO_BEHIND_WALLS_NUT_POT,
         Events.CAN_FARM_NUTS, lambda bundle: can_break_pots(bundle)),
        (EventLocations.HC_STORMS_GROTTO_BEHIND_WALLS_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.HC_STORMS_GROTTO_BEHIND_WALLS_WANDERING_BUGS,
         Events.CAN_ACCESS_BUGS, lambda bundle: True)

    ])
    # Locations
    add_locations(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (Locations.HC_STORMS_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_STORMS_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_STORMS_GROTTO_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT4, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (Regions.HC_STORMS_GROTTO, lambda bundle: True),
        (Regions.HC_STORMS_SKULLTULA, lambda bundle: hookshot_or_boomerang(bundle)),
    ])

    # Hyrule Castle Storms Skulltule
    # This is a deviation from the original SOH logic because of the union of locations
    # Locations
    add_locations(Regions.HC_STORMS_SKULLTULA, world, [
        (Locations.HC_GS_STORMS_GROTTO, lambda bundle: True)
    ])

    # Ganon's Castle Grounds
    # Events
    add_events(Regions.GANONS_CASTLE_GROUNDS, world, [
        (EventLocations.HC_OGC_RAINBOW_BRIDGE, LocalEvents.HC_OGC_RAINBOW_BRIDGE_BUILT,
         lambda bundle: can_build_rainbow_bridge(bundle))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_GROUNDS, world, [
        (Locations.HC_OGC_GS, lambda bundle: can_jump_slash_except_hammer(bundle) or
         can_use_projectile(bundle) or
         (can_shield(bundle) and can_use(Items.MEGATON_HAMMER, bundle)) or
         can_use(Items.DINS_FIRE, bundle))
    ])
    # Connections
    connect_regions(Regions.GANONS_CASTLE_GROUNDS, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: at_night(bundle)),
        (Regions.OGC_GREAT_FAIRY_FOUNTAIN, lambda bundle: can_use(
            Items.GOLDEN_GAUNTLETS, bundle) and at_night(bundle)),
        (Regions.GANONS_CASTLE_LEDGE, lambda bundle: has_item(
            LocalEvents.HC_OGC_RAINBOW_BRIDGE_BUILT, bundle))
    ])

    # OGC Great Fairy Fountain
    # Locations
    add_locations(Regions.OGC_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.OGC_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.OGC_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True)
    ])

    # Castle Grounds from Ganon's Castle
    # Connections
    connect_regions(Regions.CASTLE_GROUNDS_FROM_GANONS_CASTLE, world, [
        (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: is_child(bundle)),
        (Regions.GANONS_CASTLE_LEDGE, lambda bundle: is_adult(bundle))
    ])

    # Ganon's Castle Ledge
    # Connections
    connect_regions(Regions.GANONS_CASTLE_LEDGE, world, [
        (Regions.GANONS_CASTLE_GROUNDS, lambda bundle: has_item(
            LocalEvents.HC_OGC_RAINBOW_BRIDGE_BUILT, bundle)),
        (Regions.GANONS_CASTLE_ENTRYWAY, lambda bundle: is_adult(bundle))
    ])
