from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Items import exclusionItem_table
from ..generic.Rules import add_rule, forbid_item
from .Locations import popupChecks,formChecks,ag2Checks,corChecks


def set_rules(world: MultiWorld, player: int):
        world.completion_condition[player] = lambda state:state.has("Victory",player)
        add_rule(world.get_location(LocationName.FinalXemnas,player),lambda state:state.kh_FinalFights_unlocked(player))

        #Forbid Ablilites on popups due to game limitations
        for location in popupChecks:
            if location==LocationName.EncampmentAreaMap:
                print("your momma")
            forbid_item(world.get_location(location,player),player,exclusionItem_table["Ability"])        
        
        #Final checks of cor requires more locks than other checks in cor
        add_rule(world.get_location(LocationName.CoRMineshaftUpperLevelAPBoost,player),lambda state:
                     state.kh_HighJump_level(player,3)
                 and state.kh_AerialDodge_level(player,3)
                 and state.kh_Glide_level(player,3))
        add_rule(world.get_location(LocationName.TransporttoRemembrance,player),lambda state:
                     state.kh_HighJump_level(player,3)
                 and state.kh_AerialDodge_level(player,3)
                 and state.kh_Glide_level(player,3))


        add_rule(world.get_location(LocationName.Valorlvl2,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl3,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl4,player),lambda state: state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Valorlvl5,player),lambda state: state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Valorlvl6,player),lambda state: state.kh_FormLevel_unlocked(player,4))
        add_rule(world.get_location(LocationName.Valorlvl7,player),lambda state: state.kh_FormLevel_unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Wisdomlvl2,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Wisdomlvl3,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Wisdomlvl4,player),lambda state: state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Wisdomlvl5,player),lambda state: state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Wisdomlvl6,player),lambda state: state.kh_FormLevel_unlocked(player,4))
        add_rule(world.get_location(LocationName.Wisdomlvl7,player),lambda state: state.kh_FormLevel_unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Limitlvl2,player),lambda state:  state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Limitlvl3,player),lambda state:  state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Limitlvl4,player),lambda state:  state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Limitlvl5,player),lambda state:  state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Limitlvl6,player),lambda state:  state.kh_FormLevel_unlocked(player,4))
        add_rule(world.get_location(LocationName.Limitlvl7,player),lambda state:  state.kh_FormLevel_unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Masterlvl2,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Masterlvl3,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Masterlvl4,player),lambda state: state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Masterlvl5,player),lambda state: state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Masterlvl6,player),lambda state: state.kh_FormLevel_unlocked(player,4))
        add_rule(world.get_location(LocationName.Masterlvl7,player),lambda state: state.kh_FormLevel_unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Finallvl2,player),lambda state:  state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Finallvl3,player),lambda state:  state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Finallvl4,player),lambda state:  state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Finallvl5,player),lambda state:  state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Finallvl6,player),lambda state:  state.kh_FormLevel_unlocked(player,4))
        add_rule(world.get_location(LocationName.Finallvl7,player),lambda state:  state.kh_FormLevel_unlocked(player,5))
        
        #Option to be more in line of the current KH2 Randomizer
        if world.Max_Logic[player].value==0:
            for location in corChecks:
                forbid_item(world.get_location(location,player),player, exclusionItem_table["Forms"] and "Torn Page")
            for location in ag2Checks:
                forbid_item(world.get_location(location,player),player, exclusionItem_table["Forms"] and "Torn Page")
            #forbid forms on forms
            for location in formChecks:
                forbid_item(world.get_location(formChecks[x],player),player, exclusionItem_table["Forms"] and "Torn Page")

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


            
