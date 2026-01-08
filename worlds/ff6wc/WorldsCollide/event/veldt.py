from ..event.event import *
from ..event.veldt_helpers import *

# NOTE: if gau in menus he has been recruited (will not change based on leap status)
#       if gau not in menus he has not been recruited yet
#       if gau is available it also means he is not leapt
#       if gau is not available he can either be leapt or not recruited yet

class Veldt(Event):
    def name(self):
        return "Veldt"

    def character_gate(self):
        return self.characters.GAU

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER)

    def init_event_bits(self, space):
        # abusing init event bits space here...
        if self.reward.type != RewardType.CHARACTER:
            # use guest character slot to show up after battle for esper reward
            # NOTE: do not use CHARACTER_COUNT for the character id here
            #       CHARACTER_COUNT is banon and causes a game over if you hit him too hard to make him run
            self.char = self.characters.CHARACTER_COUNT + 1
            space.write(
                field.SetProperties(self.char, self.char),
            )

    def mod(self):
        self.leap_char = self.characters.get_characters_with_command("Leap")
        if not self.leap_char:
            self.leap_char = self.characters.GAU
        else:
            self.leap_char = self.leap_char[0]

        if self.reward.type == RewardType.CHARACTER:
            self.char = self.reward.id
            self.sprite = self.reward.id
        elif self.reward.type == RewardType.ESPER:
            import random
            self.sprite = random.choice([14, 15, 19, 20])
        elif self.reward.type == RewardType.ITEM:
            self.char = self.characters.CHARACTER_COUNT + 1
            self.sprite = self.characters.CHARACTER_COUNT + 1

        self.leap_mod()
        self.gau_ai_mod()
        self.check_gau_appear_conditions()
        self.queue_gau_event()
        self.add_gau_party()

        self.veldt_initialize_mod()
        self.battle_events_mod()

        self.log_reward(self.reward)

    def leap_mod(self):
        from ..data import event_word as event_word
        characters_available_address = event_word.address(event_word.CHARACTERS_AVAILABLE)

        space = Reserve(0x21d0d, 0x21d11, "veldt if gau not available script command", asm.NOP())
        space.write(
            asm.LDA(char_available_event_byte(self.leap_char), asm.ABS),
            asm.BIT(char_available_event_bit(self.leap_char), asm.IMM8),    # is leap_char available?
        )

        space = Reserve(0x248e1, 0x248e1, "veldt remove gau from party after leap")
        space.write(self.leap_char)

        src = [
            asm.LDA(char_available_event_bit(self.leap_char), asm.IMM8),
            asm.TRB(char_available_event_byte(self.leap_char), asm.ABS),    # clear leap_char available bit
            asm.DEC(characters_available_address, asm.ABS),                 # decrement available chars count
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "veldt set gau unavailable after leap")
        set_unavailable = space.start_address

        space = Reserve(0x248e6, 0x248ea, "veldt mark gau unavailable after leap", asm.NOP())
        space.write(
            asm.JSR(set_unavailable, asm.ABS),
        )

    def gau_ai_mod(self):
        # 32 ai data elements, 24 bytes each, starting at 0xd0fd00
        # gau returning from veldt is element 0x0a and is in battle ram at $2f4a
        # 0xf0 = 0x0a * 24
        self.gau_returns_ai_data_offset = 0xf0

        # for 8 bit lda $d0fd04
        space = Allocate(Bank.C2, 34, "veldt load hide/flip/char function", asm.NOP())
        self.load_sprite_function = space.next_address
        space.write(
            asm.CPX(self.gau_returns_ai_data_offset, asm.IMM16),    # gau returning event?
            asm.BNE("LOAD_CHAR"),

            branch_if_char_not_recruited(self.leap_char, "CHECK_CHAR_RECRUITED"),
            branch_if_char_not_available(self.leap_char, "LOAD_CHAR"),
            "CHECK_CHAR_RECRUITED",
        )
        if self.reward.type == RewardType.CHARACTER:
            space.write(
                branch_if_char_available(self.char, "LOAD_CHAR"),
            )
        else:
            space.write(
                branch_if_event_bit_set(event_bit.VELDT_REWARD_OBTAINED, "LOAD_CHAR"),
            )
        space.write(
            "LOAD_HIDE_FLIP_CHAR",
            asm.LDA(0x80 | 0x40 | self.char, asm.IMM8), # a = (hide_bit | flip_bit | self.char)
            asm.RTS(),

            "LOAD_CHAR",
            asm.LDA(0xd0fd04, asm.LNG_X),
            asm.RTS(),
        )
        space = Reserve(0x22ffe, 0x23001, "call veldt load hide/flip/actor function", asm.NOP())
        space.write(
            asm.JSR(self.load_sprite_function, asm.ABS),
        )

        # for 16 bit lda $d0fd04
        space = Allocate(Bank.C2, 39, "veldt load hide/flip/char/sprite function", asm.NOP())
        self.load_sprite_function16 = space.next_address
        space.write(
            asm.CPX(self.gau_returns_ai_data_offset, asm.IMM16),    # gau returning event?
            asm.BNE("LOAD_CHAR"),

            branch_if_char_not_recruited(self.leap_char, "CHECK_CHAR_RECRUITED"),
            branch_if_char_not_available(self.leap_char, "LOAD_CHAR"),
            "CHECK_CHAR_RECRUITED",
        )
        if self.reward.type == RewardType.CHARACTER:
            space.write(
                branch_if_char_available(self.char, "LOAD_CHAR"),
            )
        else:
            space.write(
                branch_if_event_bit_set(event_bit.VELDT_REWARD_OBTAINED, "LOAD_CHAR"),
            )
        space.write(
            "LOAD_HIDE_FLIP_CHAR",
            asm.A16(),
            asm.LDA((0x80 | 0x40 | self.char) | (self.sprite << 8), asm.IMM16),
            asm.RTS(),

            "LOAD_CHAR",
            asm.A16(),
            asm.LDA(0xd0fd04, asm.LNG_X),
            asm.RTS(),
        )
        space = Reserve(0x23028, 0x2302d, "call veldt load hide/flip/actor/char function", asm.NOP())
        space.write(
            asm.JSR(self.load_sprite_function16, asm.ABS),
        )

        space = Reserve(0x2be79, 0x2be7c, "call veldt load hide/flip/actor function", asm.NOP())
        space.write(
            asm.JSR(self.load_sprite_function, asm.ABS),
        )

        space = Reserve(0x2be94, 0x2be97, "call veldt load hide/flip/actor function", asm.NOP())
        space.write(
            asm.JSR(self.load_sprite_function, asm.ABS),
        )

        space = Reserve(0x2bea1, 0x2bea4, "call veldt load hide/flip/actor function", asm.NOP())
        space.write(
            asm.JSR(self.load_sprite_function, asm.ABS),
        )

    def check_gau_appear_conditions(self):
        space = Allocate(Bank.C2, 42, "veldt check if gau can return function", asm.NOP())
        return_check_function = space.next_address
        space.write(
            branch_if_char_not_recruited(self.leap_char, "CHECK_CHAR_RECRUITED"),
            branch_if_char_not_available(self.leap_char, "CHECK_ENEMY/CHAR_SLOTS"),
            "CHECK_CHAR_RECRUITED",
        )
        if self.reward.type == RewardType.CHARACTER:
            space.write(
                branch_if_char_available(self.char, "CLEAR_GAU/CHAR_CAN_RETURN"),
            )
        else:
            space.write(
                branch_if_event_bit_set(event_bit.VELDT_REWARD_OBTAINED, "CLEAR_GAU/CHAR_CAN_RETURN"),
            )
        space.write(
            "CHECK_ENEMY/CHAR_SLOTS",
            asm.LDA(0x3f4b, asm.ABS),               # a = id of enemy #6 in formation
            asm.INC(),
            asm.BNE("CLEAR_GAU/CHAR_CAN_RETURN"),   # branch if an enemy is in the gau slot
            asm.LDA(0xfc, asm.DIR),                 # a = number characters in party
            asm.CMP(0x04, asm.IMM8),
            asm.BLT("GAU/CHAR_CAN_RETURN"),         # branch if fewer than 4 characters in party

            "CLEAR_GAU/CHAR_CAN_RETURN",
            asm.LDA(0x01, asm.IMM8),
            asm.TRB(0x11e4, asm.ABS),               # clear char/gau as available to return on veldt
            asm.RTS(),

            "GAU/CHAR_CAN_RETURN",
            asm.JMP(self.load_sprite_function, asm.ABS),
        )

        space = Reserve(0x22fb0, 0x22fc7, "call veldt check if gau can return function", asm.NOP())
        space.write(
            asm.JSR(return_check_function, asm.ABS),
        )

    def queue_gau_event(self):
        # overwrite gau return/recruit branch and shadow leaving check
        space = Reserve(0x24840, 0x2488b, "gau return/char recruit check", asm.NOP())
        space.add_label("QUEUE_BATTLE_EVENT", 0x248c4)
        space.add_label("QUEUE_GAU_EVENT", 0x248ce)
        space.add_label("QUEUE_APPEAR_EVENT", 0x248d1)  # same as QUEUE_GAU_EVENT except skip loading event $1b
        space.write(
            asm.JSR(0x4b5a, asm.ABS),   # a = random number 0-255
            asm.CMP(0xa0, asm.IMM8),
            asm.BGE("SKIP_GAU_EVENT"),  # branch if random number >= 0xa0 (about 3/8 chance)

            asm.LDA(0x01, asm.IMM8),
            asm.TRB(0x11e4, asm.ABS),   # test and mark gau as not available to return from leap
            asm.BEQ("SKIP_GAU_EVENT"),  # branch if true gau/char can not return from leap
        )
        if self.args.character_gating:
            space.write(
                branch_if_char_not_recruited(self.character_gate(), "SKIP_GAU_EVENT"),
            )
        space.write(
            branch_if_char_not_recruited(self.leap_char, "CHAR_RECRUITED_CHECK"),
            branch_if_char_available(self.leap_char, "CHAR_RECRUITED_CHECK"),

            asm.LDX(0x3000 + self.leap_char, asm.ABS),  # x = leap character's slot
            asm.LDA(0x02, asm.IMM8),
            asm.TSB(0x3ebd, asm.ABS),       # set gau already recruited bit (so dried meat is not required)
            asm.LDA(0x3018, asm.ABS_X),     # a = leap character's mask (1, 2, 4, or 8)
            asm.BRA("QUEUE_GAU_EVENT"),

            "CHAR_RECRUITED_CHECK",
        )
        if self.reward.type == RewardType.CHARACTER:
            space.write(
                branch_if_char_available(self.char, "SKIP_GAU_EVENT"),
            )
        else:
            space.write(
                branch_if_event_bit_set(event_bit.VELDT_REWARD_OBTAINED, "SKIP_GAU_EVENT"),
            )
        space.write(
            asm.LDX(0x3000 + self.char, asm.ABS),   # x = char's character slot
            asm.LDA(0x02, asm.IMM8),
            asm.TRB(0x3ebd, asm.ABS),       # clear gau already recruited bit (dried meat required for char)
            asm.LDA(0x3018, asm.ABS_X),     # a = character's mask (1, 2, 4, or 8)

            # same as $c248ce except queue battle event $19 instead of $1b
            asm.LDX(0x19, asm.IMM8),        # load battle event $19 to have char appear after battle
            asm.BRA("QUEUE_APPEAR_EVENT"),  # queue char appear event

            "SKIP_GAU_EVENT",
        )

        # swap instructions for gau appearing to allow jumping to it and having a different battle event queued
        space = Reserve(0x248ce, 0x248d0, "veldt gau appears after battle, load character mask", asm.NOP())
        space.copy_from(0x248dc, 0x248dd) # ldx #$1b

        space = Reserve(0x248dc, 0x248dd, "veldt gau appears after battle load battle event id", asm.NOP())

    def add_gau_party(self):
        from ..data import event_word as event_word

        space = Allocate(Bank.C2, 56, "veldt recruit gau/char function", asm.NOP())
        recruit_function = space.next_address
        space.write(
            branch_if_char_not_recruited(self.leap_char, "RECRUIT_CHAR"),
            branch_if_char_not_available(self.leap_char, "RECRUIT_GAU"),

            "RECRUIT_CHAR",
        )
        if self.reward.type == RewardType.CHARACTER:
            from ..instruction import c0 as c0
            from ..memory.space import START_ADDRESS_SNES

            recruit_character_address = START_ADDRESS_SNES + c0.recruit_character
            space.write(
                asm.LDA(ram_event_bit(event_bit.VELDT_REWARD_OBTAINED), asm.IMM8),
                asm.TSB(ram_event_byte(event_bit.VELDT_REWARD_OBTAINED), asm.ABS),
                asm.LDA(0x3ed9, asm.ABS_Y), # a = character id
                asm.STA(0xeb, asm.DIR),     # store character id as arg for recruit_character event command
                asm.PHB(),                  # push data bank register
                asm.LDA(0x00, asm.IMM8),    # a = desired data bank register for recruit_character
                asm.PHA(),                  # push desired dbr onto stack
                asm.PLB(),                  # pull from stack into data bank register
                asm.PHP(),
                asm.XY16(),
                asm.PHY(),                  # push enemy script command target
                asm.JSL(recruit_character_address),
                asm.PLY(),                  # restore enemy script command target
                asm.PLP(),
                asm.PLB(),                  # restore data bank register
                asm.RTS(),
            )
        elif self.reward.type == RewardType.ESPER:
            espers_found_address = event_word.address(event_word.ESPERS_FOUND)
            space.write(
                asm.LDA(ram_event_bit(event_bit.VELDT_REWARD_OBTAINED), asm.IMM8),
                asm.TSB(ram_event_byte(event_bit.VELDT_REWARD_OBTAINED), asm.ABS),
                asm.LDA(esper_available_bit(self.reward.id), asm.IMM8),
                asm.TSB(esper_available_byte(self.reward.id), asm.ABS),
                asm.INC(espers_found_address, asm.ABS),

                # load 0xff into a to let calling function know esper was obtained
                asm.LDA(0xff, asm.IMM8),
                asm.RTS(),
            )
        # else it's an item reward (in multi-world, this would be an AP item for someone else)
        # do NOT increment either character or esper counter, see https://github.com/Rosalie-A/Archipelago/issues/38
        else:
            space.write(
                asm.LDA(ram_event_bit(event_bit.VELDT_REWARD_OBTAINED), asm.IMM8),
                asm.TSB(ram_event_byte(event_bit.VELDT_REWARD_OBTAINED), asm.ABS),
                asm.RTS(),
            )

        characters_available_address = event_word.address(event_word.CHARACTERS_AVAILABLE)
        space.write(
            "RECRUIT_GAU",
            asm.LDA(char_available_event_bit(self.leap_char), asm.IMM8),
            asm.TSB(char_available_event_byte(self.leap_char), asm.ABS),
            asm.TSB(char_recruited_event_byte(self.leap_char), asm.ABS),
            asm.INC(characters_available_address, asm.ABS),

            asm.LDA(0x3ed9, asm.ABS_Y), # a = character id
            asm.RTS(),
        )

        space = Reserve(0x21ea9, 0x21eb0, "veldt call recruit gau/char function", asm.NOP())
        space.add_label("RETURN", 0x21ec6)
        space.write(
            asm.JSR(recruit_function, asm.ABS),
        )
        if self.reward.type != RewardType.CHARACTER:
            # skip adding character to party if esper was just obtained
            space.write(
                asm.CMP(0xff, asm.IMM8),
                asm.BEQ("RETURN"),
            )

    def veldt_initialize_mod(self):
        # make at least 1 formation available on veldt so the game doesn't
        # crash if player goes there before fighting anywhere else
        src = [
            # start with code that was replaced by function call
            # loops and initializes formation bits to 0
            Read(0xbdfd, 0xbe07),

            # now add code to set the formation bits i want
            asm.LDA(0x01, asm.IMM8), # lobo x1 formation bit
            asm.STA(0x1ddd, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "veldt formations init function")
        veldt_formations_init = space.start_address

        # veldt formation initialization code
        space = Reserve(0xbdfd, 0xbe07, "call veldt formations init function", asm.NOP())
        space.write(
            asm.JSR(veldt_formations_init, asm.ABS),
        )

    def battle_events_mod(self):
        from ..instruction import battle_event as battle_event

        # this dialog is shared between char and gau appearing after battle so remove the name
        # but keep the dialog to prevent freezes/bugs from acting too soon after they appear
        uwaoo_dialog_id = 254
        gau_char_arrives_dialog_id = uwaoo_dialog_id
        self.dialogs.set_multi_line_battle_text(uwaoo_dialog_id, 'Uwaoo~!!<wait for key><end>')

        im_gau_dialog_id = 36
        leap_char_name = self.characters.get_default_name(self.leap_char)
        self.dialogs.set_single_line_battle_text(im_gau_dialog_id, "Uwao, aooh!<wait 60 frames> I'm <" + leap_char_name + ">!<wait 60 frames><line>I'm your friend!<wait 60 frames><line>Let's travel together!<wait 60 frames><end>")

        if self.reward.type == RewardType.ESPER:
            # overwrite step 4. of rage tutorial after sabin/cyan/gau event
            esper_dialog_id = 182
            gau_char_arrives_dialog_id = esper_dialog_id
            self.dialogs.set_multi_line_battle_text(esper_dialog_id, "      Received the Magicite<line>              “" + self.espers.get_name(self.reward.id) + ".“<wait for key><end>")

        # overwrite battle event $0d, fed gau dried meat for first time
        space = Reserve(0x10aa21, 0x10ac5e, "veldt gau/char fed dried meat", battle_event.NOP())
        space.write(
            battle_event.ClearAnimations(),
            battle_event.AddCharacterAnimation(self.char, 0xd0a9fe),
            battle_event.ExecuteAnimations(),

            battle_event.OpenMultiLineDialogWindow(),
            battle_event.DisplayMultiLineDialog(gau_char_arrives_dialog_id), # Gau: Uwaoo~!!
            battle_event.IncrementChecksComplete(),
            battle_event.CloseMultiLineDialogWindow(),
            battle_event.End(),
        )

        # overwrite battle event $19 (unused blitz instructions event?)
        space = Reserve(0x10c51d, 0x10c602, "veldt char appears", battle_event.NOP())
        space.write(
            battle_event.ClearAnimations(),
            battle_event.AddCharacterAnimation(self.char, 0xd0a9fe),
            battle_event.ExecuteAnimations(),
            battle_event.AddTarget(self.char),

            # NOTE: load-bearing dialog, if it is removed it is possible for player to
            #       feed dried meat to character too soon after they appear and cause hard lock
            battle_event.OpenMultiLineDialogWindow(),
            battle_event.DisplayMultiLineDialog(uwaoo_dialog_id),
            battle_event.CloseMultiLineDialogWindow(),
            battle_event.End(),
        )

        space = Reserve(0x10a9f3, 0x10a9f3, "veldt leap character appears after battle")
        space.write(self.leap_char)
        space = Reserve(0x10a9f8, 0x10a9f8, "veldt leap character appears after battle")
        space.write(self.leap_char)

        # remove gau runs away when hit event
        # to keep it, would need to create 2 seperate events for character/esper and leaper
        space = Reserve(0x10b421, 0x10b435, "veldt gau runs away after hit battle event", battle_event.End())
