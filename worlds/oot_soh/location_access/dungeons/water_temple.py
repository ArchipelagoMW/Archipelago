from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld
    
class EventLocations(str, Enum):
    WATER_TEMPLE_EAST_LOWER = "Water Temple East Lower"
    
class LocalEvents(str, Enum):
    WATER_TEMPLE_WATER_LOW_FROM_HIGH = "Water Temple Water Low From High"
    WATER_TEMPLE_WATER_MIDDLE = "Water Temple Water Middle"
    WATER_TEMPLE_WATER_HIGH = "Water Temple Water High"


def set_region_rules(world: "SohWorld") -> None:
    ## Water Temple Entryway
    # Connections
    connect_regions(Regions.WATER_TEMPLE_ENTRYWAY, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: (has_item(Items.BRONZE_SCALE))),
        (Regions.LH_FROM_WATER_TEMPLE, lambda bundle: True)
    ])
    
    ## Water Temple Lobby
    # Locations
    add_locations(Regions.WATER_TEMPLE_LOBBY, world, [
        (Locations.WATER_TEMPLE_MAIN_LEVEL2_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                  (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                                   has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle) or
                                                                   (can_use(Items.IRON_BOOTS, bundle) and
                                                                    can_use(Items.HOOKSHOT, bundle))))),
        (Locations.WATER_TEMPLE_MAIN_LEVEL2_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                  (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                                   has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle) or
                                                                   (can_use(Items.IRON_BOOTS, bundle) and
                                                                    can_use(Items.HOOKSHOT, bundle))))),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_LOBBY, world, [
        (Regions.WATER_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.WATER_TEMPLE_EAST_LOWER, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                          ((can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                            can_use(Items.ZORA_TUNIC, bundle)) and
                                                           (can_use(Items.IRON_BOOTS, bundle) or
                                                            (can_use(Items.LONGSHOT, bundle) and
                                                             can_do_trick(Tricks.WATER_LONGSHOT_TORCH, bundle)))))),
        (Regions.WATER_TEMPLE_NORTH_LOWER, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                           ((can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                             can_use(Items.ZORA_TUNIC, bundle)) and
                                                            can_use(Items.IRON_BOOTS, bundle)))),
        (Regions.WATER_TEMPLE_SOUTH_LOWER, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) and
                                                           has_explosives(bundle) and
                                                           (has_item(Items.SILVER_SCALE, bundle) or
                                                            can_use(Items.IRON_BOOTS, bundle)) and
                                                           (can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS) or
                                                            can_use(Items.ZORA_TUNIC, bundle)))),
        (Regions.WATER_TEMPLE_WEST_LOWER, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) and
                                                          has_item(Items.GORONS_BRACELET, bundle) and
                                                          (is_child(bundle) or
                                                           has_item(Items.SILVER_SCALE, bundle) or
                                                           can_use(Items.IRON_BOOTS, bundle)) and
                                                          (can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                           can_use(Items.ZORA_TUNIC, bundle)))),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_LOWER, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) and
                                                                    small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle))),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER, lambda bundle: ((has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                                    has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle)) and
                                                                    (has_fire_source_with_torch(bundle) or
                                                                     can_use(Items.FAIRY_BOW, bundle)))),
        (Regions.WATER_TEMPLE_EAST_MIDDLE, lambda bundle: ((has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                            has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle) or
                                                            (can_use(Items.IRON_BOOTS, bundle) and
                                                             water_timer(bundle) >= 16)) and
                                                           can_use(Items.LONGSHOT, bundle))),
        (Regions.WATER_TEMPLE_WEST_MIDDLE, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle))),
        (Regions.WATER_TEMPLE_HIGH_WATER, lambda bundle: (is_adult(bundle) and
                                                          (can_use(Items.HOVER_BOOTS, bundle) or
                                                           can_do_trick(Tricks.DAMAGE_BOOST, bundle) and
                                                           can_use(Items.BOMB_BAG, bundle) and
                                                           take_damage(bundle)))),
        (Regions.WATER_TEMPLE_BLOCK_CORRIDOR, lambda bundle: ((has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                               has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle)) and
                                                              (can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                               can_use(Items.FAIRY_BOW, bundle)) and 
                                                              can_use(Items.LONGSHOT, bundle) or
                                                              can_use(Items.HOVER_BOOTS, bundle) or
                                                              can_do_trick(Tricks.WATER_CENTRAL_BOW, bundle) and
                                                              (is_adult(bundle) or 
                                                               has_item(LocalEvents.WATER_TEMPLE_WATER_MIDDLE, bundle)))),
        (Regions.WATER_TEMPLE_FALLING_PLATFORM_ROOM, lambda bundle: (has_item(LocalEvents.WATER_TEMPLE_WATER_HIGH, bundle) and
                                                                     small_keys(Items.WATER_TEMPLE_SMALL_KEY, 4))),
        (Regions.WATER_TEMPLE_PRE_BOSS_ROOM, lambda bundle: ((has_item(LocalEvents.WATER_TEMPLE_WATER_HIGH, bundle) and
                                                              can_use(Items.LONGSHOT, bundle)) or
                                                             (can_do_trick(Tricks.HOVER_BOOST_SIMPLE, bundle) and
                                                              can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and 
                                                              has_explosives(bundle) and
                                                              can_use(Items.HOVER_BOOTS, bundle))))
    ])
    
    ## Water Temple East Lower
    # Events
    add_events(Regions.WATER_TEMPLE_EAST_LOWER, world, [
        (EventLocations.WATER_TEMPLE_EAST_LOWER, LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_EAST_LOWER, world, [
        (Locations.WATER_TEMPLE_TORCH_POT1, lambda bundle: (can_break_pots(bundle) and
                                                            (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                             (can_use(Items.HOOKSHOT, bundle) and
                                                              can_use(Items.IRON_BOOTS, bundle))))),
         (Locations.WATER_TEMPLE_TORCH_POT2, lambda bundle: (can_break_pots(bundle) and
                                                            (has_item(LocalEvents.WATER_TEMPLE_WATER_LOW_FROM_HIGH, bundle) or
                                                             (can_use(Items.HOOKSHOT, bundle) and
                                                              can_use(Items.IRON_BOOTS, bundle)))))
    ])
    # Connections
    
