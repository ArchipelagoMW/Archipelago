from ..event.event import *

class FigaroCastleWOR(Event):
    def name(self):
        return "Figaro Castle WOR"

    def character_gate(self):
        return self.characters.EDGAR

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        if self.args.character_gating:
            space.write(
                field.SetEventBit(npc_bit.SIEGFRIED_FIGARO_CAVE_ENTRANCE),
            )
        else:
            space.write(
                field.ClearEventBit(npc_bit.SIEGFRIED_FIGARO_CAVE_ENTRANCE),
            )
        space.write(
            field.SetEventBit(npc_bit.SIEGFRIED_FIGARO_CAVE_CHEST),
            field.SetEventBit(npc_bit.THIEVES_FIGARO_CAVE_TURTLE),
            field.ClearEventBit(npc_bit.GERAD_PRISON_FIGARO_CASTLE),
        )

    def mod(self):
        self.siegfried_entrance_npc_id = 0x10
        self.gerad_figaro_cave_npc_id = 0x15
        self.gerad_figaro_cave_npc = self.maps.get_npc(0x05a, self.gerad_figaro_cave_npc_id)
        self.gerad_engine_room_npc_id = 0x1a
        self.gerad_engine_room_npc = self.maps.get_npc(0x040, self.gerad_engine_room_npc_id)

        if self.args.character_gating:
            self.add_gating_condition()

        self.figaro_cave_mod()
        self.figaro_prison_mod()
        self.engine_room_mod()
        self.tentacles_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def add_gating_condition(self):
        if self.args.npc_dialog_tips:
            self.dialogs.set_text(2379, "I won't budge from this spot until you have recruited <EDGAR>!<end>")
        else:
            self.dialogs.set_text(2379, "SIGFRIED: Pretty dangerous from here on. Wait here.<end>")

        space = Reserve(0xa7778, 0xa7781, "figaro cave siegfried enters", field.NOP())
        space.write(
            field.Return(),
        )

        entrance_event = space.next_address
        space.write(
            field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            field.HideEntity(self.siegfried_entrance_npc_id),
            field.Return(),
        )

        self.maps.set_entrance_event(0x044, entrance_event - EVENT_CODE_START)

    def figaro_cave_mod(self):
        space = Reserve(0xa77a3, 0xa77a5, "figaro cave siegfried on the hum", field.NOP())
        space = Reserve(0xa7703, 0xa7705, "figaro cave gerad now, where are we", field.NOP())
        space = Reserve(0xa770f, 0xa7711, "figaro cave here, boy", field.NOP())
        space = Reserve(0xa7722, 0xa7724, "figaro cave presto", field.NOP())
        space = Reserve(0xa776e, 0xa776f, "figaro cave set gerad prison npc bit", field.NOP())

    def figaro_prison_mod(self):
        # normally, cannot access cave to ancient castle until get falcon,
        # change the condition to check if defeated tentacles
        space = Reserve(0xa5f26, 0xa5f26, "figaro castle wor ancient castle cave check")
        space.write(event_bit.DEFEATED_TENTACLES_FIGARO),

        # this leaves event bit 0x26e unused and free for other things
        space = Reserve(0xa6a2c, 0xa6a47, "figaro castle wor gerad wounded soldier", field.NOP())
        space.write(field.Return())

    def engine_room_mod(self):
        space = Reserve(0xa6a4f, 0xa6a61, "figaro castle wor split up party", field.NOP())
        space = Reserve(0xa6a6c, 0xa6a6e, "figaro castle wor here's the problem", field.NOP())
        space = Reserve(0xa6a85, 0xa6a87, "figaro castle wor you guys get in there", field.NOP())
        space = Reserve(0xa6aa8, 0xa6aaa, "figaro castle wor edgar!", field.NOP())
        space = Reserve(0xa6ab4, 0xa6ab6, "figaro castle wor what're ya waiting for", field.NOP())
        space = Reserve(0xa6acb, 0xa6ae5, "figaro castle wor recruit edgar", field.NOP())

    def tentacles_battle_mod(self):
        boss_pack_id = self.get_boss("Tentacles")
        battle_background = 0x37

        space = Reserve(0xa6ae6, 0xa6aec, "figaro castle wor invoke battle tentacles", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id, battle_background),
        )

    def character_mod(self, character):
        self.gerad_figaro_cave_npc.sprite = character
        self.gerad_figaro_cave_npc.palette = self.characters.get_palette(character)
        self.gerad_engine_room_npc.sprite = character
        self.gerad_engine_room_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xa6aed, 0xa6bdb, "figaro castle wor scenes after tentacles", field.NOP())
        space.write(
            field.HideEntity(self.gerad_engine_room_npc_id),
            field.RecruitAndSelectParty(character),
            field.StartSong(0x0a),
            field.FadeInScreen(),
            field.WaitForFade(),
            field.FreeScreen(),
            field.Branch(space.end_address + 1), # skip nops
        )

    def gerad_npc_mod(self):
        random_sprite = self.characters.get_random_esper_item_sprite()
        self.gerad_figaro_cave_npc.sprite = random_sprite
        self.gerad_figaro_cave_npc.palette = self.characters.get_palette(random_sprite)
        self.gerad_engine_room_npc.sprite = random_sprite
        self.gerad_engine_room_npc.palette = self.characters.get_palette(random_sprite)

    def esper_item_mod(self, esper_item_instructions):
        space = Reserve(0xa6aed, 0xa6bdb, "figaro castle wor scenes after tentacles", field.NOP())
        space.write(
            field.HideEntity(self.gerad_engine_room_npc_id),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.Move(direction.DOWN, 4),
            ),
            field.StartSong(0x0a),
            field.FadeInScreen(),
            field.WaitForFade(),

            esper_item_instructions,

            field.FreeScreen(),
            field.Branch(space.end_address + 1), # skip nops
        )

    def esper_mod(self, esper):
        self.gerad_npc_mod()
        space = self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.gerad_npc_mod()
        space = self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def finish_check_mod(self):
        src = [
            field.Call(field.HIDE_PARTY_MEMBERS_EXCEPT_LEADER),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro castle wor finish check")
        finish_check = space.start_address

        space = Reserve(0xa6bee, 0xa6bf1, "figaro castle wor hide party members except leader", field.NOP())
        space.write(
            field.Call(finish_check),
        )
