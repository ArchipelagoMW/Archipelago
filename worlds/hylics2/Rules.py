from worlds.generic.Rules import add_rule
from BaseClasses import CollectionState


def air_dash(state: CollectionState, player: int) -> bool:
    return state.has("PNEUMATOPHORE", player)


def airship(state: CollectionState, player: int) -> bool:
    return state.has("DOCK KEY", player)


def jail_key(state: CollectionState, player: int) -> bool:
    return state.has("JAIL KEY", player)


def paddle(state: CollectionState, player: int) -> bool:
    return state.has("PADDLE", player)


def worm_room_key(state: CollectionState, player: int) -> bool:
    return state.has("WORM ROOM KEY", player)


def bridge_key(state: CollectionState, player: int) -> bool:
    return state.has("BRIDGE KEY", player)


def upper_chamber_key(state: CollectionState, player: int) -> bool:
    return state.has("UPPER CHAMBER KEY", player)


def vessel_room_key(state: CollectionState, player: int) -> bool:
    return state.has("VESSEL ROOM KEY", player)


def house_key(state: CollectionState, player: int) -> bool:
    return state.has("HOUSE KEY", player)


def cave_key(state: CollectionState, player: int) -> bool:
    return state.has("CAVE KEY", player)


def skull_bomb(state: CollectionState, player: int) -> bool:
    return state.has("SKULL BOMB", player)


def tower_key(state: CollectionState, player: int) -> bool:
    return state.has("TOWER KEY", player)


def deep_key(state: CollectionState, player: int) -> bool:
    return state.has("DEEP KEY", player)


def upper_house_key(state: CollectionState, player: int) -> bool:
    return state.has("UPPER HOUSE KEY", player)


def clicker(state: CollectionState, player: int) -> bool:
    return state.has("CLICKER", player)


def all_tokens(state: CollectionState, player: int) -> bool:
    return state.has("SAGE TOKEN", player, 3)


def charge_up(state: CollectionState, player: int) -> bool:
    return state.has("CHARGE UP", player)


def paper_cup(state: CollectionState, player: int) -> bool:
    return state.has("PAPER CUP", player)


def party_1(state: CollectionState, player: int) -> bool:
    return state.has_any({"Pongorma", "Dedusmuln", "Somsnosa"}, player)


def party_2(state: CollectionState, player: int) -> bool:
    return (
        state.has_all({"Pongorma", "Dedusmuln"}, player)
        or state.has_all({"Pongorma", "Somsnosa"}, player)
        or state.has_all({"Dedusmuln", "Somsnosa"}, player)
    )


def party_3(state: CollectionState, player: int) -> bool:
    return state.has_all({"Pongorma", "Dedusmuln", "Somsnosa"}, player)


def enter_arcade2(state: CollectionState, player: int) -> bool:
    return (
        air_dash(state, player)
        and airship(state, player)
    )


def enter_wormpod(state: CollectionState, player: int) -> bool:
    return (
        airship(state, player)
        and worm_room_key(state, player)
        and paddle(state, player)
    )


def enter_sageship(state: CollectionState, player: int) -> bool:
    return (
        skull_bomb(state, player)
        and airship(state, player)
        and paddle(state, player)
    )


def enter_foglast(state: CollectionState, player: int) -> bool:
    return enter_wormpod(state, player)


def enter_hylemxylem(state: CollectionState, player: int) -> bool:
    return (
        air_dash(state, player)
        and enter_foglast(state, player)
        and bridge_key(state, player)
    )


