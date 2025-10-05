from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld

class EventLocations(str, Enum):
    HYRULE_CASTLE_GROUNDS_GOSSIP_STONE_FAIRY = "Hyrule Castle Grounds Gossip Stone Fairy"
    HYRULE_CASTLE_GROUNDS_BUTTERFLY_FAIRY = "Hyrule Castle Grounds Butterfly Fairy"
    HYRULE_CASTLE_GROUNDS_BUG_ROCK = "Hyrule Castle Grounds Bug Rock"
    HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_NUT_POT = "Hyrule Castle Storms Grotto Behind Walls Nut Pot"
    HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_GOSSIP_STONE_FAIRY = "Hyrule Castle Storms Grotto Behind Walls Gossip Stone Fairy"
    HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_WANDERING_BUGS = "Hyrule Castle Storms Grotto Behind Walls Wandering Bugs"
    GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE = "Ganon's Castle Grounds Build Rainbow Bridge"


class LocalEvents(str, Enum):
    GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE = "Ganon's Castle Grounds Build Rainbow Bridge"

def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ##Castle Grounds
    # Connections
    connect_regions(Regions.CASTLE_GROUNDS, world, [
        (Regions.MARKET, lambda bundle: True),
        (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: is_child(bundle)),
        (Regions.GANONS_CASTLE_GROUNDS, lambda bundle: is_adult(bundle))
    ])

    ##Hyrule Castle Grounds
    # Events
    add_events(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (EventLocations.HYRULE_CASTLE_GROUNDS_GOSSIP_STONE_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.HYRULE_CASTLE_GROUNDS_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle)),
        (EventLocations.HYRULE_CASTLE_GROUNDS_BUG_ROCK, Events.CAN_ACCESS_BUGS, lambda bundle: True)
    ])

    # Locations
    add_locations(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (Locations.HC_MALON_EGG, lambda bundle: True),
        (Locations.HC_GS_TREE,
         lambda bundle: can_kill_enemy(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.CLOSE) and can_bonk_trees(bundle)),
        (Locations.HC_MALON_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_MALON_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_ROCK_WALL_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_ROCK_WALL_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_NEAR_STORMS_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.HC_NEAR_STORMS_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle))
    ])

    # Connections
    connect_regions(Regions.HYRULE_CASTLE_GROUNDS, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.HC_GARDEN,
         lambda bundle: can_use(Items.WEIRD_EGG, bundle) or
                        (can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle) and can_jump_slash(bundle))),
        (Regions.HC_GREAT_FAIRY_FOUNTAIN, lambda bundle: blast_or_smash(bundle)),
        (Regions.HC_STORMS_GROTTO, lambda  bundle: can_open_storms_grotto(bundle))
    ])

    ##Hyrule Castle Garden
    # Locations
    add_locations(Regions.HC_GARDEN, world, [
        (Locations.HC_ZELDAS_LETTER, lambda bundle: True),
        (Locations.SONG_FROM_IMPA, lambda bundle: True)
    ])

    # Connections
    connect_regions(Regions.HC_GARDEN, world, [
        (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: True)
    ])

    ##Hyrule Castle Great Fairy Fountain
    # Locations
    add_locations(Regions.HC_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.HC_GREAT_FAIRY_REWARD, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])

    # Connections
    connect_regions(Regions.HC_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True)
    ])

    ##Hyrule Castle Storms Grotto
    # Locations
    add_locations(Regions.HC_STORMS_GROTTO, world, [
        (Locations.HC_GS_STORMS_GROTTO, lambda bundle: can_use(Items.BOOMERANG, bundle) and can_do_trick(Tricks.HC_STORMS_GS, bundle))
    ])

    # Connections
    connect_regions(Regions.HC_STORMS_GROTTO, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.HC_STORMS_GROTTO_BEHIND_WALLS, lambda bundle: can_break_mud_walls(bundle))
    ])

    ##Hyrule Castle Storms Grotto Behind Walls
    # Events
    add_events(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (EventLocations.HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_NUT_POT, Events.CAN_FARM_NUTS, lambda bundle: True),
        (EventLocations.HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_GOSSIP_STONE_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy(bundle)),
        (EventLocations.HYRULE_CASTLE_STORMS_GROTTO_BEHIND_WALLS_WANDERING_BUGS, Events.CAN_ACCESS_BUGS, lambda bundle: True)

    ])

    # Locations
    add_locations(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (Locations.HC_GS_STORMS_GROTTO, lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.HC_STORMS_GROTTO_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.HC_STORMS_GROTTO_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.HC_STORMS_GROTTO_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.HC_STORMS_GROTTO_POT4, lambda bundle: can_break_pots(bundle))
    ])

    # Connections
    connect_regions(Regions.HC_STORMS_GROTTO_BEHIND_WALLS, world, [
        (Regions.HC_STORMS_GROTTO, lambda bundle: True)
    ])

    ##Ganon's Castle Grounds
    # Events
    add_events(Regions.GANONS_CASTLE_GROUNDS, world, [
        (EventLocations.GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE, LocalEvents.GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE,
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
        (Regions.OGC_GREAT_FAIRY_FOUNTAIN, lambda bundle: can_use(Items.GOLDEN_GAUNTLETS) and at_night(bundle)),
        (Regions.GANONS_CASTLE_LEDGE, lambda bundle: has_item(LocalEvents.GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE, bundle))
    ])

    ##OGC Great Fairy Fountain
    # Locations
    add_locations(Regions.OGC_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.OGC_GREAT_FAIRY_REWARD, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])

    # Connections
    connect_regions(Regions.OGC_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.CASTLE_GROUNDS, lambda bundle: True)
    ])

    ##Castle Grounds from Ganon's Castle
    # Connections
    connect_regions(Regions.CASTLE_GROUNDS_FROM_GANONS_CASTLE, world, [
        (Regions.HYRULE_CASTLE_GROUNDS, lambda bundle: is_child(bundle)),
        (Regions.GANONS_CASTLE_GROUNDS, lambda bundle: is_adult(bundle))
    ])
    
    ##Ganon's Castle Ledge
    # Connections
    connect_regions(Regions.GANONS_CASTLE_LEDGE, world, [
        (Regions.GANONS_CASTLE_GROUNDS, lambda bundle: has_item(LocalEvents.GANONS_CASTLE_GROUNDS_BUILD_RAINBOW_BRIDGE, bundle)),
        (Regions.GANONS_TOWER_ENTRYWAY, lambda bundle: is_adult(bundle))
    ])
