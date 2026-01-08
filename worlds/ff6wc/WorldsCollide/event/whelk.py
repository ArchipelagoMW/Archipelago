from ..event.event import *

class Whelk(Event):
    def name(self):
        return "Whelk"

    def character_gate(self):
        return self.characters.TERRA

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.VICKS_BROKE_WHELK_GATE),
        )

    def mod(self):
        if self.reward.type == RewardType.NONE:
            return

        self.dialog_mod()
        self.entrance_event_mod()
        self.cleanup_mod()
        self.whelk_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xc9f4d, 0xc9f4f, "narshe mines we won't hand over the esper", field.NOP())
        space = Reserve(0xc9f58, 0xc9f5a, "narshe mines whelk get them", field.NOP())

    def entrance_event_mod(self):
        if self.args.character_gating:
            # use the entrance event from the beginning mines map (where whelk originally is)
            space = Reserve(0xc9ef2, 0xc9ef7, "narshe mines entrance event gate check")
            space.write(
                field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
            )
            entrance_event = space.start_address

            space = Reserve(0xc9ef9, 0xc9efa, "narshe mines entrance event change gate x/y")
            space.write(111, 30)

            # NOTE: this part of the map needs to be changed too
            #       wrapping around for layers? the real y position is 30 and the map ends at 64
            space = Reserve(0xc9f0a, 0xc9f0b, "narshe mines entrance event change gate x/y")
            space.write(111, 94)

            space = Reserve(0xc9f1a, 0xc9f29, "narshe mines entrance event set magitek armor", field.Return())
            self.maps.set_entrance_event(0x02b, entrance_event - EVENT_CODE_START)
        else:
            space = Reserve(0xc9ef2, 0xc9f29, "narshe mines beginning entrance event", field.Return())

    def cleanup_mod(self):
        # delete events/npc from unused map (mines during magitek event in beginning)
        self.maps.delete_event(0x29, 42, 9)  # break gate
        self.maps.delete_event(0x29, 38, 34) # exit back to narshe during magitek beginning
        self.maps.delete_event(0x29, 42, 5)  # whelk guard trigger
        self.maps.delete_event(0x29, 33, 22) # save point
        self.maps.remove_npc(0x29, 0x10)     # whelk guard

    def add_npc(self, sprite, palette):
        # add whelk guard npc to map 0x2b
        from ..data.npc import NPC
        new_npc = NPC()
        new_npc.x = 112
        new_npc.y = 29
        new_npc.sprite = sprite
        new_npc.palette = palette
        new_npc.direction = direction.UP
        new_npc.speed = 3
        new_npc.event_byte = 0x60
        new_npc.event_bit = 4
        return self.maps.append_npc(0x2b, new_npc)

    def add_guard_npc(self, sprite = 52, palette = 0):
        guard_npc_id = self.add_npc(sprite, palette)

        # change guard npc id to correct new npc id
        space = Reserve(0xc9f3e, 0xc9f3e, "whelk guard npc id")
        space.write(guard_npc_id)
        space = Reserve(0xc9f40, 0xc9f40, "whelk guard npc id")
        space.write(guard_npc_id)
        space = Reserve(0xc9f42, 0xc9f42, "whelk guard npc id")
        space.write(guard_npc_id)
        space = Reserve(0xc9f51, 0xc9f51, "whelk guard npc id")
        space.write(guard_npc_id)
        space = Reserve(0xc9f56, 0xc9f56, "whelk guard npc id")
        space.write(guard_npc_id)

        # add guard calls whelk event to map 0x2b
        from ..data.map_event import MapEvent
        for x in range(3):
            new_event = MapEvent()
            new_event.x = 111 + x
            new_event.y = 30
            new_event.event_address = 0xc9f37 - EVENT_CODE_START # guard calls whelk event

            self.maps.add_event(0x2b, new_event)

    def whelk_battle_mod(self):
        boss_pack_id = self.get_boss("Whelk")
        battle_background = 0x09 # mines wob background

        space = Reserve(0xc9f5d, 0xc9f63, "narshe mines invoke battle whelk", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id, battle_background),
        )

        # wedge/vicks whelk battle animation
        space = Reserve(0x109e77, 0x109ea8, "wedge/vicks whelk battle animation")
        space.clear(0xfd)
        space.write(0xff)

    def after_whelk_battle_mod(self, instructions):
        space = Reserve(0xc9f64, 0xc9f80, "narshe mines terra/vicks/wedge at esper scene", field.NOP())
        space.write(
            field.SetEventBit(event_bit.DEFEATED_WHELK),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.EnableWalkingAnimation(),
            ),
            instructions,
            field.FinishCheck(),
            field.Return(),
        )

    def character_mod(self, character):
        self.add_guard_npc(sprite = character, palette = self.characters.get_palette(character))

        self.after_whelk_battle_mod([
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
        ])

    def esper_item_mod(self, esper_item_instructions):
        self.add_guard_npc()

        self.after_whelk_battle_mod([
            field.FadeInScreen(),
            field.WaitForFade(),
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
