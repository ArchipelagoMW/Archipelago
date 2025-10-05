from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld
    
class EventLocations(str, Enum):
    FOREST_TEMPLE_MEG = "Forest Temple Meg"
    FOREST_TEMPLE_JOELLE = "Forest Temple Joelle"
    FOREST_TEMPLE_AMY = "Forest Temple Amy"
    FOREST_TEMPLE_BETH = "Forest Temple Beth"
    FOREST_TEMPLE_LOWER_STALFOS_FAIRY_POT = "Forest Temple Lower Stalfos Fairy Pot"
    FOREST_TEMPLE_STICKS = "Forest Temple Stick"
    FOREST_TEMPLE_NUTS = "Forest Temple Nuts"

class LocalEvents(str, Enum):
    DEFEATED_MEG = "Defeated Meg"
    DEFEATED_JOELLE = "Defeated Joelle"
    DEFEATED_AMY = "Defeated Amy"
    DEFEATED_BETH = "Defeated Beth"
    LOWER_STALFOS_FAIRY = "Got Lower Stalfos Fairy"
    

def set_region_rules(world: "SohWorld") -> None:
    ## Forest Temple Entryway
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_ENTRYWAY, world, [
        # Todo: Change this when we have IsVanilla vs. IsMQ
        (Regions.FOREST_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: True)
    ])
    
    ## Forest Temple First Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_FIRST_ROOM, world, [
        (Locations.FOREST_TEMPLE_FIRST_ROOM_CHEST, lambda bundle: True),
        (Locations.FOREST_TEMPLE_GS_FIRST_ROOM, lambda bundle: ((is_adult(bundle) and can_use(Items.BOMB_BAG, bundle)) or
                                                                can_use(Items.FAIRY_BOW, bundle) or
                                                                can_use(Items.HOOKSHOT, bundle) or
                                                                can_use(Items.BOOMERANG, bundle) or
                                                                can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                                can_use(Items.BOMBCHUS_5, bundle) or
                                                                can_use(Items.DINS_FIRE, bundle) or
                                                                (can_do_trick(Tricks.FOREST_FIRST_GS) and (can_jump_slash_except_hammer(bundle) or (is_child(bundle) and can_use(Items.BOMB_BAG, bundle)))))),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_FIRST_ROOM, world, [
        (Regions.FOREST_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, lambda bundle: True)
    ])
    
    ## Forest Temple South Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: (can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)))
    ])
    
    ## Foest Temple Lobby
    # Events
    add_events(Regions.FOREST_TEMPLE_LOBBY, world, [
        (EventLocations.FOREST_TEMPLE_MEG, LocalEvents.SPAWN_MEG, lambda bundle: (has_item(LocalEvents.DEFEATED_JOELLE, bundle) and
                                                                                  has_item(LocalEvents.DEFEATED_BETH, bundle) and
                                                                                  has_item(LocalEvents.DEFEATED_AMY, bundle) and
                                                                                  can_kill_enemy(bundle, Enemies.MEG)))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_LOBBY, world, [
        (Locations.FOREST_TEMPLE_GS_LOBBY, lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT4, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT5, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT6, lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_LOBBY, world, [
        (Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NORTH_CORRIDOR, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, lambda bundle: (can_use(Items.SONG_OF_TIME, bundle) or is_child(bundle))),
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, lambda bundle: (can_use(Items.FAIRY_BOW, bundle) or can_use(Items.FAIRY_SLINGSHOT, bundle))),
        (Regions.FOREST_TEMPLE_WEST_CORRIDOR, lambda bundle: (small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 1, bundle))),
        (Regions.FOREST_TEMPLE_EAST_CORRIDOR, lambda bundle: False),
        (Regions.FOREST_TEMPLE_BOSS_REGION, lambda bundle: has_item(LocalEvents.CAN_SPAWN_MEG, bundle)),
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False)
    ])
    
    ## Forest Temple North Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NORTH_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_LOWER_STALFOS, lambda bundle: True)
    ])
    
    ## Forest Temple Lower Stalfos
    # Events
    add_events(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (EventLocations.FOREST_TEMPLE_LOWER_STALFOS_FAIRY_POT, LocalEvents.LOWER_STALFOS_FAIRY, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (Locations.FOREST_TEMPLE_FIRST_STALFOS_CHEST, lambda bundle: (can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2))),
        (Locations.FOREST_TEMPLE_LOWER_STALFOS_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOWER_STALFOS_POT2, lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (Regions.FOREST_TEMPLE_NORTH_CORRIDOR, lambda bundle: True)
    ])
    
    ## Forest Temple NW Outdoors Lower
    # Events
    add_events(Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, world, [
        (EventLocations.FOREST_TEMPLE_STICKS, Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.FOREST_TEMPLE_NUTS, Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, world, [
        (Locations.FOREST_TEMPLE_GS_LEVEL_ISLAND_COURTYARD, lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Locations.FOREST_TEMPLE_WEST_COURTYARD_RIGHT_HEART, lambda bundle: (can_use(Items.BOOMERANG, bundle) and 
                                                                             can_do_trick(Tricks.FOREST_OUTDOORS_HEARTS_BOOMERANG, bundle))),
        (Locations.FOREST_TEMPLE_WEST_COURTYARD_LEFT_HEART, lambda bundle: (can_use(Items.BOOMERANG, bundle) and 
                                                                            can_do_trick(Tricks.FOREST_OUTDOORS_HEARTS_BOOMERANG, bundle)))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: can_use(Items.SONG_OF_TIME, bundle)),
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, lambda bundle: (can_do_trick(Tricks.HOVER_BOOST_SIMPLE, bundle) and
                                                                  can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and
                                                                  has_explosives(bundle) and
                                                                  can_use(Items.HOVER_BOOTS, bundle))),
        (Regions.FOREST_TEMPLE_MAP_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_SEWER, lambda bundle: (has_item(Items.GOLDEN_SCALE, bundle) or
                                                      can_use(Items.IRON_BOOTS, bundle))),
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False)
    ])
    
    ## Forest Temple NW Outdoors Upper
    # Events
    # Locations
    # Connections
    
    
