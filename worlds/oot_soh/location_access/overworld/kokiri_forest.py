from typing import TYPE_CHECKING, Dict

from worlds.generic.Rules import set_rule
from ...Regions import double_link_regions
from ...Items import SohItem
from ...Locations import SohLocation, SohLocationData
from ...Enums import *
from ...LogicHelpers import add_locations, connect_regions

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Kokiri Forest
    # Locations
    add_locations(Regions.KOKIRI_FOREST, world, [
        [Locations.KF_KOKIRI_SWORD_CHEST.value, lambda state: True],
        [Locations.KF_GS_KNOW_IT_ALL_HOUSE.value, lambda state: True],
        [Locations.KF_GS_BEAN_PATCH.value, lambda state: True],
        [Locations.KF_GS_HOUSE_OF_TWINS.value, lambda state: True],
        [Locations.KF_BEAN_SPROUT_FAIRY1.value, lambda state: True],
        [Locations.KF_BEAN_SPROUT_FAIRY2.value, lambda state: True],
        [Locations.KF_BEAN_SPROUT_FAIRY3.value, lambda state: True],
        [Locations.KF_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.KF_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.KF_BRIDGE_RUPEE.value, lambda state: True],
        [Locations.KF_BEHIND_MIDOS_HOUSE_RUPEE.value, lambda state: True],
        [Locations.KF_SOUTH_GRASS_WEST_RUPEE.value, lambda state: True],
        [Locations.KF_SOUTH_GRASS_EAST_RUPEE.value, lambda state: True],
        [Locations.KF_NORTH_GRASS_WEST_RUPEE.value, lambda state: True],
        [Locations.KF_NORTH_GRASS_EAST_RUPEE.value, lambda state: True],
        [Locations.KF_BOULDER_MAZE_FIRST_RUPEE.value, lambda state: True],
        [Locations.KF_BOULDER_MAZE_SECOND_RUPEE.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE1.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE2.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE3.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE4.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE5.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RUPEE6.value, lambda state: True],
        [Locations.KF_BEAN_PLATFORM_RED_RUPEE.value, lambda state: True],
        [Locations.KF_SARIAS_ROOF_EAST_HEART.value, lambda state: True],
        [Locations.KF_SARIAS_ROOF_NORTH_HEART.value, lambda state: True],
        [Locations.KF_SARIAS_ROOF_WEST_HEART.value, lambda state: True],
        [Locations.KF_CHILD_GRASS1.value, lambda state: True],
        [Locations.KF_CHILD_GRASS2.value, lambda state: True],
        [Locations.KF_CHILD_GRASS3.value, lambda state: True],
        [Locations.KF_CHILD_GRASS4.value, lambda state: True],
        [Locations.KF_CHILD_GRASS5.value, lambda state: True],
        [Locations.KF_CHILD_GRASS6.value, lambda state: True],
        [Locations.KF_CHILD_GRASS7.value, lambda state: True],
        [Locations.KF_CHILD_GRASS8.value, lambda state: True],
        [Locations.KF_CHILD_GRASS9.value, lambda state: True],
        [Locations.KF_CHILD_GRASS10.value, lambda state: True],
        [Locations.KF_CHILD_GRASS11.value, lambda state: True],
        [Locations.KF_CHILD_GRASS12.value, lambda state: True],
        [Locations.KF_CHILD_GRASS_MAZE1.value, lambda state: True],
        [Locations.KF_CHILD_GRASS_MAZE2.value, lambda state: True],
        [Locations.KF_CHILD_GRASS_MAZE3.value, lambda state: True],
        [Locations.KF_ADULT_GRASS1.value, lambda state: True],
        [Locations.KF_ADULT_GRASS2.value, lambda state: True],
        [Locations.KF_ADULT_GRASS3.value, lambda state: True],
        [Locations.KF_ADULT_GRASS4.value, lambda state: True],
        [Locations.KF_ADULT_GRASS5.value, lambda state: True],
        [Locations.KF_ADULT_GRASS6.value, lambda state: True],
        [Locations.KF_ADULT_GRASS7.value, lambda state: True],
        [Locations.KF_ADULT_GRASS8.value, lambda state: True],
        [Locations.KF_ADULT_GRASS9.value, lambda state: True],
        [Locations.KF_ADULT_GRASS10.value, lambda state: True],
        [Locations.KF_ADULT_GRASS11.value, lambda state: True],
        [Locations.KF_ADULT_GRASS12.value, lambda state: True],
        [Locations.KF_ADULT_GRASS13.value, lambda state: True],
        [Locations.KF_ADULT_GRASS14.value, lambda state: True],
        [Locations.KF_ADULT_GRASS15.value, lambda state: True],
        [Locations.KF_ADULT_GRASS16.value, lambda state: True],
        [Locations.KF_ADULT_GRASS17.value, lambda state: True],
        [Locations.KF_ADULT_GRASS19.value, lambda state: True],
        [Locations.KF_ADULT_GRASS20.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KOKIRI_FOREST.value, world, [
        [Regions.KF_LINKS_HOUSE.value, lambda state: True],
        [Regions.KF_MIDOS_HOUSE.value, lambda state: True],
        [Regions.KF_SARIAS_HOUSE.value, lambda state: True],
        [Regions.KF_HOUSE_OF_TWINS.value, lambda state: True],
        [Regions.KF_KNOW_IT_ALL_HOUSE.value, lambda state: True],
        [Regions.KF_KOKIRI_SHOP.value, lambda state: True],
        [Regions.KF_OUTSIDE_DEKU_TREE.value, lambda state: True],
        [Regions.LOST_WOODS.value, lambda state: True],
        [Regions.LW_BRIDGE_FROM_FOREST.value, lambda state: True],
        [Regions.KF_STORMS_GROTTO.value, lambda state: True]
    ])

    ## KF Link's House
    # Locations
    add_locations(Regions.KF_LINKS_HOUSE, world, [
        [Locations.KF_LINKS_HOUSE_COW.value, lambda state: True],
        [Locations.KF_LINKS_HOUSE_POT.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_LINKS_HOUSE.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Mido's House
    # Locations
    add_locations(Regions.KF_MIDOS_HOUSE, world, [
        [Locations.KF_MIDO_TOP_LEFT_CHEST.value, lambda state: True],
        [Locations.KF_MIDO_TOP_RIGHT_CHEST.value, lambda state: True],
        [Locations.KF_MIDO_BOTTOM_LEFT_CHEST.value, lambda state: True],
        [Locations.KF_MIDO_BOTTOM_RIGHT_CHEST.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_MIDOS_HOUSE.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Saria's House
    # Locations
    add_locations(Regions.KF_SARIAS_HOUSE, world, [
        [Locations.KF_SARIAS_HOUSE_TOP_LEFT_HEART.value, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_TOP_RIGHT_HEART.value, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_BOTTOM_LEFT_HEART.value, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_BOTTOM_RIGHT_HEART.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_SARIAS_HOUSE.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF House of Twins
    # Locations
    add_locations(Regions.KF_HOUSE_OF_TWINS, world, [
        [Locations.KF_TWINS_HOUSE_POT1.value, lambda state: True],
        [Locations.KF_TWINS_HOUSE_POT2.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_HOUSE_OF_TWINS.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Know it All House
    # Locations
    add_locations(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        [Locations.KF_BROTHERS_HOUSE_POT1.value, lambda state: True],
        [Locations.KF_BROTHERS_HOUSE_POT2.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_KNOW_IT_ALL_HOUSE.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Kokiri Shop
    # Locations
    add_locations(Regions.KF_KOKIRI_SHOP.value, world, [
        [Locations.KF_SHOP_ITEM1.value, lambda state: True],
        [Locations.KF_SHOP_ITEM2.value, lambda state: True],
        [Locations.KF_SHOP_ITEM3.value, lambda state: True],
        [Locations.KF_SHOP_ITEM4.value, lambda state: True],
        [Locations.KF_SHOP_ITEM5.value, lambda state: True],
        [Locations.KF_SHOP_ITEM6.value, lambda state: True],
        [Locations.KF_SHOP_ITEM7.value, lambda state: True],
        [Locations.KF_SHOP_ITEM8.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_KOKIRI_SHOP.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Outside Deku Tree
    # Locations
    add_locations(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        [Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_OUTSIDE_DEKU_TREE.value, world, [
        [Regions.DEKU_TREE_ENTRYWAY.value, lambda state: True],
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])

    ## KF Storms Grotto
    # Locations
    add_locations(Regions.KF_STORMS_GROTTO, world, [
        [Locations.KF_STORMS_GROTTO_CHEST.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_FISH.value, lambda state: True],
        [Locations.KF_STORMS_GOSSIP_STONE_FAIRY.value, lambda state: True],
        [Locations.KF_STORMS_GOSSIP_STONE_BIG_FAIRY.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_BEEHIVE_LEFT.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_BEEHIVE_RIGHT.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_GRASS1.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_GRASS2.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_GRASS3.value, lambda state: True],
        [Locations.KF_STORMS_GROTTO_GRASS4.value, lambda state: True],
    ])
    # Connections
    connect_regions(Regions.KF_STORMS_GROTTO.value, world, [
        [Regions.KOKIRI_FOREST.value, lambda state: True]
    ])
