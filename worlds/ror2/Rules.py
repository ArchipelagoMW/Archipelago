from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, add_rule
from .Locations import orderedstage_location
from .RoR2Environments import environment_vanilla_orderedstages_table, environment_sotv_orderedstages_table, \
    environment_orderedstages_table
from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from . import RiskOfRainWorld


# Rule to see if it has access to the previous stage
def has_entrance_access_rule(world, stage: str, entrance: str, player: int):
    world.get_entrance(entrance, player).access_rule = \
        lambda state: state.has(entrance, player) and state.has(stage, player)


def has_all_items(world, items: Set, entrance: str, player: int):
    world.get_entrance(entrance, player).access_rule = \
        lambda state: state.has_all(items, player) and state.has(entrance, player)


# Checks to see if chest/shrine are accessible
def has_location_access_rule(world, environment: str, player: int, item_number: int, item_type: str):
    if item_number == 1:
        world.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
            lambda state: state.has(environment, player)
        if item_type == "Scavenger":
            world.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
                lambda state: state.has(environment, player) and state.has("Stage 5", player)
    else:
        world.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
            lambda state: check_location(state, environment, player, item_number, item_type)


def check_location(state, environment: str, player: int, item_number: int, item_name: str):
    return state.can_reach(f"{environment}: {item_name} {item_number - 1}", "Location", player)


# unlock event to next set of stages
def get_stage_event(world, player: int, stage_number: int):
    if stage_number == 4:
        return
    world.get_entrance(f"OrderedStage_{stage_number + 1}", player).access_rule = \
        lambda state: state.has(f"Stage {stage_number + 1}", player)


def set_rules(ror2_world: "RiskOfRainWorld") -> None:
    player = ror2_world.player
    world = ror2_world.multiworld
    if world.goal[player] == "classic":
        # classic mode
        total_locations = world.total_locations[player].value  # total locations for current player
    else:
        # explore mode
        total_locations = len(
            orderedstage_location.get_locations(
                chests=world.chests_per_stage[player].value,
                shrines=world.shrines_per_stage[player].value,
                scavengers=world.scavengers_per_stage[player].value,
                scanners=world.scanner_per_stage[player].value,
                altars=world.altars_per_stage[player].value,
                dlc_sotv=world.dlc_sotv[player].value
            )
        )

    event_location_step = 25  # set an event location at these locations for "spheres"
    divisions = total_locations // event_location_step
    total_revivals = world.worlds[player].total_revivals  # pulling this info we calculated in generate_basic

    if world.goal[player] == "classic":
        # classic mode
        if divisions:
            for i in range(1, divisions + 1):  # since divisions is the floor of total_locations / 25
                if i * event_location_step != total_locations:
                    event_loc = world.get_location(f"Pickup{i * event_location_step}", player)
                    set_rule(event_loc,
                            lambda state, i=i: state.can_reach(f"ItemPickup{i * event_location_step - 1}",
                                                               "Location", player))
                    # we want to create a rule for each of the 25 locations per division
                for n in range(i * event_location_step, (i + 1) * event_location_step + 1):
                    if n > total_locations:
                        break
                    if n == i * event_location_step:
                        set_rule(world.get_location(f"ItemPickup{n}", player),
                                 lambda state, event_item=event_loc.item.name: state.has(event_item, player))
                    else:
                        set_rule(world.get_location(f"ItemPickup{n}", player),
                                 lambda state, n=n: state.can_reach(f"ItemPickup{n - 1}", "Location", player))
        set_rule(world.get_location("Victory", player),
                 lambda state: state.can_reach(f"ItemPickup{total_locations}", "Location", player))
        if total_revivals or world.start_with_revive[player].value:
            add_rule(world.get_location("Victory", player),
                     lambda state: state.has("Dio's Best Friend", player,
                                             total_revivals + world.start_with_revive[player]))

    elif world.goal[player] == "explore":
        # When explore_mode is used,
        #   scavengers need to be locked till after a full loop since that is when they are capable of spawning.
        # (While technically the requirement is just beating 5 stages, this will ensure that the player will have
        #   a long enough run to have enough director credits for scavengers and
        #   help prevent being stuck in the same stages until that point.)

        # Regions
        chests = world.chests_per_stage[player]
        shrines = world.shrines_per_stage[player]
        newts = world.altars_per_stage[player]
        scavengers = world.scavengers_per_stage[player]
        scanners = world.scanner_per_stage[player]
        for i in range(len(environment_vanilla_orderedstages_table)):
            for environment_name, _ in environment_vanilla_orderedstages_table[i].items():
                # Make sure to go through each location
                if scavengers == 1:
                    has_location_access_rule(world, environment_name, player, scavengers, "Scavenger")
                if scanners == 1:
                    has_location_access_rule(world, environment_name, player, scanners, "Radio Scanner")
                for chest in range(1, chests + 1):
                    has_location_access_rule(world, environment_name, player, chest, "Chest")
                for shrine in range(1, shrines + 1):
                    has_location_access_rule(world, environment_name, player, shrine, "Shrine")
                if newts > 0:
                    for newt in range(1, newts + 1):
                        has_location_access_rule(world, environment_name, player, newt, "Newt Altar")
                if i > 0:
                    has_entrance_access_rule(world, f"Stage {i}", environment_name, player)
            get_stage_event(world, player, i)

        if world.dlc_sotv[player]:
            for i in range(len(environment_sotv_orderedstages_table)):
                for environment_name, _ in environment_sotv_orderedstages_table[i].items():
                    # Make sure to go through each location
                    if scavengers == 1:
                        has_location_access_rule(world, environment_name, player, scavengers, "Scavenger")
                    if scanners == 1:
                        has_location_access_rule(world, environment_name, player, scanners, "Radio Scanner")
                    for chest in range(1, chests + 1):
                        has_location_access_rule(world, environment_name, player, chest, "Chest")
                    for shrine in range(1, shrines + 1):
                        has_location_access_rule(world, environment_name, player, shrine, "Shrine")
                    if newts > 0:
                        for newt in range(1, newts + 1):
                            has_location_access_rule(world, environment_name, player, newt, "Newt Altar")
                    if i > 0:
                        has_entrance_access_rule(world, f"Stage {i}", environment_name, player)
        has_entrance_access_rule(world, "Hidden Realm: A Moment, Fractured", "Hidden Realm: A Moment, Whole",
                                 player)
        has_entrance_access_rule(world, "Stage 1", "Hidden Realm: Bazaar Between Time", player)
        has_entrance_access_rule(world, "Hidden Realm: Bazaar Between Time", "Void Fields", player)
        has_entrance_access_rule(world, "Stage 5", "Commencement", player)
        has_entrance_access_rule(world, "Stage 5", "Hidden Realm: A Moment, Fractured", player)
        has_entrance_access_rule(world, "Beads of Fealty", "Hidden Realm: A Moment, Whole", player)
        if world.dlc_sotv[player]:
            if world.victory[player] == "voidling":
                has_all_items(world, {"Stage 5", "The Planetarium"}, "Commencement", player)
            has_entrance_access_rule(world, "Stage 5", "The Planetarium", player)
            has_entrance_access_rule(world, "Stage 5", "Void Locus", player)
            # has_all_items(world, {"Stage 5", "The Planetarium"}, "Void Locus", player)
    # Win Condition
    world.completion_condition[player] = lambda state: state.has("Victory", player)
