from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(str, Enum):
    GANONS_CASTLE_FREE_FAIRIES = "Ganon's Castle Free Fairies"
    GANONS_CASTLE_FOREST_TRIAL_AREA = "Ganon's Castle Forest Trial Area"
    GANONS_CASTLE_FIRE_TRIAL_AREA = "Ganon's Castle Fire Trial Area"
    GANONS_CASTLE_WATER_TRIAL_AREA = "Ganon's Castle Water Trial Area"
    GANONS_CASTLE_SHADOW_TRIAL_AREA = "Ganon's Castle Shadow Trial Area"
    GANONS_CASTLE_SPIRIT_TRIAL_AREA = "Ganon's Castle Spirit Trial Area"
    GANONS_CASTLE_LIGHT_TRIAL_AREA = "Ganon's Castle Light Trial Area"
    GANONS_CASTLE_BLUE_FIRE_ACCESS = "Ganon's Castle Blue Fire Access"
    GANONS_CASTLE_FAIRY_POT = "Ganon's Castle Fairy Pot"
    GANON_DEFEATED = "Ganon Defeated"
    
class LocalEvents(str, Enum):
    GANONS_CASTLE_FOREST_TRIAL_CLEARED = "Ganon's Castle Forest Trial Cleared"
    GANONS_CASTLE_FIRE_TRIAL_CLEARED = "Ganon's Castle Fire Trial Cleared"
    GANONS_CASTLE_WATER_TRIAL_CLEARED = "Ganon's Castle Water Trial Cleared"
    GANONS_CASTLE_SHADOW_TRIAL_CLEARED = "Ganon's Castle Shadow Trial Cleared"
    GANONS_CASTLE_SPIRIT_TRIAL_CLEARED = "Ganon's Castle Spirit Trial Cleared"
    GANONS_CASTLE_LIGHT_TRIAL_CLEARED = "Ganon's Castle Light Trial Cleared"
    


