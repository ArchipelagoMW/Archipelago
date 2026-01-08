from ..event.event import *

class CollapsingHouse(Event):
    def name(self):
        return "Collapsing House"

    def character_gate(self):
        return self.characters.SABIN

    def init_rewards(self):
        if self.args.no_free_characters_espers:
            self.reward = self.add_reward(RewardType.ITEM)
        else:
            self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        pass

    def mod(self):
        self.timer_mod()
        self.dialogs_mod()

        if self.args.character_gating:
            self.add_gating_condition()
        if self.args.flashes_remove_most or self.args.flashes_remove_worst:
            self.flash_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def timer_mod(self):
        if self.args.event_timers_random:
            import random

            # randomize timer between 2 and 5 minutes
            seconds = random.randint(120, 300)

            space = Reserve(0xc5925, 0xc5926, "collapsing house timer")
            space.write(
                (seconds * 60).to_bytes(2, "little"),
            )

            timer_display = f"{seconds // 60}:{seconds % 60:>02}"
            self.log_change(f"Timer 6:00", timer_display)
        elif self.args.event_timers_none:
            space = Reserve(0xc5923, 0xc5929, "collapsing house timer", field.NOP())

    def dialogs_mod(self):
        self.dialogs.set_text(2218, "I…I…<line>I'm losing my grip…<line>Keep up the fight!<end>")
        space = Reserve(0xc5962, 0xc5964, "collapsing house child dialog", field.NOP())
        space = Reserve(0xc597c, 0xc597e, "collapsing house talk to sabin dialog", field.NOP())
        space = Reserve(0xc590b, 0xc5922, "enter collapsing house dialog", field.NOP())
        space.copy_from(0xc5923, 0xc592d)
        space = Reserve(0xc598c, 0xc598e, "exit collapsing house dialog", field.NOP())
        space = Reserve(0xc5a16, 0xc5a29, "collapsing house sabin alive dialog", field.NOP())
        space = Reserve(0xc5a45, 0xc5a47, "collapsing house end of world dialog", field.NOP())
        space = Reserve(0xc5a55, 0xc5a6b, "collapsing house given up hope dialog", field.NOP())
        space = Reserve(0xc5a79, 0xc5a7c, "collapsing house smash kefka dialog", field.NOP())

    def flash_mod(self):
        space = Reserve(0xc5848, 0xc5849, "collapsing house initial flash 1", field.FlashScreen(field.Flash.NONE))
        space = Reserve(0xc5863, 0xc5864, "collapsing house initial flash 2", field.FlashScreen(field.Flash.NONE))
        space = Reserve(0xc5868, 0xc5869, "collapsing house initial flash 3", field.FlashScreen(field.Flash.NONE))
        space = Reserve(0xc59ec, 0xc59ed, "collapsing house final flash 1", field.FlashScreen(field.Flash.NONE))
        space = Reserve(0xc59f5, 0xc59f6, "collapsing house final flash 2", field.FlashScreen(field.Flash.NONE))

    def add_gating_condition(self):
        start_event = 0xc5844

        # do not trigger collapsing house event without sabin
        src = [
            field.ReturnIfEventBitSet(event_bit.LIGHT_JUDGEMENT_TZEN),
            field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            field.Branch(start_event),
        ]
        space = Write(Bank.CB, src, "collapsing house event check")
        start_event_check = space.start_address

        space = Reserve(0xc583e, start_event - 1, "collapsing house event tile")
        space.write(
            field.Branch(start_event_check),
        )

        space = Allocate(Bank.CC, 21, "tzen wor original entrance event", field.NOP())
        original_entrance_event = space.next_address
        space.copy_from(0xc56da, 0xc56ee)

        npc_holding_house_id = 0x11
        mother_during_collapsing_house_id = 0x12
        mother_after_collapsing_house_id = 0x13
        boy_after_collapsing_house_id = 0x1f
        mother_during_collapsing_house = self.maps.get_npc(0x131, mother_during_collapsing_house_id)

        # if gate not found yet, add new entrance event for normal wor town npcs
        src = [
            Read(0xc57e8, 0xc5828),  # fix some broken buildings

            field.DeleteEntity(npc_holding_house_id),
            field.DeleteEntity(mother_after_collapsing_house_id),
            field.DeleteEntity(boy_after_collapsing_house_id),

            # put mother in front of door, looking for child like wob
            field.CreateEntity(mother_during_collapsing_house_id),
            field.EntityAct(mother_during_collapsing_house_id, False,
                field_entity.SetPosition(16, 9),
                "TURN_LOOP",
                field_entity.Turn(direction.RIGHT),
                field_entity.Pause(2),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(2),
                field_entity.Turn(direction.LEFT),
                field_entity.Pause(2),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
                field_entity.Turn(direction.RIGHT),
                field_entity.Pause(2),
                field_entity.BranchBackwards("TURN_LOOP"),
            ),
            field.ShowEntity(mother_during_collapsing_house_id),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "tzen wor no gate character entrance event")
        gated_entrance_event = space.start_address

        # when gated, give mother her wob dialog
        mother_wob_dialog = 0xc5dc1

        # otherwise during collapsing house, use normal dialog
        space = Allocate(Bank.CC, 16, "collapsing house mother dialog", field.NOP())
        mother_original_dialog = space.next_address
        space.copy_from(0xc5ac9, 0xc5acc)

        mother_dialog_event = space.next_address
        space.write(
            field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), mother_wob_dialog),
            field.Branch(mother_original_dialog),
        )
        mother_during_collapsing_house.set_event_address(mother_dialog_event)

        space = Reserve(0xc56da, 0xc56ee, "tzen wor entrance event", field.NOP())
        space.write(
            field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), gated_entrance_event),
            field.Branch(original_entrance_event),
            field.Return(),
        )

    def character_mod(self, character):
        sabin_npc_id = 0x11
        sabin_npc = self.maps.get_npc(0x131, sabin_npc_id)
        sabin_npc.sprite = character
        sabin_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xc5a9d, 0xc5aba, "collapsing house add char", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
        )

    def esper_item_mod(self):
        sabin_npc_id = 0x11
        sabin_npc = self.maps.get_npc(0x131, sabin_npc_id)

        sabin_npc.sprite = self.characters.get_random_esper_item_sprite()
        sabin_npc.palette = self.characters.get_palette(sabin_npc.sprite)

        # ovewrite adding sabin with fading out screen and updating event bits
        space = Reserve(0xc5a9d, 0xc5aba, "collapsing house overwrite add char", field.NOP())
        space.copy_from(0xc5a8d, 0xc5a9c)

    def esper_mod(self, esper):
        self.esper_item_mod()

        # overwrite now copied fade/bits with adding esper
        space = Reserve(0xc5a8d, 0xc5a9c, "collapsing house add esper", field.NOP())
        space.write(
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        )

    def item_mod(self, item):
        self.esper_item_mod()

        # overwrite now copied fade/bits with getting item
        space = Reserve(0xc5a8d, 0xc5a9c, "collapsing house get item", field.NOP())
        space.write(
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        )

    def finish_check_mod(self):
        src = [
            field.WaitForFade(),
            field.FinishCheck(),
            field.EnableEntityCollision(field_entity.PARTY0),
            field.FreeMovement(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "collapsing house finish check")
        finish_check = space.start_address

        space = Reserve(0xc5ac4, 0xc5ac7, "collapsing house re-enable collisions", field.NOP())
        space.write(
            field.Call(finish_check),
        )
