from ..AutoWorld import LogicMixin
class KH2Logic(LogicMixin):
    #piglets house
    def _kh_torn_page_1(self, player: int):
        return self.has('Torn Page', player, 1)
    #rabbits
    def _kh_torn_page_2(self, player: int):
        return self.has('Torn Page', player, 2)
    #kangroo's house
    def _kh_torn_page_3(self, player: int):
        return self.has('Torn Page', player, 3)
    #spooky cave
    def _kh_torn_page_4(self, player: int):
        return self.has('Torn Page', player, 4)
    #Stary Hill
    def _kh_torn_page_5(self, player: int):
        return self.has('Torn Page', player, 5)
    #Movement logic for cor
    def _kh_first_half_cor(self,player):
        return self.has('Quick Run',player,2) and ('Aerial Dodge ',player,2)
    def _kh_second_half_cor(self,player):
        return self.has('High Jump',player,3) and ('Aerial Dodge ',player,3) and ('Glide',player,3)
    def _kh_lod_unlocked(self,player):
            return self.has('Sword of the Ancestor',player)
    def _kh_oc_unlocked(self,player):
        return self.has('Battlefields of War',player)
    def _kh_twtnw_unlocked(self,player):
        return self.has('Way to the Dawn',player)or('Quick Run',player,1)
    def _kh_ht_unlocked(self,player):
        return self.has('Bone Fist',player)
    def _kh_tt_unlocked(self,player:int):
       return self.has('Poster',player)
    def _kh_tt2_unlocked(self,player):
        return self.has('Ice Cream',player)
    def _kh_tt3_unlocked(self,player):
        return self.has('Picture',player) and self.has('Ice Cream',player)
    def _kh_pr_unlocked(self,player):
        return self.has('Skill and Crossbones',player)
    def _kh_sp_unlocked(self,player):
        return self.has('Idenity Disk',player)
    def _kh_stt_unlocked(self,player:int):
         return self.has('Namine Sketches',player)
    #Using Dummy 13 for this
    def _kh_dc_unlocked(self,player:int):
        return self.has('Disney Castle Key',player)
    def _kh_hb_unlocked(self,player):
        return self.has('Membership Card',player)
    def _kh_pl_unlocked(self,player):
        return self.has('Proud Fang',player)
    def _kh_ag_unlocked(self,player):
        return self.has('Scimitar',player)
    def _kh_ag_unlocked(self,player:int):
        return self.has('Scimitar',player)and ('fire element',player,1)and('blizzard element',player,1)and('thunder element',1)
    def _kh_bc_unlocked(self,player):
        return self.has("Beast's Claw",player)
    def _kh_FinalFights_Unlocked(self,player):
            return self.has('Proof of Connection',player,1)and('Proof of Nonexistence',player,1)and('Proof of Peace',player,1)
    