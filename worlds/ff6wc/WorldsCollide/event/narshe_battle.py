from ..event.event import *

class NarsheBattle(Event):
    def name(self):
        return "Narshe Battle"

    def characters_required(self):
        return 2

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.CHAR_LINEUP_BATTLE_NARSHE_WOB),
            field.SetEventBit(npc_bit.BANON_BEFORE_BATTLE_NARSHE_WOB),
        )

    def mod(self):
        self.terra_npc_id = 0x11
        self.locke_npc_id = 0x12
        self.celes_npc_id = 0x13
        self.cyan_npc_id = 0x14
        self.edgar_npc_id = 0x15
        self.sabin_npc_id = 0x16
        self.gau_npc_id = 0x17
        self.save_point_npc_id = 0x26

        self.snowfield_save_point_mod()
        self.banon_npc_mod()
        self.start_battle_mod()
        self.kefka_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def snowfield_save_point_mod(self):
        space = Reserve(0xcc591, 0xcc5fe, "narshe wob kefka battlefield save point character reset", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops to prevent delay
        )

    def banon_npc_mod(self):
        # remove banon's name from game over dialog
        self.dialogs.set_text(1745, "Couldn't hold out!?<line>I have a bad feeling about this…<end>")

        self.banon_before_battle_npc_id = 0x18
        self.banon_before_battle_npc = self.maps.get_npc(0x016, self.banon_before_battle_npc_id)

        # originally banon before battle shares same npc bit as rest of character lineup
        # to get banon to show up without the character lineup change the npc bit to
        self.banon_before_battle_npc.event_byte = 0x65
        self.banon_before_battle_npc.event_bit = 4

        # do not block path with banon before battle
        self.banon_before_battle_npc.x = 21

        self.banon_during_battle_npc_id = 0x25
        self.banon_during_battle_npc = self.maps.get_npc(0x016, self.banon_during_battle_npc_id)

    def start_battle_mod(self):
        prepared_dialog = 874
        self.dialogs.set_text(prepared_dialog, "Prepared?<line><choice> Yes<line><choice> No<end>") # remove Banon's name

        need_more_chars_dialog = 878 # overwrite mog tutorial dialog
        self.dialogs.set_text(need_more_chars_dialog, "Hurry! Find another ally!<end>")

        lose_condition_dialog = 886
        self.dialogs.set_text(lose_condition_dialog, "We're history if they reach me!<line>Good luck!<end>") # remove Banon's name

        space = Reserve(0xcc605, 0xcc62a, "narshe wob battle banon npc event", field.NOP())
        space.write(
            field.BranchIfEventWordGreater(event_word.CHARACTERS_AVAILABLE, 1, "PREPARED_DIALOG"),

            field.Dialog(need_more_chars_dialog),
            field.Return(),

            "PREPARED_DIALOG",
            field.DialogBranch(prepared_dialog, dest1 = space.end_address + 1, dest2 = 0xa5eb3),
        )

        space = Reserve(0xcc62b, 0xcc668, "narshe wob battle tutorial and char bits set", field.NOP())
        for npc_id in range(self.terra_npc_id, self.banon_before_battle_npc_id + 1):
            space.write(
                field.DeleteEntity(npc_id),
            )
        space.write(
            field.Call(field.REMOVE_ALL_CHARACTERS_FROM_ALL_PARTIES),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_TWO_PARTIES),
            field.Branch(space.end_address + 1),
        )

        space = Reserve(0xcc66f, 0xcc670, "narshe wob hide banon before battle npc", field.NOP())
        space.write(
            field.ClearEventBit(npc_bit.BANON_BEFORE_BATTLE_NARSHE_WOB),
        )

        space = Reserve(0xcc679, 0xcc687, "narshe wob create characters for battle", field.NOP())
        for npc_id in range(self.terra_npc_id, self.gau_npc_id + 1):
            space.write(
                field.DeleteEntity(npc_id),
            )
        space.write(
            field.RefreshEntities(),
        )

        space = Reserve(0xcc690, 0xcc693, "narshe wob place party 3 on map", field.NOP())

        space = Reserve(0xcc69c, 0xcc69c, "narshe wob move party 0 starting position right one")
        space.write(21)

        space = Reserve(0xcc6ab, 0xcc6ab, "narshe wob move party 1 starting position right one")
        space.write(19)

        space = Reserve(0xcc6b3, 0xcc6c1, "narshe wob initialize party 3 position, direction, speed", field.NOP())
        space.write(
            field.Branch(space.end_address + 1),
        )

        space = Reserve(0xcc6c6, 0xcc6e8, "narshe wob change characters event addresses", field.NOP())
        space.write(
            field.DeleteEntity(self.banon_before_battle_npc_id),
            field.DeleteEntity(self.save_point_npc_id),
            field.Call(field.DELETE_CHARACTERS_NOT_IN_ANY_PARTY),
            field.RefreshEntities(),
        )

        space = Reserve(0xcc6ee, 0xcc6f0, "narshe wob banon they're coming!", field.NOP())

        space = Reserve(0xcc6f7, 0xcc715, "narshe wob animate characters attack pose", field.NOP())
        space.write(
            field.HoldScreen(),
            field.Branch(space.end_address + 1),
        )

        space = Reserve(0xcc732, 0xcc734, "narshe wob kefka oho!! it's general celes", field.NOP())
        space = Reserve(0xcc82e, 0xcc830, "narshe wob kefka get those vile insects", field.NOP())

        space = Reserve(0xcc85e, 0xcc85e, "narshe wob move party 0 starting position right one (again after map reload)")
        space.write(21)

        space = Reserve(0xcc86d, 0xcc86d, "narshe wob move party 1 starting position right one (again after map reload)")
        space.write(19)

        space = Reserve(0xcc875, 0xcc883, "narshe wob initialize party 3 position, direction, speed (again after map reload)", field.NOP())
        space.write(
            field.Branch(space.end_address + 1),
        )

    def kefka_battle_mod(self):
        boss_pack_id = self.get_boss("Kefka (Narshe)")

        src = [
            Read(0xcbca0, 0xcbca1), # clear battle temp song override

            field.InvokeBattle(boss_pack_id, check_game_over = False),
            field.RefreshEntities(),
            field.UpdatePartyLeader(),

            Read(0xcbca5, 0xcbcb0), # check game over, if not show end scene, else move party back to save point spot
        ]
        space = Write(Bank.CC, src, "narshe wob invoke kefka battle")
        invoke_kefka_battle = space.start_address

        space = Reserve(0xcbca0, 0xcbcb0, "narshe battle call invoke kefka battle", field.NOP())
        space.write(
            field.Call(invoke_kefka_battle),
            field.Return(),
        )

    def end_event_mod(self, reward_instructions):
        space = Reserve(0xcbcb5, 0xcbcb7, "narshe wob kefka aack!! i wont forget this", field.NOP())
        space = Reserve(0xcbcf7, 0xcbcfa, "narshe wob wheres the esper? is it okay?", field.NOP())

        src = [
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.ClearEventBit(event_bit.ENABLE_Y_PARTY_SWITCHING),
            field.ClearEventBit(event_bit.DISABLE_SPRINT),
            field.ClearEventBit(0x1ca), # useless event bit?
            field.SetEventBit(event_bit.FINISHED_NARSHE_BATTLE),
        ]

        # delete all npcs from this map except save point
        for npc_id in range(0x10, self.save_point_npc_id):
            src += [
                field.DeleteEntity(npc_id),
            ]

        for soldier_bit in range(npc_bit.BROWN_SOLDIER1_BATTLE_NARSHE_WOB, npc_bit.BROWN_SOLDIER6_BATTLE_NARSHE_WOB + 1):
            src += [
                field.ClearEventBit(soldier_bit),
            ]

        src += [
            field.ClearEventBit(npc_bit.KEFKA_DURING_BATTLE_NARSHE_WOB),
            field.ClearEventBit(npc_bit.BANON_DURING_BATTLE_NARSHE_WOB),
            field.SetEventBit(npc_bit.SAVE_POINT_SNOWFIELD_NARSHE_WOB),

            # normally this bit is not cleared after the battle, I am clearing it so save point works again after
            field.ClearEventBit(event_bit.FIGHTING_KEFKA_NARSHE_WOB),

            reward_instructions,

            field.SetParty(1),
            
            # ref: CB/7217
            field.HoldScreen(),
            field.DisableEntityCollision(field_entity.PARTY0),

            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.DOWN, 8),
            ),

            field.FadeOutScreen(4),
            field.WaitForFade(),

            field.Call(field.REMOVE_ALL_CHARACTERS_FROM_ALL_PARTIES),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),

            field.UpdatePartyLeader(),
            field.ShowEntity(field_entity.PARTY0),
            field.RefreshEntities(),

            field.FreeScreen(),
            field.LoadMap(0x1e, direction.DOWN, default_music = True,
                          x = 60, y = 37, fade_in = False, entrance_event = True),
            field.FadeInScreen(4),
            field.WaitForFade(),

            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "narshe battle reward/end event")
        end_event = space.start_address

        space = Reserve(0xcbcff, 0xcbd04, "narshe battle call reward/event end")
        space.write(
            field.Branch(end_event),
        )

    def character_mod(self, character):
        self.banon_before_battle_npc.sprite = character
        self.banon_before_battle_npc.palette = self.characters.get_palette(character)
        self.banon_during_battle_npc.sprite = character
        self.banon_during_battle_npc.palette = self.characters.get_palette(character)

        self.end_event_mod([
            field.RecruitCharacter(character),
        ])

    def esper_item_mod(self, esper_item_instructions):
        random_sprite = self.characters.get_random_esper_item_sprite()
        self.banon_before_battle_npc.sprite = random_sprite
        self.banon_before_battle_npc.palette = self.characters.get_palette(self.banon_before_battle_npc.sprite)
        self.banon_during_battle_npc.sprite = random_sprite
        self.banon_during_battle_npc.palette = self.characters.get_palette(self.banon_during_battle_npc.sprite)

        self.end_event_mod(esper_item_instructions)

    def esper_mod(self, esper):
        self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
