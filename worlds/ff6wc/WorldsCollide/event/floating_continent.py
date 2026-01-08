from ..event.event import *

# TODO game can freeze, is this something i did or a bug in emulator/game?
#      go through and when you get to the hole that brings you to three possible holes (including the one you came from)
#      go thruogh left hole, hit both switches and go back through the hole you came from
#      can ignore the right hole since it leads nowhere and now go back through the north hole
#      now run around and take the path you just created back to the hole you came from to reach the two switches
#      going in that hole will freeze

class FloatingContinent(Event):
    def name(self):
        return "Floating Continent"

    def character_gate(self):
        return self.characters.SHADOW

    def init_rewards(self):
        self.reward1 = self.add_reward(RewardType.CHARACTER | RewardType.ESPER)
        self.reward2 = self.add_reward(RewardType.ESPER | RewardType.ITEM)
        self.reward3 = self.add_reward(RewardType.CHARACTER | RewardType.ESPER)

    def mod(self):
        self.shadow_leaves_mod()
        self.airship_battle_mod()
        if not self.args.fixed_encounters_original:
            self.airship_fixed_battles_mod()
        self.ultros_chupon_battle_mod()
        self.air_force_battle_mod()

        self.ground_shadow_npc_id = 0x1b
        self.ground_shadow_npc = self.maps.get_npc(0x18a, self.ground_shadow_npc_id)

        self.ground_reward_position_mod()
        if self.reward1.type == RewardType.CHARACTER:
            self.ground_character_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ESPER:
            self.ground_esper_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ITEM:
            self.ground_item_mod(self.reward1.id)
        self.finish_ground_check()

        self.save_point_hole_mod()
        self.airship_return_mod()
        self.atma_battle_mod()

        if self.reward2.type == RewardType.ESPER:
            self.atma_esper_mod(self.reward2.id)
        elif self.reward2.type == RewardType.ITEM:
            self.atma_item_mod(self.reward2.id)

        self.statues_scene_mod()
        self.timer_mod()
        self.nerapa_battle_mod()

        if self.reward3.type == RewardType.CHARACTER:
            self.escape_character_mod(self.reward3.id)
        elif self.reward3.type == RewardType.ESPER:
            self.escape_esper_mod(self.reward3.id)
        elif self.reward3.type == RewardType.ITEM:
            self.escape_item_mod(self.reward3.id)

        self.log_reward(self.reward1)
        self.log_reward(self.reward2)
        self.log_reward(self.reward3)

    def shadow_leaves_mod(self):
        # remove shadow from party at floating continent (if return to airship or after atma)
        # use this space to add some new functions we need
        space = Reserve(0xad9fc, 0xada2f, "floating continent shadow leaves party", field.NOP())

        # copy some instructions to here so can make room for deleting lights where code originally was
        self.enter_floating_continent_function = space.next_address
        space.copy_from(0xa5a42, 0xa5a4a) # copy loading the map, showing party and holding screen
        space.write(
            field.Return(),
        )

        # also do the same thing for when returning from save point hole
        self.return_from_save_map_function = space.next_address
        space.copy_from(0xad951, 0xad95c) # copy loading the map and positioning the party
        space.write(
            field.Return(),
        )

        # delete the lights around the statues after the map is loaded
        # otherwise airship won't show up when 4 people in party and char (or esper?) still on ground
        # i create the lights again when the statue scene starts
        self.delete_lights_function = space.next_address
        space.write(
            field.DeleteEntity(0x1d),
            field.DeleteEntity(0x1e),
            field.DeleteEntity(0x1f),
            field.DeleteEntity(0x20),
            field.DeleteEntity(0x21),
            field.Return(),
        )

    def airship_battle_mod(self):
        space = Reserve(0xa582a, 0xa5839, "floating continent do not enforce 3 characters in party", field.NOP())
        space = Reserve(0xa592f, 0xa5931, "floating continent skip IAF dialog", field.NOP())

        # skip 3 out of the 6 battles before ultros/chupon battle
        space = Reserve(0xa5978, 0xa597d, "floating continent skip to chupon appearing in sky", field.NOP())
        space.write(
            field.Branch(0xa59bb),
        )

        # small pause to prevent chupon from clipping air force sprite in sky
        space = Reserve(0xa59bb, 0xa59be, "floating continent skip something approaches dialog", field.NOP())
        space.write(
            field.Pause(2.0),
        )

        space = Reserve(0xa5a42, 0xa5a4a, "floating continent enter after defeating air force", field.NOP())
        space.write(
            field.Call(self.enter_floating_continent_function),
            field.Call(self.delete_lights_function), # delete lights so airship shows up
        )

        space = Reserve(0xa5a68, 0xa5a6a, "floating continent skip kefka, gestahl, statues ahead dialog", field.NOP())

    def airship_fixed_battles_mod(self):
        # change iaf battles to front attacks, even if the original pack id happens to be the new random one
        # because other random formations in the pack may not work with pincer attacks
        
        # adding an unused pack id (416) to increase variety of encounters
        battle_background = 48 # airship, right

        pack_start_addresses = [
            (382, 0xa5932), #sky armor / spit fire
            (416, 0xa59fc), #unused
            (382, 0xa5a0d)] #sky armor / spit fire
        for pack_start_address in pack_start_addresses:
            pack_id = pack_start_address[0]
            start_address = pack_start_address[1]
            space = Reserve(start_address, start_address + 2, "floating continent iaf invoke fixed battle")
            space.write(
                field.InvokeBattleType(pack_id, field.BattleType.FRONT, battle_background, check_game_over = False),
            )

    def ultros_chupon_battle_mod(self):
        boss_pack_id = self.get_boss("Ultros/Chupon")

        battle_type = field.BattleType.FRONT
        battle_background = 48 # airship, right
        if boss_pack_id == self.enemies.packs.get_id("Cranes"):
            battle_type = field.BattleType.PINCER
            battle_background = 37 # airship, center

        space = Reserve(0xa5a1e, 0xa5a24, "floating continent invoke battle ultros/chupon", field.NOP())
        space.write(
            field.InvokeBattleType(boss_pack_id, battle_type, battle_background),
        )

    def air_force_battle_mod(self):
        if self.args.flashes_remove_most or self.args.flashes_remove_worst:
            # Slow the scrolling background by modifying the ADC command.
            space = Reserve(0x2b1b1, 0x2b1b3, "falling through clouds background movement")
            space.write(
                asm.ADC(0x0001, asm.IMM16) #default: 0x0006
            )

        boss_pack_id = self.get_boss("Air Force")
        battle_background = 7 # sky, falling

        space = Reserve(0xa5a3b, 0xa5a41, "floating continent invoke battle air force", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id, battle_background),
        )

    def ground_reward_position_mod(self):
        self.ground_shadow_npc.x = 11
        self.ground_shadow_npc.y = 13

        space = Reserve(0xad9a7, 0xad9aa, "floating continent move party above shadow", field.NOP())

    def ground_character_mod(self, character):
        self.ground_shadow_npc.sprite = character
        self.ground_shadow_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xad9b5, 0xad9b7, "floating continent down with the empire dialog", field.NOP())

        space = Reserve(0xad9c0, 0xad9ed, "floating continent add character on ground", field.NOP())
        space.write(
            field.RecruitCharacter(character),

            # i do not know why, but i need to delete the first npcs specifically before the select party screen
            # it prevents a softlock when already recruited 12+ characters
            # seems like after 11 characters they start to overwrite the npcs so i need to delete those first to make room
            field.DeleteEntity(0x10),
            field.DeleteEntity(0x11),
            field.DeleteEntity(0x12),
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),

            # loading the map here instead of just fading in the screen prevents a graphics bug with
            # the save point when the player has already acquired around 8+ characters
            # it also reloads the npcs that were deleted before the select party screen was shown
            field.LoadMap(0x18a, direction.RIGHT, default_music = False, x = 10, y = 13, fade_in = False, entrance_event = True),
            field.DeleteEntity(0x1b),
            field.FadeInScreen(),
        )

    def ground_esper_mod(self, esper):
        self.ground_shadow_npc.sprite = 91
        self.ground_shadow_npc.palette = 2
        self.ground_shadow_npc.split_sprite = 1
        self.ground_shadow_npc.direction = direction.UP

        space = Reserve(0xad9b1, 0xad9ed, "floating continent add esper on ground", field.NOP())
        space.write(
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.DeleteEntity(self.ground_shadow_npc_id),
            field.Branch(space.end_address + 1),
        )

    def ground_item_mod(self, item):
        # use sparkle as NPC for item (or AP item)
        self.ground_shadow_npc.sprite = 106
        self.ground_shadow_npc.palette = 6
        self.ground_shadow_npc.split_sprite = 1
        self.ground_shadow_npc.direction = direction.DOWN

        space = Reserve(0xad9b1, 0xad9ed, "floating continent add item on ground", field.NOP())
        space.write(
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.DeleteEntity(self.ground_shadow_npc_id),
            field.Branch(space.end_address + 1),
        )

    def finish_ground_check(self):
        src = [
            Read(0xad9ee, 0xad9f2), # clear ground npc bit, set shadow recruited bit, update party leader
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "floating continent ground finish check")
        finish_check = space.start_address

        space = Reserve(0xad9ee, 0xad9f2, "floating continent set bits, update leader after shadow", field.NOP())
        space.write(
            field.Call(finish_check),
        )

    def save_point_hole_mod(self):
        space = Reserve(0xad951, 0xad95c, "floating continent return from save point hole", field.NOP())
        space.write(
            field.Call(self.return_from_save_map_function),
            field.Call(self.delete_lights_function), # delete lights so airship shows up
        )

    def airship_return_mod(self):
        self.dialogs.set_text(2135, "Do you wish to return?<line><choice> (No)<line><choice> (Yes)<end>")

        space = Reserve(0xa5a8b, 0xa5a8f, "floating continent do not remove shadow if return to airship", field.NOP())

        # do not set the shadow npc even bit again (otherwise when you return character/esper would be there again)
        space = Reserve(0xa5ab5, 0xa5abc, "floating continent do not put shadow npc back on map", field.NOP())

    def atma_battle_mod(self):
        boss_pack_id = self.get_boss("AtmaWeapon")

        space = Reserve(0xada30, 0xada36, "floating continent invoke battle atmaweapon", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def atma_esper_item_mod(self, esper_item_instructions):
        src = [
            esper_item_instructions,
            field.SetEventBit(event_bit.DEFEATED_ATMAWEAPON),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "floating continent atma weapon finish check")
        finish_check = space.start_address

        space = Reserve(0xada3f, 0xada46, "floating continent do not remove shadow after fighting atma", field.NOP())
        space.write(
            field.Call(finish_check),
        )

    def atma_esper_mod(self, esper):
        self.atma_esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def atma_item_mod(self, item):
        self.atma_esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def statues_scene_mod(self):
        kefka_npc_id = 0x11
        kefka_npc = self.maps.get_npc(0x18a, kefka_npc_id)
        kefka_npc.x = 60
        kefka_npc.y = 7

        gestahl_npc_id = 0x1c
        gestahl_npc = self.maps.get_npc(0x18a, gestahl_npc_id)
        gestahl_npc.x = 57
        gestahl_npc.y = 7

        space = Reserve(0xadd22, 0xaddb3, "floating continent statues move camera", field.NOP())
        space.write(
            # first create the lights i deleted
            field.CreateEntity(0x1d),
            field.CreateEntity(0x1e),
            field.CreateEntity(0x1f),
            field.CreateEntity(0x20),
            field.CreateEntity(0x21),
            field.ShowEntity(0x1d),
            field.ShowEntity(0x1e),
            field.ShowEntity(0x1f),
            field.ShowEntity(0x20),
            field.ShowEntity(0x21),
            field.RefreshEntities(),

            field.HoldScreen(),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.UP, 5),
            ),
        )

        space = Reserve(0xaddf0, 0xade0c, "floating continent statues party approach kefka", field.NOP())
        space.write(
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.Move(direction.DOWN, 3),
            ),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Move(direction.UP, 2),
            ),
            field.EntityAct(kefka_npc_id, True,
                field_entity.Turn(direction.DOWN),
            ),
            field.EntityAct(gestahl_npc_id, True,
                field_entity.Turn(direction.DOWN),
            ),
        )

        space = Reserve(0xade0f, 0xade11, "floating continent statues gestahl has goose bumps dialog", field.NOP())

        space = Reserve(0xade24, 0xade24, "floating continent statues kefka raise hand")
        space.write(kefka_npc_id)

        # for some reason the animation gestahl uses does not look right with kefka, change it
        space = Reserve(0xade26, 0xade26, "floating continent statues kefka raise hand animation")
        space.write(field_entity.AnimateFrontHandsUp())

        space = Reserve(0xade28, 0xade2b, "floating continent statues don't move camera down before shooting light", field.NOP())

        space = Reserve(0xade52, 0xade52, "floating continent statues kefka turn down during light")
        space.write(kefka_npc_id)

        begin_escape = 0xae3d6
        src = [
            field.EntityAct(0x21, False,
                field_entity.SetPosition(60, 4),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.LEFT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.LEFT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.LEFT, 1),
            ),
            field.EntityAct(0x1f, False,
                field_entity.SetPosition(60, 4),
                field_entity.Move(direction.DOWN, 8),
                field_entity.Move(direction.DOWN, 8),
            ),
            field.EntityAct(field_entity.CAMERA, False,
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.Move(direction.DOWN, 3),
                field_entity.SetSpeed(field_entity.Speed.SLOW),
            ),
            field.ShakeScreen(1, True, True, True, True, True),
            field.Pause(0.25),
            field.EntityAct(gestahl_npc_id, False,
                field_entity.AnimateKnockedOut2(),
            ),
            field.EntityAct(field_entity.PARTY0, False,
                field_entity.AnimateAttacked(),
                field_entity.DisableWalkingAnimation(),
                field_entity.AnimateKnockedOut(),
                field_entity.SetSpeed(field_entity.Speed.FAST),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
                field_entity.MoveDiagonal(direction.DOWN, 1, direction.RIGHT, 1),
            ),
            field.Call(0xad033),
            field.WaitForEntityAct(0x21),
            field.WaitForEntityAct(0x1f),

            field.Branch(begin_escape)
        ]
        space = Write(Bank.CA, src, "floating continent statues shoot light at gestahl and party")
        light_shot = space.start_address

        space = Reserve(0xade5e, 0xade63, "floating continent statues light shot branch", field.NOP())
        space.write(
            field.Branch(light_shot),
        )

    def timer_mod(self):
        if self.args.event_timers_random:
            import random

            # randomize timer between 5 and 8 minutes
            seconds = random.randint(300, 480)

            space = Reserve(0xae3f6, 0xae3f7, "floating continent timer 0")
            space.write(
                (seconds * 60).to_bytes(2, "little"),
            )

            timer_display = f"{seconds // 60}:{seconds % 60:>02}"
            self.log_change(f"Timer 6:00", timer_display)

            # floating continent escape has a second timer which expires 5 seconds before game over timer
            seconds -= 5
            space = Reserve(0xae3fc, 0xae3fd, "floating continent timer 2")
            space.write(
                (seconds * 60).to_bytes(2, "little"),
            )
        elif self.args.event_timers_none:
            space = Reserve(0xae3f5, 0xae400, "floating continent timers", field.NOP())

    def nerapa_battle_mod(self):
        boss_pack_id = self.get_boss("Nerapa")

        space = Reserve(0xada48, 0xada4e, "floating continent invoke battle nerapa", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def escape_mod(self, npc_id, airship_instructions):
        space = Reserve(0xae3ec, 0xae3f0, "floating continent get outta here dialog", field.NOP())

        space = Reserve(0xa57c0, 0xa57c0, "floating continent update character created at escape")
        space.write(npc_id)
        space = Reserve(0xa57c2, 0xa57c2, "floating continent update character placed on map at escape")
        space.write(npc_id)
        space = Reserve(0xa57cc, 0xa57cc, "floating continent update character shows at escape")
        space.write(npc_id)
        space = Reserve(0xa57cd, 0xa57cd, "floating continent update character animates in at escape")
        space.write(npc_id)
        space = Reserve(0xa57e1, 0xa57e3, "floating continent skip shadow arrives at airship dialog", field.NOP())
        space = Reserve(0xa57ea, 0xa57ea, "floating continent update character who follows party to escape")
        space.write(npc_id)

        space = Reserve(0xa48cc, 0xa48cf, "floating continent do not clear shadow bits if don't wait at airship", field.NOP())

        src = [
            field.SetEventBit(event_bit.FINISHED_FLOATING_CONTINENT),
            field.StopScreenShake(),
            field.FreeScreen(),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),

            airship_instructions,
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "floating continent return to airship")
        airship_return = space.start_address

        space = Reserve(0xa48dd, 0xa48e2, "floating continent return to airship", field.NOP())
        space.write(
            field.Branch(airship_return),
        )

    def escape_character_mod(self, character):
        space = Reserve(0xa579d, 0xa57b2, "floating continent wait dialogs", field.NOP())
        self.escape_mod(character, [
            field.LoadMap(0x06, direction.DOWN, default_music = True, x = 16, y = 6, fade_in = False),
            field.RecruitAndSelectParty(character),
            field.FadeInScreen(),
        ])

    def escape_esper_mod(self, esper):
        # use guest character to give esper reward
        guest_char_id = 0x0f
        guest_char = self.maps.get_npc(0x189, guest_char_id)

        random_sprite = self.characters.get_random_esper_item_sprite()
        random_sprite_palette = self.characters.get_palette(random_sprite)

        space = Reserve(0xa579d, 0xa57b2, "floating continent wait dialogs", field.NOP())
        space.write(
            field.SetSprite(guest_char_id, random_sprite),
            field.SetPalette(guest_char_id, random_sprite_palette),
            field.RefreshEntities(),
        )

        self.escape_mod(guest_char_id, [
            field.DeleteEntity(guest_char_id),
            field.RefreshEntities(),
            field.LoadMap(0x06, direction.DOWN, default_music = True, x = 16, y = 6, fade_in = True, entrance_event = True),
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def escape_item_mod(self, item):
        # use guest character to give item reward
        guest_char_id = 0x0f
        guest_char = self.maps.get_npc(0x189, guest_char_id)

        random_sprite = self.characters.get_random_esper_item_sprite()
        random_sprite_palette = self.characters.get_palette(random_sprite)

        space = Reserve(0xa579d, 0xa57b2, "floating continent wait dialogs", field.NOP())
        space.write(
            field.SetSprite(guest_char_id, random_sprite),
            field.SetPalette(guest_char_id, random_sprite_palette),
            field.RefreshEntities(),
        )

        self.escape_mod(guest_char_id, [
            field.DeleteEntity(guest_char_id),
            field.RefreshEntities(),
            field.LoadMap(0x06, direction.DOWN, default_music = True, x = 16, y = 6, fade_in = True, entrance_event = True),
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])