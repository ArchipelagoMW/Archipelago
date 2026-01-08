from ..event.event import *

# 0xcb4ecc
#   if in wor go to 0xcb55b0
#   else 50% chance go to 0xcb501d
#   else  cherub down (10,000)
# 0xcb501d
#   50% chance go to 0xcb5197
#   else talking chocobo
# 0xcb5197
#   if bought golem go to 0xcb5312 # (crane requirement removed below)
#   else 50% chance go to 0xcb5312
#   else golem (20,000)
# 0xcb5312
#   if bought zoneseek go to 0xcb5460 # (crane requirement removed below)
#   else 50% chance go to 0xcb5460
#   else zoneseek (10,000)
# 0xcb5460
#   cure ring (20,000)
# 0xcb55b0
#   50% chance go to 0xcb570c
#   if bought hero ring go to 0xcb570c
#   else hero ring (50,000)
# 0xcb570c
#   50% chance go to 0xcb58fa
#   else 1/1200 airship
# 0xcb58fa
#   if bought golem go to 0xcb5a39 # (crane requirement removed below)
#   else 50% chance go to 0xcb5a39
#   else golem (20,000)
# 0xcb5a39
#   if bought zoneseek go to 0xcb5b85
#   else 50% chance go to 0xcb5b85
#   else zoneseek (10,000)
# 0xcb5b85
#   if bought zephyr cape go to 0xcb5cad
#   else 50% chance go to 0xcb5cad
#   else zephyr cape (10,000)
# 0xcb5cad
#   imp robot

