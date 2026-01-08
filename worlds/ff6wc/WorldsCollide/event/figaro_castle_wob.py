from ..event.event import *

class FigaroCastleWOB(Event):
    def name(self):
        return "Figaro Castle WOB"

    def character_gate(self):
        return self.characters.EDGAR

    def init_rewards(self):
        if self.args.no_free_characters_espers:
            self.reward = self.add_reward(RewardType.ITEM)
        else:
            self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.MET_KEFKA_FIGARO_CASTLE),
            field.ClearEventBit(event_bit.NAMED_EDGAR),
            field.ClearEventBit(npc_bit.GUARDS_FIGARO_CASTLE),
        )

    def mod(self):
        self.edgar_npc_id = 0x10
        self.edgar_npc = self.maps.get_npc(0x03a, self.edgar_npc_id)

        if self.args.character_gating:
            self.add_gating_condition()

        self.guard_mod()
        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.shop_mod()

        self.log_reward(self.reward)

    def add_gating_condition(self):
        # add entrance event to hide edgar npc if gate character not found
        src = [
            field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
            field.HideEntity(self.edgar_npc_id),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro castle wob character gate")
        entrance_event = space.start_address

        self.maps.set_entrance_event(0x03a, entrance_event - EVENT_CODE_START)

    def guard_mod(self):
        # allow guard to move randomly before finishing throne check
        space = Reserve(0xaeab5, 0xaeaba, "figaro castle prison guard named edgar check", field.NOP())

    def character_mod(self, character):
        self.edgar_npc.sprite = character
        self.edgar_npc.palette = self.characters.get_palette(character)

        src = [
            field.SetEventBit(event_bit.NAMED_EDGAR),
            field.ClearEventBit(npc_bit.EDGAR_FIGARO_CASTLE_THRONE),
            field.HideEntity(self.edgar_npc_id),

            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro castle wob character reward")
        recruit_character = space.start_address

        space = Reserve(0xa6623, 0xa6628, "figaro castle wob call recruit character")
        space.write(
            field.Branch(recruit_character),
        )

    def esper_item_mod(self, esper_item_instructions):
        self.edgar_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.edgar_npc.palette = self.characters.get_palette(self.edgar_npc.sprite)

        src = [
            field.FadeOutScreen(),
            field.WaitForFade(),

            field.SetEventBit(event_bit.NAMED_EDGAR),
            field.ClearEventBit(npc_bit.EDGAR_FIGARO_CASTLE_THRONE),
            field.HideEntity(self.edgar_npc_id),

            field.FadeInScreen(),
            esper_item_instructions,
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro castle wob esper/item reward")
        add_esper_item = space.start_address

        space = Reserve(0xa6623, 0xa6628, "figaro castle wob call recruit character")
        space.write(
            field.Branch(add_esper_item),
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

    def shop_mod(self):
        # do not changes shops after defeating kefka in narshe, always use the ones after kefka
        space = Reserve(0xa67b1, 0xa67b6, "figaro castle wob left shop defeated kefka narshe branch")
        space.add_label("INVOKE_SHOP", 0xa67ba)
        space.write(
            field.Branch("INVOKE_SHOP"),
        )
        space = Reserve(0xa67cf, 0xa67d4, "figaro castle wob right shop defeated kefka narshe branch")
        space.add_label("INVOKE_SHOP", 0xa67d8)
        space.write(
            field.Branch("INVOKE_SHOP"),
        )
