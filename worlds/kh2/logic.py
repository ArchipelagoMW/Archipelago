from .Names import ItemName
from ..AutoWorld import LogicMixin


class KH2Logic(LogicMixin):
    # piglets house
    def kh_torn_page_1(self, player: int):
        return self.has(ItemName.TornPages, player, 1)

    # rabbits
    def kh_torn_page_2(self, player: int):
        return self.has(ItemName.TornPages, player, 2)

    # kangaroo's house
    def kh_torn_page_3(self, player: int):
        return self.has(ItemName.TornPages, player, 3)

    # spooky cave
    def kh_torn_page_4(self, player: int):
        return self.has(ItemName.TornPages, player, 4)

    # Stary Hill
    def kh_torn_page_5(self, player: int):
        return self.has(ItemName.TornPages, player, 5)

    def kh_lod_unlocked(self, player,amount):
        return self.has(ItemName.SwordoftheAncestor, player,amount)

    def kh_oc_unlocked(self, player,amount):
        return self.has(ItemName.BattlefieldsofWar, player,amount)

    def kh_twtnw_unlocked(self, player,amount):
        return self.has(ItemName.WaytotheDawn, player,amount)

    def kh_ht_unlocked(self, player,amount):
        return self.has(ItemName.BoneFist, player,amount)

    def kh_tt_unlocked(self, player,amount):
        return self.has(ItemName.Poster, player,amount)

    def kh_tt2_unlocked(self, player,amount):
        return self.has(ItemName.Picture, player,amount)

    def kh_tt3_unlocked(self, player,amount):
        return self.has(ItemName.IceCream, player,amount)

    def kh_pr_unlocked(self, player,amount):
        return self.has(ItemName.SkillandCrossbones, player,amount)

    def kh_sp_unlocked(self, player,amount):
        return self.has(ItemName.IdentityDisk, player,amount)

    def kh_stt_unlocked(self, player: int,amount):
        return self.has(ItemName.NamineSketches, player,amount)

    # Using Dummy 13 for this
    def kh_dc_unlocked(self, player: int,amount):
        return self.has(ItemName.CastleKey, player,amount)

    def kh_hb_unlocked(self, player,amount):
        return self.has(ItemName.MembershipCard, player,amount)

    def kh_pl_unlocked(self, player,amount):
        return self.has(ItemName.ProudFang, player,amount)

    def kh_ag_unlocked(self, player,amount):
        return self.has(ItemName.Scimitar, player,amount)

    # def kh_ag_unlocked(self, player: int):
    #    return self.has('Scimitar', player)

    def kh_bc_unlocked(self, player,amount):
        return self.has(ItemName.BeastsClaw, player,amount)

    def kh_form_level_unlocked(self, player, amount):
        level = 0
        for form in {ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                     ItemName.FinalForm}:
            if self.has(form, player):
                level += 1
        return level >= amount

    def kh_visit_locking_amount(self, player, amount):
        visit = 0
        # torn pages are not added since you cannot get exp from that world
        for item in {ItemName.CastleKey, ItemName.BattlefieldsofWar, ItemName.SwordoftheAncestor, ItemName.BeastsClaw,
                     ItemName.BoneFist, ItemName.ProudFang, ItemName.SkillandCrossbones, ItemName.Scimitar,
                     ItemName.MembershipCard,
                     ItemName.IceCream, ItemName.Picture, ItemName.WaytotheDawn, ItemName.IdentityDisk,
                     ItemName.Poster}:
            if self.has(item, player):
                visit += 1
        return visit >= amount

    def kh_three_proof_unlocked(self, player):
        return self.has(ItemName.ProofofConnection, player, 1) \
            and self.has(ItemName.ProofofNonexistence, player,1)\
            and self.has(ItemName.ProofofPeace,player, 1)
    def kh_hitlist(self,player,amount):
        return self.has(ItemName.Bounty, player,amount)

    def kh_lucky_emblem_unlocked(self,player,amount):
        return self.has(ItemName.LuckyEmblem, player, amount)

    def kh_victory(self, player):
        return self.has('Victory', player, 1)
