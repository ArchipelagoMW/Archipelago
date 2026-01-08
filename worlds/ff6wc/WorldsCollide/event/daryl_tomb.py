from ..event.event import *

class DarylTomb(Event):
    def name(self):
        return "Daryl's Tomb"

    def character_gate(self):
        return self.characters.SETZER

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.entrance_mod()
        self.staircase_mod()
        self.dullahan_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def entrance_mod(self):
        if self.args.character_gating:
            space = Reserve(0xa3f91, 0xa3f97, "daryl tomb require setzer in party", field.NOP())
            space.write(
                field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            )
        else:
            space = Reserve(0xa3f91, 0xa3f97, "daryl tomb require setzer in party", field.NOP())

        space = Reserve(0xa3f9c, 0xa3fa0, "daryl tomb make setzer party leader", field.NOP())
        space = Reserve(0xa3fb9, 0xa3fbc, "daryl tomb she was your friend?", field.NOP())

        space = Reserve(0xa3fbd, 0xa3fbd, "daryl tomb setzer opening entrance animation", field.NOP())
        space.write(field_entity.PARTY0)

        space = Reserve(0xa3fd0, 0xa3fd0, "daryl tomb setzer animation after entrance open", field.NOP())
        space.write(field_entity.PARTY0)

        space = Reserve(0xa3fda, 0xa3fdc, "daryl tomb could be anything lurking", field.NOP())

    def staircase_mod(self):
        src = [
            # reset turtle's positions before leaving in case player re-enters later
            field.ClearEventBit(event_bit.DARYL_TOMB_TURTLE1_MOVED),
            field.ClearEventBit(event_bit.DARYL_TOMB_TURTLE2_MOVED),

            # for convenience change staircase door to take player back out to wor
            field.LoadMap(0x01, direction.DOWN, default_music = True, x = 25, y = 53),
            world.End(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "daryl tomb back exit")
        back_exit = space.start_address

        space = Reserve(0xa435d, 0xa4362, "daryl tomb staircase and getting falcon scenes", field.NOP())
        space.write(
            field.Branch(back_exit),
        )

    def dullahan_battle_mod(self):
        boss_pack_id = self.get_boss("Dullahan")

        space = Reserve(0xa4321, 0xa4327, "daryl tomb invoke battle dullahan", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def daryl_sleeps_here_mod(self, new_name):
        num_spaces = 15 - len(new_name) # try to center dialog

        daryl_sleeps_here_dialog_id = 2461 # previously 2464
        self.dialogs.set_text(daryl_sleeps_here_dialog_id, f"<line><{' ' * num_spaces}>{new_name} SLEEPS HERE<end>")

        space = Reserve(0xa42f9, 0xa42fb, "daryl tomb daryl sleeps here dialog", field.NOP())
        space.write(
            field.Dialog(daryl_sleeps_here_dialog_id, inside_text_box = False),
        )

    def character_mod(self, character):
        self.daryl_sleeps_here_mod(self.characters.get_name(character))

        space = Reserve(0xa4328, 0xa4333, "daryl tomb open staircase entrance", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
        )

    def esper_item_mod(self):
        space = Reserve(0xa4329, 0xa4333, "daryl tomb open staircase entrance", field.NOP())
        space.write(
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Turn(direction.UP),
            ),
        )
        return space

    def esper_mod(self, esper):
        self.daryl_sleeps_here_mod(self.espers.get_name(esper).upper())

        space = self.esper_item_mod()
        space.write(
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        )

    def item_mod(self, item):
        self.daryl_sleeps_here_mod(self.items.get_name(item).upper())

        space = self.esper_item_mod()
        space.write(
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        )

    def finish_check_mod(self):
        src = [
            field.SetEventBit(event_bit.DEFEATED_DULLAHAN),
            field.FinishCheck(),
            field.PlaySoundEffect(187),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "daryl tomb finish check")
        finish_check = space.start_address

        OPEN_BACK_EXIT = 0xaf1ed
        space = Reserve(0xa4334, 0xa433d, "daryl tomb open back exit", field.NOP())
        space.write(
            field.Call(finish_check),
            field.ShakeScreen(intensity = 2, permanent = False,
                              layer1 = True, layer2 = True, layer3 = True, sprite_layer = True),
            field.Call(OPEN_BACK_EXIT),
        )
