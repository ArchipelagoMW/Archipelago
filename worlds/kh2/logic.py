from ..AutoWorld import LogicMixin
from .Names import LocationName,ItemName
class KH2Logic(LogicMixin):
    #piglets house
    def kh_torn_page_1(self, player: int):
        return self.has('Torn Page', player, 1)
    #rabbits
    def kh_torn_page_2(self, player: int):
        return self.has('Torn Page', player, 2)
    #kangaroo's house
    def kh_torn_page_3(self, player: int):
        return self.has('Torn Page', player, 3)
    #spooky cave
    def kh_torn_page_4(self, player: int):
        return self.has('Torn Page', player, 4)
    #Stary Hill
    def kh_torn_page_5(self, player: int):
        return self.has('Torn Page', player, 5)
<<<<<<< HEAD
    
=======
    #Movement logic for cor
    def kh_first_half_cor(self,player):
        return self.has('Quick Run',player,2) and self.has('Aerial Dodge',player,2)
    def kh_second_half_cor(self,player):
        return self.has('High Jump',player,3) and self.has('Aerial Dodge',player,3) and self.has('Glide',player,3)
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
    def kh_lod_unlocked(self,player):
            return self.has('Sword of the Ancestor',player)
    def kh_oc_unlocked(self,player):
        return self.has('Battlefields of War',player)
    def kh_twtnw_unlocked(self,player):
<<<<<<< HEAD
        return self.has('Quick Run',player,1)
    def kh_twtnw_unlocked(self,player):
        return self.has('Final Form',player)and self.kh_QuickRun_level(player,2)
=======
        return self.has('Way to the Dawn',player)and self.has('Quick Run',player,1)
    def kh_twtnw_unlocked(self,player):
        return self.has('Final Form',player)and self.has('Quick Run',player,2)
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
    def kh_ht_unlocked(self,player):
        return self.has('Bone Fist',player)
    def kh_tt_unlocked(self,player):
       return (((self.has('Poster',player))))
    def kh_tt2_unlocked(self,player):
        return self.has('Ice Cream',player)
    def kh_tt3_unlocked(self,player):
        return self.has('Picture',player)
    def kh_pr_unlocked(self,player):
        return self.has('Skill and Crossbones',player)
    def kh_sp_unlocked(self,player):
        return self.has('Idenity Disk',player)
    def kh_stt_unlocked(self,player:int):
         return self.has('Namine Sketches',player)
    #Using Dummy 13 for this
    def kh_dc_unlocked(self,player:int):
        return self.has('Disney Castle Key',player)
    def kh_hb_unlocked(self,player):
        return self.has('Membership Card',player)
    def kh_pl_unlocked(self,player):
        return self.has('Proud Fang',player)
    def kh_ag_unlocked(self,player):
        return self.has('Scimitar',player)
    def kh_ag_unlocked(self,player:int):
        return self.has('Scimitar',player)
    def kh_bc_unlocked(self,player):
        return self.has("Beast's Claw",player)
<<<<<<< HEAD
    #Movement logic for cor
    def kh_HighJump_level(self,player,amount):
        level = 0
        for highjump in {ItemName.HighJump,ItemName.HighJump2,ItemName.HighJump3,ItemName.HighJump4}:
          if self.has(highjump, player):
            level += 1
        return level>=amount
    def kh_QuickRun_level(self,player,amount):
        level = 0
        for quickrun in {ItemName.QuickRun,ItemName.QuickRun2,ItemName.QuickRun3,ItemName.QuickRun4}:
          if self.has(quickrun, player):
            level += 1
        return level>=amount
    def kh_DodgeRoll_level(self,player,amount):
        level = 0
        for dgeroll in {ItemName.DodgeRoll,ItemName.DodgeRol2,ItemName.DodgeRol3,ItemName.DodgeRol4}:
          if self.has(dgeroll, player):
            level += 1
        return level>=amount
    def kh_AerialDodge_level(self,player,amount):
        level = 0
        for aerialdge in {ItemName.AerialDodge,ItemName.AerialDodge2,ItemName.AerialDodge3,ItemName.AerialDodge4}:
          if self.has(aerialdge, player):
            level += 1
        return level>=amount
    def kh_Glide_level(self,player,amount):
        level = 0
        for glide in {ItemName.Glide,ItemName.Glide2,ItemName.Glide3,ItemName.Glide4}:
          if self.has(glide, player):
            level += 1
        return level>=amount
    
    def kh_FormLevel_unlocked(self,player,amount):
=======
    def kh_FormLevel_Unlocked(self,player,amount):
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        level = 0
        for form in {ItemName.ValorForm,ItemName.WisdomForm,ItemName.LimitForm,ItemName.MasterForm,ItemName.FinalForm}:
          if self.has(form, player):
            level += 1
        return level>=amount
<<<<<<< HEAD
    def kh_FinalFights_unlocked(self,player):
=======
    def kh_FinalFights_Unlocked(self,player):
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        return self.has('Proof of Connection',player,1)and self.has('Proof of Nonexistence',player,1)and self.has('Proof of Peace',player,1)