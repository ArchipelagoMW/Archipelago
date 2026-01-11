# Logic module for matching overworld sprites to area bosses.




####### QUARANTINE ZONE #######
###### CURSED CODE AHEAD ######




import inspect
import random
import collections
import hashlib
import re
import binascii
import math

from ...randomizer import data
from ...randomizer.logic import flags
from ...randomizer.logic.patch import Patch

from functools import wraps

class Int4(int):
    def __new__(cls, i):
        return super(Int4, cls).__new__(cls, i & 0xf)

class Int8(int):
    def __new__(cls, i):
        return super(Int8, cls).__new__(cls, i & 0xff)

def add_special_method(cls, name):
    mname = '__{}__'.format(name)
    @wraps(getattr(cls, mname))
    def convert_to_cls(self, other):
        bound_original = getattr(super(cls, self), mname)
        return type(self)(bound_original(other))
    setattr(cls, mname, convert_to_cls)

for m in ('add', 'sub', 'mul', 'floordiv', 'mod', 'pow',
          'lshift', 'rshift', 'and', 'xor', 'or'):
    add_special_method(Int4, m)
    add_special_method(Int4, 'r' + m)  # reverse operation
    add_special_method(Int8, m)
    add_special_method(Int8, 'r' + m)  # reverse operation


global preloaded_events
preloaded_events = {}

INSERT_NORTHWEST = -75

