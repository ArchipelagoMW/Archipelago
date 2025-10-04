from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld
    
class EventLocations(str, Enum):
    MARKET_GUARD_HOUSE = "Market Guard House"
    MARKET_MASK_SHOP = "Market Mask Shop"
    MARKET_BOMBCHU_BOWLING = "Market Bombchu Bowling"


class LocalEvents(str, Enum):
    CAN_EMPTY_BIG_POES = "Can Empty Big Poes"
    CAN_BORROW_MASKS = "Retrieved Zelda's Letter and Opened Kakariko Gate"
    BORROW_SKULL_MASK = "Borrow Skull Mask"
    BORROW_SPOOKY_MASK = "Borrow Spooky Mask"
    BORROW_BUNNY_HOOD = "Borrow Bunny Hood"
    BORROW_RIGHT_MASKS = "Borrow Any Right Mask"
    CAN_PLAY_BOWLING = "Can Play Bombchu Bowling"


def set_region_rules(world: "SohWorld") -> None:
    ## Market Entrance
    # Connections
    connect_regions(Regions.MARKET_ENTRANCE, world, [
        (Regions.HYRULE_FIELD, lambda bundle: (is_adult(bundle) or at_day(bundle))),
        (Regions.MARKET, lambda bundle: True),
        (Regions.MARKET_GUARD_HOUSE, lambda bundle: can_open_overworld_door(Items.GUARD_HOUSE_KEY))
    ])
    
    ## Market
    # Locations
    add_locations(Regions.MARKET, world, [
        (Locations.MARKET_MARKET_GRASS1, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS2, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS3, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS4, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS5, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS6, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS7, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        (Locations.MARKET_MARKET_GRASS8, lambda bundle: (is_child(bundle) and (can_use_sword(bundle) or has_item(Items.GORONS_BRACELET)))),
        # Todo: The crates has 'logic->CanRoll()' outcommanted in SoH. Do we need those and when?
        (Locations.MARKET_NEAR_BAZAAR_CRATE1, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_NEAR_BAZAAR_CRATE2, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_SHOOTING_GALLERY_CRATE1, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_SHOOTING_GALLERY_CRATE2, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_TREE, lambda bundle: (is_child(bundle) and can_bonk_trees(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET, world, [
        (Regions.MARKET_ENTRANCE, lambda bundle: True),
        (Regions.TOT_ENTRANCE, lambda bundle: True),
        (Regions.CASTLE_GROUNDS, lambda bundle: True),
        (Regions.MARKET_BAZAAR, lambda bundle: (is_child(bundle) and at_day(bundle) and can_open_overworld_door(Items.MARKET_BAZAAR_KEY))),
        (Regions.MARKET_MASK_SHOP, lambda bundle: (is_child(bundle) and at_day(bundle) and can_open_overworld_door(Items.MASK_SHOP_KEY))),
        (Regions.MARKET_SHOOTING_GALLERY, lambda bundle: (is_child(bundle) and at_day(bundle) and can_open_overworld_door(Items.MARKET_SHOOTING_GALLERY_KEY))),
        (Regions.MARKET_BOMBCHU_BOWLING, lambda bundle: (is_child(bundle) and can_open_overworld_door(Items.BOMBCHU_BOWLING_KEY))),
        (Regions.MARKET_TREASURE_CHEST_GAME, lambda bundle: (is_child(bundle) and at_night(bundle) and can_open_overworld_door(Items.TREASURE_CHEST_GAME_BUILDING_KEY))),
        (Regions.MARKET_POTION_SHOP, lambda bundle: (is_child(bundle) and at_day(bundle) and can_open_overworld_door(Items.MARKET_POTION_SHOP_KEY))),
        (Regions.MARKET_BACK_ALLEY, lambda bundle: is_child(bundle))
    ])
    
    ## Market Back Alley
    # Connections
    connect_regions(Regions.MARKET_BACK_ALLEY, world, [
        (Regions.MARKET, lambda bundle: True),
        (Regions.MARKET_BOMBCHU_SHOP, lambda bundle: (at_night(bundle) and can_open_overworld_door(Items.BOMBCHU_SHOP_KEY))),
        (Regions.MARKET_DOG_LADY_HOUSE, lambda bundle: (can_open_overworld_door(Items.RICHARDS_HOUSE_KEY))),
        (Regions.MARKET_MAN_IN_GREEN_HOUSE, lambda bundle: (at_night(bundle) and can_open_overworld_door(Items.ALLEY_HOUSE_KEY)))
    ])
    
    ## Market Guard House
    # Events
    add_events(Regions.MARKET_GUARD_HOUSE, world, [
        (EventLocations.MARKET_GUARD_HOUSE, LocalEvents.CAN_EMPTY_BIG_POES, lambda bundle: (is_adult(bundle)))
    ])
    # Locations
    add_locations(Regions.MARKET_GUARD_HOUSE, world, [
        # Todo: Can't decide how big poe should be handled
        #(Locations.MARKET_10_BIG_POES, lambda bundle: (is_adult(bundle) and (can_kill_enemy(Enemies.BIG_POE) || has_item(Items.BOTTLE_WITH_BIG_POE, bundle, world.options.big_poe_target_count.value)))),
        (Locations.MARKET_MARKET_GS_GUARD_HOUSE, lambda bundle: (is_child(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT1, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT2, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT3, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT4, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT5, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT6, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT7, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT8, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT9, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT10, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT11, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT12, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT13, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT14, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT15, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT16, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT17, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT18, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT19, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT20, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT21, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT22, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT23, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT24, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT25, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT26, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT27, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT28, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT29, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT30, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT31, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT32, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT33, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT34, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT35, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT36, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT37, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT38, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT39, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT40, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT41, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT42, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT43, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CHILD_POT44, lambda bundle: (is_child(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT1, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT2, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT3, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT4, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT5, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT6, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT7, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT8, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT9, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT10, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_ADULT_POT11, lambda bundle: (is_adult(bundle) and can_break_pots(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE1, lambda bundle: (is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE2, lambda bundle: (is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE3, lambda bundle: (is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE4, lambda bundle: (is_child(bundle) and can_break_crates(bundle))),
        (Locations.MARKET_GUARD_HOUSE_CRATE5, lambda bundle: (is_child(bundle) and can_break_crates(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_GUARD_HOUSE, world, [
        (Regions.MARKET_ENTRANCE, lambda bundle: True)
    ])
    
    ## Market Bazaar
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
    
    ## Market Mask Shop
    # Events
    add_events(Regions.MARKET_MASK_SHOP, world, [
        # Todo: Is this accurate?
        (EventLocations.MARKET_MASK_SHOP, LocalEvents.CAN_BORROW_MASKS, lambda bundle: (has_item(Items.ZELDAS_LETTER) and world.options.kakariko_gate.value))
        (EventLocations.MARKET_MASK_SHOP, LocalEvents.BORROW_SKULL_MASK, lambda bundle: (world.options.complete_mask_quest.value and LocalEvents.CAN_BORROW_MASKS)),
        (EventLocations.MARKET_MASK_SHOP, LocalEvents.BORROW_SPOOKY_MASK, lambda bundle: (world.options.complete_mask_quest.value and LocalEvents.CAN_BORROW_MASKS)),
        (EventLocations.MARKET_MASK_SHOP, LocalEvents.BORROW_BUNNY_HOOD, lambda bundle: (world.options.complete_mask_quest.value and LocalEvents.CAN_BORROW_MASKS)),
        (EventLocations.MARKET_MASK_SHOP, LocalEvents.BORROW_RIGHT_MASKS, lambda bundle: (world.options.complete_mask_quest.value and LocalEvents.CAN_BORROW_MASKS)),
    ])
    # Locations
    add_locations(Regions.MARKET_MASK_SHOP, world, [
        (Locations.MARKET_MASK_SHOP_HINT, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.MARKET_BAZAAR, world, [
        (Regions.MARKET, lambda bundle: True)
    ])
    
    ## Market Shooting Gallery
    # Locations
    add_locations(Regions.MARKET_SHOOTING_GALLERY, world, [
        (Locations.MARKET_SHOOTING_GALLERY, lambda bundle: (is_child(bundle) and has_item(Items.CHILD_WALLET)))
    ])
    # Connections
    connect_regions(Regions.MARKET_SHOOTING_GALLERY, world, [
        (Regions.MARKET, lambda bundle: True)
    ])
    
    ## Market Bombchu Bowling
    # Events
    add_events(Regions.MARKET_BOMBCHU_BOWLING, world, [
        (EventLocations.MARKET_BOMBCHU_BOWLING, LocalEvents.CAN_PLAY_BOWLING, lambda bundle: (has_item(Items.CHILD_WALLET)))
    ])
    # Locations
    add_locations(Regions.MARKET_BOMBCHU_BOWLING, world, [
        # Todo: Ship has logic->BombchusEnabled() here. Do we have an equivalent?
        (Locations.MARKET_BOMBCHU_BOWLING_FIRST_PRIZE, lambda bundle: (LocalEvents.CAN_PLAY_BOWLING))
        (Locations.MARKET_BOMBCHU_BOWLING_SECOND_PRIZE, lambda bundle: (LocalEvents.CAN_PLAY_BOWLING))
    ])
    # Connections
    connect_regions(Regions.MARKET_BOMBCHU_BOWLING, world, [
        (Regions.MARKET, lambda bundle: True)
    ])
    
    ## Market Potion Shop
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
    
    ## Market Treasure Chest Game
    # Locations
    add_locations(Regions.MARKET_TREASURE_CHEST_GAME, world, [
        (Locations.MARKET_GREG_HINT, lambda bundle: (has_item(Items.CHILD_WALLET))),
        # Todo: Missing 'shuffle_chest_minigame' option. Are we also missing 'logic->SmallKeys(SCENE_TREASURE_BOX_SHOP)
        # Example from Ship:
        # LOCATION(RC_MARKET_TREASURE_CHEST_GAME_KEY_1,  logic->HasItem(RG_CHILD_WALLET) && ((ctx->GetOption(RSK_SHUFFLE_CHEST_MINIGAME).Is(RO_CHEST_GAME_SINGLE_KEYS) && logic->SmallKeys(SCENE_TREASURE_BOX_SHOP, 1)) || (ctx->GetOption(RSK_SHUFFLE_CHEST_MINIGAME).Is(RO_CHEST_GAME_PACK) && logic->SmallKeys(SCENE_TREASURE_BOX_SHOP, 1)) || (logic->CanUse(RG_LENS_OF_TRUTH) && !ctx->GetOption(RSK_SHUFFLE_CHEST_MINIGAME)))),
    ])
    # Connections
    connect_regions(Regions.MARKET_POTION_SHOP, world, [
        (Regions.MARKET, lambda bundle: True)
    ])
    
    ## Market Bombchu Shop
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
    
    ## Market Dog Lady House
    # Locations
    add_locations(Regions.MARKET_DOG_LADY_HOUSE, world, [
        (Locations.MARKET_LOST_DOG, lambda bundle: (is_child(bundle) and at_night(bundle))),
        (Locations.MARKET_LOST_DOG_HOUSE_CRATE, lambda bundle: (can_break_crates(bundle)))
    ])
    # Connections
    connect_regions(Regions.MARKET_DOG_LADY_HOUSE, world, [
        (Regions.MARKET_BACK_ALLEY, lambda bundle: True)
    ])
    
    ## Market Man in Green House
    # Locations
    add_locations(Regions.MARKET_MAN_IN_GREEN_HOUSE, world, [
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT1, lambda bundle: (can_break_pots(bundle))),
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT2, lambda bundle: (can_break_pots(bundle))),
        (Locations.MARKET_BACK_ALLEY_HOUSE_POT3, lambda bundle: (can_break_pots(bundle))),
    ])
    # Connections
    connect_regions(Regions.MARKET_MAN_IN_GREEN_HOUSE, world, [
        (Regions.MARKET_BACK_ALLEY, lambda bundle: True)
    ])
    
