CHECKPOINT_BANQUET = 0 # used for narshe checkpoint and emperor's banquet
NARSHE_CHECKPOINT = 1
CHARACTERS_AVAILABLE = 2 # custom
ESPERS_FOUND = 3 # custom
CHECKS_COMPLETE = 4 # custom
CID_HEALTH = 5 # custom, originally cid_health shares coral_found event word
DRAGONS_DEFEATED = 6 # track defeated instead of remaining
CORAL_FOUND = 7 # also used for cid's health

# $1ff8 is unused and close enough to other words to be used by event commands
BOSSES_DEFEATED = 27 # custom
SCRATCH = 28 # custom, scratch space

def address(event_word):
    # event word 0 starts at 1fc2, 1 is at 1fc4, ..., 7 is at 1fd0
    return 0x1fc2 + event_word * 2

def _init_event_words_mod():
    from ..memory.space import Bank, Reserve, Write
    from ..instruction import asm as asm

    # initialize custom event words to zero
    # this is done before pregame menu so no objectives shown as complete
    src = [
        asm.JSR(0xbb0c, asm.ABS),   # call clear event bits

        asm.LDX(0x00, asm.DIR),                             # x = 0
        "LOOP_START",
        asm.STZ(address(CHARACTERS_AVAILABLE), asm.ABS_X),  # clear byte
        asm.INX(),                                          # next byte
        asm.CPX((DRAGONS_DEFEATED - CHARACTERS_AVAILABLE + 1) * 2, asm.IMM16),
        asm.BNE("LOOP_START"),

        asm.LDX(0x00, asm.DIR),                             # x = 0
        "LOOP_START2",
        asm.STZ(address(BOSSES_DEFEATED), asm.ABS_X),       # clear byte
        asm.INX(),                                          # next byte
        asm.CPX((SCRATCH - BOSSES_DEFEATED + 1) * 2, asm.IMM16),
        asm.BNE("LOOP_START2"),
        asm.RTS(),
    ]
    space = Write(Bank.C0, src, "init event words")
    init_event_words = space.start_address

    space = Reserve(0x0be87, 0x0be89, "clear event bits")
    space.write(
        asm.JSR(init_event_words, asm.ABS),
    )
_init_event_words_mod()
