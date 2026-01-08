from ..event.event import *

class MtZozo(Event):
    def name(self):
        return "Mt. Zozo"

    def character_gate(self):
        return self.characters.CYAN

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.RUST_RID_FOR_SALE),
            field.ClearEventBit(npc_bit.BOOK_OF_SECRETS_CHEST_MT_ZOZO),
        )

    def mod(self):
        # bird standing next to npc on cliff (the flying bird is a different npc)
        self.cliff_bird_npc_id = 0x10
        self.cliff_bird_npc = self.maps.get_npc(0x0b5, self.cliff_bird_npc_id)

        # npc standing out on cliff with bird
        self.cliff_cyan_npc_id = 0x12
        self.cliff_cyan_npc = self.maps.get_npc(0x0b5, self.cliff_cyan_npc_id)

        # npc that runs back in room to hide flowers
        self.room_cyan_npc_id = 0x18
        self.room_cyan_npc = self.maps.get_npc(0x0b4, self.room_cyan_npc_id)

        self.entrance_event_mod()
        self.mod_rust_rid_salesman()
        self.chest_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

    def entrance_event_mod(self):
        drunk_npc_id = 0x18

        src = [
            Read(0xaefb3, 0xaefb6), # woman laying down animate
            field.BranchIfEventBitSet(event_bit.IN_WOR, "IN_WOR"),
            field.EntityAct(drunk_npc_id, True,
                field_entity.SetPosition(50, 36)
            ),
            field.Return(),

            "IN_WOR",    # block mt zozo with drunk
            field.EntityAct(drunk_npc_id, True,
                field_entity.SetPosition(38, 58),
            ),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo entrance event wor/wob check")
        wor_wob_check = space.start_address

        space = Reserve(0xaefb3, 0xaefb6, "zozo animate woman laying down", field.NOP())
        space.write(
            field.Call(wor_wob_check),
        )

    def mod_rust_rid_salesman(self):
        # make rust rid offer one page instead of two
        self.dialogs.set_text(1063, "Rust-Rid. Yours for 1000 GP!<line><choice> Yes<line><choice> No<end>")

        space = Allocate(Bank.CA, 28, "mt zozo rust rid salesman", field.NOP())
        space.add_label("MT_ZOZO_LOCATION_DIALOG", 0xa951d)
        space.add_label("BUY_RUST_RID_OPTION", 0xa9526)
        space.write(
            field.BranchIfEventBitSet(event_bit.IN_WOR, "IN_WOR"),
            field.Dialog(1065),
            field.Return(),

            "IN_WOR",
            field.BranchIfEventBitSet(event_bit.GOT_RUST_RID, "MT_ZOZO_LOCATION_DIALOG"),
        )
        if self.args.character_gating:
            space.write(
                field.BranchIfEventBitClear(event_bit.character_recruited(self.character_gate()), "MT_ZOZO_LOCATION_DIALOG"),
            )
        space.write(
            field.Branch("BUY_RUST_RID_OPTION"),
        )
        salesman_event = space.start_address

        rust_rid_salesman_id = 0x19
        rust_rid_salesman = self.maps.get_npc(0x0dd, rust_rid_salesman_id)
        rust_rid_salesman.set_event_address(salesman_event)

        space = Reserve(0xa9513, 0xa951c, "rust rid old salesman event address", field.NOP())
        space = Reserve(0xa9520, 0xa9525, "rust rid salesman even bit branching", field.NOP())
        space.write(
            field.Return(),
        )

    def chest_mod(self):
        # book of secrets chest npc deleted, clear out space used by it
        space = Reserve(0xc42bf, 0xc42c8, "mt zozo cyan's chest locked", field.NOP())
        space = Reserve(0xc42c9, 0xc4354, "mt zozo open cyan's chest", field.NOP())
        space = Reserve(0xc4355, 0xc4361, "mt zozo find key to cyan's chest", field.NOP())

    def letter_mod(self, char_name = ""):
        letter_text = "Dear Lola,<line>I am writing to beg for your forgiveness. I am guilty of perpetuating a terrible lie…<page>I have only now realized the error of my ways. I hope I can correct a great wrong.<page>Your boyfriend, who you thought was in Mobliz, passed away some time ago. I have been writing in his stead…<page>We humans tend to allow the past to destroy our lives.<line>I implore you not to let this happen.<page>It is time to look forward, to rediscover love, and embrace the beauty of life.<page>You have so much of life left to live…"
        if char_name != "":
            letter_text += "<line><            ><" + char_name + "><end>"
        else: #https://discord.com/channels/666661907628949504/666811452350398493/1086426370910994493
            letter_text += "<end>"
        self.dialogs.set_text(2568, letter_text)

    def character_music_mod(self, character):
        from ..music.song_utils import get_character_theme

        space = Reserve(0xc4007, 0xc4008, "Play Song Cyan")
        space.write([
            field.StartSong(get_character_theme(character)),
        ])

    def character_mod(self, character):
        self.character_music_mod(character)
        self.cliff_cyan_npc.sprite = character
        self.cliff_cyan_npc.palette = self.characters.get_palette(character)

        self.room_cyan_npc.sprite = character
        self.room_cyan_npc.palette = self.characters.get_palette(character)

        space = Reserve(0xc401a, 0xc401e, "mt zozo mountain view dialog", field.NOP())
        space = Reserve(0xc402e, 0xc4030, "mt zozo CYAN!! dialog", field.NOP())
        space = Reserve(0xc403b, 0xc403d, "mt zozo CYAN: Hey!! dialog", field.NOP())

        space = Reserve(0xc4049, 0xc4095, "mt zozo cyan runs back to room", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xc409a, 0xc427a, "mt zozo scene in cyan's room", field.NOP())
        space.write(
            field.Branch(space.end_address + 1), # skip nops
        )

        space = Reserve(0xc428d, 0xc4290, "mt zozo clear flower/letter npc bit, set key npc bit", field.NOP())

        space = Reserve(0xc4291, 0xc42b4, "mt zozo add character", field.NOP())
        space.write(
            field.HideEntity(self.cliff_cyan_npc_id),
            field.RecruitAndSelectParty(character),

            field.Branch(space.end_address + 1), # skip nops
        )

        src = [
            field.UpdatePartyLeader(),
            field.FadeInScreen(8),
            field.WaitForFade(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "mt zozo character finish check")
        finish_check = space.start_address

        space = Reserve(0xc42b5, 0xc42b8, "mt zozo update leader, fade in screen", field.NOP())
        space.write(
            field.Call(finish_check),
        )

        # change the signature on the letter to lola on the table
        char_name = self.characters.get_default_name(character).upper()
        self.letter_mod(char_name)

    def esper_item_mod(self, esper_item_instructions):
        # this npc shares an event bit with outside one
        # need to remove npc so it won't show up if player exits cliffs without getting magicite/item
        self.maps.remove_npc(0x0b4, self.room_cyan_npc_id)

        space = Reserve(0xc3fec, 0xc3ff5, "mt zozo skip moving cyan npc up", field.NOP())
        space = Reserve(0xc401a, 0xc401e, "mt zozo mountain view dialog", field.NOP())

        # change which event bit is checked for whether to play cliff bird scene
        space = Reserve(0xc3fa8, 0xc3fa8, "mt zozo found cyan check")
        space.write(event_bit.FOUND_CYAN_MT_ZOZO)

        # need to keep magicite/item npc around until player interacts with it
        space = Reserve(0xc4029, 0xc42ba, "mt zozo found cyan event", field.NOP())
        space.write(
            field.SetEventBit(event_bit.FOUND_CYAN_MT_ZOZO),
            field.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            field.EntityAct(self.cliff_cyan_npc_id, True,
                field_entity.Turn(direction.DOWN),
            ),
            field.EntityAct(field_entity.CAMERA, True,
                field_entity.Move(direction.DOWN, 3),
            ),
            field.FreeScreen(),
            field.Return(),
        )

        # magicite/item taken, finish event
        add_esper_item_function = space.next_address
        space.write(
            esper_item_instructions,

            field.SetEventBit(event_bit.FINISHED_MT_ZOZO),
            field.ClearEventBit(npc_bit.CYAN_MT_ZOZO_CLIFF),
            field.FinishCheck(),
            field.Return(),
        )
        self.cliff_cyan_npc.set_event_address(add_esper_item_function)

        # when we enter cliff, if already saw bird scene, hide the bird
        cliff_entrance_event = space.next_address
        space.write(
            field.ReturnIfEventBitClear(event_bit.FOUND_CYAN_MT_ZOZO),
            field.HideEntity(self.cliff_bird_npc_id),
            field.Return(),
        )
        self.maps.set_entrance_event(0x0b5, cliff_entrance_event - EVENT_CODE_START)

        # remove the signature on the letter to lola on the table
        self.letter_mod()

    def esper_mod(self, esper):
        self.cliff_cyan_npc.sprite = 91
        self.cliff_cyan_npc.palette = 2
        self.cliff_cyan_npc.split_sprite = 1
        self.cliff_cyan_npc.direction = direction.UP

        self.esper_item_mod([
            field.AddEsper(esper),
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.HideEntity(self.cliff_cyan_npc_id),
        ])

    def item_mod(self, item):
        self.cliff_cyan_npc.sprite = 106
        self.cliff_cyan_npc.palette = 6
        self.cliff_cyan_npc.split_sprite = 1
        self.cliff_cyan_npc.direction = direction.DOWN

        self.esper_item_mod([
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.HideEntity(self.cliff_cyan_npc_id),
        ])
