CHAIN_START_CODE    = 0xFD
CHAIN_END_CODE      = 0xFC
CHAIN_INTO_CODE     = 0xFB
END_CODE            = 0xFF

COMMANDS = {
    0xC0 : ['fight'],
    0xE1 : ['pass'],
    0xE8 : ['set race {}', 'races'],
    0xE9 : ['set attack index {}', 'hex'],
    0xEA : ['set defense index {}', 'hex'],
    0xEB : ['set magic defense index {}', 'hex'],
    0xEC : ['speed {}', 'speed_delta'],
    0xED : ['set resistance {}', 'elements'],
    0xEE : ['set spell power {}', 'decimal'],
    0xEF : ['set weakness {}', 'elements'],
    0xF0 : ['set sprite {}', 'hex'],
    0xF1 : ['message {}', 'hex'],
    0xF2 : ['message {} next action', 'hex'],
    0xF3 : ['music {}', 'music'],
    0xF4 : ['condition {}', 'condition_delta'],
    0xF5 : ['set reaction {}', 'reaction'],
    0xF7 : ['darken {}', 'hex'],
    0xF8 : ['debug {}', 'hex'],
    0xF9 : ['target {}', 'target'],
}

TARGETS = {
    0x16 : 'self',
    0x17 : 'all monsters',
    0x18 : 'other monsters',
    0x19 : 'type 0 monsters',
    0x1A : 'type 1 monsters',
    0x1B : 'type 2 monsters',
    0x1C : 'front row',
    0x1D : 'back row',
    0x1E : 'stunned monster',
    0x1F : 'sleeping monster',
    0x20 : 'charmed monster',
    0x21 : 'weak monster',
    0x22 : 'random anything',
    0x23 : 'random other anything',
    0x24 : 'random monster',
    0x25 : 'random other monster',
    0x26 : 'random front row',
    0x27 : 'random back row',
    0x28 : 'all characters',
    0x29 : 'dead monsters'
}

COMMAND_CODES_BY_SLUG = {
    COMMANDS[k][0].replace('{}', '').replace(' ', '').lower() : k
    for k in COMMANDS
    }

TARGET_CODES_BY_SLUG = {
    TARGETS[k].replace(' ', '') : k
    for k in TARGETS
    }
