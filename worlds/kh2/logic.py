from ..AutoWorld import LogicMixin
from .Names import LocationName,ItemName
class KH2Logic(LogicMixin):

    #def kh_FormLevel_Unlocked(self,player,amount):
    #    count: int = self.item_count("Valor Form", player) + self.item_count("Wisdom Form", player)+ self.item_count("Master Form", player)+ \
    #        self.item_count("Limit Form", player)+ self.item_count("Final Form", player)
    #    if(count!=0):
    #       print("yas")
    #    return count >= amount
       


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
    #Movement logic for cor
    def kh_first_half_cor(self,player):
        return self.has('Quick Run',player,2) and self.has('Aerial Dodge',player,2)
    def kh_second_half_cor(self,player):
        return self.has('High Jump',player,3) and self.has('Aerial Dodge',player,3) and self.has('Glide',player,3)
    def kh_lod_unlocked(self,player):
            return self.has('Sword of the Ancestor',player)
    def kh_oc_unlocked(self,player):
        return self.has('Battlefields of War',player)
    def kh_twtnw_unlocked(self,player):
        return self.has('Way to the Dawn',player)or self.has('Quick Run',player,1)
    def kh_ht_unlocked(self,player):
        return self.has('Bone Fist',player)
    def kh_tt_unlocked(self,player):
       return (((self.has('Poster',player))))
    def kh_tt2_unlocked(self,player):
        return self.has('Ice Cream',player)
    def kh_tt3_unlocked(self,player):
        return self.has('Picture',player) and self.has('Ice Cream',player)
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
        #RE SPELL THESE
        return self.has('Scimitar',player)and self.has('fire element',player,1)and self.has('blizzard element',player,1)and self.has('thunder element',1)
    def kh_bc_unlocked(self,player):
        return self.has("Beast's Claw",player)
    def kh_FormLevel_Unlocked(self,player,amount):
        level = 0
        for form in {ItemName.ValorForm,ItemName.WisdomForm,ItemName.LimitForm,ItemName.MasterForm,ItemName.FinalForm}:
          if self.has(form, player):
            level += 1
        if(level!=0):
             print("yas")
        return level>=amount
    def kh_FinalFights_Unlocked(self,player):
        return self.has('Proof of Connection',player,1)and self.has('Proof of Nonexistence',player,1)and self.has('Proof of Peace',player,1)