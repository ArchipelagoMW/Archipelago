from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    ZF_GOSSIP_STONE_SONG_FAIRY = "ZF Gossip Stone Song Fairy"
    ZF_BUTTERFLY_FAIRY = "ZF Butterfly Fairy"


def set_region_rules(world: "SohWorld") -> None:
    # Zora's Fountain
    # Events
    add_events(Regions.ZORAS_FOUNTAIN, world, [
        (EventLocations.ZF_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (EventLocations.ZF_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.STICKS, bundle) and at_day(bundle))
    ])
    # Locations
    add_locations(Regions.ZORAS_FOUNTAIN, world, [
        (Locations.ZF_GS_TREE, lambda bundle: is_child(
            bundle) and can_bonk_trees(bundle)),
        (Locations.ZF_GS_ABOVE_THE_LOG,
         lambda bundle: is_child(bundle) and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.ZF_FAIRY_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.ZF_FAIRY_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.ZF_JABU_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle)),
        (Locations.ZF_JABU_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.ZF_NEAR_JABU_POT1, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_NEAR_JABU_POT2, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_NEAR_JABU_POT3, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_NEAR_JABU_POT4, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_TREE, lambda bundle: is_child(
            bundle) and can_bonk_trees(bundle)),
    ])
    # Connections
    connect_regions(Regions.ZORAS_FOUNTAIN, world, [
        (Regions.ZD_BEHIND_KING_ZORA, lambda bundle: True),
        (Regions.ZF_ICEBERGS, lambda bundle: is_adult(bundle)),
        (Regions.ZF_LAKEBED, lambda bundle: can_use(Items.IRON_BOOTS, bundle)),
        (Regions.ZF_HIDDEN_CAVE, lambda bundle: can_use(
            Items.SILVER_GAUNTLETS, bundle) and blast_or_smash(bundle)),
        (Regions.ZF_ROCK, lambda bundle: is_adult(
            bundle) and can_use(Items.SCARECROW, bundle)),
        (Regions.JABU_JABUS_BELLY_ENTRYWAY,
         lambda bundle: is_child(bundle) and (can_use(Items.BOTTLE_WITH_FISH, bundle) or world.options.jabu_jabu.value == 1)),
        (Regions.ZF_GREAT_FAIRY_FOUNTAIN, lambda bundle: has_explosives(bundle) or (can_do_trick(
            Tricks.ZF_GREAT_FAIRY_WITHOUT_EXPLOSIVES, bundle) and can_use(Items.MEGATON_HAMMER, bundle) and can_use(Items.SILVER_GAUNTLETS, bundle)))
    ])

    # Zora's Fountains Icebergs
    # Locations
    add_locations(Regions.ZF_ICEBERGS, world, [
        (Locations.ZF_ICEBERG_FREESTANDING_POH, lambda bundle: is_adult(bundle))
    ])
    # Connections
    connect_regions(Regions.ZF_ICEBERGS, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_use(Items.HOVER_BOOTS, bundle)),
        (Regions.ZF_LAKEBED, lambda bundle: can_use(Items.IRON_BOOTS, bundle)),
        (Regions.ZF_LEDGE, lambda bundle: True)
    ])

    # Zora's Fountain Lakebed
    # Locations
    add_locations(Regions.ZF_LAKEBED, world, [
        (Locations.ZF_BOTTOM_FREESTANDING_POH,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTH_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHEAST_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHEAST_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTH_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHWEST_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHWEST_INNER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTH_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHEAST_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHEAST_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTH_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHWEST_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHWEST_MIDDLE_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTH_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHEAST_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHEAST_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTH_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_SOUTHWEST_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
        (Locations.ZF_BOTTOM_NORTHWEST_OUTER_RUPEE,
         lambda bundle: is_adult(bundle) and can_use(Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 16),
    ])
    # Connections
    connect_regions(Regions.ZF_LAKEBED, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: has_item(Items.BRONZE_SCALE, bundle))
    ])

    # Zora's Fountain Ledge
    # Connections
    connect_regions(Regions.ZF_LEDGE, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.ZF_ICEBERGS, lambda bundle: is_adult(bundle)),
        (Regions.ZF_LAKEBED, lambda bundle: can_use(Items.IRON_BOOTS, bundle)),
        (Regions.ICE_CAVERN_ENTRYWAY, lambda bundle: True)
    ])

    # Zora's Fountain Hidden Cave
    # Locations
    add_locations(Regions.ZF_HIDDEN_CAVE, world, [
        (Locations.ZF_HIDDEN_CAVE_POT1, lambda bundle: is_adult(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_HIDDEN_CAVE_POT2, lambda bundle: is_adult(
            bundle) and can_break_pots(bundle)),
        (Locations.ZF_HIDDEN_CAVE_POT3, lambda bundle: is_adult(
            bundle) and can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.ZF_HIDDEN_CAVE, world, [
        (Regions.ZF_HIDDEN_LEDGE, lambda bundle: True)
    ])

    # Zora's Fountain Hidden Ledge
    # Locations
    add_locations(Regions.ZF_HIDDEN_LEDGE, world, [
        (Locations.ZF_GS_HIDDEN_CAVE, lambda bundle: is_adult(bundle) and can_get_enemy_drop(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOMB_THROW) and can_get_nighttime_gs(bundle))
    ])
    # Connections
    connect_regions(Regions.ZF_HIDDEN_LEDGE, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or take_damage(bundle)),
        (Regions.ZF_HIDDEN_CAVE, lambda bundle: True)
    ])

    # Zora's Fountain Rock
    # Connections
    connect_regions(Regions.ZF_ROCK, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: True)
    ])

    # Zora's Fountain Great Fairy Fountain
    # Locations
    add_locations(Regions.ZF_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.ZF_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.ZF_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.ZORAS_FOUNTAIN, lambda bundle: True)
    ])
