from ast import Import
import typing
from ..AutoWorld import LogicMixin
from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .logic import KH2Logic
from .Items import item_dictionary_table, ItemData,get_item_type,exclusionItem_table
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
from .Locations import all_locations,exclusion_table,getBonus,popupChecks,formChecks,ag2Checks,corChecks
from .Options import FinalEXP, KH2_Options, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,Visitlocking


def set_rules(world: MultiWorld, player: int):
        ##Locks forms out of ag because im too lazy to make logic for it
<<<<<<< HEAD
       # print(lambda state:state._kh_FormLevel_unlocked(self,player).value)
        #print(countForms(self))
        #set_rule(world.get_entrance(LocationName.TT_Region, player),lambda state:state.kh_tt_unlocked(player))
=======
       # print(lambda state:state._kh_FormLevel_Unlocked(self,player).value)
        #print(countForms(self))
        set_rule(world.get_entrance(LocationName.TT_Region, player),lambda state:state.kh_tt_unlocked(player))
        #add_item_rule(world.get_location(LocationName.RuinedChamberTornPages, player),
        #          lambda item: get_item_type(item) == "Wisdom Form")
        #set_rule(world.get_location("Valor level 2",player), lambda state: (state.has(ItemName.NamineSketches, player))
         #"Route 11 - Oak's Aide": lambda state: state.pokemon_rb_has_pokemon(state.world.oaks_aide_rt_11[player].value + 5, player),
<<<<<<< HEAD
        #print(lambda state:(state.kh_FormLevel_unlocked(state,player)==1))
        add_rule(world.get_location(LocationName.FinalXemnas,player),lambda state:state.kh_FinalFights_unlocked(player))

        world.completion_condition[player] = lambda state:state.has("Victory",player)
        
        
        set_rule(world.get_location(LocationName.CoRMineshaftUpperLevelAPBoost,player),lambda state:
                     state.kh_HighJump_level(player,3)
                 and state.kh_AerialDodge_level(player,3)
                 and state.kh_Glide_level(player,3))

        set_rule(world.get_location(LocationName.Valorlvl2,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl3,player),lambda state: state.kh_FormLevel_unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl4,player),lambda state: state.kh_FormLevel_unlocked(player,2))
        add_rule(world.get_location(LocationName.Valorlvl5,player),lambda state: state.kh_FormLevel_unlocked(player,3))
        add_rule(world.get_location(LocationName.Valorlvl6,player),lambda state: state.kh_FormLevel_unlocked(player,4))
        set_rule(world.get_location(LocationName.Valorlvl7,player),lambda state: state.kh_FormLevel_unlocked(player,5))
        
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
        
        #add_rule(world.get_location(LocationName.Valorlvl2,player),lambda state:state.kh_FormLevel_unlocked(player,1))
        #add_rule(world.get_location(LocationName.Valorlvl3,player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Wisdom Form",player)))
        #add_rule(world.get_location(LocationName.Valorlvl4,player),lambda state:(state.kh_FormLevel_unlocked(player,2)))
        #add_rule(world.get_location(LocationName.Valorlvl5,player),lambda state:(state.kh_FormLevel_unlocked(player,3)))
        #add_rule(world.get_location(LocationName.Valorlvl6,player),lambda state:(state.kh_FormLevel_unlocked(player,4)))
        #add_rule(world.get_location(LocationName.Valorlvl7,player),lambda state:(state.kh_FormLevel_unlocked(player,5)))
        #                                                                                                                   
        #add_rule(world.get_location("Limit level 2",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Limit Form",player)))
        #add_rule(world.get_location("Limit level 3",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Limit Form",player)))
        #add_rule(world.get_location("Limit level 4",player),lambda state:(state.kh_FormLevel_unlocked(player,2)))
        #add_rule(world.get_location("Limit level 5",player),lambda state:(state.kh_FormLevel_unlocked(player,3)))
        #add_rule(world.get_location("Limit level 6",player),lambda state:(state.kh_FormLevel_unlocked(player,4)))
        #add_rule(world.get_location("Limit level 7",player),lambda state:(state.kh_FormLevel_unlocked(player,5)))
        ##                                                                                                                   
        ##add_rule(world.get_location("Master level 2",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Master Form",player)))
        ##add_rule(world.get_location("Master level 3",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Master Form",player)))
        #add_rule(world.get_location("Master level 4",player),lambda state:(state.kh_FormLevel_unlocked(player,2)))
        #add_rule(world.get_location("Master level 5",player),lambda state:(state.kh_FormLevel_unlocked(player,3)))
        #add_rule(world.get_location("Master level 6",player),lambda state:(state.kh_FormLevel_unlocked(player,4)))
        #add_rule(world.get_location("Master level 7",player),lambda state:(state.kh_FormLevel_unlocked(player,5)))
        ##                                                                                                                   
        ##add_rule(world.get_location("Final level 2",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Final Form",player)))
        ##add_rule(world.get_location("Final level 3",player),lambda state:(state.kh_FormLevel_unlocked(self)==1 and state.has("Final Form",player)))
        #add_rule(world.get_location("Final level 4",player),lambda state:(state.kh_FormLevel_unlocked(player,2)))
        #add_rule(world.get_location("Final level 5",player),lambda state:(state.kh_FormLevel_unlocked(player,3)))
        #add_rule(world.get_location("Final level 6",player),lambda state:(state.kh_FormLevel_unlocked(player,4)))
        #add_rule(world.get_location("Final level 7",player),lambda state:(state.kh_FormLevel_unlocked(player,5)))
