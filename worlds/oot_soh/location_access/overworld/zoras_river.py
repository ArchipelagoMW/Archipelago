from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *


if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    ZORAS_RIVER_SHRUB = "Zora's River Shrub"
    MAGIC_BEAN_SALESMAN_SHOP = "Magic Bean Salesman Shop"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    # TODO: Temporary to test generation
    connect_regions(Regions.KOKIRI_FOREST, world, [
        (Regions.ZR_FRONT, lambda s, r, w: True)
    ])
    connect_regions(Regions.ZR_FRONT, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## ZR Front
    # Locations
    add_locations(Regions.ZR_FRONT, world, [
        (Locations.ZR_GS_TREE, lambda s, r, w: is_child(s, r, w) and
                                                      can_kill_enemy(s, w, Enemies.GOLD_SKULLTULA)),
        (Locations.ZR_NEAR_TREE_GRASS1, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS2, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS3, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS4, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS5, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS6, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS7, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS8, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS9, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS10, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS11, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_NEAR_TREE_GRASS12, lambda s, r, w: can_cut_shrubs(s, w))

    ])
    # Connections
    connect_regions(Regions.ZR_FRONT, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: is_adult(s, r, w) or blast_or_smash(s, w)),
        (Regions.HYRULE_FIELD, lambda s, r, w: True)
    ])

    ## Zora River
    # Events
    add_events(Regions.ZORA_RIVER, world, [
        (EventLocations.MAGIC_BEAN_SALESMAN_SHOP, Events.CAN_BUY_BEANS, 
            lambda s, r, w: has_item(Items.CHILD_WALLET, s, w) and (world.options.shuffle_merchants == 0 or world.options.shuffle_merchants == 2)), # Bean shop not randomized
        (EventLocations.ZORAS_RIVER_SHRUB, Events.BUG_ACCESS, lambda s, r, w: can_cut_shrubs(s, w))
    ])
    # Locations
    add_locations(Regions.ZORA_RIVER, world, [
        (Locations.ZR_MAGIC_BEAN_SALESMAN, lambda s, r, w: is_child(s, r, w)),
        (Locations.ZR_FROGS_OCARINA_GAME, lambda s, r, w: (is_child(s, r, w) and
                                                               can_use(Items.SONG_OF_STORMS, s, w) and
                                                               can_use(Items.SONG_OF_TIME, s, w) and
                                                               can_use(Items.ZELDAS_LULLABY, s, w) and
                                                               can_use(Items.SUNS_SONG, s, w) and
                                                               can_use(Items.EPONAS_SONG, s, w) and
                                                               can_use(Items.SARIAS_SONG, s, w))),
        (Locations.ZR_FROGS_IN_THE_RAIN, lambda s, r, w: is_child(s, r, w) and
                                                             can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_FROGS_ZELDAS_LULLABY, lambda s, r, w: is_child(s, r, w) and
                                                             can_use(Items.ZELDAS_LULLABY, s, w)),
        (Locations.ZR_FROGS_EPONAS_SONG, lambda s, r, w: is_child(s, r, w) and
                                                             can_use(Items.EPONAS_SONG, s, w)),
        (Locations.ZR_FROGS_SARIAS_SONG, lambda s, r, w: is_child(s, r, w) and
                                                             can_use(Items.SARIAS_SONG, s, w)),
        (Locations.ZR_FROGS_SUNS_SONG, lambda s, r, w: is_child(s, r, w) and
                                                           can_use(Items.SUNS_SONG, s, w)),
        (Locations.ZR_FROGS_SONG_OF_TIME, lambda s, r, w: is_child(s, r, w) and
                                                              can_use(Items.SONG_OF_TIME, s, w)),
        (Locations.ZR_NEAR_OPEN_GROTTO_FREESTANDING_POH, lambda s, r, w: is_child(s, r, w) or
                                                                              can_use(Items.HOVER_BOOTS, s, w)
                                                                              or (is_adult(s, r, w)
                                                                                  and can_do_trick("ZR Lower Piece of Heart without Hover Boots", s, w))),
        (Locations.ZR_NEAR_DOMAIN_FREESTANDING_POH, lambda s, r, w: is_child(s, r, w) or
                                                                              can_use(Items.HOVER_BOOTS, s, w)
                                                                              or (is_adult(s, r, w)
                                                                                  and can_do_trick("ZR Upper Piece of Heart without Hover Boots", s, w))),
        (Locations.ZR_GS_LADDER, lambda s, r, w: is_child(s, r, w)
                                                     and  can_attack(s, w)
                                                     and can_get_nighttime_gs(s, w)),
        (Locations.ZR_GS_NEAR_RAISED_GROTTOS, lambda s, r, w: is_adult(s, r, w) and
                                                                  (can_use(Items.PROGRESSIVE_HOOKSHOT, s, w)
                                                                   or can_use(Items.BOOMERANG, s, w)) and
                                                                  can_get_nighttime_gs(s, w)),
        (Locations.ZR_GS_ABOVE_BRIDGE, lambda s, r, w: is_adult(s, r, w) and
                                                           can_use(Items.PROGRESSIVE_HOOKSHOT, s, w) and
                                                           can_get_nighttime_gs(s, w)),
        (Locations.ZR_BEAN_SPROUT_FAIRY1, lambda s, r, w: is_child(s, r, w)
                                                              and can_use(Items.MAGIC_BEAN, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_BEAN_SPROUT_FAIRY2, lambda s, r, w: is_child(s, r, w)
                                                              and can_use(Items.MAGIC_BEAN, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_BEAN_SPROUT_FAIRY3, lambda s, r, w: is_child(s, r, w)
                                                              and can_use(Items.MAGIC_BEAN, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy(s, w)),
        (Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy(s, w)),
        (Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_BENEATH_DOMAIN_RED_LEFT_RUPEE, lambda s, r, w: is_adult(s, r, w) and
                                                                         (has_item(Items.BRONZE_SCALE, s, w) or
                                                                          can_use(Items.IRON_BOOTS, s, w) or
                                                                          can_use(Items.BOOMERANG, s, w))),
        (Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_LEFT_RUPEE, lambda s, r, w: is_adult(s, r, w) and
                                                                         (has_item(Items.BRONZE_SCALE, s, w) or
                                                                          can_use(Items.IRON_BOOTS, s, w) or
                                                                          can_use(Items.BOOMERANG, s, w))),
        (Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_RIGHT_RUPEE, lambda s, r, w: is_adult(s, r, w) and
                                                                         (has_item(Items.BRONZE_SCALE, s, w) or
                                                                          can_use(Items.IRON_BOOTS, s, w) or
                                                                          can_use(Items.BOOMERANG, s, w))),
        (Locations.ZR_BENEATH_DOMAIN_RED_RIGHT_RUPEE, lambda s, r, w: is_adult(s, r, w) and
                                                                         (has_item(Items.BRONZE_SCALE, s, w) or
                                                                          can_use(Items.IRON_BOOTS, s, w) or
                                                                          can_use(Items.BOOMERANG, s, w))),
        (Locations.ZR_NEAR_FREESTANDING_PO_HGRASS, lambda s, r, w: can_cut_shrubs(s, w))
    ])
    # Connections
    connect_regions(Regions.ZORA_RIVER, world, [
        (Regions.ZR_FRONT, lambda s, r, w: True),
        (Regions.ZR_OPEN_GROTTO, lambda s, r, w: True),
        (Regions.ZR_FAIRY_GROTTO, lambda s, r, w: blast_or_smash(s, w)), #I am not sure that there's any scenario where blast or smash wouldn't apply to here, not sure why this needs here (which checks if the other age opened it, basically)?
        (Regions.LOST_WOODS, lambda s, r, w: has_item(Items.SILVER_SCALE, s, w) or  can_use(Items.IRON_BOOTS, s, w)),
        (Regions.ZR_STORMS_GROTTO, lambda s, r, w: can_open_storms_grotto(s, w)),
        (Regions.ZR_BEHIND_WATERFALL, lambda s, r, w: world.options.sleeping_waterfall==1 or
                                                          can_use(Items.ZELDAS_LULLABY, s, w) or
                                                          (is_child(s, r, w) and
                                                           can_do_trick("ZD with Cuckoo", s, w)) or
                                                          (is_adult(s, r, w) and
                                                           can_use(Items.HOVER_BOOTS, s, w) and
                                                           can_do_trick("ZD with Hover Boots", s, w)))

    ])
    # Events

    ## ZR From Shortcut
    # Connections
    connect_regions(Regions.ZR_FROM_SHORTCUT, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: can_live(s, w) or
                                                 has_item(Items.BOTTLE_WITH_FAIRY, s, w) or
                                                 has_item(Items.BRONZE_SCALE, s, w)),
        (Regions.LOST_WOODS, lambda s, r, w: has_item(Items.SILVER_SCALE, s, w) or
                                                 can_use(Items.IRON_BOOTS, s, w))

    ])

    ## ZR Behind Waterfall
    # Connections
    connect_regions(Regions.ZR_BEHIND_WATERFALL, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: True),
        (Regions.ZORAS_DOMAIN, lambda s, r, w: True)
    ])

    ## ZR Open Grotto
    # Locations
    add_locations(Regions.ZR_OPEN_GROTTO, world, [
        (Locations.ZR_OPEN_GROTTO_CHEST, lambda s, r, w: True),
        (Locations.ZR_OPEN_GROTTO_FISH, lambda s, r, w: has_bottle(s, w)),
        (Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy(s, w)),
        (Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.ZR_OPEN_GROTTO_BEEHIVE_LEFT, lambda s, r, w: can_break_lower_hives(s, w)),
        (Locations.ZR_OPEN_GROTTO_BEEHIVE_RIGHT, lambda s, r, w: can_break_lower_hives(s, w)),
        (Locations.ZR_OPEN_GROTTO_GRASS1, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_OPEN_GROTTO_GRASS2, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_OPEN_GROTTO_GRASS3, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.ZR_OPEN_GROTTO_GRASS4, lambda s, r, w: can_cut_shrubs(s, w))
    ])
    # Connections
    connect_regions(Regions.ZR_OPEN_GROTTO, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: True)
    ])

    ## ZR Fairy Grotto
    # Locations
    add_locations(Regions.ZR_FAIRY_GROTTO, world, [
        (Locations.ZR_FAIRY_GROTTO_FAIRY1, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY2, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY3, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY4, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY5, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY6, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY7, lambda s, r, w: True),
        (Locations.ZR_FAIRY_GROTTO_FAIRY8, lambda s, r, w: True)
    ])
    # Connections
    connect_regions(Regions.ZR_FAIRY_GROTTO, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: True)
    ])

    ## ZR Storms Grotto
    # Locations
    add_locations(Regions.ZR_STORMS_GROTTO, world, [
        (Locations.ZR_DEKU_SCRUB_GROTTO_FRONT, lambda s, r, w: can_stun_deku(s, w)),
        (Locations.ZR_DEKU_SCRUB_GROTTO_REAR, lambda s, r, w: can_stun_deku(s, w)),
        (Locations.ZR_STORMS_GROTTO_BEEHIVE, lambda s, r, w: can_break_upper_hives(s, w))

    ])
    # Connections
    connect_regions(Regions.ZR_STORMS_GROTTO, world, [
        (Regions.ZORA_RIVER, lambda s, r, w: True)
    ])
