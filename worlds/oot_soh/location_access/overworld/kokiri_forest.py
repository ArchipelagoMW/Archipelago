from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    MIDO = "Mido's Location"
    MIDO_OUTSIDE = "Mido's Location From Outside Deku Tree"
    KOKIRI_FOREST_SOFT_SOIL = "Kokiri Forest Soft Soil"


class LocalEvents(str, Enum):
    MIDO_SWORD_AND_SHIELD = "Showed Mido the Sword and Shield"


def set_region_rules(world: "SohWorld") -> None:
    ## Kokiri Forest
    # Locations
    add_locations(Regions.KOKIRI_FOREST, world, [
        (Locations.KF_KOKIRI_SWORD_CHEST, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_GS_KNOW_IT_ALL_HOUSE, lambda s, r, w: (can_attack(s, w) and
                                                                        is_child(s, r, w) and
                                                                        can_get_nighttime_gs(s, w))),
        (Locations.KF_GS_BEAN_PATCH, lambda s, r, w: can_attack(s, w) and
                                                         is_child(s, r, w) and
                                                         can_use(Items.BOTTLE_WITH_BUGS, s, w)),
        (Locations.KF_GS_HOUSE_OF_TWINS, lambda s, r, w: is_adult(s, r, w) and
                                                             (hookshot_or_boomerang(s, w)
                                                              or (can_do_trick("Kokiri Forest Gold Skulltula with Hover Boots", s, w)
                                                                  and can_use(Items.HOVER_BOOTS, s, w))) and can_get_nighttime_gs(s, w)),
        (Locations.KF_BEAN_SPROUT_FAIRY1, lambda s, r, w: is_child(s, r, w)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_BEAN_SPROUT_FAIRY2, lambda s, r, w: is_child(s, r, w)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_BEAN_SPROUT_FAIRY3, lambda s, r, w: is_child(s, r, w)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w)
                                                              and can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy_except_suns(s, w)),
        (Locations.KF_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_BRIDGE_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_BEHIND_MIDOS_HOUSE_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_SOUTH_GRASS_WEST_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_SOUTH_GRASS_EAST_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_NORTH_GRASS_WEST_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_NORTH_GRASS_EAST_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_BOULDER_MAZE_FIRST_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_BOULDER_MAZE_SECOND_RUPEE, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_BEAN_PLATFORM_RUPEE1, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RUPEE2, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RUPEE3, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RUPEE4, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RUPEE5, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RUPEE6, lambda s, r, w:  is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_BEAN_PLATFORM_RED_RUPEE, lambda s, r, w: is_adult(s, r, w) and (has_item(Items.HOVER_BOOTS, s, w) or
                                                                   can_use(Items.BOOMERANG, s, w) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, s, w))),
        (Locations.KF_SARIAS_ROOF_EAST_HEART, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_SARIAS_ROOF_NORTH_HEART, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_SARIAS_ROOF_WEST_HEART, lambda s, r, w: is_child(s, r, w)),
        (Locations.KF_CHILD_GRASS1, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS2, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS3, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS4, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS5, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS6, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS7, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS8, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS9, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS10, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS11, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS12, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS_MAZE1, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS_MAZE2, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_CHILD_GRASS_MAZE3, lambda s, r, w: (is_child(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS1, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS2, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS3, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS4, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS5, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS6, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS7, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS8, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS9, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS10, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS11, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS12, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS13, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS14, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS15, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS16, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS17, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS19, lambda s, r, w: (is_adult(s, r, w)
                                                        and can_cut_shrubs(s, w))),
        (Locations.KF_ADULT_GRASS20, lambda s, r, w: (is_adult(s, r, w)))
    ])
    # Connections
    connect_regions(Regions.KOKIRI_FOREST, world, [
        (Regions.KF_LINKS_HOUSE, lambda s, r, w: True),
        (Regions.KF_MIDOS_HOUSE, lambda s, r, w: True),
        (Regions.KF_SARIAS_HOUSE, lambda s, r, w: True),
        (Regions.KF_HOUSE_OF_TWINS, lambda s, r, w: True),
        (Regions.KF_KNOW_IT_ALL_HOUSE, lambda s, r, w: True),
        (Regions.KF_KOKIRI_SHOP, lambda s, r, w: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda s, r, w: (is_adult(s, r, w) and
                                                             (can_pass_enemy(s, w, Enemies.BIG_SKULLTULA) or
                                                             has_item(Events.CLEARED_FOREST_TEMPLE, s, w)))
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, s, w)
                                                           or w.options.closed_forest==2),
        (Regions.LOST_WOODS, lambda s, r, w: True),
        (Regions.LW_BRIDGE_FROM_FOREST, lambda s, r, w: w.options.closed_forest>=1 or is_adult(s, r, w) or
                                                            has_item(Events.CLEARED_DEKU_TREE, s, w)),
        (Regions.KF_STORMS_GROTTO, lambda s, r, w: can_open_storms_grotto(s, w))
    ])
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        (EventLocations.MIDO, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda s, r, w: has_item(Items.KOKIRI_SWORD, s, w) 
                                                                    and has_item(Items.DEKU_SHIELD, s, w)),
        (EventLocations.KOKIRI_FOREST_SOFT_SOIL, Events.KOKIRI_FOREST_BEAN_PLANTED, lambda s, r, w: is_child(s, r, w) and
                                                     can_use(Items.MAGIC_BEAN, s, w)),
    ])

    ## KF Link's House
    # Locations
    add_locations(Regions.KF_LINKS_HOUSE, world, [
        (Locations.KF_LINKS_HOUSE_COW, lambda s, r, w: is_adult(s, r, w) and
                                                           can_use(Items.EPONAS_SONG, s, w) and
                                                           has_item(Events.GOTTEN_LINKS_COW, s, w)),
        (Locations.KF_LINKS_HOUSE_POT, lambda s, r, w: can_break_pots(s, w))

    ])
    # Connections
    connect_regions(Regions.KF_LINKS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF Mido's House
    # Locations
    add_locations(Regions.KF_MIDOS_HOUSE, world, [
        (Locations.KF_MIDO_TOP_LEFT_CHEST, lambda s, r, w: True),
        (Locations.KF_MIDO_TOP_RIGHT_CHEST, lambda s, r, w: True),
        (Locations.KF_MIDO_BOTTOM_LEFT_CHEST, lambda s, r, w: True),
        (Locations.KF_MIDO_BOTTOM_RIGHT_CHEST, lambda s, r, w: True)
    ])
    # Connections
    connect_regions(Regions.KF_MIDOS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF Saria's House
    # Locations
    add_locations(Regions.KF_SARIAS_HOUSE, world, [
        (Locations.KF_SARIAS_HOUSE_TOP_LEFT_HEART, lambda s, r, w: True),
        (Locations.KF_SARIAS_HOUSE_TOP_RIGHT_HEART, lambda s, r, w: True),
        (Locations.KF_SARIAS_HOUSE_BOTTOM_LEFT_HEART, lambda s, r, w: True),
        (Locations.KF_SARIAS_HOUSE_BOTTOM_RIGHT_HEART, lambda s, r, w: True)
    ])
    # Connections
    connect_regions(Regions.KF_SARIAS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF House of Twins
    # Locations
    add_locations(Regions.KF_HOUSE_OF_TWINS, world, [
        (Locations.KF_TWINS_HOUSE_POT1, lambda s, r, w: can_break_pots(s, w)),
        (Locations.KF_TWINS_HOUSE_POT2, lambda s, r, w: can_break_pots(s, w))

    ])
    # Connections
    connect_regions(Regions.KF_HOUSE_OF_TWINS, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF Know it All House
    # Locations
    add_locations(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Locations.KF_BROTHERS_HOUSE_POT1, lambda s, r, w: can_break_pots(s, w)),
        (Locations.KF_BROTHERS_HOUSE_POT2, lambda s, r, w: can_break_pots(s, w))

    ])
    # Connections
    connect_regions(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF Kokiri Shop
    # Locations
    add_locations(Regions.KF_KOKIRI_SHOP, world, [
        (Locations.KF_SHOP_ITEM1, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM2, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM3, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM4, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM5, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM6, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM7, lambda s, r, w: True),
        (Locations.KF_SHOP_ITEM8, lambda s, r, w: True)
    ])
    # Connections
    connect_regions(Regions.KF_KOKIRI_SHOP, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## KF Outside Deku Tree
    # Locations
    add_locations(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy_except_suns(s, w)),
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy_except_suns(s, w)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w))
    ])
    # Connections
    connect_regions(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda s, r, w: (is_child(s, r, w))
                                                         and (w.options.closed_forest==2
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, s, w))),
        (Regions.KOKIRI_FOREST, lambda s, r, w:  (is_adult(s, r, w) and
                                                             (can_pass_enemy(s, w, Enemies.BIG_SKULLTULA) or
                                                             has_item(Events.CLEARED_FOREST_TEMPLE, s, w)))
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, s, w)
                                                           or w.options.closed_forest==2)
    ])
    add_events(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (EventLocations.MIDO_OUTSIDE, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda s, r, w: has_item(Items.KOKIRI_SWORD, s, w) and
                                                  has_item(Items.DEKU_SHIELD, s, w)),
    ])

    ## KF Storms Grotto
    # Locations
    add_locations(Regions.KF_STORMS_GROTTO, world, [
        (Locations.KF_STORMS_GROTTO_CHEST, lambda s, r, w: True),
        (Locations.KF_STORMS_GROTTO_FISH, lambda s, r, w: has_bottle(s, w)),
        (Locations.KF_STORMS_GOSSIP_STONE_FAIRY, lambda s, r, w: call_gossip_fairy(s, w)),
        (Locations.KF_STORMS_GOSSIP_STONE_BIG_FAIRY, lambda s, r, w: can_use(Items.SONG_OF_STORMS, s, w)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_LEFT, lambda s, r, w: can_break_lower_hives(s, w)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_RIGHT, lambda s, r, w: can_break_lower_hives(s, w)),
        (Locations.KF_STORMS_GROTTO_GRASS1, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.KF_STORMS_GROTTO_GRASS2, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.KF_STORMS_GROTTO_GRASS3, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.KF_STORMS_GROTTO_GRASS4, lambda s, r, w: can_cut_shrubs(s, w)),
    ])
    # Connections
    connect_regions(Regions.KF_STORMS_GROTTO, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])




