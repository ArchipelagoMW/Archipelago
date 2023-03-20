
from BaseClasses import MultiWorld

from .Items import exclusionItem_table
from .Locations import STT_Checks, exclusion_table
from .Names import LocationName, ItemName
from ..generic.Rules import add_rule, forbid_items, set_rule


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

    for slot, weapon in exclusion_table["WeaponSlots"].items():
        add_rule(world.get_location(slot, player), lambda state: state.has(weapon, player))
    formLogicTable = {
        ItemName.ValorForm:     [LocationName.Valorlvl4,
                                 LocationName.Valorlvl5,
                                 LocationName.Valorlvl6,
                                 LocationName.Valorlvl7],
        ItemName.WisdomForm:    [LocationName.Wisdomlvl4,
                                 LocationName.Wisdomlvl5,
                                 LocationName.Wisdomlvl6,
                                 LocationName.Wisdomlvl7],
        ItemName.LimitForm:     [LocationName.Limitlvl4,
                                 LocationName.Limitlvl5,
                                 LocationName.Limitlvl6,
                                 LocationName.Limitlvl7],
        ItemName.MasterForm:    [LocationName.Masterlvl4,
                                 LocationName.Masterlvl5,
                                 LocationName.Masterlvl6,
                                 LocationName.Masterlvl7],
        ItemName.FinalForm:     [LocationName.Finallvl4,
                                 LocationName.Finallvl5,
                                 LocationName.Finallvl6,
                                 LocationName.Finallvl7]
    }

    for form in formLogicTable:
        for i in range(4):
            location = world.get_location(formLogicTable[form][i], player)
            set_rule(location, lambda state, i=i + 1, form=form: state.kh_amount_of_forms(player, i, form))

    if world.Goal[player] == "three_proofs":
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_three_proof_unlocked(player))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_three_proof_unlocked(player)
    # lucky emblem hunt
    elif world.Goal[player] == "lucky_emblem_hunt":
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value)
    # hitlist if == 2
    else:
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_hitlist(player, world.BountyRequired[player].value))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_hitlist(player, world.BountyRequired[player].value)

    #  Forbid Abilities on popups due to game limitations
    for location in exclusion_table["Popups"]:
        forbid_items(world.get_location(location, player), exclusionItem_table["Ability"])
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    for location in STT_Checks:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    # Santa's house also breaks with stat ups
    for location in {LocationName.SantasHouseChristmasTownMap, LocationName.SantasHouseAPBoost}:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    add_rule(world.get_location(LocationName.TransporttoRemembrance, player),
             lambda state: state.kh_transport(player))
