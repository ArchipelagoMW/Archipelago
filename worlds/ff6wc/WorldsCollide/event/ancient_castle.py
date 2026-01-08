from ..event.event import *

class AncientCastle(Event):
    def name(self):
        return "Ancient Castle"

    def character_gate(self):
        return self.characters.EDGAR

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.ODIN_STATUE_ANCIENT_CASTLE),
            field.SetEventBit(event_bit.GOT_ODIN),
            field.SetEventBit(event_bit.FOUND_ANCIENT_CASTLE),
            field.SetEventBit(npc_bit.BOOKCASE_ANCIENT_CASTLE),
            field.SetEventBit(npc_bit.DRAGON_ANCIENT_CASTLE),
        )

    def mod(self):
        self.dialog_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)
        self.finish_check_mod()

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xc1f5c, 0xc1f5f, "ancient castle even the queen was turned to stone", field.NOP())
        space = Reserve(0xc1f73, 0xc1f75, "ancient castle a tear comes from the stone", field.NOP())

    def character_mod(self, character):
        statue_npc_id = 0x11
        statue_npc = self.maps.get_npc(0x198, statue_npc_id)
        statue_npc.sprite = character

        space = Reserve(0xc1f72, 0xc1f72, "ancient castle pause after tear", field.NOP())

        # NOTE: statue/character turned gray at 0xc19fd
        #       for command 0x61 some colors are # 00 = black, 01 = red, 02 = green, 03 = yellow, 04 = blue, 05 = purple,
        #                                        # 06 = teal, 07 = gray, 08 = teal, 09 = blue/purple, 0a = darker yellow
        src = [
            field.SetPalette(statue_npc_id, self.characters.get_palette(character)),
            field.EntityAct(statue_npc_id, True,
                field_entity.AnimateKneeling(),
                field_entity.Pause(20),
                field_entity.AnimateStandingHeadDown(),
                field_entity.Pause(16),
                field_entity.AnimateStandingFront(),
                field_entity.Pause(8),

                # blink eyes
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
                field_entity.AnimateCloseEyes(),
                field_entity.Pause(1),
                field_entity.Turn(direction.DOWN),
                field_entity.Pause(1),
            ),

            field.FadeOutScreen(4),
            field.WaitForFade(),

            field.ClearEventBit(npc_bit.MARIA_STATUE_ANCIENT_CASTLE),
            field.HideEntity(statue_npc_id),
            field.DeleteEntity(statue_npc_id),

            field.RecruitAndSelectParty(character),

            field.FadeInScreen(),
            field.WaitForFade(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "ancient castle statue to character")
        recruit_character = space.start_address

        space = Reserve(0xc1f76, 0xc1f84, "ancient castle display receive raiden dialog and take odin", field.NOP())
        space.write(
            field.Call(recruit_character),
            field.Branch(space.end_address + 1),
        )

    def esper_mod(self, esper):
        space = Reserve(0xc1f7e, 0xc1f84, "ancient castle display receive raiden dialog and take odin", field.NOP())
        space.write(
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.AddEsper(esper, sound_effect = False),
        )

    def item_mod(self, item):
        space = Reserve(0xc1f76, 0xc1f84, "ancient castle display receive raiden dialog and take odin", field.NOP())
        space.write(
            field.Dialog(self.items.get_receive_dialog(item)),
            field.AddItem(item, sound_effect = False),
            field.Branch(space.end_address + 1), # skip nops
        )

    def finish_check_mod(self):
        src = [
            field.SetEventBit(event_bit.GOT_RAIDEN),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "ancient castle finish check")
        finish_check = space.start_address

        space = Reserve(0xc1f85, 0xc1f88, "ancient castle give raiden and set event bit", field.NOP())
        space.write(
            field.Call(finish_check),
        )
