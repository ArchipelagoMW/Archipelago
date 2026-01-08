from ..constants.entities import SETZER
from ..event.event import *

class OperaHouseWOB(Event):
    def name(self):
        return "Opera House"

    def character_gate(self):
        return self.characters.CELES

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.SAW_OPERA_OVERTURE),
            field.SetEventBit(event_bit.READY_CELES_OPERA_SCENE),

            field.SetEventBit(event_bit.OPERA_MAP_MODIFIED1),
            field.SetEventBit(event_bit.OPERA_MAP_MODIFIED2),
            field.SetEventBit(event_bit.OPERA_MAP_MODIFIED3),

            field.SetEventBit(event_bit.FOUND_ULTROS_LETTER_OPERA),
            field.SetEventBit(event_bit.SAW_OPERA_DUEL_SCENE),

            field.SetEventBit(event_bit.SETZER_ABDUCTED_CELES),
            field.SetEventBit(event_bit.TOSSED_CELES_SETZER_COIN),

            field.ClearEventBit(npc_bit.MAN_OPERA_ENTRANCE),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_ENTRANCE),
            field.ClearEventBit(npc_bit.IMPRESARIO_OPERA_LOBBY),
            field.ClearEventBit(npc_bit.ULTROS_OPERA_LOBBY),
            field.ClearEventBit(npc_bit.ULTROS_LETTER_OPERA_GROUND),
        )

    def mod(self):
        self.setzer_npc_id = 0x25
        self.setzer_npc = self.maps.get_npc(0x0e9, self.setzer_npc_id)

        self.celes_after_maria_npc_id = 0x26 # the celes sprite used after she is spun around by setzer
        self.celes_after_maria_npc = self.maps.get_npc(0x0e9, self.celes_after_maria_npc_id)
        self.celes_after_maria_npc.sprite = self.characters.CELES
        self.celes_after_maria_npc.palette = self.characters.get_palette(self.characters.CELES)
        self.celes_after_maria_npc.unknown1 = 0 # this was set to 1 and prevented animating character

        self.begin_performance_mod()
        self.performance_mod()
        self.end_performance_mod()

        self.timer_mod()
        self.dialog_mod()
        self.start_event_mod()
        self.stage_fall_mod()
        self.ultros_battle_mod()
        self.after_battle_mod()

        if not self.args.fixed_encounters_original:
            self.fixed_battles_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
            self.character_music_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
            self.character_music_mod(SETZER)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
            self.character_music_mod(SETZER)

        self.log_reward(self.reward)

    def begin_performance_mod(self):
        space = Reserve(0xaf18b, 0xaf1a1, "opera house changing room entrance event", field.NOP())
        space.write(
            field.Return(),
        )

        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FadeOutSong(0x10),
            field.FadeOutScreen(),
            field.Pause(4),
            field.StartSong(39),

            field.SetSprite(field_entity.PARTY0, 26),
            field.SetPalette(field_entity.PARTY0, 0),

            Read(0xabb0c, 0xabb16), # load castle map, tint screen
            field.Return(),
        ]
        space = Write(Bank.CA, src, "opera scene initialize")
        initialize = space.start_address

        space = Reserve(0xabafd, 0xabb16, "opera scene begin", field.NOP())
        space.write(
            field.ReturnIfAny([event_bit.FINISHED_OPERA_PERFORMANCE, True, event_bit.IN_WOR, True]),
            field.BranchIfEventBitSet(event_bit.FINISHED_OPERA_DISRUPTION, "BEGIN"),
            field.ReturnIfEventBitSet(event_bit.BEGAN_OPERA_DISRUPTION),

            "BEGIN",
            field.Call(initialize),
        )

    def fixed_battles_mod(self):
        # The rafters have 5 fixed battles, all with the same pack (281)
        # to increase the variety of encounters, we are adding 1 more and swapping 2 of the rats to it
        # 414 is an otherwise unused encounter

        replaced_encounters = [
            (414, 0xAC37B), 
            (414, 0xAC3B4),
        ]
        for pack_id_address in replaced_encounters:
            pack_id = pack_id_address[0]
            # first byte of the command is the pack_id
            invoke_encounter_pack_address = pack_id_address[1]+1
            space = Reserve(invoke_encounter_pack_address, invoke_encounter_pack_address, "rat invoke fixed battle (battle byte)")
            space.write(
                # subtrack 256 since WC stores fixed encounter IDs starting at 256
                pack_id - 0x100
            )

    def performance_mod(self):
        # change celes to party leader
        maria_action_queues = [
            0xabc28, 0xabc53, 0xabcd3, 0xabce5, 0xabd17, 0xabd95,
        ]
        for address in maria_action_queues:
            space = Reserve(address, address, "opera scene change celes to party leader")
            space.write(field_entity.PARTY0)

        src = []
        for character in range(self.characters.CHARACTER_COUNT):
            palette = self.characters.get_palette(character)
            src += [
                field.SetSprite(character, character),
                field.SetPalette(character, palette),
            ]
        src += [
            field.Return(),
        ]
        space = Write(Bank.CA, src, "opera scene restore character sprite/palette")
        restore_character_graphics = space.start_address

        space = Reserve(0xabee0, 0xabf05, "opera scene dance", field.NOP())
        space.write(
            field.Call(restore_character_graphics),
            field.StartSong(38),
        )

        # game over after first failure
        space = Reserve(0xabdba, 0xabe0f, "opera performance failed, game over", field.NOP())
        space.write(
            field.Call(restore_character_graphics), # maria does not have game over animation
            field.Call(field.GAME_OVER),
            field.Return(),
        )

    def end_performance_mod(self):
        space = Reserve(0xabf10, 0xabf11, "opera scene pause before well done", field.NOP())
        space.write(
            field.Pause(0.5),
        )

        self.dialogs.set_text(0x04c7, "Well done.<end>") # remove locke/celes names

        src = [
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.SetEventBit(event_bit.FINISHED_OPERA_PERFORMANCE),
            field.CheckObjectives(),
            field.FreeMovement(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "opera scene check conditions")
        check_conditions = space.start_address

        space = Reserve(0xabf15, 0xabf19, "opera scene call check conditions", field.NOP())
        space.write(
            field.Call(check_conditions),
        )

    def timer_mod(self):
        # game over after first failure
        space = Reserve(0xaba3f, 0xaba42, "opera failed, reset", field.NOP())
        space.write(
            field.Call(field.GAME_OVER),
        )

        if self.args.event_timers_random:
            import random

            # randomize timer between 4 and 7 minutes
            seconds = random.randint(240, 420)

            space = Reserve(0xaba03, 0xaba04, "opera house timer")
            space.write(
                (seconds * 60).to_bytes(2, "little"),
            )

            timer_display = f"{seconds // 60}:{seconds % 60:>02}"
            self.log_change(f"Timer 5:00", timer_display)
        elif self.args.event_timers_none:
            space = Reserve(0xaba02, 0xaba07, "opera house timer", field.NOP())

    def dialog_mod(self):
        space = Reserve(0xab6f7, 0xab6f9, "opera house dialog after dirt dragon", field.NOP())
        space = Reserve(0xabf31, 0xabf33, "ultros's first opera house note", field.NOP())
        space = Reserve(0xabf36, 0xabf38, "first opera house note reaction dialog", field.NOP())
        space = Reserve(0xabf3e, 0xabf40, "ultros's second opera house note", field.NOP())  # if party fails first time
        space = Reserve(0xabf43, 0xabf45, "second opera house note reaction dialog", field.NOP())  # if party fails first time
        space = Reserve(0xab998, 0xab99a, "opera house ultros 4 tons dialog", field.NOP())
        space = Reserve(0xab472, 0xab474, "stage master far right switch dialog", field.NOP())
        space = Reserve(0xabf4f, 0xabf51, "opera house ultros phew rats dialog", field.NOP())
        space = Reserve(0xac05c, 0xac05e, "opera house impresario disaster dialog", field.NOP())
        space = Reserve(0xac0af, 0xac0b1, "opera house neither draco nor ralse dialog", field.NOP())
        space = Reserve(0xac0cc, 0xac0ce, "opera house world's premier adventurer dialog", field.NOP())
        space = Reserve(0xac0d7, 0xac0d9, "opera house impresario aya dialog", field.NOP())
        space = Reserve(0xac0f0, 0xac0f2, "opera house octopus royalty dialog", field.NOP())
        space = Reserve(0xac0fc, 0xac0fe, "opera house impresario MUSIC!! dialog", field.NOP())
        space = Reserve(0xac14c, 0xac14e, "opera house just a darn minute dialog", field.NOP())
        space = Reserve(0xac2eb, 0xac2ed, "opera house man of my word dialog", field.NOP())
        space = Reserve(0xac2f4, 0xac2f6, "opera house celes that's HIM dialog", field.NOP())
        space = Reserve(0xac32e, 0xac330, "opera house impresario what a reversal dialog", field.NOP())

    def start_event_mod(self):
        # scene after showing impresario ultros' note and seeing ultros at weight
        space = Reserve(0xab744, 0xab75f, "opera house impressario What!!!?", field.NOP())
        space.add_label("IS_EVERYTHING_OK?", 0xab740)
        space.add_label("START_EVENT", 0xab95f)
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), "IS_EVERYTHING_OK?"),
            )
        space.write(
            field.FadeOutSong(48),
            field.HoldScreen(),
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.Branch("START_EVENT"),
        )

        space = Reserve(0xab9b0, 0xab9fb, "opera house after showing impresario ultros's note", field.NOP())
        space.write(
            field.ShowEntity(field_entity.PARTY0),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(15, 45),
                field_entity.Turn(direction.UP),
            ),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.Move(direction.DOWN, 8),
            ),
            field.FadeInScreen(),
            field.WaitForEntityAct(field_entity.CAMERA),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Turn(direction.DOWN),
                field_entity.SetSpriteLayer(0),
            ),
            field.FreeScreen(),
            field.Pause(0.5),
            field.Branch(space.end_address + 1),
        )

    def stage_fall_mod(self):
        # shorten scene after falling with ultros, cut pauses in half and remove audience gasps
        space = Reserve(0xac047, 0xac048, "opera house pause after fall", field.NOP())
        space = Reserve(0xac04d, 0xac04f, "opera house play whispers song after fall", field.NOP())
        space = Reserve(0xac058, 0xac058, "opera house pause after impresario runs out")
        space.write(3)
        space = Reserve(0xac060, 0xac060, "opera house pause before character kneels")
        space.write(4)
        space = Reserve(0xac065, 0xac06f, "opera house pause after character kneels", field.NOP())
        space = Reserve(0xac075, 0xac075, "opera house pause after character exclaims")
        space.write(3)
        space = Reserve(0xac0a4, 0xac0a4, "opera house pause after character jumps")
        space.write(5)

    def ultros_battle_mod(self):
        boss_pack_id = self.get_boss("Ultros 2")

        space = Reserve(0xac11b, 0xac127, "opera house invoke battle ultros", field.NOP())
        space.write(
            # game over if die to ultros instead of getting more chances
            # use the original game over so party is not refreshed (otherwise their stage positions are broken)
            field.SetEventBit(event_bit.CONTINUE_MUSIC_DURING_BATTLE),
            field.InvokeBattle(boss_pack_id, check_game_over = False),
            field.ClearEventBit(event_bit.CONTINUE_MUSIC_DURING_BATTLE),
            field.Call(field.ORIGINAL_CHECK_GAME_OVER),
        )

    def after_battle_mod(self):
        # when maria changes to celes, a special celes sprite is used
        # change it to use normal celes sprite to allow customization and use a different pose
        src = [
            field.CreateEntity(self.celes_after_maria_npc_id),
            field.EntityAct(self.celes_after_maria_npc_id, True,
                field_entity.AnimateSurprised(),
                field_entity.DisableWalkingAnimation(),
            ),
            field.ShowEntity(self.celes_after_maria_npc_id),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "opera house show celes after maria npc")
        show_celes = space.start_address

        # hide party leader to prevent possible conflict between celes being party leader and the person on stage at
        # the same time. also hide party leader when other npcs are hidden by shifting [0xcac16c, 0xcac26c] down
        # a few memory spaces into previous "what a performance!!" dialog code to make room for hiding party leader
        # bytes 0xac16c-0xac16d are inserted in character_music_mod()
        space = Reserve(0xac171, 0xac26f, "opera house move setzer entrance instructions")
        space.copy_from(0xac16e, 0xac26c)

        space = Reserve(0xac16c, 0xac16e, "opera house hide party leader", field.NOP())
        space.write(
            field.HideEntity(field_entity.PARTY0),
        )

        space = Reserve(0xac277, 0xac277, "opera house assign palette to celes on stage")
        space.write(self.characters.get_palette(self.characters.CELES))

        # do not add celes to the party
        # also hide her in case she is in party and show_char was already called for her or she can block setzer's path
        # NOTE: setzer is shown after this space so if celes is replacing setzer she will still be shown in time
        space = Reserve(0xac278, 0xac27a, "opera house do not add celes to party", field.NOP())
        space.write(
            field.HideEntity(self.characters.CELES),
        )

        space = Reserve(0xac2bf, 0xac2c2, "opera house create/show celes carried npc", field.NOP())
        space.write(
            field.Call(show_celes),
        )
       
        # do not animate the now hidden party leader
        space = Reserve(0xac28a, 0xac28d, "opera house do not turn party leader up", field.NOP())
        space = Reserve(0xac30d, 0xac312, "opera house do not move party leader up", field.NOP())

        # skip camera moving slowly down across musicians
        space = Reserve(0xac341, 0xac353, "opera house skip move camera over musicians", field.NOP())

        # do not fade out screen here, let select parties do it
        space = Reserve(0xac356, 0xac358, "opera house skip screen fade", field.NOP())

        space = Reserve(0xac35d, 0xac361, "opera house skip assign setzer properties", field.NOP())

    def reward_mod(self, reward_instructions):
        src = [
            field.Call(field.HIDE_ALL_PARTY_MEMBERS),
            field.HideEntity(self.characters.CELES), # hide celes or she will show up on airship too
            field.SetEventBit(event_bit.FINISHED_OPERA_DISRUPTION),
            field.ClearEventBit(npc_bit.FIGHTING_SOLDIERS_OPERA),
            field.ClearEventBit(npc_bit.FIGHTING_SOLDIERS_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT1_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT2_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT3_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT4_OPERA_CEILING),
            field.ClearEventBit(npc_bit.RAT5_OPERA_CEILING),
            field.SetEventBit(event_bit.AIRSHIP_FLYING), # landed to enter opera house, have to set flying bit again

            reward_instructions,
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "opera house reward/end event")
        end_event = space.start_address

        space = Reserve(0xb1b0e, 0xb1b13, "opera house call reward/end event", field.NOP())
        space.write(
            field.Branch(end_event),
        )

    def character_music_mod(self, character):
        from ..music.song_utils import get_character_theme
        # 0xac16c-0xac16d typically play setzer's theme,
        # but in the after_battle_mod() 0xac16c-0xac26c are shifted 3 bytes to the right,
        # so the theme now occupies 0xac16f-0xac170
        space = Reserve(0xac16f, 0xac170, "Play Song Setzer")
        space.write(field.StartSong(get_character_theme(character)))

    def character_mod(self, character):
        self.setzer_npc.sprite = character
        self.setzer_npc.palette = self.characters.get_palette(character)

        self.reward_mod([
            field.RecruitAndSelectParty(character),
            field.StartSong(53),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.LoadMap(0x06, direction.DOWN, default_music = True, x = 16, y = 6, fade_in = True),
        ])

    def esper_item_mod(self, esper_item_instructions):
        self.setzer_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.setzer_npc.palette = self.characters.get_palette(self.setzer_npc.sprite)

        self.reward_mod([
            field.RefreshEntities(),
            field.UpdatePartyLeader(),
            field.ShowEntity(field_entity.PARTY0),
            field.StartSong(53),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.LoadMap(0x06, direction.DOWN, default_music = True, x = 16, y = 6, fade_in = True),
            esper_item_instructions,
        ])

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
