from ..event.event import *

class BarenFalls(Event):
    def name(self):
        return "Baren Falls"

    def character_gate(self):
        return self.characters.SABIN

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        # delete row of events that trigger sabin/cyan dialog and shadow leaving (if in party)
        for x in range(9, 18):
            self.maps.delete_event(0x9c, x, 12)

        if self.args.character_gating:
            self.add_gating_condition()

        self.rizopas_battle_mod()
        self.after_battle_mod()
        self.already_complete_mod()

        if self.args.flashes_remove_most:
            self.background_scrolling_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def add_gating_condition(self):
        src = [
            field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            Read(0xbc03f, 0xbc057)   # jump? dialog
        ]
        space = Write(Bank.CB, src, "baren falls character gating")
        gate_check = space.start_address

        space = Reserve(0xbc03f, 0xbc057, "baren falls jump dialog options", field.NOP())
        space.write(
            field.Branch(gate_check),
            field.Return(),
        )

    def rizopas_battle_mod(self):
        boss_pack_id = self.get_boss("Rizopas")

        space = Reserve(0xbc0b6, 0xbc0bc, "baren falls invoke battle rizopas", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def after_battle_mod(self):
        src = [
            # move airship
            field.LoadMap(0x000, direction.DOWN, default_music = False,
                          x = 192, y = 105, fade_in = False, airship = True),
            vehicle.SetPosition(192, 105),
            vehicle.SetEventBit(event_bit.VELDT_WORLD_MUSIC),

            vehicle.LoadMap(0x09f, direction.DOWN, default_music = True, x = 15, y = 0, fade_in = False),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "baren falls move airship after rizopas battle")
        load_map = space.start_address

        space = Reserve(0xbc0bf, 0xbc0c4, "baren falls load map after rizopas battle", field.NOP())
        space.write(
            field.Call(load_map),
        )

        space = Reserve(0xbc0cb, 0xbc0cc, "baren falls pause before starting song", field.NOP())

    def already_complete_mod(self):
        # jumped after rizopas already defeated, exit to world map after battle
        src = [
            # move airship
            field.StartSong(0),
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.LoadMap(0x000, direction.DOWN, default_music = False,
                          x = 192, y = 105, fade_in = False, airship = True),
            vehicle.SetPosition(192, 105),
            vehicle.SetEventBit(event_bit.VELDT_WORLD_MUSIC),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),

            # load world map
            vehicle.LoadMap(0x000, direction.DOWN, default_music = True, x = 192, y = 105),
            world.End(),
        ]
        space = Write(Bank.CB, src, "baren falls exit function")
        exit_function = space.start_address

        space = Reserve(0xbc203, 0xbc209, "baren falls rizopas already defeated, load wob", field.NOP())
        space.write(
            field.Branch(exit_function),
        )

    def character_music_mod(self, character):
        from ..music.song_utils import get_character_theme

        space = Reserve(0xbc0ff, 0xbc100, "Play Song Gau")
        space.write([
            field.StartSong(get_character_theme(character)),
        ])

    def character_mod(self, character):
        self.character_music_mod(character)
        gau_npc_id = 0x10
        gau_npc = self.maps.get_npc(0x09f, gau_npc_id)
        gau_npc.sprite = character
        gau_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xbc15d, 0xbc1b1, "baren falls gau naming", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nop
        )

        space = Reserve(0xbc1e2, 0xbc1ee, "baren falls gau runs off", field.NOP())
        space.write(
            field.Pause(0.5),
            field.RecruitCharacter(character),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.Branch(space.end_address + 1), # skip nop
        )

        src = [
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.SetEventBit(event_bit.NAMED_GAU),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "baren falls character finish check")
        finish_check = space.start_address

        space = Reserve(0xbc1f2, 0xbc1f5, "baren falls character call finish check", field.NOP())
        space.write(
            field.Call(finish_check),
        )

    def esper_item_mod(self, esper_item_instructions):
        space = Reserve(0xbc0f7, 0xbc1b7, "baren falls gau moving/naming", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nop
        )

        space = Reserve(0xbc1c2, 0xbc1c5, "skip gau turns left at baren falls", field.NOP())

        space = Reserve(0xbc1dc, 0xbc1f5, "baren falls esper item reward", field.NOP())
        space.write(
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.SetEventBit(event_bit.NAMED_GAU),
            esper_item_instructions,
            field.FinishCheck(),
            field.Branch(space.end_address + 1), # skip nop
        )

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

    def background_scrolling_mod(self):
        # Slow the scrolling background by modifying the ADC command.
        space = Reserve(0x2b1f7, 0x2b1f9, "waterfall background movement")
        space.write(
            asm.ADC(0x0001, asm.IMM16) #default: 0x0006
        )

        # Eliminate the palette swaps without reducing any cpu cycles by just writing back the value from the previous LDA
        space = Reserve(0x2b20b, 0x2b20d, "waterfall palette change")
        space.write(
            asm.STA(0xEC71, asm.ABS_X)
        )
