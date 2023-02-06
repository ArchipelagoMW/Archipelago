from BaseClasses import MultiWorld

from .Items import exclusionItem_table
from .Locations import popupChecks, STT_Checks, CoR_Checks, Form_Checks, AG2_Checks
from .Names import LocationName, ItemName
from ..generic.Rules import add_rule, forbid_items, forbid_item


def set_rules(world: MultiWorld, player: int):
    #three proofs
    if world.Goal[player].value == 0:
        if world.FinalXemnas[player].value==1:
            add_rule(world.get_location(LocationName.FinalXemnas, player),
                     lambda state: state.kh_three_proof_unlocked(player))
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_three_proof_unlocked(player)
    #lucky emblem hunt
    elif world.Goal[player].value == 1:
        if world.FinalXemnas[player].value == 1:
            add_rule(world.get_location(LocationName.FinalXemnas, player),
                     lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value))
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value)
    #hitlist
    elif world.Goal[player].value==2:
        if world.FinalXemnas[player].value == 1:
            add_rule(world.get_location(LocationName.FinalXemnas, player),
                     lambda state: state.kh_hitlist(player, world.UltimaWeaponRequired[player].value))
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_hitlist(player, world.UltimaWeaponRequired[player].value)
    # Forbid Ablilites on popups due to game limitations
    for location in popupChecks:
        forbid_items(world.get_location(location, player), exclusionItem_table["Ability"])
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    for location in STT_Checks:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    # Santa's house also breaks with stat ups
    forbid_items(world.get_location(LocationName.SantasHouseChristmasTownMap, player), exclusionItem_table["StatUps"])
    forbid_items(world.get_location(LocationName.SantasHouseAPBoost, player), exclusionItem_table["StatUps"])

    # Final checks of cor requires more locks than other checks in cor
    add_rule(world.get_location(LocationName.CoRMineshaftUpperLevelAPBoost, player),
             lambda state:
             state.has(ItemName.HighJump, player, 3)
             and state.has(ItemName.AerialDodge, player, 3)
             and state.has(ItemName.Glide, player, 3))
    add_rule(world.get_location(LocationName.TransporttoRemembrance, player),
             lambda state:
             state.has(ItemName.HighJump, player, 3)
             and state.has(ItemName.AerialDodge, player, 3)
             and state.has(ItemName.Glide, player, 3))

    for location in {LocationName.FatalCrestGoddessofFateCup, LocationName.OrichalcumPlusGoddessofFateCup,
                     LocationName.HadesCupTrophyParadoxCups}:
        add_rule(world.get_location(location, player),
                 lambda state:
                 state.kh_ag_unlocked(player)
                 and state.kh_ht_unlocked(player)
                 and state.kh_pl_unlocked(player)
                 and state.kh_oc_unlocked(player)
                 and state.kh_dc_unlocked(player)
                 and state.kh_twtnw_unlocked(player))

    for location in {LocationName.ProtectBeltPainandPanicCup, LocationName.SerenityGemPainandPanicCup}:
        add_rule(world.get_location(location, player),
                 lambda state: state.kh_dc_unlocked(player))

    for location in {LocationName.RisingDragonCerberusCup, LocationName.SerenityCrystalCerberusCup}:
        add_rule(world.get_location(location, player),
                 lambda state:
                 state.kh_ag_unlocked(player)
                 and state.kh_ht_unlocked(player)
                 and state.kh_pl_unlocked(player))

    for location in {LocationName.GenjiShieldTitanCup, LocationName.SkillfulRingTitanCup}:
        add_rule(world.get_location(location, player),
                 lambda state:
                 state.kh_oc_unlocked(player))
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
            forbid_item(world.get_location(location, player), player, "Torn Page")
        for location in AG2_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["Forms"])
            forbid_item(world.get_location(location, player), player, "Torn Page")
        # forbid forms on forms
        for location in Form_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["Forms"])
            forbid_item(world.get_location(location, player), player, "Torn Page")

    # Creating Accsess rules for terra and mushroom 13 checks
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

    # add npc that warps player to tower after tt1 because those chests are missable

    # level 50
    if world.Level_Depth[player].value == 0:
        for level in {LocationName.Lvl20, LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28,
                      LocationName.Lvl30}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 3))
        for level in {LocationName.Lvl32, LocationName.Lvl34, LocationName.Lvl36, LocationName.Lvl39,
                      LocationName.Lvl41}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 4))
        for level in {LocationName.Lvl44, LocationName.Lvl46, LocationName.Lvl48, LocationName.Lvl50}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 6))
    # level 99
    elif world.Level_Depth[player].value == 1:
        for level in {LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28, LocationName.Lvl31}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 2))
        for level in {LocationName.Lvl33, LocationName.Lvl36, LocationName.Lvl39, LocationName.Lvl41, }:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 4))
        for level in {LocationName.Lvl44, LocationName.Lvl47, LocationName.Lvl49, LocationName.Lvl53}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 5))
        for level in {LocationName.Lvl59, LocationName.Lvl65, LocationName.Lvl73, LocationName.Lvl85,
                      LocationName.Lvl99}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 7))



    # level 50 sanity
    elif world.Level_Depth[player].value == 2 or world.Level_Depth[player].value == 3:
        for level in {LocationName.Lvl25, LocationName.Lvl26, LocationName.Lvl27, LocationName.Lvl28,
                      LocationName.Lvl29, LocationName.Lvl30,
                      LocationName.Lvl31, LocationName.Lvl32, LocationName.Lvl33, LocationName.Lvl34,
                      LocationName.Lvl35}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 3))
        for level in {LocationName.Lvl36, LocationName.Lvl37, LocationName.Lvl38, LocationName.Lvl39,
                      LocationName.Lvl40,
                      LocationName.Lvl41, LocationName.Lvl42, LocationName.Lvl43, LocationName.Lvl44,
                      LocationName.Lvl45, LocationName.Lvl46}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 4))
        for level in {LocationName.Lvl47, LocationName.Lvl48, LocationName.Lvl49, LocationName.Lvl50}:
            add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 5))
        # level 99 sanity
        if world.Level_Depth[player].value == 2:
            for level in {LocationName.Lvl51, LocationName.Lvl52, LocationName.Lvl53, LocationName.Lvl54,
                          LocationName.Lvl55,
                          LocationName.Lvl56, LocationName.Lvl57}:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 6))
            for level in {LocationName.Lvl58, LocationName.Lvl59, LocationName.Lvl60, LocationName.Lvl61,
                          LocationName.Lvl62, LocationName.Lvl63,
                          LocationName.Lvl64, LocationName.Lvl65, LocationName.Lvl66, LocationName.Lvl67,
                          LocationName.Lvl68}:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 7))
            for level in {LocationName.Lvl69, LocationName.Lvl70, LocationName.Lvl71, LocationName.Lvl72,
                          LocationName.Lvl73, LocationName.Lvl74,
                          LocationName.Lvl75, LocationName.Lvl76, LocationName.Lvl77, LocationName.Lvl78,
                          LocationName.Lvl79, }:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 8))
            for level in {LocationName.Lvl80, LocationName.Lvl81, LocationName.Lvl82, LocationName.Lvl83,
                          LocationName.Lvl84, LocationName.Lvl85,
                          LocationName.Lvl86, LocationName.Lvl87, LocationName.Lvl88, LocationName.Lvl89,
                          LocationName.Lvl90, LocationName.Lvl91,
                          LocationName.Lvl92, LocationName.Lvl93, LocationName.Lvl94, LocationName.Lvl95,
                          LocationName.Lvl96, LocationName.Lvl97,
                          LocationName.Lvl98, LocationName.Lvl99, }:
                add_rule(world.get_location(level, player), lambda state: state.kh_visit_locking_amount(player, 9))

    # if 0 then no visit locking if 1 then second visits if 2 then first and second visits with one item
    if world.Visit_locking[player].value == 1:
        add_rule(world.get_entrance(LocationName.Sp2_Region, player), lambda state: state.kh_sp_unlocked(player))
        add_rule(world.get_entrance(LocationName.Pr2_Region, player), lambda state: state.kh_pr_unlocked(player))
        add_rule(world.get_entrance(LocationName.TT2_Region, player), lambda state: state.kh_tt2_unlocked(player))
        add_rule(world.get_entrance(LocationName.TT3_Region, player), lambda state: state.kh_tt3_unlocked(player))
        add_rule(world.get_entrance(LocationName.Oc2_Region, player), lambda state: state.kh_oc_unlocked(player))
        add_rule(world.get_entrance(LocationName.Ht2_Region, player), lambda state: state.kh_ht_unlocked(player))
        add_rule(world.get_entrance(LocationName.LoD2_Region, player), lambda state: state.kh_lod_unlocked(player))
        add_rule(world.get_entrance(LocationName.Twtnw2_Region, player), lambda state: state.kh_twtnw_unlocked(player))
        add_rule(world.get_entrance(LocationName.Bc2_Region, player), lambda state: state.kh_bc_unlocked(player))
        add_rule(world.get_entrance(LocationName.Ag2_Region, player), lambda state: state.kh_ag_unlocked(player))
        add_rule(world.get_entrance(LocationName.Pl2_Region, player), lambda state: state.kh_pl_unlocked(player))
        add_rule(world.get_entrance(LocationName.Hb2_Region, player), lambda state: state.kh_hb_unlocked(player))
        add_rule(world.get_entrance(LocationName.Tr_Region, player), lambda state: state.kh_dc_unlocked(player))
        add_rule(world.get_entrance(LocationName.STT_Region, player), lambda state: state.kh_stt_unlocked(player))
    elif world.Visit_locking[player].value == 2:
        add_rule(world.get_entrance(LocationName.LoD_Region, player), lambda state: state.kh_lod_unlocked(player))
        add_rule(world.get_entrance(LocationName.Sp_Region, player), lambda state: state.kh_sp_unlocked(player))
        add_rule(world.get_entrance(LocationName.Pr_Region, player), lambda state: state.kh_pr_unlocked(player))
        add_rule(world.get_entrance(LocationName.TT_Region, player), lambda state: state.kh_tt_unlocked(player))
        add_rule(world.get_entrance(LocationName.TT2_Region, player), lambda state: state.kh_tt2_unlocked(player))
        add_rule(world.get_entrance(LocationName.TT3_Region, player), lambda state: state.kh_tt3_unlocked(player))
        add_rule(world.get_entrance(LocationName.Oc_Region, player), lambda state: state.kh_oc_unlocked(player))
        add_rule(world.get_entrance(LocationName.Ht_Region, player), lambda state: state.kh_ht_unlocked(player))
        add_rule(world.get_entrance(LocationName.Twtnw_Region, player), lambda state: state.kh_twtnw_unlocked(player))
        add_rule(world.get_entrance(LocationName.Bc_Region, player), lambda state: state.kh_bc_unlocked(player))
        add_rule(world.get_entrance(LocationName.Ag_Region, player), lambda state: state.kh_ag_unlocked(player))
        add_rule(world.get_entrance(LocationName.Pl_Region, player), lambda state: state.kh_pl_unlocked(player))
        add_rule(world.get_entrance(LocationName.Hb_Region, player), lambda state: state.kh_hb_unlocked(player))
        add_rule(world.get_entrance(LocationName.STT_Region, player), lambda state: state.kh_stt_unlocked(player))
