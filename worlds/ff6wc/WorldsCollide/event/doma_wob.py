from ..event.event import *

class DomaWOB(Event):
    def name(self):
        return "Doma WOB"

    def character_gate(self):
        return self.characters.CYAN

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.VARIOUS_DOMA_POISONING),
            field.SetEventBit(event_bit.CYAN_FOUND_POISONED_KING_DOMA),
            field.SetEventBit(event_bit.CYAN_FOUND_POISONED_FAMILY_DOMA),
        )

    def mod(self):
        self.enter_event_x = 33
        self.enter_event_y = 42

        self.exit_event_x = 33
        self.exit_event_y = 53

        # 2 tiles below doma on wob map
        self.wob_left_x = 156
        self.wob_left_y = 84
        self.wob_right_x = 157
        self.wob_right_y = 84

        self.dialog_mod()
        self.leader_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.map_events_mod()
        self.end_mod()

        self.log_reward(self.reward)

    def dialog_mod(self):
        space = Reserve(0xb9eb5, 0xb9eb7, "doma i am your worst nightmare dialog", field.NOP())
        space = Reserve(0xb9e7c, 0xb9e7e, "doma sentries exit doma with cyan dialog", field.NOP())
        space = Reserve(0xb9f2b, 0xb9f2d, "doma general's been defeated dialog", field.NOP())
        space = Reserve(0xb9fb4, 0xb9fb6, "doma walled up in there dialog", field.NOP())

        self.dialogs.set_text(536, "Thou musn't give up the fight!<end>")
        self.dialogs.set_text(537, "DOMA SENTRY: Sir!<line>Let their commander have it!<end>")

    def leader_battle_mod(self):
        boss_pack_id = self.get_boss("Leader")

        space = Reserve(0xb9eb8, 0xb9ebe, "doma wob invoke battle leader", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def enter_exit_functions_mod(self, enter_instructions, exit_instructions):
        space = Reserve(0xba083, 0xba0b6, "doma (0x11d) entrance event", field.NOP())

        # in wob, entrance is changed to a tile event from a wob exit
        # need to update the parent map to return to
        space.write(
            field.ReturnIfEventBitSet(event_bit.IN_WOR),
            field.SetParentMap(0, direction.DOWN, self.wob_left_x,self.wob_left_y),
            field.Return(),
        )

        # doma attack scene up until char (and 2 soldiers) go outside
        space = Reserve(0xb9aae, 0xb9d30, "doma add char and exit functions", field.NOP())

        self.exit_function = space.next_address
        space.write(
            exit_instructions,

            field.SetEventBit(event_bit.FINISHED_DOMA_WOB),
            field.FinishCheck(),
            field.LoadMap(0x11d, direction.UP, default_music = True,
                          x = self.exit_event_x, y = self.exit_event_y,
                          fade_in = True, entrance_event = True),
            field.Return(),
        )

        load_doma_function = space.next_address
        space.write(
            world.LoadMap(0x11d, direction.UP, default_music = True,
                          x = self.exit_event_x, y = self.exit_event_y,
                          fade_in = True, entrance_event = True),
            field.Return(),
        )

        # NOTE: adding wob event for doma to load the map at an event tile which
        #       immediately executes enter_event_function because entrance events cannot load a different map
        self.enter_function = space.next_address
        space.write(
            # enter normal doma if event bit set
            world.BranchIfEventBitSet(event_bit.FINISHED_DOMA_WOB, load_doma_function),
        )

        if self.args.character_gating:
            space.write(
                world.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), load_doma_function),
            )
        space.write(
            # else load doma attack scene and at event tile to trigger scene
            world.LoadMap(0x78, direction.UP, default_music = True,
                          x = self.enter_event_x, y = self.enter_event_y, fade_in = False),
            field.Return(),
        )

        self.enter_event_function = space.next_address
        space.write(
            field.HoldScreen(),
            field.LoadMap(0x78, direction.DOWN, default_music = True,
                          x = self.enter_event_x, y = self.enter_event_y),

            enter_instructions,

            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.DOWN, 7)
            ),
        )

        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

    def map_events_mod(self):
        self.maps.delete_short_exit(0x00, self.wob_left_x, self.wob_left_y)
        self.maps.delete_short_exit(0x00, self.wob_right_x, self.wob_right_y)

        from ..data.map_event import MapEvent

        new_event = MapEvent()
        new_event.x = self.wob_left_x
        new_event.y = self.wob_left_y
        new_event.event_address = self.enter_function - EVENT_CODE_START
        self.maps.add_event(0x00, new_event)

        new_event = MapEvent()
        new_event.x = self.wob_right_x
        new_event.y = self.wob_right_y
        new_event.event_address = self.enter_function - EVENT_CODE_START
        self.maps.add_event(0x00, new_event)

        new_event = MapEvent()
        new_event.x = self.enter_event_x
        new_event.y = self.enter_event_y
        new_event.event_address = self.enter_event_function - EVENT_CODE_START
        self.maps.add_event(0x78, new_event)

    def cyan_npc_mod(self, initial_character):
        # character who walks out with the two sentries
        space = Reserve(0xb9d31, 0xb9d31, "doma initial character position")
        space.write(initial_character),
        space = Reserve(0xb9e4f, 0xb9e4f, "doma character appears")
        space.write(initial_character)

        # controllable character (pushed back if try to leave, nods at end)
        space = Reserve(0xb9e9c, 0xb9e9c, "doma character cannot leave")
        space.write(field_entity.PARTY0)
        space = Reserve(0xb9fae, 0xb9fae, "doma character face allies")
        space.write(field_entity.PARTY0)
        space = Reserve(0xb9fcb, 0xb9fcb, "doma character head nod")
        space.write(field_entity.PARTY0)

    def character_mod(self, character):
        self.cyan_npc_mod(character)
        self.enter_exit_functions_mod([
            field.CreateEntity(character),
            field.ShowEntity(character),
        ],
        [
        ])

        src = [
            Read(0xb9e89, 0xb9e8c),  # copy call set party members' layering priority to 0

            field.RecruitAndSelectParty(character),

            # put party where the character was
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.SetPosition(self.enter_event_x, self.enter_event_y + 7),
            ),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.NORMAL),
                field_entity.Move(direction.DOWN, 7)
            ),
            field.FadeInScreen(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "doma wob recruit character")
        recruit_character = space.start_address

        space = Reserve(0xb9e89, 0xb9e8c, "doma call set party members' layering priority to 0", field.NOP())
        space.write(
            field.Call(recruit_character),
        )

    def esper_mod(self, esper):
        self.cyan_npc_mod(field_entity.PARTY0)
        self.enter_exit_functions_mod([
        ],
        [
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def item_mod(self, item):
        self.cyan_npc_mod(field_entity.PARTY0)
        self.enter_exit_functions_mod([
        ],
        [
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def end_mod(self):
        # function called after commander defeated and army retreats
        space = Reserve(0xb9ff1, 0xb9ff9, "doma call exit function", field.NOP())

        # call the new event end function instead of returning to imperial camp
        space.write(field.Call(self.exit_function))