def set_rules(hylics2world):
    world = hylics2world.multiworld
    player = hylics2world.player

    # Afterlife
    add_rule(world.get_location("Afterlife: TV", player),
        lambda state: cave_key(state, player))

    # New Muldul
    add_rule(world.get_location("New Muldul: Underground Chest", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("New Muldul: TV", player),
        lambda state: house_key(state, player))
    add_rule(world.get_location("New Muldul: Upper House Chest 1", player),
        lambda state: upper_house_key(state, player))
    add_rule(world.get_location("New Muldul: Upper House Chest 2", player),
        lambda state: upper_house_key(state, player))
    add_rule(world.get_location("New Muldul: Pot above Vault", player),
        lambda state: air_dash(state, player))

    # New Muldul Vault
    add_rule(world.get_location("New Muldul: Rescued Blerol 1", player),
        lambda state: (
            (
                (
                    jail_key(state, player)
                    and paddle(state, player)
                )
                and (
                    air_dash(state, player)
                    or airship(state, player)
                )
            )
            or enter_hylemxylem(state, player)
        ))
    add_rule(world.get_location("New Muldul: Rescued Blerol 2", player),
        lambda state: (
            (
                (
                    jail_key(state, player)
                    and paddle(state, player)
                )
                and (
                    air_dash(state, player)
                    or airship(state, player)
                )
            )
            or enter_hylemxylem(state, player)
        ))
    add_rule(world.get_location("New Muldul: Vault Left Chest", player),
        lambda state: enter_hylemxylem(state, player))
    add_rule(world.get_location("New Muldul: Vault Right Chest", player),
        lambda state: enter_hylemxylem(state, player))
    add_rule(world.get_location("New Muldul: Vault Bomb", player),
        lambda state: enter_hylemxylem(state, player))

    # Viewax's Edifice
    add_rule(world.get_location("Viewax's Edifice: Canopic Jar", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Cave Sarcophagus", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Shielded Key", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Shielded Key", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Tower Pot", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Tower Jar", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Tower Chest", player),
        lambda state: (
            paddle(state, player)
            and tower_key(state, player)
        ))
    add_rule(world.get_location("Viewax's Edifice: Viewax Pot", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Viewax's Edifice: TV", player),
        lambda state: (
            paddle(state, player)
            and jail_key(state, player)
        ))
    add_rule(world.get_location("Viewax's Edifice: Sage Fridge", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Viewax's Edifice: Sage Item 1", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Viewax's Edifice: Sage Item 2", player),
        lambda state: air_dash(state, player))

    # Arcade 1
    add_rule(world.get_location("Arcade 1: Key", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Coin Dash", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Burrito Alcove 1", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Burrito Alcove 2", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Behind Spikes Banana", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Pyramid Banana", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Moving Platforms Muscle Applique", player),
        lambda state: paddle(state, player))
    add_rule(world.get_location("Arcade 1: Bed Banana", player),
        lambda state: paddle(state, player))

    # Airship
    add_rule(world.get_location("Airship: Talk to Somsnosa", player),
        lambda state: worm_room_key(state, player))

    # Foglast
    add_rule(world.get_location("Foglast: Underground Sarcophagus", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Foglast: Shielded Key", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Foglast: TV", player),
        lambda state: (
            air_dash(state, player)
            and clicker(state, player)
        ))
    add_rule(world.get_location("Foglast: Buy Clicker", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Foglast: Shielded Chest", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Foglast: Cave Fridge", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Foglast: Roof Sarcophagus", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 1", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 2", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Under Lair Sarcophagus 3", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Sage Sarcophagus", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Sage Item 1", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))
    add_rule(world.get_location("Foglast: Sage Item 2", player),
        lambda state: (
            air_dash(state, player)
            and bridge_key(state, player)
        ))

    # Drill Castle
    add_rule(world.get_location("Drill Castle: Island Banana", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Drill Castle: Island Pot", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Drill Castle: Cave Sarcophagus", player),
        lambda state: air_dash(state, player))
    add_rule(world.get_location("Drill Castle: TV", player),
        lambda state: air_dash(state, player))

    # Sage Labyrinth
    add_rule(world.get_location("Sage Labyrinth: Sage Item 1", player),
        lambda state: deep_key(state, player))
    add_rule(world.get_location("Sage Labyrinth: Sage Item 2", player),
        lambda state: deep_key(state, player))
    add_rule(world.get_location("Sage Labyrinth: Sage Left Arm", player),
        lambda state: deep_key(state, player))
    add_rule(world.get_location("Sage Labyrinth: Sage Right Arm", player),
        lambda state: deep_key(state, player))
    add_rule(world.get_location("Sage Labyrinth: Sage Left Leg", player),
        lambda state: deep_key(state, player))
    add_rule(world.get_location("Sage Labyrinth: Sage Right Leg", player),
        lambda state: deep_key(state, player))

    # Sage Airship
    add_rule(world.get_location("Sage Airship: TV", player),
        lambda state: all_tokens(state, player))

    # Hylemxylem
    add_rule(world.get_location("Hylemxylem: Upper Chamber Banana", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Across Upper Reservoir Chest", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Chest", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 1", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 2", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 1", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 2", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 3", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Sarcophagus", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 1", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 2", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 3", player),
        lambda state: upper_chamber_key(state, player))
    add_rule(world.get_location("Hylemxylem: Upper Reservoir Hole Key", player),
        lambda state: upper_chamber_key(state, player))

    # extra rules if Extra Items in Logic is enabled
    if world.extra_items_in_logic[player]:
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: charge_up(state, player))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: (
                    charge_up(state, player)
                    and paper_cup(state, player)
                    and worm_room_key(state, player)
                ))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: (
                charge_up(state, player)
                and paper_cup(state, player)
            ))

        add_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player),
            lambda state: (
                charge_up(state, player)
                and paper_cup(state, player)
            ))

    # extra rules if Shuffle Party Members is enabled
    if world.party_shuffle[player]:
        for i in world.get_region("Arcade Island", player).entrances:
            add_rule(i, lambda state: party_3(state, player))
        for i in world.get_region("Foglast", player).entrances:
            add_rule(i, lambda state: (
                party_3(state, player)
                or (
                    party_2(state, player)
                    and jail_key(state, player)
                )
            ))
        for i in world.get_region("Sage Airship", player).entrances:
            add_rule(i, lambda state: party_3(state, player))
        for i in world.get_region("Hylemxylem", player).entrances:
            add_rule(i, lambda state: party_3(state, player))

        add_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player),
            lambda state: party_2(state, player))
        add_rule(world.get_location("New Muldul: Rescued Blerol 1", player),
            lambda state: party_2(state, player))
        add_rule(world.get_location("New Muldul: Rescued Blerol 2", player),
            lambda state: party_2(state, player))
        add_rule(world.get_location("New Muldul: Vault Left Chest", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Right Chest", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Bomb", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("Juice Ranch: Battle with Somsnosa", player),
            lambda state: party_2(state, player))
        add_rule(world.get_location("Juice Ranch: Somsnosa Joins", player),
            lambda state: party_2(state, player))
        add_rule(world.get_location("Airship: Talk to Somsnosa", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player),
            lambda state: party_3(state, player))

    # extra rules if Shuffle Red Medallions is enabled
    if world.medallion_shuffle[player]:
        add_rule(world.get_location("New Muldul: Upper House Medallion", player),
            lambda state: upper_house_key(state, player))
        add_rule(world.get_location("New Muldul: Vault Rear Left Medallion", player),
            lambda state: (
                enter_foglast(state, player)
                and bridge_key(state, player)
            ))
        add_rule(world.get_location("New Muldul: Vault Rear Right Medallion", player),
            lambda state: (
                enter_foglast(state, player)
                and bridge_key(state, player)
            ))
        add_rule(world.get_location("New Muldul: Vault Center Medallion", player),
            lambda state: (
                enter_foglast(state, player)
                and bridge_key(state, player)
            ))
        add_rule(world.get_location("New Muldul: Vault Front Left Medallion", player),
            lambda state: (
                enter_foglast(state, player)
                and bridge_key(state, player)
            ))
        add_rule(world.get_location("New Muldul: Vault Front Right Medallion", player),
            lambda state: (
                enter_foglast(state, player)
                and bridge_key(state, player)
            ))
        add_rule(world.get_location("Viewax's Edifice: Fort Wall Medallion", player),
            lambda state: paddle(state, player))
        add_rule(world.get_location("Viewax's Edifice: Jar Medallion", player),
            lambda state: paddle(state, player))
        add_rule(world.get_location("Viewax's Edifice: Sage Chair Medallion", player),
            lambda state: air_dash(state, player))
        add_rule(world.get_location("Arcade 1: Lonely Medallion", player),
            lambda state: paddle(state, player))
        add_rule(world.get_location("Arcade 1: Alcove Medallion", player),
            lambda state: paddle(state, player))
        add_rule(world.get_location("Foglast: Under Lair Medallion", player),
            lambda state: bridge_key(state, player))
        add_rule(world.get_location("Foglast: Mid-Air Medallion", player),
            lambda state: air_dash(state, player))
        add_rule(world.get_location("Foglast: Top of Tower Medallion", player),
            lambda state: paddle(state, player))
        add_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Medallion", player),
            lambda state: upper_chamber_key(state, player))

    # extra rules if Shuffle Red Medallions and Party Shuffle are enabled
    if world.party_shuffle[player] and world.medallion_shuffle[player]:
        add_rule(world.get_location("New Muldul: Vault Rear Left Medallion", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Rear Right Medallion", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Center Medallion", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Front Left Medallion", player),
            lambda state: party_3(state, player))
        add_rule(world.get_location("New Muldul: Vault Front Right Medallion", player),
            lambda state: party_3(state, player))

    # entrances
    for i in world.get_region("Airship", player).entrances:
        add_rule(i, lambda state: airship(state, player))
    for i in world.get_region("Arcade Island", player).entrances:
        add_rule(i, lambda state: (
            airship(state, player)
            and air_dash(state, player)
        ))
    for i in world.get_region("Worm Pod", player).entrances:
        add_rule(i, lambda state: enter_wormpod(state, player))
    for i in world.get_region("Foglast", player).entrances:
        add_rule(i, lambda state: enter_foglast(state, player))
    for i in world.get_region("Sage Labyrinth", player).entrances:
        add_rule(i, lambda state: skull_bomb(state, player))
    for i in world.get_region("Sage Airship", player).entrances:
        add_rule(i, lambda state: enter_sageship(state, player))
    for i in world.get_region("Hylemxylem", player).entrances:
        add_rule(i, lambda state: enter_hylemxylem(state, player))

    # random start logic (default)
    if ((not world.random_start[player]) or \
        (world.random_start[player] and hylics2world.start_location == "Waynehouse")):
        # entrances
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: (
                air_dash(state, player)
                and airship(state, player)
            ))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: airship(state, player))

    # random start logic (Viewax's Edifice)
    elif (world.random_start[player] and hylics2world.start_location == "Viewax's Edifice"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: (
                air_dash(state, player)
                or airship(state, player)
            ))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: (
                air_dash(state, player)
                or airship(state, player)
            ))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: (
                air_dash(state, player)
                or airship(state, player)
            ))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: (
                air_dash(state, player)
                or airship(state, player)
            ))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: airship(state, player))

    # random start logic (TV Island)
    elif (world.random_start[player] and hylics2world.start_location == "TV Island"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Shield Facility", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Juice Ranch", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: airship(state, player))

    # random start logic (Shield Facility)
    elif (world.random_start[player] and hylics2world.start_location == "Shield Facility"):
        for i in world.get_region("Waynehouse", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("New Muldul", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("New Muldul Vault", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Drill Castle", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Viewax", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("TV Island", player).entrances:
            add_rule(i, lambda state: airship(state, player))
        for i in world.get_region("Sage Labyrinth", player).entrances:
            add_rule(i, lambda state: airship(state, player))