=======
        print(lambda state:(state.kh_FormLevel_Unlocked(state,player)==1))
        
        
        
        
        
        
        set_rule(world.get_location(LocationName.Valorlvl2,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl3,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Valorlvl4,player),lambda state: state.kh_FormLevel_Unlocked(player,2))
        add_rule(world.get_location(LocationName.Valorlvl5,player),lambda state: state.kh_FormLevel_Unlocked(player,3))
        add_rule(world.get_location(LocationName.Valorlvl6,player),lambda state: state.kh_FormLevel_Unlocked(player,4))
        set_rule(world.get_location(LocationName.Valorlvl7,player),lambda state: state.kh_FormLevel_Unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Wisdomlvl2,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Wisdomlvl3,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Wisdomlvl4,player),lambda state: state.kh_FormLevel_Unlocked(player,2))
        add_rule(world.get_location(LocationName.Wisdomlvl5,player),lambda state: state.kh_FormLevel_Unlocked(player,3))
        add_rule(world.get_location(LocationName.Wisdomlvl6,player),lambda state: state.kh_FormLevel_Unlocked(player,4))
        add_rule(world.get_location(LocationName.Wisdomlvl7,player),lambda state: state.kh_FormLevel_Unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Limitlvl2,player),lambda state:  state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Limitlvl3,player),lambda state:  state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Limitlvl4,player),lambda state:  state.kh_FormLevel_Unlocked(player,2))
        add_rule(world.get_location(LocationName.Limitlvl5,player),lambda state:  state.kh_FormLevel_Unlocked(player,3))
        add_rule(world.get_location(LocationName.Limitlvl6,player),lambda state:  state.kh_FormLevel_Unlocked(player,4))
        add_rule(world.get_location(LocationName.Limitlvl7,player),lambda state:  state.kh_FormLevel_Unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Masterlvl2,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Masterlvl3,player),lambda state: state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Masterlvl4,player),lambda state: state.kh_FormLevel_Unlocked(player,2))
        add_rule(world.get_location(LocationName.Masterlvl5,player),lambda state: state.kh_FormLevel_Unlocked(player,3))
        add_rule(world.get_location(LocationName.Masterlvl6,player),lambda state: state.kh_FormLevel_Unlocked(player,4))
        add_rule(world.get_location(LocationName.Masterlvl7,player),lambda state: state.kh_FormLevel_Unlocked(player,5))
        
        add_rule(world.get_location(LocationName.Finallvl2,player),lambda state:  state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Finallvl3,player),lambda state:  state.kh_FormLevel_Unlocked(player,1))
        add_rule(world.get_location(LocationName.Finallvl4,player),lambda state:  state.kh_FormLevel_Unlocked(player,2))
        add_rule(world.get_location(LocationName.Finallvl5,player),lambda state:  state.kh_FormLevel_Unlocked(player,3))
        add_rule(world.get_location(LocationName.Finallvl6,player),lambda state:  state.kh_FormLevel_Unlocked(player,4))
        add_rule(world.get_location(LocationName.Finallvl7,player),lambda state:  state.kh_FormLevel_Unlocked(player,5))
        
        #add_rule(world.get_location(LocationName.Valorlvl2,player),lambda state:state.kh_FormLevel_Unlocked(player,1))
        #add_rule(world.get_location(LocationName.Valorlvl3,player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Wisdom Form",player)))
        #add_rule(world.get_location(LocationName.Valorlvl4,player),lambda state:(state.kh_FormLevel_Unlocked(player,2)))
        #add_rule(world.get_location(LocationName.Valorlvl5,player),lambda state:(state.kh_FormLevel_Unlocked(player,3)))
        #add_rule(world.get_location(LocationName.Valorlvl6,player),lambda state:(state.kh_FormLevel_Unlocked(player,4)))
        #add_rule(world.get_location(LocationName.Valorlvl7,player),lambda state:(state.kh_FormLevel_Unlocked(player,5)))
        #                                                                                                                   
        #add_rule(world.get_location("Limit level 2",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Limit Form",player)))
        #add_rule(world.get_location("Limit level 3",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Limit Form",player)))
        #add_rule(world.get_location("Limit level 4",player),lambda state:(state.kh_FormLevel_Unlocked(player,2)))
        #add_rule(world.get_location("Limit level 5",player),lambda state:(state.kh_FormLevel_Unlocked(player,3)))
        #add_rule(world.get_location("Limit level 6",player),lambda state:(state.kh_FormLevel_Unlocked(player,4)))
        #add_rule(world.get_location("Limit level 7",player),lambda state:(state.kh_FormLevel_Unlocked(player,5)))
        ##                                                                                                                   
        ##add_rule(world.get_location("Master level 2",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Master Form",player)))
        ##add_rule(world.get_location("Master level 3",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Master Form",player)))
        #add_rule(world.get_location("Master level 4",player),lambda state:(state.kh_FormLevel_Unlocked(player,2)))
        #add_rule(world.get_location("Master level 5",player),lambda state:(state.kh_FormLevel_Unlocked(player,3)))
        #add_rule(world.get_location("Master level 6",player),lambda state:(state.kh_FormLevel_Unlocked(player,4)))
        #add_rule(world.get_location("Master level 7",player),lambda state:(state.kh_FormLevel_Unlocked(player,5)))
        ##                                                                                                                   
        ##add_rule(world.get_location("Final level 2",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Final Form",player)))
        ##add_rule(world.get_location("Final level 3",player),lambda state:(state.kh_FormLevel_Unlocked(self)==1 and state.has("Final Form",player)))
        #add_rule(world.get_location("Final level 4",player),lambda state:(state.kh_FormLevel_Unlocked(player,2)))
        #add_rule(world.get_location("Final level 5",player),lambda state:(state.kh_FormLevel_Unlocked(player,3)))
        #add_rule(world.get_location("Final level 6",player),lambda state:(state.kh_FormLevel_Unlocked(player,4)))
        #add_rule(world.get_location("Final level 7",player),lambda state:(state.kh_FormLevel_Unlocked(player,5)))
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        for x in range(len(corChecks)):
            forbid_item(world.get_location(corChecks[x],player),player, exclusionItem_table["Forms"] and "Torn Page")
        #forbid forms and torn pages in ag2 to prevent softlock
        #Might not need to do this because ap already has logic
        for x in range(len(ag2Checks)):
            forbid_item(world.get_location(ag2Checks[x],player),player, exclusionItem_table["Forms"] and "Torn Page")
        #forbid forms on forms
        for x in range(len(formChecks)):
            forbid_item(world.get_location(formChecks[x],player),player, exclusionItem_table["Forms"] and "Torn Page")
        #Forbit ablitys on popups due to game limitations
        for x in range(len(popupChecks)):
            forbid_item(world.get_location(popupChecks[x],player),player,exclusionItem_table["Ability"])
        #No proof of connection or peace on terra and same for 13 mushrooms
        forbid_item(world.get_location("Lingering Will Bonus",player),player,"Proof of Peace")
        forbid_item(world.get_location("Lingering Will Bonus",player),player,"Proof of Connection")
        forbid_item(world.get_location("Lingering Will Proof of Connection",player),player,"Proof of Peace")
        forbid_item(world.get_location("Lingering Will Proof of Connection",player),player,"Proof of Connection")
        forbid_item(world.get_location("Lingering Will Manifest Illusion",player),player,"Proof of Peace")
        forbid_item(world.get_location("Lingering Will Manifest Illusion",player),player,"Proof of Connection")
        forbid_item(world.get_location("Winner's Proof",player),player,"Proof of Peace")
        forbid_item(world.get_location("Proof of Peace",player),player,"Proof of Peace")
        #
        world.completion_condition[player] = lambda state:state.kh_FinalFights_Unlocked(player)
    #sets torn page requirements

    ##LOOK AT THIS YOU STUPID
    #    set_rule(world.get_entrance(LocationName.TT_Region,player),lambda state:state._kh_torn_page_1(player,1))
    #    set_rule(world.get_entrance(all_locations.HundredAcre3_Checks,player),lambda state:state._kh_torn_page_2(player,2))
    #    set_rule(world.get_entrance(all_locations.HundredAcre4_Checks,player),lambda state:state._kh_torn_page_3(player,3))
    #    set_rule(world.get_entrance(all_locations.HundredAcre5_Checks,player),lambda state:state._kh_torn_page_4(player,4))
    #    set_rule(world.get_entrance(all_locations.HundredAcre6_Checks,player),lambda state:state._kh_torn_page_5(player,5))
        #if 0 then no visit locking  if 1 then second visits if 2 then first and second visits with one item
        if(world.Visit_locking[player].value==1):
            add_rule(world.get_entrance(LocationName.Sp2_Region,player),lambda state:state.kh_sp_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pr2_Region,player),lambda state:state.kh_pr_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT2_Region,player),lambda state:state.kh_tt2_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT3_Region,player),lambda state:state.kh_tt3_unlocked(player))
            add_rule(world.get_entrance(LocationName.Oc2_Region,player),lambda state:state.kh_oc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ht2_Region,player),lambda state:state.kh_ht_unlocked(player))
            add_rule(world.get_entrance(LocationName.LoD2_Region,player),lambda state:state.kh_lod_unlocked(player))
