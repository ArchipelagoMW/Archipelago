from BaseClasses import MultiWorld, Item, EntranceType
from worlds.AutoWorld import LogicMixin
from ..World import OracleOfSeasonsWorld
from ..data.logic.DungeonsLogic import *
from ..data.logic.OverworldLogic import *
from ..data.logic.SubrosiaLogic import *


def create_randomizable_connections(world: OracleOfSeasonsWorld, prefix: str,
                                    vanilla_connections: dict[str, str], outer_group: int, inner_group: int):
    for reg1, reg2 in vanilla_connections.items():
        region_1 = world.get_region(reg1)
        region_2 = world.get_region(reg2)

        entrance = region_1.create_exit(f"{prefix}{reg1}")
        entrance.randomization_group = outer_group
        entrance.randomization_type = EntranceType.TWO_WAY

        entrance = region_1.create_er_target(f"{prefix}{reg1}")
        entrance.randomization_group = outer_group
        entrance.randomization_type = EntranceType.TWO_WAY

        entrance = region_2.create_exit(f"{prefix}{reg2}")
        entrance.randomization_group = inner_group
        entrance.randomization_type = EntranceType.TWO_WAY

        entrance = region_2.create_er_target(f"{prefix}{reg2}")
        entrance.randomization_group = inner_group
        entrance.randomization_type = EntranceType.TWO_WAY


def create_connections(world: OracleOfSeasonsWorld, player: int, origin_name: str, options):
    all_logic = [
        make_holodrum_logic(player, origin_name, options),
        make_subrosia_logic(player),
        make_d0_logic(player),
        make_d1_logic(player),
        make_d2_logic(player),
        make_d3_logic(player),
        make_d4_logic(player),
        make_d5_logic(player),
        make_d6_logic(player),
        make_d7_logic(player),
        make_d8_logic(player),

        make_samasa_d11_logic(player, options),
        make_d11_logic(player, options)
    ]

    if world.options.shuffle_dungeons:
        create_randomizable_connections(world, "", world.dungeon_entrances,
                                        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD,
                                        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE)
    else:
        dungeon_entrances = []
        for reg1, reg2 in world.dungeon_entrances.items():
            dungeon_entrances.append([reg1, reg2, True, None])
        all_logic.append(dungeon_entrances)

    if world.options.shuffle_portals:
        create_randomizable_connections(world, "enter ", PORTAL_CONNECTIONS,
                                        OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD,
                                        OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA)
    else:
        portal_connections = []
        for reg1, reg2 in PORTAL_CONNECTIONS.items():
            portal_connections.append([reg1, reg2, True, None])
        all_logic.append(portal_connections)

    # Create connections
    for logic_array in all_logic:
        for entrance_desc in logic_array:
            region_1 = world.get_region(entrance_desc[0])
            region_2 = world.get_region(entrance_desc[1])
            is_two_way = entrance_desc[2]
            rule = entrance_desc[3]

            region_1.connect(region_2, None, rule)
            if is_two_way:
                region_2.connect(region_1, None, rule)


