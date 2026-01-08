from ..event.event import *

class ZoneEater(Event):
    def name(self):
        return "Zone Eater"

    def character_gate(self):
        return self.characters.GOGO

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.gogo_npc_id = 0x10
        self.gogo_npc = self.maps.get_npc(0x116, self.gogo_npc_id)

        if self.args.character_gating:
            self.add_gating_condition()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def add_gating_condition(self):
        chest_bridge_npc_id = 0x11
        chest_bridge_npc = self.maps.get_npc(0x114, chest_bridge_npc_id)

        import copy
        from ..data.npc import NPC
        gate_npc = copy.deepcopy(chest_bridge_npc) # copy bottom left npc to drop towards end of bottom level
        gate_npc.x = 30
        gate_npc.y = 28
        gate_npc.direction = direction.RIGHT
        gate_npc.movement = NPC.NO_MOVE # instead of completely random, restrict it to bridge in entrance event

        gate_npc_id = self.maps.append_npc(0x114, gate_npc)

        # use extra space after recruiting gogo
        enable_npc_touch_events = 0xb8200
        space = Reserve(enable_npc_touch_events, 0xb824b, "zone eater enable npc touch events", field.NOP())
        space.copy_from(0xb7dc2, 0xb7dc7) # enable touch events for original npcs
        space.write(
            field.BranchIfEventBitSet(event_bit.character_recruited(self.character_gate()), "HIDE_GATE_NPC"),
            field.EnableTouchEvent(gate_npc_id),
            field.Return(),

            "HIDE_GATE_NPC",
            field.HideEntity(gate_npc_id),
            field.Return(),
        )

        space = Reserve(0xb7dc2, 0xb7dc7, "zone eater entrance event", field.NOP())
        space.write(
            field.Call(enable_npc_touch_events),
        )

    def character_mod(self, character):
        self.gogo_npc.sprite = character
        self.gogo_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xb81ce, 0xb81ff, "zone eater recruit gogo", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),

            field.DeleteEntity(self.gogo_npc_id),
            field.ClearEventBit(npc_bit.GOGO_ZONE_EATER),
            field.SetEventBit(event_bit.RECRUITED_GOGO_WOR),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        )

    def esper_item_mod(self, esper_item_instructions):
        space = Reserve(0xb81ce, 0xb81ff, "zone eater recruit gogo", field.NOP())
        space.write(
            esper_item_instructions,

            field.DeleteEntity(self.gogo_npc_id),
            field.ClearEventBit(npc_bit.GOGO_ZONE_EATER),
            field.SetEventBit(event_bit.RECRUITED_GOGO_WOR),
            field.FinishCheck(),
            field.Return(),
        )

    def esper_mod(self, esper):
        self.gogo_npc.sprite = 91
        self.gogo_npc.palette = 2
        self.gogo_npc.split_sprite = 1
        self.gogo_npc.direction = direction.UP

        self.esper_item_mod([
            field.DisableEntityCollision(self.gogo_npc_id),
            field.EntityAct(self.gogo_npc_id, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.DOWN, 1),
                field_entity.Hide(),
            ),

            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.gogo_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.gogo_npc.palette = self.characters.get_palette(self.gogo_npc.sprite)

        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
