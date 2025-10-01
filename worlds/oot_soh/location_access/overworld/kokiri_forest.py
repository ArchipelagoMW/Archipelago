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
        (Locations.KF_KOKIRI_SWORD_CHEST, lambda bundle: is_child(bundle)),
        (Locations.KF_GS_KNOW_IT_ALL_HOUSE, lambda bundle: (can_attack(bundle) and
                                                                        is_child(bundle) and
                                                                        can_get_nighttime_gs(bundle))),
        (Locations.KF_GS_BEAN_PATCH, lambda bundle: can_attack(bundle) and
                                                         is_child(bundle) and
                                                         can_use(Items.BOTTLE_WITH_BUGS, bundle)),
        (Locations.KF_GS_HOUSE_OF_TWINS, lambda bundle: is_adult(bundle) and
                                                             (hookshot_or_boomerang(bundle)
                                                              or (can_do_trick("Kokiri Forest Gold Skulltula with Hover Boots", bundle)
                                                                  and can_use(Items.HOVER_BOOTS, bundle))) and can_get_nighttime_gs(bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle)
                                                              and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle)
                                                              and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle)
                                                              and has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle)
                                                              and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_BRIDGE_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_BEHIND_MIDOS_HOUSE_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_SOUTH_GRASS_WEST_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_SOUTH_GRASS_EAST_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_NORTH_GRASS_WEST_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_NORTH_GRASS_EAST_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_BOULDER_MAZE_FIRST_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_BOULDER_MAZE_SECOND_RUPEE, lambda bundle: is_child(bundle)),
        (Locations.KF_BEAN_PLATFORM_RUPEE1, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE2, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE3, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE4, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE5, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE6, lambda bundle:  is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RED_RUPEE, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                   can_use(Items.BOOMERANG, bundle) or
                                                                   has_item(Events.KOKIRI_FOREST_BEAN_PLANTED, bundle))),
        (Locations.KF_SARIAS_ROOF_EAST_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_SARIAS_ROOF_NORTH_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_SARIAS_ROOF_WEST_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_CHILD_GRASS1, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS2, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS3, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS4, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS5, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS6, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS7, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS8, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS9, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS10, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS11, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS12, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE1, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE2, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE3, lambda bundle: (is_child(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS1, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS2, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS3, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS4, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS5, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS6, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS7, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS8, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS9, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS10, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS11, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS12, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS13, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS14, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS15, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS16, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS17, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS19, lambda bundle: (is_adult(bundle)
                                                        and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS20, lambda bundle: (is_adult(bundle)))
    ])
    # Connections
    connect_regions(Regions.KOKIRI_FOREST, world, [
        (Regions.KF_LINKS_HOUSE, lambda bundle: True),
        (Regions.KF_MIDOS_HOUSE, lambda bundle: True),
        (Regions.KF_SARIAS_HOUSE, lambda bundle: True),
        (Regions.KF_HOUSE_OF_TWINS, lambda bundle: True),
        (Regions.KF_KNOW_IT_ALL_HOUSE, lambda bundle: True),
        (Regions.KF_KOKIRI_SHOP, lambda bundle: True),
        (Regions.KF_OUTSIDE_DEKU_TREE, lambda bundle: (is_adult(bundle) and
                                                             (can_pass_enemy(bundle, Enemies.BIG_SKULLTULA) or
                                                             has_item(Events.CLEARED_FOREST_TEMPLE, bundle)))
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle)
                                                           or world.options.closed_forest==2),  # Todo, maybe create a helper for handling settings
        (Regions.LOST_WOODS, lambda bundle: True),
        (Regions.LW_BRIDGE_FROM_FOREST, lambda bundle: world.options.closed_forest>=1 or is_adult(bundle) or
                                                            has_item(Events.CLEARED_DEKU_TREE, bundle)),
        (Regions.KF_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle))
    ])
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        (EventLocations.MIDO, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda bundle: has_item(Items.KOKIRI_SWORD, bundle) 
                                                                    and has_item(Items.DEKU_SHIELD, bundle)),
        (EventLocations.KOKIRI_FOREST_SOFT_SOIL, Events.KOKIRI_FOREST_BEAN_PLANTED, lambda bundle: is_child(bundle) and
                                                     can_use(Items.MAGIC_BEAN, bundle)),
    ])

    ## KF Link's House
    # Locations
    add_locations(Regions.KF_LINKS_HOUSE, world, [
        (Locations.KF_LINKS_HOUSE_COW, lambda bundle: is_adult(bundle) and
                                                           can_use(Items.EPONAS_SONG, bundle) and
                                                           has_item(Events.GOTTEN_LINKS_COW, bundle)),
        (Locations.KF_LINKS_HOUSE_POT, lambda bundle: can_break_pots(bundle))

    ])
    # Connections
    connect_regions(Regions.KF_LINKS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF Mido's House
    # Locations
    add_locations(Regions.KF_MIDOS_HOUSE, world, [
        (Locations.KF_MIDO_TOP_LEFT_CHEST, lambda bundle: True),
        (Locations.KF_MIDO_TOP_RIGHT_CHEST, lambda bundle: True),
        (Locations.KF_MIDO_BOTTOM_LEFT_CHEST, lambda bundle: True),
        (Locations.KF_MIDO_BOTTOM_RIGHT_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.KF_MIDOS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF Saria's House
    # Locations
    add_locations(Regions.KF_SARIAS_HOUSE, world, [
        (Locations.KF_SARIAS_HOUSE_TOP_LEFT_HEART, lambda bundle: True),
        (Locations.KF_SARIAS_HOUSE_TOP_RIGHT_HEART, lambda bundle: True),
        (Locations.KF_SARIAS_HOUSE_BOTTOM_LEFT_HEART, lambda bundle: True),
        (Locations.KF_SARIAS_HOUSE_BOTTOM_RIGHT_HEART, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.KF_SARIAS_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF House of Twins
    # Locations
    add_locations(Regions.KF_HOUSE_OF_TWINS, world, [
        (Locations.KF_TWINS_HOUSE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.KF_TWINS_HOUSE_POT2, lambda bundle: can_break_pots(bundle))

    ])
    # Connections
    connect_regions(Regions.KF_HOUSE_OF_TWINS, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF Know it All House
    # Locations
    add_locations(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Locations.KF_BROTHERS_HOUSE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.KF_BROTHERS_HOUSE_POT2, lambda bundle: can_break_pots(bundle))

    ])
    # Connections
    connect_regions(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF Kokiri Shop
    # Locations
    add_locations(Regions.KF_KOKIRI_SHOP, world, [
        (Locations.KF_SHOP_ITEM1, lambda bundle: True),
        (Locations.KF_SHOP_ITEM2, lambda bundle: True),
        (Locations.KF_SHOP_ITEM3, lambda bundle: True),
        (Locations.KF_SHOP_ITEM4, lambda bundle: True),
        (Locations.KF_SHOP_ITEM5, lambda bundle: True),
        (Locations.KF_SHOP_ITEM6, lambda bundle: True),
        (Locations.KF_SHOP_ITEM7, lambda bundle: True),
        (Locations.KF_SHOP_ITEM8, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.KF_KOKIRI_SHOP, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    ## KF Outside Deku Tree
    # Locations
    add_locations(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda bundle: (is_child(bundle))
                                                         and (world.options.closed_forest==2
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle))),
        (Regions.KOKIRI_FOREST, lambda bundle:  (is_adult(bundle) and
                                                             (can_pass_enemy(bundle, Enemies.BIG_SKULLTULA) or
                                                             has_item(Events.CLEARED_FOREST_TEMPLE, bundle)))
                                                            or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle)
                                                           or world.options.closed_forest==2)
    ])
    add_events(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (EventLocations.MIDO_OUTSIDE, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda bundle: has_item(Items.KOKIRI_SWORD, bundle) and
                                                  has_item(Items.DEKU_SHIELD, bundle)),
    ])

    ## KF Storms Grotto
    # Locations
    add_locations(Regions.KF_STORMS_GROTTO, world, [
        (Locations.KF_STORMS_GROTTO_CHEST, lambda bundle: True),
        (Locations.KF_STORMS_GROTTO_FISH, lambda bundle: has_bottle(bundle)),
        (Locations.KF_STORMS_GOSSIP_STONE_FAIRY, lambda bundle: call_gossip_fairy(bundle)),
        (Locations.KF_STORMS_GOSSIP_STONE_BIG_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_LEFT, lambda bundle: can_break_lower_hives(bundle)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_RIGHT, lambda bundle: can_break_lower_hives(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.KF_STORMS_GROTTO, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])




