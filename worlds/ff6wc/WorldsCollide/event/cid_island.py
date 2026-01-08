from ..event.event import *

class CidIsland(Event):
    def name(self):
        return "Cid's Island"

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.SetEventBit(npc_bit.CID_WALKING_CID_HOUSE),
            field.SetEventBit(npc_bit.BIRD_CIDS_ISLAND_CLIFFS),
        )

    def mod(self):
        self.dialog_mod()
        self.house_entrance_event_mod()
        self.start_feeding_cid_mod()
        self.finish_feeding_cid_mod()
        self.fish_values_mod()
        self.cid_health_event_word_mod()

        # play 'Celes' song on cliffs map
        self.maps.properties[0x018f].song = 18

        self.cliffs_entrance_mod()
        self.cliffs_leap_mod()

    def dialog_mod(self):
        # shorten dialog to single line to start feeding event
        self.dialogs.set_text(2175, "CID: I…haven't eaten in 3 or so days, ever since I became ill.<end>")

        # take out celes's name
        self.dialogs.set_text(2176, "CID: I feel much better!<line>Thanks!<end>")
        self.dialogs.set_text(2177, "CID: I…feel I'm not going to be around much longer…<end>")
        self.dialogs.set_text(2178, "CID: Thanks for all you've done for me!<end>")
        self.dialogs.set_text(2186, "Here's a fish! Eat up!<line>CID: Oh! Yum…<line>Chomp, munch, chew…<end>")

        # leap of faith
        space = Reserve(0xa54ba, 0xa54bc, "CID: Those others who were here", field.NOP())
        space = Reserve(0xa54d2, 0xa54d4, "CELES: Everyone's gone", field.NOP())
        space = Reserve(0xa558a, 0xa558c, "Why did you nurse me back to health?", field.NOP())
        space = Reserve(0xa55b2, 0xa55b4, "CELES: A bandana???", field.NOP())
        space = Reserve(0xa55cf, 0xa55d1, "CELES: He's alive", field.NOP())

    def house_entrance_event_mod(self):
        CID_GET_IN_BED = 0xaf44c

        # move cid_died event bit check/set from entrance event to talking to cid
        # this prevents entering and completing the objective condition but leaving before finishing the objective
        space = Reserve(0xaf436, 0xaf44b, "cid's island house entrance event, walk to bed only if feeding and healthy", field.NOP())
        space.write(
            field.ReturnIfEventBitClear(event_bit.STARTED_FEEDING_CID),
            field.ReturnIfEventWordLess(event_word.CID_HEALTH, 30),
        )

    def start_feeding_cid_mod(self):
        DECREMENT_HEALTH = 0xa533f      # decrement cid's health ~every second
        TALK_TO_DEAD_CID = 0xa5419      # '...' and if not found_cid_dead then set and call finish_feeding_cid
        TALK_TO_SURVIVED_CID = 0xa5713  # 'I feel better' and if not cid_survivied then set and call finish_feeding_cid
        FEED_CID = 0xa5380              # take fish, apply to cid's health, check if survived
        src = [
            field.StartTimer(0, 64, DECREMENT_HEALTH, pause_in_menu_and_battle = True),
            field.Dialog(2175),
            field.SetEventBit(event_bit.STARTED_FEEDING_CID),
            field.SetEventBit(event_bit.multipurpose_map(0)),
            field.SetEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.ClearEventBit(npc_bit.CID_WALKING_CID_HOUSE),
            field.SetEventWord(event_word.CID_HEALTH, 120),
            field.ResetTimer(0),
            field.StartTimer(0, 64, DECREMENT_HEALTH, pause_in_menu_and_battle = True),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "cid's island start feeding cid")
        start_feeding_cid = space.start_address

        # the quest can be repeated and neither/either/both of cid_survived/cid_died may be set
        src = [
            field.BranchIfEventBitClear(event_bit.STARTED_FEEDING_CID, start_feeding_cid),
            field.BranchIfEventWordLess(event_word.CID_HEALTH, 30, TALK_TO_DEAD_CID),
            field.BranchIfEventBitSet(event_bit.FINISHED_FEEDING_CID, TALK_TO_SURVIVED_CID),

            # start timer every time cid is fed so if someone starts feeding cid, leaves, and starts
            # a new timer 0 at a different event, talking to cid will resume the hp decreasing loop
            field.StartTimer(0, 64, DECREMENT_HEALTH, pause_in_menu_and_battle = True),
            field.Branch(FEED_CID),
        ]
        space = Write(Bank.CA, src, "cid's island talk to cid, feed/survive/die")
        feed_survive_die = space.start_address

        space = Reserve(0xa5374, 0xa537f, "cid's island talk to cid, check feeding/survived/dead", field.NOP())
        space.write(
            field.Branch(feed_survive_die),
        )

    def finish_feeding_cid_mod(self):
        src = [
            field.SetEventBit(event_bit.FINISHED_FEEDING_CID),
            field.ClearEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "cid's island finish feeding cid check objectives")
        finish_feeding_cid = space.start_address

        space = Reserve(0xa541c, 0xa542b, "cid's island let cid die", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.FINISHED_FEEDING_CID),
            field.SetEventBit(event_bit.CID_DIED),
            field.ResetTimer(0),
            field.Branch(finish_feeding_cid),
        )

        Free(space.end_address + 1, 0xa54b8) # celes finds cid dead and walks north to cliff

        space = Reserve(0xa5718, 0xa5727, "cid's island saved cid", field.NOP())
        space.write(
            field.ReturnIfEventBitSet(event_bit.FINISHED_FEEDING_CID),
            field.SetEventBit(event_bit.CID_SURVIVED),
            field.SetEventBit(npc_bit.CID_WALKING_CID_HOUSE),
            field.Branch(finish_feeding_cid),
        )

        Free(space.end_address + 1, 0xa5744) # cid tells celes about raft downstairs

    def fish_values_mod(self):
        # yummy fish, just a fish, rotten fish, fish
        values = [32, 16, 4, 16]                    # original values (last two subtracted from health)
        values = [value * 2 for value in values]    # double them

        addresses = [
            0xa539c, 0xa53a8, 0xa53b4, 0xa53c0
        ]
        for index, address in enumerate(addresses):
            space = Reserve(address, address + 1, "EWFEF")
            space.write(
                values[index].to_bytes(2, "little")
            )

    def cid_health_event_word_mod(self):
        # change event word to not be shared with coral
        event_word_addresses = [
            0xa5340, 0xa539b, 0xa53a7, 0xa53b3, 0xa53bf, 0xa53c6, 0xa53d0,
            0xa53da, 0xa53e4, 0xa53ee, 0xa53f8, 0xa5402, 0xa540c,
        ]
        for address in event_word_addresses:
            space = Reserve(address, address, "cid's island cid health event word")
            space.write(
                event_word.CID_HEALTH,
            )

    def cliffs_entrance_mod(self):
        world_return = 0xa5eb4  # return, do not enter cliffs map

        space = Reserve(0xa5f39, 0xa5f47, "cid's island northern cliffs entrance tile")
        space.write(
            world.BranchIfEventBitClear(event_bit.FINISHED_FEEDING_CID, world_return),
            world.FadeLoadMap(0x18f, direction.UP, False, 8, 29,
                              fade_in = True, entrance_event = True, update_parent_map = True),
            field.Return(),
        )

    def cliffs_leap_mod(self):
        # shorten pauses
        space = Reserve(0xa54d5, 0xa54d6, "cid's island cliffs pause", field.NOP())
        space = Reserve(0xa54e4, 0xa54e4, "cid's island cliffs eyes closed pause")
        space.write(0x30)
        space = Reserve(0xa554e, 0xa554e, "cid's island pause before beach")
        space.write(0x15)
        space = Reserve(0xa556a, 0xa556a, "cid's island pause before bird")
        space.write(0x15)
        space = Reserve(0xa5583, 0xa5584, "cid's island pause before character kneels", field.NOP())
        space.write(
            field.Pause(2)
        )
        space = Reserve(0xa558d, 0xa558d, "cid's island pause before question mark", field.NOP())
        space = Reserve(0xa559e, 0xa55b1, "cid's island walk around bird", field.NOP())
        space = Reserve(0xa55c7, 0xa55ce, "cid's island wait after bird flies away", field.NOP())

        # reset feeding cid
        space = Reserve(0xa55d2, 0xa55d9, "cid's island event bits after leap", field.NOP())
        space.write(
            field.ClearEventBit(event_bit.STARTED_FEEDING_CID),
            field.ClearEventBit(event_bit.FINISHED_FEEDING_CID),

            field.ClearEventBit(npc_bit.CID_IN_BED_CID_HOUSE),
            field.SetEventBit(npc_bit.CID_WALKING_CID_HOUSE),
        )
