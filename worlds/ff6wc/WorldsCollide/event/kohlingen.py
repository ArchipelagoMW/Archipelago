from ..event.event import *

# TODO use setzer npc instead of shadow's
#      for character reward show the animations setzer does in wor before daryl's tomb

class Kohlingen(Event):
    def name(self):
        return "Kohlingen"

    def character_gate(self):
        return self.characters.SETZER

    def init_rewards(self):
        if self.args.no_free_characters_espers:
            self.reward = self.add_reward(RewardType.ITEM)
        else:
            self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.KOHLINGEN_WOR_CITIZENS),
        )

    def mod(self):
        self.shadow_npc_id = 0x10
        self.shadow_npc = self.maps.get_npc(0x0bf, self.shadow_npc_id)
        self.interceptor_npc_id = 0x11

        self.rachel_house_mod()
        self.inn_entrance_event_mod()
        self.inn_sleep_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def rachel_house_mod(self):
        self.maps.delete_event(0x0c5, 39, 17) # locke/rachel flashback 0xc6a2e

    def inn_entrance_event_mod(self):
        space = Reserve(0xc6f4b, 0xc6f65, "kohlingen inn entrance event", field.NOP())
        space.add_label("THE_DAY_AFTER", 0xc6f7b)
        space.add_label("KIDS_RUNNING_THROUGH_THE_CITY", 0xc3b0e)
        space.write(
            field.HideEntity(self.interceptor_npc_id),
        )
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitSet(event_bit.character_recruited(self.character_gate()), "AFTER_HIDE_SHADOW"),
                field.HideEntity(self.shadow_npc_id),
                "AFTER_HIDE_SHADOW",
            )
        space.write(
            field.BranchIfEventBitSet(event_bit.IN_WOR, "THE_DAY_AFTER"),
            field.Branch("KIDS_RUNNING_THROUGH_THE_CITY"),
        )

    def inn_sleep_mod(self):
        src = [
            Read(0xc69e8, 0xc69ed), # copy load kohlingen inn map
            field.HideEntity(self.interceptor_npc_id),
        ]
        if self.args.character_gating:
            src += [
                field.BranchIfEventBitSet(event_bit.character_recruited(self.character_gate()), "AFTER_HIDE_SHADOW"),
                field.HideEntity(self.shadow_npc_id),
                "AFTER_HIDE_SHADOW",
            ]
        src += [
            field.Return(),
        ]
        space = Write(Bank.CC, src, "kohlingen inn sleep mod")
        load_inn_map = space.start_address

        space = Reserve(0xc69e8, 0xc69ed, "kohlingen inn call load inn map", field.NOP())
        space.write(
            field.Call(load_inn_map),
        )

    def character_mod(self, character):
        self.shadow_npc.sprite = character
        self.shadow_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xc6f84, 0xc6f8b, "kohlingen talk to shadow", field.NOP())
        space.add_label("RECEIVE_REWARD", 0xc704f)
        space.write(
            field.Branch("RECEIVE_REWARD"),
        )

        space = Reserve(0xc7058, 0xc7072, "kohlingen recruit shadow", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
            field.Branch(space.end_address + 1), # skip nops
        )

    def esper_item_mod(self, esper_item_instructions):
        self.shadow_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.shadow_npc.palette = self.characters.get_palette(self.shadow_npc.sprite)

        space = Reserve(0xc6f84, 0xc6f8b, "kohlingen talk to shadow", field.NOP())
        space.add_label("RECEIVE_REWARD", 0xc704f)
        space.write(
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.Branch("RECEIVE_REWARD"),
        )

        space = Reserve(0xc7058, 0xc7072, "kohlingen recruit shadow", field.NOP())
        space.write(
            field.FadeInScreen(),
            esper_item_instructions,
            field.Branch(space.end_address + 1), # skip nops
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

    def finish_check_mod(self):
        src = [
            field.ClearEventBit(npc_bit.SHADOW_INTERCEPTOR_KOHLINGEN_INN),
            field.SetEventBit(event_bit.RECRUITED_SHADOW_KOHLINGEN),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "kohlingen finish check")
        finish_check = space.start_address

        space = Reserve(0xc7073, 0xc7076, "kohlingen clear npc bit, set finished bit", field.NOP())
        space.write(
            field.Call(finish_check),
        )
