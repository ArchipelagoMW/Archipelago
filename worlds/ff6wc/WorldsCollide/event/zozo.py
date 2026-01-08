from ..event.event import *

class Zozo(Event):
    def name(self):
        return "Zozo"

    def character_gate(self):
        return self.characters.TERRA

    def init_rewards(self):
        self.reward = self.add_reward(RewardType.CHARACTER | RewardType.ESPER | RewardType.ITEM)

    def init_event_bits(self, space):
        space.write(
            field.SetBattleEventBit(battle_bit.ENABLE_MORPH_COMMAND),
            field.SetEventBit(event_bit.SAW_MADUIN_DIE),
            field.ClearEventBit(npc_bit.ESPER_TERRA_ZOZO),
        )
        if self.reward.type == RewardType.CHARACTER or self.reward.type == RewardType.ITEM:
            space.write(
                field.SetEventBit(npc_bit.RAMUH_ZOZO),
                field.ClearEventBit(npc_bit.RAMUH_MAGICITE_ZOZO),
            )
        if self.reward.type == RewardType.ESPER:
            space.write(
                field.ClearEventBit(npc_bit.RAMUH_ZOZO),
                field.SetEventBit(npc_bit.RAMUH_MAGICITE_ZOZO),
            )

    def mod(self):
        self.ramuh_npc_id = 0x11
        self.ramuh_npc = self.maps.get_npc(0x0e2, self.ramuh_npc_id)
        self.ramuh_magicite_npc_id = 0x12

        if self.args.character_gating:
            self.add_gating_condition()

        self.dadaluma_battle_mod()

        if self.reward.type == RewardType.CHARACTER:
            self.character_mod(self.reward.id)
        elif self.reward.type == RewardType.ESPER:
            self.esper_mod(self.reward.id)
        elif self.reward.type == RewardType.ITEM:
            self.item_mod(self.reward.id)

        self.log_reward(self.reward)

        self.set_clock_mod()

        # always randomize clock
        time = self.randomize_clock_mod()
        self.log_change("6:10:50", time)

    def add_gating_condition(self):
        src = [
            Read(0xaf004, 0xaf006), # change background layer

            field.ReturnIfEventBitSet(event_bit.character_recruited(self.character_gate())),
            field.HideEntity(self.ramuh_npc_id),
            field.HideEntity(self.ramuh_magicite_npc_id),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo entrance event character gate")
        entrance_event = space.start_address

        self.maps.set_entrance_event(0x0e2, entrance_event - EVENT_CODE_START)

    def dadaluma_battle_mod(self):
        space = Reserve(0xa96a9, 0xa96ab, "dadaluma good day, gentle folks dialog", field.NOP())

        boss_pack_id = self.get_boss("Dadaluma")

        space = Reserve(0xa96ae, 0xa96b4, "zozo invoke battle dadaluma", field.NOP())
        space.write(
            field.InvokeBattle(boss_pack_id),
        )

    def character_mod(self, character):
        self.ramuh_npc.sprite = character
        self.ramuh_npc.palette = self.characters.get_palette(character)

        src = [
            field.SetEventBit(event_bit.GOT_ZOZO_REWARD),
            field.RecruitAndSelectParty(character),
            field.ClearEventBit(npc_bit.RAMUH_ZOZO),
            field.HideEntity(self.ramuh_npc_id),
            field.RefreshEntities(),
            field.FadeInScreen(),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo character reward")
        recruit_character = space.start_address

        self.ramuh_npc.set_event_address(recruit_character)

    def esper_mod(self, esper):
        space = Reserve(0xaa7fd, 0xaa803, "receive ramuh esper dialog", field.NOP())
        space = Reserve(0xaa808, 0xaa808, "zozo pause before receiving esper", field.NOP())

        src = [
            field.Dialog(self.espers.get_receive_esper_dialog(esper)),
            field.AddEsper(esper, sound_effect = False),
            field.SetEventBit(event_bit.GOT_ZOZO_REWARD),
            field.FinishCheck(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo receive esper")
        receive_esper = space.start_address

        space = Reserve(0xaa820, 0xaa824, "zozo call receive esper", field.NOP())
        space.write(
            field.Call(receive_esper),
        )

        space = Reserve(0xaa829, 0xaa88e, "zozo update event bits", field.NOP())
        space.write(
            field.Return(),
        )

    def item_mod(self, item):
        self.ramuh_npc.sprite = 106
        self.ramuh_npc.palette = 6
        self.ramuh_npc.split_sprite = 1
        self.ramuh_npc.direction = direction.DOWN

        src = [
            field.AddItem(item),
            field.Dialog(self.items.get_receive_dialog(item)),
            field.SetEventBit(event_bit.GOT_ZOZO_REWARD),
            field.FinishCheck(),

            field.ClearEventBit(npc_bit.RAMUH_ZOZO),
            field.HideEntity(self.ramuh_npc_id),
            field.RefreshEntities(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo item reward")
        receive_item = space.start_address

        self.ramuh_npc.set_event_address(receive_item)

    def set_clock_mod(self):
        src = [
            Read(0xa9744, 0xa9747), # shake screen, set multipurpose map bit

            field.SetEventBit(event_bit.SET_ZOZO_CLOCK),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "zozo successsfully set clock check objectives")
        check_objectives = space.start_address

        space = Reserve(0xa9744, 0xa9747, "zozo successfully set clock", field.NOP())
        space.write(
            field.Call(check_objectives),
        )

    def randomize_clock_mod(self):
        import random, copy
        from collections import namedtuple

        # original clues:
        #1046 'It's now 2:00.<end>'
        #1047 'Time?<line>It's 4:00.<end>'
        #1048 'You can trust me!<line>It's 8:00.<end>'
        #1049 '10:00!<line>Time to go home!<end>'
        #1050 'It's already 12:00.<end>'
        #1057 'Clock's second hand's pointin' at 30.<end>'
        #1061 'The second hand of my watch is pointing at four.<end>'

        number_string = {
            2 : "two",
            4 : "four",
            6 : "six",
            8 : "eight",
            10 : "ten",
            12 : "twelve",
        }

        class Option:
            def __init__(self, name, values, format_string):
                self.name = name
                self.values = values
                self.format_string = format_string

            def __str__(self):
                return f"{self.name} {self.values} {self.format_string}"
        options = [
            Option("hour", [2, 4, 6, 8, 10, 12], "{}:00"),
            Option("minute", [10, 20, 30, 40, 50], "0:{}"),
            Option("second", [10, 20, 30, 40, 50], "0:00:{}"),
        ]

        # choose a correct solution
        time_string = ""
        solution_indices = []
        solution_values = []
        for option in options:
            solution_index = random.randint(0, len(option.values) - 1)
            solution_indices.append(solution_index)
            solution_values.append(option.values[solution_index])

            time_string += str(option.values[solution_index]) + ":"
            del option.values[solution_index]
        time_string = time_string[:-1]

        # update clock's correct dialog choices
        DialogBranchData = namedtuple("DialogBranchData", ["dialog_id", "correct_destination", "incorrect_destination",
                                                           "start_address", "end_address", "description"])
        dialog_branches = [
            DialogBranchData(0x041d, 0xa96e2, 0xa96e4, 0xa96cb, 0xa96e1, "zozo clock select hour dialog branch"),
            DialogBranchData(0x041f, 0xa96f8, 0xa96fa, 0xa96e4, 0xa96f7, "zozo clock select minute dialog branch"),
            DialogBranchData(0x0420, 0xa970e, 0xa9716, 0xa96fa, 0xa970d, "zozo clock select second dialog branch"),
        ]

        for index, dialog_branch in enumerate(dialog_branches):
            destinations = [dialog_branch.incorrect_destination] * (len(options[index].values) + 1)
            destinations[solution_indices[index]] = dialog_branch.correct_destination

            space = Reserve(dialog_branch.start_address, dialog_branch.end_address, dialog_branch.description)
            space.write(
                field.DialogBranch(dialog_branch.dialog_id, *destinations),
            )

        # first clue gives either the hour, minute, or second
        digit_index = random.randint(0, len(options) - 1)
        solution_value = solution_values[digit_index]
        self.dialogs.set_text(1058, (f"That clock has no {options[digit_index].name} hand."
                                      " It's never pointing to the right time anyway!<end>"))
        if options[digit_index].name == "minute" or options[digit_index].name == "second":
            solution_value = solution_value // 5
        self.dialogs.set_text(1066, f"Hand's pointin' at the {number_string[solution_value]}.<end>")
        del options[digit_index]
        del solution_values[digit_index]

        # second clue removes half (or half - 1) of the possibilities from one of the two remaining digits
        digit_index = random.randint(0, len(options) - 1)
        if options[digit_index].name == "hour":
            divisor = 4
        else:
            divisor = 20
        if solution_values[digit_index] % divisor != 0:
            options[digit_index].values = [value for value in options[digit_index].values if value % divisor != 0]
            self.dialogs.set_text(1059, f"The {options[digit_index].name}s? They're divisible by {divisor}!<end>")
        else:
            options[digit_index].values = [value for value in options[digit_index].values if value % divisor == 0]
            self.dialogs.set_text(1059, f"The {options[digit_index].name}s? They're not divisible by {divisor}!<end>")

        # remaining clues exclude one value each
        Clue = namedtuple("Clue", ["dialog_id", "dialog_string", "string_format"])
        clues = [
            Clue(1046, "It's now {}.<end>", "clock"),
            Clue(1047, "Time?<line>It's {}.<end>", "clock"),
            Clue(1048, "You can trust me!<line>It's {}.<end>", "clock"),
            Clue(1049, "{}!<line>Time to go home!<end>", "clock"),
            Clue(1050, "It's already {}.<end>", "clock"),
            Clue(1057, "Clock's {} hand's pointin' at {}.<end>", "number"),
            Clue(1061, "The {} hand of my watch is pointing at {}.<end>", "number_string"),
        ]

        single_clue_options = copy.deepcopy(options)
        for clue in clues:
            if not options:
                # if more clues than options, allow multiple clues for same value
                options = copy.deepcopy(single_clue_options)

            digit_index = random.randint(0, len(options) - 1)
            value_index = random.randint(0, len(options[digit_index].values) - 1)

            digit = options[digit_index].name
            value = options[digit_index].values[value_index]
            if clue.string_format == "number":
                self.dialogs.set_text(clue.dialog_id, clue.dialog_string.format(digit, value))
            elif clue.string_format == "number_string":
                if options[digit_index].name == "hour":
                    value = number_string[value]
                else:
                    value = number_string[value // 5]
                self.dialogs.set_text(clue.dialog_id, clue.dialog_string.format(digit, value))
            else:
                value = options[digit_index].format_string.format(value)
                self.dialogs.set_text(clue.dialog_id, clue.dialog_string.format(value))

            if len(options[digit_index].values) == 1:
                del options[digit_index]
            else:
                del options[digit_index].values[value_index]

        return time_string
