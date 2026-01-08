from ..event.event import *

class Airship(Event):
    def name(self):
        return "Airship"

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.LEARNED_TO_FLY_AIRSHIP),
            field.SetEventBit(event_bit.AIRSHIP_VISIBLE),
            field.SetEventBit(event_bit.AIRSHIP_FLYING),

            field.ClearEventBit(npc_bit.SETZER_BLACKJACK_COIN_TOSS),
            field.ClearEventBit(npc_bit.DARILL_FALCON_DECK),
        )

    def mod(self):
        self.controls_mod()
        self.unequip_party_members_npc_mod()
        self.inside_blackjack()
        self.return_to_airship()
        self.fix_fly_offscreen_bug()

    def controls_mod(self):
        fly_wor_fc_cancel_dialog = 1315
        fly_wor_cancel_dialog = 1318
        fly_wob_dg_cancel_dialog = 1293
        fly_wob_cancel_dialog = 1319

        self.dialogs.set_text(fly_wor_fc_cancel_dialog, '<choice> (Lift-off)<line><choice> (World of Ruin)<line><choice> (Floating Continent)<line><choice> (Not just yet)<end>')
        self.dialogs.set_text(fly_wor_cancel_dialog, '<choice> (Lift-off)<line><choice> (World of Ruin)<line><choice> (Not just yet)<end>')
        self.dialogs.set_text(fly_wob_dg_cancel_dialog, '<choice> (Lift-off)<line><choice> (World of Balance)<line><choice> (Search The Skies)<line><choice> (Not just yet)<end>')
        self.dialogs.set_text(fly_wob_cancel_dialog, '<choice> (Lift-off)<line><choice> (World of Balance)<line><choice> (Not just yet)<end>')

        lift_off = 0xaf58d
        enter_floating_continent = 0xa581a

        space = Allocate(Bank.CA, 298, "airship controls dialog/choices", field.NOP())

        self.enter_wor_mod(space)
        self.enter_wob_mod(space)
        self.doom_gaze_mod(space)

        fly_wor_fc_cancel_choice = space.next_address
        space.write(
            field.DialogBranch(fly_wor_fc_cancel_dialog,
                               dest1 = lift_off,
                               dest2 = self.enter_wor,
                               dest3 = enter_floating_continent,
                               dest4 = field.RETURN),
        )

        fly_wor_cancel_choice = space.next_address
        space.write(
            field.DialogBranch(fly_wor_cancel_dialog,
                               dest1 = lift_off,
                               dest2 = self.enter_wor,
                               dest3 = field.RETURN),
        )

        fly_wob_dg_cancel_choice = space.next_address
        space.write(
            field.DialogBranch(fly_wob_dg_cancel_dialog,
                               dest1 = lift_off,
                               dest2 = self.enter_wob,
                               dest3 = self.find_doom_gaze,
                               dest4 = field.RETURN),
        )

        fly_wob_cancel_choice = space.next_address
        space.write(
            field.DialogBranch(fly_wob_cancel_dialog,
                               dest1 = lift_off,
                               dest2 = self.enter_wob,
                               dest3 = field.RETURN),
        )

        # airship wor controls branching
        wor_control_checks = space.next_address
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.events["Doom Gaze"].character_gate()),
                                            fly_wob_cancel_choice),
            )
        space.write(
            field.BranchIfBattleEventBitClear(battle_bit.DEFEATED_DOOM_GAZE, fly_wob_dg_cancel_choice),
            field.Branch(fly_wob_cancel_choice),
        )

        # airship controls branching
        space = Reserve(0xaf53a, 0xaf559, "airship controls wor event bit check", field.NOP())
        space.write(
            field.BranchIfEventBitSet(event_bit.IN_WOR, wor_control_checks),
            field.BranchIfEventBitSet(event_bit.FINISHED_FLOATING_CONTINENT, fly_wor_cancel_choice),
        )
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.events["Floating Continent"].character_gate()),
                                            fly_wor_cancel_choice),
            )
        space.write(
            field.Branch(fly_wor_fc_cancel_choice),
        )

    def enter_wor_mod(self, space):
        self.enter_wor = space.next_address
        self.set_wor_bits(space)
        space.write(
            field.SetEventBit(event_bit.IN_WOR),
            field.SetEventBit(event_bit.GOT_FALCON),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.AnimateHandsUp(),
                field_entity.Pause(6),
                field_entity.Turn(direction.LEFT),
            ),
            field.ToggleWorlds(),
            vehicle.End(),
            field.Return(),
        )

    def enter_wob_mod(self, space):
        self.enter_wob = space.next_address
        self.set_wob_bits(space)
        space.write(
            field.ClearEventBit(event_bit.IN_WOR),
            field.ClearEventBit(event_bit.GOT_FALCON),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.AnimateHandsUp(),
                field_entity.Pause(6),
                field_entity.Turn(direction.LEFT),
            ),
            field.ToggleWorlds(),
            vehicle.End(),
            field.Return(),
        )

    def set_wor_bits(self, space):
        # if tentacles not defeated yet, figaro castle still underground, block doors
        #                                also hide guard and show scattered dead soldiers
        # in wob and after tentacles dead, can't be both underground and in airship
        space.write(
            field.BranchIfEventBitSet(event_bit.DEFEATED_TENTACLES_FIGARO, "DEFEATED_TENTACLES"),
            field.SetEventBit(npc_bit.BLOCK_INSIDE_DOORS_FIGARO_CASTLE),
            field.SetEventBit(npc_bit.DEAD_SOLDIERS_FIGARO_CASTLE),
            field.ClearEventBit(npc_bit.PRISON_GUARD_FIGARO_CASTLE),

            "DEFEATED_TENTACLES",
            field.ClearEventBit(npc_bit.STORES_NARSHE),
            field.SetEventBit(npc_bit.WEAPON_ELDER_NARSHE),
            field.SetEventBit(npc_bit.WEAPON_ROOM_ESPER_NARSHE),

            field.ClearEventBit(npc_bit.MOBLIZ_CITIZENS),
            field.ClearEventBit(npc_bit.MOBLIZ_SOLDIERS_LETTER),

            field.SetEventBit(event_bit.PRISON_DOOR_OPEN_FIGARO_CASTLE),
            field.ClearEventBit(npc_bit.LONE_WOLF_FIGARO_CASTLE),
            field.ClearEventBit(npc_bit.PRISONERS_FIGARO_CASTLE),

            field.SetEventBit(npc_bit.MAN_AT_COUNTER_OPERA),
            field.SetEventBit(npc_bit.IMPRESARIO_OPERA_LOBBY),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_SITTING),
            field.SetEventBit(event_bit.BEGAN_OPERA_DISRUPTION),
            field.ClearEventBit(npc_bit.ULTROS_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT1_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT2_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT3_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT4_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT5_OPERA_CEILING),
            field.ClearEventBit(npc_bit.CEILING_DOOR_OPERA_HOUSE),
            field.ClearEventBit(npc_bit.DANCING_COUPLE1_OPERA),
            field.ClearEventBit(npc_bit.DANCING_COUPLE2_OPERA),
            field.ClearEventBit(npc_bit.FIGHTING_SOLDIERS_OPERA),
            field.ClearEventBit(npc_bit.FIGHTING_SOLDIERS_OPERA_CEILING),

            field.BranchIfEventBitSet(event_bit.DEFEATED_OPERA_HOUSE_DRAGON, "WOR_BITS_END"),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_LOBBY),
            field.SetEventBit(npc_bit.IMPRESARIO_OPERA_PANICKING),
            field.SetEventBit(npc_bit.DRAGON_OPERA_HOUSE),
            "WOR_BITS_END",
        )

    def set_wob_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.STORES_NARSHE),
            field.ClearEventBit(npc_bit.WEAPON_ELDER_NARSHE),
            field.ClearEventBit(npc_bit.WEAPON_ROOM_ESPER_NARSHE),

            field.SetEventBit(npc_bit.MOBLIZ_CITIZENS),
            field.SetEventBit(npc_bit.MOBLIZ_SOLDIERS_LETTER),

            field.ClearEventBit(event_bit.PRISON_DOOR_OPEN_FIGARO_CASTLE),
            field.ClearEventBit(npc_bit.DEAD_SOLDIERS_FIGARO_CASTLE),
            field.ClearEventBit(npc_bit.BLOCK_INSIDE_DOORS_FIGARO_CASTLE),
            field.SetEventBit(npc_bit.LONE_WOLF_FIGARO_CASTLE),
            field.SetEventBit(npc_bit.PRISONERS_FIGARO_CASTLE),
            field.SetEventBit(npc_bit.PRISON_GUARD_FIGARO_CASTLE),

            field.ClearEventBit(npc_bit.MAN_AT_COUNTER_OPERA),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_PANICKING),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_LOBBY),
            field.SetEventBit(npc_bit.IMPRESARIO_OPERA_SITTING),
            field.ClearEventBit(npc_bit.DRAGON_OPERA_HOUSE),

            field.BranchIfEventBitSet(event_bit.FINISHED_OPERA_DISRUPTION, "WOB_BITS_END"),
            field.ClearEventBit(event_bit.BEGAN_OPERA_DISRUPTION),
            field.SetEventBit(npc_bit.ULTROS_OPERA_CEILING),
            field.SetEventBit(npc_bit.RAT1_OPERA_CEILING),
            field.SetEventBit(npc_bit.RAT2_OPERA_CEILING),
            field.SetEventBit(npc_bit.RAT3_OPERA_CEILING),
            field.SetEventBit(npc_bit.RAT4_OPERA_CEILING),
            field.SetEventBit(npc_bit.RAT5_OPERA_CEILING),
            field.SetEventBit(npc_bit.CEILING_DOOR_OPERA_HOUSE),
            field.SetEventBit(npc_bit.DANCING_COUPLE1_OPERA),
            field.SetEventBit(npc_bit.DANCING_COUPLE2_OPERA),
            field.SetEventBit(npc_bit.FIGHTING_SOLDIERS_OPERA_CEILING),
            "WOB_BITS_END",
        )

    def doom_gaze_mod(self, space):
        boss_pack_id = self.get_boss("Doom Gaze", log_change = False)
        boss_name = self.enemies.packs.get_name(boss_pack_id)
        battle_type = field.BattleType.FRONT
        battle_background = 41 # airship, right, wor

        receive_bahamut_function = 0xa009d

        if not self.args.doom_gaze_no_escape:
            doom_gaze_escaped = space.next_address
            space.write(
                field.LoadMap(0x1ff, direction.DOWN, default_music = False, x = 0, y = 0, fade_in = True, airship = True),
                vehicle.End(),
            )

        self.find_doom_gaze = space.next_address
        space.write(
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.AnimateHandsUp(),
                field_entity.Pause(8),
                field_entity.AnimateAttack(),
            ),
            field.FadeOutScreen(3),
            field.HoldScreen(),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.RIGHT, 1),
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.RIGHT, 2),
                field_entity.SetSpeed(field_entity.Speed.FASTEST),
                field_entity.Move(direction.RIGHT, 8),
            ),
            field.FreeScreen(),
            field.InvokeBattleType(boss_pack_id, battle_type, battle_background),
        )
        if self.args.doom_gaze_no_escape:
            space.write(
                field.SetBattleEventBit(battle_bit.DEFEATED_DOOM_GAZE),
            )
        else:
            space.write(
                field.BranchIfBattleEventBitClear(battle_bit.DEFEATED_DOOM_GAZE, doom_gaze_escaped),
            )
        space.write(
            field.LoadMap(0x11, direction.LEFT, default_music = False, x = 17, y = 8, fade_in = True, airship = False),
            field.Branch(receive_bahamut_function),
        )

    def unequip_party_members_npc_mod(self):
        # add change party members option to unequip npc

        # overwrite "This ship's going to stick out like a sore thumb..."
        change_party_unequip_dialog_id = 1309
        self.dialogs.set_text(change_party_unequip_dialog_id, "<choice> Change party members.<line><choice> Unequip those not in party.<line><choice> Unequip all members.<line><choice> Don't do a thing!<end>")

        # lift-off/not just yet and find fc/lift-off/not just yet dialog options
        space = Reserve(0xaf56e, 0xaf58c, "airship dialog branches", field.NOP())
        change_party_unequip_dialog = space.next_address
        space.write(
            field.DialogBranch(change_party_unequip_dialog_id, dest1 = 0xaf5a8, dest2 = 0xc359d, dest3 = 0xc351e, dest4 = field.RETURN),
        )

        space = Reserve(0xc3510, 0xc351d, "airship unequip some party members dialog choice", field.NOP())
        space.write(
            field.Branch(change_party_unequip_dialog),
        )

        if self.args.equipable_umaro:
            # make unequip those not in party apply to umaro
            src = [
                "UNEQUIP_GOGO",
                field.BranchIfCharacterUnavailable(self.characters.GOGO, "UNEQUIP_UMARO"),
                field.BranchIfCharacterInParty(self.characters.GOGO, "UNEQUIP_UMARO"),
                field.RemoveAllEquipment(self.characters.GOGO),

                "UNEQUIP_UMARO",
                field.BranchIfCharacterUnavailable(self.characters.UMARO, field.RETURN),
                field.BranchIfCharacterInParty(self.characters.UMARO, field.RETURN),
                field.RemoveAllEquipment(self.characters.UMARO),
                field.Return(),
            ]
            space = Write(Bank.CB, src, "airship unequip_gogo_umaro if not in party")
            unequip_gogo_umaro = space.start_address

            space = Reserve(0xc3664, 0xc3673, "airship unequip gogo if recruited and not in party", field.NOP())
            space.write(
                field.Call(unequip_gogo_umaro),
            )

            # make unequip all apply to umaro
            src = [
                "UNEQUIP_GOGO",
                field.BranchIfCharacterUnavailable(self.characters.GOGO, "UNEQUIP_UMARO"),
                field.RemoveAllEquipment(self.characters.GOGO),

                "UNEQUIP_UMARO",
                field.BranchIfCharacterUnavailable(self.characters.UMARO, field.RETURN),
                field.RemoveAllEquipment(self.characters.UMARO),
                field.Return(),
            ]
            space = Write(Bank.CB, src, "airship unequip_all_gogo_umaro")
            unequip_all_gogo_umaro = space.start_address

            space = Reserve(0xc3591, 0xc3599, "airship unequip gogo if recruited", field.NOP())
            space.write(
                field.Call(unequip_all_gogo_umaro),
            )

    def inside_blackjack(self):
        # blackjack inside (map 0x007) entrance event, do not load the setzer npc from coin toss scene
        space = Reserve(0xaf49a, 0xaf4af, "airship inside blackjack entrance event", field.NOP())
        space.write(
            field.Return(),
        )

    def return_to_airship(self):
        # this code affects phoenix cave and kefka's tower (others?)
        # fix it so setzer is not assumed to be recruited and make player choose a party instead
        space = Reserve(field.RETURN_ALL_PARTIES_TO_FALCON, 0xc2142, "return to airship with setzer after split parties", field.NOP())
        space.write(
            field.SetParty(1),
            field.Call(field.REMOVE_ALL_CHARACTERS_FROM_ALL_PARTIES),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.UpdatePartyLeader(),
            field.ShowEntity(field_entity.PARTY0),
            field.RefreshEntities(),
        )

    def fix_fly_offscreen_bug(self):
        # ref: https://discord.com/channels/666661907628949504/666811452350398493/1025236553875857468
        # fixes the vanilla bug that can occur in which characters can fly offscreen to the bottom-right
        # per Osteoclave's research, this all originates with the the H ($0871,Y)) and V ($0873,Y) 
        #  values of (0x4D0, 0x39C) being set after changing party in WoB airship.
        # CA/F5B2: C0    If ($1E80($06A) [$1E8D, bit 2] is clear), branch to $CAF5BC
        #  -> Replace with six [FD] (no-op)
        Reserve(0xaf5b2, 0xaf5b7, "skip 06a bit clear check", field.NOP())
        # CA/F5BC: If ($1E80($06A) [$1E8D, bit 2] is set), branch to $CAF5C6 (force Locke and Celes into party)
        #  -> Replace with six [FD] (no-op)
        #  -> ref: https://discord.com/channels/666661907628949504/666811452350398493/1025271937750016020
        # CA/F5C2: Call subroutine $CAF601
        #  -> Replace with four [FD] (no-op)
        Reserve(0xaf5bc, 0xaf5c5, "skip force Locke/Celes into party", field.NOP())