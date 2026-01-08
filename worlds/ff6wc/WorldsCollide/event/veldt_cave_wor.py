from ..event.event import *

class VeldtCaveWOR(Event):
    def name(self):
        return "Veldt Cave WOR"

    def character_gate(self):
        return self.characters.SHADOW

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.shadow_npc_id = 0x12
        self.shadow_npc = self.maps.get_npc(0x161, self.shadow_npc_id)

        self.relm_npc_id = 0x13
        self.relm_npc = self.maps.get_npc(0x161, self.relm_npc_id)

        self.dialog_mod()

        if self.args.character_gating:
            self.add_gating_condition()

        self.srbehemoth_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xb79cd, 0xb79d5, "veldt cave wor you're coming with us", field.NOP())
        space = Reserve(0xb7a43, 0xb7a45, "veldt cave wor look at those wounds", field.NOP())

    def add_gating_condition(self):
        interceptor_beginning_id = 0x11
        interceptor_end_id = 0x15

        space = Reserve(0xb7d08, 0xb7d57, "veldt cave wor relm/shadow in bed in thamasa after veldt cave", field.NOP())

        entrance_event = space.next_address
        space.copy_from(0xb7982, 0xb7989) # shadow/relm animate laying down
        space.write(
            field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
            field.HideEntity(interceptor_beginning_id),
            field.HideEntity(interceptor_end_id),
            field.Return(),
        )

        interceptor_beginning_event = space.next_address
        space.copy_from(0xb79a5, 0xb79b0) # bark, pause, call blink 3 times, set event bit
        space.write(
            field.Return(),
        )

        sr_behemoth_event = space.next_address
        space.copy_from(0xb7a1e, 0xb7a2f) # pause, animate surprised, hold screen, move camera down/up
        space.write(
            field.Return(),
        )

        space = Reserve(0xb7982, 0xb7989, "veldt cave wor entrance event shadow/relm animate laying down", field.NOP())
        space.write(
            field.Call(entrance_event),
        )

        space = Reserve(0xb79a5, 0xb79b0, "veldt cave interceptor beginning event gate check", field.NOP())
        space.write(
            field.ReturnIfAny([event_bit.FOUND_INTERCEPTOR_VELDT_CAVE_WOR, True, event_bit.character_recruited(self.character_gate()), False]),
            field.Call(interceptor_beginning_event),
        )

        space = Reserve(0xb7a1e, 0xb7a2f, "veldt cave wor sr behemoth event gate check", field.NOP())
        space.write(
            field.ReturnIfAny([event_bit.DEFEATED_SR_BEHEMOTH, True, event_bit.character_recruited(self.character_gate()), False]),
            field.Call(sr_behemoth_event),
        )

    def srbehemoth_battle_mod(self):
        boss_pack_id = self.get_boss("SrBehemoth")

        space = Reserve(0xb7a73, 0xb7a98, "veldt cave wor invoke battle srbehemoth", field.NOP())
        space.write(
            # stop music before battle to prevent it playing after winning and before moving to thamasa
            field.StartSong(0), # silence
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.InvokeBattle(boss_pack_id),
            field.ClearEventBit(npc_bit.BEHEMOTH_VELDT_CAVE),
            field.SetEventBit(event_bit.DEFEATED_SR_BEHEMOTH),
        )

    def move_to_thamasa(self, reward_instructions):
        space = Reserve(0xb7aa1, 0xb7be2, "veldt cave wor move party to strago's room in thamasa", field.NOP())
        space.write(
            field.FadeInSong(0x08, 0x30),
            field.LoadMap(0x001, direction.DOWN, default_music = False, x = 251, y = 230, fade_in = False, airship = True),
            vehicle.SetPosition(251, 231),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x15d, direction.DOWN, default_music = True, x = 61, y = 13, update_parent_map = True),

            # make interceptor only appear until you leave the screen
            field.ClearEventBit(npc_bit.INTERCEPTOR_STRAGO_ROOM),

            reward_instructions,

            field.FinishCheck(),
            field.Return(),
        )

    def character_mod(self, character):
        self.shadow_npc.sprite = character
        self.shadow_npc.palette = self.characters.get_palette(character)
        self.relm_npc.sprite = character
        self.relm_npc.palette = self.characters.get_palette(character)

        self.move_to_thamasa([
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
        ])

    def esper_item_mod(self, esper_item_instructions):
        self.move_to_thamasa([
            field.FadeInScreen(),
            esper_item_instructions,
        ])

    def esper_mod(self, esper):
        self.shadow_npc.sprite = 91
        self.shadow_npc.palette = 2
        self.shadow_npc.split_sprite = 1
        self.shadow_npc.direction = direction.UP

        self.relm_npc.sprite = 91
        self.relm_npc.palette = 2
        self.relm_npc.split_sprite = 1
        self.relm_npc.direction = direction.UP

        self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        random_sprite = self.characters.get_random_esper_item_sprite()

        self.shadow_npc.sprite = random_sprite
        self.shadow_npc.palette = self.characters.get_palette(self.shadow_npc.sprite)

        self.relm_npc.sprite = random_sprite
        self.relm_npc.palette = self.characters.get_palette(self.relm_npc.sprite)

        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