<<<<<<< HEAD
            add_rule(world.get_entrance(LocationName.Twtnw2_Region,player),lambda state:state.kh_twtnw_unlocked(player))
=======
            add_rule(world.get_entrance(LocationName.Twtnw2_Region,player),lambda state:state.kh_twtnw_unlocked(player) and state.kh_twtnw2_unlocked(player))
            add_rule(world.get_entrance(LocationName.Bc2_Region,player),lambda state:state.kh_bc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ag2_Region,player),lambda state:state.kh_ag_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pl2_Region,player),lambda state:state.kh_pl_unlocked(player))
            add_rule(world.get_entrance(LocationName.Hb2_Region,player),lambda state:state.kh_hb_unlocked(player))
            add_rule(world.get_entrance(LocationName.Tr_Region,player),lambda state:state.kh_dc_unlocked(player))
<<<<<<< HEAD
            add_rule(world.get_entrance(LocationName.STT_Region,player),lambda state:state.kh_stt_unlocked(player))
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        elif(world.Visit_locking[player].value==2):
            add_rule(world.get_entrance(LocationName.Sp_Region,player),lambda state:state.kh_sp_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pr_Region,player),lambda state:state.kh_pr_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT_Region,player),lambda state:state.kh_tt_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT2_Region,player),lambda state:state.kh_tt2_unlocked(player))
            add_rule(world.get_entrance(LocationName.TT3_Region,player),lambda state:state.kh_tt3_unlocked(player))
            add_rule(world.get_entrance(LocationName.Oc_Region,player),lambda state:state.kh_oc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ht_Region,player),lambda state:state.kh_ht_unlocked(player))
            add_rule(world.get_entrance(LocationName.LoD_Region,player),lambda state:state.kh_lod_unlocked(player))
