from ..event.event import *

class Tritoch(Event):
    def name(self):
        return "Tritoch"

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.dialog_mod()
        self.tritoch_battle_mod()

        if self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        elif self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xc375e, 0xc3760, "tritoch you HUMANS freed me", field.NOP())

    def tritoch_battle_mod(self):
        boss_pack_id = self.get_boss("Tritoch")

        space = Reserve(0xc373a, 0xc3740, "tritoch invoke battle", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def esper_item_mod(self, add_reward_instructions, reward_dialog_id):
        space = Reserve(0xc3782, 0xc3784, "tritoch receive esper dialog", field.NOP())
        space.write(
            field.Dialog(reward_dialog_id),
        )

        src = [
            add_reward_instructions,
            field.SetEventBit(event_bit.GOT_TRITOCH),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "tritoch receive reward finish check")
        receive_reward = space.start_address

        space = Reserve(0xc37a6, 0xc37a9, "tritoch add esper", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

    def esper_mod(self, esper):
        add_esper_instructions = field.AddEsper(esper, sound_effect = False)
        receive_esper_dialog_id = self.espers.get_receive_esper_dialog(esper)

        self.esper_item_mod(add_esper_instructions, receive_esper_dialog_id)

    def item_mod(self, item):
        magicite_npc_id = 0x11
        magicite_npc = self.maps.get_npc(0x23, magicite_npc_id)
        magicite_npc.sprite = 106
        magicite_npc.palette = 6
        magicite_npc.split_sprite = 1
        magicite_npc.direction = direction.DOWN

        space = Reserve(0xc3779, 0xc377e, "tritoch esper sound effect and flash screen white", field.NOP())
        space.write(
            field.PlaySoundEffect(141),
        )

        space = Reserve(0xc3781, 0xc3781, "tritoch pause before receive dialog", field.NOP())

        add_item_instructions = field.AddItem(item, sound_effect = False)
        receive_item_dialog_id = self.items.get_receive_dialog(item)

        self.esper_item_mod(add_item_instructions, receive_item_dialog_id)

    def character_mod(self, character):
        magicite_npc_id = 0x11
        magicite_npc = self.maps.get_npc(0x23, magicite_npc_id)
        magicite_npc.sprite = character
        magicite_npc.palette = self.characters.get_palette(character)
        magicite_npc.split_sprite = 0
        magicite_npc.direction = direction.DOWN
        # clear unknown bits that cause a glitchy sprite if reward is a character (Archipelago)
        magicite_npc.unknown1 = 0
        magicite_npc.unknown2 = 0

        space = Reserve(0xc3779, 0xc377e, "tritoch esper sound effect and flash screen white", field.NOP())
        space.write(
            field.PlaySoundEffect(141),
        )

        space = Reserve(0xc3781, 0xc3781, "tritoch pause before receive dialog", field.NOP())
        # Don't write out a dialogue for character recruit
        space = Reserve(0xc3782, 0xc3784, "tritoch receive esper dialog", field.NOP())
        # need to set the event bit BEFORE we recruit character so the map loads in the proper state (Umaro Hole vs. Tritoch Ice)
        src = [
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.SetEventBit(event_bit.GOT_TRITOCH),
            field.RecruitAndSelectParty(character),
            field.FreeScreen(),
            field.LoadMap(0x23, direction.DOWN, default_music = True,
                          x = 9, y = 13, fade_in = True, entrance_event = True),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "tritoch receive reward finish check")
        receive_reward = space.start_address

        space = Reserve(0xc37a6, 0xc37a9, "tritoch add reward", field.NOP())
        space.write(
            field.Call(receive_reward),
        )