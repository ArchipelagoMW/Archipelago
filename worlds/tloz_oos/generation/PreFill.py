from BaseClasses import MultiWorld
from Fill import fill_restrictive
from ..World import OracleOfSeasonsWorld
from ..data import LOCATIONS_DATA
from ..data.Constants import DUNGEON_NAMES


def stage_pre_fill_dungeon_items(multiworld: MultiWorld):
    # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
    # of those which makes them pretty crowded.
    # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
    # To circumvent this, we perform a restricted pre-fills here, placing only those dungeon items
    # before anything else.
    oos_players = multiworld.get_game_players(OracleOfSeasonsWorld.game)

    base_all_state = multiworld.get_all_state(False, collect_pre_fill_items=False, perform_sweep=False)
    # Collect all pre_fill_items except our OoS's and then sweep. This gives more accurate results in cases of item
    # plando being used to remove items from the item pool and placing them into locations locked behind pre_fill
    # items.
    for player in multiworld.player_ids:
        if player in oos_players:
            continue
        subworld = multiworld.worlds[player]
        for item in subworld.get_pre_fill_items():
            subworld.collect(base_all_state, item)
    base_all_state.sweep_for_advancements()

    for filling_player in oos_players:
        # Create a player-specific state for just the player that is filling dungeons.
        per_player_base_all_state = base_all_state.copy()
        # Collect the pre_fill_items() of all other OoS players into the state.
        for other_player in oos_players:
            if other_player == filling_player:
                continue
            subworld = multiworld.worlds[other_player]
            for item in subworld.get_pre_fill_items():
                subworld.collect(per_player_base_all_state, item)
        # And then sweep the state to pick up pre-placed items.
        per_player_base_all_state.sweep_for_advancements()

        # Get the world for the player that is filling.
        filling_world = multiworld.worlds[filling_player]

        # Fill each of this world's dungeons.
        for i in range(0, 10):
            if i == 9:
                i = 11
            # Build a list of locations in this dungeon
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == i]
            dungeon_locations = [loc for loc in multiworld.get_locations(filling_player)
                                 if loc.name in dungeon_location_names and not loc.locked]

            # From the list of all dungeon items that needs to be placed restrictively, only filter the ones for the
            # dungeon we are currently processing.
            confined_dungeon_items = [item for item in filling_world.pre_fill_items
                                      if item.name.endswith(f"({DUNGEON_NAMES[i]})")]
            if len(confined_dungeon_items) == 0:
                continue  # This list might be empty with some keysanity options

            # Remove from the pre_fill_items the items we're about to place
            for item in confined_dungeon_items:
                filling_world.pre_fill_items.remove(item)
            collection_state = per_player_base_all_state.copy()
            # Collect the remaining pre_fill_items into the state.
            for item in filling_world.get_pre_fill_items():
                collection_state.collect(item, True)
            # Sweep the copied state across the entire multiworld to again account for unusual item plando. It is
            # also beneficial to pass as maximal a state as possible to fill_restrictive to reduce how much sweeping
            # fill_restrictive must do.
            collection_state.sweep_for_advancements()
            # Perform a prefill to place confined items inside locations of this dungeon
            filling_world.random.shuffle(dungeon_locations)
            fill_restrictive(multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)
            for item in confined_dungeon_items:
                assert item.location is not None
