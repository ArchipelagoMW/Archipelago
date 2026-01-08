from ..event.event import *

class SouthFigaro(Event):
    def name(self):
        return "South Figaro"

    def character_gate(self):
        return self.characters.CELES

    def init_rewards(self):
        if self.args.no_free_characters_espers:
            self.reward = self.add_reward(RewardType.ITEM)
        else:
            self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.WOUND_THE_CLOCK_SOUTH_FIGARO),
            field.SetEventBit(event_bit.NAMED_CELES),
            field.SetEventBit(event_bit.CELES_LOCKE_ESCAPED_SOUTH_FIGARO),
            field.SetEventBit(event_bit.SAW_SHADOW_WALKING_TO_CAFE_SOUTH_FIGARO),

            field.SetEventBit(npc_bit.CHAINED_CELES_SOUTH_FIGARO),
            field.ClearEventBit(npc_bit.SHADOW_SOUTH_FIGARO_PUB),
        )

    def mod(self):
        self.celes_npc_id = 0x13
        self.celes_npc = self.maps.get_npc(0x053, self.celes_npc_id)
        self.celes_npc.unknown1 = 0 # this was set to 1 and prevented animating character in entrance event

        # delete underground exit map event
        self.maps.delete_event(0x56, 52, 29)

        self.entrance_event_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.airship_follow_boat_mod()

        self.log_reward(self.reward)

    def entrance_event_mod(self):
        space = Reserve(0xaecdc, 0xaecf1, "south figaro celes basement (0x53) entrance event", field.NOP())
        space.write(
            field.ReturnIfEventBitClear(npc_bit.CHAINED_CELES_SOUTH_FIGARO),
            field.EntityAct(self.celes_npc_id, True,
                field_entity.AnimateKneeling(),
            ),
        )
        if self.args.character_gating:
            space.write(
                field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
                field.HideEntity(self.celes_npc_id),
            )
        space.write(
            field.Return(),
        )

    def character_mod(self, character):
        self.celes_npc.sprite = character
        self.celes_npc.palette = self.characters.get_palette(character)

        src = [
            field.RecruitAndSelectParty(character),
            field.HideEntity(self.celes_npc_id),
            field.ClearEventBit(npc_bit.CHAINED_CELES_SOUTH_FIGARO),
            field.SetEventBit(event_bit.FREED_CELES),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "south figaro basement recruit character")
        recruit_character = space.start_address

        space = Reserve(0xa8837, 0xa8841, "south figaro basement recruit character branch", field.NOP())
        space.write(
            field.Branch(recruit_character),
        )
        celes_npc_event = space.start_address

        self.celes_npc.set_event_address(celes_npc_event)

    def esper_item_mod(self, esper_item_instructions):
        self.celes_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.celes_npc.palette = self.characters.get_palette(self.celes_npc.sprite)

        src = [
            esper_item_instructions,

            field.FadeOutScreen(),
            field.WaitForFade(),
            field.HideEntity(self.celes_npc_id),
            field.ClearEventBit(npc_bit.CHAINED_CELES_SOUTH_FIGARO),
            field.SetEventBit(event_bit.FREED_CELES),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "south figaro basement esper/item reward")
        esper_item_reward = space.start_address

        space = Reserve(0xa8837, 0xa8841, "south figaro basement esper/item reward branch", field.NOP())
        space.write(
            field.Branch(esper_item_reward),
        )
        celes_npc_event = space.start_address

        self.celes_npc.set_event_address(celes_npc_event)

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

    def airship_follow_boat_mod(self):
        # make airship follow boat to south figaro from nikeah in wor
        space = Reserve(0xa92d8, 0xa931b, "south figaro wor crimson robbers exit boat after arriving", field.NOP())
        space.write(
            vehicle.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x01, direction.DOWN, default_music = False,
                            x = 113, y = 96, fade_in = False, airship = True),
            vehicle.SetPosition(113, 96),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.FadeLoadMap(0x5b, direction.LEFT, default_music = True,
                                x = 12, y = 11, fade_in = True, entrance_event = True),
            field.SetParentMap(0x01, direction.DOWN, 113, 95),
            field.Return(),
        )
