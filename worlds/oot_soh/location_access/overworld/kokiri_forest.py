from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    MIDO = "Mido"
    MIDO_FROM_OUTSIDE_DEKU_TREE = "Mido From Outside Deku Tree"
    KF_GOSSIP_STONE_SONG_FAIRY = "KF Gossip Stone Song Fairy"
    KF_SOFT_SOIL = "KF Soft Soil"
    KF_DEKU_TREE_DEKU_BABA_NUTS = "KF Deku Tree Deku Baba Nuts"
    KF_DEKU_TREE_DEKU_BABA_STICKS = "KF Deku Tree Deku Baba Sticks"
    KF_DEKU_TREE_GOSSIP_STONE_SONG_FAIRY = "KF Deku Tree Gossip Stone Song Fairy"
    KF_STORMS_GROTTO_GOSSIP_STONE_SONG_FAIRY = "KF Storms Grotto Gossip Stone Song Fairy"
    KF_STORMS_GROTTO_BUTTERFLY_FAIRY = "KF Storms Grotto Butterfly Fairy"
    KF_STORMS_GROTTO_BUG_GRASS = "KF Storms Grotto Bugs"
    KF_STORMS_GROTTO_PUDDLE_FISH = "KF Storms Grotto Puddle Fish"


class LocalEvents(StrEnum):
    MIDO_SWORD_AND_SHIELD = "Showed Mido the Sword and Shield"
    KF_BEAN_PLANTED = "KF Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # Kokiri Forest
    # Events
    add_events(Regions.KOKIRI_FOREST, world, [
        (EventLocations.MIDO, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda bundle: (is_child(bundle)
                                                                                 and has_item(Items.KOKIRI_SWORD, bundle)
                                                                                 and has_item(Items.DEKU_SHIELD, bundle))
         or world.options.closed_forest.value == 2),
        (EventLocations.KF_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (EventLocations.KF_SOFT_SOIL, LocalEvents.KF_BEAN_PLANTED, lambda bundle: is_child(bundle) and
         can_use(Items.MAGIC_BEAN, bundle)),
    ])
    # Locations
    add_locations(Regions.KOKIRI_FOREST, world, [
        (Locations.KF_KOKIRI_SWORD_CHEST, lambda bundle: is_child(bundle)),
        (Locations.KF_GS_KNOW_IT_ALL_HOUSE, lambda bundle: (is_child(bundle) and
                                                            can_attack(bundle) and
                                                            can_get_nighttime_gs(bundle))),
        (Locations.KF_GS_BEAN_PATCH, lambda bundle: can_attack(bundle) and
         is_child(bundle) and
         can_use(Items.BOTTLE_WITH_BUGS, bundle)),
        (Locations.KF_GS_HOUSE_OF_TWINS, lambda bundle: is_adult(bundle) and
         (hookshot_or_boomerang(bundle)
          or (can_do_trick(Tricks.KF_ADULT_GS, bundle)
              and can_use(Items.HOVER_BOOTS, bundle))) and can_get_nighttime_gs(bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle)
         and has_item(LocalEvents.KF_BEAN_PLANTED, bundle)
         and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle)
         and has_item(LocalEvents.KF_BEAN_PLANTED, bundle)
         and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle)
         and has_item(LocalEvents.KF_BEAN_PLANTED, bundle)
         and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
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
                                                                                 has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE2, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                 can_use(Items.BOOMERANG, bundle) or
                                                                                 has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE3, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                 can_use(Items.BOOMERANG, bundle) or
                                                                                 has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE4, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                 can_use(Items.BOOMERANG, bundle) or
                                                                                 has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE5, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                 can_use(Items.BOOMERANG, bundle) or
                                                                                 has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RUPEE6, lambda bundle:  is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                  can_use(Items.BOOMERANG, bundle) or
                                                                                  has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_BEAN_PLATFORM_RED_RUPEE, lambda bundle: is_adult(bundle) and (has_item(Items.HOVER_BOOTS, bundle) or
                                                                                    can_use(Items.BOOMERANG, bundle) or
                                                                                    has_item(LocalEvents.KF_BEAN_PLANTED, bundle))),
        (Locations.KF_SARIAS_ROOF_EAST_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_SARIAS_ROOF_NORTH_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_SARIAS_ROOF_WEST_HEART, lambda bundle: is_child(bundle)),
        (Locations.KF_CHILD_GRASS1, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS2, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS3, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS4, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS5, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS6, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS7, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS8, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS9, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS10, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS11, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS12, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE1, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE2, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_CHILD_GRASS_MAZE3, lambda bundle: (
            is_child(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS1, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS2, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS3, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS4, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS5, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS6, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS7, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS8, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS9, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS10, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS11, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS12, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS13, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS14, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS15, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS16, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS17, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS18, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS19, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
        (Locations.KF_ADULT_GRASS20, lambda bundle: (
            is_adult(bundle) and can_cut_shrubs(bundle))),
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
                                                        has_item(Events.FOREST_TEMPLE_COMPLETED, bundle)))
         or (is_child(bundle) and has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle))
         # Todo, maybe create a helper for handling settings
         or world.options.closed_forest.value == 2),
        (Regions.LOST_WOODS, lambda bundle: True),
        (Regions.LW_BRIDGE_FROM_FOREST, lambda bundle: world.options.closed_forest.value >= 1 or is_adult(bundle) or
         has_item(Events.DEKU_TREE_COMPLETED, bundle)),
        (Regions.KF_STORMS_GROTTO, lambda bundle: can_open_storms_grotto(bundle))
    ])

    # KF Outside Deku Tree
    # Locations
    add_events(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (EventLocations.KF_DEKU_TREE_DEKU_BABA_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: (can_get_deku_baba_nuts(bundle))),
        (EventLocations.KF_DEKU_TREE_DEKU_BABA_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: (can_get_deku_baba_sticks(bundle))),
        (EventLocations.MIDO_FROM_OUTSIDE_DEKU_TREE, LocalEvents.MIDO_SWORD_AND_SHIELD, lambda bundle: (is_child(bundle)
                                                                                                        and has_item(Items.KOKIRI_SWORD, bundle)
                                                                                                        and has_item(Items.DEKU_SHIELD, bundle))
         or world.options.closed_forest.value == 2),
        (EventLocations.KF_DEKU_TREE_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: (call_gossip_fairy_except_suns(bundle))),
    ])
    add_locations(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_DEKU_TREE_LEFT_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.KF_DEKU_TREE_RIGHT_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
    ])
    # Connections
    connect_regions(Regions.KF_OUTSIDE_DEKU_TREE, world, [
        (Regions.DEKU_TREE_ENTRYWAY, lambda bundle: (is_child(bundle))
         # Todo: Add dungeons shuffle rule when entrance shuffle is implementedd
         and (world.options.closed_forest.value == 2
              or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle))),
        (Regions.KOKIRI_FOREST, lambda bundle:  (is_adult(bundle) and
                                                 (can_pass_enemy(bundle, Enemies.BIG_SKULLTULA) or
                                                  has_item(Events.FOREST_TEMPLE_COMPLETED, bundle)))
         or has_item(LocalEvents.MIDO_SWORD_AND_SHIELD, bundle)
         or world.options.closed_forest.value == 2)
    ])

    # KF Link's House
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

    # KF Mido's House
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

    # KF Saria's House
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

    # KF House of Twins
    # Locations
    add_locations(Regions.KF_HOUSE_OF_TWINS, world, [
        (Locations.KF_TWINS_HOUSE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.KF_TWINS_HOUSE_POT2, lambda bundle: can_break_pots(bundle))

    ])
    # Connections
    connect_regions(Regions.KF_HOUSE_OF_TWINS, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    # KF Know it All House
    # Locations
    add_locations(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Locations.KF_BROTHERS_HOUSE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.KF_BROTHERS_HOUSE_POT2, lambda bundle: can_break_pots(bundle))

    ])
    # Connections
    connect_regions(Regions.KF_KNOW_IT_ALL_HOUSE, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])

    # KF Kokiri Shop
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

    # KF Storms Grotto
    # Events
    add_events(Regions.KF_STORMS_GROTTO, world, [
        (EventLocations.KF_STORMS_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.KF_STORMS_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.KF_STORMS_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.KF_STORMS_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.KF_STORMS_GROTTO, world, [
        (Locations.KF_STORMS_GROTTO_CHEST, lambda bundle: True),
        (Locations.KF_STORMS_GROTTO_FISH, lambda bundle: has_bottle(bundle)),
        (Locations.KF_STORMS_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.KF_STORMS_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_LEFT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.KF_STORMS_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: can_break_lower_hives(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS1, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS2, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS3, lambda bundle: can_cut_shrubs(bundle)),
        (Locations.KF_STORMS_GROTTO_GRASS4, lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.KF_STORMS_GROTTO, world, [
        (Regions.KOKIRI_FOREST, lambda bundle: True)
    ])
