from .Names import ItemName
from ..AutoWorld import LogicMixin


class KH2Logic(LogicMixin):
    def kh_lod_unlocked(self, player, amount):
        return self.has(ItemName.SwordoftheAncestor, player, amount)

    def kh_oc_unlocked(self, player, amount):
        return self.has(ItemName.BattlefieldsofWar, player, amount)

    def kh_twtnw_unlocked(self, player, amount):
        return self.has(ItemName.WaytotheDawn, player, amount)

    def kh_ht_unlocked(self, player, amount):
        return self.has(ItemName.BoneFist, player, amount)

    def kh_tt_unlocked(self, player, amount):
        return self.has(ItemName.IceCream, player, amount)

    def kh_pr_unlocked(self, player, amount):
        return self.has(ItemName.SkillandCrossbones, player, amount)

    def kh_sp_unlocked(self, player, amount):
        return self.has(ItemName.IdentityDisk, player, amount)

    def kh_stt_unlocked(self, player: int, amount):
        return self.has(ItemName.NamineSketches, player, amount)

    # Using Dummy 13 for this
    def kh_dc_unlocked(self, player: int, amount):
        return self.has(ItemName.CastleKey, player, amount)

    def kh_hb_unlocked(self, player, amount):
        return self.has(ItemName.MembershipCard, player, amount)

    def kh_pl_unlocked(self, player, amount):
        return self.has(ItemName.ProudFang, player, amount)

    def kh_ag_unlocked(self, player, amount):
        return self.has(ItemName.Scimitar, player, amount)

    def kh_bc_unlocked(self, player, amount):
        return self.has(ItemName.BeastsClaw, player, amount)

    def kh_amount_of_forms(self, player, amount, requiredform="None"):
        level = 0
        formList = [ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                    ItemName.FinalForm]
        #  required form is in the logic for region connections
        if requiredform != "None":
            formList.remove(requiredform)
        for form in formList:
            if self.has(form, player):
                level += 1
        return level >= amount

    def kh_visit_locking_amount(self, player, amount):
        visit = 0
        # torn pages are not added since you cannot get exp from that world
        for item in {ItemName.CastleKey, ItemName.BattlefieldsofWar, ItemName.SwordoftheAncestor, ItemName.BeastsClaw,
                     ItemName.BoneFist, ItemName.ProudFang, ItemName.SkillandCrossbones, ItemName.Scimitar,
                     ItemName.MembershipCard,
                     ItemName.IceCream, ItemName.WaytotheDawn,
                     ItemName.IdentityDisk, ItemName.NamineSketches}:
            visit += self.item_count(item, player)
        return visit >= amount

    def kh_three_proof_unlocked(self, player):
        return self.has(ItemName.ProofofConnection, player, 1) \
            and self.has(ItemName.ProofofNonexistence, player, 1) \
            and self.has(ItemName.ProofofPeace, player, 1)

    def kh_hitlist(self, player, amount):
        return self.has(ItemName.Bounty, player, amount)

    def kh_lucky_emblem_unlocked(self, player, amount):
        return self.has(ItemName.LuckyEmblem, player, amount)

    def kh_victory(self, player):
        return self.has(ItemName.Victory, player, 1)

    def kh_summon(self, player, amount):
        summonlevel = 0
        for summon in {ItemName.Genie, ItemName.ChickenLittle, ItemName.Stitch, ItemName.PeterPan}:
            if self.has(summon, player):
                summonlevel += 1
        return summonlevel >= amount

    # magic progression
    def kh_fire(self, player):
        return self.has(ItemName.FireElement, player, 1)

    def kh_fira(self, player):
        return self.has(ItemName.FireElement, player, 2)

    def kh_firaga(self, player):
        return self.has(ItemName.FireElement, player, 3)

    def kh_blizzard(self, player):
        return self.has(ItemName.BlizzardElement, player, 1)

    def kh_blizzara(self, player):
        return self.has(ItemName.BlizzardElement, player, 2)

    def kh_blizzaga(self, player):
        return self.has(ItemName.BlizzardElement, player, 3)

    def kh_thunder(self, player):
        return self.has(ItemName.ThunderElement, player, 1)

    def kh_thundara(self, player):
        return self.has(ItemName.ThunderElement, player, 2)

    def kh_thundaga(self, player):
        return self.has(ItemName.ThunderElement, player, 3)

    def kh_magnet(self, player):
        return self.has(ItemName.MagnetElement, player, 1)

    def kh_magnera(self, player):
        return self.has(ItemName.MagnetElement, player, 2)

    def kh_magnega(self, player):
        return self.has(ItemName.MagnetElement, player, 3)

    def kh_reflect(self, player):
        return self.has(ItemName.ReflectElement, player, 1)

    def kh_reflera(self, player):
        return self.has(ItemName.ReflectElement, player, 2)

    def kh_reflega(self, player):
        return self.has(ItemName.ReflectElement, player, 3)

    def kh_highjump(self, player, amount):
        return self.has(ItemName.HighJump, player, amount)

    def kh_quickrun(self, player, amount):
        return self.has(ItemName.QuickRun, player, amount)

    def kh_dodgeroll(self, player, amount):
        return self.has(ItemName.DodgeRoll, player, amount)

    def kh_aerialdodge(self, player, amount):
        return self.has(ItemName.AerialDodge, player, amount)

    def kh_glide(self, player, amount):
        return self.has(ItemName.Glide, player, amount)

    def kh_comboplus(self, player, amount):
        return self.has(ItemName.ComboPlus, player, amount)

    def kh_aircomboplus(self, player, amount):
        return self.has(ItemName.AirComboPlus, player, amount)

    def kh_valorgenie(self, player):
        return self.has(ItemName.Genie, player) and self.has(ItemName.ValorForm, player)

    def kh_wisdomgenie(self, player):
        return self.has(ItemName.Genie, player) and self.has(ItemName.WisdomForm, player)

    def kh_mastergenie(self, player):
        return self.has(ItemName.Genie, player) and self.has(ItemName.MasterForm, player)

    def kh_finalgenie(self, player):
        return self.has(ItemName.Genie, player) and self.has(ItemName.FinalForm, player)

    def kh_rsr(self, player):
        return self.has(ItemName.Slapshot, player, 1) and self.has(ItemName.ComboMaster, player) and self.kh_reflect(
            player)

    def kh_gapcloser(self, player):
        return self.has(ItemName.FlashStep, player, 1) or self.has(ItemName.SlideDash, player)

    #  Crowd Control and Berserk Hori will be used when I add hard logic.

    def kh_crowdcontrol(self, player):
        return self.kh_magnera(player) and self.has(ItemName.ChickenLittle, player) \
            or self.kh_magnega(player) and self.kh_mastergenie(player)

    def kh_berserkhori(self, player):
        return self.has(ItemName.HorizontalSlash, player, 1) and self.has(ItemName.BerserkCharge, player)

    def kh_donaldlimit(self, player):
        return self.has(ItemName.FlareForce, player, 1) or self.has(ItemName.Fantasia, player)

    def kh_goofylimit(self, player):
        return self.has(ItemName.TornadoFusion, player, 1) or self.has(ItemName.Teamwork, player)

    def kh_basetools(self, player):
        # TODO: if option is easy then add reflect,gap closer and second chance&once more. #option east scom option normal adds gap closer or combo master #hard is what is right now
        return self.has(ItemName.Guard, player, 1) and self.has(ItemName.AerialRecovery, player, 1) \
            and self.has(ItemName.FinishingPlus, player, 1)

    def kh_roxastools(self, player):
        return self.kh_basetools(player) and (
                    self.has(ItemName.QuickRun, player) or self.has(ItemName.NegativeCombo, player, 2))

    def kh_painandpanic(self, player):
        return (self.kh_goofylimit(player) or self.kh_donaldlimit(player)) and self.kh_dc_unlocked(player, 2)

    def kh_cerberuscup(self, player):
        return self.kh_amount_of_forms(player, 2) and self.kh_thundara(player) \
            and self.kh_ag_unlocked(player, 1) and self.kh_ht_unlocked(player, 1) \
            and self.kh_pl_unlocked(player, 1)

    def kh_titan(self, player: int):
        return self.kh_summon(player, 2) and (self.kh_thundara(player) or self.kh_magnera(player)) \
            and self.kh_oc_unlocked(player, 2)

    def kh_gof(self, player):
        return self.kh_titan(player) and self.kh_cerberuscup(player) \
            and self.kh_painandpanic(player) and self.kh_twtnw_unlocked(player, 1)

    def kh_dataroxas(self, player):
        return self.kh_basetools(player) and \
            ((self.has(ItemName.LimitForm, player) and self.kh_amount_of_forms(player, 3) and self.has(
                ItemName.TrinityLimit, player) and self.kh_gapcloser(player))
             or (self.has(ItemName.NegativeCombo, player, 2) or self.kh_quickrun(player, 2)))

    def kh_datamarluxia(self, player):
        return self.kh_basetools(player) and self.kh_reflera(player) \
            and ((self.kh_amount_of_forms(player, 3) and self.has(ItemName.FinalForm, player) and self.kh_fira(
                player)) or self.has(ItemName.NegativeCombo, player, 2) or self.kh_donaldlimit(player))

    def kh_datademyx(self, player):
        return self.kh_basetools(player) and self.kh_amount_of_forms(player, 5) and self.kh_firaga(player) \
            and (self.kh_donaldlimit(player) or self.kh_blizzard(player))

    def kh_datalexaeus(self, player):
        return self.kh_basetools(player) and self.kh_amount_of_forms(player, 3) and self.kh_reflera(player) \
            and (self.has(ItemName.NegativeCombo, player, 2) or self.kh_donaldlimit(player))

    def kh_datasaix(self, player):
        return self.kh_basetools(player) and (self.kh_thunder(player) or self.kh_blizzard(player)) \
            and self.kh_highjump(player, 2) and self.kh_aerialdodge(player, 2) and self.kh_glide(player, 2) and self.kh_amount_of_forms(player, 3) \
            and (self.kh_rsr(player) or self.has(ItemName.NegativeCombo, player, 2) or self.has(ItemName.PeterPan,
                                                                                                player))

    def kh_dataxaldin(self, player):
        return self.kh_basetools(player) and self.kh_donaldlimit(player) and self.kh_goofylimit(player) \
            and self.kh_highjump(player, 2) and self.kh_aerialdodge(player, 2) and self.kh_glide(player,
                                                                                                 2) and self.kh_magnet(
                player)
        # and (self.kh_form_level_unlocked(player, 3) or self.kh_berserkhori(player))

    def kh_dataxemnas(self, player):
        return self.kh_basetools(player) and self.kh_rsr(player) and self.kh_gapcloser(player) \
            and (self.has(ItemName.LimitForm, player) or self.has(ItemName.TrinityLimit, player))

    def kh_dataxigbar(self, player):
        return self.kh_basetools(player) and self.kh_donaldlimit(player) and self.has(ItemName.FinalForm, player) \
            and self.kh_amount_of_forms(player, 3) and self.kh_reflera(player)

    def kh_datavexen(self, player):
        return self.kh_basetools(player) and self.kh_donaldlimit(player) and self.has(ItemName.FinalForm, player) \
            and self.kh_amount_of_forms(player, 4) and self.kh_reflera(player) and self.kh_fira(player)

    def kh_datazexion(self, player):
        return self.kh_basetools(player) and self.kh_donaldlimit(player) and self.has(ItemName.FinalForm, player) \
            and self.kh_amount_of_forms(player, 3) \
            and self.kh_reflera(player) and self.kh_fira(player)

    def kh_dataaxel(self, player):
        return self.kh_basetools(player) \
            and ((self.kh_reflera(player) and self.kh_blizzara(player)) or self.has(ItemName.NegativeCombo, player, 2))

    def kh_dataluxord(self, player):
        return self.kh_basetools(player) and self.kh_reflect(player)

    def kh_datalarxene(self, player):
        return self.kh_basetools(player) and self.kh_reflera(player) \
            and ((self.has(ItemName.FinalForm, player) and self.kh_amount_of_forms(player, 4) and self.kh_fire(
                player))
                 or (self.kh_donaldlimit(player) and self.kh_amount_of_forms(player, 2)))

    def kh_sephi(self, player):
        return self.kh_dataxemnas(player)

    def kh_onek(self, player):
        return self.kh_reflect(player) or self.has(ItemName.Guard, player)

    def kh_terra(self, player):
        return self.has(ItemName.ProofofConnection, player) and self.kh_basetools(player) \
            and self.kh_dodgeroll(player, 2) and self.kh_aerialdodge(player, 2) and self.kh_glide(player, 3) \
            and ((self.kh_comboplus(player, 2) and self.has(ItemName.Explosion, player)) or self.has(
                ItemName.NegativeCombo, player, 2))

    def kh_cor(self, player):
        return self.kh_reflect(player) \
            and self.kh_highjump(player, 2) and self.kh_quickrun(player, 2) and self.kh_aerialdodge(player, 2) \
            and (self.has(ItemName.MasterForm, player) and self.kh_fire(player)
                 or (self.has(ItemName.ChickenLittle, player) and self.kh_donaldlimit(player) and self.kh_glide(player,
                                                                                                                2)))

    def kh_transport(self, player):
        return self.kh_basetools(player) and self.kh_reflera(player) \
            and ((self.kh_mastergenie(player) and self.kh_magnera(player) and self.kh_donaldlimit(player))
                 or (self.has(ItemName.FinalForm, player) and self.kh_amount_of_forms(player, 4) and self.kh_fira(
                        player)))

    def kh_gr2(self, player):
        return (self.has(ItemName.MasterForm, player) or self.has(ItemName.Stitch, player)) \
            and (self.kh_fire(player) or self.kh_blizzard(player) or self.kh_thunder(player))

    def kh_xaldin(self, player):
        return self.kh_basetools(player) and (self.kh_donaldlimit(player) or self.kh_amount_of_forms(player, 1))

    def kh_mcp(self, player):
        return self.kh_reflect(player) and (
                    self.has(ItemName.MasterForm, player) or self.has(ItemName.FinalForm, player))
