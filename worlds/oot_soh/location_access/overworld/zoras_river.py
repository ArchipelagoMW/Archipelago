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
        [Regions.ZR_FRONT, lambda state: True]
    ])
    connect_regions(Regions.ZR_FRONT, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## ZR Front
    # Locations
    add_locations(Regions.ZR_FRONT, world, [
        [Locations.ZR_GS_TREE, lambda state: is_child(state, world) and
                                                      can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA)],
        [Locations.ZR_NEAR_TREE_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS4, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS5, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS6, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS7, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS8, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS9, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS10, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS11, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_NEAR_TREE_GRASS12, lambda state: can_cut_shrubs(state, world)]

    ])
    # Connections
    connect_regions(Regions.ZR_FRONT, world, [
        [Regions.ZORA_RIVER, lambda state: is_adult(state, world) or blast_or_smash(state, world)],
        [Regions.HYRULE_FIELD, lambda state: True]
    ])

    ## Zora River
    # Events
    add_events(Regions.ZORA_RIVER, world, [
        [EventLocations.MAGIC_BEAN_SALESMAN_SHOP, Events.CAN_BUY_BEANS, 
            lambda state: has_item(Items.CHILD_WALLET, state, world) and (world.options.shuffle_merchants == 0 or world.options.shuffle_merchants == 2)], # Bean shop not randomized
        [EventLocations.ZORAS_RIVER_SHRUB, Events.BUG_ACCESS, lambda state: can_cut_shrubs(state, world)]
    ])
    # Locations
    add_locations(Regions.ZORA_RIVER, world, [
        [Locations.ZR_MAGIC_BEAN_SALESMAN, lambda state: is_child(state, world)],
        [Locations.ZR_FROGS_OCARINA_GAME, lambda state: (is_child(state, world) and
                                                               can_use(Items.SONG_OF_STORMS, state, world) and
                                                               can_use(Items.SONG_OF_TIME, state, world) and
                                                               can_use(Items.ZELDAS_LULLABY, state, world) and
                                                               can_use(Items.SUNS_SONG, state, world) and
                                                               can_use(Items.EPONAS_SONG, state, world) and
                                                               can_use(Items.SARIAS_SONG, state, world))],
        [Locations.ZR_FROGS_IN_THE_RAIN, lambda state: is_child(state, world) and
                                                             can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_FROGS_ZELDAS_LULLABY, lambda state: is_child(state, world) and
                                                             can_use(Items.ZELDAS_LULLABY, state, world)],
        [Locations.ZR_FROGS_EPONAS_SONG, lambda state: is_child(state, world) and
                                                             can_use(Items.EPONAS_SONG, state, world)],
        [Locations.ZR_FROGS_SARIAS_SONG, lambda state: is_child(state, world) and
                                                             can_use(Items.SARIAS_SONG, state, world)],
        [Locations.ZR_FROGS_SUNS_SONG, lambda state: is_child(state, world) and
                                                           can_use(Items.SUNS_SONG, state, world)],
        [Locations.ZR_FROGS_SONG_OF_TIME, lambda state: is_child(state, world) and
                                                              can_use(Items.SONG_OF_TIME, state, world)],
        [Locations.ZR_NEAR_OPEN_GROTTO_FREESTANDING_POH, lambda state: is_child(state, world) or
                                                                              can_use(Items.HOVER_BOOTS, state, world)
                                                                              or (is_adult(state, world)
                                                                                  and can_do_trick("ZR Lower Piece of Heart without Hover Boots", state, world))],
        [Locations.ZR_NEAR_DOMAIN_FREESTANDING_POH, lambda state: is_child(state, world) or
                                                                              can_use(Items.HOVER_BOOTS, state, world)
                                                                              or (is_adult(state, world)
                                                                                  and can_do_trick("ZR Upper Piece of Heart without Hover Boots", state, world))],
        [Locations.ZR_GS_LADDER, lambda state: is_child(state, world)
                                                     and  can_attack(state, world)
                                                     and can_get_nighttime_gs(state, world)],
        [Locations.ZR_GS_NEAR_RAISED_GROTTOS, lambda state: is_adult(state, world) and
                                                                  (can_use(Items.PROGRESSIVE_HOOKSHOT, state, world)
                                                                   or can_use(Items.BOOMERANG, state, world)) and
                                                                  can_get_nighttime_gs(state, world)],
        [Locations.ZR_GS_ABOVE_BRIDGE, lambda state: is_adult(state, world) and
                                                           can_use(Items.PROGRESSIVE_HOOKSHOT, state, world) and
                                                           can_get_nighttime_gs(state, world)],
        [Locations.ZR_BEAN_SPROUT_FAIRY1, lambda state: is_child(state, world)
                                                              and can_use(Items.MAGIC_BEAN, state, world)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_BEAN_SPROUT_FAIRY2, lambda state: is_child(state, world)
                                                              and can_use(Items.MAGIC_BEAN, state, world)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_BEAN_SPROUT_FAIRY3, lambda state: is_child(state, world)
                                                              and can_use(Items.MAGIC_BEAN, state, world)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy(state, world)],
        [Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy(state, world)],
        [Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_BENEATH_DOMAIN_RED_LEFT_RUPEE, lambda state: is_adult(state, world) and
                                                                         (state.has(Items.BRONZE_SCALE) or
                                                                          can_use(Items.IRON_BOOTS, state, world) or
                                                                          can_use(Items.BOOMERANG, state, world))],
        [Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_LEFT_RUPEE, lambda state: is_adult(state, world) and
                                                                         (state.has(Items.BRONZE_SCALE) or
                                                                          can_use(Items.IRON_BOOTS, state, world) or
                                                                          can_use(Items.BOOMERANG, state, world))],
        [Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_RIGHT_RUPEE, lambda state: is_adult(state, world) and
                                                                         (state.has(Items.BRONZE_SCALE) or
                                                                          can_use(Items.IRON_BOOTS, state, world) or
                                                                          can_use(Items.BOOMERANG, state, world))],
        [Locations.ZR_BENEATH_DOMAIN_RED_RIGHT_RUPEE, lambda state: is_adult(state, world) and
                                                                         (state.has(Items.BRONZE_SCALE) or
                                                                          can_use(Items.IRON_BOOTS, state, world) or
                                                                          can_use(Items.BOOMERANG, state, world))],
        [Locations.ZR_NEAR_FREESTANDING_PO_HGRASS, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.ZORA_RIVER, world, [
        [Regions.ZR_FRONT, lambda state: True],
        [Regions.ZR_OPEN_GROTTO, lambda state: True],
        [Regions.ZR_FAIRY_GROTTO, lambda state: blast_or_smash(state, world)], #I am not sure that there's any scenario where blast or smash wouldn't apply to here, not sure why this needs here (which checks if the other age opened it, basically)?
        [Regions.LOST_WOODS, lambda state: state.has(Items.SILVER_SCALE) or  can_use(Items.IRON_BOOTS, state, world)],
        [Regions.ZR_STORMS_GROTTO, lambda state: can_open_storms_grotto(state, world)],
        [Regions.ZR_BEHIND_WATERFALL, lambda state: world.options.sleeping_waterfall==1 or
                                                          can_use(Items.ZELDAS_LULLABY, state, world) or
                                                          (is_child(state, world) and
                                                           can_do_trick("ZD with Cuckoo", state, world)) or
                                                          (is_adult(state, world) and
                                                           can_use(Items.HOVER_BOOTS, state, world) and
                                                           can_do_trick("ZD with Hover Boots", state, world))]

    ])
    # Events

    ## ZR From Shortcut
    # Connections
    connect_regions(Regions.ZR_FROM_SHORTCUT, world, [
        [Regions.ZORA_RIVER, lambda state: can_live(state, world) or
                                                 state.has(Items.BOTTLE_WITH_FAIRY) or
                                                 state.has(Items.BRONZE_SCALE)],
        [Regions.LOST_WOODS, lambda state: state.has(Items.SILVER_SCALE) or
                                                 can_use(Items.IRON_BOOTS, state, world)]

    ])

    ## ZR Behind Waterfall
    # Connections
    connect_regions(Regions.ZR_BEHIND_WATERFALL, world, [
        [Regions.ZORA_RIVER, lambda state: True],
        [Regions.ZORAS_DOMAIN, lambda state: True]
    ])

    ## ZR Open Grotto
    # Locations
    add_locations(Regions.ZR_OPEN_GROTTO, world, [
        [Locations.ZR_OPEN_GROTTO_CHEST, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_FISH, lambda state: has_bottle(state, world)],
        [Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy(state, world)],
        [Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.ZR_OPEN_GROTTO_BEEHIVE_LEFT, lambda state: can_break_lower_hives(state, world)],
        [Locations.ZR_OPEN_GROTTO_BEEHIVE_RIGHT, lambda state: can_break_lower_hives(state, world)],
        [Locations.ZR_OPEN_GROTTO_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_OPEN_GROTTO_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_OPEN_GROTTO_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_OPEN_GROTTO_GRASS4, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.ZR_OPEN_GROTTO, world, [
        [Regions.ZORA_RIVER, lambda state: True]
    ])

    ## ZR Fairy Grotto
    # Locations
    add_locations(Regions.ZR_FAIRY_GROTTO, world, [
        [Locations.ZR_FAIRY_GROTTO_FAIRY1, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY2, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY3, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY4, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY5, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY6, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY7, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY8, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZR_FAIRY_GROTTO, world, [
        [Regions.ZORA_RIVER, lambda state: True]
    ])

    ## ZR Storms Grotto
    # Locations
    add_locations(Regions.ZR_STORMS_GROTTO, world, [
        [Locations.ZR_DEKU_SCRUB_GROTTO_FRONT, lambda state: can_stun_deku(state, world)],
        [Locations.ZR_DEKU_SCRUB_GROTTO_REAR, lambda state: can_stun_deku(state, world)],
        [Locations.ZR_STORMS_GROTTO_BEEHIVE, lambda state: can_break_upper_hives(state, world)]

    ])
    # Connections
    connect_regions(Regions.ZR_STORMS_GROTTO, world, [
        [Regions.ZORA_RIVER, lambda state: True]
    ])
