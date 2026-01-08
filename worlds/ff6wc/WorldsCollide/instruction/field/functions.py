from ...memory.space import Bank, Reserve, Write
from ...instruction.field import instructions as field
from ...instruction.field import entity as field_entity
from ...data import battle_bit as battle_bit

RETURN = 0xa5eb3    # return command, used for branching
END = 0xa5eb4       # end command, used for branching
GAME_OVER = 0xce566 # black screen with character -> title screen

NOT_ENOUGH_MONEY = 0xb69ff
HEAL_PARTY_HP_MP_STATUS = 0xacfbd
GATHER_AFTER_INN = 0xacf9e
CREATE_AVAILABLE_CHARACTERS = 0xac90b
DELETE_CHARACTERS_NOT_IN_ANY_PARTY = 0xacca4
REMOVE_ALL_CHARACTERS_FROM_ALL_PARTIES = 0xaf61a
HIDE_ALL_PARTY_MEMBERS = 0xb39ac
SHOW_ALL_PARTY_MEMBERS = 0xb39b5
HIDE_PARTY_MEMBERS_EXCEPT_LEADER = 0xacb95
UPDATE_LEADER_AND_SHOW_ALL_PARTY_MEMBERS = 0xac766
ENABLE_COLLISIONS_FOR_PARTY_MEMBERS = 0xb2e2b
DISABLE_COLLISIONS_FOR_PARTY_MEMBERS = 0xb2e34
RETURN_ALL_PARTIES_TO_FALCON = 0xc2109
UPDATE_PARTY_SIZE_EVENT_BITS = 0xac5c1

def _delete_all_characters_mod():
    from ...constants.entities import CHARACTER_COUNT

    src = []
    for character in range(CHARACTER_COUNT):
        src += [
            field.DeleteEntity(character),
        ]
    src += [
        field.Return(),
    ]
    space = Write(Bank.CA, src, "field function delete all characters")
    return space.start_address
DELETE_ALL_CHARACTERS = _delete_all_characters_mod()

def _refresh_characters_and_select_parties_mod(count):
    # create all available characters, select count parties, delete characters not placed into any party
    src = [
        field.Call(DELETE_ALL_CHARACTERS),
        field.Call(CREATE_AVAILABLE_CHARACTERS),
        field.RefreshEntities(),
        field.SelectParties(count),
        field.Call(DELETE_CHARACTERS_NOT_IN_ANY_PARTY),
        field.RefreshEntities(),
        field.Return(),
    ]
    return src

def _select_party_mod():
    src = _refresh_characters_and_select_parties_mod(1)
    space = Write(Bank.CA, src, "field function refresh characters and select party")
    return space.start_address
REFRESH_CHARACTERS_AND_SELECT_PARTY = _select_party_mod()

def _select_two_parties_mod():
    src = _refresh_characters_and_select_parties_mod(2)
    space = Write(Bank.CA, src, "field function refresh characters and select two parties")
    return space.start_address
REFRESH_CHARACTERS_AND_SELECT_TWO_PARTIES = _select_two_parties_mod()

def _select_three_parties_mod():
    src = _refresh_characters_and_select_parties_mod(3)
    space = Write(Bank.CA, src, "field function refresh characters and select three parties")
    return space.start_address
REFRESH_CHARACTERS_AND_SELECT_THREE_PARTIES = _select_three_parties_mod()

def _toggle_party_magitek_mod():
    src = [
        field.ToggleStatusEffects(field_entity.PARTY0, field.Status.MAGITEK),
        field.ToggleStatusEffects(field_entity.PARTY1, field.Status.MAGITEK),
        field.ToggleStatusEffects(field_entity.PARTY2, field.Status.MAGITEK),
        field.ToggleStatusEffects(field_entity.PARTY3, field.Status.MAGITEK),
        field.Return(),
    ]
    space = Write(Bank.CA, src, "field function toggle party magitek")
    return space.start_address
TOGGLE_PARTY_MAGITEK = _toggle_party_magitek_mod()

def _original_check_game_over_mod():
    src = [
        field.ReturnIfBattleEventBitClear(battle_bit.PARTY_ANNIHILATED),
        field.Call(GAME_OVER),
        field.Return(),
    ]
    space = Write(Bank.CA, src, "field function original check game over")
    return space.start_address
ORIGINAL_CHECK_GAME_OVER = _original_check_game_over_mod()

def _check_game_over_mod():
    src = [
        # bababreath can remove the party leader and cause the party to be invisible after a battle
        # refresh objects and update party leader to prevent invisible party
        field.RefreshEntities(),
        field.UpdatePartyLeader(),

        field.ReturnIfBattleEventBitClear(battle_bit.PARTY_ANNIHILATED),
        field.Call(GAME_OVER),
        field.Return(),
    ]
    space = Write(Bank.CA, src, "field function check game over")
    check_game_over = space.start_address

    # replace original game over check with bababreath safe one
    space = Reserve(0xa5ea9, 0xa5eb2, "field function call check game over", field.NOP())
    space.write(
        field.Call(check_game_over),
        field.Return(),
    )
    return check_game_over
CHECK_GAME_OVER = _check_game_over_mod()

class CheckObjectives(field.Call):
    def __init__(self):
        from ... import objectives as objectives

        src = []
        for objective in objectives:
            src += [
                objective.check_complete.field(),
            ]
        src += [
            field.Return(),
        ]
        space = Write(Bank.CA, src, "field check objectives")
        CheckObjectives.__init__ = lambda self : super().__init__(space.start_address)
        self.__init__()

class FinishCheck(field.Call):
    def __init__(self):
        from ...data import event_word as event_word
        src = [
            field.IncrementEventWord(event_word.CHECKS_COMPLETE),
            CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "field function finish check")
        FinishCheck.__init__ = lambda self : super().__init__(space.start_address)
        self.__init__()
