from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Items import exclusionItem_table
from ..generic.Rules import add_rule, forbid_items,add_item_rule,forbid_item
from .Locations import popupChecks,STT_Checks,CoR_Checks,Form_Checks,AG2_Checks


def set_rules(world: MultiWorld, player: int):
        world.completion_condition[player] = lambda state:state.has("Victory",player)
        add_rule(world.get_location(LocationName.FinalXemnas,player),lambda state:state.kh_FinalFights_unlocked(player))

        #Forbid Ablilites on popups due to game limitations
        for location in popupChecks:
            forbid_items(world.get_location(location,player),exclusionItem_table["Ability"]) 

        for location in STT_Checks:
            forbid_items(world.get_location(location,player),exclusionItem_table["Ability"])
        
                 
        #Santa's house also breaks with abilities
        forbid_items(world.get_location(LocationName.SantasHouseChristmasTownMap,player),exclusionItem_table["Ability"])
        forbid_items(world.get_location(LocationName.SantasHouseAPBoost,player),exclusionItem_table["Ability"])

        #Final checks of cor requires more locks than other checks in cor
        add_rule(world.get_location(LocationName.CoRMineshaftUpperLevelAPBoost,player),lambda state:
                     state.kh_HighJump_level(player,3)
                 and state.kh_AerialDodge_level(player,3)
                 and state.kh_Glide_level(player,3))
        add_rule(world.get_location(LocationName.TransporttoRemembrance,player),lambda state:
                     state.kh_HighJump_level(player,3)
                 and state.kh_AerialDodge_level(player,3)
                 and state.kh_Glide_level(player,3))


        for formlvl2 in {LocationName.Valorlvl2,LocationName.Wisdomlvl2,LocationName.Limitlvl2,LocationName.Masterlvl2,LocationName.Finallvl2}:
                add_rule(world.get_location(formlvl2,player),lambda state: state.kh_FormLevel_unlocked(player,1))

        for formlvl3 in {LocationName.Valorlvl3,LocationName.Wisdomlvl3,LocationName.Limitlvl3,LocationName.Masterlvl3,LocationName.Finallvl3}:
                add_rule(world.get_location(formlvl3,player),lambda state: state.kh_FormLevel_unlocked(player,1))

        for formlvl4 in {LocationName.Valorlvl4,LocationName.Wisdomlvl4,LocationName.Limitlvl4,LocationName.Masterlvl4,LocationName.Finallvl4}:
                add_rule(world.get_location(formlvl4,player),lambda state: state.kh_FormLevel_unlocked(player,2))

        for formlvl5 in {LocationName.Valorlvl5,LocationName.Wisdomlvl5,LocationName.Limitlvl5,LocationName.Masterlvl5,LocationName.Finallvl5}:
                add_rule(world.get_location(formlvl5,player),lambda state: state.kh_FormLevel_unlocked(player,3))

        for formlvl6 in {LocationName.Valorlvl6,LocationName.Wisdomlvl6,LocationName.Limitlvl6,LocationName.Masterlvl6,LocationName.Finallvl6}:
                add_rule(world.get_location(formlvl6,player),lambda state: state.kh_FormLevel_unlocked(player,4))

        for formlvl7 in {LocationName.Valorlvl7,LocationName.Wisdomlvl7,LocationName.Limitlvl7,LocationName.Masterlvl7,LocationName.Finallvl7}:
                add_rule(world.get_location(formlvl7,player),lambda state: state.kh_FormLevel_unlocked(player,5))
        
        
        #Option to be more in line of the current KH2 Randomizer
        if world.Max_Logic[player].value==1:
            for location in CoR_Checks:
                forbid_items(world.get_location(location,player), exclusionItem_table["Forms"])
                forbid_item(world.get_location(location,player),player, "Torn Page")
            for location in AG2_Checks:
                forbid_items(world.get_location(location,player), exclusionItem_table["Forms"])
                forbid_item(world.get_location(location,player),player, "Torn Page")
            #forbid forms on forms
            for location in Form_Checks:
                forbid_items(world.get_location(location,player),exclusionItem_table["Forms"])
                forbid_item(world.get_location(location,player),player, "Torn Page")

        #Creating Accsess rules for terra and mushroom 13 checks
        add_rule(world.get_location(LocationName.LingeringWillBonus,player),lambda state: state.has(ItemName.ProofofConnection,player))
        add_rule(world.get_location(LocationName.LingeringWillProofofConnection,player),lambda state: state.has(ItemName.ProofofConnection,player))
        add_rule(world.get_location(LocationName.LingeringWillManifestIllusion,player),lambda state: state.has(ItemName.ProofofConnection,player))
        add_rule(world.get_location(LocationName.WinnersProof,player),lambda state: state.has(ItemName.ProofofPeace,player))
        add_rule(world.get_location(LocationName.ProofofPeace,player),lambda state: state.has(ItemName.ProofofPeace,player))

        #if 0 then no visit locking if 1 then second visits if 2 then first and second visits with one item
        if(world.Visit_locking[player].value==1):
            add_rule(world.get_entrance(LocationName.Sp2_Region,player),lambda state:state.kh_sp_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pr2_Region,player),lambda state:state.kh_pr_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT2_Region,player),lambda state:state.kh_tt2_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT3_Region,player),lambda state:state.kh_tt3_unlocked(player))
            add_rule(world.get_entrance(LocationName.Oc2_Region,player),lambda state:state.kh_oc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ht2_Region,player),lambda state:state.kh_ht_unlocked(player))
            add_rule(world.get_entrance(LocationName.LoD2_Region,player),lambda state:state.kh_lod_unlocked(player))
            add_rule(world.get_entrance(LocationName.Twtnw2_Region,player),lambda state:state.kh_twtnw_unlocked(player)) 
            add_rule(world.get_entrance(LocationName.Bc2_Region,player),lambda state:state.kh_bc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ag2_Region,player),lambda state:state.kh_ag_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pl2_Region,player),lambda state:state.kh_pl_unlocked(player))
            add_rule(world.get_entrance(LocationName.Hb2_Region,player),lambda state:state.kh_hb_unlocked(player))
            add_rule(world.get_entrance(LocationName.Tr_Region,player),lambda state:state.kh_dc_unlocked(player))
            add_rule(world.get_entrance(LocationName.STT_Region,player),lambda state:state.kh_stt_unlocked(player))
        elif(world.Visit_locking[player].value==2):
            add_rule(world.get_entrance(LocationName.LoD_Region,player),lambda state:state.kh_lod_unlocked(player))
            add_rule(world.get_entrance(LocationName.Sp_Region,player),lambda state:state.kh_sp_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pr_Region,player),lambda state:state.kh_pr_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT_Region,player),lambda state:state.kh_tt_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT2_Region,player),lambda state:state.kh_tt2_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT3_Region,player),lambda state:state.kh_tt3_unlocked(player))
            add_rule(world.get_entrance(LocationName.Oc_Region,player),lambda state:state.kh_oc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ht_Region,player),lambda state:state.kh_ht_unlocked(player))
            add_rule(world.get_entrance(LocationName.Twtnw_Region,player),lambda state:state.kh_twtnw_unlocked(player))
            add_rule(world.get_entrance(LocationName.Bc_Region,player),lambda state:state.kh_bc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ag_Region,player),lambda state:state.kh_ag_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pl_Region,player),lambda state:state.kh_pl_unlocked(player))
            add_rule(world.get_entrance(LocationName.Hb_Region,player),lambda state:state.kh_hb_unlocked(player))
            add_rule(world.get_entrance(LocationName.STT_Region,player),lambda state:state.kh_stt_unlocked(player))


            
