from ..event.event import *
from ..music.song_utils import get_character_theme

class GauFatherHouse(Event):
    def name(self):
        return "Gau Father House"

    def character_gate(self):
        return self.characters.SHADOW

    def init_rewards(self):
        if self.args.no_free_characters_espers:
            self.reward = self.add_reward(RewardType.ITEM)
        else:
            self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.shadow_npc_id = 0x10
        self.shadow_npc = self.maps.get_npc(0x073, self.shadow_npc_id)
        self.interceptor_npc_id = 0x11
        self.merchant_npc_id = 0x12
        self.merchant_npc = self.maps.get_npc(0x073, self.merchant_npc_id)

        self.merchant_mod()
        self.entrance_event_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def merchant_mod(self):
        # first time speak with merchant he has extra dialog, always skip that
        self.merchant_npc.set_event_address(0xb0ba1)

    def entrance_event_mod(self):
        # only show shadow and play shadows theme if haven't received reward yet or it is not available yet
        # normally, it plays shadow theme unless shadow is in party or have already been locked in phantom train
        space = Reserve(0xb0b6b, 0xb0b77, "gau father house shadow them conditions", field.NOP())
        space.add_label("NO_SHADOW", 0xb0b7b)
        space.write(
            field.BranchIfEventBitClear(npc_bit.SHADOW_GAU_FATHER_HOUSE, "NO_SHADOW"),
        )
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), "NO_SHADOW"),
            )

        # use first time speaking to merchant space
        space = Reserve(0xb0b7d, 0xb0ba0, "gau father house merchant first dialog", field.NOP())
        space.write(
            field.HideEntity(self.shadow_npc_id),
            field.HideEntity(self.interceptor_npc_id),
            field.Return(),
        )

    def character_music_mod(self, character):
        space = Reserve(0xb0b78, 0xb0b79, "Play Song Shadow")
        space.write([
            field.StartSong(get_character_theme(character)),
        ])

    def character_mod(self, character):
        self.character_music_mod(character)
        self.shadow_npc.sprite = character
        self.shadow_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xb0a5f, 0xb0aed, "gau father house wob recruit shadow", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
            field.Branch(space.end_address + 1), # skip all the nop
        )

    def esper_item_mod(self, esper_item_instructions):
        self.shadow_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.shadow_npc.palette = self.characters.get_palette(self.shadow_npc.sprite)

        space = Reserve(0xb0a5f, 0xb0af9, "gau father house wob esper item reward", field.NOP())
        space.write(
            esper_item_instructions,

            field.FadeOutScreen(),
            field.WaitForFade(),
            field.Branch(space.end_address + 1), # skip all the nop
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
            field.UpdatePartyLeader(),
            field.SetEventBit(event_bit.RECRUITED_SHADOW_GAU_FATHER_HOUSE),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "gau father house finish check")
        finish_check = space.start_address

        space = Reserve(0xb0b02, 0xb0b05, "gau father house recruit shadow bit, fade in", field.NOP())
        space.write(
            field.Call(finish_check),
        )