<<<<<<< HEAD
            add_rule(world.get_entrance(LocationName.Twtnw_Region,player),lambda state:state.kh_twtnw_unlocked(player))
=======
            add_rule(world.get_entrance(LocationName.Twtnw_Region,player),lambda state:state.kh_twtnw_unlocked(player) and state.kh_twtnw_unlocked(player))
            add_rule(world.get_entrance(LocationName.Bc_Region,player),lambda state:state.kh_bc_unlocked(player))
            add_rule(world.get_entrance(LocationName.Ag_Region,player),lambda state:state.kh_ag_unlocked(player))
            add_rule(world.get_entrance(LocationName.Pl_Region,player),lambda state:state.kh_pl_unlocked(player))
            add_rule(world.get_entrance(LocationName.Hb_Region,player),lambda state:state.kh_hb_unlocked(player))
            add_rule(world.get_entrance(LocationName.Dc_Region,player),lambda state:state.kh_dc_unlocked(player))
<<<<<<< HEAD
            add_rule(world.get_entrance(LocationName.STT_Region,player),lambda state:state.kh_stt_unlocked(player))

=======

            #add_rule(world.get_entrance(LocationName.TT_Region,player),lambda state:state.kh_tt_unlocked)
            
            

        #print(world.Valor_Form_Level[player].value)
    #if 1 then no visit locking  if 2 then second visits if 3 then first and second visits with one item  
        #if Visitlocking.value==2 or Visitlocking==3:
        #    add_rule(world.get_entrance(all_locations.LoD2_Checks, player),lambda state:state._kh_lod_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.TWTNW2_Checks,player),lambda state:state._kh_twtnw_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.TT2_Checks,player),lambda state:state._kh_tt2_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.TT3_Checks,player),lambda state:state._kh_tt3_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.PL2_Checks,player),lambda state:state._kh_pl_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.CoR_Checks,player),lambda state:state._kh_hb_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.FirstHalf_Checks, player),lambda state:state._kh_hb_unlocked(player) and state._kh_first_half_cor(player,2))
        #    add_rule(world.get_entrance(all_locations.SecondHalf_Checks,player),lambda state:state._kh_hb_unlocked(player) and state._kh_first_half_cor(player,2) and state._kh_second_half_cor(player,3))
        #    add_rule(world.get_entrance(all_locations.HB2_Checks,player),lambda state:state._kh_hb_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.PR2_Checks,player),lambda state:state._kh_pr_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.SP2_Checks,player),lambda state:state._kh_sp_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.BC2_Checks,player),lambda state:state._kh_bc_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.OC2_Checks,player),lambda state:state._kh_oc_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.ShitCups,player),lambda state:state._kh_oc_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.BetterCups,player),lambda state:state._kh_oc_unlocked(player))
        #    add_rule(world.get_entrance(all_locations.HundredAcre1_Checks,player),lambda state:state._kh_oc_unlocked(player))
        #    #add_rule(world.get_entrance(all_locations.AG2_Checks,player),lambda state:state._kh_ag_unlocked(player)>=1))
        #
        #    if Visitlocking.value==3:
        #       add_rule(world.get_entrance(all_locations.LoD_Checks, player),lambda state:state._kh_lod_unlocked(self,player))
        #       add_rule(world.get_entrance(all_locations.TWTNW_Checks,player),lambda state:state._kh_twtnw_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.TT_Checks,player),lambda state:state._kh_tt2_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.PL_Checks,player),lambda state:state._kh_pl_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.HB_Checks,player),lambda state:state._kh_hb_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.PR_Checks,player),lambda state:state._kh_pr_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.SP_Checks,player),lambda state:state._kh_sp_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.BC_Checks,player),lambda state:state._kh_bc_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.OC_Checks,player),lambda state:state._kh_oc_unlocked(player))
        #       add_rule(world.get_entrance(all_locations.AG_Checks,player),lambda state:state._kh_ag_unlocked(player))

  
            

