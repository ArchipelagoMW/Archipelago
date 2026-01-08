from ..event.event import *
from ..data import npc_bit as npc_bit
from ..constants.entities import character_id
from ..data import direction
from ..data.npc import NPC

class NarsheMoogleDefense(Event):
    WOB_MAP_ID = 0x33
    MARSHAL_NPC_ID = 0x12
    LEFT_MOOGLE_NPC_ID = 0x10
    RIGHT_MOOGLE_NPC_ID = 0x11
    COLLAPSED_TERRA_NPC_ID = 0x19

    def name(self):
        return "Narshe Moogle Defense"

    def character_gate(self):
        return self.characters.MOG

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.ARVIS_INTRO), # show Arvis
            field.ClearEventBit(npc_bit.MARSHAL_NARSHE_WOB), # do not show marshal
        )

    def _add_moogle_to_party_src(self, party_idx):
        # Event logic to add a moogle to the given party

        # map of characters to replacement moogles. Our logic will be to replace any characters not in our party with their mapped moogle.
        # index is the character (0 - 14) -- note: no Terra, Locke, or Umaro replacement
        # value is the associated replacement Moogle (-1 = no replacement)
        MOOGLE_REPLACEMENT = [
            -1, #TERRA
            -1, #LOCKE
            0x12, # CYAN -> KUPEK
            0x13, # SHADOW -> KUPOP
            0x14, # EDGAR -> KUMAMA
            0x15, # SABIN -> KUKU
            0x16, # CELES -> KUTAN
            0x17, # STRAGO -> KUPAN
            0x18, # RELM -> KUSHU
            0x19, # SETZER -> KURIN
            0x0A, # MOG
            0x1A, # GAU -> KURU
            0x1B, # GOGO -> KAMOG
            -1, #UMARO
        ]

        # Goes through moogles, checking whether they're already created (either them or their associated character)
        MOOGLE_CHARACTERS = range(2,13) # range of characters replacable with moogles
        src = []
        for character_idx in MOOGLE_CHARACTERS:
            moogle_id = MOOGLE_REPLACEMENT[character_idx]
            src += [
                # Has the character been recruited (we aren't replacing them due to SetProperties)?
                field.LoadRecruitedCharacters(),
                field.BranchIfEventBitSet(event_bit.multipurpose(character_idx), f"SKIP_{character_idx}"),
                # or, is the character currently in a party (aka, they're a moogle)?
                field.LoadCreatedCharacters(),
                field.BranchIfEventBitSet(event_bit.multipurpose(character_idx), f"SKIP_{character_idx}"),
                #if not, make it a moogle
                # Make character look like a moogle
                field.SetSprite(character_idx, self.characters.get_sprite(self.characters.MOG)),
                field.SetPalette(character_idx, self.characters.get_palette(self.characters.MOG)),
                # Give it the name and properties of the moogle
                field.SetName(character_idx, moogle_id),
                field.SetEquipmentAndCommands(character_idx, moogle_id),
            ]
            if self.args.start_average_level:
                src += [
                    # Average character level via field command - example ref: CC/3A2C
                    field.AverageLevel(character_idx),
                    field.RestoreHp(character_idx, 0x7f), # restore all HP
                    field.RestoreMp(character_idx, 0x7f), # restore all MP
                ]
            src += [
                field.CreateEntity(character_idx),
                field.AddCharacterToParty(character_idx, party_idx),
                field.Branch("RETURN"), # added 1 - we're done
                f"SKIP_{character_idx}", 
            ]
        src += [
            f"RETURN",
            field.Return(),
        ]

        return src

    def add_moogles_to_parties(self):
        # Method for selecting parties or moogle replacements

        self.add_moogle_to_party = [] #note: 0-indexed whereas parties are 1 indexed in code
        # Create the needed methods for adding a moogle to a party
        for i in range(1,4):
            space = Write(Bank.CC, self._add_moogle_to_party_src(i), f"Add moogle to party {i}")
            self.add_moogle_to_party.append(space.start_address)

        src = [
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.Call(field.DELETE_CHARACTERS_NOT_IN_ANY_PARTY),
        ]
        # special logic for party 1, which will already have party members.
        # Here, we add moogles to fill in gaps
        src += [
            field.SetParty(1),
            # if shadow not in party, remove dog block from him so that KUPOP doesn't have Interceptor
            field.BranchIfCharacterInParty(self.characters.SHADOW, "HAVE_SHADOW"),
            field.RemoveStatusEffects(self.characters.SHADOW, field.Status.DOG_BLOCK),
            "HAVE_SHADOW",
            field.BranchIfPartySize(1, "ADD_3"),
            field.BranchIfPartySize(2, "ADD_2"),
            field.BranchIfPartySize(3, "ADD_1"),
            field.BranchIfPartySize(4, "ADD_0"),
            "ADD_3",
            field.Call(self.add_moogle_to_party[0]),
            "ADD_2",
            field.Call(self.add_moogle_to_party[0]),
            "ADD_1",
            field.Call(self.add_moogle_to_party[0]),
            "ADD_0",
            # this line fixes the issue in which the party appears twice if spot 0 is empty before recruiting
            field.HideEntity(field_entity.PARTY0),
        ]

        # For parties 2 and 3, just iterate 4 times each
        for party in range(2,4):
             for party_spot in range(0, 4):
                 src += [
                     field.Call(self.add_moogle_to_party[party-1])
                 ]

        src += [
            field.RefreshEntities(),
            field.Call(field.DELETE_CHARACTERS_NOT_IN_ANY_PARTY),
        ]

        space = Reserve(0xca905, 0xcaa03, "moogle defense party creation", field.NOP())
        space.write(
            src,
            field.SetEventBit(event_bit.CONTINUE_MUSIC_DURING_BATTLE), # cause locke's theme to keep playing through battles
            field.Branch(space.end_address + 1), # skip nops
        )

    def marshal_battle_mod(self):
        # Replace Marshal battle
        boss_pack_id = self.get_boss("Marshal")

        space = Reserve(0xcadac, 0xcadae, "marshal invoke battle", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id, check_game_over = False)
        )

    def terra_npc_mod(self):
        # Add an NPC to replace Terra during the chase scene in Narshe South Caves (map 50). 
        # By doing so, it allows us to change her sprite without affecting a party Terra
        self.terra_npc = NPC()
        self.terra_npc.x = 55
        self.terra_npc.y = 11
        self.terra_npc.direction = direction.UP
        self.terra_npc.speed = 0
        self.terra_npc.event_byte = npc_bit.event_byte(npc_bit.MARSHAL_NARSHE_WOB) #dual purpose with showing Marshal NPC
        self.terra_npc.event_bit = npc_bit.event_bit(npc_bit.MARSHAL_NARSHE_WOB)
        self.terra_npc_id = self.maps.append_npc(50, self.terra_npc)
        
        # Replace collapsed Terra NPC
        self.terra_collapsed_npc = self.maps.get_npc(self.WOB_MAP_ID, self.COLLAPSED_TERRA_NPC_ID)

        # ensure that the terra falls in hole event never triggers, as we're reusing the associated event bit
        space = Reserve(0xca2e5, 0xca2e5, "terra falls in hole event start")
        space.write(
            field.Return()
        )

    def marshal_test_mod(self):
        # Test code to add a Marshal battle NPC to Blackjack
        from ..data.bosses import name_pack
        src = [
            field.InvokeBattle(name_pack["Marshal"], 17),
            field.FadeInScreen(),
            field.WaitForFade(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "TEST Marshal battle")
        test_marshal_battle = space.start_address

        test_npc = NPC()
        test_npc.x = 16
        test_npc.y = 4
        test_npc.sprite = 52
        test_npc.palette = 0
        test_npc.direction = direction.DOWN
        test_npc.speed = 0
        test_npc.set_event_address(test_marshal_battle)
        self.maps.append_npc(0x6, test_npc)


        # Add Item-giver NPC
        src = []
        for i in range(0, 10):
            src += [
                field.AddItem("Potion", sound_effect = False),
                field.AddItem("Fenix Down", sound_effect = False),
                field.AddItem("Revivify", sound_effect = False),
                field.AddItem("Antidote", sound_effect = False),
                field.AddItem("Shuriken", sound_effect = False),
            ]
        src += [
            field.AddItem("Sniper", sound_effect = False),
            field.AddItem("Scimitar", sound_effect = False),
            field.AddItem("Force Armor", sound_effect = False),
            field.AddItem("Force Shld", sound_effect = False),
            field.AddItem("Flash", sound_effect = False),
            field.AddItem("Chain Saw", sound_effect = False),
            field.AddItem("Ninja Star", sound_effect = False),
            field.AddItem("Tack Star", sound_effect = False),
            field.AddItem("White Cape", sound_effect = False),
            field.AddItem("Jewel Ring", sound_effect = False),
            field.AddItem("Fairy Ring", sound_effect = False),
            field.AddItem("Barrier Ring", sound_effect = False),
            field.AddItem("MithrilGlove", sound_effect = False),
            field.AddItem("Guard Ring", sound_effect = False),
            field.AddItem("RunningShoes", sound_effect = False),
            field.AddItem("Wall Ring", sound_effect = False),
            field.AddItem("Cherub Down", sound_effect = False),
            field.AddItem("Cure Ring", sound_effect = False),
            field.AddItem("Hero Ring", sound_effect = True),
            field.Return()
        ]
        space = Write(Bank.CC, src, "Item Giver Debug NPC")
        item_giver = space.start_address

        item_giver_npc = NPC()
        item_giver_npc.x = 17
        item_giver_npc.y = 4
        item_giver_npc.sprite = 33
        item_giver_npc.palette = 2
        item_giver_npc.direction = direction.DOWN
        item_giver_npc.speed = 0
        item_giver_npc.set_event_address(item_giver)
        self.maps.append_npc(0x6, item_giver_npc)

    def marshal_npc_mod(self):
        # Change the NPC bit that activates Marshal
        marshal_npc = self.maps.get_npc(self.WOB_MAP_ID, 0x12)
        marshal_npc.event_byte = npc_bit.event_byte(npc_bit.MARSHAL_NARSHE_WOB)
        marshal_npc.event_bit = npc_bit.event_bit(npc_bit.MARSHAL_NARSHE_WOB)

    def arvis_start_mod(self):
        NARSHE_OTHER_ROOM_MAP_ID = 0x1e

        # Move Arvis NPC
        ARVIS_NPC_ID = 0x11
        arvis_npc = self.maps.get_npc(NARSHE_OTHER_ROOM_MAP_ID, ARVIS_NPC_ID)
        arvis_npc.x = 61
        arvis_npc.y = 36

        # Update Narshe: Other Rooms entrance event
        # Hide the 6 NPCs in Mayor's house that share event code with Arvis.
        src = []
        for npc_id in range(0x15, 0x1b):
            src += [
                field.HideEntity(npc_id)
            ]
        # - Hide Arvis if in WoR
        # - Hide Arvis if character gating and no Mog
        src += [
            field.BranchIfEventBitClear(event_bit.IN_WOR, "WOB"),
            field.HideEntity(ARVIS_NPC_ID),
            "WOB",
        ]
        if self.args.character_gating:
            src += [
                field.BranchIfEventBitSet(event_bit.character_recruited(self.character_gate()), "RETURN"),
                field.HideEntity(ARVIS_NPC_ID),
            ]
        src += [
            "RETURN",
            Read(0xc395a, 0xc3965), # displaced code
            field.Return(),
        ]
        space = Write(Bank.CC, src, "narshe moogle defense character gate")
        entrance_event = space.start_address

        space = Reserve(0xc395a, 0xc3965, "narshe: other rooms entrance event")
        space.write(field.Branch(entrance_event))

        # Actions after accepting
        src = [
            field.FadeOutScreen(),
            field.WaitForFade(),
            field.HideEntity(field_entity.PARTY0),
            field.SetEventBit(npc_bit.MARSHAL_NARSHE_WOB), # Show "Terra" in south caves and Marshal in battle
            field.SetEventBit(npc_bit.TERRA_COLLAPSED_NARSHE_WOB), # Show collapsed "Terra"
            field.LoadMap(0x32, direction.UP, True, 55, 11),
            field.FadeInScreen(),
            field.WaitForFade(),
            field.Branch(0xCCA2EB) # 'Got her!' scene
        ]
        space = Write(Bank.CC, src, "load narshe caves map for Terra event")
        got_her_map_change = space.start_address

        # Change Arvis Script
        prepared_dialog = 0x21 # reuse "OLD MAN: Make your way out through the mines! I’ll keep these brutes occupied!"
        self.dialogs.set_text(prepared_dialog, f"Imperial troops are searching the mines as we speak. They must have found something important!<line>Will you stop them?<line><choice> Yes<line><choice> No<end>")
        space = Reserve(0xca06f, 0xca07d, "arvis dialog", field.NOP())
        space.write(
             field.DialogBranch(prepared_dialog,
                                dest1 = got_her_map_change,
                                dest2 = field.RETURN)
        )

    def event_start_mod(self):
        #Replace Terra commands in script with new NPC for which we can manipulate the sprite/palette to match the reward
        terra_action_queues = [0xCA2EB, 0xCA2F3, 0xCA31F, 0xCA32D, 0xCA34F, 0xCA362, 0xCA371, 0xCA38B, 0xCA390, 0xCA397, 0xCA3BC]
        for address in terra_action_queues:
            space = Reserve(address, address, "terra chased action queues")
            space.write(self.terra_npc_id)

        # Clear got her dialog
        space = Reserve(0xca2f0, 0xca2f2, "dialog: Got her", field.NOP()) # 'Got her' dialog

        # clear out Terra's fall & flashback, but show "Locke" (party leader) to allow for drop-down
        space = Reserve(0xca3f9, 0xca769, "Terra fall and flashback", field.NOP())
        space.write(
            field.ShowEntity(self.COLLAPSED_TERRA_NPC_ID),
            field.HideEntity(self.MARSHAL_NPC_ID),
            field.ShowEntity(field_entity.PARTY0),
            field.RefreshEntities(),
            field.StartSong(13), # play song: Locke
            field.SetEventBit(event_bit.TEMP_SONG_OVERRIDE), # keep song playing
            field.Branch(space.end_address + 1), # skip nops
        )

        # replace overly long pause (~2 seconds) before locke drops down
        space = Reserve(0xca778, 0xca778, "pre-locke drop pause")
        space.write(field.Pause(0.50))

        # Change Locke actions to Party Leader
        locke_action_queues = [0xca76b, 0xca77b, 0xca786, 
                               0xca78e, 0xca793 , 0xca799, 0xca79f, 
                               0xca7a4, 0xca7a8, 0xca7af, 0xca7b3, 
                               0xca7b8]
                               # 0xca868 NO-OP'd below
        for address in locke_action_queues:
            space = Reserve(address, address, "locke drop down to protect terra")
            space.write(field_entity.PARTY0)

        # Speed up Marshal coming down stairs
        space = Reserve(0xca7dd, 0xca7dd, "marshal normal")
        space.write(field_entity.Speed.FAST)

        # Clear guard dialog
        space = Reserve(0xca7ee, 0xca7f0, "dialog: Now we gotcha!", field.NOP())

        # No dialog starting at cc/a85f -- reasonable point to add in the Marshal NPC
        space = Reserve(0xca85f, 0xca86f, "dialog: There's a whole bunch of 'em + Kupo", field.NOP())
        space.write(
            field.ShowEntity(self.MARSHAL_NPC_ID), # show the Marshal NPC
        )

        # Change moogles starting location to match their location at start of battle
        space = Reserve(0xca8ab, 0xca8b1, "moogle 11 moves down left", field.NOP())
        space.write(
            # just move down 1 to put at 15,13
            field.EntityAct(self.RIGHT_MOOGLE_NPC_ID, True,
                field_entity.Move(direction.DOWN, 1),
            ),
        )

        # Remove Locke-Moogle dialog - replace by moving moogle 10 down 1
        space = Reserve(0xca8b2, 0xca8d4, "dialog: Moogles! Are you saying you want to help me? + Nod + dialog: Kupo!!!", field.NOP())
        space.write(
            field.EntityAct(self.LEFT_MOOGLE_NPC_ID, True,
                field_entity.Turn(direction.DOWN),
                field_entity.Move(direction.DOWN, 1),
            )
        )

        # Remove small pause
        space = Reserve(0xca8ff, 0xca8ff, "small pause before fade", field.NOP())

        # Change logic for moogle party selection to account for any party variation
        self.add_moogles_to_parties()

        # Add party size checks around the addition of parties 2 and 3 to the map
        src = [
            field.BranchIfPartyEmpty(2, "RETURN"), # if there's no party 2, there's no party 3
            Read(0xcaa23, 0xcaa26), # displaced code -- place party 2 on map
            field.BranchIfPartyEmpty(3, "RETURN"),
            Read(0xcaa27, 0xcaa2a), # displaced code -- place party 3 on map
            "RETURN", 
            field.Return(),
        ]
        space = Write(Bank.CC, src, "Check for Party 2 and 3 sizes before placing")
        place_parties = space.start_address

        space = Reserve(0xcaa23, 0xcaa2a, "place party 2 and 3 on map", field.NOP())
        space.write(
            field.Call(place_parties),
        )

        src = [
            field.BranchIfPartyEmpty(2, "RETURN"), # if there's no party 2, there's no party 3
            Read(0xcaa3a, 0xcaa48), # displaced code -- position party 2 on map
            field.BranchIfPartyEmpty(3, "RETURN"),
            Read(0xcaa49, 0xcaa57), # displaced code -- position party 3 on map
            "RETURN",
            field.Return(),
        ]
        space = Write(Bank.CC, src, "Position party 2")
        position_parties = space.start_address

        space = Reserve(0xcaa3a, 0xcaa57, "position party 2 on map", field.NOP())
        space.write(
            field.Call(position_parties),
        )

        # Clear use of event_bit.12E (TERRA_COLLAPSED_NARHSE_WOB) and event_bit.003 (moogle defense) at cc/aaab so that we can reuse 12E 
        # and so that 003 doesn't cause issues at WoB Narshe entrance
        space = Reserve(0xcaaab, 0xcaaae, "set terra falls event bit & initiated moogle defense bit", field.NOP())

    def after_battle_mod(self, reward_instructions):
        # Loss - remove Locke's name from dialog
        self.dialogs.set_text(1744, "Couldn't hold out…!?<line>Uh oh…<end>")

        # Victory condition (marshal defeated)
        # Remove moogles from party 
        src = [ 
            reward_instructions, 

            Read(0xcade5, 0xcadec), # vanilla fade out and pan camera north

            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE), # allow song to change on map change
            field.ClearEventBit(npc_bit.MARSHAL_NARSHE_WOB), # Remove Marshal and "Terra" in south caves
            field.ClearEventBit(npc_bit.TERRA_COLLAPSED_NARSHE_WOB), # Remove collapsed Terra

            Read(0xcaded, 0xcadf2), # load map

            field.HideEntity(0x1B), # the exit block at top of map

            field.SetParty(1),
            field.Call(field.REMOVE_ALL_CHARACTERS_FROM_ALL_PARTIES),
            field.LoadRecruitedCharacters(),
        ]
        for character_idx in range(self.characters.CHARACTER_COUNT):
            src += [
                #only restore if character has not been recruited (meaning they were moogled)
                field.BranchIfEventBitSet(event_bit.multipurpose(character_idx), f"SKIP_{character_idx}"), 
                field.RemoveStatusEffects(character_idx, field.Status.FLOAT | field.Status.DARKNESS | field.Status.ZOMBIE | field.Status.POISON | field.Status.VANISH | field.Status.IMP | field.Status.PETRIFY | field.Status.DEATH),
                field.RemoveDeath(character_idx), # added due to permadeath situations to make sure the corresponding party member is alive
                field.RestoreHp(character_idx, 0x7f), # restore all HP
                field.RestoreMp(character_idx, 0x7f), # restore all MP
                # Restore character appearance, name, and properties
                field.SetSprite(character_idx, self.characters.get_sprite(character_idx)),
                field.SetPalette(character_idx, self.characters.get_palette(character_idx)),
                field.SetName(character_idx, character_idx),
                field.SetEquipmentAndCommands(character_idx, character_idx),
                f"SKIP_{character_idx}",
            ]
        src += [
            # give Shadow Interceptor again
            field.AddStatusEffects(self.characters.SHADOW, field.Status.DOG_BLOCK),
            
            field.Call(field.REFRESH_CHARACTERS_AND_SELECT_PARTY),
            field.UpdatePartyLeader(),
            field.ShowEntity(field_entity.PARTY0),
            field.RefreshEntities(),

            field.FreeScreen(),

            field.FadeInScreen(),
            field.WaitForFade(),

            field.SetEventBit(event_bit.FINISHED_MOOGLE_DEFENSE),
            field.FreeMovement(),

            # hide Arvis 
            field.ClearEventBit(npc_bit.ARVIS_INTRO),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Reserve(0xcade5, 0xcb04f, "moogle defense victory", field.NOP())
        space.write(src)

    def character_mod(self, character):
        sprite = character
        self.terra_npc.sprite = sprite
        self.terra_npc.palette = self.characters.get_palette(sprite)
        self.terra_collapsed_npc.sprite = sprite
        self.terra_collapsed_npc.palette = self.characters.get_palette(sprite)

        self.after_battle_mod([
            # Restore character appearance, name, and properties
            field.SetSprite(character, self.characters.get_sprite(character)),
            field.SetPalette(character, self.characters.get_palette(character)),
            field.SetName(character, character),
            field.SetEquipmentAndCommands(character, character),
            field.RemoveStatusEffects(character, field.Status.FLOAT | field.Status.DARKNESS | field.Status.ZOMBIE | field.Status.POISON | field.Status.VANISH | field.Status.IMP | field.Status.PETRIFY | field.Status.DEATH),
            field.RemoveDeath(character), # added due to permadeath situations to make sure the corresponding party member is alive
            field.RestoreHp(character, 0x7f), # restore all HP
            field.RestoreMp(character, 0x7f), # restore all MP
            field.RecruitCharacter(character),
        ])

    def esper_item_mod(self, esper_item_instructions):
        if self.args.character_gating:
            #Using thematic Moogle sprite for Esper/Items
            esper_item_sprite = self.characters.get_sprite(self.characters.MOG)
        else:
            # Open world -- use standard sprites
            esper_item_sprite = self.characters.get_random_esper_item_sprite()
        self.terra_npc.sprite = esper_item_sprite
        self.terra_npc.palette = self.characters.get_palette(self.terra_npc.sprite)
        self.terra_collapsed_npc.sprite = esper_item_sprite
        self.terra_collapsed_npc.palette = self.characters.get_palette(self.terra_collapsed_npc.sprite)

        self.after_battle_mod(esper_item_instructions)

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

    def mod(self):
        self.terra_npc_mod() 

        if self.args.debug:
            self.marshal_test_mod()

        self.marshal_npc_mod()

        self.arvis_start_mod()
        self.event_start_mod()
        self.marshal_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)




