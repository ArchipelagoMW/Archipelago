from ..event.event import *
from ..data.item_names import id_name
from ..ff6wcutils.truncated_discrete_distribution import truncated_discrete_distribution

class MoblizWOB(Event):
    def name(self):
        return "Mobliz WOB"

    def mod(self):
        self.item_reward = self.items.get_random()
        self.item_reward_name = id_name[self.item_reward]
        self.log_change("Tintinabar", self.item_reward_name)

        self.prices = []
        for _ in range(5):
            self.prices.append(truncated_discrete_distribution(500, 1000, 1, 2 ** 16 - 1))
        self.log_change("", ', '.join([str(x) for x in self.prices]))

        self.set_postal_prices()
        self.finish_injured_lad()
        self.hide_duane_and_dog()

    def set_postal_prices(self):
        self.dialogs.set_text(765, f"Postage to Maranda is {self.prices[0]} GP.<page>Gonna send a letter for that soldier, right?<line><choice> (Send it)<line><choice> (Forget it)<end>")
        self.dialogs.set_text(769, f"For {self.prices[1]} GP you can send a record.<line><choice> (Send it)<line><choice> (Forget it)<end>")
        self.dialogs.set_text(771, f"For {self.prices[2]} GP you can send Tonic.<line><choice> (Send it)<line><choice> (Forget it)<end>")
        self.dialogs.set_text(773, f"For {self.prices[3]} GP you can send a letter.<line><choice> (Send it)<line><choice> (Forget it)<end>")
        self.dialogs.set_text(775, f"For {self.prices[4]} GP you can send a book.<line><choice> (Send it)<line><choice> (Forget it)<end>")

        take_gp_addresses = [0xc67e2, 0xc6803, 0xc6824, 0xc6845, 0xc6866]
        for index, address in enumerate(take_gp_addresses):
            space = Reserve(address, address + 2, f"mobliz wob injured lad remove {self.prices[index]} gp", field.NOP())
            space.write(
                field.RemoveGP(self.prices[index]),
            )

    def finish_injured_lad(self):
        received_text = self.dialogs.get_centered(f"Received “{self.item_reward_name}.”")
        self.dialogs.set_text(782, f"I heard…<line>In my name you send Lola many things…<page>I wish to thank you.<line>Please accept this as a token of my appreciation.<page><line>{received_text}<end>")

        src = [
            field.AddItem(self.item_reward, sound_effect = False),
            field.SetEventBit(event_bit.HELPED_INJURED_LAD),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "mobliz wob injured lad reward, check objectives")
        reward_check_objectives = space.start_address

        space = Reserve(0xc6883, 0xc6886, "mobliz wob injured lad item, event bit", field.NOP())
        space.write(
            field.Call(reward_check_objectives),
        )

    def hide_duane_and_dog(self):
        dog_id = 0x13
        duane_id = 0x14
        src = [
            field.Call(0xc5136), # music
            field.ReturnIfEventBitSet(event_bit.IN_WOR),

            field.HideEntity(dog_id),
            field.HideEntity(duane_id),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "mobliz wob hide duane/dog")
        hide_npcs = space.start_address

        space = Reserve(0xc50ea, 0xc50ed, "mobliz wob entrance event music", field.NOP())
        space.write(
            field.Call(hide_npcs),
        )