def apply_self_locking_rules(multiworld: MultiWorld, player: int):
    if multiworld.worlds[player].options.accessibility == Accessibility.option_full:
        return

    # Process self-locking keys first
    key_rules = {
        "Hero's Cave: Final Chest": lambda state, item: any([
            is_small_key(item, player, 0),
            is_item(item, player, f"Master Key ({DUNGEON_NAMES[0]})")
        ]),
        "Gnarled Root Dungeon: Item in Basement": lambda state, item: all([
            is_small_key(item, player, 1),
            oos_has_small_keys(state, player, 1, 1)
        ]),
        "Snake's Remains: Chest on Terrace": lambda state, item: all([
            is_small_key(item, player, 2),
            oos_has_small_keys(state, player, 2, 2)
        ]),
        "Poison Moth's Lair (1F): Chest in Mimics Room": lambda state, item: all([
            is_small_key(item, player, 3),
            oos_can_kill_normal_enemy(state, player)
        ]),
        "Dancing Dragon Dungeon (1F): Crumbling Room Chest": lambda state, item: all([
            is_small_key(item, player, 4),
            oos_has_small_keys(state, player, 4, 2)
        ]),
        "Dancing Dragon Dungeon (1F): Eye Diving Spot Item": lambda state, item: all([
            is_small_key(item, player, 4),
            oos_has_small_keys(state, player, 4, 2),
            oos_can_swim(state, player, False),
        ]),
        "Unicorn's Cave: Magnet Gloves Chest": lambda state, item: is_small_key(item, player, 5),
        "Unicorn's Cave: Treadmills Basement Item": lambda state, item: all([
            is_small_key(item, player, 5),
            oos_has_small_keys(state, player, 5, 3),
            state.has("_dropped_d5_magnet_ball", player),
            oos_has_magnet_gloves(state, player),
            any([
                oos_can_kill_magunesu(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_feather(state, player)
                ])
            ])
        ]),
        "Explorer's Crypt (B1F): Chest in Jumping Stalfos Room": lambda state, item: all([
            is_small_key(item, player, 7),
            oos_has_small_keys(state, player, 7, 4),
            any([
                oos_can_jump_5_wide_pit(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_can_jump_1_wide_pit(state, player, False)
                ])
            ]),
            oos_can_kill_stalfos(state, player),
        ]),
        "Explorer's Crypt (1F): Chest Right of Entrance": lambda state, item: all([
            is_small_key(item, player, 7),
            oos_can_kill_normal_enemy(state, player),
            oos_has_small_keys(state, player, 7, 1),
        ])
    }

    for location_name, key_rule in key_rules.items():
        location = multiworld.get_location(location_name, player)
        location.always_allow = key_rule

    # Process other self-locking items
    OTHER_SELF_LOCKING_ITEMS = {
        "North Horon: Malon Trade": "Cuccodex",
        "Maple Trade": "Lon Lon Egg",
        "Holodrum Plain: Mrs. Ruul Trade": "Ghastly Doll",
        "Subrosia: Subrosian Chef Trade": "Iron Pot",
        "Sunken City: Ingo Trade": "Goron Vase",
        "North Horon: Yelling Old Man Trade": "Fish",
        "Horon Village: Tick Tock Trade": "Wooden Bird",
        "Eastern Suburbs: Guru-Guru Trade": "Engine Grease",
        "Subrosia: Smithy Hard Ore Reforge": "Hard Ore",
        "Subrosia: Smithy Rusty Bell Reforge": "Rusty Bell",
        "Sunken City: Master's Plaque Trade": "Master's Plaque",
        "Subrosia: Market #1": "Star Ore",
    }
    if not multiworld.worlds[player].options.secret_locations:
        OTHER_SELF_LOCKING_ITEMS["Goron Mountain: Biggoron Trade"] = "Lava Soup"

    for loc_name, item_name in OTHER_SELF_LOCKING_ITEMS.items():
        location = multiworld.get_location(loc_name, player)
        location.always_allow = make_self_locking_item_lambda(player, item_name)

    # Great Furnace special case
    location = multiworld.get_location("Subrosia: Item Smelted in Great Furnace", player)
    location.always_allow = lambda state, item: (item.player == player and item.name in ["Red Ore", "Blue Ore"])


def is_small_key(item: Item, player: int, dungeon: int):
    return is_item(item, player, f"Small Key ({DUNGEON_NAMES[dungeon]})")


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name


def make_self_locking_item_lambda(player: int, item_name: str, required_count: int = 0):
    if required_count == 0:
        return lambda state, item: (item.player == player and item.name == item_name)

    return lambda state, item: (item.player == player
                                and item.name == item_name
                                and state.has(item_name, player, required_count))
