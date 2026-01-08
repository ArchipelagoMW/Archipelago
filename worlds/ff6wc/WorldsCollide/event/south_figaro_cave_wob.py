from ..event.event import *

class SouthFigaroCaveWOB(Event):
    def name(self):
        return "South Figaro Cave"

    def character_gate(self):
        return self.characters.LOCKE

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.SOLDIER_SOUTH_FIGARO_CAVE),
        )

    def mod(self):
        self.cleanup_mod()
        self.requirement_mod()
        self.noises_mod()
        self.tunnel_armor_battle_mod()
        self.entrance_exit_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def cleanup_mod(self):
        # south figaro cave maps 0x48 and 0x49 are never used
        # free up some unused events
        self.maps.delete_event(0x048, 16, 42)
        self.maps.delete_event(0x049, 47, 33)
        self.maps.delete_event(0x049, 47, 29)

        # figaro guards outside south figaro cave entrance
        self.maps.remove_npc(0x47, 0x12)
        self.maps.remove_npc(0x47, 0x12)

    def requirement_mod(self):
        # after lete river a different figaro cave is loaded which has tunnel armor
        # remove the lete river completed requirement
        space = Reserve(0xa5ee3, 0xa5ee8, "figaro cave lete river complete requirement")
        space.add_label("LOAD_MAP", 0xa5ef0),
        space.write(
            world.Branch("LOAD_MAP"),
        )

        space = Reserve(0xa5ef7, 0xa5efc, "figaro cave lete river complete requirement")
        space.add_label("LOAD_MAP", 0xa5f04)
        space.write(
            field.Branch("LOAD_MAP"),
        )

    def noises_mod(self):
        # because player can now enter cave from either side
        # make each noise require the previous noise and make tunnel armor require all three noises
        src = [
            Read(0xa767a, 0xa7687),
        ]
        space = Write(Bank.CA, src, "figaro cave first noise")
        first_noise = space.start_address

        space = Reserve(0xa7674, 0xa7687, "figaro cave first noise branch", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.FIRST_NOISE_FIGARO_CAVE),
        )
        if self.args.character_gating:
            space.write(
                field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            )
        space.write(
            field.Branch(first_noise),
        )

        src = [
            Read(0xa768e, 0xa769b),
        ]
        space = Write(Bank.CA, src, "figaro cave second noise")
        second_noise = space.start_address

        space = Reserve(0xa7688, 0xa769b, "figaro cave second noise branch", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.SECOND_NOISE_FIGARO_CAVE),
            field.ReturnIfEventBitClear(event_bit.FIRST_NOISE_FIGARO_CAVE),
            field.Branch(second_noise),
        )

        src = [
            Read(0xa76a2, 0xa76a9),
            # skip copying "LOCKE: What IS that noise?" dialog
            Read(0xa76ad, 0xa76b2),
        ]
        space = Write(Bank.CA, src, "figaro cave third noise")
        third_noise = space.start_address

        space = Reserve(0xa769c, 0xa76b2, "figaro cave third noise branch", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.THIRD_NOISE_FIGARO_CAVE),
            field.ReturnIfEventBitClear(event_bit.SECOND_NOISE_FIGARO_CAVE),
            field.Branch(third_noise),
        )

    def tunnel_armor_battle_mod(self):
        space = Reserve(0x10a8c4, 0x10a8cf, "figaro cave tunnel armor battle dialog",)
        space.clear(0xfd)
        space.write(0xff)

    def entrance_exit_mod(self):
        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FadeLoadMap(0x00, direction.DOWN, default_music = False,
                              x = 73, y = 94, fade_in = False, airship = True),
            vehicle.SetPosition(73, 94),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x047, direction.DOWN, default_music = True, x = 11, y = 49),
            field.FadeInScreen(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro cave move airship to castle side")
        move_airship_to_castle_side = space.start_address

        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FadeLoadMap(0x00, direction.DOWN, default_music = False,
                              x = 75, y = 103, fade_in = False, airship = True),
            vehicle.SetPosition(75, 103),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x00, direction.DOWN, default_music = True, x = 75, y = 103),
            world.Turn(direction.DOWN),
            world.End(),
        ]
        space = Write(Bank.CA, src, "figaro cave move airship to town side")
        move_airship_to_town_side = space.start_address

        from ..data.map_event import MapEvent
        self.maps.delete_short_exit(0x046, 47, 40)
        new_event = MapEvent()
        new_event.x = 47
        new_event.y = 40
        new_event.event_address = move_airship_to_castle_side - EVENT_CODE_START
        self.maps.add_event(0x046, new_event)

        self.maps.delete_short_exit(0x045, 16, 43)
        new_event = MapEvent()
        new_event.x = 16
        new_event.y = 43
        new_event.event_address = move_airship_to_town_side - EVENT_CODE_START
        self.maps.add_event(0x045, new_event)

    def tunnel_armor_function(self, reward_instructions):
        boss_pack_id = self.get_boss("TunnelArmr")

        src = [
            Read(0xa89c2, 0xa89cc),   # shake screen, change volume

            field.InvokeBattle(boss_pack_id),
            reward_instructions,
            field.Return(),
        ]
        space = Write(Bank.CA, src, "figaro cave tunnel armor and reward")
        battle_reward = space.start_address

        space = Reserve(0xa89af, 0xa89eb, "figaro cave tunnel armor", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.DEFEATED_TUNNEL_ARMOR),
            field.ReturnIfEventBitClear(event_bit.THIRD_NOISE_FIGARO_CAVE),

            # some replaced code from 0xa89b5 to 0xa89be
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Turn(direction.UP),
            ),
            field.ShakeScreen(intensity = 3, permanent = True, layer1 = True,
                              layer2 = True, layer3 = True, sprite_layer = True),
            field.PlaySoundEffect(165),
            field.Pause(2.5),

            # call new function
            field.Call(battle_reward),

            field.SetEventBit(event_bit.DEFEATED_TUNNEL_ARMOR),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FinishCheck(),

            field.Return(),
        )

    def character_mod(self, character):
        self.tunnel_armor_function([
            field.CreateEntity(character),
            field.EntityAct(character, True,
                field_entity.SetPosition(47, 34),
                field_entity.SetSpeed(field_entity.Speed.SLOW),
            ),
            field.ShowEntity(character),
            field.FadeInScreen(),
            field.EntityAct(character, True,
                field_entity.Move(direction.DOWN, 2),
                field_entity.Pause(8),
                field_entity.AnimateStandingHeadDown(),
                field_entity.Pause(8),
                field_entity.AnimateStandingFront(),
                field_entity.Pause(4),
            ),
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
        ])

    def esper_item_mod(self, esper_item_instructions):
        self.tunnel_armor_function([
            field.FadeInScreen(),
            field.WaitForFade(),
            esper_item_instructions,
        ])

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
