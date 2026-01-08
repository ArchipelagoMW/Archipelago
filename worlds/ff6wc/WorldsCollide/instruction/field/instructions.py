from ...data import event_bit as event_bit

from ...instruction.event import _Instruction, _Branch, _LoadMap, EVENT_CODE_START
from enum import IntEnum, IntFlag
from ... import data

class NOP(_Instruction):
    def __init__(self):
        super().__init__(0xfd)

class Return(_Instruction):
    def __init__(self):
        super().__init__(0xfe)

class End(_Instruction):
    def __init__(self):
        super().__init__(0xff)

class Call(_Instruction):
    def __init__(self, address):
        self.address = address - EVENT_CODE_START
        super().__init__(0xb2, self.address.to_bytes(3, "little"))

    def __str__(self):
        return super().__str__(hex(self.address))

class MultipleCalls(_Instruction):
    def __init__(self, times, address):
        self.address = address - EVENT_CODE_START
        super().__init__(0xb3, times, self.address.to_bytes(3, "little"))

    def __str__(self):
        return super().__str__(hex(self.address))

class SelectParties(_Instruction):
    def __init__(self, count, unmovable_characters = 0x0000):
        super().__init__(0x99, count, unmovable_characters.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(self.args[0])

class AddCharacterToParty(_Instruction):
    def __init__(self, character, party):
        super().__init__(0x3f, character, party)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class RemoveCharacterFromParties(_Instruction):
    def __init__(self, character):
        super().__init__(0x3f, character, 0x00)

    def __str__(self):
        return super().__str__(f"{self.args[0]}")

def RecruitAndSelectParty(character):
    from ...instruction.field.custom import RecruitCharacter
    from ...instruction.field.functions import REFRESH_CHARACTERS_AND_SELECT_PARTY
    return RecruitCharacter(character), Call(REFRESH_CHARACTERS_AND_SELECT_PARTY)

def RecruitAndSelectParty2(character):
    from ...instruction.field.custom import RecruitCharacter2
    from ...instruction.field.functions import REFRESH_CHARACTERS_AND_SELECT_PARTY
    return RecruitCharacter2(character), Call(REFRESH_CHARACTERS_AND_SELECT_PARTY)

class SetParty(_Instruction):
    def __init__(self, party):
        super().__init__(0x46, party)

    def __str__(self):
        return super().__str__(self.args[0])

class SetPartyMap(_Instruction):
    def __init__(self, party, map_id):
        super().__init__(0x79, party, map_id.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(f"{self.args[0]} {hex(self.args[1])}")

class UpdatePartyLeader(_Instruction):
    def __init__(self):
        super().__init__(0x47)

class ShakeScreen(_Instruction):
    def __init__(self, intensity, permanent, layer1, layer2, layer3, sprite_layer):
        if intensity == 1:
            options_byte = 0x01
        elif intensity == 2:
            options_byte = 0x02
        elif intensity == 3:
            options_byte = 0x03

        if permanent: # shake screen until stopped
            options_byte |= 0x04

        if layer1:
            options_byte |= 0x10
        if layer2:
            options_byte |= 0x20
        if layer3:
            options_byte |= 0x40
        if sprite_layer:
            options_byte |= 0x80

        super().__init__(0x58, options_byte)

    def __str__(self):
        return super().__str__(self.args[0])

class StopScreenShake(_Instruction):
    def __init__(self):
        # uses same opcode as shake screen, with option_byte 0x00
        super().__init__(0x58, 0x00)

class _AddItem(_Instruction):
    def __init__(self, item):
        if isinstance(item, str):
            from ...data.item_names import name_id
            self.item = name_id[item]
            self.item_name = item
        else:
            from ...data.item_names import id_name
            self.item = item
            self.item_name = id_name[item]

        super().__init__(0x80, self.item)

    def __str__(self):
        return super().__str__(f"'{self.item_name}'")

def AddItem(item, sound_effect = True):
    AddItem = type("AddItem", (_AddItem,), {})
    if sound_effect:
        return AddItem(item), PlaySoundEffect(141)
    else:
        return AddItem(item)

class AddGP(_Instruction):
    MAX = 2 ** 16 - 1 # 2 bytes max value
    def __init__(self, amount):
        self.amount = amount
        super().__init__(0x84, amount.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(self.amount)

class RemoveGP(_Instruction):
    # NOTE: if not enough gp, event bit 0x1be is set and no gp is removed
    MAX = 2 ** 16 - 1 # 2 bytes max value
    def __init__(self, amount):
        self.amount = amount
        super().__init__(0x85, amount.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(self.amount)

class _AddEsper(_Instruction):
    def __init__(self, esper_id):
        self.esper_id = esper_id
        super().__init__(0x86, esper_id + 0x36)

    def __str__(self):
        return super().__str__(self.esper_id)

def AddEsper(esper_id, sound_effect = True):
    AddEsper = type("AddEsper", (_AddEsper,), {})
    if sound_effect:
        return AddEsper(esper_id), PlaySoundEffect(141)
    else:
        return AddEsper(esper_id)

class _AddEsper2(_Instruction):
    def __init__(self):
        super().__init__(0xa3)

    def __str__(self):
        return super().__str__()

def AddEsper2(esper_id, sound_effect = True):
    AddEsper = type("AddEsper", (_AddEsper2,), {})
    if sound_effect:
        return AddEsper(), PlaySoundEffect(0xCD)
    else:
        return AddEsper()

class RemoveEsper(_Instruction):
    def __init__(self, esper_id):
        self.esper_id = esper_id
        super().__init__(0x87, esper_id + 0x36)

    def __str__(self):
        return super().__str__(self.esper_id)

class Status(IntEnum):
    DOG_BLOCK   = 0x0040
    FLOAT       = 0x0080
    DARKNESS    = 0x0100
    ZOMBIE      = 0x0200
    POISON      = 0x0400
    MAGITEK     = 0x0800
    VANISH      = 0x1000
    IMP         = 0x2000
    PETRIFY     = 0x4000
    DEATH       = 0x8000

class RemoveStatusEffects(_Instruction):
    def __init__(self, character, status_effects):
        status_effects = 0xffff - status_effects # command 0x88 is really remove all status effects EXCEPT given
        self.status_effects = status_effects
        super().__init__(0x88, character, (status_effects & 0xff00) >> 8, status_effects & 0xff)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {hex(self.status_effects)}")

class AddStatusEffects(_Instruction):
    def __init__(self, character, status_effects):
        self.status_effects = status_effects
        super().__init__(0x89, character, (status_effects & 0xff00) >> 8, status_effects & 0xff)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {hex(self.status_effects)}")

class ToggleStatusEffects(_Instruction):
    def __init__(self, character, status_effects):
        self.status_effects = status_effects
        super().__init__(0x8a, character, (status_effects & 0xff00) >> 8, status_effects & 0xff)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {hex(self.status_effects)}")

class RemoveAllEquipment(_Instruction):
    def __init__(self, character):
        self.character = character
        super().__init__(0x8d, character)

    def __str__(self):
        return super().__str__(self.character)

class Dialog(_Instruction):
    def __init__(self, dialog_id, wait_for_input = True, inside_text_box = True, top_of_screen = True):
        self.dialog_id = dialog_id

        if wait_for_input:
            opcode = 0x4b
        else:
            opcode = 0x48

        if not inside_text_box and top_of_screen:
            dialog_arg = dialog_id | 0x4000
        elif inside_text_box and not top_of_screen:
            dialog_arg = dialog_id | 0x8000
        elif not inside_text_box and not top_of_screen:
            dialog_arg = dialog_id | 0xc000
        else:
            dialog_arg = dialog_id

        super().__init__(opcode, dialog_arg.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(self.dialog_id)

class _DialogBranch(_Branch):
    def __init__(self, dest1, dest2, dest3, dest4, dest5, dest6):

        args = [dest1]
        if dest2 is not None:
            args.append(dest2)
        if dest3 is not None:
            args.append(dest3)
        if dest4 is not None:
            args.append(dest4)
        if dest5 is not None:
            args.append(dest5)
        if dest6 is not None:
            args.append(dest6)

        super().__init__(0xb6, [], *args)

def DialogBranch(dialog_id, dest1, dest2 = None, dest3 = None, dest4 = None, dest5 = None, dest6 = None,
                 wait_for_input = True, inside_text_box = True, top_of_screen = True):

    dialog = Dialog(dialog_id, wait_for_input, inside_text_box, top_of_screen)

    DialogBranch = type("DialogBranch", (_DialogBranch,), {})
    dialog_branch = DialogBranch(dest1, dest2, dest3, dest4, dest5, dest6)

    return dialog, dialog_branch, Return() # dialog branch always followed by a return to know how many options

class SetName(_Instruction):
    def __init__(self, character, name_index):
        # name_index = index of rom character name data
        super().__init__(0x7f, character, name_index)

    def __str__(self):
        return super().__str__(self.args[0])

class SetProperties(_Instruction):
    def __init__(self, character, data_index):
        # data_index = index of init hp/mp/commands/stats/equip/relics/...
        super().__init__(0x40, character, data_index)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class SetSprite(_Instruction):
    def __init__(self, entity, sprite):
        super().__init__(0x37, entity, sprite)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class SetPalette(_Instruction):
    def __init__(self, entity, palette):
        super().__init__(0x43, entity, palette)

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class CreateEntity(_Instruction):
    def __init__(self, entity):
        super().__init__(0x3d, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class DeleteEntity(_Instruction):
    def __init__(self, entity):
        super().__init__(0x3e, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class ShowEntity(_Instruction):
    def __init__(self, entity):
        super().__init__(0x41, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class HideEntity(_Instruction):
    def __init__(self, entity):
        super().__init__(0x42, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class Vehicle(IntEnum):
    NONE                = 0x00
    CHOCOBO             = 0x20
    MAGITEK             = 0x40
    RAFT                = 0x60
    CHOCOBO_AND_RIDER   = 0xa0
    MAGITEK_AND_RIDER   = 0xc0
    RAFT_AND_RIDER      = 0xe0
class SetVehicle(_Instruction):
    def __init__(self, entity, vehicle):
        super().__init__(0x44, entity, vehicle)

    def __str__(self):
        return super().__str__(f"{self.args[0]}, {self.args[1]}")

class RefreshEntities(_Instruction):
    def __init__(self):
        super().__init__(0x45)

class EnableEntityCollision(_Instruction):
    def __init__(self, entity):
        super().__init__(0x36, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class DisableEntityCollision(_Instruction):
    def __init__(self, entity):
        super().__init__(0x78, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class EnableTouchEvent(_Instruction):
    # entity's event triggered on touch
    def __init__(self, entity):
        super().__init__(0x7c, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class Tint(IntEnum):
    BLUE        = 0x27 # save point flash color
    RED         = 0x33
    WHITE       = 0x3f
    YELLOW      = 0x87 # flashback color
    TURQUOISE   = 0x93
    NIGHT       = 0x9b
    BLACK       = 0x9f
class TintBackground(_Instruction):
    def __init__(self, tint, invert = False):
        self.tint = tint
        self.invert = invert
        if invert:
            tint += 0x40
        super().__init__(0x50, tint)

    def __str__(self):
        substring = f"{self.tint}"
        if self.invert:
            substring += ", Invert"
        return super().__str__(substring)

class TintColorRange(_Instruction):
    def __init__(self, tint, range_start, range_end, invert = False):
        self.tint = tint
        self.invert = invert
        if invert:
            tint += 0x40
        super().__init__(0x53, tint, range_start, range_end)

    def __str__(self):
        substring = f"{self.args[0]}, [{self.args[1]}, {self.args[2]}]"
        if self.invert:
            substring += ", Invert"
        return super().__str__(substring)

def TintSpritePalette(tint, palette, invert = False):
    TintSpritePalette = type("TintSpritePalette", (TintColorRange,), {})
    return TintSpritePalette(tint, palette * 0x10, palette * 0x10 + 0x0f, invert)

class Flash(IntFlag):
    NONE        = 0x00
    RED         = 0x20
    GREEN       = 0x40
    BLUE        = 0x80
    YELLOW      = RED | GREEN,
    WHITE       = RED | GREEN | BLUE
class FlashScreen(_Instruction):
    def __init__(self, color):
        if color != Flash.NONE and (not (color & Flash.RED) and not (color & Flash.GREEN) and not (color & Flash.BLUE)):
            raise ValueError(f"FlashScreen: invalid color {hex(color)}")
        super().__init__(0x55, color)

    def __str__(self):
        return super().__str__(self.args[0])

class HoldScreen(_Instruction):
    def __init__(self):
        super().__init__(0x38)

class FreeScreen(_Instruction):
    def __init__(self):
        super().__init__(0x39),

class FreeMovement(_Instruction):
    def __init__(self):
        super().__init__(0x3a)

class FadeInScreen(_Instruction):
    def __init__(self, speed = None):
        self.speed = speed

        if speed is None:
            super().__init__(0x96)
        else:
            super().__init__(0x59, speed)

    def __str__(self):
        if self.speed is not None:
            return super().__str__(self.speed)
        return super().__str__()

class FadeOutScreen(_Instruction):
    def __init__(self, speed = None):
        self.speed = speed

        if speed is None:
            super().__init__(0x97)
        else:
            super().__init__(0x5a, speed)

    def __str__(self):
        if self.speed is not None:
            return super().__str__(self.speed)
        return super().__str__()

class WaitForFade(_Instruction):
    def __init__(self):
        super().__init__(0x5c)

class Pause(_Instruction):
    def __init__(self, seconds):
        import math
        if math.isclose(seconds, 0.25):         # 15 units
            super().__init__(0x91)
        elif math.isclose(seconds, 0.50):       # 30 units
            super().__init__(0x92)
        elif math.isclose(seconds, 0.75):       # 45 units
            super().__init__(0x93)
        elif math.isclose(seconds, 1.00):       # 60 units
            super().__init__(0x94)
        elif math.isclose(seconds, 1.50):       # 90 units
            super().__init__(0xb5, 6)           # 15 * 6 = 90
        elif math.isclose(seconds, 2.50):       # 150 units
            super().__init__(0xb5, 10)          # 15 * 10 = 150
        elif math.isclose(seconds, 2.00):       # 120 units
            super().__init__(0x95)
        elif math.isclose(seconds, 4.00):       # 240 units
            super().__init__(0xb5, 16)          # 15 * 16 = 240
        else:
            print("pause: invalid seconds")

    def __str__(self):
        substring = ""
        if len(self.args) == 1:
            substring = str(self.args[0])
        return super().__str__(substring)

class PauseUnits(_Instruction):
    def __init__(self, units):
        super().__init__(0xb4, units)

    def __str__(self):
        return super().__str__(self.args[0])

class StartSong(_Instruction):
    def __init__(self, song):
        super().__init__(0xf0, song)

    def __str__(self):
        return super().__str__(self.args[0])

class FadeInSong(_Instruction):
    def __init__(self, song, fade_time):
        super().__init__(0xf1, song, fade_time)

    def __str__(self):
        return super().__str__(f"{self.args[0]}, {self.args[1]}")

class FadeOutSong(_Instruction):
    def __init__(self, fade_time):
        super().__init__(0xf2, fade_time)

    def __str__(self):
        return super().__str__(self.args[0])

class PlaySoundEffect(_Instruction):
    def __init__(self, sound_effect_id):
        self.sound_effect_id = sound_effect_id
        super().__init__(0xf4, sound_effect_id)

    def __str__(self):
        return super().__str__(self.sound_effect_id)

class WaitForSong(_Instruction):
    def __init__(self):
        super().__init__(0xfa)

class FadeSongVolume(_Instruction):
    def __init__(self, fade_time, volume):
        super().__init__(0xf6, 0x81, fade_time, volume)

    def __str__(self):
        return super().__str__(f"{self.args[1]}, {self.args[2]}")

class FadeLoadMap(_LoadMap):
    # same as load map, except fades out screen
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0x6a, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)

class LoadMap(_LoadMap):
    def __init__(self, map_id, direction, default_music, x, y, fade_in = False, entrance_event = False,
                 airship = False, chocobo = False, update_parent_map = False, unknown = False):

        super().__init__(0x6b, map_id, direction, default_music, x, y,
                         fade_in, entrance_event, airship, chocobo, update_parent_map, unknown)

class SetParentMap(_Instruction):
    def __init__(self, map_id, direction, x, y):
        self.map_id = map_id
        self.x = x
        self.y = y

        from ...data import direction as data_direction
        if direction == data_direction.UP:
            dir_arg = 2
        elif direction == data_direction.RIGHT:
            dir_arg = 3
        elif direction == data_direction.DOWN:
            dir_arg = 0
        elif direction == data_direction.LEFT:
            dir_arg = 1

        super().__init__(0x6c, map_id & 0xff, (map_id & 0xff00) >> 8, x, y, dir_arg)

    def __str__(self):
        return super().__str__(f"{self.map_id} ({self.x}, {self.y})")

class SetMapTiles(_Instruction):
    # x, y = top left of where to replace tiles
    # w, h = width, height of area to replace
    # tiles = what to replace the area with
    def __init__(self, layer, x, y, w, h, tiles):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if layer == 2:
            y += 0x40
        elif layer == 3:
            y += 0x80

        args = [x, y, w, h]
        args.extend(tiles)
        super().__init__(0x73, args)

    def __str__(self):
        return super().__str__(f"({self.x}, {self.y}) {self.w}x{self.h}")

class SetEventBit(_Instruction):
    def __init__(self, event_bit):
        self.event_bit = event_bit
        assert self.event_bit <= 0x6ff

        opcode = 0xd0 + (self.event_bit // 0x100) * 2
        arg = self.event_bit & 0xff
        super().__init__(opcode, arg)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class ClearEventBit(_Instruction):
    def __init__(self, event_bit):
        self.event_bit = event_bit
        assert self.event_bit <= 0x6ff

        opcode = 0xd1 + (self.event_bit // 0x100) * 2
        arg = self.event_bit & 0xff
        super().__init__(opcode, arg)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class BranchIfEventBitSet(_Branch):
    def __init__(self, event_bit, destination):
        self.event_bit = event_bit
        event_bit_arg = (event_bit | 0x8000).to_bytes(2, "little")

        super().__init__(0xc0, [event_bit_arg], destination)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class ReturnIfEventBitSet(BranchIfEventBitSet):
    def __init__(self, event_bit):
        from ...instruction.field.functions import RETURN
        super().__init__(event_bit, RETURN)

class BranchIfEventBitClear(_Branch):
    def __init__(self, event_bit, destination):
        self.event_bit = event_bit
        event_bit_arg = event_bit.to_bytes(2, "little")

        super().__init__(0xc0, [event_bit_arg], destination)

    def __str__(self):
        return super().__str__(hex(self.event_bit))

class ReturnIfEventBitClear(BranchIfEventBitClear):
    def __init__(self, event_bit):
        from ...instruction.field.functions import RETURN
        super().__init__(event_bit, RETURN)

class BranchIfAny(_Branch):
    def __init__(self, checks, destination):
        assert len(checks) // 2 <= 7
        opcode = 0xc1 + (len(checks) // 2) - 2

        args = []
        self.arg_strings = []
        for i in range(0, len(checks), 2):
            self.arg_strings.append((checks[i], checks[i + 1]))

            args.append(checks[i] & 0xff)
            args.append((checks[i] & 0xff00) >> 8)
            if checks[i + 1]:
                args[-1] |= 0x80
        super().__init__(opcode, args, destination)

    def __str__(self):
        substrings = []
        for bit_value in self.arg_strings:
            substrings.append(f"{hex(bit_value[0])} = {bit_value[1]}")
        substring = " or ".join(substrings) + ","
        return super().__str__(substring)

class BranchIfAll(_Branch):
    def __init__(self, checks, destination):
        assert len(checks) // 2 <= 7
        opcode = 0xc9 + (len(checks) // 2) - 2

        args = []
        self.arg_strings = []
        for i in range(0, len(checks), 2):
            self.arg_strings.append((checks[i], checks[i + 1]))

            args.append(checks[i] & 0xff)
            args.append((checks[i] & 0xff00) >> 8)
            if checks[i + 1]:
                args[-1] |= 0x80
        super().__init__(opcode, args, destination)

    def __str__(self):
        substrings = []
        for bit_value in self.arg_strings:
            substrings.append(f"{hex(bit_value[0])} = {bit_value[1]}")
        substring = " and ".join(substrings) + ","
        return super().__str__(substring)

class ReturnIfAny(BranchIfAny):
    def __init__(self, checks):
        from ...instruction.field.functions import RETURN
        super().__init__(checks, RETURN)

class ReturnIfAll(BranchIfAll):
    def __init__(self, checks):
        from ...instruction.field.functions import RETURN
        super().__init__(checks, RETURN)

class Branch(BranchIfEventBitClear):
    def __init__(self, destination):
        super().__init__(event_bit.ALWAYS_CLEAR, destination)

class BranchRandomly(_Branch):
    def __init__(self, destination):
        super().__init__(0xbd, [], destination)

class SetBattleEventBit(_Instruction):
    def __init__(self, battle_event_bit):
        self.battle_event_bit = battle_event_bit
        super().__init__(0xb8, battle_event_bit)

    def __str__(self):
        return super().__str__(hex(self.battle_event_bit))

class BranchIfBattleEventBitClear(_Branch):
    def __init__(self, battle_event_bit, destination):
        self.battle_event_bit = battle_event_bit
        super().__init__(0xb7, [battle_event_bit], destination)

    def __str__(self):
        return super().__str__(hex(self.battle_event_bit))

class ReturnIfBattleEventBitClear(BranchIfBattleEventBitClear):
    def __init__(self, battle_event_bit):
        from ...instruction.field.functions import RETURN
        super().__init__(battle_event_bit, RETURN)

class SetEventWord(_Instruction):
    def __init__(self, event_word, value):
        self.event_word = event_word
        self.value = value
        super().__init__(0xe8, event_word, value.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(f"{hex(self.event_word)} {self.value}")

class AddToEventWord(_Instruction):
    def __init__(self, event_word, value):
        self.value = value
        super().__init__(0xe9, event_word, value.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class IncrementEventWord(AddToEventWord):
    def __init__(self, event_word):
        super().__init__(event_word, 1)

    def __str__(self):
        return super(AddToEventWord, self).__str__(f"{self.args[0]}")

class SubtractFromEventWord(_Instruction):
    def __init__(self, event_word, value):
        self.value = value
        super().__init__(0xea, event_word, value.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.args[1]}")

class DecrementEventWord(SubtractFromEventWord):
    def __init__(self, event_word):
        super().__init__(event_word, 1)

    def __str__(self):
        return super(SubtractFromEventWord, self).__str__(f"{self.args[0]}")

class CompareEventWord(_Instruction):
    def __init__(self, event_word, value):
        # compare event word to value, set 0x1a0 if equal, set 0x1a1 if event_word > value, 0x1a2 if event_word < value
        self.value = value
        super().__init__(0xeb, event_word, value.to_bytes(2, "little"))

    def __str__(self):
        return super().__str__(f"{self.args[0]} {self.value}")

class _BranchIfEventWordEqual(BranchIfEventBitSet):
    def __init__(self, destination):
        super().__init__(0x1a0, destination)

def BranchIfEventWordEqual(event_word, value, destination):
    BranchIfEventWordEqual = type("BranchIfEventWordEqual", (_BranchIfEventWordEqual,), {})
    return CompareEventWord(event_word, value), BranchIfEventWordEqual(destination)

class _BranchIfEventWordNotEqual(BranchIfEventBitClear):
    def __init__(self, destination):
        super().__init__(0x1a0, destination)

def BranchIfEventWordNotEqual(event_word, value, destination):
    BranchIfEventWordNotEqual = type("BranchIfEventWordNotEqual", (_BranchIfEventWordNotEqual,), {})
    return CompareEventWord(event_word, value), BranchIfEventWordNotEqual(destination)

class _BranchIfEventWordGreater(BranchIfEventBitSet):
    def __init__(self, destination):
        super().__init__(0x1a1, destination)

def BranchIfEventWordGreater(event_word, value, destination):
    BranchIfEventWordGreater = type("BranchIfEventWordGreater", (_BranchIfEventWordGreater,), {})
    return CompareEventWord(event_word, value), BranchIfEventWordGreater(destination)

class _BranchIfEventWordLess(BranchIfEventBitSet):
    def __init__(self, destination):
        super().__init__(0x1a2, destination)

def BranchIfEventWordLess(event_word, value, destination):
    BranchIfEventWordLess = type("BranchIfEventWordLess", (_BranchIfEventWordLess,), {})
    return CompareEventWord(event_word, value), BranchIfEventWordLess(destination)

class _ReturnIfEventWordLess(ReturnIfEventBitSet):
    def __init__(self):
        super().__init__(0x1a2)

def ReturnIfEventWordLess(event_word, value):
    ReturnIfEventWordLess = type("ReturnIfEventWordLess", (_ReturnIfEventWordLess,), {})
    return CompareEventWord(event_word, value), ReturnIfEventWordLess()

class LoadPartyMembers(_Instruction):
    def __init__(self):
        # caseword bits = characters in party
        super().__init__(0xde)

class LoadCreatedCharacters(_Instruction):
    def __init__(self):
        # caseword bits = characters created
        super().__init__(0xdf)

class LoadRecruitedCharacters(_Instruction):
    def __init__(self):
        # caseword bits = characters recruited
        super().__init__(0xe0)

class LoadAvailableCharacters(_Instruction):
    def __init__(self):
        # caseword bits = characters available
        super().__init__(0xe1)

def BranchIfCharacterInParty(character, destination):
    return LoadPartyMembers(), BranchIfEventBitSet(event_bit.multipurpose(character), destination)

def ReturnIfCharacterNotInParty(character):
    return LoadPartyMembers(), ReturnIfEventBitClear(event_bit.multipurpose(character))

def BranchIfCharacterUnavailable(character, destination):
    return LoadAvailableCharacters(), BranchIfEventBitClear(event_bit.multipurpose(character), destination)

def BranchIfCharacterNotRecruited(character, destination):
    return LoadRecruitedCharacters(), BranchIfEventBitClear(event_bit.multipurpose(character), destination)

def ReturnIfCharacterNotRecruited(character):
    return LoadRecruitedCharacters(), ReturnIfEventBitClear(event_bit.multipurpose(character))

class _BranchIfPartySize(BranchIfEventBitSet):
    def __init__(self, size, destination):
        self.size = size

        event_bit_arg = event_bit.multipurpose(size - 1)
        super().__init__(event_bit_arg, destination)

    def __str__(self):
        return super(BranchIfEventBitSet, self).__str__(self.size)

def BranchIfPartySize(size, destination):
    from ...instruction.field.functions import UPDATE_PARTY_SIZE_EVENT_BITS
    BranchIfPartySize = type("BranchIfPartySize", (_BranchIfPartySize,), {})
    return Call(UPDATE_PARTY_SIZE_EVENT_BITS), BranchIfPartySize(size, destination)

class LoadActiveParty(_Instruction):
    def __init__(self):
        # caseword bits = active party number
        super().__init__(0xe4)

def BranchIfEsperNotFound(esper, destination):
    from ...instruction.field.custom import LoadEsperFound
    return LoadEsperFound(esper), BranchIfEventBitClear(event_bit.multipurpose(0), destination)

def BranchIfPartyEmpty(party, destination):
    from ...instruction.field.custom import LoadPartiesWithCharacters
    return LoadPartiesWithCharacters(), BranchIfEventBitClear(event_bit.multipurpose(party-1), destination)

class _InvokeBattle(_Instruction):
    def __init__(self, pack, background, battle_sound, battle_animation):
        self.pack = pack

        pack_arg = pack - 0x100
        background_sound_animation = background
        if not battle_sound:
            background_sound_animation |= 0x40
        if not battle_animation:
            background_sound_animation |= 0x80

        super().__init__(0x4d, pack_arg, background_sound_animation)

    def __str__(self):
        return super().__str__(str(self.pack))

def InvokeBattle(pack, background = 0x3f, battle_sound = True, battle_animation = True, check_game_over = True):
    InvokeBattle = type("InvokeBattle", (_InvokeBattle,), {})
    commands = [InvokeBattle(pack, background, battle_sound, battle_animation)]
    if check_game_over:
        from ...instruction.field.functions import CHECK_GAME_OVER
        commands.append(Call(CHECK_GAME_OVER))
    return commands

class BattleType(IntEnum):
    FRONT   = 0
    BACK    = 1
    PINCER  = 2
    SIDE    = 3
def InvokeBattleType(pack, battle_type, background = 0x3f, check_game_over = True):
    from ...instruction.field.custom import _InvokeBattleType
    InvokeBattleType = type("InvokeBattleType", (_InvokeBattleType,), {})
    commands = [InvokeBattleType(pack, battle_type, background)]
    if check_game_over:
        from ...instruction.field.functions import CHECK_GAME_OVER
        commands.append(Call(CHECK_GAME_OVER))
    return commands

class InvokeColiseumBattle(_Instruction):
    def __init__(self):
        super().__init__(0xaf)

class _EntityAct(_Instruction):
    def __init__(self, entity, wait_until_complete, *actions):
        from ...instruction.field import entity as field_entity
        actions = list(actions) + [field_entity.End()]

        self.actions_size = 0
        for action in actions:
            if not isinstance(action, str):
                self.actions_size += len(action)
        self.wait_until_complete = wait_until_complete

        size_wait = self.actions_size
        if wait_until_complete:
            size_wait |= 0x80

        super().__init__(entity, size_wait)

    def __str__(self):
        result = f"{type(self).__name__}, {self.actions_size} bytes"
        if self.wait_until_complete:
            result += ", Wait"
        else:
            result += ", No Wait"
        return result

def EntityAct(entity, wait_until_complete, *actions):
        from ...instruction.field import entity as field_entity
        EntityAct = type("EntityAct", (_EntityAct,), {})
        return EntityAct(entity, wait_until_complete, *actions), list(actions), field_entity.End()

class WaitForEntityAct(_Instruction):
    def __init__(self, entity):
        super().__init__(0x35, entity)

    def __str__(self):
        return super().__str__(self.args[0])

class _RepeatStart(_Instruction):
    def __init__(self, count, *commands):
        super().__init__(0xb0, count)

    def __str__(self):
        return super().__str__(self.args[0])

class _RepeatEnd(_Instruction):
    def __init__(self):
        super().__init__(0xb1)

def Repeat(count, *commands):
    RepeatStart = type("RepeatStart", (_RepeatStart,), {})
    RepeatEnd = type("RepeatEnd", (_RepeatEnd,), {})
    return RepeatStart(count), list(commands), RepeatEnd()

class StartTimer(_Instruction):
    def __init__(self, timer_id, units, expire_address, show_in_menu = False, show_on_map = False,
                 pause_in_menu_and_battle = False, exit_menu_and_battle_if_expire = False):
        # 1 unit = ~1/60 of a second

        address_flags = (expire_address - EVENT_CODE_START)
        address_flags |= timer_id << 18
        if show_in_menu:
            address_flags |= 0x100000
        if exit_menu_and_battle_if_expire:
            address_flags |= 0x200000
        if show_on_map:
            address_flags |= 0x400000
        if pause_in_menu_and_battle:
            address_flags |= 0x800000

        super().__init__(0xa0, units.to_bytes(2, "little"), address_flags.to_bytes(3, "little"))

class ResetTimer(_Instruction):
    def __init__(self, timer_id):
        super().__init__(0xa1, timer_id)

class ResetScreenColors(_Instruction):
    def __init__(self):
        super().__init__(0x54)

class DeleteRotatingPyramids(_Instruction):
    def __init__(self):
        super().__init__(0xa6)

class InvokeFinalLineup(_Instruction):
    def __init__(self):
        super().__init__(0x9d)

class AverageLevel(_Instruction):
    def __init__(self, character):
        super().__init__(0x77, character)

class RestoreHp(_Instruction):
    def __init__(self, character, amount):
        # Modify actor A's Hit Points. B is the amount, however, bit 0x80 tells it to subtract. The amount in 0x7F is a power of 2 to add/subtract.
        # So, for instance, 8B 01 04 would Add (high bit clear) to Locke (character 01) 16 HP (2^4). Clear as mud?
        # Caveats (1) if the parameter is 7F, it just sets the HP to maximum. (2) No matter how much is subtracted, it can't end up below 1 HP.
        super().__init__(0x8b, character, amount)

class RestoreMp(_Instruction):
    def __init__(self, character, amount):
        # Modify actor A's Magic Points. B is the amount, however, bit 0x80 tells it to subtract. The amount in 0x7F is a power of 2 to add/subtract.
        # This command appears to have been a copy/paste of the Hit Points, however, they did not code the powers of 2 part, so in reality, the only 
        # thing this can do is set MP to max via the 7F second parameter.
        super().__init__(0x8c, character, amount)