# #piglets house
#def _kh_torn_page_1(self, player: int):
#   return has('Torn Page', player, 1)
##rabbits
#def _kh_torn_page_2(self, player: int):
#    return has('Torn Page', player, 2)
##kangroo's house
#def _kh_torn_page_3(self, player: int):
#    return has('Torn Page', player, 3)
##spooky cave
#def _kh_torn_page_4(self, player: int):
#    return has('Torn Page', player, 4)
##Stary Hill
#def _kh_torn_page_5(self, player: int):
#    return has('Torn Page', player, 5)
##Movement logic for cor
#def _kh_first_half_cor(self,player):
#    return has('Quick Run',player,2) and ('Aerial Dodge ',player,2)
#def _kh_second_half_cor(self,player):
#    return has('High Jump',player,3) and ('Aerial Dodge ',player,3) and ('Glide',player,3)
#def _kh_lod_unlocked(self,player):
#        return has('Sword of the Ancestor',player)
#def _kh_oc_unlocked(self,player):
#    return has('Battlefields of War',player)
#def _kh_twtnw_unlocked(self,player):
#    return has('Way to the Dawn',player)or('Quick Run',player,1)
#def _kh_ht_unlocked(self,player):
#    return has('Bone Fist',player)
#def _kh_tt_unlocked(self,player:int):
#   return has('Poster',player)
#def _kh_tt2_unlocked(self,player):
#    return has('Ice Cream',player)
#def _kh_tt3_unlocked(self,player):
#    return has('Picture',player) and has('Ice Cream',player)
#def _kh_pr_unlocked(self,player):
#    return has('Skill and Crossbones',player)
#def _kh_sp_unlocked(self,player):
#    return has('Idenity Disk',player)
#def _kh_stt_unlocked(self,player:int):
#     return has('Namine Sketches',player)
##Using Dummy 13 for this
#def _kh_dc_unlocked(self,player:int):
#    return has('Disney Castle Key',player)
#def _kh_hb_unlocked(self,player):
#    return has('Membership Card',player)
#def _kh_pl_unlocked(self,player):
#    return has('Proud Fang',player)
#def _kh_ag_unlocked(self,player):
#    return has('Scimitar',player)
#def _kh_ag_unlocked(self,player:int):
#    return has('Scimitar',player)and ('fire element',player,1)and('blizzard element',player,1)and('thunder element',1)
#def _kh_bc_unlocked(self,player):
#    return has("Beast's Claw",player)
<<<<<<< HEAD
#def _kh_FinalFights_unlocked(self,player):
#        return has('Proof of Connection',player,1)and('Proof of Nonexistence',player,1)and('Proof of Peace',player,1)
#def _kh_FormLevel_unlocked(self,player):
=======
#def _kh_FinalFights_Unlocked(self,player):
#        return has('Proof of Connection',player,1)and('Proof of Nonexistence',player,1)and('Proof of Peace',player,1)
#def _kh_FormLevel_Unlocked(self,player):
#    formlevel=0
#    if has("Valor Form",player,1):
#        formlevel=+1
#    if has("Wisdom Form",player,1):
#        formlevel=+1
#    if has("Limit Form",player,1):
#        formlevel=+1
#    if has("Master Form",player,1):
#        formlevel=+1
#    if has("Final Form",player,1):
#        formlevel=+1
#    return formlevel
#
#