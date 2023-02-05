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

    # def kh_ag_unlocked(self, player: int):
    #    return self.has('Scimitar', player)

    def kh_bc_unlocked(self, player):
        return self.has(ItemName.BeastsClaw, player)

    def kh_form_level_unlocked(self, player, amount):
        level = 0
        for form in {ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                     ItemName.FinalForm}:
            if self.has(form, player):
                level += 1
        return level >= amount

    def kh_visit_locking_amount(self, player, amount):
        level = 0
        # torn pages are not added since you cannot get exp from that world
        for item in {ItemName.CastleKey, ItemName.BattlefieldsofWar, ItemName.SwordoftheAncestor, ItemName.BeastsClaw,
                     ItemName.BoneFist, ItemName.ProudFang, ItemName.SkillandCrossbones, ItemName.Scimitar,
                     ItemName.MembershipCard,
                     ItemName.IceCream, ItemName.Picture, ItemName.WaytotheDawn, ItemName.IdentityDisk,
                     ItemName.Poster}:
            if self.has(item, player):
                level += 1
        return level >= amount

    def kh_three_proof_unlocked(self, player):
        return self.has(ItemName.ProofofConnection, player, 1) \
            and self.has(ItemName.ProofofNonexistence, player,1)\
            and self.has(ItemName.ProofofPeace,player, 1)
    def kh_all_blue_numbers_unlocked(self, player):
        return self.has(ItemName.ProofofConnection, player, 1) \
            and self.has(ItemName.ProofofNonexistence, player, 1) \
            and self.has(ItemName.ProofofPeace, player, 1) \
            and self.has(ItemName.FireElement, player, 3) \
            and self.has(ItemName.BlizzardElement, player, 3) \
            and self.has(ItemName.ThunderElement, player, 3) \
            and self.has(ItemName.ReflectElement, player, 3) \
            and self.has(ItemName.MagnetElement, player, 3) \
            and self.has(ItemName.CureElement, player, 3) \
            and self.has(ItemName.FinalForm, player, 1) \
            and self.has(ItemName.LimitForm, player, 1) \
            and self.has(ItemName.MasterForm, player, 1) \
            and self.has(ItemName.ValorForm, player, 1) \
            and self.has(ItemName.WisdomForm, player, 1) \
            and self.has(ItemName.ChickenLittle, player, 1) \
            and self.has(ItemName.Stitch, player, 1) \
            and self.has(ItemName.Genie, player, 1) \
            and self.has(ItemName.PeterPan, player, 1) \
            and self.has(ItemName.OnceMore, player, 1) \
            and self.has(ItemName.SecondChance, player, 1) \
            and self.has(ItemName.TornPages, player, 5) \
            and self.has(ItemName.SecondChance, player, 1)\
            and self.has(ItemName.SecretAnsemsReport1,player,1)\
            and self.has(ItemName.SecretAnsemsReport2,player,1)\
            and self.has(ItemName.SecretAnsemsReport3,player,1)\
            and self.has(ItemName.SecretAnsemsReport4,player,1)\
            and self.has(ItemName.SecretAnsemsReport5,player,1)\
            and self.has(ItemName.SecretAnsemsReport6,player,1)\
            and self.has(ItemName.SecretAnsemsReport7,player,1)\
            and self.has(ItemName.SecretAnsemsReport8,player,1)\
            and self.has(ItemName.SecretAnsemsReport9,player,1)\
            and self.has(ItemName.SecretAnsemsReport10,player,1)\
            and self.has(ItemName.SecretAnsemsReport11,player,1)\
            and self.has(ItemName.SecretAnsemsReport12,player,1)\
            and self.has(ItemName.SecretAnsemsReport13,player,1)

    def kh_lucky_emblem_unlocked(self,player,amount):
        return self.has(ItemName.LuckyEmblem, player, amount)

    def kh_victory(self, player):
        return self.has('Victory', player, 1)