class AuctionHouse(Event):
    def name(self):
        return "Auction House"

    def init_rewards(self):
        # ignore the -nfp and -ame flags in multi-world as they don't make sense in this context
        self.reward1 = self.add_reward(RewardType.ESPER | RewardType.ITEM)
        self.reward2 = self.add_reward(RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.requirements_mod()

        if self.args.auction_no_chocobo_airship:
            self.no_chocobo_airship_mod()

        self.start_auction = 0xb4e5e
        if self.args.auction_door_esper_hint:
            self.door_npc_mod()

        self.reward1_start_price = 500
        self.reward2_start_price = 1000
        self.cherub_down_start_price = 500
        self.cure_ring_start_price = 1500
        self.hero_ring_start_price = 3000
        self.zephyr_cape_start_price = 3000

        # overwriting some dialog from zozo ramuh scene to fit new auctioneer dialog
        self.reward1_announce_dialog_id = 1111     # previously 2728
        self.reward2_announce_dialog_id = 1115     # previously 2729
        self.cherub_down_announce_dialog_id = 1117 # previously 2629
        self.cure_ring_announce_dialog_id = 1118   # previously 2631
        self.hero_ring_announce_dialog_id = 1119   # previously 2633
        self.zephyr_cape_announce_dialog_id = 1121 # previously 2635

        self.chest_dialog_id = 2628 # here's a splendid chest, inside is...

        self.show_chest = 0xb4eb1
        self.open_chest = 0xb4eba
        self.hide_chest = 0xb4ec3

        if self.reward1.type == RewardType.ESPER:
            self.esper1_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ITEM:
            self.item1_mod(self.reward1.id)

        if self.reward2.type == RewardType.ESPER:
            self.esper2_mod(self.reward2.id)
        elif self.reward2.type == RewardType.ITEM:
            self.item2_mod(self.reward2.id)

        self.cherub_down_item = self.items.get_id("Cherub Down")
        self.cure_ring_item = self.items.get_id("Cure Ring")
        self.hero_ring_item = self.items.get_id("Hero Ring")
        self.zephyr_cape_item = self.items.get_id("Zephyr Cape")

        if self.args.auction_random_items:
            self.cherub_down_item = self.items.get_random()
            self.cure_ring_item = self.items.get_random()
            self.hero_ring_item = self.items.get_random()
            self.zephyr_cape_item = self.items.get_random()

            self.log_change("Cherub Down", f"{self.items.get_name(self.cherub_down_item):<12} (10,000, WOB, multiple)")
            self.log_change("Cure Ring", f"{self.items.get_name(self.cure_ring_item):<12} (20,000, WOB, multiple)")
            self.log_change("Hero Ring", f"{self.items.get_name(self.hero_ring_item):<12} (50,000, WOR, single)")
            self.log_change("Zephyr Cape", f"{self.items.get_name(self.zephyr_cape_item):<12} (10,000, WOR, single)")

        self.cherub_down_mod(self.cherub_down_item)
        self.cure_ring_mod(self.cure_ring_item)
        self.hero_ring_mod(self.hero_ring_item)
        self.zephyr_cape_mod(self.zephyr_cape_item)

        self.log_reward(self.reward1, suffix = " (10,000)") # zoneseek
        self.log_reward(self.reward2, suffix = " (20,000)") # golem

    def get_reward_announce_dialog(self, name, start_price, item):
        if item:
            reward_dialog = '“' + name + '”!' #https://discord.com/channels/666661907628949504/666811452350398493/1085018091844554832
        else:
            reward_dialog = 'The Magicite, “' + name + '”!'

        # keep auctioneer dialog somewhat centered with new esper/item names
        # looks like about 32 characters on a line (32 is just an estimate, it is not monospace)
        line_length = 32
        space_count = (line_length - len(reward_dialog)) // 2

        return '<line>' + (' ' * space_count) + reward_dialog + '<page><line>Who\'ll give me ' + str(start_price) + ' GP?<end>'

    def announce_dialog_mod(self, start_addr, end_addr, space_description, dialog_id):
        space = Reserve(start_addr, end_addr, space_description, field.NOP())
        space.write(
            field.Dialog(dialog_id),
        )

    def reward1_announce_dialog_mod(self, reward_name, item):
        announce_dialog = self.get_reward_announce_dialog(reward_name, self.reward1_start_price, item)
        self.dialogs.set_text(self.reward1_announce_dialog_id, announce_dialog)

        self.announce_dialog_mod(0xb5339, 0xb533b, "update announce reward1 dialog in auction", self.reward1_announce_dialog_id)
        self.announce_dialog_mod(0xb5a5e, 0xb5a60, "update announce reward1 dialog in auction in wor", self.reward1_announce_dialog_id)

    def reward2_announce_dialog_mod(self, reward_name, item):
        announce_dialog = self.get_reward_announce_dialog(reward_name, self.reward2_start_price, item)
        self.dialogs.set_text(self.reward2_announce_dialog_id, announce_dialog)

        self.announce_dialog_mod(0xb51be, 0xb51c0, "update announce reward2 dialog in auction", self.reward2_announce_dialog_id)
        self.announce_dialog_mod(0xb5921, 0xb5923, "update announce reward2 dialog in auction in wor", self.reward2_announce_dialog_id)

    def show_chest_mod(self, start_addr, end_addr, space_description):
        space = Reserve(start_addr, end_addr, space_description, field.NOP())
        space.write(
            field.Call(self.show_chest),
            field.Pause(1.50),
            field.Dialog(self.chest_dialog_id),
            field.Call(self.open_chest),
        )

    def hide_chest_mod(self, start_addr, end_addr, space_description):
        space = Reserve(start_addr, end_addr, space_description, field.NOP())
        space.write(
            field.Call(self.hide_chest),
        )

    def chest1_mod(self):
        self.show_chest_mod(0xb532c, 0xb5338, "show chest1 in auction")
        self.show_chest_mod(0xb5a51, 0xb5a5d, "show chest1 in auction in wor")

        self.hide_chest_mod(0xb53e1, 0xb53e5, "hide chest1 in auction after losing")
        self.hide_chest_mod(0xb5b06, 0xb5b0a, "hide chest1 in auction after losing in wor")
        self.hide_chest_mod(0xb544b, 0xb544f, "hide chest1 in auction after winning")
        self.hide_chest_mod(0xb5b70, 0xb5b74, "hide chest1 in auction after winning in wor")

    def chest2_mod(self):
        self.show_chest_mod(0xb51b1, 0xb51bd, "show chest2 in auction")
        self.show_chest_mod(0xb5914, 0xb5920, "show chest2 in auction in wor")

        self.hide_chest_mod(0xb5250, 0xb5254, "hide chest2 in auction after losing")
        self.hide_chest_mod(0xb59b3, 0xb59b7, "hide chest2 in auction after losing in wor")
        self.hide_chest_mod(0xb52c2, 0xb52c6, "hide chest2 in auction after winning")
        self.hide_chest_mod(0xb5a25, 0xb5a29, "hide chest2 in auction after winning in wor")

    def receive_esper_mod(self, start_addr, end_addr, space_description, esper, event_bit_to_set):
        src = [
            field.AddEsper(esper, sound_effect = False),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.SetEventBit(event_bit.WON_AN_AUCTION),
            field.SetEventBit(event_bit_to_set), # while this is also called right after this in the vanilla event code, it's required here to cause the check objective to fire
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, space_description)
        receive_esper = space.start_address

        space = Reserve(start_addr, end_addr, "call " + space_description, field.NOP())
        space.write(
            field.Call(receive_esper),
        )

    def receive_check_item_mod(self, start_addr, end_addr, space_description, item, event_bit_to_set):
        src = [
            field.AddItem(item, sound_effect = False),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.SetEventBit(event_bit.WON_AN_AUCTION),
            field.SetEventBit(event_bit_to_set), # while this is also called right after this in the vanilla event code, it's required here to cause the check objective to fire
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, space_description)
        receive_item = space.start_address

        space = Reserve(start_addr, end_addr, space_description, field.NOP())
        space.write(
            field.Call(receive_item),
        )

    def receive_item_mod(self, start_addr, end_addr, space_description, item):
        src = [
            field.AddItem(item, sound_effect = False),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.SetEventBit(event_bit.WON_AN_AUCTION),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, space_description)
        receive_item = space.start_address

        space = Reserve(start_addr, end_addr, space_description, field.NOP())
        space.write(
            field.Call(receive_item),
        )

    def esper1_mod(self, esper):
        esper_name = self.espers.get_name(esper)

        # update esper announced dialog
        self.reward1_announce_dialog_mod(esper_name, False)

        # update esper received and dialog
        self.receive_esper_mod(0xb5452, 0xb5456, "update esper1 received in auction", esper, event_bit.AUCTION_BOUGHT_ESPER1)
        self.receive_esper_mod(0xb5b77, 0xb5b7b, "update esper1 received in auction in wor", esper, event_bit.AUCTION_BOUGHT_ESPER1)

    def item1_mod(self, item):
        item_name = self.items.get_name(item)

        # change magicite to a chest
        self.chest1_mod()

        # update item announced dialog
        self.reward1_announce_dialog_mod(item_name, True)

        # update item received and dialog
        self.receive_check_item_mod(0xb5452, 0xb5456, "update item1 received in auction", item, event_bit.AUCTION_BOUGHT_ESPER1)
        self.receive_check_item_mod(0xb5b77, 0xb5b7b, "update item1 received in auction in wor", item, event_bit.AUCTION_BOUGHT_ESPER1)

    def esper2_mod(self, esper):
        esper_name = self.espers.get_name(esper)

        # update esper announced dialog
        self.reward2_announce_dialog_mod(esper_name, False)

        # update esper received and dialog
        self.receive_esper_mod(0xb52c9, 0xb52cd, "update esper2 received in auction", esper, event_bit.AUCTION_BOUGHT_ESPER2)
        self.receive_esper_mod(0xb5a2c, 0xb5a30, "update esper2 received in auction in wor", esper, event_bit.AUCTION_BOUGHT_ESPER2)

    def item2_mod(self, item):
        item_name = self.items.get_name(item)

        # change magicite to a chest
        self.chest2_mod()

        # update item announced dialog
        self.reward2_announce_dialog_mod(item_name, True)

        # update item received and dialog
        self.receive_check_item_mod(0xb52c9, 0xb52cd, "update item2 received in auction", item, event_bit.AUCTION_BOUGHT_ESPER2)
        self.receive_check_item_mod(0xb5a2c, 0xb5a30, "update item2 received in auction in wor", item, event_bit.AUCTION_BOUGHT_ESPER2)

    def normal_item_set_announce_dialog(self, new_item_id, start_price, announce_dialog_id):
        item_name = self.items.get_name(new_item_id)
        self.items.add_receive_dialog(new_item_id)

        announce_dialog = self.get_reward_announce_dialog(item_name, start_price, True)
        self.dialogs.set_text(announce_dialog_id, announce_dialog)

    def cherub_down_mod(self, item):
        self.normal_item_set_announce_dialog(item, self.cherub_down_start_price, self.cherub_down_announce_dialog_id)
        self.announce_dialog_mod(0xb4ef1, 0xb4ef3, "update announce cherub down dialog in auction", self.cherub_down_announce_dialog_id)
        self.receive_item_mod(0xb5012, 0xb5016, "update cherub down received in auction", item)

    def cure_ring_mod(self, item):
        self.normal_item_set_announce_dialog(item, self.cure_ring_start_price, self.cure_ring_announce_dialog_id)
        self.announce_dialog_mod(0xb547b, 0xb547d, "update announce cure ring dialog in auction", self.cure_ring_announce_dialog_id)
        self.receive_item_mod(0xb55a4, 0xb55a8, "update cure ring received in auction", item)

    def hero_ring_mod(self, item):
        self.normal_item_set_announce_dialog(item, self.hero_ring_start_price, self.hero_ring_announce_dialog_id)
        self.announce_dialog_mod(0xb55d5, 0xb55d7, "update announce hero ring dialog in auction", self.hero_ring_announce_dialog_id)
        self.receive_item_mod(0xb56ff, 0xb5703, "update hero ring received in auction", item)

    def zephyr_cape_mod(self, item):
        self.normal_item_set_announce_dialog(item, self.zephyr_cape_start_price, self.zephyr_cape_announce_dialog_id)
        self.announce_dialog_mod(0xb5bad, 0xb5baf, "update announce zephyr cape dialog in auction", self.zephyr_cape_announce_dialog_id)
        self.receive_item_mod(0xb5c9f, 0xb5ca3, "update zephyr cape received in auction", item)

    def door_npc_mod(self):
        normal_door_npc_dialog_id = 2625
        esper_door_npc_dialog_id = 2621     # overwrite some dialog from recruiting mog in wor

        self.dialogs.set_text(esper_door_npc_dialog_id, "See anything you want?<line>Glowing stones still available!<page><choice> (Bid on items!)<line><choice> (Another time.)<end>")

        src = []
        if self.reward1.type == RewardType.ESPER:
            src += [
                field.BranchIfEventBitClear(event_bit.AUCTION_BOUGHT_ESPER1, "ESPERS_AVAILABLE"),
            ]
        if self.reward2.type == RewardType.ESPER:
            src += [
                field.BranchIfEventBitClear(event_bit.AUCTION_BOUGHT_ESPER2, "ESPERS_AVAILABLE"),
            ]
        src += [
            "NO_ESPERS_AVAILABLE",
            field.DialogBranch(normal_door_npc_dialog_id, dest1 = self.start_auction, dest2 = field.RETURN),

            "ESPERS_AVAILABLE",
            field.DialogBranch(esper_door_npc_dialog_id,
                               dest1 = self.start_auction,
                               dest2 = field.RETURN),
        ]
        space = Write(Bank.CB, src, "auction house door npc hint")
        door_npc_hint = space.start_address

        space = Reserve(0xb4e53, 0xb4e5c, "auction house door npc original dialog", field.NOP())
        space.write(
            field.Call(door_npc_hint),
        )

    def no_chocobo_airship_mod(self):
        space = Reserve(0xb501d, 0xb5196, "talking chocobo auction", field.NOP())
        space.write(
            field.Branch(0xb5197),
            field.Return(),
        )

        space = Reserve(0xb570c, 0xb58f9, "1/1200 airship auction", field.NOP())
        space.write(
            field.Branch(0xb58fa),
            field.Return(),
        )

    def requirements_mod(self):
        # remove cranes killed after magitek facility requirements
        space = Reserve(0xb4e4d, 0xb4e52, "remove auction house magitek facility cranes killed requirement", field.NOP())

        space = Reserve(0xb5197, 0xb519e, "check if reward2 bought at auction house", field.NOP())
        space.write(
            field.BranchIfEventBitSet(event_bit.AUCTION_BOUGHT_ESPER2, 0xb5312),
        )

        space = Reserve(0xb5312, 0xb5319, "check if reward1 bought at auction house", field.NOP())
        space.write(
            field.BranchIfEventBitSet(event_bit.AUCTION_BOUGHT_ESPER1, 0xb5460),
        )

        space = Reserve(0xb58fa, 0xb5901, "check if reward2 bought at auction house in wor", field.NOP())
        space.write(
            field.BranchIfEventBitSet(event_bit.AUCTION_BOUGHT_ESPER2, 0xb5a39),
        )

        # NOTE: check if reward1 bought at auction house in wor (0xb5a39) does not have crane requirement so no need to mod
