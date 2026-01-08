from ..event.event import *

class Tzen(Event):
    def name(self):
        return "Tzen"

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.ESPER_SELLER_TZEN),
        )

    def mod(self):
        from random import randint
        self.wob_price = randint(1, field.RemoveGP.MAX)
        self.wor_price = randint(1, field.RemoveGP.MAX)

        if self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward, suffix = f" ({self.wob_price:,} WOB, {self.wor_price:,} WOR)")

    def esper_item_mod(self, wob_dialog, reward_instructions):
        # update dialog npc says
        wor_dialog = f"If you want it, just give me {self.wor_price} GP.<line><choice> Yes<line><choice> No<end>"

        wob_dialog_id = 1569
        wor_dialog_id = 1570

        self.dialogs.set_text(wob_dialog_id, wob_dialog)
        self.dialogs.set_text(wor_dialog_id, wor_dialog)

        # update how much gp taken from party
        space = Reserve(0xc5e00, 0xc5e01, "tzen esper take gp wob")
        space.write(self.wob_price.to_bytes(2, 'little'))

        space = Reserve(0xc5e14, 0xc5e15, "tzen esper take gp wor")
        space.write(self.wor_price.to_bytes(2, 'little'))

        src = [
            reward_instructions,

            field.SetEventBit(event_bit.BOUGHT_ESPER_TZEN),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "tzen receive reward")
        receive_reward = space.start_address

        space = Reserve(0xc5e08, 0xc5e10, "tzen call receive reward wob", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

        space = Reserve(0xc5e1c, 0xc5e24, "tzen call receive reward wor", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

    def esper_mod(self, esper):
        wob_dialog = f"For {self.wob_price} GP this glowing stone\'s yours.<line><choice> Yes<line><choice> No<end>"
        self.esper_item_mod(wob_dialog, [
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        wob_dialog = f"For {self.wob_price} GP this is yours.<line><choice> Yes<line><choice> No<end>"
        self.esper_item_mod(wob_dialog, [
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])
