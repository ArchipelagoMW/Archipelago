from ..event.event import *

class EightDragons(Event):
    def name(self):
        return "8 Dragons"

    def init_rewards(self):
        self.item_rewards = []
        for dragon_index in range(self.enemies.DRAGON_COUNT):
            self.item_rewards.append(self.add_reward(RewardType.ITEM))

    def init_event_bits(self, space):
        space.write(
            field.SetEventWord(event_word.DRAGONS_DEFEATED, 0),
        )

    def mod(self):
        from collections import namedtuple
        DragonData = namedtuple("DragonData", ["name", "event_bit", "battle_address", "countdown_address"])
        self.dragon_data = [
            DragonData("Ice Dragon", event_bit.DEFEATED_NARSHE_DRAGON, 0xc36df, 0xc36ec),
            DragonData("Storm Drgn", event_bit.DEFEATED_MT_ZOZO_DRAGON, 0xc43cd, 0xc43dc),
            DragonData("Dirt Drgn", event_bit.DEFEATED_OPERA_HOUSE_DRAGON, 0xab6df, 0xab6f3),
            DragonData("Gold Drgn", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_G, 0xc18f3, 0xc1900),
            DragonData("Skull Drgn", event_bit.DEFEATED_KEFKA_TOWER_DRAGON_S, 0xc1920, 0xc192d),
            DragonData("Blue Drgn", event_bit.DEFEATED_ANCIENT_CASTLE_DRAGON, 0xc205b, 0xc2068),
            DragonData("Red Dragon", event_bit.DEFEATED_PHOENIX_CAVE_DRAGON, 0xc2048, 0xc2055),
            DragonData("White Drgn", event_bit.DEFEATED_FANATICS_TOWER_DRAGON, 0xc558b, 0xc559d),
        ]

        self.dialog_mod()
        self.dragon_battles_mod()
        self.dragon_rewards_mod()
        self.white_dragon_reward_mod()

        for reward in self.item_rewards:
            self.log_reward(reward)

    def dialog_mod(self):
        # remove reference to crusader
        self.dialogs.set_text(1593, f"I found this in a 1000 year-old text:<line>8 dragons seal away awesome artifacts.<page>Defeat these dragons, and their power can be released…<end>")

        # remove the number of dragons
        self.dialogs.set_text(1505, "    Dragon Seal broken!!<end>")

    def dragon_battles_mod(self):
        call_size = 6 # invoke battle + call check game over
        for dragon in self.dragon_data:
            boss_pack_id = self.get_boss(dragon.name)

            space = Reserve(dragon.battle_address, dragon.battle_address + call_size,
                            f"8 dragons invoke battle {dragon.name.lower()}", field.NOP())
            space.write(
                field.InvokeBattle(boss_pack_id),
            )

    def dragon_rewards_mod(self):
        call_instr_size = 4
        for index, dragon in enumerate(self.dragon_data):
            reward = self.item_rewards[index]
            src = [
                field.AddItem(reward.id),
                field.Dialog(self.items.get_receive_dialog(reward.id)),
                field.SetEventBit(dragon.event_bit),
                field.FinishCheck(),
                field.Return(),
            ]
            space = Write(Bank.CC, src, f"8 dragons {dragon.name.lower()} receive reward")
            receive_reward = space.start_address

            space = Reserve(dragon.countdown_address, dragon.countdown_address + call_instr_size - 1,
                            f"8 dragons call receive reward {hex(receive_reward)}", field.NOP())
            space.write(
                field.Call(receive_reward),
            )

    def white_dragon_reward_mod(self):
        # white dragon does not drop its item reward
        # it is given after the battle (probably because it can be found on the veldt)
        # remove the reward after the battle in the fanatic's tower
        # and make pearl lance a white dragon drop for shuffled/random bosses
        space = Reserve(0xc5598, 0xc559c, "8 dragons pearl lance obtained after white dragon battle", field.NOP())

        pearl_lance_id = self.items.get_id("Pearl Lance")
        white_dragon_id = self.enemies.get_enemy("White Drgn")
        self.enemies.set_rare_drop(white_dragon_id, pearl_lance_id)
        self.enemies.set_common_drop(white_dragon_id, pearl_lance_id)
