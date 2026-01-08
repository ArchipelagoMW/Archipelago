from ..memory.space import BANK_SIZE, Free

# https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:rom_map
# https://www.ff6hacking.com/wiki/doku.php?id=ff3:ff3us:doc:asm:rom_map:unused_space
spaces = [
    (0x00d613, 0x00df9f),
    (0x00ec20, 0x00ee9f),
    (0x00fcab, 0x00fcff),
    (0x00ff18, 0x00ffaf),
    (0x01ffe5, 0x01ffff),
    (0x026469, 0x0267ff),
    (0x02a65a, 0x02a7ff),
    (0x02faa4, 0x02fc6c),
    (0x03f091, 0x03ffff),
    (0x046a6b, 0x046abf),
    (0x04a4c0, 0x04b9ff),
    (0x04bfb9, 0x04c007),
    (0x04f1c2, 0x04f476),
    (0x04ff72, 0x04ffff),
    (0x09fcec, 0x09fdff),
    (0x0eefbb, 0x0ef0ff),
    (0x0ef463, 0x0ef5ff),
    (0x0efee0, 0x0effff),
    (0x0f3bae, 0x0f3c3f),
    (0x0f3c9b, 0x0f3cff),
    (0x0f83c0, 0x0f83ff),
    (0x0fcf50, 0x0fd0cf),
    (0x0ffb29, 0x0ffbff),
    (0x0ffce0, 0x0ffcff),
    (0x0ffda0, 0x0ffdff),
    (0x0fff47, 0x0fff9d),
    (0x0fffbe, 0x0fffff),
    (0x1095e6, 0x1097ff),
    (0x10cf4a, 0x10cfff),
    (0x10fc7a, 0x10fcff),
    (0x11e989, 0x11ead7),
    (0x11f751, 0x11f79f),
    (0x11f9d0, 0x11f9ff),
    (0x126f6f, 0x126fff),
    (0x12b224, 0x12b2ff),
    (0x12eb44, 0x12ebff),
    (0x14c998, 0x14c9ff),
    (0x14cf5b, 0x14cfff),
    (0x14f646, 0x14ffff),
    (0x186f29, 0x186fff),
    (0x18ce51, 0x18ce9f),
    (0x18dcd2, 0x18dcff),
    (0x18e7b1, 0x18e7ff),
    (0x18ee47, 0x18efff),
    (0x199a51, 0x199d4a),
    (0x19a569, 0x19a7ff),
    (0x19cc4b, 0x19cd0f),
    (0x1fb3d4, 0x1fb3ff),
    (0x1fbae4, 0x1fbaff),
    (0x1fd978, 0x1fd9ff),
    (0x26cd3d, 0x26cd5f),
    (0x26f198, 0x26f1ff),
    (0x26f440, 0x26f48f),
    (0x2962c1, 0x2962ff),
    (0x2ce200, 0x2ce3bf),
    (0x2d63e0, 0x2d63ff),
    (0x2d7787, 0x2d779f),
    (0x2d8bca, 0x2d8e5a),
    (0x2d8e9b, 0x2d8eff),
    (0x2dfcaa, 0x2dfdff),
    (0x2eaf01, 0x2eb1ff),
    (0x2ffbc8, 0x2ffeef),

    # EVENTS
    (0x0a4363, 0x0a48bf), # daryl tomb staircase daryl flashback
    (0x0a48e3, 0x0a533e), # end of the world
    (0x0a6629, 0x0a6785), # terra/locke meet edgar in figaro castle wob
    (0x0a75ee, 0x0a7673), # figaro cave entrance guard
    (0x0a83c0, 0x0a8467), # mt kolts sabin joins party
    (0x0a8842, 0x0a89ae), # south figaro celes/locke escape basement scenes
    (0x0a8d27, 0x0a8ee4), # finished serpent trench boat to south figaro scene
    (0x0a9749, 0x0a9d0f), # zozo meet ramuh, learn about magicite/magitek factory
    (0x0ac3c7, 0x0ac5c0), # party flies back to zozo to see terra and load esper world
    (0x0ade64, 0x0ae3d5), # floating continent statues scene before escape
    (0x0afab8, 0x0affef), # returner's hideout gauntlet/genji glove and wounded returner
    (0x0b0080, 0x0b03f5), # returner's hideout meeting and wounded returner
    (0x0b094e, 0x0b0a1b), # lete river choose terra/edgar/banon scenario and continue river"
    (0x0b0f2f, 0x0b1031), # imperial camp leo/soldier letter from emperor
    (0x0b1b14, 0x0b1e4c), # airship back room scene after opera
    (0x0b22bb, 0x0b2378), # locke/setzer "could it crash?" sore thumb scene
    (0x0b39de, 0x0b3dca), # sealed gate opening/kefka/close scene
    (0x0b75d6, 0x0b77c7), # relm and strago find gungho hurt in thamasa wor
    (0x0ba0ec, 0x0ba37d), # doma poisoned, purple water function, cyan checks liege
    (0x0bba0c, 0x0bbec3), # cyan's family scene after phantom train
    (0x0bbfe9, 0x0bc026), # baren falls shadow leaves
    (0x0bc228, 0x0bc5fa), # serpent trench cave various tile events (gau forget, scare sabin, drop gp, ...)
    (0x0bc730, 0x0bc84c), # serpent trench cave go outside and jump in water
    (0x0bd982, 0x0bdcb2), # meet/name strago/relm in thamasa
    (0x0bdcce, 0x0be5ca), # thamasa night villagers outside burning house scene
    (0x0bea65, 0x0bec91), # after burning house, strago explanation scene
    (0x0bf168, 0x0bf295), # esper mountain statues event
    (0x0bf2b5, 0x0bff6f), # from espers in esper mountain until play as leo in thamasa
    (0x0c0000, 0x0c0976), # leo challenges kefka to after full party arrives in thamasa
    (0x0c1a66, 0x0c1e3f), # ancient castle flashback scene
    (0x0c1f9f, 0x0c2047), # 8 dragons decrement count, receive crusader
    (0x0c2bf0, 0x0c3296), # kohlingen rachel scenes after phoenix cave
    (0x0c3971, 0x0c3af7), # recruit mog wor
    (0x0c4ced, 0x0c5029), # mobliz wor esper terra and children scene
    (0x0c6150, 0x0c62a5), # locke/celes albrook inn night scene
    (0x0c6a2e, 0x0c6ce3), # locke/rachel lost memories flashback at rachel's house
    (0x0c6f8c, 0x0c704e), # hire shadow kohlingen inn
    (0x0c73e1, 0x0c7564), # kefka throwing ifrit and shiva into trash scene
    (0x0c7a85, 0x0c7ec3), # magitek factory tube espers and celes scene"
    (0x0c985b, 0x0c9a4e), # intro text, terra/wedge/vicks on cliff
    (0x0c9b1d, 0x0c9ef1), # narshe beginning events, guard fights, vicks breaks gate
    (0x0cbd05, 0x0cc1b2), # esper terra/tritoch scenes after kefka at narshe
]

def free():
    for space in spaces:
        Free(space[0], space[1])

    # expanded rom free space
    for bank in range(0x30, 0x40):
        start = bank * BANK_SIZE
        end = start + BANK_SIZE - 1
        Free(start, end)
