from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (add_locations, connect_regions, can_cut_shrubs)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld



def set_region_rules(world: "SohWorld") -> None:

    player = world.player
    
    ## ZR Front
    # Locations
    add_locations(Regions.ZR_FRONT.value, world, [
        [Locations.ZR_GS_TREE.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS1.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS2.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS3.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS4.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS5.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS6.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS7.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS8.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS9.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS10.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS11.value, lambda state: True],
        [Locations.ZR_NEAR_TREE_GRASS12.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZR_FRONT.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True],
        [Regions.HYRULE_FIELD.value, lambda state: True]
    ])

    ## Zora River
    # Locations

    add_locations(Regions.ZORA_RIVER, world, [
        [Events.BUG_SHRUBS.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.ZR_MAGIC_BEAN_SALESMAN.value, lambda state: True],
        [Locations.ZR_FROGS_OCARINA_GAME.value, lambda state: True],
        [Locations.ZR_FROGS_IN_THE_RAIN.value, lambda state: True],
        [Locations.ZR_FROGS_ZELDAS_LULLABY.value, lambda state: True],
        [Locations.ZR_FROGS_EPONAS_SONG.value, lambda state: True],
        [Locations.ZR_FROGS_SARIAS_SONG.value, lambda state: True],
        [Locations.ZR_FROGS_SUNS_SONG.value, lambda state: True],
        [Locations.ZR_FROGS_SONG_OF_TIME.value, lambda state: True],
        [Locations.ZR_NEAR_OPEN_GROTTO_FREESTANDING_PO_H.value, lambda state: True],
        [Locations.ZR_NEAR_DOMAIN_FREESTANDING_PO_H.value, lambda state: True],
        [Locations.ZR_GS_LADDER.value, lambda state: True],
        [Locations.ZR_GS_NEAR_RAISED_GROTTOS.value, lambda state: True],
        [Locations.ZR_GS_ABOVE_BRIDGE.value, lambda state: True],
        [Locations.ZR_BEAN_SPROUT_FAIRY1.value, lambda state: True],
        [Locations.ZR_BEAN_SPROUT_FAIRY2.value, lambda state: True],
        [Locations.ZR_BEAN_SPROUT_FAIRY3.value, lambda state: True],
        [Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.ZR_NEAR_GROTTOS_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.ZR_NEAR_DOMAIN_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.ZR_BENEATH_DOMAIN_RED_LEFT_RUPEE.value, lambda state: True],
        [Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_LEFT_RUPEE.value, lambda state: True],
        [Locations.ZR_BENEATH_DOMAIN_RED_MIDDLE_RIGHT_RUPEE.value, lambda state: True],
        [Locations.ZR_BENEATH_DOMAIN_RED_RIGHT_RUPEE.value, lambda state: True],
        [Locations.ZR_NEAR_FREESTANDING_PO_HGRASS.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZORA_RIVER.value, world, [
        [Regions.ZR_FRONT.value, lambda state: True],
        [Regions.ZR_OPEN_GROTTO.value, lambda state: True],
        [Regions.ZR_FAIRY_GROTTO.value, lambda state: True],
        [Regions.LOST_WOODS.value, lambda state: True],
        [Regions.ZR_STORMS_GROTTO.value, lambda state: True],
        [Regions.ZR_BEHIND_WATERFALL.value, lambda state: True]
    ])

    ## ZR From Shortcut
    # Connections
    connect_regions(Regions.ZR_FROM_SHORTCUT.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True],
        [Regions.LOST_WOODS.value, lambda state: True]
    ])

    ## ZR Behind Waterfall
    # Connections
    connect_regions(Regions.ZR_BEHIND_WATERFALL.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True],
        [Regions.ZORAS_DOMAIN.value, lambda state: True]
    ])

    ## ZR Open Grotto
    # Locations
    add_locations(Regions.ZR_OPEN_GROTTO.value, world, [
        [Locations.ZR_OPEN_GROTTO_CHEST.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_FISH.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_BEEHIVE_LEFT.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_BEEHIVE_RIGHT.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GRASS1.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GRASS2.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GRASS3.value, lambda state: True],
        [Locations.ZR_OPEN_GROTTO_GRASS4.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZR_OPEN_GROTTO.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True]
    ])

    ## ZR Fairy Grotto
    # Locations
    add_locations(Regions.ZR_FAIRY_GROTTO.value, world, [
        [Locations.ZR_FAIRY_GROTTO_FAIRY1.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY2.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY3.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY4.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY5.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY6.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY7.value, lambda state: True],
        [Locations.ZR_FAIRY_GROTTO_FAIRY8.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZR_FAIRY_GROTTO.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True]
    ])

    ## ZR Storms Grotto
    # Locations
    add_locations(Regions.ZR_STORMS_GROTTO.value, world, [
        [Locations.ZR_DEKU_SCRUB_GROTTO_FRONT.value, lambda state: True],
        [Locations.ZR_DEKU_SCRUB_GROTTO_REAR.value, lambda state: True],
        [Locations.ZR_STORMS_GROTTO_BEEHIVE.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.ZR_STORMS_GROTTO.value, world, [
        [Regions.ZORA_RIVER.value, lambda state: True]
    ])