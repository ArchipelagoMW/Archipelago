from ..event.event import *

class MagitekFactory(Event):
    def name(self):
        return "Magitek Factory"

    def character_gate(self):
        return self.characters.CELES

    def init_rewards(self):
        self.reward1 = self.add_reward(RewardType.ESPER | RewardType.ITEM)
        self.reward2 = self.add_reward(RewardType.ESPER | RewardType.ITEM)
        self.reward3 = self.add_reward(RewardType.CHARACTER | RewardType.ESPER)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.TALKED_TO_IFRIT_MAGITEK_FACTORY),
            field.SetEventBit(event_bit.TALKED_TO_SHIVA_MAGITEK_FACTORY),
            field.SetEventBit(event_bit.MET_SETZER_AFTER_MAGITEK_FACTORY),
        )

    def mod(self):
        self.setzer_npc_id = 0x18
        self.setzer_npc = self.maps.get_npc(0x0f0, self.setzer_npc_id)

        self.vector_mod()

        if self.reward1.type == RewardType.ESPER:
            self.ifrit_shiva_esper_mod(self.reward1.id)
        elif self.reward1.type == RewardType.ITEM:
            self.ifrit_shiva_item_mod(self.reward1.id)
        self.ifrit_shiva_battle_mod()

        if self.reward2.type == RewardType.ESPER:
            self.number024_esper_mod(self.reward2.id)
        elif self.reward2.type == RewardType.ITEM:
            self.number024_item_mod(self.reward2.id)

        self.esper_tubes_mod()

        self.minecart_mod()
        if not self.args.fixed_encounters_original:
            self.fixed_battles_mod()
        self.number128_battle_mod()

        if self.reward3.type == RewardType.CHARACTER:
            self.character_mod(self.reward3.id)
        elif self.reward3.type == RewardType.ESPER:
            self.esper_mod(self.reward3.id)
        elif self.reward3.type == RewardType.ITEM:
            self.item_mod(self.reward3.id)

        self.crane_battle_mod()
        self.after_cranes_mod()
        self.guardian_mod()

        self.log_reward(self.reward1)
        self.log_reward(self.reward2)
        self.log_reward(self.reward3)

    def vector_mod(self):
        # npcs used to block/enter magitek factory
        sympathizer_npc_id = 0x10
        north_soldier_id = 0x11
        red_soldier_id = 0x12
        south_soldier_id = 0x13

        # never show vector redish while burning, so hide npcs here instead
        # also do not conditionally branch to 0xc9540, always execute npc queues/movement
        space = Reserve(0xc9527, 0xc953f, "vector entrance event", field.NOP())
        space.add_label("NPC_QUEUES", 0xc9540)
        space.write(
            field.HideEntity(sympathizer_npc_id),
        )
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), "NPC_QUEUES"),
            )
        space.write(
            field.HideEntity(north_soldier_id),
            field.HideEntity(red_soldier_id),
            field.HideEntity(south_soldier_id),

            field.Branch("NPC_QUEUES"),
        )

        # delete jump up onto boxes event
        self.maps.delete_event(0x0f2, 43, 38)

        # delete getting caught after passing guards events
        self.maps.delete_event(0x0f2, 56, 39)
        self.maps.delete_event(0x0f2, 57, 39)
        self.maps.delete_event(0x0f2, 58, 39)

    def ifrit_shiva_mod(self, esper_item_instructions):
        ifrit_npc_id = 0x14
        shiva_npc_id = 0x15

        # delete kefka throwing ifrit/shiva into trash tile events
        self.maps.delete_event(0x107, 40, 32)
        self.maps.delete_event(0x107, 41, 32)
        self.maps.delete_event(0x107, 42, 32)

        space = Reserve(0xc7962, 0xc7964, "magitek factory well, ramuh", field.NOP())
        space = Reserve(0xc7986, 0xc7988, "magitek factory gestahl has grabbed our friends", field.NOP())
        space = Reserve(0xc7998, 0xc799a, "magitek factory they drained our powers", field.NOP())

        space = Reserve(0xc79a4, 0xc79cf, "magitek factory ifrit/shiva magicite", field.NOP())
        src = []
        if self.args.flashes_remove_most or self.args.flashes_remove_worst:
            src.append(field.FlashScreen(field.Flash.NONE))
        else:
            src.append(field.FlashScreen(field.Flash.WHITE))

        src.append([
            field.PlaySoundEffect(80),
            field.HideEntity(ifrit_npc_id),
            field.HideEntity(shiva_npc_id),
            field.RefreshEntities(),
            field.ClearEventBit(npc_bit.IFRIT_SHIVA_MAGITEK_FACTORY),
            field.ClearEventBit(event_bit.DISABLE_HOOK_MAGITEK_FACTORY),
            field.Pause(1.5),

            esper_item_instructions,
            field.SetEventBit(event_bit.GOT_IFRIT_SHIVA),
            field.FinishCheck(),
            field.Return(),
        ])
        space.write(src)

    def ifrit_shiva_esper_mod(self, esper):
        self.ifrit_shiva_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def ifrit_shiva_item_mod(self, item):
        self.ifrit_shiva_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def ifrit_shiva_battle_mod(self):
        boss_pack_id = self.get_boss("Ifrit/Shiva")

        space = Reserve(0xc7958, 0xc795e, "magitek factory invoke battle ifrit/shiva", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def number024_mod(self, esper_item_instructions):
        boss_pack_id = self.get_boss("Number 024")

        space = Reserve(0xc79ed, 0xc79f3, "magitek factory number 024 battle", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

        # use some of the receive ifrit/shiva magicite space
        space = Reserve(0xc79d0, 0xc79ec, "magitek factory ifrit/shiva magicite", field.NOP())
        space.write(
            Read(0xc79f7, 0xc79fa), # clear npc bit, fade in, wait for fade
            esper_item_instructions,
            field.SetEventBit(event_bit.DEFEATED_NUMBER_024),
            field.FinishCheck(),
            field.Return(),
        )
        receive_reward = space.start_address

        space = Reserve(0xc79f7, 0xc79fa, "magitek factory number 024 battle", field.NOP())
        space.write(
            field.Call(receive_reward),
        )

    def number024_esper_mod(self, esper):
        self.number024_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
        ])

    def number024_item_mod(self, item):
        self.number024_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
        ])

    def esper_tubes_mod(self):
        cid_npc_id = 0x1c
        elevator_npc_id = 0x22 # elevator is also an npc

        space = Reserve(0xc7ec9, 0xc7ecb, "magitek factory cid ooh, ooh", field.NOP())
        space = Reserve(0xc7ed1, 0xc7edc, "magitek factory characters turn down after screen shake", field.NOP())

        space = Reserve(0xc7ee4, 0xc7eef, "magitek factory turn party towards cid", field.NOP())
        space.write(
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Turn(direction.LEFT),
            ),
        )

        space = Reserve(0xc7ef6, 0xc7ef8, "magitek factory this is a disaster", field.NOP())
        space = Reserve(0xc7f04, 0xc7f16, "magitek factory combine party members", field.NOP())

        space = Reserve(0xc7a6c, 0xc7a84, "magitek factory tube espers and celes scene", field.NOP())
        space.add_label("CID_ENTER", 0xc7ec4)
        space.write(
            field.FadeOutSong(128),
            field.EntityAct(field_entity.PARTY0, True,
                field_entity.Move(direction.DOWN, 2),
            ),
            field.EntityAct(cid_npc_id, True,
                field_entity.SetPosition(18, 12),
            ),
            field.EntityAct(elevator_npc_id, True,
                field_entity.SetSpeed(field_entity.Speed.SLOW),
                field_entity.Move(direction.UP, 3),
            ),

            field.Branch("CID_ENTER"), # skip scene
        )

    def minecart_mod(self):
        space = Reserve(0xc7f6c, 0xc7f71, "magitek factory load elevator ride down with cid map", field.NOP())
        space = Reserve(0xc7f80, 0xc7fc2, "magitek factory elevator ride down with cid", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )
        space = Reserve(0xc8014, 0xc801a, "magitek factory move party down after elevator", field.NOP())
        space = Reserve(0xc8027, 0xc802a, "magitek factory celes i've known her", field.NOP())
        space = Reserve(0xc803a, 0xc803d, "magitek factory no! it's kefka!", field.NOP())
        space = Reserve(0xc805c, 0xc805e, "magitek factory go!!", field.NOP())

        # shorten the mine cart script, how i think this works:
        # commands 00-07 are for the mine cart ride (which parts to show? e.g. straight, left, right, up, down, fork, ...)
        # commands e0 and e1 are battles with mag roader packs, e2 is battle with number 128, and ff is end script
        # commands are executed in groups of 5, 4 ride commands then a possible ride/battle/end command
        space = Reserve(0x2e2ef2, 0x2e2faf, "magitek factory mine cart commands")
        space.copy_from(0x2e2f24, 0x2e2f3c) # ride data and battle with mag roaders
        space.copy_from(0x2e2f4c, 0x2e2f5e) # ride data (using these groups of 5 because they are more interesting, fork in the road)
        space.copy_from(0x2e2f6e, 0x2e2f6e) # battle with mag roaders
        space.copy_from(0x2e2f7e, 0x2e2f91) # ride data and battle with mag roaders
        space.copy_from(0x2e2f92, 0x2e2fa5) # ride data and battle with Number 128
        space.copy_from(0x2e2fa6, 0x2e2faf) # ride data and end script

    def fixed_battles_mod(self):
        from ..instruction import asm as asm

        # force front attacks for fixed battles
        # luckily, value chosen for front attack is one shift away from overriding battle song bit so this fits in the original space
        front_attack = [
            asm.LDA(0x04, asm.IMM8),    # load 0b0100 into a register for front attack
            asm.STA(0x00011e3, asm.LNG),# store battle type in the same place invoke_battle_type does
            asm.ASL(),                  # set bit for overriding battle song (a = 0x08)
        ]

        space = Reserve(0x2e32b0, 0x2e32b6, "magitek factory set front attack for first fixed pack", asm.NOP())
        space.write(
            front_attack,
        )

        space = Reserve(0x2e32fe, 0x2e3304, "magitek factory set front attack for second fixed pack", asm.NOP())
        space.write(
            front_attack,
        )

    def number128_battle_mod(self):
        from ..instruction import asm as asm

        boss_pack_id = self.get_boss("Number 128")
        if boss_pack_id == self.enemies.packs.get_id("Phunbaba 3"):
            # TODO: if bababreath removes a character in this battle they are somehow back in the party after the mine cart ride
            #       if phunbaba3 ends up here, replace him with phunbaba4 which does not use bababreath
            boss_pack_id = self.enemies.packs.get_id("Phunbaba 4")
        boss_formation_id = self.enemies.packs.get_formations(boss_pack_id)[0]

        # load new boss formation with battle type and save some space doing it
        space = Reserve(0x2e3316, 0x2e332d, "magitek factory set number 128 formation", asm.NOP())
        space.write(
            asm.A16(),
            asm.LDA(boss_formation_id, asm.IMM16),
            asm.STA(0x0011e0, asm.LNG), # store formation at $0011e0 (low byte) and $0011e1 (high byte)
            asm.A8(),
            asm.LDA(0x04, asm.IMM8),    # load 0b0100 into a register for front attack
            asm.STA(0x0011e3, asm.LNG), # store battle type in the same place invoke_battle_type does
        )

        # don't overwrite the battle type just set with zero
        space = Reserve(0x2e3335, 0x2e3338, "magitek factory set number 128 high background byte", asm.NOP())

        # use original game over check function after mine cart ride, the custom one cannot be used here
        # refreshing objects or updating the party leader causes a hard lock at the end of the ride (never return from black screen)
        space = Reserve(0xc80ad, 0xc80b0, "magitek factory check game over after mine cart ride", field.NOP())
        space.write(
            field.Call(field.ORIGINAL_CHECK_GAME_OVER),
        )

    def character_mod(self, character):
        self.setzer_npc.sprite = character
        self.setzer_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xc819b, 0xc81c4, "magitek factory setzer dialog and party splits", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xc81da, 0xc8302, "magitek factory add char and kefka cranes scene", field.NOP())
        space.write(
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.RecruitAndSelectParty(character),
            field.Branch(space.end_address + 1), # skip nops
        )

    def esper_mod(self, esper):
        self.setzer_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.setzer_npc.palette = self.characters.get_palette(self.setzer_npc.sprite)

        space = Reserve(0xc819b, 0xc8302, "magitek factory add char and kefka cranes scene", field.NOP())
        space.write(
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.Branch(space.end_address + 1), # skip nops
        )

    def item_mod(self, item):
        self.setzer_npc.sprite = self.characters.get_random_esper_item_sprite()
        self.setzer_npc.palette = self.characters.get_palette(self.setzer_npc.sprite)

        space = Reserve(0xc819b, 0xc8302, "magitek factory add char and kefka cranes scene", field.NOP())
        space.write(
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.Branch(space.end_address + 1),  # skip nops
        )

    def crane_battle_mod(self):
        boss_pack_id = self.get_boss("Cranes")

        battle_type = field.BattleType.FRONT
        battle_background = 48 # airship, right
        if boss_pack_id == self.enemies.packs.get_id("Cranes"):
            battle_type = field.BattleType.PINCER
            battle_background = 37 # airship, center

        space = Reserve(0xb40e5, 0xb40eb, "magitek factory invoke battle cranes", field.NOP())
        space.write(
            field.InvokeBattleType(boss_pack_id, battle_type, battle_background),
        )

    def after_cranes_mod(self):
        space = Reserve(0xb3ff1, 0xb40e0, "magitek factory scene before crane fight", field.NOP())
        space.write(
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.IncrementEventWord(event_word.CHECKS_COMPLETE), # objectives finished after battle
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xc8303, 0xc8304, "after magitek factory do not delete vector townspeople", field.NOP())

        space = Reserve(0xc8319, 0xc831f, "after magitek factory do not call go to zozo scenes", field.Return())
        space.write(
            field.LoadMap(0x00, direction.DOWN, default_music = True, x = 120, y = 188, airship = True),
            vehicle.End(),
        )

    def guardian_mod(self):
        # guardian is made up of 9 npcs, remove them all
        for guardian_npc_id in range(0x20, 0x29):
            self.maps.remove_npc(0x0f2, 0x20)

        # delete the events that trigger guardian battle
        self.maps.delete_event(0x0f2, 30, 59)
        self.maps.delete_event(0x0f2, 31, 60)
        self.maps.delete_event(0x0f2, 32, 60)
        self.maps.delete_event(0x0f2, 33, 60)
        self.maps.delete_event(0x0f2, 34, 59)
