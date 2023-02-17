from BaseClasses import MultiWorld

from .Items import exclusionItem_table
from .Locations import popupChecks, STT_Checks, CoR_Checks, Form_Checks, AG2_Checks, exclusion_table,weaponslots
from .Names import LocationName, ItemName,RegionName
from ..generic.Rules import add_rule, forbid_items, forbid_item


def set_rules(world: MultiWorld, player: int):

    add_rule(world.get_location(LocationName.RoxasDataMagicBoost, player),
             lambda state: state.kh_dataroxas(player))
    add_rule(world.get_location(LocationName.DemyxDataAPBoost, player),
            lambda state: state.kh_datademyx(player))
    add_rule(world.get_location(LocationName.SaixDataDefenseBoost, player),
             lambda state: state.kh_datasaix(player))
    add_rule(world.get_location(LocationName.XaldinDataDefenseBoost, player),
             lambda state: state.kh_dataxaldin(player))
    add_rule(world.get_location(LocationName.XemnasDataPowerBoost, player),
             lambda state: state.kh_dataxemnas(player))
    add_rule(world.get_location(LocationName.XigbarDataDefenseBoost, player),
             lambda state: state.kh_dataxigbar(player))
    add_rule(world.get_location(LocationName.VexenDataLostIllusion, player),
             lambda state: state.kh_dataaxel(player))
    add_rule(world.get_location(LocationName.LuxordDataAPBoost, player),
             lambda state: state.kh_dataluxord(player))


    for slot,weapon in weaponslots.items():
        add_rule(world.get_location(slot,player),lambda state: state.has(weapon,player))

    if world.Goal[player].value == 0:
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_three_proof_unlocked(player))
        if world.FinalXemnas[player].value == 1:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_three_proof_unlocked(player)
    # lucky emblem hunt
    elif world.Goal[player].value == 1:
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value))
        if world.FinalXemnas[player].value == 1:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value)
    # hitlist
    elif world.Goal[player].value == 2:
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_hitlist(player, world.BountyRequired[player].value))
        if world.FinalXemnas[player].value == 1:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_hitlist(player,world.BountyRequired[player].value)

    # Forbid Ablilites on popups due to game limitations
    for location in popupChecks:
        forbid_items(world.get_location(location, player), exclusionItem_table["Ability"])
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    for location in STT_Checks:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    # Santa's house also breaks with stat ups
    for location in {LocationName.SantasHouseChristmasTownMap,LocationName.SantasHouseAPBoost}:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    add_rule(world.get_location(LocationName.TransporttoRemembrance, player),
             lambda state:state.kh_transport(player))





