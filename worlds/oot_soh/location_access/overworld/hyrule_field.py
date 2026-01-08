from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    HF_BIG_POE = "HF Big Poe"
    HF_RUNNING_MAN = "HF Running Man"
    HF_COW_GROTTO_BEHIND_WEBS_GOSSIP_STONE_SONG_FAIRY = "HF Cow Grotto Behind Webs Gossip Stone Song Fairy"
    HF_COW_GROTTO_BEHIND_WEBS_BUGS_SHRUB = "HF Cow Grotto Behind Webs Bugs Shrub"
    HF_FAIRY_GROTTO_FAIRY = "HF Fairy Grotto Fairy"
    HF_SOUTHEAST_GROTTO_GOSSIP_STONE_SONG_FAIRY = "HF Southeast Grotto Gossip Stone Song Fairy"
    HF_SOUTHEAST_GROTTO_BUTTERFLY_FAIRY = "HF Southeast Grotto Butterfly Fairy"
    HF_SOUTHEAST_GROTTO_BUG_GRASS = "HF Southeast Grotto Bugs"
    HF_SOUTHEAST_GROTTO_PUDDLE_FISH = "HF Southeast Grotto Puddle Fish"
    HF_OPEN_GROTTO_GOSSIP_STONE_SONG_FAIRY = "HF Open Grotto Gossip Stone Song Fairy"
    HF_OPEN_GROTTO_BUTTERFLY_FAIRY = "HF Open Grotto Butterfly Fairy"
    HF_OPEN_GROTTO_BUG_GRASS = "HF Open Grotto Bugs"
    HF_OPEN_GROTTO_PUDDLE_FISH = "HF Open Grotto Puddle Fish"
    HF_NEAR_MARKET_GROTTO_GOSSIP_STONE_SONG_FAIRY = "HF Near Market Grotto Gossip Stone Song Fairy"
    HF_NEAR_MARKET_GROTTO_BUTTERFLY_FAIRY = "HF Near Market Grotto Butterfly Fairy"
    HF_NEAR_MARKET_GROTTO_BUG_GRASS = "HF Near Market Grotto Bugs"
    HF_NEAR_MARKET_GROTTO_PUDDLE_FISH = "HF Near Market Grotto Puddle Fish"
    HF_DAY_NIGHT_CYCLE_CHILD = "HF Day Night Cycle Child"
    HF_DAY_NIGHT_CYCLE_ADULT = "HF Day Night Cycle Adult"


