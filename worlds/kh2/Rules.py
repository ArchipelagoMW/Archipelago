from BaseClasses import MultiWorld

from .Items import exclusionItem_table
from .Locations import popupChecks, STT_Checks, CoR_Checks, Form_Checks, AG2_Checks, exclusion_table,weaponslots
from .Names import LocationName, ItemName,RegionName
from ..generic.Rules import add_rule, forbid_items, forbid_item


def set_rules(world: MultiWorld, player: int,firstvisitlocking,secondvisitlocking):

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
    forbid_items(world.get_location(LocationName.SantasHouseChristmasTownMap, player), exclusionItem_table["StatUps"])
    forbid_items(world.get_location(LocationName.SantasHouseAPBoost, player), exclusionItem_table["StatUps"])


    add_rule(world.get_location(LocationName.TransporttoRemembrance, player),
             lambda state:state.kh_transport(player))

    for formlvl2 in {LocationName.Valorlvl2, LocationName.Wisdomlvl2, LocationName.Limitlvl2, LocationName.Masterlvl2,
                     LocationName.Finallvl2}:
        add_rule(world.get_location(formlvl2, player), lambda state: state.kh_form_level_unlocked(player, 1))

    for formlvl3 in {LocationName.Valorlvl3, LocationName.Wisdomlvl3, LocationName.Limitlvl3, LocationName.Masterlvl3,
                     LocationName.Finallvl3}:
        add_rule(world.get_location(formlvl3, player), lambda state: state.kh_form_level_unlocked(player, 1))

    for formlvl4 in {LocationName.Valorlvl4, LocationName.Wisdomlvl4, LocationName.Limitlvl4, LocationName.Masterlvl4,
                     LocationName.Finallvl4}:
        add_rule(world.get_location(formlvl4, player), lambda state: state.kh_form_level_unlocked(player, 2))

    for formlvl5 in {LocationName.Valorlvl5, LocationName.Wisdomlvl5, LocationName.Limitlvl5, LocationName.Masterlvl5,
                     LocationName.Finallvl5}:
        add_rule(world.get_location(formlvl5, player), lambda state: state.kh_form_level_unlocked(player, 3))

    for formlvl6 in {LocationName.Valorlvl6, LocationName.Wisdomlvl6, LocationName.Limitlvl6, LocationName.Masterlvl6,
                     LocationName.Finallvl6}:
        add_rule(world.get_location(formlvl6, player), lambda state: state.kh_form_level_unlocked(player, 4))

    for formlvl7 in {LocationName.Valorlvl7, LocationName.Wisdomlvl7, LocationName.Limitlvl7, LocationName.Masterlvl7,
                     LocationName.Finallvl7}:
        add_rule(world.get_location(formlvl7, player), lambda state: state.kh_form_level_unlocked(player, 5))

    # Option to be more in line of the current KH2 Randomizer
    if world.Max_Logic[player].value == 0:
        for location in CoR_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["Forms"])
            forbid_item(world.get_location(location, player), "Torn Page", player)
        for location in AG2_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["Forms"])
            forbid_item(world.get_location(location, player), "Torn Page", player)
        # forbid forms on forms
        for location in Form_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["Forms"])
            forbid_item(world.get_location(location, player), "Torn Page", player)

    # Creating Access rules for terra and mushroom 13 checks
    add_rule(world.get_location(LocationName.LingeringWillBonus, player),
             lambda state: state.has(ItemName.ProofofConnection, player))
    add_rule(world.get_location(LocationName.LingeringWillProofofConnection, player),
             lambda state: state.has(ItemName.ProofofConnection, player))
    add_rule(world.get_location(LocationName.LingeringWillManifestIllusion, player),
             lambda state: state.has(ItemName.ProofofConnection, player))
    add_rule(world.get_location(LocationName.WinnersProof, player),
             lambda state: state.has(ItemName.ProofofPeace, player))
    add_rule(world.get_location(LocationName.ProofofPeace, player),
             lambda state: state.has(ItemName.ProofofPeace, player))

    # level 50
    if world.LevelDepth[player].value == 0:
        for level in {LocationName.Lvl20, LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28,
                      LocationName.Lvl30}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 6*secondvisitlocking))
        for level in {LocationName.Lvl32, LocationName.Lvl34, LocationName.Lvl36, LocationName.Lvl39,
                      LocationName.Lvl41}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 7*secondvisitlocking))
        for level in {LocationName.Lvl44, LocationName.Lvl46, LocationName.Lvl48, LocationName.Lvl50}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 8*secondvisitlocking))
    # level 99
    elif world.LevelDepth[player].value == 1:
        for level in {LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28, LocationName.Lvl31}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 6*secondvisitlocking))
        for level in {LocationName.Lvl33, LocationName.Lvl36, LocationName.Lvl39, LocationName.Lvl41, }:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 7*secondvisitlocking))
        for level in {LocationName.Lvl44, LocationName.Lvl47, LocationName.Lvl49, LocationName.Lvl53}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 8*secondvisitlocking))
        for level in {LocationName.Lvl59, LocationName.Lvl65, LocationName.Lvl73, LocationName.Lvl85,
                      LocationName.Lvl99}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 9*secondvisitlocking))



    # level 50 sanity
    elif world.LevelDepth[player].value == 2 or world.LevelDepth[player].value == 3:
        for level in {LocationName.Lvl25, LocationName.Lvl26, LocationName.Lvl27, LocationName.Lvl28,
                      LocationName.Lvl29, LocationName.Lvl30,
                      LocationName.Lvl31, LocationName.Lvl32, LocationName.Lvl33, LocationName.Lvl34,
                      LocationName.Lvl35}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 3*secondvisitlocking))
        for level in {LocationName.Lvl36, LocationName.Lvl37, LocationName.Lvl38, LocationName.Lvl39,
                      LocationName.Lvl40,
                      LocationName.Lvl41, LocationName.Lvl42, LocationName.Lvl43, LocationName.Lvl44,
                      LocationName.Lvl45, LocationName.Lvl46}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 4*secondvisitlocking))
        for level in {LocationName.Lvl47, LocationName.Lvl48, LocationName.Lvl49, LocationName.Lvl50}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 5*secondvisitlocking))
        # level 99 sanity
        if world.LevelDepth[player].value == 2:
            for level in {LocationName.Lvl51, LocationName.Lvl52, LocationName.Lvl53, LocationName.Lvl54,
                          LocationName.Lvl55,
                          LocationName.Lvl56, LocationName.Lvl57}:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 6*secondvisitlocking))
            for level in {LocationName.Lvl58, LocationName.Lvl59, LocationName.Lvl60, LocationName.Lvl61,
                          LocationName.Lvl62, LocationName.Lvl63,
                          LocationName.Lvl64, LocationName.Lvl65, LocationName.Lvl66, LocationName.Lvl67,
                          LocationName.Lvl68}:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 7*secondvisitlocking))
            for level in {LocationName.Lvl69, LocationName.Lvl70, LocationName.Lvl71, LocationName.Lvl72,
                          LocationName.Lvl73, LocationName.Lvl74,
                          LocationName.Lvl75, LocationName.Lvl76, LocationName.Lvl77, LocationName.Lvl78,
                          LocationName.Lvl79, }:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 8*secondvisitlocking))
            for level in {LocationName.Lvl80, LocationName.Lvl81, LocationName.Lvl82, LocationName.Lvl83,
                          LocationName.Lvl84, LocationName.Lvl85,
                          LocationName.Lvl86, LocationName.Lvl87, LocationName.Lvl88, LocationName.Lvl89,
                          LocationName.Lvl90, LocationName.Lvl91,
                          LocationName.Lvl92, LocationName.Lvl93, LocationName.Lvl94, LocationName.Lvl95,
                          LocationName.Lvl96, LocationName.Lvl97,
                          LocationName.Lvl98, LocationName.Lvl99}:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 9*secondvisitlocking))





