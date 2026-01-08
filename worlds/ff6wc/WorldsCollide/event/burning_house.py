from ..event.event import *

# TODO: only trigger this event in wob

class BurningHouse(Event):
    def name(self):
        return "Burning House"

    def character_gate(self):
        return self.characters.STRAGO

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.MET_STRAGO_RELM),
            field.SetEventBit(event_bit.DEFEATED_KEFKA_THAMASA),
            field.SetEventBit(event_bit.LEO_BURIED_THAMASA),
            field.SetEventBit(event_bit.FINISHED_THAMASA_KEFKA),

            field.ClearEventBit(npc_bit.FIRST_MAYOR_THAMASA),
            field.ClearEventBit(npc_bit.STRAGO_THAMASA_HOME),
            field.ClearEventBit(npc_bit.PARTY_THAMASA_AFTER_KEFKA),
            field.ClearEventBit(npc_bit.GUNGHO_OUTSIDE_THAMASA),
            field.SetEventBit(npc_bit.THAMASA_CITIZENS),
        )

    def mod(self):
        if self.args.character_gating:
            self.add_gating_condition()

        self.enter_burning_house_mod()
        self.flame_eater_mod()
        self.wake_up_mod()

        if not self.args.fixed_encounters_original:
            self.fixed_battles_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def add_gating_condition(self):
        # increase the price from 1500
        self.dialogs.set_text(1936, "You're strangers…<page>100000000 GP<line><choice> (Well, okay.)<line><choice> (No way!)<end>")

        space = Reserve(0xbd774, 0xbd79c, "burning house inn stranger sleep", field.NOP())
        space.write(
            field.Call(field.NOT_ENOUGH_MONEY),
            field.Return(),
        )

        space = Reserve(0xbd73f, 0xbd746, "burning house inn stranger check", field.NOP())
        space.add_label("STRANGER_PRICE", 0xbd769),
        space.write(
            field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), "STRANGER_PRICE"),
        )

    def enter_burning_house_mod(self):
        # wake up in middle of night, enter burning house, skip scene with villagers outside burning house
        space = Reserve(0xbdcc7, 0xbdccd, "load burning house map", field.NOP())
        space.write(
            field.LoadMap(0x15f, direction.UP, default_music = True, x = 4, y = 11, fade_in = True),
            field.Return(),
        )

        # event at entrance of burning house
        space = Reserve(0xbe5e4, 0xbe621, "burning house entrance event", field.NOP())
        space.write(
            field.Return(),
        )

    def flame_eater_mod(self):
        boss_pack_id = self.get_boss("FlameEater")

        space = Reserve(0xbe793, 0xbe799, "burning house invoke battle flame eater", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

        # split party, "Is this the source of our blaze...?"
        space = Reserve(0xbe76c, 0xbe78d, "burning house approach flame eater dialog", field.NOP())

    def defeated_flame_eater_mod(self, space):
        space.write(
            field.SetEventBit(event_bit.DEFEATED_FLAME_EATER),
            field.SetEventBit(npc_bit.SHADOW_AFTER_FLAME_EATER),
            field.HoldScreen(),
        )

    def wake_up_mod(self):
        src = [
            field.FadeOutSong(0x60),
            field.Pause(1),
            field.StartSong(0xb8),
            field.WaitForSong(),

            field.LoadMap(0x15a, direction.DOWN, default_music = True, x = 13, y = 16, fade_in = False, entrance_event = True),
            field.Call(field.UPDATE_LEADER_AND_SHOW_ALL_PARTY_MEMBERS),
            field.Call(field.DISABLE_COLLISIONS_FOR_PARTY_MEMBERS),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.SetPosition(15, 14), # top right bed
                field_entity.Turn(direction.DOWN),
            ),
            field.EntityAct(field_entity.PARTY1, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.SetPosition(11, 14), # top left bed
                field_entity.Turn(direction.DOWN),
            ),
            field.EntityAct(field_entity.PARTY2, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.SetPosition(15, 18), # bottom right bed
                field_entity.Turn(direction.DOWN),
            ),
            field.EntityAct(field_entity.PARTY3, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.SetPosition(11, 18), # bottom left bed
                field_entity.Turn(direction.DOWN),
            ),
            field.Call(field.HEAL_PARTY_HP_MP_STATUS),
            field.FadeInScreen(8),
            field.Pause(2.00),
            field.FinishCheck(),
            field.Call(field.GATHER_AFTER_INN),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "burning house wake up")
        self.wake_up = space.start_address

    def fixed_battles_mod(self):
        # BH has 12 fixed encounters that all share the same pack ID
        # to increase the variety of encounters, we are adding 1 more and swapping 6 of the flames to it
        # 415 is an otherwise unused encounter

        replaced_encounters = [
            (415, 0xBE6FF), 
            (415, 0xBE740),
            (415, 0xBE70C),
            (415, 0xBE733),
            (415, 0xBE726),
            (415, 0xBE74D),
        ]
        for pack_id_address in replaced_encounters:
            pack_id = pack_id_address[0]
            # first byte of the command is the pack_id
            invoke_encounter_pack_address = pack_id_address[1]+1
            space = Reserve(invoke_encounter_pack_address, invoke_encounter_pack_address, "flame invoke fixed battle (battle byte)")
            space.write(
                # subtrack 256 since WC stores fixed encounter IDs starting at 256
                pack_id - 0x100
            )

    def character_mod(self, character):
        shadow_npc_id = 0x1d
        shadow_npc = self.maps.get_npc(0x15f, shadow_npc_id)
        shadow_npc.sprite = character
        shadow_npc.palette = self.characters.get_palette(character)

        # strago jumps around, party finds relm
        space = Reserve(0xbe79e, 0xbe8da, "flame eater defeated", field.NOP())
        self.defeated_flame_eater_mod(space)
        space.write(
            field.CreateEntity(character),
            field.CreateEntity(0x1d),
            field.DeleteEntity(0x1b),
            field.RefreshEntities(),
            field.ShowEntity(0x1d),
            field.HideEntity(0x1b),

            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(49, 43),
                field_entity.AnimateKnockedOut(),
            ),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.UP, 7),
            ),
            field.Branch(space.end_address + 1), # skip nop
        )

        # "I'll use a smoke bomb"
        space = Reserve(0xbea2c, 0xbea2e, "burning house smoke bomb dialog", field.NOP())

        space = Reserve(0xbea44, 0xbea64, "burning house wake up", field.NOP())
        space.write(
            field.RecruitAndSelectParty(character),
            field.Branch(self.wake_up),
        )

    def esper_item_mod(self, instructions):
        # strago jumps around, party finds relm
        space = Reserve(0xbe79f, 0xbea3e, "burning house esper item", field.NOP())
        self.defeated_flame_eater_mod(space)
        space.write(
            instructions,

            field.FadeOutScreen(4),
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xbea44, 0xbea64, "burning house wake up", field.NOP())
        space.write(
            field.Branch(self.wake_up),
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