def set_region_rules(world: "SohWorld") -> None:
    # Hyrule Field
    # Events
    add_events(Regions.HYRULE_FIELD, world, [
        (EventLocations.HF_BIG_POE, Events.CAN_DEFEAT_BIG_POE, lambda bundle: (has_bottle(bundle) and
                                                                               can_use(Items.FAIRY_BOW, bundle) and
                                                                               (can_use(Items.EPONA, bundle) or can_do_trick(Tricks.HF_BIG_POE_WITHOUT_EPONA, bundle)))),
        (EventLocations.HF_RUNNING_MAN, Events.SOLD_BUNNY_HOOD, lambda bundle: (is_child(bundle) and
                                                                                has_item(Events.CAN_BORROW_BUNNY_HOOD, bundle) and
                                                                                has_item(Items.KOKIRIS_EMERALD, bundle) and
                                                                                has_item(Items.GORONS_RUBY, bundle) and
                                                                                has_item(Items.ZORAS_SAPPHIRE, bundle) and
                                                                                has_item(Items.CHILD_WALLET, bundle))),
        (EventLocations.HF_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
        (EventLocations.HF_DAY_NIGHT_CYCLE_ADULT,
         Events.ADULT_CAN_PASS_TIME, lambda bundle: is_adult(bundle)),
    ])
    # Locations
    add_locations(Regions.HYRULE_FIELD, world, [
        (Locations.HF_OCARINA_OF_TIME_ITEM, lambda bundle: (is_child(bundle) and
                                                            stone_count(bundle) == 3 and
                                                            has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.SONG_FROM_OCARINA_OF_TIME, lambda bundle: (is_child(bundle) and
                                                              stone_count(bundle) == 3 and
                                                              has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.HF_POND_SONG_OF_STORMS_FAIRY, lambda bundle: (
            can_use(Items.SONG_OF_STORMS, bundle))),
        (Locations.HF_CENTRAL_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS4, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS5, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS6, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS7, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS8, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS9, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS10, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS11, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_CENTRAL_GRASS12, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS4, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS5, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS6, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS7, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS8, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS9, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS10, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS11, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTH_GRASS12, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS4, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS5, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS6, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS7, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS8, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS9, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS10, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS11, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS12, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS4, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS5, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS6, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS7, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS8, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS9, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS10, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS11, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GRASS12, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS4, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS5, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS6, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS7, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS8, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS9, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS10, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS11, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_KFGRASS12, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_LLR_TREE, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_LH_TREE, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_CHILD_NEAR_GV_TREE, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_ADULT_NEAR_GV_TREE, lambda bundle: (
            is_adult(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_NEAR_ZR_TREE, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_KAK_TREE, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_KAK_SMALL_TREE, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_MARKET_TREE_1, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_MARKET_TREE_2, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NEAR_MARKET_TREE_3, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_1, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_2, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_3, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_4, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_5, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_NORTHWEST_TREE_6, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_1, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_2, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_3, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_4, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_5, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_EAST_TREE_6, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_1, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_2, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_3, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_4, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_5, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_6, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_7, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_8, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_9, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_10, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_11, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_12, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_13, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_14, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_15, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_16, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_17, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_18, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_SOUTHEAST_TREE_19, lambda bundle: (can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_1, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_2, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_3, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_4, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_5, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_CHILD_SOUTHEAST_TREE_6, lambda bundle: (
            is_child(bundle) and can_bonk_trees(bundle))),
        (Locations.HF_TEKTITE_GROTTO_TREE, lambda bundle: (can_bonk_trees(bundle)))
    ])
    # Connections
    connect_regions(Regions.HYRULE_FIELD, world, [
        (Regions.LW_BRIDGE, lambda bundle: True),
        (Regions.LAKE_HYLIA, lambda bundle: True),
        (Regions.GERUDO_VALLEY, lambda bundle: True),
        (Regions.MARKET_ENTRANCE, lambda bundle: True),
        (Regions.KAKARIKO_VILLAGE, lambda bundle: True),
        (Regions.ZR_FRONT, lambda bundle: True),
        (Regions.LON_LON_RANCH, lambda bundle: True),
        (Regions.HF_SOUTHEAST_GROTTO, lambda bundle: (blast_or_smash(bundle))),
        (Regions.HF_OPEN_GROTTO, lambda bundle: True),
        (Regions.HF_INSIDE_FENCE_GROTTO, lambda bundle: (
            can_open_bomb_grotto(bundle))),
        (Regions.HF_COW_GROTTO, lambda bundle: ((can_use(Items.MEGATON_HAMMER,
         bundle) or is_child(bundle)) and can_open_bomb_grotto(bundle))),
        (Regions.HF_NEAR_MARKET_GROTTO, lambda bundle: (blast_or_smash(bundle))),
        (Regions.HF_FAIRY_GROTTO, lambda bundle: (blast_or_smash(bundle))),
        (Regions.HF_NEAR_KAK_GROTTO, lambda bundle: (can_open_bomb_grotto(bundle))),
        (Regions.HF_TEKTITE_GROTTO, lambda bundle: (can_open_bomb_grotto(bundle))),
    ])

    # HF Southeast Grotto
    # Events
    add_events(Regions.HF_SOUTHEAST_GROTTO, world, [
        (EventLocations.HF_SOUTHEAST_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.HF_SOUTHEAST_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.HF_SOUTHEAST_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.HF_SOUTHEAST_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.HF_SOUTHEAST_GROTTO, world, [
        (Locations.HF_SOUTHEAST_GROTTO_CHEST, lambda bundle: True),
        (Locations.HF_SOUTHEAST_GROTTO_FISH, lambda bundle: (has_bottle(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: (call_gossip_fairy(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: (can_use(Items.SONG_OF_STORMS, bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_BEEHIVE_LEFT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GRASS1,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GRASS2,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GRASS3,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_SOUTHEAST_GROTTO_GRASS4,
         lambda bundle: (can_cut_shrubs(bundle)))
    ])
    # Connections
    connect_regions(Regions.HF_SOUTHEAST_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Open Grotto
    # Events
    add_events(Regions.HF_OPEN_GROTTO, world, [
        (EventLocations.HF_OPEN_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.HF_OPEN_GROTTO_BUTTERFLY_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.HF_OPEN_GROTTO_BUG_GRASS, Events.CAN_ACCESS_BUGS,
         lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.HF_OPEN_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.HF_OPEN_GROTTO, world, [
        (Locations.HF_OPEN_GROTTO_CHEST, lambda bundle: True),
        (Locations.HF_OPEN_GROTTO_FISH, lambda bundle: (has_bottle(bundle))),
        (Locations.HF_OPEN_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: (call_gossip_fairy(bundle))),
        (Locations.HF_OPEN_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: (can_use(Items.SONG_OF_STORMS, bundle))),
        (Locations.HF_OPEN_GROTTO_BEEHIVE_LEFT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_OPEN_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_OPEN_GROTTO_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_OPEN_GROTTO_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_OPEN_GROTTO_GRASS3, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_OPEN_GROTTO_GRASS4, lambda bundle: (can_cut_shrubs(bundle)))
    ])
    # Connections
    connect_regions(Regions.HF_OPEN_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Inside Fence Grotto
    # Locations
    add_locations(Regions.HF_INSIDE_FENCE_GROTTO, world, [
        (Locations.HF_DEKU_SCRUB_GROTTO, lambda bundle: (can_stun_deku(bundle))),
        (Locations.HF_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_FENCE_GROTTO_STORMS_FAIRY, lambda bundle: (
            can_use(Items.SONG_OF_STORMS, bundle)))
    ])
    # Connections
    connect_regions(Regions.HF_INSIDE_FENCE_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Cow Grotto
    # Connections
    connect_regions(Regions.HF_COW_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True),
        (Regions.HF_COW_GROTTO_BEHIND_WEBS,
         lambda bundle: (has_fire_source(bundle)))
    ])

    # HF Cow Grotto Behind Webs
    # Events
    add_events(Regions.HF_COW_GROTTO_BEHIND_WEBS, world, [
        (EventLocations.HF_COW_GROTTO_BEHIND_WEBS_BUGS_SHRUB,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.HF_COW_GROTTO_BEHIND_WEBS_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle)))
    ])
    # Locations
    add_locations(Regions.HF_COW_GROTTO_BEHIND_WEBS, world, [
        (Locations.HF_GS_COW_GROTTO, lambda bundle: (can_get_enemy_drop(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))),
        (Locations.HF_COW_GROTTO_COW, lambda bundle: (
            can_use(Items.EPONAS_SONG, bundle))),
        (Locations.HF_COW_GROTTO_GOSSIP_STONE_FAIRY,
         lambda bundle: (call_gossip_fairy(bundle))),
        (Locations.HF_COW_GROTTO_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: (can_use(Items.SONG_OF_STORMS, bundle))),
        (Locations.HF_COW_GROTTO_POT1, lambda bundle: (can_break_pots(bundle))),
        (Locations.HF_COW_GROTTO_POT2, lambda bundle: (can_break_pots(bundle))),
        (Locations.HF_COW_GROTTO_GRASS1, lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_COW_GROTTO_GRASS2, lambda bundle: (can_cut_shrubs(bundle))),
    ])
    # Connections
    connect_regions(Regions.HF_COW_GROTTO_BEHIND_WEBS, world, [
        (Regions.HF_COW_GROTTO, lambda bundle: True)
    ])

    # HF Near Market Grotto
    # Events
    add_events(Regions.HF_NEAR_MARKET_GROTTO, world, [
        (EventLocations.HF_NEAR_MARKET_GROTTO_GOSSIP_STONE_SONG_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (call_gossip_fairy(bundle))),
        (EventLocations.HF_NEAR_MARKET_GROTTO_BUTTERFLY_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: (can_use(Items.STICKS, bundle))),
        (EventLocations.HF_NEAR_MARKET_GROTTO_BUG_GRASS,
         Events.CAN_ACCESS_BUGS, lambda bundle: (can_cut_shrubs(bundle))),
        (EventLocations.HF_NEAR_MARKET_GROTTO_PUDDLE_FISH,
         Events.CAN_ACCESS_FISH, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.HF_NEAR_MARKET_GROTTO, world, [
        (Locations.HF_NEAR_MARKET_GROTTO_CHEST, lambda bundle: True),
        (Locations.HF_NEAR_MARKET_GROTTO_FISH,
         lambda bundle: (has_bottle(bundle))),
        (Locations.HF_NEAR_MARKET_GOSSIP_STONE_FAIRY,
         lambda bundle: (call_gossip_fairy(bundle))),
        (Locations.HF_NEAR_MARKET_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: (can_use(Items.SONG_OF_STORMS, bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_BEEHIVE_LEFT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_BEEHIVE_RIGHT,
         lambda bundle: (can_break_lower_hives(bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_GRASS1,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_GRASS2,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_GRASS3,
         lambda bundle: (can_cut_shrubs(bundle))),
        (Locations.HF_NEAR_MARKET_GROTTO_GRASS4,
         lambda bundle: (can_cut_shrubs(bundle)))
    ])
    # Connections
    connect_regions(Regions.HF_NEAR_MARKET_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Fairy Grotto
    # Events
    add_events(Regions.HF_FAIRY_GROTTO, world, [
        (EventLocations.HF_FAIRY_GROTTO_FAIRY,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.HF_FAIRY_GROTTO, world, [
        (Locations.HF_FAIRY_GROTTO_FAIRY1, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY2, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY3, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY4, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY5, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY6, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY7, lambda bundle: True),
        (Locations.HF_FAIRY_GROTTO_FAIRY8, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.HF_FAIRY_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Near Kak Grotto
    # Locations
    add_locations(Regions.HF_NEAR_KAK_GROTTO, world, [
        (Locations.HF_GS_STONE_BRIDGE_TREE_GROTTO,
         lambda bundle: hookshot_or_boomerang(bundle))
    ])
    # Connections
    connect_regions(Regions.HF_NEAR_KAK_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])

    # HF Tektite Grotto
    # Locations
    add_locations(Regions.HF_TEKTITE_GROTTO, world, [
        (Locations.HF_TEKTITE_GROTTO_FREESTANDING_POH, lambda bundle: (has_item(Items.GOLDEN_SCALE, bundle) or
                                                                       can_use(Items.IRON_BOOTS, bundle)))
    ])
    # Connections
    connect_regions(Regions.HF_TEKTITE_GROTTO, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True)
    ])
