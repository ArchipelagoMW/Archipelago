from ..event.event import *

class MtKolts(Event):
    def name(self):
        return "Mt. Kolts"

    def character_gate(self):
        return self.characters.SABIN

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def mod(self):
        self.vargas_npc_id = 0x10

        self.dialog_mod()

        if self.args.character_gating:
            self.add_gating_condition()

        self.shadow_vargas_mod()
        self.vargas_battle_mod()
        self.entrance_exit_mod()
        self.vargas_trigger_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def dialog_mod(self):
        # "sabin sent you, right?" dialog
        space = Reserve(0xa8297, 0xa8299, "mt kolts sabin sent you dialog", field.NOP())

    def add_gating_condition(self):
        src = [
            field.ReturnIfEventBitClear(event_bit.character_recruited(self.character_gate())),
            Read(0xa8267, 0xa828e)
        ]
        space = Write(Bank.CA, src, "mt kolts vargas appears at end gate")
        vargas_appears = space.start_address

        space = Reserve(0xa8267, 0xa828e, "mt kolts vargas appears at end", field.NOP())
        space.write(
            field.Branch(vargas_appears),
        )

    def shadow_vargas_mod(self):
        # shadowy vargas uses sabin's sprite with an all black palette
        # character npc palettes are updated to match the character in npc data, change vargas back to black palette
        vargas_shadow_npc1 = self.maps.get_npc(0x060, self.vargas_npc_id)
        vargas_shadow_npc1.palette = 0x06
        vargas_shadow_npc2 = self.maps.get_npc(0x061, self.vargas_npc_id)
        vargas_shadow_npc2.palette = 0x06

    def vargas_battle_mod(self):
        # sabin appears in vargas battle
        space = Reserve(0x10a49d, 0x10a576, "mt kolts vargas battle sabin appears")
        space.clear(0xfd)
        space.write(0xff)

        # sabin hit with death sentence by vargas
        space = Reserve(0x10a6b4, 0x10a6e1, "mt kolts vargas battle sabin death sentence")
        space.clear(0xfd)
        space.write(0xff)

        # after sabin uses pummel on vargas
        space = Reserve(0x10a6fb, 0x10a706, "mt kolts sabin pummeled vargas")
        space.clear(0xfd)
        space.write(0xff)

    def entrance_exit_mod(self):
        # if vargas hasn't been defeated yet, block the back entrance (coming from returner's hideout)
        src = [
            field.ReturnIfEventBitSet(event_bit.DEFEATED_VARGAS),
            field.SetMapTiles(layer = 2, x = 9, y = 47, w = 2, h = 3, tiles = [
                              101, 101,
                                1,  54,
                                1,  70,
            ]),
            field.SetMapTiles(layer = 1, x = 8, y = 47, w = 3, h = 5, tiles = [
                              102, 221, 223,
                              160, 237, 239,
                              176, 253, 255,
                              192, 100, 102,
                               64, 193, 194,
            ]),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "mt kolts block back entrance")
        block_back_entrance = space.start_address

        self.maps.set_entrance_event(0x64, block_back_entrance - EVENT_CODE_START)

        # move the airship, have it follow player on both sides of mt kolts
        # NOTE: cannot use entrance events to load a map (i.e. the world map to move airship)
        #       instead, replace exits leading to entrance/exit cliffs with events to move it
        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FadeLoadMap(0x00, direction.DOWN, default_music = False,
                              x = 102, y = 101, fade_in = False, airship = True),
            vehicle.SetPosition(102, 101),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x5f, direction.LEFT, default_music = True, x = 10, y = 26),
            field.FadeInScreen(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "mt kolts entrance move airship")
        entrance_move_airship = space.start_address

        src = [
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.FadeLoadMap(0x00, direction.DOWN, default_music = False,
                              x = 98, y = 93, fade_in = False, airship = True),
            vehicle.SetPosition(98, 93),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x65, direction.DOWN, default_music = True, x = 10, y = 49),
            field.FadeInScreen(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "mt kolts exit move airship")
        exit_move_airship = space.start_address

        from ..data.map_event import MapEvent
        self.maps.delete_short_exit(0x64, 7, 13)
        new_event = MapEvent()
        new_event.x = 7
        new_event.y = 13
        new_event.event_address = entrance_move_airship - EVENT_CODE_START
        self.maps.add_event(0x64, new_event)

        self.maps.delete_short_exit(0x64, 17, 59)
        new_event = MapEvent()
        new_event.x = 17
        new_event.y = 59
        new_event.event_address = exit_move_airship - EVENT_CODE_START
        self.maps.add_event(0x64, new_event)

    def vargas_trigger_mod(self):
        # Vargas appears on the map 0x62 via 2 tile triggers. With B-Dash, players can outpace him leading to soft-locks.
        # Change the 2 event tile triggers to a different location.
        old_event = self.maps.get_event(0x62, 10, 32) # get existing event

        self.maps.delete_event(0x62, 10, 32) # vargas event tile (left)
        self.maps.delete_event(0x62, 11, 32) # vargas event tile (right)

        from ..data.map_event import MapEvent
        # add event tile to earlier on the path
        new_event = MapEvent()
        new_event.x = 21
        new_event.y = 19
        new_event.event_address = old_event.event_address
        self.maps.add_event(0x62, new_event)

        # add event tile to bottom right of stairs
        new_event = MapEvent()
        new_event.x = 21
        new_event.y = 20
        new_event.event_address = old_event.event_address
        self.maps.add_event(0x62, new_event)

    def character_mod(self, character):
        boss_pack_id = self.get_boss("Vargas")

        space = Reserve(0xa82a3, 0xa831f, "mt kolts invoke vargas battle", field.NOP())
        space.write(
            field.Pause(1),
            field.InvokeBattle(boss_pack_id, 0x0b),
            field.HideEntity(self.vargas_npc_id),

            field.ClearEventBit(npc_bit.VARGAS_MT_KOLTS_EXIT),
            field.SetEventBit(event_bit.DEFEATED_VARGAS),
            field.RecruitCharacter(character),

            field.CreateEntity(field_entity.PARTY1),
            field.CreateEntity(field_entity.PARTY2),
            field.CreateEntity(field_entity.PARTY3),

            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(20, 33),
                field_entity.Turn(direction.RIGHT),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
            ),
            field.EntityAct(field_entity.PARTY1, True,
                field_entity.SetPosition(21, 34),
                field_entity.Turn(direction.UP),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
            ),
            field.EntityAct(field_entity.PARTY2, True,
                field_entity.SetPosition(22, 35),
                field_entity.Turn(direction.UP),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
            ),
            field.EntityAct(field_entity.PARTY3, True,
                field_entity.SetPosition(19, 33),
                field_entity.Turn(direction.RIGHT),
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
            ),

            field.ShowEntity(field_entity.PARTY1),
            field.ShowEntity(field_entity.PARTY2),
            field.ShowEntity(field_entity.PARTY3),

            field.CreateEntity(character),
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xa8328, 0xa8329, "mt kolts show sabin", field.NOP())
        space.write(
            field.ShowEntity(character),
        )

        space = Reserve(0xa832b, 0xa832c, "mt kolts pause after vargas battle", field.NOP())
        space = Reserve(0xa8353, 0xa8353, "mt kolts pause before locke approaches sabin", field.NOP())

        src = [
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "mt kolts character receive reward")
        receive_reward = space.start_address

        space = Reserve(0xa83b3, 0xa83bf, "mt kolts hide party, add char", field.NOP())
        space.write(
            field.HideEntity(field_entity.PARTY1),
            field.HideEntity(field_entity.PARTY2),
            field.HideEntity(field_entity.PARTY3),
            field.Call(receive_reward),
            field.Return(),
        )

        # change sabin to new character
        space = Reserve(0xa8320, 0xa8320, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa8335, 0xa8335, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa8345, 0xa8345, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa8349, 0xa8349, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa834f, 0xa834f, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa839a, 0xa839a, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa83a6, 0xa83a6, "mt kolts after vargas sabin")
        space.write(character)
        space = Reserve(0xa83ac, 0xa83ac, "mt kolts after vargas sabin")
        space.write(character)

        # change edgar to party 0
        space = Reserve(0xa832d, 0xa832d, "mt kolts after vargas edgar")
        space.write(field_entity.PARTY0)

        # change locke to party 1
        space = Reserve(0xa8357, 0xa8357, "mt kolts after vargas locke")
        space.write(field_entity.PARTY1)
        space = Reserve(0xa8377, 0xa8377, "mt kolts after vargas locke")
        space.write(field_entity.PARTY1)
        space = Reserve(0xa8392, 0xa8392, "mt kolts after vargas locke")
        space.write(field_entity.PARTY1)

        # change terra to party 2
        space = Reserve(0xa837c, 0xa837c, "mt kolts after vargas terra")
        space.write(field_entity.PARTY2)
        space = Reserve(0xa8396, 0xa8396, "mt kolts after vargas terra")
        space.write(field_entity.PARTY2)

        # remove dialogs
        space = Reserve(0xa8332, 0xa8334, "mt kolts SABIN!!", field.NOP())
        space = Reserve(0xa8354, 0xa8356, "mt kolts Big brother?", field.NOP())
        space = Reserve(0xa8379, 0xa837b, "mt kolts The brothers are reunited", field.NOP())
        space = Reserve(0xa838f, 0xa8391, "mt kolts Younger brother?", field.NOP())
        space = Reserve(0xa83a0, 0xa83a2, "mt kolts Bodybuilder?!", field.NOP())

    def esper_item_mod(self, esper_item_instructions):
        boss_pack_id = self.get_boss("Vargas")

        # scene with vargas and sabin
        # replace with: vargas jumps on party and fight happens
        space = Reserve(0xa82a3, 0xa82bf, "mt kolts invoke vargas battle", field.NOP())
        space.write(
            field.Pause(1),
            field.InvokeBattle(boss_pack_id, 0x0b),
            field.HideEntity(self.vargas_npc_id),
            field.ClearEventBit(npc_bit.VARGAS_MT_KOLTS_EXIT),
            field.SetEventBit(event_bit.DEFEATED_VARGAS),
            field.FadeInScreen(),

            esper_item_instructions,
            field.FinishCheck(),
            field.Return(),
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
