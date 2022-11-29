from ast import Import
import typing
from ..AutoWorld import LogicMixin
from BaseClasses import MultiWorld
#from .Regions import HundredAcre1_Region
from .Names import LocationName, ItemName
from .Items import item_dictionary_table, ItemData,get_item_type,exclusionItem_table
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
from .Locations import all_locations,exclusion_table,getBonus
from .Options import FinalEXP, KH2_Options, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,Visitlocking


def set_rules(world: MultiWorld, player: int,self):
        ##Locks forms out of ag because im too lazy to make logic for it
        #add_item_rule(self.world.get_location(LocationName.RuinedChamberTornPages, self.player),
        #          lambda item: get_item_type(item) == "Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,Forms_Table.name)
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),player,"Wisdom Form")
        #forbid_item(self.world.get_entrance(all_locations.AG2_Checks,self.player,player, "Final Form"))
        #forbid_item(self.world.get_entrance(all_locations.AG2_Checks,self.player,player, "Limit Form"))
        #forbid_item(self.world.get_entrance(all_locations.AG2_Checks,self.player,player, "Valor Form"))
        #forbid_item(self.world.get_entrance(all_locations.AG2_Checks,self.player,player, "Master Form"))
        #forbid_item(self.world.get_entrance(all_locations.AG2_Checks,self.player,player, "Torn Page"))
        ##locks forms and torn pages from cor
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Torn Page"))
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Wisdom Form"))
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Final Form"))
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Limit Form"))
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Valor Form"))
        #forbid_item(self.world.get_entrance(all_locations.FirstHalf_Checks, self.player, "Master Form"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Torn Page"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Wisdom Form"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Final Form"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Limit Form"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Valor Form"))
        #forbid_item(self.world.get_entrance(all_locations.SecondHalf_Checks, self.player, "Master Form"))
        ##forbid forms on forms
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Wisdom Form"))
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Final Form"))
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Limit Form"))
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Valor Form"))
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Master Form"))
        #forbid_item(self.world.get_entrance(all_locations.form_checks, self.player, "Torn Page"))
        #Forbit ablitys on popups due to game limitations
        #forbid_item(self.world.get_location(LocationName.RuinedChamberTornPages,self.player),self.player,exclusionItem_table["SupportAbility"])
        #forbid_item(self.world.get_location(exclusion_table.Popups,self.player,all_locations.LvlAbility_Table))
        #forbid_item(self.world.get_location(exclusion_table.Popups,self.player,all_locations.ActionAbility_Table))
        ##No proof of connection or peace on terra and same for 13 mushrooms
        #forbid_item(self.world.get_location("Lingering Will Bonus",self.player,"Proof of Peace"))
        #forbid_item(self.world.get_location("Lingering Will Bonus",self.player,"Proof of Connection"))
        #forbid_item(self.world.get_location("Lingering Will Proof of Connection",self.player,"Proof of Peace"))
        #forbid_item(self.world.get_location("Lingering Will Proof of Connection",self.player,"Proof of Connection"))
        #forbid_item(self.world.get_location("Lingering Will Manifest Illusion",self.player,"Proof of Peace"))
        #forbid_item(self.world.get_location("Lingering Will Manifest Illusion",self.player,"Proof of Connection"))
        #forbid_item(self.world.get_location("Winner's Proof",self.player,"Proof of Peace"))
        #forbid_item(self.world.get_location("Proof of Peace Location",self.player,"Proof of Peace"))
        #
        #world.completion_condition[player] = lambda state:state._kh_FinalFights_Unlocked(self,player)
    #sets torn page requirements

    #LOOK AT THIS YOU STUPID
        set_rule(world.get_entrance(LocationName.TT_Region,self.player),lambda state:state._kh_torn_page_1(player,1))
        set_rule(world.get_entrance(all_locations.HundredAcre3_Checks,player),lambda state:state._kh_torn_page_2(player,2))
        set_rule(world.get_entrance(all_locations.HundredAcre4_Checks,player),lambda state:state._kh_torn_page_3(player,3))
        set_rule(world.get_entrance(all_locations.HundredAcre5_Checks,player),lambda state:state._kh_torn_page_4(player,4))
        set_rule(world.get_entrance(all_locations.HundredAcre6_Checks,player),lambda state:state._kh_torn_page_5(player,5))
    
    #if 1 then no visit locking  if 2 then second visits if 3 then first and second visits with one item  
        if Visitlocking.value==2 or Visitlocking==3:
            add_rule(world.get_entrance(all_locations.LoD2_Checks, player),lambda state:state._kh_lod_unlocked(player))
            add_rule(world.get_entrance(all_locations.TWTNW2_Checks,player),lambda state:state._kh_twtnw_unlocked(player))
            add_rule(world.get_entrance(all_locations.TT2_Checks,player),lambda state:state._kh_tt2_unlocked(player))
            add_rule(world.get_entrance(all_locations.TT3_Checks,player),lambda state:state._kh_tt3_unlocked(player))
            add_rule(world.get_entrance(all_locations.PL2_Checks,player),lambda state:state._kh_pl_unlocked(player))
            add_rule(world.get_entrance(all_locations.CoR_Checks,player),lambda state:state._kh_hb_unlocked(player))
            add_rule(world.get_entrance(all_locations.FirstHalf_Checks, player),lambda state:state._kh_hb_unlocked(player) and state._kh_first_half_cor(player,2))
            add_rule(world.get_entrance(all_locations.SecondHalf_Checks,player),lambda state:state._kh_hb_unlocked(player) and state._kh_first_half_cor(player,2) and state._kh_second_half_cor(player,3))
            add_rule(world.get_entrance(all_locations.HB2_Checks,player),lambda state:state._kh_hb_unlocked(player))
            add_rule(world.get_entrance(all_locations.PR2_Checks,player),lambda state:state._kh_pr_unlocked(player))
            add_rule(world.get_entrance(all_locations.SP2_Checks,player),lambda state:state._kh_sp_unlocked(player))
            add_rule(world.get_entrance(all_locations.BC2_Checks,player),lambda state:state._kh_bc_unlocked(player))
            add_rule(world.get_entrance(all_locations.OC2_Checks,player),lambda state:state._kh_oc_unlocked(player))
            add_rule(world.get_entrance(all_locations.ShitCups,player),lambda state:state._kh_oc_unlocked(player))
            add_rule(world.get_entrance(all_locations.BetterCups,player),lambda state:state._kh_oc_unlocked(player))
            add_rule(world.get_entrance(all_locations.HundredAcre1_Checks,player),lambda state:state._kh_oc_unlocked(player))
            #add_rule(world.get_entrance(all_locations.AG2_Checks,player),lambda state:state._kh_ag_unlocked(player,1))
        
            if Visitlocking.value==3:
               add_rule(world.get_entrance(all_locations.LoD_Checks, player),lambda state:state._kh_lod_unlocked(player))
               add_rule(world.get_entrance(all_locations.TWTNW_Checks,player),lambda state:state._kh_twtnw_unlocked(player))
               add_rule(world.get_entrance(all_locations.TT_Checks,player),lambda state:state._kh_tt2_unlocked(player))
               add_rule(world.get_entrance(all_locations.PL_Checks,player),lambda state:state._kh_pl_unlocked(player))
               add_rule(world.get_entrance(all_locations.HB_Checks,player),lambda state:state._kh_hb_unlocked(player))
               add_rule(world.get_entrance(all_locations.PR_Checks,player),lambda state:state._kh_pr_unlocked(player))
               add_rule(world.get_entrance(all_locations.SP_Checks,player),lambda state:state._kh_sp_unlocked(player))
               add_rule(world.get_entrance(all_locations.BC_Checks,player),lambda state:state._kh_bc_unlocked(player))
               add_rule(world.get_entrance(all_locations.OC_Checks,player),lambda state:state._kh_oc_unlocked(player))
               add_rule(world.get_entrance(all_locations.AG_Checks,player),lambda state:state._kh_ag_unlocked(player))

    
            