def patch_overworld_bosses(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        randomizer.logic.patch.Patch: Patch data.

    """
    patch = Patch()

    spritePhaseEvents = []

    bank_1e_scarecrow_queues = []
    bank_1e_scarecrow_addresses = []
    bank_1f_scarecrow_queues = []
    bank_1f_scarecrow_addresses = []
    bank_20_scarecrow_queues = []
    bank_20_scarecrow_addresses = []
    bank_21_scarecrow_queues = []
    bank_21_scarecrow_addresses = []
    scarecrow_face_northwest = [0x08, 0x40, 0x80]
    scarecrow_face_northeast = [0x08, 0x40, 0x00]
    scarecrow_face_southwest = [0x08, 0x40, 0x01]
    scarecrow_face_southeast = [0x08, 0x40, 0x81]
    scarecrow_add_northwest = 0x95
    scarecrow_add_northeast = 0x97
    scarecrow_add_southwest = 0x93
    scarecrow_add_southeast = 0x91
    global bank_21_free_events
    global bank_21_free_event_lengths
    global bank_21_array_index
    global bank_21_address_index
    global bank_20_free_events
    global bank_20_free_event_lengths
    global bank_20_array_index
    global bank_20_address_index
    global bank_1F_free_events
    global bank_1F_free_event_lengths
    global bank_1F_array_index
    global bank_1F_address_index
    global bank_1E_free_events
    global bank_1E_free_event_lengths
    global bank_1E_array_index
    global bank_1E_address_index
    bank_21_free_events = [0x21300d, 0x213015, 0x21301d, 0x213668, 0x216694, 0x21663A, 0x210B7c,
                           0x2165B3]
    bank_21_free_event_lengths = [8, 8, 8, 78, 80, 89, 104, 134]
    bank_21_array_index = 0
    bank_21_address_index = 0
    bank_20_free_events = [0x200d1b, 0x20adf9, 0x20DAEE, 0x20B335, 0x200D9F, 0x20AB6F]
    bank_20_free_event_lengths = [101, 133, 208, 338, 387, 650]
    bank_20_array_index = 0
    bank_20_address_index = 0
    bank_1F_free_events = [0x1f2946, 0x1f2aa7, 0x1f1ced, 0x1f67C0]
    bank_1F_free_event_lengths = [241, 510, 561, 671]
    bank_1F_array_index = 0
    bank_1F_address_index = 0
    bank_1E_free_events = [0x1EC006]
    bank_1E_free_event_lengths = [1079]
    bank_1E_array_index = 0
    bank_1E_address_index = 0

    northeast = 77
    northwest = 75
    southwest = 93
    southeast = 91

    preloader_commands = {}

    def set_bit(v, index, x):
        """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
        mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
        v &= ~mask  # Clear the bit indicated by the mask (if x is False)
        if x:
            v |= mask  # If x was True, set the bit indicated by the mask.
        return v

    def is_set(x, n):
        return x & 1 << n != 0

    def rewrite_npc(sprite_data, shadow, solidity, y_shift, boss_location, flip_byte_3_bit_7 = None):

        NO_SHADOW = 0
        SMALL_SHADOW = 1
        MED_SHADOW = 2
        LARGE_SHADOW = 3
        BLOCK_SHADOW = 4

        output = sprite_data;
        original_data = boss_location.original_data
        output.append(original_data[2])
        byte3 = original_data[3]
        #clear out and set y shift, shadow size
        # if len(solidity) > 0:
        #     byte3 = set_bit(byte3, 0, False)
        #     byte3 = set_bit(byte3, 1, False)
        #     byte3 = set_bit(byte3, 2, False)
        #     byte3 = set_bit(byte3, 3, False)
        #     byte3 += int(bin(Int4(y_shift)), 2)
        byte3 = set_bit(byte3, 0, False)
        byte3 = set_bit(byte3, 1, False)
        byte3 = set_bit(byte3, 2, False)
        byte3 = set_bit(byte3, 3, False)
        #i programmed this part really stupidly bc i didnt anticipate having to set this bit on purpose, ever, i think this is the "cannot clone" bit
        if flip_byte_3_bit_7 == True:
            byte3 = set_bit(byte3, 7, False)
        elif flip_byte_3_bit_7 == False and not (flip_byte_3_bit_7 == None):
            byte3 = set_bit(byte3, 7, True)
        byte3 = set_bit(byte3, 5, False)
        byte3 = set_bit(byte3, 6, False)
        if shadow == MED_SHADOW or shadow == BLOCK_SHADOW:
            byte3 = set_bit(byte3, 5, True)
        if shadow == LARGE_SHADOW or shadow == BLOCK_SHADOW:
            byte3 = set_bit(byte3, 6, True)
        output.append(byte3)
        if len(solidity) > 0:
            byte4 = max(5, solidity[0]) << 4;
            byte4 += max(5, solidity[1]);
            output.append(byte4)
        else:
            output.append(original_data[4])
        byte5 = original_data[5];
        #unset shadow
        if boss_location.name in ["Croco1", "Jagger"]:
            byte5 = set_bit(byte5, 5, True)
        else:
            byte5 = set_bit(byte5, 5, False)
        if len(solidity) > 0:
            #clear out solidity Y
            byte5 = set_bit(byte5, 0, False)
            byte5 = set_bit(byte5, 1, False)
            byte5 = set_bit(byte5, 2, False)
            byte5 = set_bit(byte5, 3, False)
            byte5 = set_bit(byte5, 4, False)
            byte5 += solidity[2];
        output.append(byte5)
        output.append(original_data[6])
        return output



    def calcpointer(dec, origBytes=[]):
        if (dec > 0xFFFF):
            dec = dec % 0x10000
        origBytes.reverse()
        str = format(dec, 'x')
        hexcode = str.zfill(4)
        hexbytes = [int(hexcode[i:i + 2], 16) for i in range(0, len(hexcode), 2)]
        iterator = 0
        for by in origBytes:
            hexbytes[iterator] += by
            iterator += 1
        hexbytes.reverse()
        return hexbytes

    def approximate_dimension(num):
        base = max(num - 32, 0)
        return 32 + math.ceil(base / 8) * 8

    class PreloaderEvent:
        actions = []
        non_replace_actions = []
        event_jump = None
        original_event = None

        def __init__(self, actions, original_event, event_jump):
            self.actions = actions
            self.event_jump = event_jump
            self.original_event = original_event

    def remove_shadows(room, npcs, original_event, original_event_address):
        actions = []
        actions.extend([0x00, 0x82, 0xFD, 0x01])
        for i in range(npcs + 1):
            actions.extend([0x14 + i, 0x82, 0xFD, 0x01])
        new_preloader_event(room, actions, original_event, original_event_address)

    def new_preloader_event(room: object, actions: object, original_event: object = None,
                            event_jump: object = None) -> object:
        if room not in preloaded_events and original_event == None:
            return
        if room not in preloaded_events and original_event != None:
            preloaded_events[room] = PreloaderEvent([], event_jump, [])
            r = []
            r.append(0xD0)
            eventpointer = calcpointer(original_event)
            r.extend(eventpointer)
            r.append(0xFE)
            preloaded_events[room].event_jump.extend(r)
            preloaded_events[room].actions.append(actions)
        else:
            preloaded_events[room].actions.append(actions)

    class SpritePhaseEvent:
        global preloaded_events
        npc = 0
        sprite = 0
        mold = 0
        is_sequence_and_not_mold = True
        sequence = 0
        reverse = False
        original_event = 0
        original_event_location = 0
        level = 0
        invert_se_sw = False

        def __init__(self, npc, sprite, mold, is_sequence_and_not_mold, sequence, reverse, level, original_event,
                     original_event_location):
            self.npc = npc
            self.sprite = sprite
            self.mold = mold
            self.is_sequence_and_not_mold = is_sequence_and_not_mold
            self.sequence = sequence
            self.reverse = reverse
            self.level = level
            self.original_event = original_event
            self.original_event_location = original_event_location
            if not isinstance(self.npc, list):
                self.generate_code()
            else:
                self.generate_code_culex()

        # convert a sprite value to a pointer that can be patched in

        def generate_code_culex(self):

            returnBytes = [];
            for i in range(len(self.npc)):
                if self.level in [109, 115, 122, 120, 110, 341, 155, 113, 119, 408, 499, 501, 440, 497, 447]:
                    returnBytes.extend([(0x14 + self.npc[i]), 0x83])
                    if not self.is_sequence_and_not_mold:
                        if not self.reverse[i]:
                            returnBytes.extend([0x08, 0x18 + self.sprite, self.mold[i]])
                        else:
                            returnBytes.extend([0x08, 0x18 + self.sprite, 0x80 + self.mold[i]])
                    else:
                        if self.sequence[i] > 0:
                            if not self.reverse[i]:
                                returnBytes.extend([0x08, 0x50 + self.sprite, self.sequence[i]])
                            else:
                                returnBytes.extend([0x08, 0x50 + self.sprite, 0x80 + self.sequence[i]])
                        else:
                            if not self.reverse[i]:
                                returnBytes.extend([0x08, 0x10 + self.sprite, self.sequence[i]])
                            else:
                                returnBytes.extend([0x08, 0x10 + self.sprite, 0x80 + self.sequence[i]])
                else:
                    returnBytes.extend([(0x14 + self.npc[i]), 0x83])
                    if not self.reverse[i]:
                        returnBytes.extend([0x08, 0x50 + self.sprite, self.sequence[i]])
                    else:
                        returnBytes.extend([0x08, 0x50 + self.sprite, 0x80 + self.sequence[i]])
            if self.level not in preloaded_events:
                preloaded_events[self.level] = PreloaderEvent([], self.original_event_location, [])
                r = []
                r.append(0xD0)
                eventpointer = calcpointer(self.original_event)
                r.extend(eventpointer)
                r.append(0xFE)
                preloaded_events[self.level].event_jump.extend(r)
            preloaded_events[self.level].actions.append(returnBytes)

        def generate_code(self):
            returnBytes = [];
            if not isinstance(self.npc, list):
                npcs = [];
                npcs.append(self.npc)
            else:
                npcs = self.npc
            for npc in npcs:
                rb = [];
                if self.level in [109, 115, 122, 120, 110, 341, 155, 113, 119, 408, 499, 501, 440, 497, 447]:
                    if not self.is_sequence_and_not_mold:
                        if not self.reverse:
                            rb.extend([0x08, 0x18 + self.sprite, self.mold])
                        else:
                            rb.extend([0x08, 0x18 + self.sprite, 0x80 + self.mold])
                        initial_bytes = [(0x14 + npc), 0x80 + len(rb)]
                    else:
                        if self.sequence > 0:
                            if self.is_sequence_and_not_mold and not self.reverse:
                                rb.extend([0x08, 0x50 + self.sprite, self.sequence])
                            elif self.is_sequence_and_not_mold and self.reverse:
                                rb.extend([0x08, 0x50 + self.sprite, 0x80 + self.sequence])
                        else:
                            if self.is_sequence_and_not_mold and not self.reverse:
                                rb.extend([0x08, 0x10 + self.sprite, self.sequence])
                            elif self.is_sequence_and_not_mold and self.reverse:
                                rb.extend([0x08, 0x10 + self.sprite, 0x80 + self.sequence])
                        initial_bytes = [(0x14 + npc), 0x80 + len(rb)]
                else:
                    if self.is_sequence_and_not_mold and not self.reverse:
                        rb.extend([0x08, 0x40 + self.sprite, self.sequence])
                    elif self.is_sequence_and_not_mold and self.reverse:
                        rb.extend([0x08, 0x40 + self.sprite, 0x80 + self.sequence])
                    elif not self.is_sequence_and_not_mold and not self.reverse:
                        rb.extend([0x08, 0x08 + self.sprite, self.mold])
                    elif not self.is_sequence_and_not_mold and self.reverse:
                        rb.extend([0x08, 0x08 + self.sprite, 0x80 + self.mold])
                    initial_bytes = [(0x14 + npc), 0x80 + len(rb)]
                initial_bytes.extend(rb)
                returnBytes.extend(initial_bytes)
            if self.level not in preloaded_events:
                preloaded_events[self.level] = PreloaderEvent([], self.original_event_location, [])
                r = []
                r.append(0xD0)
                eventpointer = calcpointer(self.original_event)
                r.extend(eventpointer)
                r.append(0xFE)
                preloaded_events[self.level].event_jump.extend(r)
            preloaded_events[self.level].actions.append(returnBytes)

        def export_sprite_load(self):
            returnBytes = [];
            if not isinstance(self.npc, list):
                npcs = [];
                npcs.append(self.npc)
            else:
                npcs = self.npc
            for npc in npcs:
                returnBytes.extend([(0x14 + npc), 0x83])
                if self.is_sequence_and_not_mold and not self.reverse:
                    returnBytes.extend([0x08, 0x40 + self.sprite, self.sequence])
                elif self.is_sequence_and_not_mold and self.reverse:
                    returnBytes.extend([0x08, 0x40 + self.sprite, 0x80 + self.sequence])
                elif not self.is_sequence_and_not_mold and not self.reverse:
                    returnBytes.extend([0x08, 0x08 + self.sprite, self.mold])
                elif not self.is_sequence_and_not_mold and self.reverse:
                    returnBytes.extend([0x08, 0x08 + self.sprite, 0x80 + self.mold])
            return returnBytes

        def export_sprite_sequence(self):
            returnBytes = [];
            if not isinstance(self.npc, list):
                npcs = [];
                npcs.append(self.npc)
            else:
                npcs = self.npc
            for npc in npcs:
                if self.is_sequence_and_not_mold and not self.reverse:
                    returnBytes.extend([0x08, 0x40 + self.sprite, self.sequence])
                elif self.is_sequence_and_not_mold and self.reverse:
                    returnBytes.extend([0x08, 0x40 + self.sprite, 0x80 + self.sequence])
                elif not self.is_sequence_and_not_mold and not self.reverse:
                    returnBytes.extend([0x08, 0x08 + self.sprite, self.mold])
                elif not self.is_sequence_and_not_mold and self.reverse:
                    returnBytes.extend([0x08, 0x08 + self.sprite, 0x80 + self.mold])
            return returnBytes

    #### Logic for rewriting overworld sprites ####

    global preloaded_events
    preloaded_events = {}

    # Some sprites are not default, and need an event to set the proper mold.
    # This array will contain a set of building blocks for those sprites and where they should appear, and rewrite 1110 to control it.

    def get_directional_command(sprite, direction=1, replace=True, sequence=0, is_scarecrow=False):
        if not is_scarecrow:
            if replace:
                if direction == northeast or direction == southeast:
                    s = sprite * 1000 + sequence * 10 + 8 + 1
                elif direction == northwest or direction == southwest:
                    s = sprite * 1000 + sequence * 10 + 8
            else:
                if direction == northeast or direction == southeast:
                    s = sprite * 1000 + sequence * 10 + 1
                elif direction == northwest or direction == southwest:
                    s = sprite * 1000 + sequence * 10
            # print(s)
            return s
        else:
            if replace:
                if direction == northwest:
                    return scarecrow_face_northwest
                elif direction == northeast:
                    return scarecrow_face_northeast
                elif direction == southeast:
                    return scarecrow_face_southeast
                elif direction == southwest:
                    return scarecrow_face_southwest
            else:
                if direction == northwest:
                    return scarecrow_add_northwest
                elif direction == northeast:
                    return scarecrow_add_northeast
                elif direction == southeast:
                    return scarecrow_add_southeast
                elif direction == southwest:
                    return scarecrow_add_southwest

    def add_scarecrow_script(npc, instructions, referencing_address, is_sync, loop = True, mold = None):
        global bank_21_free_events
        global bank_21_free_event_lengths
        global bank_21_array_index
        global bank_21_address_index
        global bank_20_free_events
        global bank_20_free_event_lengths
        global bank_20_array_index
        global bank_20_address_index
        global bank_1F_free_events
        global bank_1F_free_event_lengths
        global bank_1F_array_index
        global bank_1F_address_index
        global bank_1E_free_events
        global bank_1E_free_event_lengths
        global bank_1E_array_index
        global bank_1E_address_index
        croco_special_case_position = 0

        loop_byte = 0
        if not loop:
            loop_byte = 0x10

        new_instructions = []  # belome's new action script
        length_of_instructions_being_replaced = 0  # counter of how many bytes to zero out for old action script
        for instruction in instructions:
            if instruction == scarecrow_add_northwest:
                new_instructions.extend(scarecrow_face_northwest)
            elif instruction == scarecrow_add_northeast:
                new_instructions.extend(scarecrow_face_northeast)
            elif instruction == scarecrow_add_southwest:
                new_instructions.extend(scarecrow_face_southwest)
            elif instruction == scarecrow_add_southeast:
                new_instructions.extend(scarecrow_face_southeast)
            elif not isinstance(instruction, list):
                if instruction == INSERT_NORTHWEST:
                    new_instructions.extend([0x08, 0x40 + loop_byte, 0x01])
                else:
                    if instruction < 1000:
                        plus = 0
                    else:
                        plus = math.floor(instruction / 1000)
                    if instruction < 10:
                        sequence = 0
                    else:
                        sequence = math.floor((instruction % 1000) / 10)
                    direction = instruction % 10
                    if direction >= 8:
                        direction = direction % 8
                        length_of_instructions_being_replaced += 1
                    if mold != None:
                        new_instructions.extend([0x08, 0x08 + loop_byte + plus, 0x80 * direction + mold])
                    else:
                        new_instructions.extend([0x08, 0x40 + loop_byte + plus, 0x80 * direction + sequence])
            else:
                if instruction == scarecrow_face_northwest or instruction == scarecrow_face_northeast or instruction == scarecrow_face_southwest or instruction == scarecrow_face_southeast:
                    length_of_instructions_being_replaced += 1
                else:
                    length_of_instructions_being_replaced += len(instruction)
                new_instructions.extend(instruction)
            if instruction == [0xFD, 0x3D, 0x1C, 0x8B, 0x35]:
                croco_special_case_position = len(new_instructions) - 5
        if referencing_address >= 0x210000:
            script_to_add = []
            script_to_add.extend(new_instructions)
            script_to_add.extend([0xD2])
            script_to_add.extend(calcpointer(referencing_address + 3))
            # write new instructions in an unused event
            while bank_21_address_index + len(script_to_add) > bank_21_free_event_lengths[bank_21_array_index]:
                bank_21_array_index += 1
                bank_21_address_index = 0
                if bank_21_array_index >= len(bank_21_free_event_lengths):
                    #print( '21 too long: ', world.boss_locations )
                    raise flags.FlagError("B flag error: Bank 21 needs more space! Please tell the devs about this. Paste your flag string and the seed value " + world.seed)
            patch.add_data(bank_21_free_events[bank_21_array_index] + bank_21_address_index, script_to_add)
            # replace original script with a pointer to new one
            replace_original_script = []
            replace_original_script.append(0xD2)
            replace_original_script.extend(
                calcpointer(bank_21_free_events[bank_21_array_index] + bank_21_address_index))
            for i in range(length_of_instructions_being_replaced):
                if i >= 3:
                    replace_original_script.append(0x9b)
            patch.add_data(referencing_address, replace_original_script)
            # move address memory up
            bank_21_address_index += len(script_to_add)
            # add jump to surrogate action in main action, do important actions, jump back to next address in main action
        else:
            length_of_instructions_being_replaced += 2  # action queue header

            if is_sync:
                script_to_add = [0x14 + npc, len(new_instructions)]
            else:
                script_to_add = [0x14 + npc, 0x80 + len(new_instructions)]
            script_to_add.extend(new_instructions)
            script_to_add.extend([0xD2])
            script_to_add.extend(calcpointer(referencing_address + 3))

            if referencing_address >= 0x200000:
                # write new instructions in an unused event
                while bank_20_address_index + len(script_to_add) > bank_20_free_event_lengths[bank_20_array_index]:
                    bank_20_array_index += 1
                    bank_20_address_index = 0
                    if bank_20_array_index >= len(bank_20_free_event_lengths):
                        #print( '20 too long: ', world.boss_locations )
                        raise flags.FlagError("B flag error: Bank 20 needs more space! Please tell the devs about this. Paste your flag string and the seed value " + world.seed)
                patch.add_data(bank_20_free_events[bank_20_array_index] + bank_20_address_index, script_to_add)
                # replace original script with a pointer to new one
                replace_original_script = []
                replace_original_script.append(0xD2)
                replace_original_script.extend(
                    calcpointer(bank_20_free_events[bank_20_array_index] + bank_20_address_index))
                for i in range(length_of_instructions_being_replaced):
                    if i >= 3:
                        replace_original_script.append(0x9b)
                patch.add_data(referencing_address, replace_original_script)
                # move address memory up
                bank_20_address_index += len(script_to_add)
            elif referencing_address >= 0x1f0000:
                # write new instructions in an unused event
                while bank_1F_address_index + len(script_to_add) > bank_1F_free_event_lengths[bank_1F_array_index]:
                    bank_1F_array_index += 1
                    bank_1F_address_index = 0
                    if bank_1F_array_index >= len(bank_1F_free_event_lengths):
                        #print( '1F too long: ', world.boss_locations )
                        raise flags.FlagError("B flag error: Bank 1F needs more space! Please tell the devs about this. Paste your flag string and the seed value " + world.seed)
                patch.add_data(bank_1F_free_events[bank_1F_array_index] + bank_1F_address_index, script_to_add)
                # replace original script with a pointer to new one
                replace_original_script = []
                replace_original_script.append(0xD2)
                replace_original_script.extend(
                    calcpointer(bank_1F_free_events[bank_1F_array_index] + bank_1F_address_index))

                # croco special case
                if croco_special_case_position > 0:
                    command_position = bank_1F_free_events[
                                           bank_1F_array_index] + bank_1F_address_index + croco_special_case_position + 2
                    patch.add_data(command_position + 3, calcpointer(command_position - 2))

                for i in range(length_of_instructions_being_replaced):
                    if i >= 3:
                        replace_original_script.append(0x9b)
                patch.add_data(referencing_address, replace_original_script)

                # move address memory up
                bank_1F_address_index += len(script_to_add)
            elif referencing_address >= 0x1e0000:
                # write new instructions in an unused event
                while bank_1E_address_index + len(script_to_add) > bank_1E_free_event_lengths[bank_1E_array_index]:
                    bank_1E_array_index += 1
                    bank_1E_address_index = 0
                    if bank_1E_array_index >= len(bank_1E_free_event_lengths):
                        #print( '1E too long: ', world.boss_locations )
                        raise flags.FlagError("B flag error: Bank 1E needs more space! Please tell the devs about this. Paste your flag string and the seed value " + world.seed)
                patch.add_data(bank_1E_free_events[bank_1E_array_index] + bank_1E_address_index, script_to_add)
                # replace original script with a pointer to new one
                replace_original_script = [];
                replace_original_script.append(0xD2)
                replace_original_script.extend(
                    calcpointer(bank_1E_free_events[bank_1E_array_index] + bank_1E_address_index))
                for i in range(length_of_instructions_being_replaced):
                    if i >= 3:
                        replace_original_script.append(0x9b)
                patch.add_data(referencing_address, replace_original_script)
                # move address memory up
                bank_1E_address_index += len(script_to_add)

    jinx_size = 0
    jagger_size = 0
    belome_shadow_off = False

    for location in world.boss_locations:
        if (location.name in ["HammerBros", "Croco1", "Mack", "Belome1", "Bowyer", "Croco2", "Punchinello",
                              "KingCalamari",
                              "Booster", "Bundt", "Johnny", "Yaridovich", "Belome2", "Jagger", "Jinx3",
                              "MegaSmilax", "Dodo", "Valentina", "Magikoopa", "Boomer", "CzarDragon", "AxemRangers",
                              "Countdown", "Clerk", "Manager", "Director", "Gunyolk"]):
            for enemy in location.pack.common_enemies:
                if enemy.overworld_sprite != None:
                    shuffled_boss = enemy
            #use battle sprite
            if location.name != "Gunyolk" and (
                    (approximate_dimension(shuffled_boss.sprite_height) <= approximate_dimension(location.sprite_height)
                     and approximate_dimension(shuffled_boss.sprite_width) <= approximate_dimension(
                                location.sprite_width))
                    or (location.name in ["Belome1", "Belome2",
                                          "Dodo"] and shuffled_boss.sprite_height < 80 and shuffled_boss.sprite_width < 48)):
                sprite = shuffled_boss.battle_sprite
                mold = shuffled_boss.battle_mold
                sequence = shuffled_boss.battle_sequence
                plus = shuffled_boss.battle_sprite_plus
                freeze = shuffled_boss.battle_freeze
                sesw_only = shuffled_boss.battle_sesw_only or shuffled_boss.battle_freeze
                invert_se_sw = shuffled_boss.battle_invert_se_sw
                extra_sequence = shuffled_boss.battle_extra_sequence
                push_sequence = shuffled_boss.battle_push_sequence
                push_length = shuffled_boss.battle_push_length
                northeast_mold = shuffled_boss.battle_northeast_mold
                dont_reverse_northeast = False
                if shuffled_boss.battle_sprite == shuffled_boss.overworld_sprite:
                    overworld_is_skinny = shuffled_boss.overworld_is_skinny
                    solidity = shuffled_boss.overworld_solidity
                    y_shift = shuffled_boss.overworld_y_shift
                    shadow = shuffled_boss.shadow
                else:
                    overworld_is_skinny = False
                    solidity = shuffled_boss.battle_solidity
                    y_shift = shuffled_boss.battle_y_shift
                    shadow = 3
                    belome_shadow_off = True
                if shuffled_boss.battle_sprite == shuffled_boss.overworld_sprite:
                    overworld_is_empty = shuffled_boss.overworld_is_empty
                else:
                    overworld_is_empty = False
                statue_mold = shuffled_boss.statue_mold
            #use overworld sprite
            else:
                if location.name in ["Booster", "Mack", "Croco1", "HammerBros", "Manager", "Dodo", "Belome1",
                                     "Belome2", "Valentina", "Magikoopa"] and shuffled_boss.name == "Culex":
                    freeze = True
                    mold = 0
                    stats = [shuffled_boss.attack, shuffled_boss.defense, shuffled_boss.magic_attack,
                             shuffled_boss.magic_defense]
                    crystal_colour = stats.index(max(stats))
                    if crystal_colour == 0:
                        sprite = 786
                        sequence = 1
                        statue_mold = 1
                    elif crystal_colour == 1:
                        sprite = 789
                        sequence = 0
                    elif crystal_colour == 2:
                        sprite = 789
                        sequence = 1
                        statue_mold = 1
                    elif crystal_colour == 3:
                        sprite = 786
                        sequence = 0
                elif location.name in ["Croco1"] and shuffled_boss.name == "DodoSolo":
                    sprite = 389
                    sequence = 0
                    freeze = False
                    mold = shuffled_boss.overworld_mold
                    statue_mold = shuffled_boss.statue_mold
                else:
                    sprite = shuffled_boss.overworld_sprite
                    sequence = shuffled_boss.overworld_sequence
                    freeze = shuffled_boss.overworld_freeze
                    mold = shuffled_boss.overworld_mold
                    statue_mold = shuffled_boss.statue_mold
                solidity = shuffled_boss.overworld_solidity
                y_shift = shuffled_boss.overworld_y_shift
                plus = shuffled_boss.overworld_sprite_plus
                sesw_only = shuffled_boss.overworld_sesw_only or shuffled_boss.overworld_freeze
                invert_se_sw = shuffled_boss.overworld_invert_se_sw
                extra_sequence = shuffled_boss.overworld_extra_sequence
                push_sequence = shuffled_boss.overworld_push_sequence
                push_length = shuffled_boss.overworld_push_length
                northeast_mold = shuffled_boss.overworld_northeast_mold
                dont_reverse_northeast = shuffled_boss.overworld_dont_reverse_northeast
                overworld_is_skinny = shuffled_boss.overworld_is_skinny
                overworld_is_empty = shuffled_boss.overworld_is_empty
                shadow = shuffled_boss.shadow
            fat_sidekicks = shuffled_boss.fat_sidekicks
            empty_sidekicks = shuffled_boss.empty_sidekicks

            if shuffled_boss.statue_east_shift:
                shuffled_boss.statue_east_shift = Int8(shuffled_boss.statue_east_shift)
            if shuffled_boss.statue_south_shift:
                shuffled_boss.statue_south_shift = Int8(shuffled_boss.statue_south_shift)
            if shuffled_boss.statue_west_shift:
                shuffled_boss.statue_west_shift = Int8(shuffled_boss.statue_west_shift)
            if shuffled_boss.statue_north_shift:
                shuffled_boss.statue_north_shift = Int8(shuffled_boss.statue_north_shift)
            if shuffled_boss.opposite_statue_east_shift:
                shuffled_boss.opposite_statue_east_shift = Int8(shuffled_boss.opposite_statue_east_shift)
            if shuffled_boss.opposite_statue_south_shift:
                shuffled_boss.opposite_statue_south_shift = Int8(shuffled_boss.opposite_statue_south_shift)
            if shuffled_boss.opposite_statue_west_shift:
                shuffled_boss.opposite_statue_west_shift = Int8(shuffled_boss.opposite_statue_west_shift)
            if shuffled_boss.opposite_statue_north_shift:
                shuffled_boss.opposite_statue_north_shift = Int8(shuffled_boss.opposite_statue_north_shift)



            if invert_se_sw:
                is_scarecrow = True
            else:
                is_scarecrow = False

            # print (shuffled_boss.name, invert_se_sw)


            if location.name == "HammerBros":
                #location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "HammerBro":
                    #patch.add_data(location.sprite_offset, calcpointer(sprite, [0x00, 0x68]));
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x68]), shadow, solidity, y_shift, location))
                    # for sprites that require a specific mold or sequence, change the room load events to set the proper sequence or mold first
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(7, plus, mold, sub_sequence, sequence, False, 205, 2814, 0x20f045))

            if location.name == "Croco1":
                #print(location.name + ": " + shuffled_boss.name)
                # use npc 110, set properties to match croco's
                for addr in [0x1495e1, 0x14963a, 0x14969f, 0x14b4c7, 0x14b524]:
                    patch.add_data(addr, [0xBB, 0x01])
                # replace its sprite
                if shuffled_boss.name == "CountDown":
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1DBB02, calcpointer(sprite, [0x00, 0x28]).extend([0x80, 0x22, 0x55, 0x2A, 0x00]));
                elif freeze or sesw_only:
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1DBB02, calcpointer(sprite, [0x00, 0x08]).extend([0x80, 0x22, 0x55, 0x2A, 0x00]));
                else:
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1DBB02, calcpointer(sprite, [0x00, 0x00]).extend([0x80, 0x22, 0x55, 0x2A, 0x00]));
                # need to change a lot of things in bandit's way to get every boss to work
                sub_sequence = False
                if sequence > 0:
                    sub_sequence = True
                # bandits way 1
                if sequence > 0 or mold > 0:
                    spritePhaseEvents.append(
                        SpritePhaseEvent(5, plus, mold, sub_sequence, sequence, False, 76, 1714, 0x20e8e0))
                if not freeze:
                    if extra_sequence != False:
                        patch.add_data(0x1f3bac, [0x08, 0x40, 0x80 + extra_sequence])
                    else:
                        patch.add_data(0x1f3bac, [0x08, 0x40 + plus, 0x80 + sequence])
                else:
                    patch.add_data(0x1f3bac, [0x9b, 0x9b, 0x9b])
                if invert_se_sw or freeze:  # scarecrow needs a special script
                    scarecrow_script = []
                    scarecrow_script.append([0xFD, 0x0F, 0x03, 0x10, 0xC1])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append(
                        [0x43, 0xFD, 0x9E, 0x21, 0x7F, 0x60, 0x00, 0x52, 0x04, 0xFD, 0x9E, 0x21, 0x7F, 0x6C, 0x00])
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x06, 0xFD, 0x0E, 0x10, 0xC2, 0x50, 0x06, 0x01])
                    add_scarecrow_script(5, scarecrow_script, 0x1f3bed, True)
                if freeze or sequence > 0 or (not sub_sequence and mold > 0):  # dont reset properties
                    patch.add_data(0x1f3bb1, [0x9b])
                # bandits way 2
                if sequence > 0 or mold > 0:
                    spritePhaseEvents.append(
                        SpritePhaseEvent(8, plus, mold, sub_sequence, sequence, False, 207, 1702, 0x20F07b))
                if not freeze:
                    if extra_sequence != False:
                        patch.add_data(0x1f3541, [0x08, 0x40, 0x80 + extra_sequence])
                    else:
                        patch.add_data(0x1f3541, [0x08, 0x40 + plus, 0x80 + sequence])
                else:
                    patch.add_data(0x1f3541, [0x9b, 0x9b, 0x9b])
                if invert_se_sw or freeze:  # scarecrow needs a special script
                    #####
                    #####first script
                    scarecrow_script = []
                    # clear solidity, play sound jump, pause
                    scarecrow_script.append([0x0C, 0x04, 0xFD, 0x9E, 0x21, 0x7F, 0x60, 0x00, 0xF0, 0x07])
                    # dont reset
                    scarecrow_script.append([0x9B])
                    # face southwest
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    # pause for 8 frames
                    scarecrow_script.append([0xF0, 0x07])
                    # face northwest
                    scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(8, scarecrow_script, 0x1f3546, False)
                    #####
                    #####second script
                    scarecrow_script = []
                    scarecrow_script.append([0x04, 0x10, 0xC1])
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x02])
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x41, 0x13, 0x03, 0xFD, 0x0F, 0x03])
                    scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                    scarecrow_script.append(
                        [0x0B, 0x04, 0xF0, 0x0C, 0xFD, 0x9E, 0x21, 0x7F, 0x90, 0x00, 0x57, 0x04, 0x67, 0x10])
                    scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                    # everything else
                    scarecrow_script.append(
                        [0x06, 0xF0, 0x09, 0x60, 0x32, 0xFD, 0x9E, 0x21, 0x7F, 0x50, 0x00, 0x60, 0x28, 0xF0, 0x00])
                    scarecrow_script.append([0xFD, 0x3D, 0x1C, 0x8B, 0x35])
                    scarecrow_script.append([0x10, 0xC1, 0xFD, 0x9E, 0x21, 0x7F, 0x80, 0x00, 0x50, 0x04, 0x01])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3561, True)
                elif sequence > 0 or (not sub_sequence and mold > 0):  # dont reset properties
                    patch.add_data(0x1f3552, [0x9b])
                # bandits way 3
                if sequence > 0 or mold > 0:
                    spritePhaseEvents.append(
                        SpritePhaseEvent(8, plus, mold, sub_sequence, sequence, False, 77, 1713, 0x20e8e3))
                if not freeze:
                    if extra_sequence != False:
                        patch.add_data(0x1f3b81, [0x08, 0x40, 0x80 + extra_sequence])
                    else:
                        patch.add_data(0x1f3b81, [0x08, 0x40 + plus, 0x80 + sequence])
                else:
                    patch.add_data(0x1f3b81, [0x9b, 0x9b, 0x9b])
                if invert_se_sw or freeze:  # scarecrow needs a special script
                    scarecrow_script = []
                    scarecrow_script.append([0xFD, 0x9E, 0x21, 0x7F, 0x60, 0x00, 0xF0, 0x1D])
                    scarecrow_script.append([0x9B])
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(8, scarecrow_script, 0x1f3b86, False)
                    # action script replacements
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x80, 0x14, 0x6C])
                    add_scarecrow_script(None, scarecrow_script, 0x211fe1, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x02, 0x10, 0xC2])
                    add_scarecrow_script(None, scarecrow_script, 0x211ff1, False)
                    scarecrow_script = []
                    scarecrow_script.append([0x92, 0x18, 0x52, 0x00, 0x00])
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(None, scarecrow_script, 0x211ff5, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x09, 0x10, 0xC2])
                    add_scarecrow_script(None, scarecrow_script, 0x212018, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x02, 0x10, 0xC1])
                    add_scarecrow_script(None, scarecrow_script, 0x212022, False)
                    scarecrow_script = []
                    scarecrow_script.append([0x92, 0x18, 0x2b, 0x00, 0x00])
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(None, scarecrow_script, 0x212026, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x04, 0x10, 0xC1])
                    add_scarecrow_script(None, scarecrow_script, 0x212044, False)
                    scarecrow_script = []
                    scarecrow_script.append([0x92, 0x14, 0x10, 0x00, 0x00])
                    scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                    add_scarecrow_script(None, scarecrow_script, 0x212054, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x05, 0x01])
                    add_scarecrow_script(None, scarecrow_script, 0x21206D, False)
                elif sequence > 0 or (not sub_sequence and mold > 0):  # dont reset properties
                    patch.add_data(0x1f3b90, [0x9b])
                # bandits way 4
                #new_preloader_event(78, [0xF2, 0xCE, 0x3C], 1698, 0x20e8e6)
                if invert_se_sw or freeze:  # scarecrow needs a special script
                    spritePhaseEvents.append(SpritePhaseEvent(12, plus, mold, True, sequence, False, 78, 1698, 0x20e8e6))
                    #####script 1
                    scarecrow_script = []
                    scarecrow_script.append([0xFD, 0x01, 0x00, 0x04, 0x67, 0x01, 0x06, 0x62, 0x08, 0x07])
                    scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                    add_scarecrow_script(12, scarecrow_script, 0x1f33c4, True)
                    #####script 2
                    scarecrow_script = []
                    scarecrow_script.append([0xF0, 0x13])
                    scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                    scarecrow_script.append([0xF0, 0x07])
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    scarecrow_script.append([0xF0, 0x13, 0x53, 0x03, 0x10, 0x80])
                    add_scarecrow_script(12, scarecrow_script, 0x1f3402, False)
                    #####script 3
                    scarecrow_script = []
                    scarecrow_script.append([0x10, 0xC1])
                    scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                    scarecrow_script.append(
                        [0xF0, 0x1D, 0xFD, 0x9E, 0x21, 0x7F, 0x70, 0x00, 0x06, 0x50, 0x04, 0x01])
                    add_scarecrow_script(12, scarecrow_script, 0x1f3410, False)
                else:
                    if sequence > 0 or mold > 0:
                        spritePhaseEvents.append(
                            SpritePhaseEvent(12, plus, mold, sub_sequence, sequence, False, 78, 1698, 0x20e8e6))
                # bandits way 5
                if sequence > 0 or mold > 0:
                    spritePhaseEvents.append(
                        SpritePhaseEvent(8, plus, mold, sub_sequence, sequence, False, 206, 1708, 0x20f078))
                if shuffled_boss.name == "CountDown":
                    remove_shadows(206, 10, 1708, 0x20f078)
                    patch.add_data(0x215B53, 0x01)
                    #partition 114
                    patch.add_data(0x14b48B, 0x72)
                #new_preloader_event(206, [0xF2, 0xCE, 0x3C, 0x1E, 0xF9], 1708, 0x20f078)
                if not freeze:
                    if extra_sequence != False:
                        patch.add_data(0x1f3863, [0x08, 0x40, 0x80 + extra_sequence])
                    else:
                        patch.add_data(0x1f3863, [0x08, 0x40 + plus, 0x80 + sequence])
                else:
                    patch.add_data(0x1f3863, [0x9b, 0x9b, 0x9b])
                if invert_se_sw or freeze:  # scarecrow sprite sequence 0 and 1 are inverted
                    #####script 1
                    scarecrow_script = []
                    scarecrow_script.append([0xFD, 0x9E, 0x21, 0x7F, 0x60, 0x00, 0xF0, 0x07])
                    scarecrow_script.append([0x9b])
                    scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                    scarecrow_script.append([0xF0, 0x13])
                    scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(8, scarecrow_script, 0x1f3868, False)
                    # replace "Face Mario" since dont know what direction that will be
                    patch.add_data(0x1f3995, [0x9b])
                    patch.add_data(0x1f39ac, [0x9b])
                    #####script 2
                    scarecrow_script = []
                    scarecrow_script.append([0x92, 0x0B, 0x73, 0x00])
                    scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                    scarecrow_script.append([0x00])
                    add_scarecrow_script(8, scarecrow_script, 0x1f38DE, False)
                    #####script 3
                    scarecrow_script = []
                    scarecrow_script.append([0x07])
                    scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                    add_scarecrow_script(8, scarecrow_script, 0x1f39d7, False)
                    #####script 4
                    scarecrow_script = []
                    scarecrow_script.append([0xFD, 0x9E, 0x0B, 0x10, 0xC3])
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x03, 0x52, 0x0B, 0x51, 0x04, 0x10, 0xC4, 0xD4, 0x01])
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x04, 0x52, 0x02, 0x51, 0x04])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x53, 0x08])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x08, 0x56, 0x02])
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x08, 0xD7])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3877, True)
                    ####1707
                    scarecrow_script = []
                    scarecrow_script.append(
                        [0x00, 0x10, 0xC3, 0x0C, 0x04, 0x0C, 0xF0, 0xDC, 0x1F, 0x8E, 0x36, 0x42, 0x41, 0x40])
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x03])
                    add_scarecrow_script(8, scarecrow_script, 0x1f367C, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x08])
                    add_scarecrow_script(8, scarecrow_script, 0x1f36CC, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x47, 0x46])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x45, 0x56, 0x08])
                    add_scarecrow_script(8, scarecrow_script, 0x1f36D3, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x47, 0x46])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x09])
                    add_scarecrow_script(8, scarecrow_script, 0x1f36DD, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x07, 0x50, 0x03])
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x03])
                    add_scarecrow_script(8, scarecrow_script, 0x1f370D, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x57, 0x08])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3718, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x09, 0x42])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x43])
                    add_scarecrow_script(8, scarecrow_script, 0x1f371F, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x51, 0x09, 0x42])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x43])
                    add_scarecrow_script(8, scarecrow_script, 0x1f374F, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x53, 0x08])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3758, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x52, 0x08, 0x41])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x42, 0x43])
                    add_scarecrow_script(8, scarecrow_script, 0x1f375F, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x47, 0x46])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x09])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3790, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x53, 0x03, 0x54, 0x03])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x55, 0x07])
                    add_scarecrow_script(8, scarecrow_script, 0x1f3799, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x53, 0x08])
                    add_scarecrow_script(8, scarecrow_script, 0x1f37A4, False)
                    scarecrow_script = []
                    scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                    scarecrow_script.append([0xDC, 0x26, 0x0E, 0x38, 0x10, 0xC4, 0xA0, 0x1F])
                    scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x53, 0x03, 0x44])
                    scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                    scarecrow_script.append([0x45, 0x46])
                    scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                    add_scarecrow_script(8, scarecrow_script, 0x1f37FD, False)
                elif sequence > 0 or (not sub_sequence and mold > 0):  # dont reset properties
                    patch.add_data(0x1f3872, [0x9b])

            if location.name == "Mack":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Mack":
                    # reassign NPC 480's sprite
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x68]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1Dc520, calcpointer(sprite, [0x00, 0x68]));
                    # face southwest
                    patch.add_data(0x14ca86, 0x63);
                    # delete sequence init, this can be delegated to spritePhaseEvents if special sequence needs to be loaded
                    patch.add_data(0x1e2921, [0x9b, 0x9b, 0x9b])
                    # for sprites that require a specific mold or sequence, change the room load events to set the proper sequence or mold first
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(3, plus, mold, sub_sequence, sequence, False, 326, 368, 0x20f47d))

            if location.name == "Belome1":
                #print(location.name + ": " + shuffled_boss.name)
                # use npc 371, set properties to match belome's
                patch.add_data(0x14c67a, [0xcd, 0x05]);
                # replace its sprite
                patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0xA8]), shadow, solidity, y_shift, location))
                #patch.add_data(0x1Dc225, calcpointer(sprite, [0x00, 0xA8]));
                if sequence > 0 or mold > 0:
                    patch.add_data(0x203513, [0x08, 0x50 + plus, sequence]);
                    if sequence > 0:
                        sub_sequence = True
                    elif mold > 0:
                        sub_sequence = False
                    spritePhaseEvents.append(
                        SpritePhaseEvent(3, plus, mold, sub_sequence, sequence, False, 302, 3135, 0x20f3be))

            if location.name == "Bowyer":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Bowyer":
                    # reassign NPC 455's sprite
                    # try big sprite
                    patch.add_data(0x1dc54a, calcpointer(sprite, [0x00, 0x68]));
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(16, plus, mold, sub_sequence, sequence, False, 232, 15, 0x20F1C6))

            if location.name == "Croco2":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name not in ["Croco1", "Croco2"]:
                    # use npc 367, set properties to match croco's
                    patch.add_data(0x14c2a2, [0xBE, 0xA5]);
                    patch.add_data(0x14c300, [0xBE, 0xE5]);
                    patch.add_data(0x14c33e, [0xBE, 0xF5]);
                    patch.add_data(0x14c398, [0xBE, 0xC5]);
                    patch.add_data(0x14c3e6, [0xBE, 0xD5]);
                    patch.add_data(0x14c448, [0xBE, 0xB5]);
                    # replace its sprite
                    if overworld_is_empty and shuffled_boss.name not in ["Culex"]:
                        #works for: birdo
                        #patch.add_data(0x1Dc209, calcpointer(sprite, [0x00, 0x28]));
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location, False))
                        remove_shadows(273, 4, 15, 0x20f301)
                        remove_shadows(283, 6, 3204, 0x20f32b)
                    elif freeze or sesw_only:
                        #patch.add_data(0x1Dc209, calcpointer(sprite, [0x00, 0x08]));
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1Dc209, calcpointer(sprite, [0x00, 0x00]));
                    # change partitions for small sprites
                    if overworld_is_skinny:
                        # area 4 - modify partition 53
                        patch.add_data(0x1DDED5, 0x81)
                        # area 5 and 7 - reconfigure and use partition 2
                        patch.add_data(0x14c33a, 0x02)
                        patch.add_data(0x14c3e2, 0x02)
                        patch.add_data(0x1dde08, [0xB1, 0x81, 0x80, 0x80]);
                        # area 6 and 8 can use partition 60, it meets its needs when a small sprite is on croco
                        patch.add_data(0x14c2fc, 0x3c)
                        patch.add_data(0x14c394, 0x3c)
                        # area 9 - reconfigure and use partition 1
                        patch.add_data(0x14c444, 0x01)
                        patch.add_data(0x1dde04, [0xB2, 0x81, 0x80, 0x80]);
                    elif overworld_is_empty:
                        #area 5 and 7 need a special partition with culex
                        if shuffled_boss.name in ["Culex"]:
                            # area 5 - use partition reconfigure and use partition 2
                            patch.add_data(0x14c33a, 0x02)
                            patch.add_data(0x14c3e2, 0x02)
                            patch.add_data(0x1dde08, [0xA0, 0x87, 0x81, 0x80]);
                        else:
                            # area 5 - use partition 107
                            patch.add_data(0x14C33A, 0x6B)
                            # area 7 - use partition 107
                            patch.add_data(0x14C3E2, 0x6B)
                        # area 4 - use partition 114
                        patch.add_data(0x14C29E, 0x72)
                        # area 6 - use partition 114
                        patch.add_data(0x14C2FC, 0x72)
                        # area 8 - use partition 114
                        patch.add_data(0x14C394, 0x72)
                        # area 9 - use partition 114
                        patch.add_data(0x14C444, 0x72)
                    # need to change a lot of things in moleville to get this to work
                    sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if invert_se_sw or freeze:  # scarecrow sprite sequence 0 and 1 are inverted
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x21886f, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x43])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x05])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x57, 0x07])
                        add_scarecrow_script(None, scarecrow_script, 0x21887A, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x41])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x47])
                        add_scarecrow_script(None, scarecrow_script, 0x218885, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x57, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x2188FB, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x57, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218905, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x57, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x0A])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(None, scarecrow_script, 0x218910, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x06])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x05])
                        add_scarecrow_script(None, scarecrow_script, 0x21891C, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218993, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x55, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x21899D, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x02])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x2189AE, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218a1D, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x53, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218a27, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x04, 0xF0, 0x07])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x07])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x07, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x218a32, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218ab7, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x218ac2, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x43, 0x07, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218ac9, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218b37, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218b41, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x03, 0x04, 0xF0, 0x07, 0x7F, 0x40, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x05, 0xF0, 0x0F])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x57, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x05])
                        add_scarecrow_script(None, scarecrow_script, 0x218b4C, False)
                        # attempt to fix NPCs in area 5
                        new_preloader_event(273, [0xF2, 0x15, 0x2D, 0xF2, 0x15, 0x2F], 15, 0x20f301)
                        new_preloader_event(277, [0x16, 0xF9, 0x17, 0xF9], 15, 0x20F313)
                        # attempt to fix NPCs in area 7
                        new_preloader_event(273, [0xF2, 0x19, 0x2B, 0xF2, 0x19, 0x2D, 0xF2, 0x19, 0x2F], 15, 0x20f301)
                        new_preloader_event(281, [0x15, 0xF9, 0x16, 0xF9, 0x17, 0xF9], 15, 0x20F325)
                    elif shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x21886f, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x43])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x05])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, 1, is_scarecrow))
                        scarecrow_script.append([0x57, 0x07])
                        add_scarecrow_script(None, scarecrow_script, 0x21887A, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x41])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, 1, is_scarecrow))
                        scarecrow_script.append([0x47])
                        add_scarecrow_script(None, scarecrow_script, 0x218885, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northwest, False, 1, is_scarecrow))
                        scarecrow_script.append([0x57, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x2188FB, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northwest, True, 1, is_scarecrow))
                        scarecrow_script.append([0x00, 0x57, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218905, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northwest, False, 1, is_scarecrow))
                        scarecrow_script.append([0x57, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, 1, is_scarecrow))
                        scarecrow_script.append([0x55, 0x0A])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(None, scarecrow_script, 0x218910, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x06])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, 1, is_scarecrow))
                        scarecrow_script.append([0x55, 0x05])
                        add_scarecrow_script(None, scarecrow_script, 0x21891C, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, False, 1, is_scarecrow))
                        scarecrow_script.append([0x55, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218993, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, True, 1, is_scarecrow))
                        scarecrow_script.append([0x00, 0x55, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x21899D, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, 1, is_scarecrow))
                        scarecrow_script.append([0x55, 0x02])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, 1, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x2189AE, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218a1D, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x53, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218a27, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x04, 0xF0, 0x07])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, 1, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x07])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x07, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x218a32, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218ab7, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x04])
                        add_scarecrow_script(None, scarecrow_script, 0x218ac2, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x43, 0x07, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218ac9, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x10, 0x41])
                        add_scarecrow_script(None, scarecrow_script, 0x218b37, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x51, 0x02])
                        add_scarecrow_script(None, scarecrow_script, 0x218b41, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x03, 0x04, 0xF0, 0x07, 0x7F, 0x40, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x02, 0x05, 0xF0, 0x0F])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, 1, is_scarecrow))
                        scarecrow_script.append([0x57, 0x05])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x05])
                        add_scarecrow_script(None, scarecrow_script, 0x218b4C, False)
                    if sequence > 0 or mold > 0:
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 273, 15, 0x20f301))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 277, 15, 0x20f313))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 275, 15, 0x20f30d))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 281, 15, 0x20f325))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 279, 15, 0x20f319))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 283, 3204, 0x20f32b))

            if location.name == "Punchinello":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Punchinello":
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x48]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1dc4b0, calcpointer(sprite, [0x00, 0x48]));
                    # push animations
                    if not freeze and push_sequence != False:
                        if shuffled_boss.name == "Booster":
                            patch.add_data(0x1dc4b0, calcpointer(502, [0x00, 0x48]));
                            patch.add_data(0x1e6d8b, [0x08, 0x50, 3])
                        else:
                            patch.add_data(0x1e6d8b, [0x08, 0x50, push_sequence])
                    else:
                        patch.add_data(0x1e6d8b, [0x9b, 0x9b, 0x9b])
                    if shuffled_boss.name == "Hidon":  # tiny bombs become goombettes
                        patch.add_data(0x1DB903, [0x5D, 0x09])
                    patch.add_data(0x1e6d99, [0xf0, (max(1, push_length - 1))]);
                    patch.add_data(0x1e6da4, [0xf0, (max(1, push_length - 1))]);
                    patch.add_data(0x1e6d90, [0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1e6e04, [0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1e6e1b, [0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1e6e32, [0x9b, 0x9b, 0x9b, 0x9b])
                    sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    spritePhaseEvents.append(
                        SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 289, 592, 0x20F36b))

            if location.name == "KingCalamari":
                #print(location.name + ": " + shuffled_boss.name)
                if (shuffled_boss.name != "KingCalamari"):
                    #patch.add_data(0x1dbc98, calcpointer(sprite, [0x00, 0x28]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    patch.add_data(0x214068, 0x9b)
                    patch.add_data(0x214098, 0x9b)
                    patch.add_data(0x21409D, 0x9b)
                    patch.add_data(0x214076, [0x9b, 0x9b, 0x9b])
                    patch.add_data(0x21407b, [0x9b, 0x9b, 0x9b])
                    if sequence > 0:
                        sub_sequence = True
                        patch.add_data(0x21406c, [0x08, 0x50 + plus, sequence])
                    elif mold > 0:
                        sub_sequence = False
                        patch.add_data(0x21406c, [0x08, 0x58 + plus, mold])
                    spritePhaseEvents.append(
                        SpritePhaseEvent(7, plus, mold, sub_sequence, sequence, False, 177, 3224, 0x20eef1))

            if location.name == "Booster":
                #print(location.name + ": " + shuffled_boss.name)
                if (shuffled_boss.name != "Booster"):

                    #remove shadows -- these are just way too rough to deal with in here on a case-by-case basis
                    patch.add_data(0x1EF497, calcpointer(262, [0x00, 0x00]))
                    patch.add_data(0x1EF3D7, [0x9B, 0x9B])
                    # fix marrymore if fat sprite is used
                    if shuffled_boss.name == "Bundt":
                        # chapel - partition 41
                        patch.add_data(0x14a8c9, 0x29)
                    elif overworld_is_skinny and fat_sidekicks and shuffled_boss.name in ["Bundt", "Clerk", "Manager",
                                                                                          "Director", "Croco1",
                                                                                          "Croco2", "Mack", "Bowyer",
                                                                                          "Punchinello", "Johnny",
                                                                                          "Megasmilax", "CzarDragon",
                                                                                          "Birdo", "Valentina", "Hidon",
                                                                                          "Yaridovich"]:
                        # chapel - partition 106
                        # works for valentina
                        patch.add_data(0x14a8c9, 0x6A)
                    elif fat_sidekicks and world.character_join_order[4].name != "Mallow" and shuffled_boss.name in [
                        "Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2", "Mack", "Bowyer", "Punchinello",
                        "Johnny", "Megasmilax", "CzarDragon", "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        # chapel - partition 83
                        # works for croco
                        patch.add_data(0x14a8c9, 0x53)
                    elif not overworld_is_skinny:
                        # chapel - partition 108
                        # works for knife guy
                        patch.add_data(0x14a8c9, 0x6C)
                    # fix partitions in lower booster tower rooms if booster is replaced
                    if overworld_is_empty:
                        patch.add_data(0x14B13E, 0x5D)
                    elif not overworld_is_skinny:
                        patch.add_data(0x14B13E, 0x60)
                    #increase elevation in portrait room if boss is short
                    if len(solidity) >= 2 and solidity[2] < 6:
                        patch.add_data(0x14B1CF, 0x80)
                    # replace sprite for npc 50
                    increase_sprite_size = 0
                    # fix sprite size if certain animations are used
                    if shuffled_boss.name in ["Croco1", "Croco2", "Magikoopa", "Boomer", "CountDown"]:
                        increase_sprite_size = 0x20
                    if shuffled_boss.name in ["Croco1", "Croco2", "DodoSolo"]:
                        remove_shadows(192, 7, 1359, 0x20efad)
                    if freeze or sesw_only:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, increase_sprite_size + 0x08]), shadow, [5, 5, 12 if len(solidity) < 3 else solidity[2]], y_shift, location))
                        #patch.add_data(0x1db95e, calcpointer(sprite, [0x00, increase_sprite_size + 0x08]))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, increase_sprite_size + 0x00]), shadow, [5, 5, 12 if len(solidity) < 3 else solidity[2]], y_shift, location))
                        #patch.add_data(0x1db95e, calcpointer(sprite, [0x00, increase_sprite_size + 0x00]))
                    # was gonna replace snifits too for axems + culex's sidekicks, but they are cloned + it wouldnt work
                    # only do it for clerk, manager, director, croco, mack, bowyer, punchinello, johnny, megasmilax, czar dragon
                    if shuffled_boss.name in ["Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2", "Mack",
                                              "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon", "Birdo",
                                              "Valentina", "Hidon", "Yaridovich", "Boomer"]:
                        patch.add_data(0x1dc5c8, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x20]))
                        if shuffled_boss.name != "Birdo" and shuffled_boss.name != "Boomer":  # eggs and shyguys break marrymore unfortunately
                            patch.add_data(0x1db8fc, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x00]))
                        # tower
                        patch.add_data(0x1ee8b4, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b3d, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b42, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b47, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b4d, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b52, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b57, [0x75, 0x75, 0x75])
                        patch.add_data(0x216b5c, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ee8ff, [0x75, 0x75, 0x75])
                        patch.add_data(0x1EE947, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ee98e, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ee9d7, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eea69, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eea7a, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeae0, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeaef, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeb5b, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeb6b, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eebe3, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eec02, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eec16, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeca5, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eecad, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eed16, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eed28, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eed91, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eeda3, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eee78, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eee7f, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eee86, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eef0d, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eef1d, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eef2d, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eefc0, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eefc5, [0x75, 0x75, 0x75])
                        patch.add_data(0x1eefca, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef05d, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef062, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef067, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef0fa, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef109, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef10e, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef11a, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef11f, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef12b, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef1e0, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef1fe, [0x75, 0x75, 0x75])
                        patch.add_data(0x1ef217, [0x75, 0x75, 0x75])
                        patch.add_data(0x214764, [0x08, 0x40, 0x00])
                        patch.add_data(0x214769, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x21476E, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214773, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214778, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x21477D, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214782, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214789, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x21478E, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214793, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x214798, [0x9B, 0x9B, 0x9B])
                    sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        #curtain room
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x63, 0x08])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x03])
                        add_scarecrow_script(None, scarecrow_script, 0x218155, False)
                        # portrait room
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x12, 0x19])
                        scarecrow_script.append([0x65, 0x05, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xFD, 0x0F, 0x00, 0x13, 0x00])
                        add_scarecrow_script(6, scarecrow_script, 0x1ee04D, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x1D, 0x10, 0x85, 0x9B, 0x9B, 0x9B])
                        add_scarecrow_script(6, scarecrow_script, 0x1ee071, False)
                        patch.add_data(0x1ee08e, [0x9B, 0x9B, 0x9B])
                        # tower
                        scarecrow_script = []
                        scarecrow_script.append([0xFD, 0x0F, 0x03, 0x92, 0x05, 0x10, 0x00, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x04])
                        add_scarecrow_script(0, scarecrow_script, 0x1ed88F, True)
                        scarecrow_script = []
                        scarecrow_script.append(
                            [0x92, 0x09, 0x12, 0x00, 0xFD, 0x0F, 0x03, 0x0C, 0x04, 0x10, 0x45, 0x10, 0x80])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0x53, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x02])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ee4bf, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC1])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x06, 0x53, 0x01])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x55, 0x01, 0x10, 0xC0, 0xF0, 0x1D, 0x08, 0x40 + plus, sequence, 0xF0, 0x1D])
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1ee53d, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x07])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ee6c6, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x07])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09, 0x7F, 0x32, 0x00])
                        add_scarecrow_script(0, scarecrow_script, 0x1eea36, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x10, 0x40, 0x10, 0x81])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x63, 0x08])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x55, 0x02, 0x65, 0x0D, 0xF0, 0x0E, 0x9B, 0x9B, 0x9B, 0xF0, 0x06, 0x9B,
                             0x9B, 0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef2b9, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x18, 0x10, 0x41, 0x10, 0x83])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x04, 0x06, 0x7F, 0x70, 0x00])
                        scarecrow_script.append([0x51, 0x03, 0x04])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef2e9, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x05])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ef358, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x07])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ef35D, False)
                        scarecrow_script = []
                        scarecrow_script.append(
                            [0x10, 0xC0, 0xF0, 0x1D, 0x08, 0x40 + plus, 0x80 + sequence, 0xF0, 0x1D, 0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef373, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x3B, 0x10, 0x83, 0x08, 0x40 + plus, 0x80 + sequence])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef388, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x3B, 0x7F, 0x40, 0x00, 0xF0, 0x1D])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef3f4, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0x83, 0x10, 0x41, 0x9C, 0x18])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x03])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef411, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ef42f, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC3])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x03, 0x61, 0x08])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x06])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef432, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x00])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x82, 0x05, 0x1D])
                        add_scarecrow_script(7, scarecrow_script, 0x1ef4da, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC1, 0x92, 0x04, 0x15, 0x00])
                        scarecrow_script.append([0x61, 0x08])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ef4ff, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x07])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append([0x10, 0xC3, 0x90, 0x05, 0x13, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1ef5b4, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        add_scarecrow_script(0, scarecrow_script, 0x1ef539, True)
                        # marrymore
                        scarecrow_script = []
                        scarecrow_script.append(
                            [0x94, 0xFC, 0xF8, 0x00, 0xF0, 0x0B, 0x10, 0x45, 0x10, 0x81, 0x67, 0x08, 0x10, 0x43])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x57, 0x0D, 0x67, 0x08, 0x0B, 0x04, 0xFD, 0x02, 0x57, 0x03, 0x9B, 0x9B, 0x9B, 0x10, 0x44,
                             0x9C, 0x31, 0x67, 0x02, 0x63, 0x04, 0x67, 0x04, 0x63, 0x04, 0x67, 0x03, 0x63, 0x02, 0x67,
                             0x02, 0x63, 0x01])
                        add_scarecrow_script(15, scarecrow_script, 0x20D301, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x61, 0x0A, 0xF0, 0x1D])
                        scarecrow_script.append([0x65, 0x0E])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(15, scarecrow_script, 0x20d5cb, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(15, scarecrow_script, 0x20d5fc, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x06, 0x10, 0x41])
                        scarecrow_script.append([0x41, 0x10, 0x80, 0x08, 0x40 + plus, sequence])
                        add_scarecrow_script(15, scarecrow_script, 0x20d61D, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append([0x07])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(15, scarecrow_script, 0x20d6fa, False)
                        # booster hill
                        scarecrow_script = []
                        scarecrow_script.append([0x07, 0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(7, scarecrow_script, 0x207153, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x06])
                        add_scarecrow_script(7, scarecrow_script, 0x20716A, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC1])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x0B, 0x10, 0x80])
                        add_scarecrow_script(7, scarecrow_script, 0x206b25, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(7, scarecrow_script, 0x206d27, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(7, scarecrow_script, 0x206d40, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x07, 0x10, 0xC1, 0xF0, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x08, 0x01])
                        add_scarecrow_script(7, scarecrow_script, 0x206F32, True)
                    # special animations
                    else:
                        if extra_sequence != False:
                            # tower
                            patch.add_data(0x1ee54b, [0x08, 0x40, extra_sequence])
                            patch.add_data(0x1ef379, [0x08, 0x40, 0x80 + extra_sequence])
                            patch.add_data(0x1ef38e, [0x08, 0x40, 0x80 + extra_sequence])
                            # marrymore
                            patch.add_data(0x20d625, [0x08, 0x40, extra_sequence])
                            # if shuffled_boss.name is not "Boomer":
                            #    patch.add_data(0x20d625, [0x08, 0x40, extra_sequence])
                            # else:
                            #       patch.add_data(0x20d625, [0x77, 0x9b, 0x9b])
                        else:
                            # tower
                            patch.add_data(0x1ee54b, [0x08, 0x40 + plus, sequence])
                            patch.add_data(0x1ef379, [0x08, 0x40 + plus, 0x80 + sequence])
                            patch.add_data(0x1ef38e, [0x08, 0x40 + plus, 0x80 + sequence])
                            # marrymore
                            patch.add_data(0x20d625, [0x77, 0x9b, 0x9b])
                        # portrait room
                        patch.add_data(0x1ee078, [0x9b, 0x9b, 0x9b])
                        # tower
                        patch.add_data(0x1ef2c9, [0x9b, 0x9b, 0x9b])
                        patch.add_data(0x1ef2ce, [0x9b, 0x9b, 0x9b])
                        # marrymore
                        patch.add_data(0x20d31B, [0x77, 0x9b, 0x9b])
                    if sequence > 0 or mold > 0:
                        # make booster not face on contact
                        patch.add_data(0x14A93F, 0x40)
                        # tower
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 7], plus, mold, sub_sequence, [sequence, sequence], [False, False],
                                             192, 1359, 0x20efad))
                        # marrymore
                        spritePhaseEvents.append(
                            SpritePhaseEvent(15, plus, mold, sub_sequence, sequence, False, 154, 600, 0x20edc7))
                        # portrait room
                        spritePhaseEvents.append(
                            SpritePhaseEvent(6, plus, mold, sub_sequence, sequence, False, 195, 1339, 0x20efe4))
                        # stair room
                        spritePhaseEvents.append(
                            SpritePhaseEvent(6, plus, mold, sub_sequence, sequence, True, 193, 15, 0x20efce))
                        # booster hill
                        spritePhaseEvents.append(
                            SpritePhaseEvent(7, plus, mold, sub_sequence, sequence, False, 54, 3499, 0x20e74f))
                    #shift crown's landing spot depending on boss' height
                        if len(solidity) >= 3:
                            if solidity[2] <= 6:
                                patch.add_data(0x20D6E0, 5)

            if location.name == "Bundt":
                # always replace npc sprite here, it's normally just the feather
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Bundt":
                    if shuffled_boss.name == "CountDown":
                        #patch.add_data(0x1DC4DA, calcpointer(sprite, [0x00, 0x08]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location, True))
                    elif freeze or sesw_only:
                        #patch.add_data(0x1DC4DA, calcpointer(sprite, [0x00, 0x08]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))

                    else:
                        #patch.add_data(0x1DC4DA, calcpointer(sprite, [0x00, 0x00]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                    if shuffled_boss.name in ["Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2", "Mack",
                                              "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1DC2DB, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x08]))
                    # use partition 40
                    if shuffled_boss.name in ["Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2", "Mack",
                                              "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        if overworld_is_skinny and fat_sidekicks:  # valentina
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x81, 0x80, 0x81])
                        elif overworld_is_skinny:  # czar
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xC0, 0x81, 0x81, 0x81])
                        elif overworld_is_empty and empty_sidekicks:  # birdo
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x85, 0x85, 0x85])
                        elif fat_sidekicks:  # croco
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x80, 0x80, 0x81])
                        patch.add_data(0x213CD4, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x213D02, [0x9B, 0x9B, 0x9B])
                        patch.add_data(0x213D19, [0x9B, 0x9B, 0x9B])
                    else:
                        if shuffled_boss.name == "CountDown":
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x87, 0x87, 0x87])
                        elif overworld_is_skinny:
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x81, 0x81, 0x81])
                        elif overworld_is_empty:
                            patch.add_data(0x14A956, 0x28)
                            patch.add_data(0x1DDEA0, [0xA0, 0x87, 0x81, 0x81])
                    if shuffled_boss.name in ["Pandorite", "Hidon", "HammerBro", "BoxBoy", "DodoSolo"]: # shift up a little bit
                        patch.add_data(0x14A961, 0x97)

                    sub_sequence = True
                    if statue_mold != None:
                        sub_sequence = False
                    if sequence == 0 and statue_mold == None:
                        statue_mold = 0
                        sub_sequence = False
                    spritePhaseEvents.append(
                        SpritePhaseEvent(0, plus, statue_mold, sub_sequence, sequence, False, 155, 628, 0x20EDD0))
                    # elif shuffled_boss.name is "Culex":
                    #     new_preloader_event(155, [0x14, 0x83, 0x08, 0x18, 0x03], 628, 0x20EDD0)
                    # elif shuffled_boss.name is "Exor":
                    #     new_preloader_event(155, [0x14, 0x83, 0x08, 0x1B, 0x16], 628, 0x20EDD0)
                    patch.add_data(0x1E7CC9, [0x9B, 0x9B, 0x9B])
                    patch.add_data(0x1dbb95, calcpointer(sprite, [0x00, 0x88]))
                    #npc_queue = [0x14, 3, 0x84, 0x00, 0x00]
                    #new_preloader_event(155, npc_queue, 628, 0x20EDD0)

            if location.name == "Johnny":
                #print(location.name + ": " + shuffled_boss.name)
                if (shuffled_boss.name != "Johnny"):
                    # change partition 13 if needed
                    if shuffled_boss.name == "CountDown":
                        patch.add_data(0x1dde34, [0xA0, 0x87, 0x87, 0x87])
                        remove_shadows(28, 9, 3282, 0x20E586)
                    elif freeze:
                        # might only be necessary for culex
                        patch.add_data(0x1dde35, 0x85)
                    elif fat_sidekicks and shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director",
                                                                  "Croco1", "Croco2", "Mack", "Bowyer", "Punchinello",
                                                                  "Booster", "Megasmilax", "CzarDragon", "Birdo",
                                                                  "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1dde35, 0x80)
                    elif overworld_is_empty:
                        patch.add_data(0x1dc10e, [0x01, 0x80, 0xA2])
                    # replace sprite for npc 52
                    # replace its sprite
                    if shuffled_boss.name == "CountDown":
                        #patch.add_data(0x1DB96C, calcpointer(sprite, [0x00, 0x28]));
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location, True))
                    elif freeze or sesw_only:
                        #patch.add_data(0x1db96c, calcpointer(sprite, [0x00, 0x08]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    else:
                        #patch.add_data(0x1db96c, calcpointer(sprite, [0x00, 0x00]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                    # these bosses will have someone replace bandana blues
                    if shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2",
                                              "Mack", "Bowyer", "Punchinello", "Booster", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1dc10d, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x20]))
                    # if freeze: #never change directions
                    #     patch.add_data(0x203873, 0x9b)
                    sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x18, 0x6E])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append([0x02])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(2, scarecrow_script, 0x20386c, True)
                        patch.add_data(0x213fb1, 0x9b)
                    # preload sprite form if needed
                    patch.add_data(0x213FA7, [0x9b, 0x9b, 0x9b])
                    if sequence > 0 or mold > 0:
                        spritePhaseEvents.append(
                            SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, False, 28, 3282, 0x20E586))
                    # megasmilax has weird sprites
                    if shuffled_boss.name == "Megasmilax":
                        patch.add_data(0x203873, 0x77)
                    if shuffled_boss.name in ["Pandorite", "Hidon", "HammerBro", "BoxBoy", "DodoSolo"]: # shift up a little bit
                        patch.add_data(0x148A03, 0xF1)

            if location.name == "Yaridovich":
                # replace elder's sprite
                #print(location.name + ": " + shuffled_boss.name)
                # always make him face NW, no matter who it is
                scarecrow_script = []
                scarecrow_script.append([0x10, 0xC3])
                scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                if not (freeze or sesw_only or invert_se_sw):
                    scarecrow_script.append(INSERT_NORTHWEST)
                scarecrow_script.append([0x55, 0x1E, 0x01])
                add_scarecrow_script(4, scarecrow_script, 0x1ECBE8, True)
                if shuffled_boss.name not in ["Yaridovich"]:
                    # replace its sprite
                    if shuffled_boss.name == "CountDown":
                        #patch.add_data(0x1DB918, calcpointer(sprite, [0x00, 0x28]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    elif freeze or sesw_only:
                        #patch.add_data(0x1DB918, calcpointer(sprite, [0x00, 0x08]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    else:
                        #patch.add_data(0x1DB918, calcpointer(sprite, [0x00, 0x00]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(4, plus, mold, sub_sequence, sequence, False, 208, 1119, 0x20f0A0))
                        patch.add_data(0x1ECCD6, [0x9B, 0x9B, 0x9B])

            if location.name == "Belome2":
                # replace belome's sprite
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name not in ["Belome1", "Belome2"]:
                    #patch.add_data(0x1Dc471, calcpointer(sprite, [0x00, 0xA8]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0xA8]), shadow, solidity, y_shift, location))
                    if sequence > 0 or mold > 0:
                        patch.add_data(0x14C13F, 0xC0)
                        patch.add_data(0x1f47BB, 0x9B)
                        patch.add_data(0x1F65ED, [0x08, 0x40 + plus, sequence])
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(4, plus, mold, sub_sequence, sequence, False, 268, 1771, 0x20f2e6))

            if location.name == "Jagger":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Jagger":
                    # partition size for jinx will be decided after entire boss loop, since also depends on jagger
                    if overworld_is_skinny:
                        jagger_size = 1
                    elif overworld_is_empty:
                        jagger_size = 0
                    else:
                        jagger_size = 2
                    # replace jagger's sprite
                    if shuffled_boss.name == "Booster":
                        #patch.add_data(0x1dbc44, calcpointer(502, [0x00, 0x20]));
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(502, [0x00, 0x20]), shadow, [4, 4, 11 if len(solidity) < 3 else solidity[2]], y_shift, location))
                    elif freeze or sesw_only:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, [4, 4, 11 if len(solidity) < 3 else solidity[2]], y_shift, location))
                        #patch.add_data(0x1Dbc44, calcpointer(sprite, [0x00, 0x28]))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x20]), shadow, [4, 4, 11 if len(solidity) < 3 else solidity[2]], y_shift, location))
                        #patch.add_data(0x1Dbc44, calcpointer(sprite, [0x00, 0x20]))
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    # if freeze or (not sub_sequence and mold > 0): #dont loop
                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x06, 0x0D])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6bb4, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x05, 0x0F, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6bc0, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x05, 0x09])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6bca, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x05, 0x0E])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0xFD, 0x0B])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6bdb, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x1D, 0x10, 0x80, 0x08, 0x50 + plus, sequence, 0xF0, 0x0E])
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6bfe, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0x81, 0x10, 0x40])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0x9B, 0x07])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6c27, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0x80])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(1, scarecrow_script, 0x1f6c77, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x06, 0x10, 0x41, 0x7E, 0x35, 0x00])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x57, 0x01, 0xF0, 0x13, 0x10, 0x80, 0x9b, 0x9b, 0x08, 0x50 + plus, sequence, 0xF0, 0x2C])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6c7c, True)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x45])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x07, 0xF0, 0x1D, 0x10, 0xC5, 0x53, 0x01])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6cbd, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0x81, 0x08, 0x40 + plus, sequence, 0xF0, 0x2C])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x2C, 0x10, 0xC2])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x80, 0x05, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(1, scarecrow_script, 0x1f6d0e, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x4F, 0x07])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(1, scarecrow_script, 0x1f6d24, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC1, 0x80, 0x05, 0x0E])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x10, 0xC0])
                        add_scarecrow_script(1, scarecrow_script, 0x1f6f45, False)
                    else:
                        # remove sfx
                        patch.add_data(0x1f6c8a, [0x9b, 0x9b])
                        patch.add_data(0x1f6c05, [0x9b, 0x9b, 0x9b])
                    # special animations
                    if shuffled_boss.name == "Booster":
                        patch.add_data(0x1f6c8c, [0x08, 0x50, 3])
                        patch.add_data(0x1f6d12, [0x08, 0x50, 4])
                    elif not freeze and not invert_se_sw:
                        if push_sequence != False:
                            patch.add_data(0x1f6c8c, [0x08, 0x50, push_sequence])
                        elif extra_sequence != False:
                            patch.add_data(0x1f6c8c, [0x08, 0x50, extra_sequence])
                        else:
                            patch.add_data(0x1f6c8c, [0x08, 0x50, sequence])
                        if extra_sequence != False:
                            patch.add_data(0x1f6d12, [0x08, 0x40, extra_sequence])
                        else:
                            patch.add_data(0x1f6d12, [0x9b, 0x9b, 0x9b])
                    # If Jinx needs preloading, do it now
                    for l in world.boss_locations:
                        if (l.name in ["HammerBros", "Croco1", "Mack", "Belome1", "Bowyer", "Croco2",
                                       "Punchinello", "KingCalamari",
                                       "Booster", "Johnny", "Belome2", "Jagger", "Jinx3",
                                       "Megasmilax", "Dodo", "Valentina", "Magikoopa",
                                       "CzarDragon", "AxemRangers",
                                       "Countdown", "Clerk", "Manager", "Director", "Gunyolk"]):
                            for e in l.pack.common_enemies:
                                if e.overworld_sprite != None:
                                    if l.name == "Jinx3" and e.name not in ["Jinx1", "Jinx2", "Jinx3"]:
                                        if e.overworld_sequence > 0 or e.overworld_mold > 0:
                                            # make him not face on contact
                                            patch.add_data(0x14BE5B, 0x40)
                                            if e.overworld_sequence > 0:
                                                patch.add_data(0x1f6c5e,
                                                               [0x14, 0x86, 0x08, 0x40 + e.overworld_sprite_plus,
                                                                e.overworld_sequence, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                                                0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                                            elif e.overworld_mold > 0:
                                                patch.add_data(0x1f6c5e,
                                                               [0x14, 0x86, 0x08, 0x08 + e.overworld_sprite_plus,
                                                                e.overworld_mold, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                                                0x9b, 0x9b, 0x9b, 0x9b])
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        # make him not face on contact
                        patch.add_data(0x14BE67, 0x40)
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(1, plus, mold, sub_sequence, sequence, False, 255, 2064, 0x20f2a1))

            if location.name == "Jinx3":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name not in ["Jinx1", "Jinx2", "Jinx3"]:
                    # partition size for jinx will be decided after entire boss loop, since also depends on jagger
                    if overworld_is_skinny:
                        jinx_size = 1
                    elif overworld_is_empty:
                        jinx_size = 0
                    else:
                        jinx_size = 2
                    if shuffled_boss.name == "Booster":
                        jinx_size = 3
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(502, [0x00, 0x20]), shadow, solidity, y_shift, location, True))
                        #patch.add_data(0x1dbda9, calcpointer(502, [0x00, 0x00]));
                    elif shuffled_boss.name == "CountDown":
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location, True))
                        #patch.add_data(0x1dbda9, calcpointer(sprite, [0x00, 0x28]));
                        #patch.add_data(0x1Dbdab, [0x80, 0x00])
                    elif freeze or sesw_only:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1Dbda9, calcpointer(sprite, [0x00, 0x08]))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1Dbda9, calcpointer(sprite, [0x00, 0x00]))
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    # if freeze or (not sub_sequence and mold > 0): #dont loop
                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x05, 0x0F, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6bd1, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x06, 0x10, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00, 0xFD, 0x00, 0xFD, 0x0B])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6be4, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x06, 0x08, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x00])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6cb4, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x0C, 0x04, 0xF0, 0x0E])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xF0, 0x1D, 0x10, 0x40, 0x10, 0x80, 0xFD, 0x00, 0x7F, 0x30, 0x00, 0x51, 0x01])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6d2a, False)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x04, 0x10, 0x45, 0x51, 0x02])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x02, 0xFD, 0x01, 0x10, 0x46, 0x53, 0x01, 0xF0, 0x0E])
                        scarecrow_script.append([0x9b])
                        scarecrow_script.append([0x06, 0x10, 0x43, 0x10, 0x81, 0x7E, 0x30, 0x00, 0xFD, 0x9E, 0x79])
                        scarecrow_script.append(
                            [0x61, 0x04, 0x01, 0x61, 0x08, 0x00, 0x61, 0x04, 0xF0, 0x00, 0x07, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xF0, 0x00, 0x06, 0xF0, 0x00, 0x7E, 0x30, 0x00, 0xFD, 0x9E, 0x79, 0x63, 0x04, 0x01, 0x63,
                             0x20, 0x00, 0x63, 0x04, 0xF0, 0x00, 0x07, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xF0, 0x00, 0x06, 0xF0, 0x00, 0x7E, 0x30, 0x00, 0xFD, 0x9E, 0x79, 0x65, 0x04, 0x01, 0x65,
                             0x0A, 0x00, 0x65, 0x04, 0xF0, 0x00, 0x07, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6d3e, False)
                        scarecrow_script = []
                        scarecrow_script.append(
                            [0x0C, 0xF0, 0xF0, 0x18, 0xFD, 0x9E, 0x79, 0x65, 0x04, 0x01, 0x65, 0x0A, 0x00, 0x65, 0x04,
                             0xF0, 0x00, 0x07, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xF0, 0x00, 0x06, 0xF0, 0x00, 0xFD, 0x9E, 0x79, 0x67, 0x04, 0x01, 0x67, 0x10, 0x00, 0x67,
                             0x04, 0xF0, 0x00, 0x07, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xF0, 0x00, 0x06, 0xF0, 0x00, 0xFD, 0x9E, 0x79, 0x61, 0x04, 0x01, 0x61, 0x0A, 0x00, 0x61,
                             0x04, 0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x0B, 0xF0, 0x07])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6dac, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0x80])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1f6e15, True)
                        patch.add_data(0x1F6E69, [0x08, 0x50, sequence])
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x45])
                        scarecrow_script.append([0x9B])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x07, 0xF0, 0x1D, 0x10, 0xC5, 0x53, 0x01])
                        add_scarecrow_script(0, scarecrow_script, 0x1f6eb4, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xC3, 0x07])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x53, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x53, 0x01, 0x01, 0x9C, 0x10, 0xF0, 0x00, 0x9C, 0x16, 0xF0, 0x00, 0x9C, 0x3A, 0xF0, 0x00,
                             0x9C, 0x19, 0xF0, 0x07, 0x9C, 0x19, 0xF0, 0x07, 0x9C, 0x19, 0xF0, 0x00, 0x9C, 0x19, 0xF0,
                             0x07, 0x9C, 0x19, 0xF0, 0x07, 0x9C, 0x19, 0xF0, 0x00, 0x9C, 0x10, 0x00])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x57, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x51, 0x01])
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x80, 0x06, 0x10, 0x9B])
                        #scarecrow_script.append([0x57, 0x04])
                        #scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        #scarecrow_script.append([0x55, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(0, scarecrow_script, 0x1f6efa, False)
                    # if dont_reverse_northeast: #factory clerks
                    # special animations
                    if shuffled_boss.name == "Booster":
                        patch.add_data(0x1f6e69, [0x08, 0x50, 3])
                    elif not freeze and not invert_se_sw:
                        if push_sequence != False:
                            patch.add_data(0x1f6e69, [0x08, 0x50, push_sequence])
                        elif extra_sequence != False:
                            patch.add_data(0x1f6e69, [0x08, 0x50, extra_sequence])
                        else:
                            patch.add_data(0x1f6e69, [0x08, 0x50, sequence])
                    else:
                        patch.add_data(0x1f6e69, [0x9b, 0x9b, 0x9b])

            if location.name == "MegaSmilax":
                # maybe bring shy away back for added comedy
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Megasmilax":
                    # use npc 154, set properties to match smilax's
                    # fix scripts
                    patch.add_data(0x14be2c,
                                   [0x6B, 0xF2, 0xC0, 0xFC, 0x69, 0x00, 0x9B, 0x46, 0x61, 0x00, 0x40, 0x50, 0x2B, 0xF7,
                                    0xC0, 0xFC, 0x09, 0x00, 0x1B])
                    #patch.add_data(0x1dbc36, calcpointer(sprite, [0x00, 0x08]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    patch.add_data(0x1dbc38, [0x80, 0x01, 0x44, 0x07])
                    patch.add_data(0x1fdb24, [0x15, 0xF9])
                    patch.add_data(0x1fdb26, [0x16, 0xF9])
                    patch.add_data(0x1fdb3b, [0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fdb2d, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                    # dingaling needs special properties to work
                    if shuffled_boss.name == "CountDown":
                        patch.add_data(0x1dbC37, 0x29)
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        patch.add_data(0x1fdb28,
                                       SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 254, 2555,
                                                        0x20f299).export_sprite_load())
                    else:
                        patch.add_data(0x1fdb28, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                    if shuffled_boss.name in ["Pandorite", "Hidon", "HammerBro", "BoxBoy", "DodoSolo"]: # shift up a little bit
                        patch.add_data(0x14BE33, 0xC6)
                    #partition
                    patch.add_data(0x14bE28, 0x72)

            if location.name == "Dodo":
                # always replace npc sprite here, it's normally just the feather
                #print(location.name + ": " + shuffled_boss.name)
                # load dodo in save room if you won statue game
                sub_sequence = True
                if sequence == 0 and mold > 0:
                    sub_sequence = False
                spritePhaseEvents.append(
                    SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, True, 112, 2108,
                                     0x20eb10))
                patch.add_data(0x1F759F, [0x9B, 0x9B, 0x9B])
                patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x88]), shadow, solidity, y_shift, location))

            if location.name == "Valentina":
                #print(location.name + ": " + shuffled_boss.name)
                #statue vars
                total_shift = [0x84]
                total_opposite_shift = [0x84]
                total_opposite_dodo_shift = [0x84]
                northwest_109 = [3, 4, 5]
                northwest_115 = [1]
                northwest_122 = [1]
                northwest_120 = [1]
                northeast_110 = [0, 1, 2]
                south_109 = [0, 1, 2]
                south_115 = [0]
                south_122 = [0]
                south_120 = [0]
                patch.add_data(0x209034, [0x9B, 0x9B, 0x9B, 0x9B]) # remove the "is valentina cleared" check that fails to position statues in dodo minigame
                new_preloader_event(112, [0x15, 0xF9, 0xF2, 0x70, 0x2A], 2108, 0x20EB10) #remove from level 112
                if shuffled_boss.name != "Valentina":
                    if freeze or sesw_only:
                        #patch.add_data(0x1db988, calcpointer(sprite, [0x00, 0x08]))
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                        patch.add_data(location.statue_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                        patch.add_data(location.statue_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1db988, calcpointer(sprite, [0x00, 0x00]))
                        #patch.add_data(0x1db9B9, calcpointer(sprite, [0x00, 0x00]))
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if shuffled_boss.name in ["Culex", "DodoSolo"]:
                        # use partition 82
                        patch.add_data(0x14DFCC, 0x52)
                        patch.add_data(0x14DD18, 0x52)
                        remove_shadows(416, 16, 3642, 0x20F987)
                        remove_shadows(430, 12, 738, 0x20FA1A)
                        #remove mario's shadow after trampoline
                        patch.add_data(0x20963B, calcpointer(262, [0x00, 0x00]))
                    if overworld_is_skinny:
                    # garro's house, use partition 12
                        patch.add_data(0x14CD61, 0x0C)
                    elif overworld_is_empty:
                        #garro's house, use partition 32 and remove shadows
                        patch.add_data(0x14CD61, 0x20)
                        remove_shadows(341, 11, 737, 0x20F595)

                    bosses_that_need_alternate_flip_condition = ["KnifeGuy", "Croco1", "Croco2", "Clerk", "Manager", "Director"]
                    if shuffled_boss.statue_east_shift or shuffled_boss.statue_southeast_shift or shuffled_boss.statue_south_shift or shuffled_boss.statue_southwest_shift or shuffled_boss.statue_west_shift or shuffled_boss.statue_northwest_shift or shuffled_boss.statue_north_shift or shuffled_boss.statue_northeast_shift or shuffled_boss.opposite_statue_east_shift or shuffled_boss.opposite_statue_southeast_shift or shuffled_boss.opposite_statue_south_shift or shuffled_boss.opposite_statue_southwest_shift or shuffled_boss.opposite_statue_west_shift or shuffled_boss.opposite_statue_northwest_shift or shuffled_boss.opposite_statue_north_shift or shuffled_boss.opposite_statue_northeast_shift:
                        if not sesw_only:
                            #east-west for south-facing sprites
                            if shuffled_boss.statue_east_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_east_shift), 2))
                            elif shuffled_boss.statue_west_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_west_shift * -1), 2))
                            else:
                                total_shift.append(0)

                            #east-west for north-facing sprites
                            if shuffled_boss.name in bosses_that_need_alternate_flip_condition:
                                if shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                                    total_opposite_npc1_dodo_shift = []
                                    if shuffled_boss.statue_east_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_east_shift * -1), 2))
                                        total_opposite_npc1_dodo_shift.append(int(bin(0), 2))
                                    elif shuffled_boss.statue_west_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_west_shift * -1), 2))
                                        total_opposite_npc1_dodo_shift.append(int(bin(0), 2))
                                    else:
                                        total_opposite_npc1_dodo_shift.append(0)
                                        total_opposite_dodo_shift.append(0)
                                else:
                                    if shuffled_boss.statue_east_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_east_shift * -1), 2))
                                    elif shuffled_boss.statue_west_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_west_shift * -1), 2))
                                    else:
                                        total_opposite_dodo_shift.append(0)
                                if shuffled_boss.opposite_statue_east_shift:
                                    total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift), 2))
                                elif shuffled_boss.opposite_statue_west_shift:
                                    total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift * -1), 2))
                                else:
                                    total_opposite_shift.append(0)
                            else:
                                if shuffled_boss.name in ["Gunyolk"]:
                                    if shuffled_boss.statue_east_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_east_shift * -1 - 5), 2))
                                    elif shuffled_boss.statue_west_shift:
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.statue_west_shift * -1 - 5), 2))
                                    else:
                                        total_opposite_dodo_shift.append(0)
                                    if shuffled_boss.opposite_statue_east_shift:
                                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift), 2))
                                    elif shuffled_boss.opposite_statue_west_shift:
                                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift * -1), 2))
                                    else:
                                        total_opposite_shift.append(0)
                                else:
                                    if shuffled_boss.opposite_statue_east_shift:
                                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift), 2))
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift * -1), 2))
                                    elif shuffled_boss.opposite_statue_west_shift:
                                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift * -1), 2))
                                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift), 2))
                                    else:
                                        total_opposite_shift.append(0)
                                        total_opposite_dodo_shift.append(0)

                            #north-south
                            if shuffled_boss.statue_south_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_south_shift), 2))
                            elif shuffled_boss.statue_north_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_north_shift * -1), 2))
                            else:
                                total_shift.append(0)
                            if shuffled_boss.opposite_statue_south_shift:
                                total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_south_shift), 2))
                                total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_south_shift), 2))
                            elif shuffled_boss.opposite_statue_north_shift:
                                total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_north_shift * -1), 2))
                                total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_north_shift * -1), 2))
                            else:
                                total_opposite_shift.append(0)
                                total_opposite_dodo_shift.append(0)
                        else:
                            if shuffled_boss.statue_east_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_east_shift), 2))
                            elif shuffled_boss.statue_west_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_west_shift * -1), 2))
                            else:
                                total_shift.append(0)
                            if shuffled_boss.statue_south_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_south_shift), 2))
                            elif shuffled_boss.statue_north_shift:
                                total_shift.append(int(bin(shuffled_boss.statue_north_shift * -1), 2))
                            else:
                                total_shift.append(0)
                            total_opposite_dodo_shift = total_shift.copy()
                    elif shuffled_boss.name not in ["DodoSolo"]:
                        total_shift.extend([0, 0])
                        total_opposite_dodo_shift.extend([0, 0])
                        if not sesw_only:
                            total_opposite_shift.extend([0, 0])

                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, northeast, False, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x10, 0x81, 0x57, 0x02, 0x10, 0x45, 0x10, 0x80, 0x47, 0x10, 0x45, 0x67, 0x08, 0x10, 0x80,
                             0x10, 0x46, 0x67, 0x08])
                        add_scarecrow_script(9, scarecrow_script, 0x1ea357, True)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea3de, True)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea401, True)
                        scarecrow_script = []
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x04])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0x10, 0x43, 0x06, 0x67, 0x02, 0xD4, 0x09, 0x63, 0x04, 0x67, 0x04, 0xD7])
                        add_scarecrow_script(9, scarecrow_script, 0x1ea424, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x09])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea50d, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x06, 0x10, 0x40, 0x04, 0x62, 0x0C, 0x05, 0x07])
                        add_scarecrow_script(9, scarecrow_script, 0x1ea51F, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x01])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea56E, True)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea590, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x01])
                        scarecrow_script.append(get_directional_command(plus, northeast, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea598, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        add_scarecrow_script(9, scarecrow_script, 0x1ea5a2, False)
                        #statues
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, (southwest if sesw_only else northeast), True, sequence, is_scarecrow))
                        if len(total_opposite_dodo_shift) == 3:
                            scarecrow_script.append(total_opposite_dodo_shift)
                            scarecrow_script.append([0x9b])
                        else:
                            scarecrow_script.append([0x9b, 0x9b, 0x9b, 0x9b])
                        add_scarecrow_script(0, scarecrow_script, 0x1F7658, True, False, statue_mold)
                        add_scarecrow_script(1, scarecrow_script, 0x1F765F, True, False, statue_mold)
                        add_scarecrow_script(2, scarecrow_script, 0x1F7666, False, False, statue_mold)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, (southwest if sesw_only else northeast), True, sequence, is_scarecrow))
                        if len(total_opposite_dodo_shift) == 3:
                            scarecrow_script.append(total_opposite_dodo_shift)
                            scarecrow_script.append([0x9b, 0x9b, 0x9B])
                        else:
                            scarecrow_script.append([0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1F76A2, True, False, statue_mold)
                        add_scarecrow_script(1, scarecrow_script, 0x1F76AB, True, False, statue_mold)
                        add_scarecrow_script(2, scarecrow_script, 0x1F76B4, False, False, statue_mold)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, (southwest if sesw_only else northeast), True, sequence, is_scarecrow))
                        if len(total_opposite_dodo_shift) == 3:
                            scarecrow_script.append(total_opposite_dodo_shift)
                            scarecrow_script.append([0x9b])
                        else:
                            scarecrow_script.append([0x9b, 0x9b, 0x9b, 0x9b])
                        add_scarecrow_script(0, scarecrow_script, 0x20903C, True, False, statue_mold)
                        add_scarecrow_script(1, scarecrow_script, 0x209043, True, False, statue_mold)
                        add_scarecrow_script(2, scarecrow_script, 0x20904A, False, False, statue_mold)

                    # preload if needed
                    #then load sequence
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(9, plus, mold, sub_sequence, sequence, True, 430, 738, 0x20fa1a))
                    if invert_se_sw:
                        spritePhaseEvents.append(
                            SpritePhaseEvent([3, 4, 5], plus, mold, sub_sequence, [0, 0, 0],
                                             [True, True, True], 341, 737, 0x20F595))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1, 2, 3, 4, 5, 6], plus, mold, sub_sequence, [1, 1, 1, 0, 0, 0, 0],
                                             [True, True, True, True, True, True, True], 109, 3670, 0x20EAFB))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 0], [True, True], 115, 3730,
                                             0x20EB31))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 0], [True, True], 122, 3726,
                                             0x20EBAE))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 0], [True, True], 120, 3729,
                                             0x20EB79))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1, 2], plus, mold, sub_sequence, [0, 0, 0], [False, False, False], 110,
                                             2112, 0x20EB0A))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(3, plus, mold, sub_sequence, 0, True, 113, 15,
                                             0x20EB1F))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([6, 7], plus, mold, sub_sequence, [1, 0], [True, True], 119, 3701,
                                             0x20EB70))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([6, 7], plus, mold, sub_sequence, [1, 0], [True, True], 408, 3702,
                                             0x20F945))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([1, 2, 3, 4], plus, mold, sub_sequence, [1, 0, 0, 1], [True, True, True, True], 499, 3762,
                                             0x20FDA2))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 0], [True, True], 501, 15,
                                             0x20FDA8))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 0], [True, True], 440, 3740,
                                             0x20FA73))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 0], [True, True], 497, 15,
                                             0x20FD96))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [1, 1, 0, 0], [True, True, True, True], 447, 3756, 0x20FACF))
                        #wont face properly unless you set all to face south
                        patch.add_data(0x149e56, 0x23)
                        patch.add_data(0x149e5A, 0x23)
                        patch.add_data(0x149e5E, 0x23)
                        patch.add_data(0x149eAB, 0x21)
                        patch.add_data(0x149eAF, 0x21)
                        patch.add_data(0x149eB3, 0x21)
                        patch.add_data(0x149FC0, 0x21)
                        patch.add_data(0x14A151, 0x21)
                        patch.add_data(0x14A1FB, 0x23)
                        patch.add_data(0x14CD6D, 0x20)
                        patch.add_data(0x14CD71, 0x22)
                        patch.add_data(0x14CD75, 0x22)
                        #post-fight statues
                        patch.add_data(0x149F62, 0x21)
                        patch.add_data(0x14A13C, 0x21)
                        patch.add_data(0x14A140, 0x21)
                        patch.add_data(0x14DB3C, 0x21)
                        patch.add_data(0x14DB40, 0x21)
                        patch.add_data(0x14E1E8, 0x21)
                        patch.add_data(0x14E1EC, 0x21)
                        patch.add_data(0x14ED4C, 0x21)
                        patch.add_data(0x14ED50, 0x21)
                        patch.add_data(0x14EDB6, 0x21)
                        patch.add_data(0x14EDBA, 0x21)
                        patch.add_data(0x14EDBE, 0x21)
                        patch.add_data(0x14EDC2, 0x21)
                        patch.add_data(0x14EE20, 0x21)
                        patch.add_data(0x14EE24, 0x21)
                        patch.add_data(0x14e306, 0x25)
                        patch.add_data(0x14e30A, 0x25)
                        patch.add_data(0x14e30E, 0x25)
                        patch.add_data(0x14e312, 0x25)
                    elif shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                        patch.add_data(0x149eAB, 0x61)
                        patch.add_data(0x149eAF, 0x61)
                        patch.add_data(0x149eB3, 0x61)
                        #post-fight statues
                        patch.add_data(0x149F62, 0x61)
                        patch.add_data(0x14A13C, 0x21)
                        patch.add_data(0x14A140, 0x61)
                        patch.add_data(0x14DB3C, 0x21)
                        patch.add_data(0x14DB40, 0x61)
                        patch.add_data(0x14E1E8, 0x21)
                        patch.add_data(0x14E1EC, 0x61)
                        patch.add_data(0x14ED4C, 0x61)
                        patch.add_data(0x14ED50, 0x61)
                        patch.add_data(0x14EDB6, 0x21)
                        patch.add_data(0x14EDBA, 0x61)
                        patch.add_data(0x14EDBE, 0x61)
                        patch.add_data(0x14EDC2, 0x21)
                        patch.add_data(0x14EE20, 0x21)
                        patch.add_data(0x14EE24, 0x61)
                        patch.add_data(0x14e306, 0x25)
                        patch.add_data(0x14e30A, 0x25)
                        patch.add_data(0x14e30E, 0x65)
                        patch.add_data(0x14e312, 0x65)
                        spritePhaseEvents.append(
                            SpritePhaseEvent([3, 4, 5], plus, mold, sub_sequence, [1, 1, 1],
                                             [True, True, True], 341, 737, 0x20F595))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1, 2, 3, 4, 5, 6], plus, mold, sub_sequence, [0, 0, 0, 1, 1, 1, 1],
                                             [True, True, True, True, True, True, True], 109, 3670, 0x20EAFB))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 1], [True, True], 115, 3730,
                                             0x20EB31))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 1], [True, True], 122, 3726,
                                             0x20EBAE))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 1], [True, True], 120, 3729,
                                             0x20EB79))
                        # spritePhaseEvents.append(
                        #     SpritePhaseEvent([0, 1, 2], plus, mold, sub_sequence, [1, 1, 1], [True, True, True], 110,
                        #                      2112, 0x20EB0A))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(3, plus, mold, sub_sequence, 0, True, 113, 15,
                                             0x20EB1F))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([6, 7], plus, mold, sub_sequence, [0, 1], [False, False], 119, 3701,
                                             0x20EB70))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([6, 7], plus, mold, sub_sequence, [0, 1], [False, False], 408, 3702,
                                             0x20F945))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([1, 2, 3, 4], plus, mold, sub_sequence, [0, 1, 1, 0], [False, True, True, False], 499, 3762,
                                             0x20FDA2))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 1], [False, True], 501, 15,
                                             0x20FDA8))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [0, 1], [False, True], 440, 3740,
                                             0x20FA73))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1], plus, mold, sub_sequence, [1, 1], [True, True], 497, 15,
                                             0x20FD96))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [0, 0, 1, 1], [False, False, True, True], 447, 3756, 0x20FACF))
                    elif sequence > 0 or statue_mold != None or sesw_only or freeze:
                        mold = statue_mold
                        if sequence == 0:
                            mold = 0
                        if mold != None:
                            sub_sequence = False
                        if sesw_only:
                            patch.add_data(0x149e4a, 0x63)
                            patch.add_data(0x149e4e, 0x63)
                            patch.add_data(0x149e52, 0x63)
                            patch.add_data(0x149eab, 0x61)
                            patch.add_data(0x149eaf, 0x61)
                            patch.add_data(0x149eb3, 0x61)
                            patch.add_data(0x149fbc, 0x61)
                            patch.add_data(0x14a14d, 0x61)
                            patch.add_data(0x14a1f7, 0x63)
                            patch.add_data(0x14e306, 0x65)
                            patch.add_data(0x14e30A, 0x65)
                            patch.add_data(0x14e30E, 0x65)
                            patch.add_data(0x14e312, 0x65)
                            #post-fight statues
                            patch.add_data(0x149F62, 0x61)
                            patch.add_data(0x14A13C, 0x61)
                            patch.add_data(0x14A140, 0x61)
                            patch.add_data(0x14DB3C, 0x61)
                            patch.add_data(0x14DB40, 0x61)
                            patch.add_data(0x14E1E8, 0x61)
                            patch.add_data(0x14E1EC, 0x61)
                            patch.add_data(0x14ED4C, 0x61)
                            patch.add_data(0x14ED50, 0x61)
                            patch.add_data(0x14EDB6, 0x61)
                            patch.add_data(0x14EDBA, 0x61)
                            patch.add_data(0x14EDBE, 0x61)
                            patch.add_data(0x14EDC2, 0x61)
                            patch.add_data(0x14EE20, 0x61)
                            patch.add_data(0x14EE24, 0x61)
                            spritePhaseEvents.append(
                                SpritePhaseEvent([3, 4, 5], plus, [mold, mold, mold], sub_sequence, [sequence,
                                                                       sequence, sequence],
                                                 [False, False, False], 341, 737, 0x20F595))
                            spritePhaseEvents.append(SpritePhaseEvent([0, 1, 2, 3, 4, 5, 6], plus, [mold, mold, mold, mold, mold, mold, mold], sub_sequence,
                                                                      [sequence, sequence, sequence, sequence, sequence,
                                                                       sequence, sequence],
                                                                      [False, False, False, False, False, False, True], 109,
                                                                      3670, 0x20EAFB))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 115,
                                                 3730, 0x20EB31))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 122,
                                                 3726, 0x20EBAE))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 120,
                                                 3729, 0x20EB79))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1, 2], plus, [mold, mold, mold], sub_sequence, [sequence, sequence, sequence],
                                                 [False, False, False], 110, 2112, 0x20EB0A))
                            spritePhaseEvents.append(
                                SpritePhaseEvent(3, plus, mold, sub_sequence, 0, False, 113, 15,
                                                 0x20EB1F))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([6, 7], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 119, 3701,
                                                 0x20EB70))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([6, 7], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 408, 3702,
                                                 0x20F945))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [sequence, sequence, sequence, sequence], [False, False, False, False], 499, 3762,
                                                 0x20FDA2))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 501, 15,
                                                 0x20FDA8))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 440, 3740,
                                                 0x20FA73))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [False, False], 497, 15,
                                             0x20FD96))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [sequence, sequence, sequence, sequence], [False, False, False, False], 447, 3756, 0x20FACF))
                        else:
                            spritePhaseEvents.append(
                                SpritePhaseEvent([3, 4, 5], plus, [mold, mold, mold], sub_sequence, [sequence,
                                                                       sequence, sequence],
                                                 [False, False, False], 341, 737, 0x20F595))
                            spritePhaseEvents.append(SpritePhaseEvent([0, 1, 2, 3, 4, 5, 6], plus, [mold, mold, mold, mold, mold, mold, mold], sub_sequence,
                                                                      [sequence, sequence, sequence, sequence, sequence,
                                                                       sequence, sequence],
                                                                      [True, True, True, False, False, False, True], 109,
                                                                      3670, 0x20EAFB))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 115,
                                                 3730, 0x20EB31))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 122,
                                                 3726, 0x20EBAE))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 120,
                                                 3729, 0x20EB79))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1, 2], plus, [mold, mold, mold], sub_sequence, [sequence, sequence, sequence],
                                                 [True, True, True], 110, 2112, 0x20EB0A))
                            spritePhaseEvents.append(
                                SpritePhaseEvent(3, plus, mold, sub_sequence, 0, False, 113, 15,
                                                 0x20EB1F))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([6, 7], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 119, 3701,
                                                 0x20EB70))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([6, 7], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 408, 3702,
                                                 0x20F945))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [sequence, sequence, sequence, sequence], [True, False, False, True], 499, 3762,
                                                 0x20FDA2))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 501, 15,
                                                 0x20FDA8))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 440, 3740,
                                                 0x20FA73))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([0, 1], plus, [mold, mold], sub_sequence, [sequence, sequence], [True, False], 497, 15,
                                             0x20FD96))
                            spritePhaseEvents.append(
                                SpritePhaseEvent([1, 2, 3, 4], plus, [mold, mold, mold, mold], sub_sequence, [sequence, sequence, sequence, sequence], [True, True, False, False], 447, 3756, 0x20FACF))



                    if len(total_shift) > 1 or len(total_opposite_shift) > 1:
                        northwest_109 = [3, 4, 5]
                        northwest_115 = [1]
                        northwest_122 = [1]
                        northwest_120 = [1]
                        northwest_341 = [3, 4, 5]
                        northwest_113 = [3]
                        northwest_119 = [7]
                        northwest_408 = [7]
                        northwest_499 = [2, 3]
                        northwest_501 = [1]
                        northwest_440 = [1]
                        northwest_497 = [0, 1]
                        northwest_447 = [3, 4]

                        northeast_110 = [0, 1, 2]

                        south_109 = [0, 1, 2]
                        south_115 = [0]
                        south_122 = [0]
                        south_120 = [0]
                        south_119 = [6]
                        south_408 = [6]
                        south_499 = [1, 4]
                        south_501 = [0]
                        south_440 = [0]
                        south_447 = [1, 2]

                        if not sesw_only:
                            if len(total_shift) > 1:
                                for npc in south_109:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(109, npc_queue, 3670, 0x20EAFB)
                                for npc in south_115:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                                for npc in south_122:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                                for npc in south_120:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                                for npc in south_499:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                                for npc in south_501:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                                for npc in south_440:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                                for npc in south_447:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(447, npc_queue, 3756, 0x20FACF)
                                if overworld_is_skinny:
                                    for npc in south_119:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(119, npc_queue, 3701, 0x20EB70)
                                    for npc in south_408:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(408, npc_queue, 3702, 0x20F945)
                            if len(total_opposite_shift) > 1:
                                for npc in northwest_109:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(109, npc_queue, 3670, 0x20EAFB)
                                for npc in northwest_115:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                                for npc in northwest_122:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                                for npc in northwest_120:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                                for npc in northeast_110:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_dodo_shift)
                                    new_preloader_event(110, npc_queue, 2112, 0x20EB0A)
                                for npc in northwest_341:
                                    if is_scarecrow:
                                        npc_queue = [0x14 + npc, 0x80 + len(total_opposite_dodo_shift)]
                                    else:
                                        npc_queue = [0x14 + npc, len(total_opposite_dodo_shift)]
                                    npc_queue.extend(total_opposite_dodo_shift)
                                    new_preloader_event(341, npc_queue, 737, 0x20F595)
                                for npc in northwest_113:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(113, npc_queue, 15, 0x20EB1F)
                                for npc in northwest_499:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                                for npc in northwest_501:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                                for npc in northwest_440:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                                for npc in northwest_497:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(497, npc_queue, 15, 0x20FD96)
                                for npc in northwest_447:
                                    npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                    npc_queue.extend(total_opposite_shift)
                                    new_preloader_event(447, npc_queue, 3756, 0x20FACF)
                                if overworld_is_skinny:
                                    for npc in northwest_119:
                                        npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                        npc_queue.extend(total_opposite_shift)
                                        new_preloader_event(119, npc_queue, 3701, 0x20EB70)
                                    for npc in northwest_408:
                                        npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                        npc_queue.extend(total_opposite_shift)
                                        new_preloader_event(408, npc_queue, 3702, 0x20F945)
                        else:
                            if len(total_shift) > 0:
                                for npc in south_109:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(109, npc_queue, 3670, 0x20EAFB)
                                for npc in south_115:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                                for npc in south_122:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                                for npc in south_120:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                                for npc in south_499:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                                for npc in south_501:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                                for npc in south_440:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                                for npc in south_447:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(447, npc_queue, 3756, 0x20FACF)
                                for npc in northwest_109:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(109, npc_queue, 2112, 0x20EB0A)
                                for npc in northwest_115:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                                for npc in northwest_122:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                                for npc in northwest_120:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                                for npc in northwest_341:
                                    if is_scarecrow:
                                        npc_queue = [0x14 + npc, 0x80 + len(total_shift)]
                                    else:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(341, npc_queue, 737, 0x20F595)
                                for npc in northeast_110:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(110, npc_queue, 2112, 0x20EB0A)
                                for npc in northwest_113:
                                    npc_queue = [0x14 + npc, len(total_opposite_dodo_shift)]
                                    npc_queue.extend(total_opposite_dodo_shift)
                                    new_preloader_event(113, npc_queue, 15, 0x20EB1F)
                                for npc in northwest_499:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                                for npc in northwest_501:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                                for npc in northwest_440:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                                for npc in northwest_497:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(497, npc_queue, 15, 0x20FD96)
                                for npc in northwest_447:
                                    npc_queue = [0x14 + npc, len(total_shift)]
                                    npc_queue.extend(total_shift)
                                    new_preloader_event(447, npc_queue, 3756, 0x20FACF)
                                if overworld_is_skinny or shuffled_boss.name in ["DodoSolo", "Culex"]:
                                    for npc in northwest_119:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(119, npc_queue, 3701, 0x20EB70)
                                    for npc in northwest_408:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(408, npc_queue, 3702, 0x20F945)
                                    for npc in south_119:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(119, npc_queue, 3701, 0x20EB70)
                                    for npc in south_408:
                                        npc_queue = [0x14 + npc, len(total_shift)]
                                        npc_queue.extend(total_shift)
                                        new_preloader_event(408, npc_queue, 3702, 0x20F945)


                    # align in polishing room
                    if not (freeze or invert_se_sw):
                        if sesw_only:
                            direction = 0x73
                        elif shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                            direction = 0x75
                        else:
                            direction = 0x77 # is this misaligning everyone else?
                        if len(total_opposite_dodo_shift) == 3: #overwrite 9Bs in dodo events if necessary
                            long_dodo_shift = total_opposite_dodo_shift.copy()
                            short_dodo_shift = total_opposite_dodo_shift.copy()
                            if shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                                freeze_dodo_shift = total_opposite_npc1_dodo_shift.copy()
                                long_freeze_dodo_shift = total_opposite_npc1_dodo_shift.copy()
                                secondary_short_dodo_shift = total_opposite_dodo_shift.copy();
                                secondary_short_dodo_shift.extend([0x9B, 0x75])
                                freeze_dodo_shift.extend([0x9B, 0x75])
                                long_freeze_dodo_shift.extend([0x9B, 0x75])
                            long_dodo_shift.extend([0x9b, 0x9b, 0x9B, direction])
                            short_dodo_shift.extend([0x9B, direction])
                            if shuffled_boss.name in ["Clerk", "Manager", "Director"]: #i hate this solution lol
                                patch.add_data(0x1F765A, short_dodo_shift)
                                patch.add_data(0x1F7661, freeze_dodo_shift)
                                patch.add_data(0x1F7668, freeze_dodo_shift)
                                patch.add_data(0x20903E, secondary_short_dodo_shift)
                                patch.add_data(0x209045, secondary_short_dodo_shift)
                                patch.add_data(0x20904C, secondary_short_dodo_shift)
                                patch.add_data(0x1F76A4, long_dodo_shift)
                                patch.add_data(0x1F76AD, long_freeze_dodo_shift)
                                patch.add_data(0x1F76B6, long_freeze_dodo_shift)
                            else:
                                patch.add_data(0x1F765A, short_dodo_shift)
                                patch.add_data(0x1F7661, short_dodo_shift)
                                patch.add_data(0x1F7668, short_dodo_shift)
                                patch.add_data(0x20903E, short_dodo_shift)
                                patch.add_data(0x209045, short_dodo_shift)
                                patch.add_data(0x20904C, short_dodo_shift)
                                patch.add_data(0x1F76A4, long_dodo_shift)
                                patch.add_data(0x1F76AD, long_dodo_shift)
                                patch.add_data(0x1F76B6, long_dodo_shift)
                        else:
                            patch.add_data(0x1F76A4, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                            patch.add_data(0x1F76AD, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                            patch.add_data(0x1F76B6, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                            patch.add_data(0x1F765A, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                            patch.add_data(0x1F7661, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                            patch.add_data(0x1F7668, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                            patch.add_data(0x20903E, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                            patch.add_data(0x209045, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                            patch.add_data(0x20904C, [0x9b, 0x9b, 0x9b, 0x9b, direction])

                    #room 110 has to go after pixel shifting for these bosses for some reason... this is just ignorant
                    if shuffled_boss.name in ["Clerk", "Manager", "Director"]:
                        spritePhaseEvents.append(
                            SpritePhaseEvent([0, 1, 2], plus, [mold, mold, mold], sub_sequence, [1, 1, 1], [False, False, False], 110,
                                             2112, 0x20EB0A))
                    #statue partitions
                    if overworld_is_skinny:
                        ###statues
                        ##room 109
                        # change partition to 12
                        patch.add_data(0x149e3e, 0x0c)
                        ##room 115
                        # change partition to 72
                        patch.add_data(0x149FB0, 0x48)
                        ##room 122
                        # change partition to 82
                        patch.add_data(0x14A1EB, 0x52)
                        ##room 120
                        # change partition to 82
                        patch.add_data(0x14A141, 0x52)
                        ##room 110
                        # change partition to 93
                        patch.add_data(0x149E9F, 0x5D)
                        ##room 119
                        # change partition to 72
                        patch.add_data(0x14A0F0, 0x48)
                        ##room 499
                        # modify partition 34 and use it
                        patch.add_data(0x1DDE88, [0xA0, 0x82, 0x81, 0x84])
                        patch.add_data(0x14ED9E, 0x22)
                        ##room 501
                        # change partition to 23
                        patch.add_data(0x14EE14, 0x17)
                        ##room 440
                        # modify partition 33 and use it
                        patch.add_data(0x1DDE84, [0xA0, 0x87, 0x81, 0x80])
                        patch.add_data(0x14E1DC, 0x21)
                        ##room 497
                        # change partition to 9
                        patch.add_data(0x14ED40, 0x09)
                        ##room 447
                        # change partition to 64
                        patch.add_data(0x14E2EE, 0x40)
                    else:
                        #remove statue in room 113, partitions are too screwy in here due to the statue swap
                        new_preloader_event(113, [0xF2, 0x71, 0x2E, 0x17, 0xF9], 15, 0x20EB1F)
                    if overworld_is_empty:
                        remove_shadows(109, 11, 3670, 0x20EAFB)
                        remove_shadows(120, 9, 3729, 0x20EB79)
                        if shuffled_boss.name == "Exor":
                            ##room 109
                            # breaks shadow...
                            # modify partition 8 and use it
                            patch.add_data(0x1DDE20, [0xB3, 0x87, 0x87, 0x87])
                            patch.add_data(0x149e3e, 0x08)
                            ##room 115, 501
                            # use partition 8
                            patch.add_data(0x149FB0, 0x08)
                            patch.add_data(0x14EE14, 0x08)
                            ##room 122
                            # modify partition 10 and use it
                            patch.add_data(0x1DDE28, [0xA3, 0x87, 0x87, 0x87])
                            patch.add_data(0x14A1EB, 0x0A)
                            ##room 120, 440 and also 497
                            # modify partition 17 and use it
                            patch.add_data(0x14A141, 0x11)
                            patch.add_data(0x14E1Dc, 0x11)
                            patch.add_data(0x1DDE44, [0xB1, 0x87, 0x87, 0x87])
                            patch.add_data(0x14ED40, 0x11)
                            remove_shadows(440, 10, 3740, 0x20FA73)
                            ##room 110
                            # use partition 8
                            patch.add_data(0x149E9F, 0x08)
                            ##room 499
                            # use parition 32
                            patch.add_data(0x14ED9E, 0x20)
                            remove_shadows(499, 9, 3762, 0x20FDA2)
                            ##room 447
                            # change partition to 10, like room 122
                            patch.add_data(0x14E2EE, 0x0A)
                        else:
                            # countdown, hammerbro, chest monsters all work with this
                            # change npc properties
                            if shuffled_boss.name == "CountDown":
                                patch.add_data(0x1DB9BA, 0x21)
                                patch.add_data(0x1DB989, 0x21)
                            elif shuffled_boss.name == "HammerBro":
                                patch.add_data(0x1DB9BA, 0x22)
                                patch.add_data(0x1DB989, 0x22)
                            ##room 109
                            # modify partition 8 and use it
                            patch.add_data(0x1DDE20, [0xB0, 0x87, 0x85, 0x85])
                            patch.add_data(0x149e3e, 0x08)
                            ##room 115, 501
                            # use partition 8
                            patch.add_data(0x149FB0, 0x08)
                            patch.add_data(0x14EE14, 0x08)
                            ##room 122
                            # modify partition 10 and use it
                            patch.add_data(0x1DDE28, [0xB0, 0x87, 0x87, 0x87])
                            patch.add_data(0x14A1EB, 0x0A)
                            ##room 120, 440 and also 497
                            # modify partition 17 and use it
                            patch.add_data(0x14A141, 0x11)
                            patch.add_data(0x14E1Dc, 0x11)
                            patch.add_data(0x1DDE44, [0xB0, 0x87, 0x87, 0x87])
                            patch.add_data(0x14ED40, 0x11)
                            remove_shadows(440, 10, 3740, 0x20FA73)
                            ##room 110
                            # use partition 8
                            patch.add_data(0x149E9F, 0x08)
                            ##room 499
                            # use parition 32
                            patch.add_data(0x14ED9E, 0x20)
                            remove_shadows(499, 9, 3762, 0x20FDA2)
                            ##room 447
                            # change partition to 32
                            patch.add_data(0x14E2EE, 0x20)
                            if shuffled_boss.name in ["CountDown", "HammerBro"]:
                                #remove birds in room 499, graphics engine cant handle all NPCs and size 1 sprites
                                new_preloader_event(499, [0xF2, 0xF3, 0x39, 0xF2, 0xF3, 0x3B, 0x1C, 0xF9, 0x1D, 0xF9], 3762, 0x20FDA2)

                    if shuffled_boss.name in ["Pandorite", "Hidon", "HammerBro", "Culex", "BoxBoy", "DodoSolo"]: # shift up a little bit
                        patch.add_data(0x149E49, 0x9A)
                        patch.add_data(0x149E4D, 0x97)
                        patch.add_data(0x149E51, 0x93)
                        patch.add_data(0x149E55, 0x9F)
                        patch.add_data(0x149E59, 0x9C)
                        patch.add_data(0x149E5D, 0x96)
                        patch.add_data(0x149E61, 0x9E)
                        patch.add_data(0x149EAA, 0xBE)
                        patch.add_data(0x149EAE, 0xC1)
                        patch.add_data(0x149EB2, 0xC7)
                        patch.add_data(0x149F61, 0xB5)
                        patch.add_data(0x149FBB, 0x90)
                        patch.add_data(0x149FBE, 0x93)
                        patch.add_data(0x14A13B, 0x94)
                        patch.add_data(0x14A13F, 0x97)
                        patch.add_data(0x14A14C, 0xBC)
                        patch.add_data(0x14A150, 0xBF)
                        patch.add_data(0x14A1F6, 0xFB)
                        patch.add_data(0x14A1FA, 0xFE)
                        patch.add_data(0x14DB3B, 0x94)
                        patch.add_data(0x14DB3F, 0x97)
                        patch.add_data(0x14E1E7, 0xBC)
                        patch.add_data(0x14E1EB, 0xBF)
                        patch.add_data(0x14ED4B, 0x99)
                        patch.add_data(0x14ED4F, 0x92)
                        patch.add_data(0x14EDB5, 0xEB)
                        patch.add_data(0x14EDB9, 0xFC)
                        patch.add_data(0x14EDBD, 0xEE)
                        patch.add_data(0x14EDC1, 0xF9)
                        patch.add_data(0x14EE1F, 0x90)
                        patch.add_data(0x14EE24, 0x93)
                        patch.add_data(0x14CD80, 0x99)
                        patch.add_data(0x14CD84, 0x98)
                        patch.add_data(0x14CD88, 0x97)
                        patch.add_data(0x14E305, 0xF2)
                        patch.add_data(0x14E309, 0xEE)
                        patch.add_data(0x14E30D, 0xF2)
                        patch.add_data(0x14E311, 0xF6)


                else: #shift vanilla statues

                    if shuffled_boss.statue_east_shift:
                        total_shift.append(int(bin(shuffled_boss.statue_east_shift), 2))
                    elif shuffled_boss.statue_west_shift:
                        total_shift.append(int(bin(shuffled_boss.statue_west_shift * -1), 2))
                    else:
                        total_shift.append(0)
                    if shuffled_boss.statue_south_shift:
                        total_shift.append(int(bin(shuffled_boss.statue_south_shift), 2))
                    elif shuffled_boss.statue_north_shift:
                        total_shift.append(int(bin(shuffled_boss.statue_north_shift * -1), 2))
                    else:
                        total_shift.append(0)
                    if shuffled_boss.opposite_statue_east_shift:
                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift), 2))
                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_east_shift), 2))
                    elif shuffled_boss.opposite_statue_west_shift:
                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift * -1), 2))
                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_west_shift * -2), 2))
                    else:
                        total_opposite_shift.append(0)
                        total_opposite_dodo_shift.append(0)
                    if shuffled_boss.opposite_statue_south_shift:
                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_south_shift), 2))
                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_south_shift), 2))
                    elif shuffled_boss.opposite_statue_north_shift:
                        total_opposite_shift.append(int(bin(shuffled_boss.opposite_statue_north_shift * -1), 2))
                        total_opposite_dodo_shift.append(int(bin(shuffled_boss.opposite_statue_north_shift * -2), 2))
                    else:
                        total_opposite_shift.append(0)
                        total_opposite_dodo_shift.append(0)
                    if len(total_shift) > 1 or len(total_opposite_shift) > 1:

                        northwest_109 = [3, 4, 5]
                        northwest_115 = [1]
                        northwest_122 = [1]
                        northwest_120 = [1]
                        northwest_341 = [3, 4, 5]
                        northwest_113 = [3]
                        northwest_119 = [7]
                        northwest_408 = [7]
                        northwest_499 = [2, 3]
                        northwest_501 = [1]
                        northwest_440 = [1]
                        northwest_497 = [0, 1]

                        northeast_110 = [0, 1, 2]

                        south_109 = [0, 1, 2]
                        south_115 = [0]
                        south_122 = [0]
                        south_120 = [0]
                        south_119 = [6]
                        south_408 = [6]
                        south_499 = [1, 4]
                        south_501 = [0]
                        south_440 = [0]

                        if len(total_shift) > 1:
                            for npc in south_109:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(109, npc_queue, 3670, 0x20EAFB)
                            for npc in south_115:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                            for npc in south_122:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                            for npc in south_120:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                            for npc in south_499:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                            for npc in south_501:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                            for npc in south_440:
                                npc_queue = [0x14 + npc, len(total_shift)]
                                npc_queue.extend(total_shift)
                                new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                            for npc in northwest_109:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(109, npc_queue, 3670, 0x20EAFB)
                            for npc in northwest_115:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(115, npc_queue, 3730, 0x20EB31)
                            for npc in northwest_122:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(122, npc_queue, 3726, 0x20EBAE)
                            for npc in northwest_120:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(120, npc_queue, 3729, 0x20EB79)
                            for npc in northeast_110:
                                npc_queue = [0x14 + npc, len(total_opposite_dodo_shift)]
                                npc_queue.extend(total_opposite_dodo_shift)
                                new_preloader_event(110, npc_queue, 2112, 0x20EB0A)
                            for npc in northwest_341:
                                npc_queue = [0x14 + npc, len(total_opposite_dodo_shift)]
                                npc_queue.extend(total_opposite_dodo_shift)
                                new_preloader_event(341, npc_queue, 737, 0x20F595)
                            for npc in northwest_113:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(113, npc_queue, 15, 0x20EB1F)
                            for npc in northwest_499:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(499, npc_queue, 3762, 0x20FDA2)
                            for npc in northwest_501:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(501, npc_queue, 15, 0x20FDA8)
                            for npc in northwest_440:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(440, npc_queue, 3740, 0x20FA73)
                            for npc in northwest_497:
                                npc_queue = [0x14 + npc, len(total_opposite_shift)]
                                npc_queue.extend(total_opposite_shift)
                                new_preloader_event(497, npc_queue, 15, 0x20FD96)
                    direction = 0x77
                    if len(total_opposite_dodo_shift) == 3:  # overwrite 9Bs in dodo events if necessary
                        long_dodo_shift = total_opposite_dodo_shift.copy();
                        short_dodo_shift = total_opposite_dodo_shift.copy();
                        long_dodo_shift.extend([0x9b, 0x9b, 0x9B, direction])
                        short_dodo_shift.extend([0x9B, direction])
                        patch.add_data(0x1F765A, short_dodo_shift)
                        patch.add_data(0x1F7661, short_dodo_shift)
                        patch.add_data(0x1F7668, short_dodo_shift)
                        patch.add_data(0x20903E, short_dodo_shift)
                        patch.add_data(0x209045, short_dodo_shift)
                        patch.add_data(0x20904C, short_dodo_shift)
                        patch.add_data(0x1F76A4, long_dodo_shift)
                        patch.add_data(0x1F76AD, long_dodo_shift)
                        patch.add_data(0x1F76B6, long_dodo_shift)
                    else:
                        patch.add_data(0x1F76A4, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                        patch.add_data(0x1F76AD, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                        patch.add_data(0x1F76B6, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9B, direction])
                        patch.add_data(0x1F765A, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                        patch.add_data(0x1F7661, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                        patch.add_data(0x1F7668, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                        patch.add_data(0x20903E, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                        patch.add_data(0x209045, [0x9b, 0x9b, 0x9b, 0x9b, direction])
                        patch.add_data(0x20904C, [0x9b, 0x9b, 0x9b, 0x9b, direction])

                # dont change statues back to king nimbus after castle finished, since doesnt exist in changed mold
                # always doing this, bc using those action scripts for scarecrow
                # entrance hall
                for addr in [0x209f9b, 0x209f9f, 0x209fa3, 0x209fa7, 0x209fab, 0x209faf]:
                    patch.add_data(addr, [0x9b, 0x9b, 0x9b, 0x9b])
                for addr in [0x209056, 0x209061, 0x20906C]:
                    patch.add_data(addr, [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])

            if location.name == "CzarDragon":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "CzarDragon":
                    if shuffled_boss.name in ["Culex", "Birdo", "Johnny"]:
                        remove_shadows(352, 9, 3330, 0x20F608)
                    # for added hilarity, use npc 155 to summon other sprites instead of sparky
                    if fat_sidekicks and shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director",
                                                                "Mack", "Bowyer", "Punchinello", "Johnny", "Megasmilax",
                                                                "CzarDragon", "Birdo", "Valentina", "Hidon",
                                                                "Yaridovich", "Croco1", "Croco2"]:
                        patch.add_data(0x14cFB8, 0x1C)
                    elif empty_sidekicks and shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director",
                                                                    "Mack", "Bowyer", "Punchinello", "Johnny",
                                                                    "Megasmilax", "CzarDragon", "Birdo", "Valentina",
                                                                    "Hidon", "Yaridovich", "Croco1", "Croco2"]:
                        patch.add_data(0x14cFB8, 0x72)
                        patch.add_data(0x1DBDE9, [0x29, 0x80, 0x80])
                    if shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director", "Mack", "Bowyer",
                                              "Punchinello", "Johnny", "Megasmilax", "CzarDragon", "Birdo", "Valentina",
                                              "Hidon", "Yaridovich", "Croco1", "Croco2"]:
                        patch.add_data(0x14cfd4, [0x6f, 0x82])
                        if len(shuffled_boss.czar_sprite) > 0:
                            patch.add_data(0x1dbc3d, calcpointer(shuffled_boss.czar_sprite[0], [0x00, 0x08]))
                        else:
                            patch.add_data(0x1dbc3d, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x08]))
                        patch.add_data(0x1dbc3f, [0x80, 0x23, 0x55, 0x2b])
                    #patch.add_data(0x1dbde8, calcpointer(sprite, [0x00, 0x68]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x68]), shadow, solidity, y_shift, location))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(1, plus, mold, sub_sequence, sequence, False, 352, 3330, 0x20f608))

            if location.name == "AxemRangers":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "AxemRangers":
                    # change partitions for small sprites
                    if shuffled_boss.name == "Exor":
                        # trampoline room
                        # use and modify partition 3
                        patch.add_data(0x14d761, 0x03)
                        patch.add_data(0x1dde0c, [0xA0, 0x87, 0x87, 0x87])
                    elif shuffled_boss.name == "Cloaker":
                        # use and modify partition 3
                        patch.add_data(0x14d761, 0x03)
                        patch.add_data(0x1dde0c, [0xA0, 0x80, 0x87, 0x87])
                    elif shuffled_boss.name in ["Bundt"]:  # big boss, skinny sidekicks
                        # use partition 6
                        patch.add_data(0x14d761, 0x06)
                    elif overworld_is_empty or shuffled_boss.name in ["KnifeGuy", "Clerk", "Manager", "Director", "Gunyolk"]:
                        # use partition 32
                        patch.add_data(0x14d761, 0x20)
                    elif overworld_is_skinny:
                        # use and modify partition 3
                        patch.add_data(0x14d761, 0x03)
                        # may need to make partition data different depending on underling sprites
                        # ie bowyer arrows may also need slot C modified
                        if fat_sidekicks:
                            patch.add_data(0x1dde0c, [0xA0, 0x87, 0x81]);
                        else:
                            patch.add_data(0x1dde0c, [0xA0, 0x81, 0x81]);
                    elif not overworld_is_skinny:
                        patch.add_data(0x14d761, 0x03)
                        if len(shuffled_boss.other_sprites) > 0 and not fat_sidekicks:
                            patch.add_data(0x1dde0e, 0x81);
                    if shuffled_boss.name in ["Culex"]:
                        remove_shadows(394, 3, 3342, 0x20F8A5)
                    # axem red
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1dbdb0, calcpointer(sprite, [0x00, 0x08]))
                    if shuffled_boss.name == "CountDown":
                        patch.add_data(0x1dbdb1, [0x29, 0x80, 0x80])
                    if freeze or sequence > 0 or mold > 0:  # never change directions
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if shuffled_boss.name != "Culex":
                        if len(shuffled_boss.other_sprites) < 1:
                            # dont show axem green
                            # room 4
                            patch.add_data(0x20496d,
                                           [0xD9, 0xF4, 0x87, 0x49, 0xA1, 0xF4, 0x15, 0x05, 0x01, 0xFD, 0xF2, 0x57,
                                            0x02, 0x14, 0x07, 0x01, 0xFD, 0xF2, 0x08, 0x40, 0x81, 0x47, 0xD1, 0x0F,
                                            0x00, 0xFE, 0xD0, 0x0F, 0x00])
                            # visibility, for some reason this doesnt do anything, why is this game so dumb
                            patch.add_data(0x14d729,
                                           [0x0C, 0x2D, 0x60, 0x00, 0x40, 0x04, 0x43, 0x33, 0xC0, 0x00, 0x01, 0x04,
                                            0x0C, 0x2F, 0x20, 0x15, 0x00, 0x41, 0x00, 0x4B, 0xF1, 0xC0, 0xFD, 0x00])
                            patch.add_data(0x14d752, 0x12)
                            # room 6 visibility
                            patch.add_data(0x2049b4, [0x9b, 0x9b, 0x9b, 0x9b])
                            # trampoline
                            patch.add_data(0x204a39,
                                           [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b])
                        if len(shuffled_boss.other_sprites) < 2:
                            # dont show axem yellow
                            # visibility, for some reason this doesnt do anything, why is this game so dumb
                            patch.add_data(0x14d756, 0x12)
                            # room 6 visibility
                            patch.add_data(0x2049bb, [0x9b, 0x9b, 0x9b, 0x9b])
                            patch.add_data(0x204a6a,
                                           [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b])
                        if len(shuffled_boss.other_sprites) < 3:
                            # dont show axem pink
                            # room 5 visibility
                            new_preloader_event(394, [0xF2, 0x8A, 0x2D, 0x16, 0xF9], 3342, 0x20f8a5)
                            # room 6 visibility
                            patch.add_data(0x2049c2, [0x9b, 0x9b, 0x9b, 0x9b])
                            # trampoline
                            patch.add_data(0x204a9b,
                                           [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b])
                        if len(shuffled_boss.other_sprites) < 4:
                            # dont show axem black
                            # room 5 visibility
                            new_preloader_event(394, [0xF2, 0x8A, 0x2B, 0x15, 0xF9], 3342, 0x20f8a5)
                            # room 6 visibility
                            patch.add_data(0x2049c9, [0x9b, 0x9b, 0x9b, 0x9b])
                            # trampoline
                            patch.add_data(0x204acc,
                                           [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                            0x9b])
                        # trampoline bounces
                        patch.add_data(0x204aff, [0xD4, min(len(shuffled_boss.other_sprites), 4)])
                        # load sprites from whatever boss is there
                        if len(shuffled_boss.other_sprites) >= 1:
                            patch.add_data(0x1dbdcc, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x08]))
                        if len(shuffled_boss.other_sprites) >= 2:
                            patch.add_data(0x1dbdc5, calcpointer(shuffled_boss.other_sprites[1], [0x00, 0x08]))
                        if len(shuffled_boss.other_sprites) >= 3:
                            patch.add_data(0x1dbdbe, calcpointer(shuffled_boss.other_sprites[2], [0x00, 0x08]))
                        if len(shuffled_boss.other_sprites) >= 4:
                            patch.add_data(0x1dbdb7, calcpointer(shuffled_boss.other_sprites[3], [0x00, 0x08]))
                            if sequence > 0 or mold > 0:
                                if sequence > 0:
                                    sub_sequence = True
                                elif mold > 0:
                                    sub_sequence = False
                        bytesFor629 = [0xF2, 0x88, 0x2B, 0xF2, 0x88, 0x2D, 0xF2, 0x88, 0x2F, 0xF2, 0x88, 0x31, 0xF2, 0x88, 0x33]
                        if len(shuffled_boss.other_sprites) < 4:
                            bytesFor629.extend([0xF2, 0x89, 0x35, 0x1a, 0xf9])
                            if len(shuffled_boss.other_sprites) < 3:
                                bytesFor629.extend([0xF2, 0x89, 0x33, 0x19, 0xf9])
                                if len(shuffled_boss.other_sprites) < 2:
                                    bytesFor629.extend([0xF2, 0x89, 0x31, 0x18, 0xf9])
                                    if len(shuffled_boss.other_sprites) < 1:
                                        bytesFor629.extend([0xF2, 0x89, 0x2f, 0x17, 0xf9])
                        bytesFor629.append(0xD0)
                        bytesFor629.extend(calcpointer(3344))
                        bytesFor629.append(0xFE)
                        patch.add_data(0x1E7CCE, bytesFor629)
                        spritePhaseEvents.append(
                                    SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, False, 393, 629, 0x20f8a2))
                        if sequence > 0 or mold > 0:
                            if sequence > 0:
                                sub_sequence = True
                            elif mold > 0:
                                sub_sequence = False
                            spritePhaseEvents.append(
                                SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, True, 357, 3332, 0x20f63b))
                            spritePhaseEvents.append(
                                SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, False, 388, 3339, 0x20f88d))
                            spritePhaseEvents.append(
                                SpritePhaseEvent(3, plus, mold, sub_sequence, sequence, True, 394, 3342, 0x20f8a5))
                            spritePhaseEvents.append(
                                SpritePhaseEvent(1, plus, mold, sub_sequence, sequence, False, 392, 15, 0x20f899))
                    # culex needs special rules
                    else:
                        allies = shuffled_boss.other_sprites.copy()
                        ally_sprites = shuffled_boss.other_sprites_sequences.copy()
                        patch.add_data(0x1dbdcc, calcpointer(allies[0], [0x00, 0x08]))
                        patch.add_data(0x1dbdc5, calcpointer(allies[1], [0x00, 0x08]))
                        patch.add_data(0x1dbdbe, calcpointer(allies[2], [0x00, 0x08]))
                        patch.add_data(0x1dbdb7, calcpointer(allies[3], [0x00, 0x08]))
                        spritePhaseEvents.append(SpritePhaseEvent([2, 3, 4, 5, 6], 0, 0, True,
                                                                  [sequence, ally_sprites[0], ally_sprites[1],
                                                                   ally_sprites[2], ally_sprites[3]],
                                                                  [True, True, True, True, True], 357, 3332, 0x20f63b))
                        spritePhaseEvents.append(SpritePhaseEvent([2, 3, 4, 5, 6], 0, 0, True,
                                                                  [sequence, ally_sprites[0], ally_sprites[1],
                                                                   ally_sprites[2], ally_sprites[3]],
                                                                  [True, True, True, False, False], 388, 3339,
                                                                  0x20f88d))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(1, 0, 0, True, ally_sprites[2], True, 365, 15, 0x20f653))
                        spritePhaseEvents.append(
                            SpritePhaseEvent(1, 0, 0, True, ally_sprites[0], True, 391, 3341, 0x20f896))
                        spritePhaseEvents.append(
                            SpritePhaseEvent([1, 2, 3], 0, 0, True, [ally_sprites[3], ally_sprites[3], sequence],
                                             [True, False, True], 394, 3342, 0x20f8a5))
                        spritePhaseEvents.append(SpritePhaseEvent([1, 2, 3, 4, 5], 0, 0, True,
                                                                  [sequence, ally_sprites[0], ally_sprites[1],
                                                                   ally_sprites[2], ally_sprites[3]],
                                                                  [False, False, False, False, False], 392, 15,
                                                                  0x20f899))
                        spritePhaseEvents.append(SpritePhaseEvent([2, 3, 4, 5, 6], 0, 0, True,
                                                                  [sequence, ally_sprites[0], ally_sprites[1],
                                                                   ally_sprites[2], ally_sprites[3]],
                                                                  [False, False, False, False, False], 393, 3344,
                                                                  0x20f8a2))

            if location.name == "Magikoopa":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Magikoopa":
                    if shuffled_boss.name == "Booster":
                        #patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(502, [0x00, 0x40]), shadow, solidity, y_shift, location))
                        patch.add_data(0x1dbd32, calcpointer(502, [0x00, 0x40]))
                    elif shuffled_boss.name in ["Croco1", "Croco2"]:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(496, [0x00, 0x40]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1dbd32, calcpointer(496, [0x00, 0x40]))
                    elif freeze or sesw_only:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x48]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1dbd32, calcpointer(sprite, [0x00, 0x48]))
                    else:
                        patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x40]), shadow, solidity, y_shift, location))
                        #patch.add_data(0x1dbd32, calcpointer(sprite, [0x00, 0x40]))
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    if invert_se_sw or freeze:  # change north-south cardinality on everything
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x19, 0x65])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append(
                            [0xFD, 0x9E, 0x2C, 0xD4, 0x01, 0x00, 0xF0, 0x01, 0x01, 0xF0, 0x03, 0xD7, 0xD4, 0x01, 0x00,
                             0xF0, 0x01, 0x01, 0xF0, 0x01, 0xD7, 0xD4, 0x01, 0x00, 0xF0, 0x00, 0x01, 0xF0, 0x00, 0xD7,
                             0x00])
                        add_scarecrow_script(2, scarecrow_script, 0x1f8817, False)
                        scarecrow_script = []
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0xF0, 0x3B])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x03])
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        scarecrow_script.append([0xF0, 0x0E])
                        add_scarecrow_script(2, scarecrow_script, 0x1f8859, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x9b])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x04])
                        add_scarecrow_script(2, scarecrow_script, 0x1f88c8, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x10, 0xc1])
                        scarecrow_script.append(get_directional_command(plus, northwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x55, 0x03])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x10, 0x80, 0x04])
                        add_scarecrow_script(2, scarecrow_script, 0x1f88cd, False)
                        scarecrow_script = []
                        scarecrow_script.append([0x82, 0x18, 0x62, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southeast, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x04])
                        add_scarecrow_script(2, scarecrow_script, 0x1f87fb, True)
                        # battle doors
                        patch.add_data(0x21B929, 0x9B)
                        patch.add_data(0x21B929, 0x9B)
                        patch.add_data(0x21B94B, [0x9b, 0x9b, 0x9b])
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x08, 0x36, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1F845C, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8622, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7D35, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7EF9, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F80BF, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8296, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x0C, 0x2E, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1F84CD, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8698, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7DA4, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7F6A, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F812E, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8307, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x10, 0x26, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1F853E, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8709, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7E15, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7FDB, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F81A2, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8378, True)
                        scarecrow_script = []
                        scarecrow_script.append([0x92, 0x14, 0x1E, 0x00])
                        scarecrow_script.append(get_directional_command(plus, southwest, True, sequence, is_scarecrow))
                        scarecrow_script.append([0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1F85AF, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F877D, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F7E86, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F804C, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F8213, True)
                        add_scarecrow_script(0, scarecrow_script, 0x1F83E9, True)
                    # special animations
                    if shuffled_boss.name == "Booster":
                        patch.add_data(0x1f8842, [0x08, 0x50, 3])
                        patch.add_data(0x21B94B, [0x08, 0x50, 3])
                        patch.add_data(0x1f885e, [0x08, 0x50, 0x80 + 2])
                    elif shuffled_boss.name in ["Croco1", "Croco2"]:
                        patch.add_data(0x1f8842, [0x9b, 0x9b, 0x9b])
                        patch.add_data(0x21B94B, [0x08, 0x50, 4])
                        patch.add_data(0x1f885e, [0x08, 0x50, 0x80 + 4])
                        patch.add_data(0x1f887F, [0xF0, 0x9F])
                    elif not freeze and not invert_se_sw:
                        if push_sequence != False:
                            patch.add_data(0x1f8842, [0x08, 0x50, push_sequence])
                        else:
                            patch.add_data(0x1f8842, [0x9b, 0x9b, 0x9b])
                        if extra_sequence != False and shuffled_boss.name != "Jagger":
                            patch.add_data(0x1f885e, [0x08, 0x50, 0x80 + extra_sequence])
                        elif push_sequence != False:
                            patch.add_data(0x1f885e, [0x08, 0x50, 0x80 + push_sequence])
                        else:
                            patch.add_data(0x1f885e, [0x9b, 0x9b, 0x9b])
                        # battle doors
                        if push_sequence != False:
                            patch.add_data(0x21B94B, [0x08, 0x50, push_sequence])
                        elif extra_sequence != False and shuffled_boss.name != "Jagger":
                            patch.add_data(0x21B94B, [0x08, 0x50, extra_sequence])
                        else:
                            patch.add_data(0x21B94B, [0x9b, 0x9b, 0x9b])
                    else:
                        patch.add_data(0x1f8842, [0x9b, 0x9b, 0x9b])
                        patch.add_data(0x1f885e, [0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1f8861,
                                   [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                    0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                    0x9b, 0x9b])
                    patch.add_data(0x1f8881,
                                   [0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                    0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b,
                                    0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1f8855, [0x9b, 0x9b, 0x9b, 0x9b])
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(2, plus, mold, sub_sequence, sequence, False, 266, 2208, 0x20F2Da))

            if location.name == "Boomer":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Boomer":
                    if freeze or sequence > 0 or mold > 0:  # never change directions
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x68]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1dc52e, calcpointer(sprite, [0x00, 0x68]))
                    # special animations
                    if not freeze:
                        if push_sequence != False:
                            patch.add_data(0x1f8a34, [0x08, 0x50, push_sequence])
                        elif extra_sequence != False:
                            patch.add_data(0x1f8a34, [0x08, 0x40, extra_sequence])
                        elif sequence > 0 or mold > 0:
                            # needed for exor
                            patch.add_data(0x1f8a34, [0x9b, 0x9b, 0x9b])
                        else:
                            patch.add_data(0x1f8a34, [0x08, 0x40, sequence])
                    else:
                        patch.add_data(0x1f8a34, [0x9b, 0x9b, 0x9b])
                        patch.add_data(0x1f8a34, [0x9b, 0x9b, 0x9b])
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 400, 2224, 0x20F8e1))

            if location.name == "Countdown":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "CountDown":
                    if freeze or invert_se_sw:
                        scarecrow_script = []
                        scarecrow_script.append([0xFD, 0x0F, 0x03, 0x66, 0x04, 0x65, 0x01])
                        scarecrow_script.append(get_directional_command(plus, southwest, False, sequence, is_scarecrow))
                        scarecrow_script.append([0x9B, 0x9B, 0x9B])
                        add_scarecrow_script(0, scarecrow_script, 0x1FA828, True)
                    if freeze or sequence > 0 or mold > 0:
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1dc463, calcpointer(sprite, [0x00, 0x28]))
                    if shuffled_boss.name in ["Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2", "Mack",
                                              "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon", "Birdo",
                                              "Valentina", "Hidon", "Yaridovich"]:
                        if len(shuffled_boss.czar_sprite) > 0:
                            patch.add_data(0x1dc46A, calcpointer(shuffled_boss.czar_sprite[0], [0x00, 0x28]))
                        else:
                            patch.add_data(0x1dc46A, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x28]))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(0, plus, mold, sub_sequence, sequence, False, 223, 2363, 0x20F145))

            if location.name == "Clerk":
                #print(location.name + ": " + shuffled_boss.name)
                # fix cannon action scripts
                if shuffled_boss.name != "Clerk":
                    if fat_sidekicks and shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director",
                                                                "Croco1", "Croco2", "Mack", "Bowyer", "Punchinello",
                                                                "Johnny", "Megasmilax", "CzarDragon", "Birdo",
                                                                "Valentina", "Hidon", "Yaridovich"]:
                        # reconfigure and use partition 4
                        #this might need to be 14E79A
                        patch.add_data(0x14E798, 0x04)
                        patch.add_data(0x1DDE10, [0xA0, 0x87, 0x81, 0x80])
                    elif shuffled_boss.name == "Birdo":
                        # use partition 32
                        patch.add_data(0x14E798, 0x20)
                    # change sequence 01 of Clerk, wherever he is, if not vanilla, to be his NW facing sprite, to make animations work
                    if freeze or sequence > 0 or mold > 0:
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x08]), shadow, solidity, y_shift, location))
                    #patch.add_data(0x1dc55f, calcpointer(sprite, [0x00, 0x08]))
                    if shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2",
                                              "Mack", "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1dbf15, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x00]))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(9, plus, mold, sub_sequence, sequence, True, 469, 2605, 0x20Fc24))
                    patch.add_data(0x1fe34f, [0x9b, 0x9b, 0x9b])

            if location.name == "Manager":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Manager":
                    if freeze or sequence > 0 or mold > 0:  # never change directions
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    #patch.add_data(0x1dc57b, calcpointer(sprite, [0x00, 0x28]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    if shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2",
                                              "Mack", "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1dc0d5, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x00]))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(16, plus, mold, sub_sequence, sequence, True, 471, 2617, 0x20Fc3c))
                    patch.add_data(0x1fe69c, [0x9b, 0x9b, 0x9b])

            if location.name == "Director":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Director":
                    if shuffled_boss.name == "Mack":
                        # change animation of background guys
                        patch.add_data(0x21b3cc, 0x04)
                        patch.add_data(0x21b3e6, 0x04)
                        patch.add_data(0x21b400, 0x04)
                    if freeze or sequence > 0 or mold > 0:  # never change directions
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    #patch.add_data(0x1dc597, calcpointer(sprite, [0x00, 0x28]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x28]), shadow, solidity, y_shift, location))
                    if shuffled_boss.name in ["Booster", "Bundt", "Clerk", "Manager", "Director", "Croco1", "Croco2",
                                              "Mack", "Bowyer", "Punchinello", "Johnny", "Megasmilax", "CzarDragon",
                                              "Birdo", "Valentina", "Hidon", "Yaridovich"]:
                        patch.add_data(0x1dc50b, calcpointer(shuffled_boss.other_sprites[0], [0x00, 0x20]))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(10, plus, mold, sub_sequence, sequence, True, 472, 2621, 0x20Fc51))
                    patch.add_data(0x1fe92e, [0x9b, 0x9b, 0x9b])

            if location.name == "Gunyolk":
                #print(location.name + ": " + shuffled_boss.name)
                if shuffled_boss.name != "Gunyolk":
                    if freeze or sequence > 0 or mold > 0:  # never change directions
                        sub_sequence = True
                    if sequence == 0 and mold > 0:
                        sub_sequence = False
                    #patch.add_data(0x1dc53c, calcpointer(sprite, [0x00, 0x00]))
                    patch.add_data(location.sprite_offset, rewrite_npc(calcpointer(sprite, [0x00, 0x00]), shadow, solidity, y_shift, location))
                    # preload if needed
                    if sequence > 0 or mold > 0:
                        if sequence > 0:
                            sub_sequence = True
                        elif mold > 0:
                            sub_sequence = False
                        spritePhaseEvents.append(
                            SpritePhaseEvent(13, plus, mold, sub_sequence, sequence, True, 470, 2601, 0x20Fc2d))
                    patch.add_data(0x14e839, 0x20)
                    patch.add_data(0x1fe1bd, [0x01, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1c4, [0x01, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1cb, [0x01, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1d2, [0x01, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1d9, [0x01, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1e4, [0x01, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])
                    patch.add_data(0x1fe1ed, [0x01, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b, 0x9b])

    # set sprite molds and sequences where necessary
    if len(preloaded_events) > 0:
        patch.add_data(0x1ec43d, 0xC3)
        start_instructions = 0x1ec43e
        shortened_start_instructions = 0xc43e
        append_jumps = []
        total_jump_length = len(preloaded_events) * 5
        current_length_of_npc_code = 0
        for room, script in preloaded_events.items():
            patch.add_data(script.original_event, calcpointer(1110))
            append_jumps.append(0xe2)
            append_jumps.extend(calcpointer(room))
            append_jumps.extend(
                calcpointer(shortened_start_instructions + total_jump_length + current_length_of_npc_code))
            full_instructions = []
            for action in script.actions:
                full_instructions.extend(action)
            full_instructions.extend(script.event_jump)
            current_length_of_npc_code += len(full_instructions)
        for room, script in preloaded_events.items():
            full_instructions = []
            for action in script.actions:
                full_instructions.extend(action)
            full_instructions.extend(script.event_jump)
            append_jumps.extend(full_instructions)
        patch.add_data(start_instructions, append_jumps)
        if len(append_jumps) > 1312:
            raise flags.FlagError("B flag error: Event 1110 cannot contain all the necessary preloaders! Please tell the devs about this. Paste your flag string and the seed value " + world.seed)
            #print( 'preloaders too long: ', len(append_jumps), world.boss_locations )
    # set dojo partition
    if jinx_size > 0:
        # use and modify partition 5
        patch.add_data(0x14BE59, 0x05)
        if jinx_size == 3:
            patch.add_data(0x1dde14, [0xB1, 0x87, 0x87, 0x87])
        else:
            patch.add_data(0x1dde14, [0xC0, 0x81, 0x87, 0x87])

    return patch
