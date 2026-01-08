from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    ZD_GOSSIP_STONE_SONG_FAIRY = "ZD Gossip Stone Song Fairy"
    ZD_NUT_POT = "ZD Nut Pot"
    ZD_STICK_POT = "ZD Stick Pot"
    ZD_FISH_GROUP = "ZD Fish Group"
    ZD_KING_ZORA_THAWING = "ZD King Zora Thawing"
    ZD_BEHIND_KING_ZORA_THAWING = "ZD Behind King Zora Thawing"
    ZD_DELIVER_RUTOS_LETTER = "ZD Deliver Ruto's Letter"
    ZD_FAIRY_GROTTO_FAIRY = "ZD Fairy Grotto Fairy"


class LocalEvents(StrEnum):
    KING_ZORA_THAWED = "King Zora Thawed"


def set_region_rules(world: "SohWorld") -> None:
    # Zoras Domain
    # Events
    if world.options.zoras_fountain.value != 2:
        add_events(Regions.ZORAS_DOMAIN, world, [
            (EventLocations.ZD_DELIVER_RUTOS_LETTER, Events.DELIVER_LETTER,
             lambda bundle: can_use(Items.BOTTLE_WITH_RUTOS_LETTER, bundle) and is_child(bundle))
        ])
    add_events(Regions.ZORAS_DOMAIN, world, [
        (EventLocations.ZD_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (EventLocations.ZD_NUT_POT, Events.CAN_FARM_NUTS, lambda bundle: True),
        (EventLocations.ZD_STICK_POT, Events.CAN_FARM_STICKS,
         lambda bundle: is_child(bundle)),
        (EventLocations.ZD_FISH_GROUP, Events.CAN_ACCESS_FISH,
         lambda bundle: is_child(bundle)),
        (EventLocations.ZD_KING_ZORA_THAWING, LocalEvents.KING_ZORA_THAWED,
         lambda bundle: is_adult(bundle) and blue_fire(bundle))
    ])
    # Locations
    add_locations(Regions.ZORAS_DOMAIN, world, [
        (Locations.ZD_DIVING_MINIGAME,
         lambda bundle: has_item(Items.BRONZE_SCALE, bundle) and has_item(Items.CHILD_WALLET, bundle) and is_child(
             bundle)),
        (Locations.ZD_CHEST, lambda bundle: is_child(
            bundle) and can_use(Items.STICKS, bundle)),
        (Locations.ZD_KING_ZORA_THAWED,
         lambda bundle: is_adult(bundle) and has_item(LocalEvents.KING_ZORA_THAWED, bundle)),
        (Locations.ZD_TRADE_PRESCRIPTION,
         lambda bundle: is_adult(bundle) and has_item(LocalEvents.KING_ZORA_THAWED, bundle) and can_use(
             Items.PRESCRIPTION, bundle)),
        (Locations.ZD_GS_FROZEN_WATERFALL, lambda bundle: is_adult(bundle)
         and (hookshot_or_boomerang(bundle)
              or can_use(Items.FAIRY_SLINGSHOT, bundle)
              or can_use(Items.FAIRY_BOW, bundle)
              or (can_use(Items.MAGIC_SINGLE, bundle)
                  and (can_use(Items.MASTER_SWORD, bundle)
                       or can_use(Items.KOKIRI_SWORD, bundle)
                       or can_use(Items.BIGGORONS_SWORD, bundle))))
         or (can_do_trick(Tricks.ZD_GS, bundle)
             and can_jump_slash_except_hammer(bundle))
         and can_get_nighttime_gs(bundle)),
        (Locations.ZD_FISH1, lambda bundle: is_child(bundle) and has_bottle(bundle)),
        (Locations.ZD_FISH2, lambda bundle: is_child(bundle) and has_bottle(bundle)),
        (Locations.ZD_FISH3, lambda bundle: is_child(bundle) and has_bottle(bundle)),
        (Locations.ZD_FISH4, lambda bundle: is_child(bundle) and has_bottle(bundle)),
        (Locations.ZD_FISH5, lambda bundle: is_child(bundle) and has_bottle(bundle)),
        (Locations.ZD_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.ZD_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.ZD_IN_FRONT_OF_KING_ZORA_BEEHIVE_LEFT,
         lambda bundle: is_child(bundle) and can_break_upper_beehives(bundle)),
        (Locations.ZD_IN_FRONT_OF_KING_ZORA_BEEHIVE_RIGHT,
         lambda bundle: is_child(bundle) and can_break_upper_beehives(bundle)),
        (Locations.ZD_NEAR_SHOP_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.ZD_NEAR_SHOP_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.ZD_NEAR_SHOP_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.ZD_NEAR_SHOP_POT4, lambda bundle: can_break_pots(bundle)),
        (Locations.ZD_NEAR_SHOP_POT5, lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.ZORAS_DOMAIN, world, [
        (Regions.ZR_BEHIND_WATERFALL, lambda bundle: True),
        (Regions.LH_FROM_SHORTCUT, lambda bundle: is_child(bundle) and (
            has_item(Items.SILVER_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Regions.ZD_BEHIND_KING_ZORA,
         lambda bundle: has_item(Events.DELIVER_LETTER, bundle) or world.options.zoras_fountain.value == 2 or (
             world.options.zoras_fountain.value == 1 and is_adult(bundle)) or (
             can_do_trick(Tricks.ZD_KING_ZORA_SKIP, bundle) and is_adult(bundle))),
        (Regions.ZD_SHOP, lambda bundle: is_child(bundle) or blue_fire(bundle)),
        (Regions.ZORAS_DOMAIN_ISLAND, lambda bundle: True),
    ])

    # Zoras Domain Island
    # Connections
    connect_regions(Regions.ZORAS_DOMAIN_ISLAND, world, [
        (Regions.ZORAS_DOMAIN, lambda bundle: is_adult(
            bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.ZD_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle)),
    ])

    # ZD Behind King Zora
    # Events
    add_events(Regions.ZD_BEHIND_KING_ZORA, world, [
        (EventLocations.ZD_BEHIND_KING_ZORA_THAWING, LocalEvents.KING_ZORA_THAWED,
         lambda bundle: is_adult(bundle) and blue_fire(bundle)),
    ])
    # Locations
    add_locations(Regions.ZD_BEHIND_KING_ZORA, world, [
        (Locations.ZD_BEHIND_KING_ZORA_BEEHIVE, lambda bundle: is_child(
            bundle) and can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.ZD_BEHIND_KING_ZORA, world, [
        (Regions.ZORAS_DOMAIN,
         lambda bundle: has_item(Events.DELIVER_LETTER, bundle) or world.options.zoras_fountain.value == 2 or (
             world.options.zoras_fountain.value == 1 and is_adult(bundle))),
        (Regions.ZORAS_FOUNTAIN, lambda bundle: True),
    ])

    # ZD Shop
    # Locations
    add_locations(Regions.ZD_SHOP, world, [
        (Locations.ZD_SHOP_ITEM1, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM2, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM3, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM4, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM5, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM6, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM7, lambda bundle: True),
        (Locations.ZD_SHOP_ITEM8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.ZD_SHOP, world, [
        (Regions.ZORAS_DOMAIN, lambda bundle: True),
    ])

    # ZD Storms Grotto
    # Events
    add_events(Regions.ZD_STORMS_GROTTO, world, [
        (EventLocations.ZD_FAIRY_GROTTO_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.ZD_STORMS_GROTTO, world, [
        (Locations.ZD_FAIRY_GROTTO_FAIRY1, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY2, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY3, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY4, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY5, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY6, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY7, lambda bundle: True),
        (Locations.ZD_FAIRY_GROTTO_FAIRY8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.ZD_STORMS_GROTTO, world, [
        (Regions.ZORAS_DOMAIN_ISLAND, lambda bundle: True),
    ])
