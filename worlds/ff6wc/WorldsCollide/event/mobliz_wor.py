from ..event.event import *

class MoblizWOR(Event):
    def name(self):
        return "Mobliz WOR"

    def character_gate(self):
        return self.characters.TERRA

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.DOGS_BARKED_MOBLIZ_WOR),
            field.SetEventBit(event_bit.MET_TERRA_WOR),
            field.SetEventBit(event_bit.SAW_MOBLIZ_LIGHT_OF_JUDGEMENT_SCENE),
            field.SetEventBit(event_bit.FOUGHT_PHUNBABA1),
            field.SetEventBit(event_bit.GOT_FENRIR),
            field.SetEventBit(event_bit.KATARIN_PREGNANT),

            field.ClearEventBit(npc_bit.KATARIN_IN_BED_MOBLIZ_WOR),
            field.ClearEventBit(npc_bit.DUANE_WITH_CHILDREN_MOBLIZ_WOR),
            field.ClearEventBit(npc_bit.KATARIN_WITH_CHILDREN_MOBLIZ_WOR),
            field.ClearEventBit(npc_bit.TERRA_BY_FIREPLACE_MOBLIZ_WOR),
            field.SetEventBit(npc_bit.GIRLS_WITH_OTHER_CHILDREN_MOBLIZ_WOR),
            field.SetEventBit(npc_bit.TERRA_DUANE_KATARIN_DOG_SOLDIER_HOUSE_MOBLIZ_WOR),
            field.SetBattleEventBit(battle_bit.DOUBLE_MORPH_DURATION),
        )

    def mod(self):
        self.terra_fireplace_npc_id = 0x11
        self.terra_fireplace_npc = self.maps.get_npc(0x09a, self.terra_fireplace_npc_id)
        self.terra_in_bed_npc_id = 0x12
        self.terra_in_bed_npc = self.maps.get_npc(0x09a, self.terra_in_bed_npc_id)
        self.terra_outside_npc_id = 0x1d
        self.terra_outside_npc = self.maps.get_npc(0x09e, self.terra_outside_npc_id)
        self.terra_with_katarin_npc_id = 0x10
        self.terra_with_katarin_npc = self.maps.get_npc(0x096, self.terra_with_katarin_npc_id)

        if self.args.character_gating:
            self.add_gating_condition()

        self.dog_walking_mod()
        self.phunbaba_mod()
        if self.args.shuffle_random_phunbaba3:
            self.phunbaba3_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def add_gating_condition(self):
        # katarin is always pregnant, change the condition
        space = Reserve(0xc5114, 0xc5119, "mobliz wor basement behind bookshelf katarin pregnant requirement")
        space.write(
            field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
        )

    def dog_walking_mod(self):
        space = Reserve(0xc4b0c, 0xc4b13, "mobliz wor katarin pregnant and not recruited terra dog conditions")
        space.write(
            field.ReturnIfAny([event_bit.IN_WOR, False, event_bit.RECRUITED_TERRA_MOBLIZ, True]),
        )

    def phunbaba_mod(self):
        space = Reserve(0xc4b51, 0xc4c06, "mobliz wor katarin pregnant scene", field.NOP())
        space.write(
            field.FadeOutSong(30),
            field.WaitForSong(),
            field.StartSong(0x32),
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xc4c09, 0xc4c1a, "mobliz wor jump straight to attacking phunbaba", field.NOP())
        space = Reserve(0xc4c88, 0xc4c8b, "mobliz wor phunbaba 2 TERRA!!", field.NOP())
        space = Reserve(0xc4c97, 0xc4cc7, "mobliz wor turn terra into esper", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

    def phunbaba3_battle_mod(self):
        boss_pack_id = self.get_boss("Phunbaba 3")

        space = Reserve(0xc4c56, 0xc4c5c, "mobliz wor invoke battle phunbaba 3", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id)
        )

    def terra_npc_mod(self, sprite, palette):
        self.terra_fireplace_npc.sprite = sprite
        self.terra_fireplace_npc.palette = palette
        self.terra_in_bed_npc.sprite = sprite
        self.terra_in_bed_npc.palette = palette
        self.terra_outside_npc.sprite = sprite
        self.terra_outside_npc.palette = palette
        self.terra_with_katarin_npc.sprite = sprite
        self.terra_with_katarin_npc.palette = palette

    def character_mod(self, character):
        self.terra_npc_mod(character, self.characters.get_palette(character))

        char_default_name = self.characters.get_default_name(character)
        self.dialogs.set_text(2307, "You're not gonna take <" + char_default_name + "> away, are you?<end>")
        self.dialogs.set_text(2315, "I'm not gonna cry.<line>If I do, <" + char_default_name + ">'ll feel sad…<end>")

        src = [
            # check for 4 party members in case phunbaba 3 was not the previous boss and no bababreath happened
            field.BranchIfPartySize(4, "RETURN"),

            field.CreateEntity(character),
            field.AddCharacterToParty(character, 1),
            field.RefreshEntities(),
        ]
        if self.args.start_average_level:
            src += [
                # Average character level via field command - example ref: CC/3A2C
                field.AverageLevel(character),
                field.RestoreHp(character, 0x7f), # restore all HP
                field.RestoreMp(character, 0x7f), # restore all MP
            ]
        src += [
            "RETURN",
            field.Return(),
        ]
        space = Write(Bank.CC, src, "character joins before Mobliz battle")
        add_character = space.start_address

        space = Reserve(0xc4cca, 0xc4cd9, "mobliz wor add character to party before phunbaba 4 if room available", field.NOP())
        space.write(
            field.Call(add_character),
        )

        boss_pack_id = self.get_boss("Phunbaba 4")

        space = Reserve(0xc4cda, 0xc4cec, "mobliz wor phunbaba 4 battle, esper terra and children scene", field.NOP())
        space.add_label("FINISH_EVENT", 0xc502a),
        space.write(
            field.InvokeBattle(boss_pack_id),
            field.RecruitAndSelectParty(character),
            field.Branch("FINISH_EVENT"), # skip scene
        )

        space = Reserve(0xc503f, 0xc5059, "mobliz wor add terra to party", field.NOP())
        space.write(
            field.FadeInScreen(),
            field.FinishCheck(),
            field.FreeScreen(),
            field.Return(),
        )

    def esper_item_mod(self, esper_item_name, esper_item_instructions):
        random_sprite = self.characters.get_random_esper_item_sprite()
        self.terra_npc_mod(random_sprite, self.characters.get_palette(random_sprite))

        # change children's dialog to replace terra's name with the esper/item name for fun
        # espers/items do not have a single byte dedicated to their name so need to use other, longer dialogs
        self.dialogs.set_text(2264, "You're not gonna take " + esper_item_name + " away, are you?<end>")
        self.dialogs.set_text(2265, "I'm not gonna cry.<line>If I do, " + esper_item_name + "'ll feel sad…<end>")
        space = Reserve(0xc4549, 0xc454b, "mobliz wor you're not gonna take terra away")
        space.write(field.Dialog(2264))
        space = Reserve(0xc506a, 0xc506c, "mobliz I'm not gonna cry")
        space.write(field.Dialog(2265))

        boss_pack_id = self.get_boss("Phunbaba 4")

        space = Reserve(0xc4cca, 0xc4cec, "mobliz wor phunbaba 4 battle, esper terra and children scene", field.NOP())
        space.add_label("FINISH_EVENT", 0xc502a),
        space.write(
            field.InvokeBattle(boss_pack_id),
        )
        if not self.args.shuffle_random_phunbaba3:
            space.write(
                field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            )
        space.write(
            field.FadeOutSong(0),
            field.Branch("FINISH_EVENT"), # skip scene
        )

        space = Reserve(0xc503f, 0xc5059, "mobliz wor phunbaba 4 battle, esper terra and children scene", field.NOP())
        space.write(
            field.FadeInScreen(),
            field.FreeScreen(),

            esper_item_instructions,
            field.FinishCheck(),
            field.Return(),
        )

    def esper_mod(self, esper):
        self.esper_item_mod(self.espers.get_name(esper), [
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.esper_item_mod(self.items.get_name(item), [
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
