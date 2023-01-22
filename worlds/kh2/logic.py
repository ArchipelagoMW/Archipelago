from ..AutoWorld import LogicMixin
from .Names import ItemName


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

    def kh_lod_unlocked(self, player):
        return self.has(ItemName.SwordoftheAncestor, player)

    def kh_oc_unlocked(self, player):
        return self.has(ItemName.BattlefieldsofWar, player)

    def kh_twtnw_unlocked(self, player):
        return self.has(ItemName.WaytotheDawn, player)

    def kh_ht_unlocked(self, player):
        return self.has(ItemName.BoneFist, player)

    def kh_tt_unlocked(self, player):
        return self.has(ItemName.Poster, player)

    def kh_tt2_unlocked(self, player):
        return self.has(ItemName.Picture, player)

    def kh_tt3_unlocked(self, player):
        return self.has(ItemName.IceCream, player)

    def kh_pr_unlocked(self, player):
        return self.has(ItemName.SkillandCrossbones, player)

    def kh_sp_unlocked(self, player):
        return self.has(ItemName.IdentityDisk, player)

    def kh_stt_unlocked(self, player: int):
        return self.has(ItemName.NamineSketches, player)

    # Using Dummy 13 for this
    def kh_dc_unlocked(self, player: int):
        return self.has(ItemName.CastleKey, player)

    def kh_hb_unlocked(self, player):
        return self.has(ItemName.MembershipCard, player)

    def kh_pl_unlocked(self, player):
        return self.has(ItemName.ProudFang, player)

    def kh_ag_unlocked(self, player):
        return self.has(ItemName.Scimitar, player)

    #def kh_ag_unlocked(self, player: int):
    #    return self.has('Scimitar', player)

    def kh_bc_unlocked(self, player):
        return self.has(ItemName.BeastsClaw, player)

    # Movement logic for cor
    #def kh_HighJump_level(self, player, amount):
    #    level = 0
    #    for highjump in {ItemName.HighJump, ItemName.HighJump2, ItemName.HighJump3, ItemName.HighJump4}:
    #        if self.has(highjump, player):
    #            level += 1
    #    return level >= amount
    #
    #def kh_QuickRun_level(self, player, amount):
    #    level = 0
    #    for quickrun in {ItemName.QuickRun, ItemName.QuickRun2, ItemName.QuickRun3, ItemName.QuickRun4}:
    #        if self.has(quickrun, player):
    #            level += 1
    #    return level >= amount
    #
    #def kh_DodgeRoll_level(self, player, amount):
    #    level = 0
    #    for dgeroll in {ItemName.DodgeRoll, ItemName.DodgeRol2, ItemName.DodgeRol3, ItemName.DodgeRol4}:
    #        if self.has(dgeroll, player):
    #            level += 1
    #    return level >= amount
    #
    #def kh_AerialDodge_level(self, player, amount):
    #    level = 0
    #    for aerialdge in {ItemName.AerialDodge, ItemName.AerialDodge2, ItemName.AerialDodge3, ItemName.AerialDodge4}:
    #        if self.has(aerialdge, player):
    #            level += 1
    #    return level >= amount
    #
    #def kh_Glide_level(self, player, amount):
    #    level = 0
    #    for glide in {ItemName.Glide, ItemName.Glide2, ItemName.Glide3, ItemName.Glide4}:
    #        if self.has(glide, player):
    #            level += 1
        return level >= amount

    def kh_FormLevel_unlocked(self, player, amount):
        level = 0
        for form in {ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                     ItemName.FinalForm}:
            if self.has(form, player):
                level += 1
        return level >= amount

    def kh_FinalFights_unlocked(self, player):
        return self.has(ItemName.ProofofConnection, player, 1) and self.has(ItemName.ProofofNonexistence, player, 1) and self.has(
            ItemName.ProofofPeace, player, 1)

    def kh_Vicotry(self, player):
        return self.has('Victory', player, 1)
