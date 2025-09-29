from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import (add_locations, connect_regions, is_adult, can_attack,
                                         is_child, can_use, can_do_trick, call_gossip_fairy_except_suns,
                                         can_cut_shrubs, can_break_pots, has_bottle, call_gossip_fairy,
                                         can_break_lower_hives, can_open_storms_grotto, can_pass_enemy,
                                         hookshot_or_boomerang, can_get_nighttime_gs, add_events)


if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    MIDO = "Mido's Location"
    MIDO_OUTSIDE = "Mido's Location From Outside Deku Tree"
    KOKIRI_FOREST_SOFT_SOIL = "Kokiri Forest Soft Soil"


class LocalEvents(str, Enum):
    MIDO_SWORD_AND_SHIELD = "Showed Mido the Sword and Shield"


def set_region_rules(world: "SohWorld") -> None:

    player = world.player

    ## Kokiri Forest
    # Locations
    add_locations(Regions.KOKIRI_FOREST, world, [
        [Locations.KF_KOKIRI_SWORD_CHEST, lambda state: is_child(state, world)],
        [Locations.KF_GS_KNOW_IT_ALL_HOUSE, lambda state: (can_attack(state, world) and
                                                                        is_child(state, world) and
                                                                        can_get_nighttime_gs(state,world))],
        [Locations.KF_GS_BEAN_PATCH, lambda state: can_attack(state, world) and
                                                         is_child(state, world) and
                                                         can_use(Items.BOTTLE_WITH_BUGS, state, world)],
        [Locations.KF_GS_HOUSE_OF_TWINS, lambda state: is_adult(state, world) and
                                                             (hookshot_or_boomerang(state, world)
                                                              or (can_do_trick("Kokiri Forest Gold Skulltula with Hover Boots", state, world)
                                                                  and can_use(Items.HOVER_BOOTS, state, world))) and can_get_nighttime_gs(state, world)],
        [Locations.KF_BEAN_SPROUT_FAIRY1, lambda state: is_child(state, world)
                                                              and state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_BEAN_SPROUT_FAIRY2, lambda state: is_child(state, world)
                                                              and state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_BEAN_SPROUT_FAIRY3, lambda state: is_child(state, world)
                                                              and state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player)
                                                              and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy_except_suns(state, world)],
        [Locations.KF_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_BRIDGE_RUPEE, lambda state: is_child(state,world)],
        [Locations.KF_BEHIND_MIDOS_HOUSE_RUPEE, lambda state: is_child(state,world)],
        [Locations.KF_SOUTH_GRASS_WEST_RUPEE, lambda state: is_child(state,world)],
        [Locations.KF_SOUTH_GRASS_EAST_RUPEE, lambda state: is_child(state ,world)],
        [Locations.KF_NORTH_GRASS_WEST_RUPEE, lambda state: is_child(state, world)],
        [Locations.KF_NORTH_GRASS_EAST_RUPEE, lambda state: is_child(state, world)],
        [Locations.KF_BOULDER_MAZE_FIRST_RUPEE, lambda state: is_child(state, world)],
        [Locations.KF_BOULDER_MAZE_SECOND_RUPEE, lambda state: is_child(state, world)],
        [Locations.KF_BEAN_PLATFORM_RUPEE1, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RUPEE2, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RUPEE3, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RUPEE4, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RUPEE5, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RUPEE6, lambda state:  is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_BEAN_PLATFORM_RED_RUPEE, lambda state: is_adult(state, world) and (Items.HOVER_BOOTS, state, world or
                                                                   can_use(Items.BOOMERANG, state, world) or
                                                                   state.has(Events.KOKIRI_FOREST_BEAN_PLANTED, player))],
        [Locations.KF_SARIAS_ROOF_EAST_HEART, lambda state: is_child(state, world)],
        [Locations.KF_SARIAS_ROOF_NORTH_HEART, lambda state: is_child(state, world)],
        [Locations.KF_SARIAS_ROOF_WEST_HEART, lambda state: is_child(state, world)],
        [Locations.KF_CHILD_GRASS1, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS2, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS3, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS4, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS5, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS6, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS7, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS8, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS9, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS10, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS11, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS12, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS_MAZE1, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS_MAZE2, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_CHILD_GRASS_MAZE3, lambda state: (is_child(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS1, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS2, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS3, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS4, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS5, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS6, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS7, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS8, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS9, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS10, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS11, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS12, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS13, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS14, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS15, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS16, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS17, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS19, lambda state: (is_adult(state, world)
                                                        and can_cut_shrubs(state, world))],
        [Locations.KF_ADULT_GRASS20, lambda state: (is_adult(state, world))]
    ])
    # Connections
    connect_regions(Regions.KOKIRI_FOREST, world, [
        [Regions.KF_LINKS_HOUSE, lambda state: True],
        [Regions.KF_MIDOS_HOUSE, lambda state: True],
        [Regions.KF_SARIAS_HOUSE, lambda state: True],
        [Regions.KF_HOUSE_OF_TWINS, lambda state: True],
        [Regions.KF_KNOW_IT_ALL_HOUSE, lambda state: True],
        [Regions.KF_KOKIRI_SHOP, lambda state: True],
        [Regions.KF_OUTSIDE_DEKU_TREE, lambda state: (is_adult(state, world) and
                                                             (can_pass_enemy(state, world, Enemies.BIG_SKULLTULA) or
                                                             state.has(Events.CLEARED_FOREST_TEMPLE, player)))
                                                            or state.has(LocalEvents.MIDO_SWORD_AND_SHIELD, player)
                                                           or world.options.closed_forest==2],
        [Regions.LOST_WOODS, lambda state: True],
        [Regions.LW_BRIDGE_FROM_FOREST, lambda state: world.options.closed_forest>=1 or is_adult(state, world) or
                                                            state.has(Events.CLEARED_DEKU_TREE, player)],
        [Regions.KF_STORMS_GROTTO, lambda state: can_open_storms_grotto(state, world)]
    ])
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        [EventLocations.MIDO, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda state: Items.KOKIRI_SWORD and
                                                          Items.DEKU_SHIELD],
        [EventLocations.KOKIRI_FOREST_SOFT_SOIL, Events.KOKIRI_FOREST_BEAN_PLANTED, lambda state: is_child(state, world) and
                                                     can_use(Items.MAGIC_BEAN, state, world)],
    ])

    ## KF Link's House
    # Locations
    add_locations(Regions.KF_LINKS_HOUSE, world, [
        [Locations.KF_LINKS_HOUSE_COW, lambda state: is_adult(state, world) and
                                                           can_use(Items.EPONAS_SONG, state, world) and
                                                           state.has(Events.GOTTEN_LINKS_COW, player)],
        [Locations.KF_LINKS_HOUSE_POT, lambda state: can_break_pots(state, world)]

    ])
    # Connections
    connect_regions(Regions.KF_LINKS_HOUSE, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF Mido's House
    # Locations
    add_locations(Regions.KF_MIDOS_HOUSE, world, [
        [Locations.KF_MIDO_TOP_LEFT_CHEST, lambda state: True],
        [Locations.KF_MIDO_TOP_RIGHT_CHEST, lambda state: True],
        [Locations.KF_MIDO_BOTTOM_LEFT_CHEST, lambda state: True],
        [Locations.KF_MIDO_BOTTOM_RIGHT_CHEST, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_MIDOS_HOUSE, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF Saria's House
    # Locations
    add_locations(Regions.KF_SARIAS_HOUSE, world, [
        [Locations.KF_SARIAS_HOUSE_TOP_LEFT_HEART, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_TOP_RIGHT_HEART, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_BOTTOM_LEFT_HEART, lambda state: True],
        [Locations.KF_SARIAS_HOUSE_BOTTOM_RIGHT_HEART, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_SARIAS_HOUSE, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF House of Twins
    # Locations
    add_locations(Regions.KF_HOUSE_OF_TWINS, world, [
        [Locations.KF_TWINS_HOUSE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.KF_TWINS_HOUSE_POT2, lambda state: can_break_pots(state, world)]

    ])
    # Connections
    connect_regions(Regions.KF_HOUSE_OF_TWINS, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF Know it All House
    # Locations
    add_locations(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        [Locations.KF_BROTHERS_HOUSE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.KF_BROTHERS_HOUSE_POT2, lambda state: can_break_pots(state, world)]

    ])
    # Connections
    connect_regions(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF Kokiri Shop
    # Locations
    add_locations(Regions.KF_KOKIRI_SHOP, world, [
        [Locations.KF_SHOP_ITEM1, lambda state: True],
        [Locations.KF_SHOP_ITEM2, lambda state: True],
        [Locations.KF_SHOP_ITEM3, lambda state: True],
        [Locations.KF_SHOP_ITEM4, lambda state: True],
        [Locations.KF_SHOP_ITEM5, lambda state: True],
        [Locations.KF_SHOP_ITEM6, lambda state: True],
        [Locations.KF_SHOP_ITEM7, lambda state: True],
        [Locations.KF_SHOP_ITEM8, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.KF_KOKIRI_SHOP, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## KF Outside Deku Tree
    # Locations
    add_locations(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        [Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy_except_suns(state, world)],
        [Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy_except_suns(state, world)],
        [Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)]
    ])
    # Connections
    connect_regions(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        [Regions.DEKU_TREE_ENTRYWAY, lambda state: (is_child(state, world))
                                                         and (world.options.closed_forest==2
                                                            or state.has(LocalEvents.MIDO_SWORD_AND_SHIELD, player))],
        [Regions.KOKIRI_FOREST, lambda state:  (is_adult(state, world) and
                                                             (can_pass_enemy(state, world, Enemies.BIG_SKULLTULA) or
                                                             state.has(Events.CLEARED_FOREST_TEMPLE, player)))
                                                            or state.has(LocalEvents.MIDO_SWORD_AND_SHIELD, player)
                                                           or world.options.closed_forest==2]
    ])
    add_events(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        [EventLocations.MIDO_OUTSIDE, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda state: Items.KOKIRI_SWORD and
                                                  Items.DEKU_SHIELD],
    ])

    ## KF Storms Grotto
    # Locations
    add_locations(Regions.KF_STORMS_GROTTO, world, [
        [Locations.KF_STORMS_GROTTO_CHEST, lambda state: True],
        [Locations.KF_STORMS_GROTTO_FISH, lambda state: has_bottle(state, world)],
        [Locations.KF_STORMS_GOSSIP_STONE_FAIRY, lambda state: call_gossip_fairy(state, world)],
        [Locations.KF_STORMS_GOSSIP_STONE_BIG_FAIRY, lambda state: can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.KF_STORMS_GROTTO_BEEHIVE_LEFT, lambda state: can_break_lower_hives(state, world)],
        [Locations.KF_STORMS_GROTTO_BEEHIVE_RIGHT, lambda state: can_break_lower_hives(state, world)],
        [Locations.KF_STORMS_GROTTO_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.KF_STORMS_GROTTO_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.KF_STORMS_GROTTO_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.KF_STORMS_GROTTO_GRASS4, lambda state: can_cut_shrubs(state, world)],
    ])
    # Connections
    connect_regions(Regions.KF_STORMS_GROTTO, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])