def set_region_rules(world: "SohWorld") -> None:
    ## Ganon's Castle Entryway
    # Connections
    connect_regions(Regions.GANONS_CASTLE_ENTRYWAY, world, [
        (Regions.GANONS_CASTLE_LOBBY, lambda bundle: True),
        (Regions.CASTLE_GROUNDS_FROM_GANONS_CASTLE, lambda bundle: True)
    ])
    
    ## Ganon's Castle Lobby
    # Connections
    connect_regions(Regions.GANONS_CASTLE_LOBBY, world, [
        (Regions.GANONS_CASTLE_ENTRYWAY, lambda bundle: True),
        (Regions.GANONS_CASTLE_FOREST_TRIAL, lambda bundle: True),
        (Regions.GANONS_CASTLE_FIRE_TRIAL, lambda bundle: True),
        (Regions.GANONS_CASTLE_WATER_TRIAL, lambda bundle: True),
        (Regions.GANONS_CASTLE_SHADOW_TRIAL, lambda bundle: True),
        (Regions.GANONS_CASTLE_SPIRIT_TRIAL, lambda bundle: True),
        (Regions.GANONS_CASTLE_LIGHT_TRIAL, lambda bundle: can_use(Items.GOLDEN_GAUNTLETS, bundle)),
        (Regions.GANONS_TOWER_ENTRYWAY, lambda bundle: True),
        (Regions.GANONS_CASTLE_DEKU_SCRUBS, lambda bundle: (can_do_trick(Tricks.LENS_GANON) or
                                                            can_use(Items.LENS_OF_TRUTH, bundle))),
    ])
    ## Ganon's Castle Deku Scrubs
    # Events
    add_events(Regions.GANONS_CASTLE_DEKU_SCRUBS, world, [
        (EventLocations.GANONS_CASTLE_FREE_FAIRIES, Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_DEKU_SCRUBS, world, [
        (Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_LEFT, lambda bundle: can_stun_deku(bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_RIGHT, lambda bundle: can_stun_deku(bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_RIGHT, lambda bundle: can_stun_deku(bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_LEFT, lambda bundle: can_stun_deku(bundle)),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY1, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY2, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY3, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY4, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY5, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY6, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY7, lambda bundle: True),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY8, lambda bundle: True),
    ])
    ## Ganon's Castle Forest Trial
    # Events
    add_events(Regions.GANONS_CASTLE_FOREST_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_FOREST_TRIAL_AREA, LocalEvents.GANONS_CASTLE_FOREST_TRIAL_CLEARED, lambda bundle: (can_use(Items.LIGHT_ARROW, bundle) and
                                                                                                                         (can_use(Items.FIRE_ARROW, bundle) or
                                                                                                                          can_use(Items.DINS_FIRE, bundle))))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_FOREST_TRIAL, world, [
        (Locations.GANONS_CASTLE_FOREST_TRIAL_CHEST, lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Locations.GANONS_CASTLE_FOREST_TRIAL_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                    (can_use(Items.FIRE_ARROW, bundle) or
                                                                     (can_use(Items.DINS_FIRE, bundle) or
                                                                      can_use(Items.HOOKSHOT, bundle))))),
        (Locations.GANONS_CASTLE_FOREST_TRIAL_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                    (can_use(Items.FIRE_ARROW, bundle) or
                                                                     (can_use(Items.DINS_FIRE, bundle) or
                                                                      can_use(Items.HOOKSHOT, bundle))))),
    ])
    ## Ganon's Castle Fire Trial
    # Events
    add_events(Regions.GANONS_CASTLE_FIRE_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_FIRE_TRIAL_AREA, LocalEvents.GANONS_CASTLE_FIRE_TRIAL_CLEARED, lambda bundle: (can_use(Items.GORON_TUNIC, bundle) and
                                                                                                                     can_use(Items.GOLDEN_GAUNTLETS) and
                                                                                                                     can_use(Items.LIGHT_ARROW, bundle) and
                                                                                                                     can_use(Items.LONGSHOT, bundle)))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_FIRE_TRIAL, world, [
        (Locations.GANONS_CASTLE_FIRE_TRIAL_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                  can_use(Items.GORON_TUNIC, bundle) and 
                                                                  can_use(Items.GOLDEN_GAUNTLETS, bundle) and
                                                                  can_use(Items.LONGSHOT, bundle))),
        (Locations.GANONS_CASTLE_FIRE_TRIAL_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                  can_use(Items.GORON_TUNIC, bundle) and 
                                                                  can_use(Items.GOLDEN_GAUNTLETS, bundle) and
                                                                  can_use(Items.LONGSHOT, bundle))),
        (Locations.GANONS_CASTLE_FIRE_TRIAL_HEART, lambda bundle: can_use(Items.GORON_TUNIC, bundle))
    ])
    ## Ganon's Castle Water Trial
    # Events
    add_events(Regions.GANONS_CASTLE_WATER_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_BLUE_FIRE_ACCESS, Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: True),
        (EventLocations.GANONS_CASTLE_FAIRY_POT, Events.CAN_ACCESS_FAIRIES, lambda bundle: (blue_fire(bundle) and
                                                                                            can_kill_enemy(bundle, Enemies.FREEZARD))),
        (EventLocations.GANONS_CASTLE_WATER_TRIAL_AREA, LocalEvents.GANONS_CASTLE_WATER_TRIAL_CLEARED, lambda bundle: (blue_fire(bundle) and
                                                                                                                       is_adult(bundle) and 
                                                                                                                       can_use(Items.MEGATON_HAMMER, bundle) and
                                                                                                                       can_use(Items.LIGHT_ARROW, bundle)))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_WATER_TRIAL, world, [
        (Locations.GANONS_CASTLE_WATER_TRIAL_LEFT_CHEST, lambda bundle: True),
        (Locations.GANONS_CASTLE_WATER_TRIAL_RIGHT_CHEST, lambda bundle: True),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                   blue_fire(bundle) and
                                                                   is_adult(bundle) and
                                                                   can_use(Items.MEGATON_HAMMER, bundle))),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                   blue_fire(bundle) and
                                                                   is_adult(bundle) and
                                                                   can_use(Items.MEGATON_HAMMER, bundle))),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT3, lambda bundle: (can_break_pots(bundle) and
                                                                   blue_fire(bundle) and
                                                                   is_adult(bundle) and
                                                                   can_use(Items.MEGATON_HAMMER, bundle)))
    ])
    ## Ganon's Castle Shadow Trial
    # Events
    add_events(Regions.GANONS_CASTLE_SHADOW_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_SHADOW_TRIAL_AREA, LocalEvents.GANONS_CASTLE_SHADOW_TRIAL_CLEARED, lambda bundle: (can_use(Items.FIRE_ARROW, bundle) or
                                                                                                                         can_use(Items.HOOKSHOT, bundle) or
                                                                                                                         can_use(Items.HOVER_BOOTS, bundle) or
                                                                                                                         (can_do_trick(Tricks.LENS_GANON, bundle) or
                                                                                                                          can_use(Items.LENS_OF_TRUTH, bundle) or
                                                                                                                          (can_use(Items.LONGSHOT, bundle) and
                                                                                                                           (can_use(Items.HOVER_BOOTS, bundle) or
                                                                                                                            (can_use(Items.DINS_FIRE, bundle) and
                                                                                                                             (can_do_trick(Tricks.LENS_GANON, bundle) or
                                                                                                                              can_use(Items.LENS_OF_TRUTH, bundle))))))))
    ])
    # Locations
    
    ## Ganon's Castle Spirit Trial
    ## Ganon's Castle Light Trial
    ## Ganon's Tower Entryway
    ## Ganon's Tower Floor 1
    ## Ganon's Tower Floor 2
    ## Ganon's Tower Floor 3
    ## Ganon's Tower Before Ganondorf's Lair
    ## Ganondorf's Lair
    ## Ganon's Castle Escape
    ## Ganon's Arena
    
    # TODO: Temporary to test generation
    connect_regions(Regions.KOKIRI_FOREST, world, [
        (Regions.GANONS_ARENA, lambda bundle: True)
    ])
    connect_regions(Regions.GANONS_ARENA, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])
    add_events(Regions.GANONS_ARENA, world, [
        (EventLocations.GANON_DEFEATED, Events.GAME_COMPLETED, lambda bundle: 
         (can_use(Items.LIGHT_ARROW, bundle) and can_use(Items.MASTER_SWORD, bundle)
          and not world.options.triforce_hunt)
         or has_item(Events.GAME_COMPLETED, bundle))
    ])
