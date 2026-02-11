from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    MARKET_GUARD_HOUSE = "Market Guard House"
    MARKET_MASK_SHOP_MASKS = "Market Mask Shop Masks"
    MARKET_MASK_SHOP_SKULL_MASK = "Market Mask Shop Skull Mask"
    MARKET_MASK_SHOP_SPOOKY_MASK = "Market Mask Shop Spooky Mask"
    MARKET_MASK_SHOP_BUNNY_HOOD = "Market Mask Shop Bunny Hood"
    MARKET_MASK_SHOP_MASK_OF_TRUTH = "Market Mask Shop Mask of Truth"
    MARKET_BOMBCHU_BOWLING_GAME = "Market Bombchu Bowling Game"


def set_region_rules(world: "SohWorld") -> None:
    # Market Entrance
    # Connections
    connect_regions(Regions.MARKET_ENTRANCE, world, [
        (Regions.HYRULE_FIELD, lambda bundle: (
            is_adult(bundle) or at_day(bundle))),
        (Regions.MARKET, lambda bundle: True),
        (Regions.MARKET_GUARD_HOUSE, lambda bundle: can_open_overworld_door(
            Items.GUARD_HOUSE_KEY, bundle))
    ])

    # Market
    # Locations
    add_locations(Regions.MARKET, world, [
        (Locations.MARKET_MARKET_GRASS1, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS2, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS3, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS4, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS5, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS6, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS7, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_MARKET_GRASS8, lambda bundle: (is_child(bundle) and (
            can_use_sword(bundle) or has_item(Items.GORONS_BRACELET, bundle)))),
        (Locations.MARKET_NEAR_BAZAAR_CRATE1, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_NEAR_BAZAAR_CRATE2, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_SHOOTING_GALLERY_CRATE1,
         lambda bundle: (is_child(bundle))),
        (Locations.MARKET_SHOOTING_GALLERY_CRATE2,
         lambda bundle: (is_child(bundle))),
        (Locations.MARKET_TREE, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET, world, [
        (Regions.MARKET_ENTRANCE, lambda bundle: True),
        (Regions.TOT_ENTRANCE, lambda bundle: True),
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.MARKET_BAZAAR, lambda bundle: (is_child(bundle) and at_day(
            bundle) and can_open_overworld_door(Items.MARKET_BAZAAR_KEY, bundle))),
        (Regions.MARKET_MASK_SHOP, lambda bundle: (is_child(bundle) and at_day(
            bundle) and can_open_overworld_door(Items.MASK_SHOP_KEY, bundle))),
        (Regions.MARKET_SHOOTING_GALLERY, lambda bundle: (is_child(bundle) and at_day(
            bundle) and can_open_overworld_door(Items.MARKET_SHOOTING_GALLERY_KEY, bundle))),
        (Regions.MARKET_BOMBCHU_BOWLING, lambda bundle: (is_child(bundle)
         and can_open_overworld_door(Items.BOMBCHU_BOWLING_KEY, bundle))),
        (Regions.MARKET_TREASURE_CHEST_GAME, lambda bundle: (is_child(bundle) and at_night(
            bundle) and can_open_overworld_door(Items.TREASURE_CHEST_GAME_BUILDING_KEY, bundle))),
        (Regions.MARKET_POTION_SHOP, lambda bundle: (is_child(bundle) and at_day(
            bundle) and can_open_overworld_door(Items.MARKET_POTION_SHOP_KEY, bundle))),
        (Regions.MARKET_BACK_ALLEY, lambda bundle: is_child(bundle))
    ])

    # Market Back Alley
    # Connections
    connect_regions(Regions.MARKET_BACK_ALLEY, world, [
        (Regions.MARKET, lambda bundle: True),
        (Regions.MARKET_BOMBCHU_SHOP, lambda bundle: (at_night(bundle)
         and can_open_overworld_door(Items.BOMBCHU_SHOP_KEY, bundle))),
        (Regions.MARKET_DOG_LADY_HOUSE, lambda bundle: (
            can_open_overworld_door(Items.RICHARDS_HOUSE_KEY, bundle))),
        (Regions.MARKET_MAN_IN_GREEN_HOUSE, lambda bundle: (at_night(bundle)
         and can_open_overworld_door(Items.ALLEY_HOUSE_KEY, bundle)))
    ])

    # Market Guard House
    # Events
    add_events(Regions.MARKET_GUARD_HOUSE, world, [
        (EventLocations.MARKET_GUARD_HOUSE,
         Events.CAN_EMPTY_BIG_POES, lambda bundle: (is_adult(bundle)))
    ])
    # Locations
    add_locations(Regions.MARKET_GUARD_HOUSE, world, [
        (Locations.MARKET_10_BIG_POES, lambda bundle: (is_adult(bundle) and
                                                       ((has_bottle(bundle) and
                                                        has_item(Events.CAN_DEFEAT_BIG_POE, bundle)) or
                                                       has_item(Items.BOTTLE_WITH_BIG_POE, bundle, world.options.big_poe_target_count.value)))),
        (Locations.MARKET_MARKET_GS_GUARD_HOUSE, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT1, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT2, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT3, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT4, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT5, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT6, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT7, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT8, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT9, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT10, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT11, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT12, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT13, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT14, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT15, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT16, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT17, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT18, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT19, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT20, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT21, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT22, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT23, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT24, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT25, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT26, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT27, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT28, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT29, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT30, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT31, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT32, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT33, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT34, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT35, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT36, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT37, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT38, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT39, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT40, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT41, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT42, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT43, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT44, lambda bundle: (
            is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT1, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT2, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT3, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT4, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT5, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT6, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT7, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT8, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT9, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT10, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT11, lambda bundle: (
            is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE1, lambda bundle: (
            is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE2, lambda bundle: (
            is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE3, lambda bundle: (
            is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE4, lambda bundle: (
            is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE5, lambda bundle: (
            is_child(bundle) and can_break_crates(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_GUARD_HOUSE, world, [
        (Regions.MARKET_ENTRANCE, lambda bundle: True)
    ])

    # Market Bazaar
    # Locations
    add_locations(Regions.MARKET_BAZAAR, world, [
        (Locations.MARKET_BAZAAR_ITEM1, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM2, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM3, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM4, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM5, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM6, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM7, lambda bundle: True),
        (Locations.MARKET_BAZAAR_ITEM8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.MARKET_BAZAAR, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Mask Shop
    # Events
    add_events(Regions.MARKET_MASK_SHOP, world, [
        (EventLocations.MARKET_MASK_SHOP_MASKS, Events.CAN_BORROW_MASKS, lambda bundle: (
            has_item(Items.ZELDAS_LETTER, bundle) and has_item(Events.KAKARIKO_GATE_OPEN, bundle))),
        (EventLocations.MARKET_MASK_SHOP_SKULL_MASK, Events.CAN_BORROW_SKULL_MASK, lambda bundle: has_item(Events.CAN_BORROW_MASKS, bundle) and (bool(world.options.complete_mask_quest) or
                                                                                                                                                 has_item(Events.SOLD_KEATON_MASK, bundle))),
        (EventLocations.MARKET_MASK_SHOP_SPOOKY_MASK, Events.CAN_BORROW_SPOOKY_MASK, lambda bundle: has_item(Events.CAN_BORROW_MASKS, bundle) and (bool(world.options.complete_mask_quest) or
                                                                                                                                                   has_item(Events.SOLD_SKULL_MASK, bundle))),
        (EventLocations.MARKET_MASK_SHOP_BUNNY_HOOD, Events.CAN_BORROW_BUNNY_HOOD, lambda bundle: has_item(Events.CAN_BORROW_MASKS, bundle) and (bool(world.options.complete_mask_quest) or
                                                                                                                                                 has_item(Events.SOLD_SPOOKY_MASK, bundle))),
        (EventLocations.MARKET_MASK_SHOP_MASK_OF_TRUTH, Events.CAN_BORROW_MASK_OF_TRUTH, lambda bundle: has_item(Events.CAN_BORROW_MASKS, bundle) and (bool(world.options.complete_mask_quest) or
                                                                                                                                                       has_item(Events.SOLD_BUNNY_HOOD, bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_MASK_SHOP, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Shooting Gallery
    # Locations
    add_locations(Regions.MARKET_SHOOTING_GALLERY, world, [
        (Locations.MARKET_SHOOTING_GALLERY, lambda bundle: (
            is_child(bundle) and has_item(Items.CHILD_WALLET, bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_SHOOTING_GALLERY, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Bombchu Bowling
    # Events
    add_events(Regions.MARKET_BOMBCHU_BOWLING, world, [
        (EventLocations.MARKET_BOMBCHU_BOWLING_GAME, Events.COULD_PLAY_BOWLING,
         lambda bundle: has_item(Items.CHILD_WALLET, bundle) and bombchus_enabled(bundle))
    ])
    # Locations
    add_locations(Regions.MARKET_BOMBCHU_BOWLING, world, [
        (Locations.MARKET_BOMBCHU_BOWLING_FIRST_PRIZE, lambda bundle: (
            has_item(Events.COULD_PLAY_BOWLING, bundle))),
        (Locations.MARKET_BOMBCHU_BOWLING_SECOND_PRIZE, lambda bundle: (
            has_item(Events.COULD_PLAY_BOWLING, bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_BOMBCHU_BOWLING, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Potion Shop
    # Locations
    add_locations(Regions.MARKET_POTION_SHOP, world, [
        (Locations.MARKET_POTION_SHOP_ITEM1, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM2, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM3, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM4, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM5, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM6, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM7, lambda bundle: True),
        (Locations.MARKET_POTION_SHOP_ITEM8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.MARKET_POTION_SHOP, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Treasure Chest Game
    # Locations
    add_locations(Regions.MARKET_TREASURE_CHEST_GAME, world, [
        (Locations.MARKET_TREASURE_CHEST_GAME_REWARD, lambda bundle: (has_item(Items.CHILD_WALLET, bundle) and
                                                                      can_use(Items.LENS_OF_TRUTH, bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_TREASURE_CHEST_GAME, world, [
        (Regions.MARKET, lambda bundle: True)
    ])

    # Market Bombchu Shop
    # Locations
    add_locations(Regions.MARKET_BOMBCHU_SHOP, world, [
        (Locations.MARKET_BOMBCHU_SHOP_ITEM1, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM2, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM3, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM4, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM5, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM6, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM7, lambda bundle: True),
        (Locations.MARKET_BOMBCHU_SHOP_ITEM8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.MARKET_BOMBCHU_SHOP, world, [
        (Regions.MARKET_BACK_ALLEY, lambda bundle: True)
    ])

    # Market Dog Lady House
    # Locations
    add_locations(Regions.MARKET_DOG_LADY_HOUSE, world, [
        (Locations.MARKET_LOST_DOG, lambda bundle: (
            is_child(bundle) and at_night(bundle))),
        (Locations.MARKET_LOST_DOG_HOUSE_CRATE,
         lambda bundle: (can_break_crates(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_DOG_LADY_HOUSE, world, [
        (Regions.MARKET_BACK_ALLEY, lambda bundle: True)
    ])

    # Market Man in Green House
    # Locations
    add_locations(Regions.MARKET_MAN_IN_GREEN_HOUSE, world, [
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT1,
         lambda bundle: (can_break_pots(bundle))),
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT2,
         lambda bundle: (can_break_pots(bundle))),
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT3,
         lambda bundle: (can_break_pots(bundle))),
    ])
    # Connections
    connect_regions(Regions.MARKET_MAN_IN_GREEN_HOUSE, world, [
        (Regions.MARKET_BACK_ALLEY, lambda bundle: True)
    ])
