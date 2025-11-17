normal_door_hook = [
    0x00862021,  # ADDU  A0, A0, A2
    0x80849C60,  # LB    A0, 0x9C60 (A0)
    0x0C0FF174,  # JAL   0x803FC5D0
    0x308900FF   # ANDI  T1, A0, 0x00FF
]

normal_door_code = [
    0x00024080,  # SLL   T0, V0, 2
    0x3C048039,  # LUI   A0, 0x8039
    0x00882021,  # ADDU  A0, A0, T0
    0x8C849BE4,  # LW    A0, 0x9BE4 (A0)
    0x8C6A0008,  # LW    T2, 0x0008 (V1)
    0x008A5824,  # AND   T3, A0, T2
    0x11600003,  # BEQZ  T3,     [forward 0x03]
    0x00000000,  # NOP
    0x24020003,  # ADDIU V0, R0, 0x0003
    0x27FF006C,  # ADDIU RA, RA, 0x006C
    0x03E00008   # JR    RA
]

ct_door_hook = [
    0x0C0FF182,  # JAL	 0x803FC608
    0x00000000,  # NOP
    0x315900FF   # ANDI  T9, T2, 0x00FF
]

ct_door_code = [
    0x3C0A8039,  # LUI   T2, 0x8039
    0x8D429BF8,  # LW    V0, 0x9BF8 (T2)
    0x01465021,  # ADDU  T2, T2, A2
    0x814A9C60,  # LB    T2, 0x9C60 (T2)
    0x00495824,  # AND   T3, V0, T1
    0x55600001,  # BNEZL T3,     [forward 0x01]
    0x27FF0010,  # ADDIU RA, RA, 0x0010
    0x03E00008   # JR    RA
]

stage_select_overwrite = [
    # Replacement for the "wipe world state" function when using the warp menu. Now it's the "Special1 jewel checker"
    # to see how many destinations can be selected on it with the current count.
    0x8FA60018,  # LW	 A2, 0x0018 (SP)
    0xA0606437,  # SB	 R0, 0x6437 (V1)
    0x10000029,  # B	         [forward 0x29]
    0x00000000,  # NOP
    0x3C0A8039,  # LUI	 T2, 0x8039
    0x254A9C4B,  # ADDIU T2, T2, 0x9C4B
    0x814B0000,  # LB	 T3, 0x0000 (T2)
    0x240C000A,  # ADDIU T4, R0, 0x000A
    0x016C001B,  # DIVU	 T3, T4
    0x00003012,  # MFLO	 A2
    0x24C60001,  # ADDIU A2, A2, 0x0001
    0x28CA0009,  # SLTI	 T2, A2, 0x0009
    0x51400001,  # BEQZL T2, 0x8012AC7C
    0x24060008,  # ADDIU A2, R0, 0x0008
    0x3C0A800D,  # LUI   T2, 0x800D
    0x914A5E20,  # LBU   T2, 0x5E20 (T2)
    0x314A0040,  # ANDI  T2, T2, 0x0040
    0x11400003,  # BEQZ  T2,     [forward 0x03]
    0x240BFFFE,  # ADDIU T3, R0, 0xFFFE
    0x3C0C8034,  # LUI   T4, 0x8034
    0xAD8B2084,  # SW    T3, 0x2084 (T4)
    0x03200008,  # JR    T9
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
]

custom_code_loader = [
    # On boot, when the company logos show up, this will trigger and load most of the custom ASM data in this module
    # off from ROM offsets 0xBFC000-0xBFFFFF and into the 803FC000-803FFFFF range in RAM.
    0x3C080C10,  # LUI   T0, 0x0C10
    0x2508F1C0,  # ADDIU T0, T0, 0xF1C0
    0x3C098000,  # LUI   T1, 0x8000
    0xAD282438,  # SW    T0, 0x2438 (T1)
    0x3C088040,  # LUI   T0, 0x8040
    0x9108C000,  # ADDIU T0, 0xC000 (T0)
    0x15000007,  # BNEZ  T0,     [forward 0x07]
    0x3C0400C0,  # LUI   A0, 0x00C0
    0x2484C000,  # ADDIU A0, A0, 0xC000
    0x3C058040,  # LUI   A1, 0x8040
    0x24A5C000,  # ADDIU A1, A1, 0xC000
    0x24064000,  # ADDIU A2, R0, 0x4000
    0x08005DFB,  # J     0x800177EC
    0x00000000,  # NOP
    0x03E00008   # JR    RA
]

remote_item_giver = [
    # The essential multiworld function. Every frame wherein the player is in control and not looking at a text box,
    # this thing will check some bytes in RAM to see if an item or DeathLink has been received and trigger the right
    # functions accordingly to either reward items or kill the player.

    # Primary checks
    0x3C088034,  # LUI   T0, 0x8034
    0x9509244A,  # LHU   T1, 0x244A (T0)
    0x3C088039,  # LUI   T0, 0x8039
    0x910A9EFB,  # LBU   T2, 0x9EFF (T0)
    0x012A4821,  # ADDU  T1, T1, T2
    0x910A9EFF,  # LBU   T2, 0x9EFF (T0)
    0x012A4821,  # ADDU  T1, T1, T2
    0x910A9CCF,  # LBU   T2, 0x9CCF (T0)
    0x012A4821,  # ADDU	 T1, T1, T2
    0x910A9EEF,  # LBU	 T2, 0x9EEF (T0)
    0x012A4821,  # ADDU	 T1, T1, T2
    0x910A9CD3,  # LBU	 T2, 0x9CD3 (T0)
    0x012A4821,  # ADDU	 T1, T1, T2
    0x3C088038,  # LUI	 T0, 0x8038
    0x910A7ADD,  # LBU	 T2, 0x7ADD (T0)
    0x012A4821,  # ADDU	 T1, T1, T2
    0x3C0B8039,  # LUI	 T3, 0x8039
    0x916A9BE0,  # LBU	 T2, 0x9BE0 (T3)
    0x012A4821,  # ADDU  T1, T1, T2
    0x11200006,  # BEQZ	 T1,     [forward 0x06]
    0x00000000,  # NOP
    0x11400002,  # BEQZ  T2,     [forward 0x02]
    0x254AFFFF,  # ADDIU T2, T2, 0xFFFF
    0xA16A9BE0,  # SB	 T2, 0x9BE0 (T3)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Item-specific checks
    0x3C088034,  # LUI 	 T0, 0x8034
    0x91082891,  # LBU	 T0, 0x2891 (T0)
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x15090012,  # BNE	 T0, T1, [forward 0x12]
    0x00000000,  # NOP
    0x256B9BDF,  # ADDIU T3, T3, 0x9BDF
    0x91640000,  # LBU	 A0, 0x0000 (T3)
    0x14800003,  # BNEZ	 A0, [forward 0x03]
    0x00000000,  # NOP
    0x10000005,  # B	         [forward 0x05]
    0x256B0002,  # ADDIU T3, T3, 0x0002
    0x2409000F,  # ADDIU T1, R0, 0x000F
    0xA1690001,  # SB	 T1, 0x0001 (T3)
    0x080FF8DD,  # J	 0x803FE374
    0xA1600000,  # SB	 R0, 0x0000 (T3)
    0x91640000,  # LBU	 A0, 0x0000 (T3)
    0x14800002,  # BNEZ	 A0,     [forward 0x02]
    0x00000000,  # NOP
    0x10000003,  # B             [forward 0x03]
    0x2409000F,  # ADDIU T1, R0, 0x000F
    0x080FF864,  # J	 0x803FE190
    0xA169FFFF,  # SB	 T1, 0xFFFF (T3)
    # DeathLink-specific checks
    0x3C0B8039,  # LUI   T3, 0x8039
    0x256B9BE1,  # ADDIU T3, T3, 0x9BE1
    0x91640002,  # LBU   A0, 0x0002 (T3)
    0x14800002,  # BNEZ  A0,     [forward 0x02]
    0x916900A7,  # LBU   T1, 0x00A7 (T3)
    0x080FF9C0,  # J     0x803FE700
    0x312A0080,  # ANDI  T2, T1, 0x0080
    0x11400002,  # BEQZ  T2,     [forward 0x02]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x35290080,  # ORI   T1, T1, 0x0080
    0xA16900A7,  # SB    T1, 0x00A7 (T3)
    0x2484FFFF,  # ADDIU A0, A0, 0xFFFF
    0x24080001,  # ADDIU T0, R0, 0x0001
    0x03E00008,  # JR    RA
    0xA168FFFD,  # SB    T0, 0xFFFD (T3)
]

deathlink_nitro_edition = [
    # Alternative to the end of the above DeathLink-specific checks that kills the player with the Nitro explosion
    # instead of the normal death.
    0x91690043,  # LBU   T1, 0x0043 (T3)
    0x080FF9C0,  # J     0x803FE700
    0x3C088034,  # LUI   T0, 0x8034
    0x91082BFE,  # LBU   T0, 0x2BFE (T0)
    0x11000002,  # BEQZ  T0,     [forward 0x02]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x35290080,  # ORI   T1, T1, 0x0080
    0xA1690043,  # SB    T1, 0x0043 (T3)
    0x2484FFFF,  # ADDIU A0, A0, 0xFFFF
    0x24080001,  # ADDIU T0, R0, 0x0001
    0x03E00008,  # JR    RA
    0xA168FFFD,  # SB    T0, 0xFFFD (T3)
]

deathlink_nitro_state_checker = [
    # Checks to see if the player is in an alright state before exploding them. If not, then the Nitro explosion spawn
    # code will be aborted, and they should eventually explode after getting out of that state.
    #
    # Invalid states so far include: interacting/going through a door, being grabbed by a vampire.
    0x90880009,  # LBU   T0, 0x0009 (A0)
    0x24090005,  # ADDIU T1, R0, 0x0005
    0x11090005,  # BEQ   T0, T1, [forward 0x05]
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x11090003,  # BEQ   T0, T1, [forward 0x03]
    0x00000000,  # NOP
    0x08000660,  # J     0x80001980
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0xAC400048   # SW    R0, 0x0048 (V0)
]

launch_fall_killer = [
    # Custom code to force the instant fall death if at a high enough falling speed after getting killed by something
    # that launches you (whether it be the Nitro explosion or a Big Toss hit). The game doesn't normally run the check
    # that would trigger the fall death after you get killed by some other means, which could result in a softlock
    # when a killing blow launches you into an abyss.
    0x3C0C8035,  # LUI   T4, 0x8035
    0x918807E2,  # LBU   T0, 0x07E2 (T4)
    0x24090008,  # ADDIU T1, R0, 0x0008
    0x11090002,  # BEQ   T0, T1, [forward 0x02]
    0x2409000C,  # ADDIU T1, R0, 0x000C
    0x15090006,  # BNE   T0, T1, [forward 0x06]
    0x3C098035,  # LUI   T1, 0x8035
    0x91290810,  # LBU   T1, 0x0810 (T1)
    0x240A00C1,  # ADDIU T2, R0, 0x00C1
    0x152A0002,  # BNE   T1, T2, [forward 0x02]
    0x240B0001,  # ADDIU T3, R0, 0x0001
    0xA18B07E2,  # SB    T3, 0x07E2 (T4)
    0x03E00008   # JR    RA
]

deathlink_counter_decrementer = [
    # Decrements the DeathLink counter if it's above zero upon loading a previous state. Checking this number will be
    # how the client will tell if a player's cause of death was something in-game or a DeathLink (and send a DeathLink
    # to the server if it was the former). Also resets the remote item values to 00 so the player's received items don't
    # get mucked up in-game.
    0x3C088039,  # LUI   T0, 0x8039
    0x91099BE3,  # LBU   T1, 0x9BE3 (T0)
    0x11200002,  # BEQZ  T1, 0x803FC154
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1099BE3,  # SB    T1, 0x9BE3
    0x240900FF,  # ADDIU T1, R0, 0x00FF
    0xA1099BE0,  # SB    T1, 0x9BE0 (T0)
    0xA1009BDF,  # SB	 R0, 0x9BDF (T0)
    0xA1009BE1,  # SB	 R0, 0x9BE1 (T0)
    0x91099BDE,  # LBU   T1, 0x9BDE (T0)
    0x55200001,  # BNEZL T1,     [forward 0x01]
    0x24090000,  # ADDIU T1, R0, 0x0000
    0xA1099BDE,  # SB    T1, 0x9BDE (T0)
    0x91099C24,  # LBU   T1, 0x9C24 (T0)
    0x312A0080,  # ANDI  T2, T1, 0x0080
    0x55400001,  # BNEZL T2,     [forward 0x01]
    0x3129007F,  # ANDI  T1, T1, 0x007F
    0x03E00008,  # JR    RA
    0xA1099C24   # SB    T1, 0x9C24 (T0)
]

death_flag_unsetter = [
    # Un-sets the Death status bitflag when overwriting the "Restart this stage" state and sets health to full if it's
    # empty. This is to ensure DeathLinked players won't get trapped in a perpetual death loop for eternity should they
    # receive one right before transitioning to a different stage.
    0x3C048039,  # LUI   A0, 0x8039
    0x90889C88,  # LBU   T0, 0x9C88 (A0)
    0x31090080,  # ANDI  T1, T0, 0x0080
    0x01094023,  # SUBU  T0, T0, T1
    0x908A9C3F,  # LBU   T2, 0x9C3F (A0)
    0x24090064,  # ADDIU T1, R0, 0x0064
    0x51400001,  # BEQZL T2,     [forward 0x01]
    0xA0899C3F,  # SB    T1, 0x9C3F (A0)
    0x08006DAE,  # J     0x8001B6B8
    0xA0889C88   # SB    T0, 0x9C88 (A0)
]

warp_menu_opener = [
    # Enables opening the Stage Select menu by pausing while holding Z + R when not in a boss fight, the castle
    # crumbling sequence following Fake Dracula, or Renon's arena (in the few seconds after his health bar vanishes).
    0x3C08800D,  # LUI   T0, 0x800D
    0x85095E20,  # LH    T1, 0x5E20 (T0)
    0x24083010,  # ADDIU T0, R0, 0x3010
    0x15090011,  # BNE   T0, T1, [forward 0x11]
    0x3C088035,  # LUI   T0, 0x8035
    0x9108F7D8,  # LBU   T0, 0xF7D8 (T0)
    0x24090020,  # ADDIU T1, R0, 0x0020
    0x1109000D,  # BEQ   T0, T1, [forward 0x0D]
    0x3C088039,  # LUI   T0, 0x8039
    0x91099BFA,  # LBU   T1, 0x9BFA (T0)
    0x31290001,  # ANDI  T1, T1, 0x0001
    0x15200009,  # BNEZ  T1,     [forward 0x09]
    0x8D099EE0,  # LW    T1, 0x9EE0
    0x3C0A001B,  # LUI   T2, 0x001B
    0x254A0003,  # ADDIU T2, T2, 0x0003
    0x112A0005,  # BEQ   T1, T2, [forward 0x05]
    0x3C098034,  # LUI   T1, 0x8034
    0xA1009BE1,  # SB    R0, 0x9BE1 (T0)
    0x2408FFFC,  # ADDIU T0, R0, 0xFFFC
    0x0804DA70,  # J     0x80136960
    0xAD282084,  # SW    T0, 0x2084 (T1)
    0x0804DA70,  # J     0x80136960
    0xA44E6436   # SH    T6, 0x6436 (V0)
]

give_subweapon_stopper = [
    # Extension to "give subweapon" function to not change the player's weapon if the received item is a Stake or Rose.
    # Can also increment the Ice Trap counter if getting a Rose or jump to prev_subweapon_dropper if applicable.
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x11240009,  # BEQ   T1, A0, [forward 0x09]
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x11240003,  # BEQ   T1, A0, [forward 0x03]
    0x9465618A,  # LHU   A1, 0x618A (V1)
    0xA46D618A,  # SH    T5, 0x618A (V1)
    0x0804F0BF,  # J     0x8013C2FC
    0x3C098039,  # LUI   T1, 0x8039
    0x912A9BE2,  # LBU   T2, 0x9BE2 (T1)
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0xA12A9BE2,  # SB    T2, 0x9BE2 (T1)
    0x0804F0BF,  # J     0x8013C2FC
]

give_powerup_stopper = [
    # Extension to "give PowerUp" function to not increase the player's PowerUp count beyond 2
    0x240D0002,  # ADDIU T5, R0, 0x0002
    0x556D0001,  # BNEL  T3, T5, [forward 0x01]
    0xA46C6234,  # SH    T4, 0x6234 (V1)
    0x0804F0BF   # J     0x8013C2FC
]

npc_item_hack = [
    # Hack to make NPC items show item textboxes when received (and decrease the Countdown if applicable).
    0x3C098039,  # LUI   T1, 0x8039
    0x001F5602,  # SRL   T2, RA, 24
    0x240B0080,  # ADDIU T3, R0, 0x0080
    0x114B001F,  # BEQ   T2, T3, [forward 0x1F]
    0x240A001A,  # ADDIU T2, R0, 0x001A
    0x27BD0020,  # ADDIU SP, SP, 0x20
    0x15440004,  # BNE   T2, A0, [forward 0x04]
    0x240B0029,  # ADDIU T3, R0, 0x0029
    0x34199464,  # ORI   T9, R0, 0x9464
    0x10000004,  # B             [forward 0x04]
    0x240C0002,  # ADDIU T4, R0, 0x0002
    0x3419DA64,  # ORI   T9, R0, 0xDA64
    0x240B0002,  # ADDIU T3, R0, 0x0002
    0x240C000E,  # ADDIU T4, R0, 0x000E
    0x012C7021,  # ADDU  T6, T1, T4
    0x316C00FF,  # ANDI  T4, T3, 0x00FF
    0x000B5A02,  # SRL   T3, T3, 8
    0x91CA9CA4,  # LBU   T2, 0x9CA4 (T6)
    0x3C0D8040,  # LUI   T5, 0x8040
    0x256FFFFF,  # ADDIU T7, T3, 0xFFFF
    0x01AF6821,  # ADDU  T5, T5, T7
    0x91B8D71C,  # LBU   T8, 0xD71C (T5)
    0x29EF0019,  # SLTI  T7, T7, 0x0019
    0x51E00001,  # BEQZL T7,     [forward 0x01]
    0x91B8D71F,  # LBU   T8, 0xD71F (T5)
    0x13000002,  # BEQZ  T8,     [forward 0x02]
    0x254AFFFF,  # ADDIU T2, T2, 0xFFFF
    0xA1CA9CA4,  # SB    T2, 0x9CA4 (T6)
    0xA12C9BDF,  # SB    T4, 0x9BDF (T1)
    0x3C0400BB,  # LUI   A0, 0x00BB
    0x00992025,  # OR    A0, A0, T9
    0x3C058019,  # LUI   A1, 0x8019
    0x24A5BF98,  # ADDIU A1, A1, 0xBF98
    0x08005DFB,  # J     0x800177EC
    0x24060100,  # ADDIU A2, R0, 0x0100
    0x0804EFFD,  # J     0x8013BFF4
    0xAFBF0014   # SW    RA, 0x0014 (SP)
]

overlay_modifiers = [
    # Whenever a compressed overlay gets decompressed and mapped in the 0F or 0E domains, this thing will check the
    # number ID in the T0 register to tell which one it is and overwrite some instructions in it on-the-fly accordingly
    # to said number before it runs. Confirmed to NOT be a foolproof solution on console and Simple64; the instructions
    # may not be properly overwritten on the first execution of the overlay.

    # Prevent being able to throw Nitro into the Hazardous Waste Disposals
    0x3C0A2402,  # LUI   T2, 0x2402
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x24090023,  # ADDIU T1, R0, 0x0023
    0x15090003,  # BNE   T0, T1, [forward 0x03]
    0x00000000,  # NOP
    0x03200008,  # JR    T9
    0xAF2A01D4,  # SW    T2, 0x01D4 (T9)
    # Make it so nothing can be taken from the Nitro or Mandragora shelves through the textboxes
    0x24090022,  # ADDIU T1, R0, 0x0022
    0x11090002,  # BEQ   T0, T1, [forward 0x02]
    0x24090021,  # ADDIU T1, R0, 0x0021
    0x15090003,  # BNE   T0, T1, [forward 0x03]
    0x254AFFFF,  # ADDIU T2, T2, 0xFFFF
    0x03200008,  # JR    T9
    0xAF2A0194,  # SW    T2, 0x0194 (T9)
    # Fix to allow placing both bomb components at a cracked wall at once while having multiple copies of each, and
    # prevent placing them at the downstairs crack altogether until the seal is removed. Also enables placing both in
    # one interaction.
    0x24090024,  # ADDIU T1, R0, 0x0024
    0x15090012,  # BNE   T0, T1, [forward 0x12]
    0x240A0040,  # ADDIU T2, R0, 0x0040
    0x240BC338,  # ADDIU T3, R0, 0xC338
    0x240CC3D4,  # ADDIU T4, R0, 0xC3D4
    0x240DC38C,  # ADDIU T5, R0, 0xC38C
    0xA32A030F,  # SB    T2, 0x030F (T9)
    0xA72B0312,  # SH    T3, 0x0312 (T9)
    0xA32A033F,  # SB    T2, 0x033F (T9)
    0xA72B0342,  # SH    T3, 0x0342 (T9)
    0xA32A03E3,  # SB    T2, 0x03E3 (T9)
    0xA72C03E6,  # SH    T4, 0x03E6 (T9)
    0xA32A039F,  # SB    T2, 0x039F (T9)
    0xA72D03A2,  # SH    T5, 0x03A2 (T9)
    0xA32A03CB,  # SB    T2, 0x03CB (T9)
    0xA72D03CE,  # SH    T5, 0x03CE (T9)
    0xA32A05CF,  # SB    T2, 0x05CF (T9)
    0x240EE074,  # ADDIU T6, R0, 0xE074
    0xA72E05D2,  # SH    T6, 0x05D2 (T9)
    0x03200008,  # JR    T9
    # Disable the costume and Hard Mode flag checks so that pressing Up on the Player Select screen will always allow
    # the characters' alternate costumes to be used as well as Hard Mode being selectable without creating save data.
    0x2409012E,  # ADDIU T1, R0, 0x012E
    0x1509000A,  # BNE   T0, T1, [forward 0x0A]
    0x3C0A3C0B,  # LUI   T2, 0x3C0B
    0x254A8000,  # ADDIU T2, T2, 0x8000
    0x240B240E,  # ADDIU T3, R0, 0x240E
    0x240C240F,  # ADDIU T4, R0, 0x240F
    0x240D0024,  # ADDIU T5, R0, 0x0024
    0xAF2A0C78,  # SW    T2, 0x0C78 (T9)
    0xA72B0CA0,  # SH    T3, 0x0CA0 (T9)
    0xA72C0CDC,  # SH    T4, 0x0CDC (T9)
    0xA32D0168,  # SB    T5, 0x0024 (T9)
    0x03200008,  # JR    T9
    # Overwrite instructions in the Forest end cutscene script to store a spawn position ID instead of a cutscene ID.
    0x2409002E,  # ADDIU T1, R0, 0x002E
    0x15090005,  # BNE   T0, T1, [forward 0x05]
    0x3C0AA058,  # LUI   T2, 0xA058
    0x254A642B,  # ADDIU T2, T2, 0x642B
    0xAF2A0D88,  # SW    T2, 0x0D88 (T9)
    0xAF200D98,  # SW    R0, 0x0D98 (T9)
    0x03200008,  # JR    T9
    # Disable the rapid flashing effect in the CC planetarium cutscene to ensure it won't trigger seizures.
    0x2409003E,  # ADDIU T1, R0, 0x003E
    0x1509000C,  # BNE   T0, T1, [forward 0x0C]
    0x00000000,  # NOP
    0xAF200C5C,  # SW    R0, 0x0C5C
    0xAF200CD0,  # SW    R0, 0x0CD0
    0xAF200C64,  # SW    R0, 0x0C64
    0xAF200C74,  # SW    R0, 0x0C74
    0xAF200C80,  # SW    R0, 0x0C80
    0xAF200C88,  # SW    R0, 0x0C88
    0xAF200C90,  # SW    R0, 0x0C90
    0xAF200C9C,  # SW    R0, 0x0C9C
    0xAF200CB4,  # SW    R0, 0x0CB4
    0xAF200CC8,  # SW    R0, 0x0CC8
    0x03200008,  # JR    T9
    0x24090134,  # ADDIU T1, R0, 0x0134
    0x15090005,  # BNE   T0, T1, [forward 0x05]
    0x340B8040,  # ORI   T3, R0, 0x8040
    0x340CDD20,  # ORI   T4, R0, 0xDD20
    0xA72B1D1E,  # SH    T3, 0x1D1E (T9)
    0xA72C1D22,  # SH    T4, 0x1D22 (T9)
    0x03200008,  # JR    T9
    # Make the Ice Trap model check branch properly
    0x24090125,  # ADDIU T1, R0, 0x0125
    0x15090003,  # BNE   T0, T1, [forward 0x03]
    0x3C0B3C19,  # LUI   T3, 0x3C19
    0x356B803F,  # ORI   T3, T3, 0x803F
    0xAF2B04D0,  # SW    T3, 0x04D0 (T9)
    0x03200008   # JR    T9
]

double_component_checker = [
    # When checking to see if a bomb component can be placed at a cracked wall, this will run if the code lands at the
    # "no need to set 2" outcome to see if the other can be set.

    # Mandragora checker
    0x10400007,  # BEQZ  V0,     [forward 0x07]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x31098000,  # ANDI  T1, T0, 0x8000
    0x15200008,  # BNEZ  T1,     [forward 0x08]
    0x91499C5D,  # LBU   T1, 0x9C5D (T2)
    0x11200006,  # BEQZ  T1, 0x80183938
    0x00000000,  # NOP
    0x10000007,  # B     [forward 0x07]
    0x31E90100,  # ANDI  T1, T7, 0x0100
    0x15200002,  # BNEZ  T1,     [forward 0x02]
    0x91499C5D,  # LBU   T1, 0x9C5D (T2)
    0x15200003,  # BNEZ  T1,     [forward 0x03]
    0x3C198000,  # LUI   T9, 0x8000
    0x27391590,  # ADDIU T9, T9, 0x1590
    0x03200008,  # JR    T9
    0x24090001,  # ADDIU T1, R0, 0x0001
    0xA4E9004C,  # SH    T1, 0x004C (A3)
    0x3C190E00,  # LUI   T9, 0x0E00
    0x273903E0,  # ADDIU T9, T9, 0x03E0
    0x03200008,  # JR    T9
    0x00000000,  # NOP
    # Nitro checker
    0x10400007,  # BEQZ  V0,     [forward 0x07]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x31694000,  # ANDI  T1, T3, 0x4000
    0x15200008,  # BNEZ  T1,     [forward 0x08]
    0x91499C5C,  # LBU   T1, 0x9C5C
    0x11200006,  # BEQZ  T1,     [forward 0x06]
    0x00000000,  # NOP
    0x1000FFF4,  # B     [backward 0x0B]
    0x914F9C18,  # LBU   T7, 0x9C18 (T2)
    0x31E90002,  # ANDI  T1, T7, 0x0002
    0x1520FFEC,  # BNEZ  T1,     [backward 0x13]
    0x91499C5C,  # LBU   T1, 0x9C5C (T2)
    0x1520FFEF,  # BNEZ  T1,     [backward 0x15]
    0x00000000,  # NOP
    0x1000FFE8,  # B             [backward 0x17]
    0x00000000,  # NOP
]

downstairs_seal_checker = [
    # This will run specifically for the downstairs crack to see if the seal has been removed before then deciding to
    # let the player set the bomb components or not. An anti-dick measure, since there is a limited number of each
    # component per world.
    0x14400004,  # BNEZ  V0,     [forward 0x04]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914A9C18,  # LBU   T2, 0x9C18 (T2)
    0x314A0001,  # ANDI  T2, T2, 0x0001
    0x11400003,  # BEQZ  T2,     [forward 0x03]
    0x3C198000,  # LUI   T9, 0x8000
    0x27391448,  # ADDIU T9, T9, 0x1448
    0x03200008,  # JR    T9
    0x3C190E00,  # LUI   T9, 0x0E00
    0x273902B4,  # ADDIU T9, T9, 0x02B4
    0x03200008,  # JR    T9
    0x00000000,  # NOP
]

map_data_modifiers = [
    # Overwrites the map data table on-the-fly after it loads and before the game reads it to load objects. Good for
    # changing anything that is part of a compression chain in the ROM data, including some freestanding item IDs.
    # Also jumps to the function that overwrites the "Restart this stage" data if entering through the back of a level.

    0x08006DAA,  # J	 0x8001B6A8
    0x00000000,  # NOP
    # Demo checker (if we're in a title demo, don't do any of this)
    0x3C028034,  # LUI   V0, 0x8034
    0x9449244A,  # LHU   T1, 0x244A (V0)
    0x11200002,  # BEQZ  T1,     [forward 0x02]
    # Zero checker (if there are zeroes in the word at 0x8034244A, where the entity list address is stored, don't do
    # any of this either)
    0x8C422B00,  # LW    V0, 0x2B00 (V0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    0x14400002,  # BNEZ  V0,     [forward 0x02]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x3C088039,  # LUI   T0, 0x8039
    0x91199EE3,  # LBU	 T9, 0x9EE3 (T0)
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    # Forest of Silence (replaces 1 invisible chicken)
    0x15000006,  # BNEZ  T0,     [forward 0x06]
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Werewolf plaque
    0xA44A01C8,  # SH    T2, 0x01C8 (V0)
    0x24090001,  # ADDIU T1, R0, 0x0001
    0x1139FFED,  # BEQ   T1, T9, [backward 0x12]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Villa front yard (replaces 1 moneybag and 2 beefs)
    0x24090003,  # ADDIU T1, R0, 0x0003
    0x15090008,  # BNE   T0, T1, [forward 0x08]
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Fountain FL
    0x340B0001,  # ORI   T3, R0, 0x0001         <- Fountain RL
    0x340C001F,  # ORI   T4, R0, 0x0001         <- Dog food gate
    0xA44A0058,  # SH    T2, 0x0058 (V0)
    0xA44B0038,  # SH    T3, 0x0038 (V0)
    0xA44C0068,  # SH    T4, 0x0068 (V0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Villa living area (Replaces 1 chicken, 1 knife, and 3 invisible Purifyings and assigns flags to the sub-weapons)
    0x24090005,  # ADDIU T1, R0, 0x0005
    0x15090025,  # BNE   T0, T1, [forward 0x25]
    0x340B0010,  # ORI   T3, R0, 0x0001         <- Hallway axe
    0xA44B00B8,  # SH    T3, 0x00B8 (V0)
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Storeroom R
    0x340B0010,  # ORI   T3, R0, 0x0001         <- Hallway knife
    0x340C0001,  # ORI   T4, R0, 0x0001         <- Living Room painting
    0x340D0001,  # ORI   T5, R0, 0x0001         <- Dining Room vase
    0x340E0001,  # ORI   T6, R0, 0x0001         <- Archives table
    0xA44A0078,  # SH    T2, 0x0078 (V0)
    0xA44B00C8,  # SH    T3, 0x00C8 (V0)
    0xA44C0108,  # SH    T4, 0x0108 (V0)
    0xA44D0128,  # SH    T5, 0x0128 (V0)
    0xA44E0138,  # SH    T6, 0x0138 (V0)
    0x340A0000,  # ORI   T2, R0, 0x0000         <- Sub-weapons left flag half
    0xA44A009C,  # SH    T2, 0x009C (V0)
    0xA44A00AC,  # SH    T2, 0x00AC (V0)
    0xA44A00BC,  # SH    T2, 0x00BC (V0)
    0xA44A00CC,  # SH    T2, 0x00CC (V0)
    0x340A0000,  # ORI   T2, R0, 0x0000         <- Sub-weapons right flag halves
    0x240B0000,  # ADDIU T3, R0, 0x0000
    0x240C0000,  # ADDIU T4, R0, 0x0000
    0x240D0000,  # ADDIU T5, R0, 0x0000
    0xA44A00CA,  # SH    T2, 0x00CA (V0)
    0xA44B00BA,  # SH    T3, 0x00BA (V0)
    0xA44C009A,  # SH    T4, 0x009A (V0)
    0xA44D00AA,  # SH    T5, 0x00AA (V0)
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Near bed
    0x340B0010,  # ORI   T3, R0, 0x0001         <- Storeroom L
    0x340C0001,  # ORI   T4, R0, 0x0001         <- Storeroom statue
    0x340D0001,  # ORI   T5, R0, 0x0001         <- Exit knight
    0x340E0001,  # ORI   T6, R0, 0x0001         <- Sitting room table
    0xA44A0048,  # SH    T2, 0x0078 (V0)
    0xA44B0088,  # SH    T3, 0x00C8 (V0)
    0xA44C00D8,  # SH    T4, 0x0108 (V0)
    0xA44D00F8,  # SH    T5, 0x0128 (V0)
    0xA44E0118,  # SH    T6, 0x0138 (V0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Tunnel (replaces 1 invisible Cure Ampoule)
    0x24090007,  # ADDIU T1, R0, 0x0007
    0x1509000A,  # BNE   T0, T1, [forward 0x0A]
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Twin arrow signs
    0xA44A0268,  # SH    T2, 0x0268 (V0)
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Bucket
    0xA44A0258,  # SH    T2, 0x0258 (V0)
    0x240B0005,  # ADDIU T3, R0, 0x0005
    0xA04B0150,  # SB    T3, 0x0150 (V0)
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x1139FFB0,  # BEQ   T1, T9, [backward 0x50]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Center factory floor (replaces 1 moneybag, 1 jewel, and gives every lizard man coffin item a unique flag)
    0x2409000B,  # ADDIU T1, R0, 0x000B
    0x15090016,  # BNE   T0, T1, [forward 0x16]
    0x340A001A,  # ORI   T2, R0, 0x001A         <- Lizard coffin nearside mid-right
    0x340B0003,  # ORI   T3, R0, 0x0003         <- Lizard coffin nearside mid-left
    0xA44A00C8,  # SH    T2, 0x00C8 (V0)
    0xA44B00D8,  # SH    T3, 0x00D8 (V0)
    0x240A1000,  # ADDIU T2, R0, 0x1000
    0x240B2000,  # ADDIU T3, R0, 0x2000
    0x240C0400,  # ADDIU T4, R0, 0x0400
    0x240D0800,  # ADDIU T5, R0, 0x0800
    0x240E0200,  # ADDIU T6, R0, 0x0200
    0x240F0100,  # ADDIU T7, R0, 0x0100
    0xA44A009A,  # SH    T2, 0x009A (V0)
    0xA44B00AA,  # SH    T3, 0x00AA (V0)
    0xA44C00CA,  # SH    T4, 0x00CA (V0)
    0xA44D00BA,  # SH    T5, 0x00BA (V0)
    0xA44E00DA,  # SH    T6, 0x00DA (V0)
    0xA44F00EA,  # SH    T7, 0x00EA (V0)
    0x340A0017,  # ORI   T2, R0, 0x0017         <- Lizard coffin nearside mid-right
    0x340B000C,  # ORI   T3, R0, 0x000C         <- Lizard coffin nearside mid-left
    0xA44A00A8,  # SH    T2, 0x00C8 (V0)
    0xA44B00E8,  # SH    T3, 0x00D8 (V0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Duel Tower (replaces a flame on top of a rotating lion pillar with a White Jewel on the invisible bridge ledge)
    0x24090013,  # ADDIU T1, R0, 0x0013
    0x1509000F,  # BNE   T0, T1, [forward 0x0F]
    0x3C0A00B9,  # LUI   T2, 0x00BB
    0x254A012B,  # ADDIU T2, T2, 0x012B
    0x3C0BFE2A,  # LUI   T3, 0xFE2A
    0x256B0027,  # ADDIU T3, T3, 0x0027
    0x3C0C0001,  # LUI   T4, 0x0001
    0x3C0D0022,  # LUI   T5, 0x0022
    0x25AD0100,  # ADDIU T5, T5, 0x0100
    0xAC4A0A80,  # SW    T2, 0x0AE0 (V0)
    0xAC4B0A84,  # SW    T3, 0x0AE4 (V0)
    0xAC4C0A88,  # SW    T4, 0x0AE8 (V0)
    0xAC4D0A8C,  # SW    T5, 0x0AEC (V0)
    0x24090001,  # ADDIU T1, R0, 0x0001
    0x1139FF87,  # BEQ   T1, T9, [backward 0x77]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Keep outside (replaces 1 invisible Healing Kit and gives both invisible Healing Kits pickup flags)
    0x24090014,  # ADDIU T1, R0, 0x0014
    0x1509000A,  # BNE   T0, T1, [forward 0x0A]
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Right flame
    0xA44A0058,  # SH    T2, 0x0058 (V0)
    0x240A0001,  # ADDIU T2, R0, 0x0001
    0x240B0002,  # ADDIU T3, R0, 0x0002
    0xA44A004A,  # SH    T2, 0x004A (V0)
    0xA44B005A,  # SH    T3, 0x005A (V0)
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x1139FF7B,  # BEQ   T0, T1, [backward 0x74]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Wall main area (sets a flag for the freestanding Holy Water if applicable and the "beginning of stage"
    # state if entered from the rear)
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x15090006,  # BNE   T0, T1, [forward 0x06]
    0x24090000,  # ADDIU T1, R0, 0x0000
    0xA049009B,  # SB    T1, 0x009B (V0)
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x1139FF73,  # BEQ   T1, T9, [backward 0x8D]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Villa vampire crypt (sets the "beginning of stage" state if entered from the rear, as well as the "can warp here"
    # flag if arriving for the first time)
    0x2409001A,  # ADDIU T1, R0, 0x001A
    0x15090008,  # BNE   T0, T1, [forward 0x08]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914B9C1C,  # LBU   T3, 0x9C1C (T2)
    0x356B0001,  # ORI   T3, T3, 0x0001
    0xA14B9C1C,  # SB    T3, 0x9C1C (T2)
    0x24090003,  # ADDIU T1, R0, 0x0003
    0x1139FF69,  # BEQ   T1, T9, [backward 0x98]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Underground Waterway (sets the "beginning of stage" state if entered from the rear)
    0x24090008,  # ADDIU T1, R0, 0x0008
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090001,  # ADDIU T1, R0, 0x0001
    0x1139FF63,  # BEQ   T1, T9, [backward 0x9F]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Center elevator top (sets the "beginning of stage" state if entered from either rear, as well as the "can
    # warp here" flag if arriving for the first time)
    0x2409000F,  # ADDIU T1, R0, 0x000F
    0x1509000A,  # BNE   T0, T1, [forward 0x0A]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914B9C1C,  # LBU   T3, 0x9C1C (T2)
    0x356B0002,  # ORI   T3, T3, 0x0002
    0xA14B9C1C,  # SB    T3, 0x9C1C (T2)
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x1139FF59,  # BEQ   T1, T9, [backward 0xAA]
    0x24090003,  # ADDIU T1, R0, 0x0003
    0x1139FF57,  # BEQ   T1, T9, [backward 0xAC]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Execution (sets the "beginning of stage" state if entered from the rear)
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x15090004,  # BNE   T0, T1, [forward 0x10]
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x1139FF51,  # BEQ   T1, T9, [backward 0xAF]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Sorcery (sets the "beginning of stage" state if entered from the rear)
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090013,  # ADDIU T1, R0, 0x0013
    0x1139FF4B,  # BEQ   T1, T9, [backward 0xBA]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Science (sets the "beginning of stage" state if entered from the rear)
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090004,  # ADDIU T1, R0, 0x0004
    0x1139FF45,  # BEQ   T1, T9, [backward 0xC1]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Room of Clocks (changes 2 candle settings if applicable and sets the "begging of stage" state if spawning at end)
    0x2409001B,  # ADDIU T1, R0, 0x001B
    0x15090008,  # BNE   T0, T1, [forward 0x08]
    0x24090006,  # ADDIU T1, R0, 0x0006
    0x240A0006,  # ADDIU T2, R0, 0x0006
    0xA0490059,  # SB    T1, 0x0059 (V0)
    0xA04A0069,  # SB    T2, 0x0069 (V0)
    0x24090014,  # ADDIU T1, R0, 0x0014
    0x1139FF3B,  # BEQ   T1, T9, [backward 0xCC]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Center basement (changes 2 non-pickup-able Mandragoras into 2 real items and moves the torture shelf item
    # forward slightly if it's turned visible)
    0x24090009,  # ADDIU T1, R0, 0x0009
    0x15090011,  # BNE   T0, T1, [forward 0x11]
    0x3409FFFC,  # ORI   T1, R0, 0xFFFC
    0xA44907C0,  # SH    T1, 0x07C0 (V0)
    0xA44907D0,  # SH    T1, 0x07D0 (V0)
    0x240A0027,  # ADDIU T2, R0, 0x0027
    0xA44A07C6,  # SH    T2, 0x07C6 (V0)
    0xA44A07D6,  # SH    T2, 0x07D6 (V0)
    0x340B0001,  # ORI   T3, R0, 0x0001      <- Right Mandragora
    0x340C0001,  # ORI   T4, R0, 0x0001      <- Left Mandragora
    0xA44B07C8,  # SH    T3, 0x07C8 (V0)
    0xA44C07D8,  # SH    T4, 0x07D8 (V0)
    0x240D00F5,  # ADDIU T5, R0, 0x00F5
    0xA04D06D1,  # SB    T5, 0x06D1 (V0)
    0x24090040,  # ADDIU T1, R0, 0x0040
    0x240A0080,  # ADDIU T2, R0, 0x0080
    0xA04907CA,  # SB    T1, 0x07CA (V0)
    0xA04A07DA,  # SB    T2, 0x07DA (V0)
    0x03E00008,  # JR    RA
    # Castle Center nitro area (changes 2 non-pickup-able Nitros into 2 real items)
    0x2409000E,  # ADDIU T1, R0, 0x000E
    0x15090015,  # BNE   T0, T1, [forward 0x15]
    0x240900C0,  # ADDIU T1, R0, 0x00C0
    0x240A00CE,  # ADDIU T2, R0, 0x00CE
    0xA0490471,  # SB    T1, 0x0471 (V0)
    0xA04A04A1,  # SB    T2, 0x04A1 (V0)
    0x24090027,  # ADDIU T1, R0, 0x0027
    0xA4490476,  # SH    T1, 0x0476 (V0)
    0xA44904A6,  # SH    T1, 0x04A6 (V0)
    0x340A0001,  # ORI   T2, R0, 0x0001      <- Invention-side shelf
    0x340B0001,  # ORI   T3, R0, 0x0001      <- Heinrich-side shelf
    0xA44A0478,  # SH    T2, 0x0478 (V0)
    0xA44B04A8,  # SH    T3, 0x04A8 (V0)
    0x24090080,  # ADDIU T1, R0, 0x0080
    0xA049047A,  # SB    T1, 0x047A (V0)
    0xA440047C,  # SH    R0, 0x047C (V0)
    0x240A0400,  # ADDIU T2, R0, 0x0400
    0x340BFF05,  # ORI   T3, R0, 0xFF05
    0xA44A04AA,  # SH    T2, 0x04AA (V0)
    0xA44B04AC,  # SH    T3, 0x04AC (V0)
    0x24090046,  # ADDIU T1, R0, 0x0046
    0xA04904A3,  # SB    T1, 0x04A3 (V0)
    0x03E00008,  # JR    RA
    # Fan meeting room (sets "beginning of stage" flag)
    0x24090019,  # ADDIU T1, R0, 0x0019
    0x1109FF0D,  # BEQ   T1, T9, [backward 0xFB]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
]

renon_cutscene_checker = [
    # Prevents Renon's departure/pre-fight cutscene from playing if the player is either in the escape sequence or both
    # did not spend the required 30K to fight him and lacks the required Special2s to fight Dracula.
    0x15810002,  # BNE   T4, AT, [forward 0x02]
    0x00000000,  # NOP
    0x08049EB3,  # J     0x80127ACC
    0x24090016,  # ADDIU T1, R0, 0x0016
    0x11C90002,  # BEQ   T6, T1, [forward 0x02]
    0x00000000,  # NOP
    0x08049ECA,  # J     0x80127B28
    0x24190000,  # ADDIU T9, R0, 0x0000
    0x8C696208,  # LW    T1, 0x6208 (V1)
    0x292A7531,  # SLTI  T2, T1, 0x7531
    0x51400001,  # BEQZL T2,     [forward 0x01]
    0x24190001,  # ADDIU T9, R0, 0x0001
    0x3C0B8013,  # LUI   T3, 0x8013
    0x916BAC9F,  # LBU   T3, 0xAC9F (T3)
    0x906C6194,  # LBU   T4, 0x6194 (V1)
    0x018B502A,  # SLT   T2, T4, T3
    0x51400001,  # BEQZL T2,     [forward 0x01]
    0x24190001,  # ADDIU T9, R0, 0x0001
    0x90696142,  # LBU   T1, 0x6142 (V1)
    0x31290002,  # ANDI  T1, T1, 0x0002
    0x55200001,  # BNEZL T1,     [forward 0x01]
    0x24190000,  # ADDIU T9, R0, 0x0000
    0x17200003,  # BNEZ  T9,     [forward 0x03]
    0x00000000,  # NOP
    0x08049ECC,  # J     0x80127B30
    0x00000000,  # NOP
    0x08049ECA   # J     0x80127B28
]

renon_cutscene_checker_jr = [
    # Like renon_cutscene_checker, but without the checks for the Special2 and spent money counters. Inserted instead if
    # the player chooses to guarantee or disable the Renon fight on their YAML.
    0x15810002,  # BNE   T4, AT, [forward 0x02]
    0x00000000,  # NOP
    0x08049EB3,  # J     0x80127ACC
    0x24090016,  # ADDIU T1, R0, 0x0016
    0x11C90002,  # BEQ   T6, T1, [forward 0x02]
    0x00000000,  # NOP
    0x08049ECA,  # J     0x80127B28
    0x24190001,  # ADDIU T9, R0, 0x0001
    0x90696142,  # LBU   T1, 0x6142 (V1)
    0x31290002,  # ANDI  T1, T1, 0x0002
    0x55200001,  # BNEZL T1,     [forward 0x01]
    0x24190000,  # ADDIU T9, R0, 0x0000
    0x17200003,  # BNEZ  T9,     [forward 0x03]
    0x00000000,  # NOP
    0x08049ECC,  # J     0x80127B30
    0x00000000,  # NOP
    0x08049ECA   # J     0x80127B28
]

ck_door_music_player = [
    # Plays Castle Keep's song if you spawn in front of Dracula's door (teleporting via the warp menu) and haven't
    # started the escape sequence yet.
    0x17010002,  # BNE   T8, AT, [forward 0x02]
    0x00000000,  # NOP
    0x08063DF9,  # J     0x8018F7E4
    0x240A0000,  # ADDIU T2, R0, 0x0000
    0x3C088039,  # LUI   T0, 0x8039
    0x91089BFA,  # LBU   T0, 0x9BFA (T0)
    0x31080002,  # ANDI  T0, T0, 0x0002
    0x51090001,  # BEQL  T0, T1, [forward 0x01]
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x24080003,  # ADDIU T0, R0, 0x0003
    0x51180001,  # BEQL  T0, T8, [forward 0x01]
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x240B0002,  # ADDIU T3, R0, 0x0002
    0x114B0002,  # BEQ   T2, T3, [forward 0x02]
    0x00000000,  # NOP
    0x08063DFD,  # J     0x8018F7F4
    0x00000000,  # NOP
    0x08063DF9   # J     0x8018F7E4
]

dracula_door_text_redirector = [
    # Switches the standard pointer to the map text with one to a custom message for Dracula's chamber door if the
    # current scene is Castle Keep exterior (Scene 0x14).
    0x3C088039,  # LUI   T0, 0x8039
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    0x24090014,  # ADDIU T1, R0, 0x0014
    0x15090006,  # BNE   T0, T1, [forward 0x06]
    0x3C088014,  # LUI   T0, 0x8014
    0x2508B9F4,  # ADDIU T0, T0, 0xB9F4
    0x151F0003,  # BNE   T0, RA, [forward 0x03]
    0x00000000,  # NOP
    0x3C028040,  # LUI   V0, 0x8040
    0x2442CC48,  # ADDIU V0, V0, 0xCC48
    0x03E00008   # JR    RA
]

coffin_time_checker = [
    # When entering the Villa coffin, this will check to see whether it's day or night and send you to either the Tunnel
    # or Underground Waterway level slot accordingly regardless of which character you are
    0x28490006,  # SLTI  T1, V0, 0x0006
    0x15200005,  # BNEZ  T1,     [forward 0x05]
    0x28490012,  # SLTI  T1, V0, 0x0012
    0x11200003,  # BEQZ  T1,     [forward 0x03]
    0x00000000,  # NOP
    0x08055AEB,  # J     0x80156BAC
    0x00000000,  # NOP
    0x08055AED   # J     0x80156BB4
]

werebull_flag_unsetter = [
    # This will un-set Were-bull's defeat flag in Duel Tower after beating him so that the check above his arena can
    # still be acquired later, if it hasn't been acquired already. This is the only check in the entire game that can be
    # permanently missed even with the ability to return to levels.
    0x3C0E0400,  # LUI   T6, 0x0400
    0x15CF0006,  # BNE   T6, T7, [forward 0x06]
    0x00187402,  # SRL   T6, T8, 16
    0x31CE2000,  # ANDI  T6, T6, 0x2000
    0x15C00003,  # BNEZ  T6,     [forward 0x03]
    0x3C0E0020,  # LUI   T6, 0x0020
    0x014E5025,  # OR    T2, T2, T6
    0xAC4A613C,  # SW    T2, 0x613C (V0)
    0x03200008   # JR    T9
]

werebull_flag_unsetter_special2_electric_boogaloo = [
    # Like werebull_flag_unsetter, but with the added feature of awarding a Special2 after determining the player isn't
    # trying to beat Were-bull twice! This will be inserted over the former if the goal is set to boss hunt.
    0x3C0E0400,  # LUI   T6, 0x0400
    0x15CF0008,  # BNE   T6, T7, [forward 0x06]
    0x00187402,  # SRL   T6, T8, 16
    0x31CE2000,  # ANDI  T6, T6, 0x2000
    0x15C00005,  # BNEZ  T6,     [forward 0x05]
    0x3C0E0020,  # LUI   T6, 0x0020
    0x014EC024,  # AND   T8, T2, T6
    0x014E5025,  # OR    T2, T2, T6
    0xAC4A613C,  # SW    T2, 0x613C (V0)
    0x17000003,  # BNEZ  T8,     [forward 0x03]
    0x3C188039,  # LUI   T8, 0x8039
    0x240E0005,  # ADDIU T6, R0, 0x0005
    0xA30E9BDF,  # SB    T6, 0x9BDF (T8)
    0x03200008   # JR    T9
]

werebull_flag_pickup_setter = [
    # Checks to see if an item being picked up is the one on top of Were-bull's arena. If it is, then it'll check to see
    # if our makeshift "Were-bull defeated once" flag and, if it is, set Were-bull's arena flag proper, so it'll
    # permanently stay down.
    0x3C088038,  # LUI   T0, 0x8038
    0x25083AC8,  # ADDIU T0, T0, 0x3AC8
    0x15020007,  # BNE   T0, V0, [forward 0x07]
    0x3C082000,  # LUI   T0, 0x2000
    0x15040005,  # BNE   T0, A0, [forward 0x05]
    0x9449612C,  # LHU   T1, 0x612C (V0)
    0x31290020,  # ANDI  T1, T1, 0x0020
    0x11200002,  # BEQZ  T1,     [forward 0x02]
    0x3C0A0400,  # LUI   T2, 0x0400
    0x014D6825,  # OR    T5, T2, T5
    0xAC4D612C,  # SW    T5, 0x612C (V0)
    0x03E00008   # JR    RA
]

boss_special2_giver = [
    # Enables the rewarding of Special2s upon the vanishing of a boss's health bar when defeating it.

    # Also sets a flag in the case of the Castle Wall White Dragons' health bar going away. Their defeat flag in vanilla
    # is tied to hitting the lever after killing them, so this alternate flag is used to track them for the "All Bosses"
    # goal in the event someone kills them and then warps out opting to not be a Konami pachinko champ.
    0x3C118035,  # LUI   S1, 0x8035
    0x962DF834,  # LHU   T5, 0xF834 (S1)
    0x240E3F73,  # ADDIU T6, R0, 0x3F73
    0x15AE0012,  # BNE   T5, T6, [forward 0x12]
    0x3C118039,  # LUI   S1, 0x8039
    0x922D9EE1,  # LBU   T5, 0x9EE1 (S1)
    0x240E0013,  # ADDIU T6, R0, 0x0013
    0x11AE000E,  # BEQ   T5, T6, [forward 0x0E]
    0x922F9BFA,  # LBU   T7, 0x9BFA (S1)
    0x31EF0001,  # ANDI  T7, T7, 0x0001
    0x15E0000B,  # BNEZ  T7,     [forward 0x0B]
    0x240E0002,  # ADDIU T6, R0, 0x0002
    0x15AE0006,  # BNE   T5, T6, [forward 0x06]
    0x00000000,  # NOP
    0x862F9BF4,  # LH    T7, 0x9BF4 (S1)
    0x31ED0080,  # ANDI  T5, T7, 0x0080
    0x15A00005,  # BNEZ  T5,     [forward 0x05]
    0x35EF0080,  # ORI   T7, T7, 0x0080
    0xA62F9BF4,  # SH    T7, 0x9BF4 (S1)
    0x240D0005,  # ADDIU T5, R0, 0x0005
    0xA22D9BDF,  # SB    T5, 0x9BDF (S1)
    0xA22D9BE0,  # SB    T5, 0x9BE0 (S1)
    0x03E00008   # JR    RA
]

boss_goal_checker = [
    # Checks each boss flag to see if every boss with a health meter has been defeated and puts 0x0004 in V0 to
    # disallow opening Dracula's door if not all have been.
    0x3C0A8039,  # LUI   T2, 0x8039
    0x954B9BF4,  # LHU   T3, 0x9BF4 (T2)
    0x316D0BA0,  # ANDI  T5, T3, 0x0BA0
    0x914B9BFB,  # LBU   T3, 0x9BFB (T2)
    0x000B6182,  # SRL   T4, T3, 6
    0x11800010,  # BEQZ  T4,     [forward 0x10]
    0x240C00C0,  # ADDIU T4, R0, 0x00C0
    0x01AC6821,  # ADDU  T5, T5, T4
    0x914B9BFD,  # LBU   T3, 0x9BFD (T2)
    0x316C0020,  # ANDI  T4, T3, 0x0020
    0x01AC6821,  # ADDU  T5, T5, T4
    0x914B9BFE,  # LBU   T3, 0x9BFE (T2)
    0x316C0010,  # ANDI  T4, T3, 0x0010
    0x01AC6821,  # ADDU  T5, T5, T4
    0x914B9C18,  # LBU   T3, 0x9C18 (T2)
    0x316C0010,  # ANDI  T4, T3, 0x0010
    0x01AC6821,  # ADDU  T5, T5, T4
    0x914B9C1B,  # LBU   T3, 0x9C1B (T2)
    0x000B6102,  # SRL   T4, T3, 4
    0x11800005,  # BEQZ  T4,     [forward 0x05]
    0x240C0050,  # ADDIU T4, R0, 0x0050
    0x01AC6821,  # ADDU  T5, T5, T4
    0x240E0CF0,  # ADDIU T6, R0, 0x0CF0
    0x55CD0001,  # BNEL  T6, T5, [forward 0x01]
    0x24020004,  # ADDIU V0, R0, 0x0004
    0x03E00008   # JR    RA
]

special_goal_checker = [
    # Checks the Special2 counter to see if the specified threshold has been reached and puts 0x0001 in V0 to disallow
    # opening Dracula's door if it hasn't been.
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914B9C4C,  # LBU   T3, 0x9C4C (T2)
    0x296A001E,  # SLTI  T2, T3, 0x001E
    0x55400001,  # BNEZL T2, 0x8012AC8C
    0x24020001,  # ADDIU V0, R0, 0x0001
    0x03E00008   # JR    RA
]

warp_menu_rewrite = [
    # Rewrite to the warp menu code to ensure each option can have its own scene ID, spawn ID, and fade color.
    # Start Warp
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x1000001F,  # B         [forward 0x1F]
    0x3C0F8000,  # LUI   T7, 0x8000
    # Warp 1
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x1000001B,  # B         [forward 0x1B]
    0x3C0F8040,  # LUI   T7, 0x8040
    # Warp 2
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x10000017,  # B         [forward 0x17]
    0x3C0F8080,  # LUI   T7, 0x8080
    # Warp 3
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x10000013,  # B         [forward 0x13]
    0x3C0F0080,  # LUI   T7, 0x0080
    # Warp 4
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x3C0F0080,  # LUI   T7, 0x0080
    0x1000000E,  # B         [forward 0x0E]
    0x25EF8000,  # ADDIU T7, T7, 0x8000
    # Warp 5
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x1000000A,  # B         [forward 0x0A]
    0x340F8000,  # ORI   T7, R0, 0x8000
    # Warp 6
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x3C0F8000,  # LUI   T7, 0x8000
    0x10000005,  # B         [forward 0x05]
    0x35EF8000,  # ORI   T7, T7, 0x8000
    # Warp 7
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x3C0F8040,  # LUI   T7, 0x8040
    0x35EF8000,  # ORI   T7, T7, 0x8000
    # Warp Crypt
    0x3C18800D,  # LUI   T8, 0x800D
    0x97185E20,  # LHU   T8, 0x5E20 (T8)
    0x24192000,  # ADDIU T9, R0, 0x2000
    0x17190009,  # BNE   T8, T9, [forward 0x09]
    0x3C088039,  # LUI   T0, 0x8039
    0x91089C1C,  # LBU   T0, 0x9C1C (T0)
    0x31080001,  # ANDI  T0, T0, 0x0001
    0x1100000F,  # BEQZ  T0,     [forward 0x0F]
    0x00000000,  # NOP
    0x3C0E001A,  # LUI   T6, 0x001A
    0x25CE0003,  # ADDIU T6, T6, 0x0003
    0x1000000B,  # B     [forward 0x0B]
    0x240F0000,  # ADDIU T7, R0, 0x0000
    # Warp Elevator
    0x24190010,  # ADDIU T9, R0, 0x0010
    0x17190008,  # BNE   T8, T9, [forward 0x08]
    0x91089C1C,  # LBU   T0, 0x9C1C (T0)
    0x31080002,  # ANDI  T0, T0, 0x0002
    0x11000005,  # BEQZ  T0,     [forward 0x05]
    0x00000000,  # NOP
    0x3C0E000F,  # LUI   T6, 0x000F
    0x25CE0001,  # ADDIU T6, T6, 0x0001
    0x3C0F8080,  # LUI   T7, 0x8080
    0x35EF8000,  # ORI   T7, T7, 0x8000
    # All
    0xAC6E6428,  # SW    T6, 0x6428 (V1)
    0xAC6F642C,  # SW    T7, 0x642C (V1)
    0x2402001E,  # ADDIU V0, R0, 0x001E
    0xA4626430,  # SH	 V0, 0x6430 (V1)
    0xA4626432,  # SH	 V0, 0x6432 (V1)
]

warp_pointer_table = [
    # Changed pointer table addresses to go with the warp menu rewrite
    0x8012AD74,
    0x8012AD84,
    0x8012AD94,
    0x8012ADA4,
    0x8012ADB4,
    0x8012ADC8,
    0x8012ADD8,
    0x8012ADEC,
]

spawn_coordinates_extension = [
    # Checks if the 0x10 bit is set in the spawn ID and references the below list of custom spawn coordinates if it is.
    0x316A0010,  # ANDI  T2, T3, 0x0010
    0x11400003,  # BEQZ  T2,     [forward 0x03]
    0x8CD90008,  # LW    T9, 0x0008 (A2)
    0x3C198040,  # LUI   T9, 0x8040
    0x2739C2CC,  # ADDIU T9, T9, 0xC2CC
    0x08054A83,  # J 0x80152A0C
    0x00000000,  # NOP
    0x00000000,  # NOP

    # Castle Wall end: 10
    #     player    camera    focus point
    # x = 0xFFFF    0xFFFF    0xFFFF
    # y = 0x0003    0x0012    0x000D
    # z = 0xFFF3    0xEDFF    0xFFF3
    # r = 0xC000
    0x0000FFFF,
    0x0003FFF3,
    0xC000FFFF,
    0x0012FFED,
    0xFFFF000D,
    0xFFF30000,

    # Tunnel end: 11
    #     player    camera    focus point
    # x = 0x0088    0x0087    0x0088
    # y = 0x01D6    0x01F1    0x01E5
    # z = 0xF803    0xF7D2    0xF803
    # r = 0xC000
    0x008801D6,
    0xF803C000,
    0x008701F1,
    0xF7D20088,
    0x01E5F803,

    # Tower of Execution end: 12
    #     player    camera    focus point
    # x = 0x00AC    0x00EC    0x00AC
    # y = 0x0154    0x0183    0x0160
    # z = 0xFE8F    0xFE8F    0xFE8F
    # r = 0x8000
    0x000000AC,
    0x0154FE8F,
    0x800000EC,
    0x0183FE8F,
    0x00AC0160,
    0xFE8F0000,

    # Tower of Sorcery end: 13
    #     player    camera    focus point
    # x = 0xFEB0    0xFE60    0xFEB0
    # y = 0x0348    0x036D    0x0358
    # z = 0xFEFB    0xFEFB    0xFEFB
    # r = 0x0000
    0xFEB00348,
    0xFEFB0000,
    0xFE60036D,
    0xFEFBFEB0,
    0x0358FEFB,

    # Room of Clocks end: 14
    #     player    camera    focus point
    # x = 0x01B1    0x01BE    0x01B1
    # y = 0x0006    0x001B    0x0015
    # z = 0xFFCD    0xFFCD    0xFFCD
    # r = 0x8000
    0x000001B1,
    0x0006FFCD,
    0x800001BE,
    0x001BFFCD,
    0x01B10015,
    0xFFCD0000,

    # Duel Tower savepoint: 15
    #     player    camera    focus point
    # x = 0x00B9    0x00B9    0x00B9
    # y = 0x012B    0x0150    0x0138
    # z = 0xFE20    0xFE92    0xFE20
    # r = 0xC000
    0x00B9012B,
    0xFE20C000,
    0x00B90150,
    0xFE9200B9,
    0x0138FE20
]

waterway_end_coordinates = [
    # Underground Waterway end: 01
    #     player    camera    focus point
    # x = 0x0397    0x03A1    0x0397
    # y = 0xFFC4    0xFFDC    0xFFD3
    # z = 0xFDB9    0xFDB8    0xFDB9
    # r = 0x8000
    0x00000397,
    0xFFC4FDB9,
    0x800003A1,
    0xFFDCFDB8,
    0x0397FFD3,
    0xFDB90000
]

continue_cursor_start_checker = [
    # This is used to improve the Game Over screen's "Continue" menu by starting the cursor on whichever checkpoint
    # is most recent instead of always on "Previously saved". If a menu has a cursor start value of 0xFF in its text
    # data, this will read the byte at 0x80389BC0 to determine which option to start the cursor on.
    0x8208001C,  # LB    T0, 0x001C(S0)
    0x05010003,  # BGEZ  T0,     [forward 0x03]
    0x3C098039,  # LUI   T1, 0x8039
    0x81289BC0,  # LB    T0, 0x9BC0 (T1)
    0xA208001C,  # SB    T0, 0x001C (S0)
    0x03E00008   # JR    RA
]

savepoint_cursor_updater = [
    # Sets the value at 0x80389BC0 to 0x00 after saving to let the Game Over screen's "Continue" menu know to start the
    # cursor on "Previously saved" as well as updates the entrance variable for B warping. It then jumps to
    # deathlink_counter_decrementer in the event we're loading a save from the Game Over screen.
    0x3C088039,  # LUI    T0, 0x8039
    0x91099C95,  # LBU    T1, 0x9C95 (T0)
    0x000948C0,  # SLL    T1, T1, 3
    0x3C0A8018,  # LUI    T2, 0x8018
    0x01495021,  # ADDU   T2, T2, T1
    0x914B17CF,  # LBU    T3, 0x17CF (T2)
    0xA10B9EE3,  # SB     T3, 0x9EE3 (T0)
    0xA1009BC0,  # SB     R0, 0x9BC0 (T0)
    0x080FF8F0   # J 0x803FE3C0
]

stage_start_cursor_updater = [
    # Sets the value at 0x80389BC0 to 0x01 after entering a stage to let the Game Over screen's "Continue" menu know to
    # start the cursor on "Restart this stage".
    0x3C088039,  # LUI    T0, 0x8039
    0x24090001,  # ADDIU  T1, R0, 0x0001
    0xA1099BC0,  # SB     T1, 0x9BC0 (T0)
    0x03E00008   # JR     RA
]

elevator_flag_checker = [
    # Prevents the top elevator in Castle Center from activating if the bottom elevator switch is not turned on.
    0x3C088039,  # LUI   T0, 0x8039
    0x91089C07,  # LBU   T0, 0x9C07 (T0)
    0x31080002,  # ANDI  T0, T0, 0x0002
    0x15000002,  # BNEZ  T0,     [forward 0x02]
    0x848E004C,  # LH    T6, 0x004C (A0)
    0x240E0000,  # ADDIU T6, R0, 0x0000
    0x03E00008   # JR    RA
]

crystal_special2_giver = [
    # Gives a Special2 upon activating the big crystal in CC basement.
    0x3C098039,  # LUI   T1, 0x8039
    0x24190005,  # ADDIU T9, R0, 0x0005
    0xA1399BDF,  # SB    T9, 0x9BDF (T1)
    0x03E00008,  # JR    RA
    0x3C198000   # LUI   T9, 0x8000
]

boss_save_stopper = [
    # Prevents usage of a White Jewel if in a boss fight. Important for the lizard-man trio in Waterway as escaping
    # their fight by saving/reloading can render a Special2 permanently missable.
    0x24080001,  # ADDIU T0, R0, 0x0001
    0x15030005,  # BNE   T0, V1, [forward 0x05]
    0x3C088035,  # LUI   T0, 0x8035
    0x9108F7D8,  # LBU   T0, 0xF7D8 (T0)
    0x24090020,  # ADDIU T1, R0, 0x0020
    0x51090001,  # BEQL  T0, T1, [forward 0x01]
    0x24020000,  # ADDIU V0, R0, 0x0000
    0x03E00008   # JR    RA
]

music_modifier = [
    # Uses the ID of a song about to be played to pull a switcheroo by grabbing a new ID from a custom table to play
    # instead. A hacky way to circumvent song IDs in the compressed overlays' "play song" function calls, but it works!
    0xAFBF001C,  # SW    RA, 0x001C (SP)
    0x0C004A6B,  # JAL   0x800129AC
    0x44800000,  # MTC1  R0, F0
    0x10400003,  # BEQZ  V0,     [forward 0x03]
    0x3C088040,  # LUI   T0, 0x8040
    0x01044821,  # ADDU  T1, T0, A0
    0x9124CD20,  # LBU   A0, 0xCD20 (T1)
    0x08004E64   # J     0x80013990
]

music_comparer_modifier = [
    # The same as music_modifier, but for the function that compares the "song to play" ID with the one that's currently
    # playing. This will ensure the randomized music doesn't reset when going through a loading zone in Villa or CC.
    0x3C088040,  # LUI   T0, 0x8040
    0x01044821,  # ADDU  T1, T0, A0
    0x9124CD20,  # LBU   A0, 0xCD20 (T1)
    0x08004A60,  # J     0x80012980
]

item_customizer = [
    # Allows changing an item's appearance settings and visibility independent of what it actually is as well as setting
    # its bitflag literally anywhere in the save file by changing things in the item actor's data as it's being created
    # for the below three functions to then utilize.
    0x03205825,  # OR    T3, T9, R0
    0x000B5A02,  # SRL   T3, T3, 8
    0x316C0080,  # ANDI  T4, T3, 0x0080
    0xA0CC0041,  # SB    T4, 0x0041 (A2)
    0x016C5823,  # SUBU  T3, T3, T4
    0xA0CB0040,  # SB    T3, 0x0040 (A2)
    0x333900FF,  # ANDI  T9, T9, 0x00FF
    0xA4D90038,  # SH    T9, 0x0038 (A2)
    0x8CCD0058,  # LW    T5, 0x0058 (A2)
    0x31ACFF00,  # ANDI  T4, T5, 0xFF00
    0x340EFF00,  # ORI   T6, R0, 0xFF00
    0x158E000A,  # BNE   T4, T6, [forward 0x0A]
    0x31AC00FF,  # ANDI  T4, T5, 0x00FF
    0x240E0002,  # ADDIU T6, R0, 0x0002
    0x018E001B,  # DIVU  T4, T6
    0x00006010,  # MFHI  T4
    0x000D5C02,  # SRL   T3, T5, 16
    0x51800001,  # BEQZL T4,     [forward 0x01]
    0x000B5C00,  # SLL   T3, T3, 16
    0x00006012,  # MFLO  T4
    0xA0CC0055,  # SB    T4, 0x0055 (A2)
    0xACCB0058,  # SW    T3, 0x0058 (A2)
    0x080494E5,  # J     0x80125394
    0x032A0019   # MULTU T9, T2
]

item_appearance_switcher = [
    # Determines an item's model appearance by checking to see if a different item appearance ID was written in a
    # specific spot in the actor's data; if one wasn't, then the appearance value will be grabbed from the item's entry
    # in the item property table like normal instead.
    0x92080040,  # LBU   T0, 0x0040 (S0)
    0x55000001,  # BNEZL T0, T1, [forward 0x01]
    0x01002025,  # OR    A0, T0, R0
    0x03E00008,  # JR    RA
    0xAFA70024   # SW    A3, 0x0024 (SP)
]

item_model_visibility_switcher = [
    # If 80 is written one byte ahead of the appearance switch value in the item's actor data, parse 0C00 to the
    # function that checks if an item should be invisible or not. Otherwise, grab that setting from the item property
    # table like normal.
    0x920B0041,  # LBU   T3, 0x0041 (S0)
    0x316E0080,  # ANDI  T6, T3, 0x0080
    0x11C00003,  # BEQZ  T6,     [forward 0x03]
    0x240D0C00,  # ADDIU T5, R0, 0x0C00
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x958D0004   # LHU   T5, 0x0004 (T4)
]

item_shine_visibility_switcher = [
    # Same as the above, but for item shines instead of the model.
    0x920B0041,  # LBU   T3, 0x0041 (S0)
    0x31690080,  # ANDI  T1, T3, 0x0080
    0x11200003,  # BEQZ  T1,     [forward 0x03]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x240C0C00,  # ADDIU T4, R0, 0x0C00
    0x03E00008,  # JR    RA
    0x958CA908   # LHU   T4, 0xA908 (T4)
]

three_hit_item_flags_setter = [
    # As the function to create items from the 3HB item lists iterates through said item lists, this will pass unique
    # flag values to each item when calling the "create item instance" function by right-shifting said flag by a number
    # of bits depending on which item in the list it is. Unlike the vanilla game which always puts flags of 0x00000000
    # on each of these.
    0x8DC80008,  # LW    T0, 0x0008 (T6)
    0x240A0000,  # ADDIU T2, R0, 0x0000
    0x00084C02,  # SRL   T1, T0, 16
    0x3108FFFF,  # ANDI  T0, T0, 0xFFFF
    0x00094842,  # SRL   T1, T1, 1
    0x15200003,  # BNEZ  T1,     [forward 0x03]
    0x00000000,  # NOP
    0x34098000,  # ORI   T1, R0, 0x8000
    0x25080001,  # ADDIU T0, T0, 0x0001
    0x0154582A,  # SLT   T3, T2, S4
    0x1560FFF9,  # BNEZ  T3,     [backward 0x07]
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x00094C00,  # SLL   T1, T1, 16
    0x01094025,  # OR    T0, T0, T1
    0x0805971E,  # J     0x80165C78
    0xAFA80010   # SW    T0, 0x0010 (SP)
]

chandelier_item_flags_setter = [
    # Same as the above, but for the unique function made specifically and ONLY for the Villa foyer chandelier's item
    # list. KCEK, why the heck did you have to do this!?
    0x8F280014,  # LW    T0, 0x0014 (T9)
    0x240A0000,  # ADDIU T2, R0, 0x0000
    0x00084C02,  # SRL   T1, T0, 16
    0x3108FFFF,  # ANDI  T0, T0, 0xFFFF
    0x00094842,  # SRL   T1, T1, 1
    0x15200003,  # BNEZ  T1,     [forward 0x03]
    0x00000000,  # NOP
    0x34098000,  # ORI   T1, R0, 0x8000
    0x25080001,  # ADDIU T0, T0, 0x0001
    0x0155582A,  # SLT   T3, T2, S5
    0x1560FFF9,  # BNEZ  T3,     [backward 0x07]
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x00094C00,  # SLL   T1, T1, 16
    0x01094025,  # OR    T0, T0, T1
    0x0805971E,  # J     0x80165C78
    0xAFA80010   # SW    T0, 0x0010 (SP)
]

prev_subweapon_spawn_checker = [
    # When picking up a sub-weapon this will check to see if it's different from the one the player already had (if they
    # did have one) and jump to prev_subweapon_dropper, which will spawn a subweapon actor of what they had before
    # directly behind them.
    0x322F3031,  # Previous sub-weapon bytes
    0x10A00009,  # BEQZ  A1,     [forward 0x09]
    0x00000000,  # NOP
    0x10AD0007,  # BEQ   A1, T5, [forward 0x07]
    0x3C088040,  # LUI   T0, 0x8040
    0x01054021,  # ADDU  T0, T0, A1
    0x0C0FF418,  # JAL   0x803FD060
    0x9104CFC3,  # LBU   A0, 0xCFC3 (T0)
    0x2484FF9C,  # ADDIU A0, A0, 0xFF9C
    0x3C088039,  # LUI   T0, 0x8039
    0xAD049BD4,  # SW    A0, 0x9BD4 (T0)
    0x0804F0BF,  # J     0x8013C2FC
    0x24020001   # ADDIU V0, R0, 0x0001
]

prev_subweapon_fall_checker = [
    # Checks to see if a pointer to a previous sub-weapon drop actor spawned by prev_subweapon_dropper is in 80389BD4
    # and calls the function in prev_subweapon_dropper to lower the weapon closer to the ground on the next frame if a
    # pointer exists and its actor ID is 0x0027. Once it hits the ground or despawns, the connection to the actor will
    # be severed by 0-ing out the pointer.
    0x3C088039,  # LUI   T0, 0x8039
    0x8D049BD4,  # LW    A0, 0x9BD4 (T0)
    0x10800008,  # BEQZ  A0,     [forward 0x08]
    0x00000000,  # NOP
    0x84890000,  # LH    T1, 0x0000 (A0)
    0x240A0027,  # ADDIU T2, R0, 0x0027
    0x152A0004,  # BNE   T1, T2, [forward 0x04]
    0x00000000,  # NOP
    0x0C0FF452,  # JAL   0x803FD148
    0x00000000,  # NOP
    0x50400001,  # BEQZL V0,     [forward 0x01]
    0xAD009BD4,  # SW    R0, 0x9BD4 (T0)
    0x080FF40F   # J     0x803FD03C
]

prev_subweapon_dropper = [
    # Spawns a pickup actor of the sub-weapon the player had before picking up a new one behind them at their current
    # position like in other CVs. This will enable them to pick it back up again if they still want it.
    # Courtesy of Moisés; see derp.c in the src folder for the C source code.
    0x27BDFFC8,
    0xAFBF001C,
    0xAFA40038,
    0xAFB00018,
    0x0C0006B4,
    0x2404016C,
    0x00402025,
    0x0C000660,
    0x24050027,
    0x1040002B,
    0x00408025,
    0x3C048035,
    0x848409DE,
    0x00042023,
    0x0C0230D4,
    0x3084FFFF,
    0x44822000,
    0x3C018040,
    0xC428D370,
    0x468021A0,
    0x3C048035,
    0x848409DE,
    0x00042023,
    0x46083282,
    0x3084FFFF,
    0x0C01FFAC,
    0xE7AA0024,
    0x44828000,
    0x3C018040,
    0xC424D374,
    0x468084A0,
    0x27A40024,
    0x00802825,
    0x3C064100,
    0x46049182,
    0x0C004562,
    0xE7A6002C,
    0x3C058035,
    0x24A509D0,
    0x26040064,
    0x0C004530,
    0x27A60024,
    0x3C018035,
    0xC42809D4,
    0x3C0140A0,
    0x44815000,
    0x00000000,
    0x460A4400,
    0xE6100068,
    0xC6120068,
    0xE6120034,
    0x8FAE0038,
    0xA60E0038,
    0x8FBF001C,
    0x8FB00018,
    0x27BD0038,
    0x03E00008,
    0x00000000,
    0x3C068040,
    0x24C6D368,
    0x90CE0000,
    0x27BDFFE8,
    0xAFBF0014,
    0x15C00027,
    0x00802825,
    0x240400DB,
    0x0C0006B4,
    0xAFA50018,
    0x44802000,
    0x3C038040,
    0x2463D364,
    0x3C068040,
    0x24C6D368,
    0x8FA50018,
    0x1040000A,
    0xE4640000,
    0x8C4F0024,
    0x3C013F80,
    0x44814000,
    0xC5E60044,
    0xC4700000,
    0x3C018040,
    0x46083280,
    0x460A8480,
    0xE432D364,
    0x94A20038,
    0x2401000F,
    0x24180001,
    0x10410006,
    0x24010010,
    0x10410004,
    0x2401002F,
    0x10410002,
    0x24010030,
    0x14410005,
    0x3C014040,
    0x44813000,
    0xC4640000,
    0x46062200,
    0xE4680000,
    0xA0D80000,
    0x10000023,
    0x24020001,
    0x3C038040,
    0x2463D364,
    0xC4600000,
    0xC4A20068,
    0x3C038039,
    0x24639BD0,
    0x4600103E,
    0x00001025,
    0x45000006,
    0x00000000,
    0x44808000,
    0xE4A00068,
    0xA0C00000,
    0x10000014,
    0xE4700000,
    0x3C038039,
    0x24639BD0,
    0x3C018019,
    0xC42AC870,
    0xC4600000,
    0x460A003C,
    0x00000000,
    0x45000006,
    0x3C018019,
    0xC432C878,
    0x46120100,
    0xE4640000,
    0xC4600000,
    0xC4A20068,
    0x46001181,
    0x24020001,
    0xE4A60068,
    0xC4A80068,
    0xE4A80034,
    0x8FBF0014,
    0x27BD0018,
    0x03E00008,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x0000001B,
    0x060048E0,
    0x40000000,
    0x06AEFFD3,
    0x06004B30,
    0x40000000,
    0x00000000,
    0x06004CB8,
    0x0000031A,
    0x002C0000,
    0x060059B8,
    0x40000248,
    0xFFB50186,
    0x06005B68,
    0xC00001DF,
    0x00000000,
    0x06005C88,
    0x80000149,
    0x00000000,
    0x06005DC0,
    0xC0000248,
    0xFFB5FE7B,
    0x06005F70,
    0xC00001E0,
    0x00000000,
    0x06006090,
    0x8000014A,
    0x00000000,
    0x06007D28,
    0x4000010E,
    0xFFF100A5,
    0x06007F60,
    0xC0000275,
    0x00000000,
    0x06008208,
    0x800002B2,
    0x00000000,
    0x060083B0,
    0xC000010D,
    0xFFF2FF5C,
    0x060085E8,
    0xC0000275,
    0x00000000,
    0x06008890,
    0x800002B2,
    0x00000000,
    0x3D4CCCCD,
    0x3FC00000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0xB8000100,
    0xB8000100,
]

subweapon_surface_checker = [
    # During the process of remotely giving an item received via multiworld, this will check to see if the item being
    # received is a subweapon and, if it is, wait until the player is not above an abyss or instant kill surface before
    # giving it. This is to ensure dropped previous subweapons won't land somewhere inaccessible.
    0x2408000D,  # ADDIU T0, R0, 0x000D
    0x11040006,  # BEQ   T0, A0, [forward 0x06]
    0x2409000E,  # ADDIU T1, R0, 0x000E
    0x11240004,  # BEQ   T1, A0, [forward 0x04]
    0x2408000F,  # ADDIU T0, R0, 0x000F
    0x11040002,  # BEQ   T0, A0, [forward 0x02]
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x1524000B,  # BNE   T1, A0, [forward 0x0B]
    0x3C0A800D,  # LUI   T2, 0x800D
    0x8D4A7B5C,  # LW    T2, 0x7B5C (T2)
    0x1140000E,  # BEQZ  T2,     [forward 0x0E]
    0x00000000,  # NOP
    0x914A0001,  # LBU   T2, 0x0001 (T2)
    0x240800A2,  # ADDIU T0, R0, 0x00A2
    0x110A000A,  # BEQ   T0, T2, [forward 0x0A]
    0x24090092,  # ADDIU T1, R0, 0x0092
    0x112A0008,  # BEQ   T1, T2, [forward 0x08]
    0x24080080,  # ADDIU T0, R0, 0x0080
    0x110A0006,  # BEQ   T0, T2, [forward 0x06]
    0x956C00DD,  # LHU   T4, 0x00DD (T3)
    0xA1600000,  # SB    R0, 0x0000 (T3)
    0x258C0001,  # ADDIU T4, T4, 0x0001
    0x080FF8D0,  # J     0x803FE340
    0xA56C00DD,  # SH    T4, 0x00DD (T3)
    0x00000000,  # NOP
    0x03E00008   # JR    RA
]

countdown_number_displayer = [
    # Displays a number below the HUD clock of however many items are left to find in whichever stage the player is in.
    # Which number in the save file to display depends on which map the player is currently on. It can track either
    # items marked progression only or all locations in the stage.
    # Courtesy of Moisés; see print_text_ovl.c in the src folder for the C source code.
    0x27BDFFD8,
    0xAFBF0024,
    0x00002025,
    0x0C000360,
    0x2405000C,
    0x3C038040,
    0x3C198034,
    0x2463D6D0,
    0x37392814,
    0x240E0002,
    0x3C0F0860,
    0x24180014,
    0xAC620000,
    0xAFB80018,
    0xAFAF0014,
    0xAFAE0010,
    0xAFB9001C,
    0x00002025,
    0x00402825,
    0x2406001E,
    0x0C0FF55D,
    0x24070028,
    0x8FBF0024,
    0x3C018040,
    0xAC22D6D4,
    0x03E00008,
    0x27BD0028,
    0x27BDFFE0,
    0xAFA40020,
    0x93AE0023,
    0x3C058039,
    0xAFBF001C,
    0x3C048040,
    0x3C068040,
    0x240F0014,
    0x00AE2821,
    0x90A59CA4,
    0xAFAF0010,
    0x8CC6D6D0,
    0x8C84D6D4,
    0x0C0FF58A,
    0x24070002,
    0x8FBF001C,
    0x27BD0020,
    0x03E00008,
    0x00000000,
    0x00000000,
    0x00000000,
    0x90820000,
    0x00001825,
    0x50400008,
    0xA4A00000,
    0xA4A20000,
    0x90820001,
    0x24840001,
    0x24A50002,
    0x1440FFFB,
    0x24630001,
    0xA4A00000,
    0x03E00008,
    0x00601025,
    0x27BDFFD8,
    0xAFBF0024,
    0xAFB0001C,
    0xAFA40028,
    0xAFA5002C,
    0xAFB10020,
    0xAFA60030,
    0xAFA70034,
    0x00008025,
    0x24050064,
    0x0C000360,
    0x00002025,
    0x8FA40040,
    0x00408825,
    0x3C05800A,
    0x10800004,
    0x8FA6003C,
    0x0C04B2E2,
    0x8CA5B450,
    0x00408025,
    0x5200001A,
    0x8FBF0024,
    0x12200017,
    0x8FAE0028,
    0x11C00015,
    0x02002025,
    0x97A5002E,
    0x97A60032,
    0x0C04B33F,
    0x24070001,
    0x02002025,
    0x83A50037,
    0x87A6003A,
    0x00003825,
    0x0C04B345,
    0xAFA00010,
    0x8FA40028,
    0x0C0FF51C,
    0x02202825,
    0x0C006CF0,
    0x02202025,
    0x02002025,
    0x02202825,
    0x00003025,
    0x0C04B34E,
    0x00003825,
    0x8FBF0024,
    0x02001025,
    0x8FB0001C,
    0x8FB10020,
    0x03E00008,
    0x27BD0028,
    0x27BDFFD8,
    0x8FAE0044,
    0xAFB00020,
    0xAFBF0024,
    0xAFA40028,
    0xAFA5002C,
    0xAFA60030,
    0xAFA70034,
    0x11C00007,
    0x00008025,
    0x3C05800A,
    0x8CA5B450,
    0x01C02025,
    0x0C04B2E2,
    0x8FA6003C,
    0x00408025,
    0x12000017,
    0x8FAF002C,
    0x11E00015,
    0x02002025,
    0x97A50032,
    0x97A60036,
    0x0C04B33F,
    0x24070001,
    0x02002025,
    0x24050001,
    0x24060064,
    0x00003825,
    0x0C04B345,
    0xAFA00010,
    0x8FA40028,
    0x8FA5002C,
    0x93A6003B,
    0x0C04B5BD,
    0x8FA70040,
    0x02002025,
    0x8FA5002C,
    0x00003025,
    0x0C04B34E,
    0x00003825,
    0x8FBF0024,
    0x02001025,
    0x8FB00020,
    0x03E00008,
    0x27BD0028,
    0x27BDFFE8,
    0xAFBF0014,
    0xAFA40018,
    0xAFA5001C,
    0xAFA60020,
    0x10C0000B,
    0xAFA70024,
    0x00A02025,
    0x00C02825,
    0x93A60027,
    0x0C04B5BD,
    0x8FA70028,
    0x8FA20018,
    0x3C010100,
    0x8C4F0000,
    0x01E1C025,
    0xAC580000,
    0x8FBF0014,
    0x27BD0018,
    0x03E00008,
    0x00000000,
    0xAFA50004,
    0x1080000E,
    0x30A500FF,
    0x24010001,
    0x54A10008,
    0x8C980000,
    0x8C8E0000,
    0x3C017FFF,
    0x3421FFFF,
    0x01C17824,
    0x03E00008,
    0xAC8F0000,
    0x8C980000,
    0x3C018000,
    0x0301C825,
    0xAC990000,
    0x03E00008,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000
]

countdown_number_manager = [
    # Tables and code for managing things about the Countdown number at the appropriate times.
    0x00010102,  # Map ID offset table start
    0x02020D03,
    0x04050505,
    0x0E0E0E05,
    0x07090806,
    0x0C0C000B,
    0x0C050D0A,
    0x00000000,  # Table end
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000001,  # Major identifiers table start
    0x01000000,
    0x00000000,
    0x00000000,
    0x01000000,
    0x01010000,
    0x00010101,
    0x01010101,
    0x01010101,
    0x01010000,
    0x00000000,  # Table end
    # Decrements the counter upon picking up an item if the counter should be decremented.
    0x90E80039,  # LBU   T0, 0x0039 (A3)
    0x240B0011,  # ADDIU T3, R0, 0x0011
    0x110B0002,  # BEQ   T0, T3, [forward 0x02]
    0x90EA0040,  # LBU   T2, 0x0040 (A3)
    0x2548FFFF,  # ADDIU T0, T2, 0xFFFF
    0x3C098040,  # LUI   T1, 0x8040
    0x01284821,  # ADDIU T1, T1, T0
    0x9129D71C,  # LBU   T1, 0xD71C (T1)
    0x11200009,  # BEQZ  T1,     [forward 0x09]
    0x3C088039,  # LUI   T0, 0x8039
    0x91099EE1,  # LBU   T1, 0x9EE1 (T0)
    0x3C0A8040,  # LUI   T2, 0x8040
    0x01495021,  # ADDU  T2, T2, T1
    0x914AD6DC,  # LBU   T2, 0xD6DC (T2)
    0x010A4021,  # ADDU  T0, T0, T2
    0x91099CA4,  # LBU   T1, 0x9CA4 (T0)
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1099CA4,  # SB    T1, 0x9CA4 (T0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Moves the number to/from its pause menu position when pausing/un-pausing.
    0x3C088040,  # LUI   T0, 0x8040
    0x8D08D6D4,  # LW    T0, 0xD6D4
    0x11000009,  # BEQZ  T0,     [forward 0x09]
    0x92090000,  # LBU   T1, 0x0000 (S0)
    0x14200004,  # BNEZ  AT,     [forward 0x04]
    0x3C0A0033,  # LUI   T2, 0x0033
    0x254A001F,  # ADDIU T2, T2, 0x001F
    0x03E00008,  # JR    RA
    0xAD0A0014,  # SW    T2, 0x0014 (T0)
    0x3C0A00D4,  # LUI   T2, 0x00D4
    0x254A003C,  # ADDIU T2, T2, 0x003C
    0xAD0A0014,  # SW    T2, 0x0014 (T0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Hides the number when going into a cutscene or the Options menu.
    0x3C048040,  # LUI   A0, 0x8040
    0x8C84D6D4,  # LW    A0, 0xD6D4 (A0)
    0x0C0FF59F,  # JAL   0x803FD67C
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x0804DFE0,  # J     0x80137FB0
    0x3C048000,  # LUI   A0, 0x8000
    0x00000000,  # NOP
    # Un-hides the number when leaving a cutscene or the Options menu.
    0x3C048040,  # LUI   A0, 0x8040
    0x8C84D6D4,  # LW    A0, 0xD6D4 (A0)
    0x0C0FF59F,  # JAL   0x803FD67C
    0x24050001,  # ADDIU A1, R0, 0x0000
    0x0804DFFA,  # J     0x8013
    0x3C047FFF,  # LUI   A0, 0x7FFFF
    0x00000000,  # NOP
    # Kills the last map's pointer to the Countdown stuff.
    0x3C088040,  # LUI   T0, 0x8040
    0xFD00D6D0,  # SD    R0, 0xD6D0 (T0)
    0x03E00008   # JR    RA
]

new_game_extras = [
    # Upon starting a new game, this will write anything extra to the save file data that the run should have at the
    # start. The initial Countdown numbers begin here.
    0x24080000,  # ADDIU T0, R0, 0x0000
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x11090008,  # BEQ   T0, T1, [forward 0x08]
    0x3C0A8040,  # LUI   T2, 0x8040
    0x01485021,  # ADDU  T2, T2, T0
    0x8D4AD818,  # LW    T2, 0xD818 (T2)
    0x3C0B8039,  # LUI   T3, 0x8039
    0x01685821,  # ADDU  T3, T3, T0
    0xAD6A9CA4,  # SW    T2, 0x9CA4 (T3)
    0x1000FFF8,  # B             [backward 0x08]
    0x25080004,  # ADDIU T0, T0, 0x0004
    # start_inventory begins here
    0x3C088039,  # LUI   T0, 0x8039
    0x91099C27,  # LBU   T1, 0x9C27 (T0)
    0x31290010,  # ANDI  T1, T1, 0x0010
    0x15200005,  # BNEZ  T1,     [forward 0x05]
    0x24090000,  # ADDIU T1, R0, 0x0000  <- Starting jewels
    0xA1099C49,  # SB    T1, 0x9C49
    0x3C0A8040,  # LUI   T2, 0x8040
    0x8D4BE514,  # LW    T3, 0xE514 (T2) <- Starting money
    0xAD0B9C44,  # SW    T3, 0x9C44 (T0)
    0x24090000,  # ADDIU T1, R0, 0x0000  <- Starting PowerUps
    0xA1099CED,  # SB    T1, 0x9CED (T0)
    0x24090000,  # ADDIU T1, R0, 0x0000  <- Starting sub-weapon
    0xA1099C43,  # SB    T1, 0x9C43 (T0)
    0x24090000,  # ADDIU T1, R0, 0x0000  <- Starting Ice Traps
    0xA1099BE2,  # SB    T1, 0x9BE2 (T0)
    0x240C0000,  # ADDIU T4, R0, 0x0000
    0x240D0023,  # ADDIU T5, R0, 0x0023
    0x11AC0007,  # BEQ   T5, T4, [forward 0x07]
    0x3C0A8040,  # LUI   T2, 0x8040
    0x014C5021,  # ADDU  T2, T2, T4
    0x814AE518,  # LB    T2, 0xE518      <- Starting inventory items
    0x25080001,  # ADDIU T0, T0, 0x0001
    0xA10A9C4A,  # SB    T2, 0x9C4A (T0)
    0x1000FFF9,  # B             [backward 0x07]
    0x258C0001,  # ADDIU T4, T4, 0x0001
    0x03E00008   # JR    RA
]

shopsanity_stuff = [
    # Everything related to shopsanity.
    # Flag table (in bytes) start
    0x80402010,
    0x08000000,
    0x00000000,
    0x00000000,
    0x00040200,
    # Replacement item table (in halfwords) start
    0x00030003,
    0x00030003,
    0x00030000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000003,
    0x00030000,
    # Switches the vanilla item being bought with the randomized one, if its flag is un-set, and sets its flag.
    0x3C088040,  # LUI   T0, 0x8040
    0x01044021,  # ADDU  T0, T0, A0
    0x9109D8CA,  # LBU   T1, 0xD8CA (T0)
    0x3C0B8039,  # LUI   T3, 0x8039
    0x916A9C1D,  # LBU   T2, 0x9C1D (T3)
    0x01496024,  # AND   T4, T2, T1
    0x15800005,  # BNEZ  T4,     [forward 0x05]
    0x01495025,  # OR    T2, T2, T1
    0xA16A9C1D,  # SB    T2, 0x9C1D (T3)
    0x01044021,  # ADDU  T0, T0, A0
    0x9504D8D8,  # LHU   A0, 0xD8D8 (T0)
    0x308400FF,  # ANDI  A0, A0, 0x00FF
    0x0804EFFB,  # J     0x8013BFEC
    0x00000000,  # NOP
    # Switches the vanilla item model on the buy menu with the randomized item if the randomized item isn't purchased.
    0x3C088040,  # LUI   T0, 0x8040
    0x01044021,  # ADDU  T0, T0, A0
    0x9109D8CA,  # LBU   T1, 0xD8CA (T0)
    0x3C0B8039,  # LUI   T3, 0x8039
    0x916A9C1D,  # LBU   T2, 0x9C1D (T3)
    0x01495024,  # AND   T2, T2, T1
    0x15400005,  # BNEZ  T2,     [forward 0x05]
    0x01044021,  # ADDU  T0, T0, A0
    0x9504D8D8,  # LHU   A0, 0xD8D8 (T0)
    0x00046202,  # SRL   T4, A0, 8
    0x55800001,  # BNEZL T4,     [forward 0x01]
    0x01802021,  # ADDU  A0, T4, R0
    0x0804F180,  # J     0x8013C600
    0x00000000,  # NOP
    # Replacement item names table start.
    0x00010203,
    0x04000000,
    0x00000000,
    0x00000000,
    0x00050600,
    0x00000000,
    # Switches the vanilla item name in the shop menu with the randomized item if the randomized item isn't purchased.
    0x3C088040,  # LUI   T0, 0x8040
    0x01064021,  # ADDU  T0, T0, A2
    0x9109D8CA,  # LBU   T1, 0xD8CA (T0)
    0x3C0B8039,  # LUI   T3, 0x8039
    0x916A9C1D,  # LBU   T2, 0x9C1D (T3)
    0x01495024,  # AND   T2, T2, T1
    0x15400004,  # BNEZ  T2,     [forward 0x04]
    0x00000000,  # NOP
    0x9105D976,  # LBU   A1, 0xD976 (T0)
    0x3C048001,  # LUI   A0, 8001
    0x3484A100,  # ORI   A0, A0, 0xA100
    0x0804B39F,  # J     0x8012CE7C
    0x00000000,  # NOP
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    # Displays "Not purchased." if the selected randomized item is nor purchased, or the current holding amount of that
    # slot's vanilla item if it is.
    0x3C0C8040,  # LUI   T4, 0x8040
    0x018B6021,  # ADDU  T4, T4, T3
    0x918DD8CA,  # LBU   T5, 0xD8CA (T4)
    0x3C0E8039,  # LUI   T6, 0x8039
    0x91D89C1D,  # LBU   T8, 0x9C1D (T6)
    0x030DC024,  # AND   T8, T8, T5
    0x13000003,  # BEQZ  T8,     [forward 0x03]
    0x00000000,  # NOP
    0x0804E819,  # J     0x8013A064
    0x00000000,  # NOP
    0x0804E852,  # J     0x8013A148
    0x820F0061,  # LB    T7, 0x0061 (S0)
    0x00000000,  # NOP
    # Displays a custom item description if the selected randomized item is not purchased.
    0x3C088040,  # LUI   T0, 0x8040
    0x01054021,  # ADDU  T0, T0, A1
    0x9109D8D0,  # LBU   T1, 0xD8D0 (T0)
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914B9C1D,  # LBU   T3, 0x9C1D (T2)
    0x01695824,  # AND   T3, T3, T1
    0x15600003,  # BNEZ  T3,     [forward 0x03]
    0x00000000,  # NOP
    0x3C048002,  # LUI   A0, 0x8002
    0x24849C00,  # ADDIU A0, A0, 0x9C00
    0x0804B39F   # J     0x8012CE7C
]

special_sound_notifs = [
    # Plays a distinct sound whenever you get enough Special1s to unlock a new location or enough Special2s to unlock
    # Dracula's door.
    0x3C088013,  # LUI   A0, 0x8013
    0x9108AC9F,  # LBU   T0, 0xAC57 (T0)
    0x3C098039,  # LUI   T1, 0x8039
    0x91299C4C,  # LBU   T1, 0x9C4B (T1)
    0x15090003,  # BNE   T0, T1, [forward 0x03]
    0x00000000,  # NOP
    0x0C004FAB,  # JAL   0x80013EAC
    0x24040162,  # ADDIU A0, R0, 0x0162
    0x0804F0BF,  # J     0x8013C2FC
    0x00000000,  # NOP
    0x3C088013,  # LUI   T0, 0x8013
    0x9108AC57,  # LBU   T0, 0xAC57 (T0)
    0x3C098039,  # LUI   T1, 0x8039
    0x91299C4B,  # LBU   T1, 0x9C4B (T1)
    0x0128001B,  # DIVU  T1, T0
    0x00005010,  # MFHI
    0x15400006,  # BNEZ  T2,     [forward 0x06]
    0x00005812,  # MFLO  T3
    0x296C0008,  # SLTI  T4, T3, 0x0008
    0x11800003,  # BEQZ  T4,     [forward 0x03]
    0x00000000,  # NOP
    0x0C004FAB,  # JAL   0x80013EAC
    0x2404019E,  # ADDIU A0, R0, 0x019E
    0x0804F0BF   # J     0x8013C2FC
]

map_text_redirector = [
    # Checks for Map Texts 06 or 08 if in the Forest or Castle Wall Main maps respectively and redirects the text
    # pointer to a blank string, skipping all the yes/no prompt text for pulling levers.
    0x0002FFFF,  # Dummy text string
    0x3C0B8039,  # LUI   T3, 0x8039
    0x91689EE1,  # LBU   T0, 0x9EE1 (T3)
    0x1100000F,  # BEQZ  T0,     [forward 0x0F]
    0x24090006,  # ADDIU T1, R0, 0x0006
    0x240A0002,  # ADDIU T2, R0, 0x0002
    0x110A000C,  # BEQ   T0, T2, [forward 0x0C]
    0x24090008,  # ADDIU T1, R0, 0x0008
    0x240A0009,  # ADDIU T2, R0, 0x0009
    0x110A0009,  # BEQ   T0, T2, [forward 0x09]
    0x24090004,  # ADDIU T1, R0, 0x0004
    0x240A000A,  # ADDIU T2, R0, 0x000A
    0x110A0006,  # BEQ   T0, T2, [forward 0x06]
    0x24090001,  # ADDIU T1, R0, 0x0001
    0x240A000C,  # ADDIU T2, R0, 0x000C
    0x110A0003,  # BEQ   T0, T2, [forward 0x03]
    0x2409000C,  # ADDIU T1, R0, 0x000C
    0x10000008,  # B     0x803FDB34
    0x00000000,  # NOP
    0x15250006,  # BNE   T1, A1, [forward 0x06]
    0x00000000,  # NOP
    0x3C04803F,  # LUI   A0, 0x803F
    0x3484DACC,  # ORI   A0, A0, 0xDACC
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x0804B39F,  # J     0x8012CE7C
    0x00000000,  # NOP
    # Redirects to a custom message if you try placing the bomb ingredients at the bottom CC crack before deactivating
    # the seal.
    0x24090009,  # ADDIU T1, R0, 0x0009
    0x15090009,  # BNE   T0, T1, [forward 0x09]
    0x240A0002,  # ADDIU T2, R0, 0x0002
    0x15450007,  # BNE   T2, A1, [forward 0x07]
    0x916A9C18,  # LBU   T2, 0x9C18 (T3)
    0x314A0001,  # ANDI  T2, T2, 0x0001
    0x15400004,  # BNEZ  T2,     [forward 0x04]
    0x00000000,  # NOP
    0x3C04803F,  # LUI   A0, 0x803F
    0x3484DBAC,  # ORI   A0, A0, 0xDBAC
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x0804B39F,  # J     0x8012CE7C
    0x00000000,  # NOP
    # Checks for Map Texts 02 or 00 if in the Villa hallway or CC lizard lab maps respectively and redirects the text
    # pointer to a blank string, skipping all the NPC dialogue mandatory for checks.
    0x3C088039,  # LUI   T0, 0x8039
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    0x240A0005,  # ADDIU T2, R0, 0x0005
    0x110A0006,  # BEQ   T0, T2, [forward 0x06]
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x240A000C,  # ADDIU T2, R0, 0x000C
    0x110A0003,  # BEQ   T0, T2, [forward 0x03]
    0x24090000,  # ADDIU T1, R0, 0x0000
    0x0804B39F,  # J     0x8012CE7C
    0x00000000,  # NOP
    0x15250004,  # BNE   T1, A1, [forward 0x04]
    0x00000000,  # NOP
    0x3C04803F,  # LUI   A0, 0x803F
    0x3484DACC,  # ORI   A0, A0, 0xDACC
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x0804B39F   # J     0x8012CE7C
]

special_descriptions_redirector = [
    # Redirects the menu description when looking at the Special1 and 2 items to different, custom strings that tell
    # how many are needed per warp and to fight Dracula respectively, and how many there are of both in the whole seed.
    0x240A0003,  # ADDIU T2, R0, 0x0003
    0x10AA0005,  # BEQ   A1, T2, [forward 0x05]
    0x240A0004,  # ADDIU T2, R0, 0x0004
    0x10AA0003,  # BEQ   A1, T2, [forward 0x03]
    0x00000000,  # NOP
    0x0804B39F,  # J     0x8012CE7C
    0x00000000,  # NOP
    0x3C04803F,  # LUI   A0, 0x803F
    0x3484E53C,  # ORI   A0, A0, 0xE53C
    0x24A5FFFD,  # ADDIU A1, A1, 0xFFFD
    0x0804B39F   # J     0x8012CE7C
]

forest_cw_villa_intro_cs_player = [
    # Plays the Forest, Castle Wall, or Villa intro cutscene after transitioning to a different map if the map being
    # transitioned to is the start of their levels respectively. Gets around the fact that they have to be set on the
    # previous loading zone for them to play normally.
    0x3C088039,  # LUI   T0, 0x8039
    0x8D099EE0,  # LW    T1, 0x9EE0 (T0)
    0x1120000B,  # BEQZ  T1  T1, [forward 0x0B]
    0x240B0000,  # ADDIU T3, R0, 0x0000
    0x3C0A0002,  # LUI   T2, 0x0002
    0x112A0008,  # BEQ   T1, T2, [forward 0x08]
    0x240B0007,  # ADDIU T3, R0, 0x0007
    0x254A0007,  # ADDIU T2, T2, 0x0007
    0x112A0005,  # BEQ   T1, T2, [forward 0x05]
    0x3C0A0003,  # LUI   T2, 0x0003
    0x112A0003,  # BEQ   T1, T2, [forward 0x03]
    0x240B0003,  # ADDIU T3, R0, 0x0003
    0x08005FAA,  # J     0x80017EA8
    0x00000000,  # NOP
    0x010B6021,  # ADDU  T4, T0, T3
    0x918D9C08,  # LBU   T5, 0x9C08 (T4)
    0x31AF0001,  # ANDI  T7, T5, 0x0001
    0x15E00009,  # BNEZ  T7,     [forward 0x09]
    0x240E0009,  # ADDIU T6, R0, 0x0009
    0x3C180003,  # LUI   T8, 0x0003
    0x57090001,  # BNEL  T8, T1, [forward 0x01]
    0x240E0004,  # ADDIU T6, R0, 0x0004
    0x15200003,  # BNEZ  T1,     [forward 0x03]
    0x240F0001,  # ADDIU T7, R0, 0x0001
    0xA18F9C08,  # SB    T7, 0x9C08 (T4)
    0x240E003C,  # ADDIU T6, R0, 0x003C
    0xA10E9EFF,  # SB    T6, 0x9EFF (T0)
    0x08005FAA   # J     0x80017EA8
]

map_id_refresher = [
    # After transitioning to a different map, if this detects the map ID being transitioned to as FF, it will write back
    # the past map ID so that the map will reset. Useful for thngs like getting around a bug wherein the camera fixes in
    # place if you enter a loading zone that doesn't actually change the map, which can happen in a seed that gives you
    # any character tower stage at the very start.
    0x240800FF,  # ADDIU T0, R0, 0x00FF
    0x110E0003,  # BEQ   T0, T6, [forward 0x03]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0xA44E61D8,  # SH    T6, 0x61D8
    0x904961D9,  # LBU   T1, 0x61D9
    0xA0496429,  # SB    T1, 0x6429
    0x03E00008   # JR    RA
]

character_changer = [
    # Changes the character being controlled if the player is holding L while loading into a map by swapping the
    # character ID.
    0x3C08800D,  # LUI   T0, 0x800D
    0x910B5E21,  # LBU   T3, 0x5E21 (T0)
    0x31680020,  # ANDI  T0, T3, 0x0020
    0x3C0A8039,  # LUI   T2, 0x8039
    0x1100000B,  # BEQZ  T0,     [forward 0x0B]
    0x91499C3D,  # LBU   T1, 0x9C3D (T2)
    0x11200005,  # BEQZ  T1,     [forward 0x05]
    0x24080000,  # ADDIU T0, R0, 0x0000
    0xA1489C3D,  # SB    T0, 0x9C3D (T2)
    0x25080001,  # ADDIU T0, T0, 0x0001
    0xA1489BC2,  # SB    T0, 0x9BC2 (T2)
    0x10000004,  # B             [forward 0x04]
    0x24080001,  # ADDIU T0, R0, 0x0001
    0xA1489C3D,  # SB    T0, 0x9C3D (T2)
    0x25080001,  # ADDIU T0, T0, 0x0001
    0xA1489BC2,  # SB    T0, 0x9BC2 (T2)
    # Changes the alternate costume variables if the player is holding C-up.
    0x31680008,  # ANDI  T0, T3, 0x0008
    0x11000009,  # BEQZ  T0,     [forward 0x09]
    0x91499C24,  # LBU   T1, 0x9C24 (T2)
    0x312B0040,  # ANDI  T3, T1, 0x0040
    0x2528FFC0,  # ADDIU T0, T1, 0xFFC0
    0x15600003,  # BNEZ  T3,     [forward 0x03]
    0x240C0000,  # ADDIU T4, R0, 0x0000
    0x25280040,  # ADDIU T0, T1, 0x0040
    0x240C0001,  # ADDIU T4, R0, 0x0001
    0xA1489C24,  # SB    T0, 0x9C24 (T2)
    0xA14C9CEE,  # SB    T4, 0x9CEE (T2)
    0x080062AA,  # J     0x80018AA8
    0x00000000,  # NOP
    # Plays the attack sound of the character being changed into to indicate the change was successful.
    0x3C088039,  # LUI   T0, 0x8039
    0x91099BC2,  # LBU   T1, 0x9BC2 (T0)
    0xA1009BC2,  # SB    R0, 0x9BC2 (T0)
    0xA1009BC1,  # SB    R0, 0x9BC1 (T0)
    0x11200006,  # BEQZ  T1,     [forward 0x06]
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0x240402F6,  # ADDIU A0, R0, 0x02F6
    0x55200001,  # BNEZL T1,     [forward 0x01]
    0x240402F8,  # ADDIU A0, R0, 0x02F8
    0x08004FAB,  # J     0x80013EAC
    0x00000000,  # NOP
    0x03E00008   # JR    RA
]

panther_dash = [
    # Changes various movement parameters when holding C-right so the player will move way faster.
    # Increases movement speed and speeds up the running animation.
    0x3C08800D,  # LUI   T0, 0x800D
    0x91085E21,  # LBU   T0, 0x5E21 (T0)
    0x31080001,  # ANDI  T0, T0, 0x0001
    0x24093FEA,  # ADDIU T1, R0, 0x3FEA
    0x11000004,  # BEQZ  T0,     [forward 0x04]
    0x240B0010,  # ADDIU T3, R0, 0x0010
    0x3C073F20,  # LUI   A3, 0x3F20
    0x240940AA,  # ADDIU T1, R0, 0x40AA
    0x240B000A,  # ADDIU T3, R0, 0x000A
    0x3C0C8035,  # LUI   T4, 0x8035
    0xA18B07AE,  # SB    T3, 0x07AE (T4)
    0xA18B07C2,  # SB    T3, 0x07C2 (T4)
    0x3C0A8034,  # LUI   T2, 0x8034
    0x03200008,  # JR    T9
    0xA5492BD8,  # SH    T1, 0x2BD8 (T2)
    0x00000000,  # NOP
    # Increases the turning speed so that handling is better.
    0x3C08800D,  # LUI   T0, 0x800D
    0x91085E21,  # LBU   T0, 0x5E21 (T0)
    0x31080001,  # ANDI  T0, T0, 0x0001
    0x11000002,  # BEQZ  T0,     [forward 0x02]
    0x240A00D9,  # ADDIU T2, R0, 0x00D9
    0x240A00F0,  # ADDIU T2, R0, 0x00F0
    0x3C0B8039,  # LUI   T3, 0x8039
    0x916B9C3D,  # LBU   T3, 0x9C3D (T3)
    0x11600003,  # BEQZ  T3,     [forward 0x03]
    0xD428DD58,  # LDC1  F8, 0xDD58 (AT)
    0x03E00008,  # JR    RA
    0xA02ADD59,  # SB    T2, 0xDD59 (AT)
    0xD428D798,  # LDC1  F8, 0xD798 (AT)
    0x03E00008,  # JR    RA
    0xA02AD799,  # SB    T2, 0xD799 (AT)
    0x00000000,  # NOP
    # Increases crouch-walking x and z speed.
    0x3C08800D,  # LUI   T0, 0x800D
    0x91085E21,  # LBU   T0, 0x5E21 (T0)
    0x31080001,  # ANDI  T0, T0, 0x0001
    0x11000002,  # BEQZ  T0,     [forward 0x02]
    0x240A00C5,  # ADDIU T2, R0, 0x00C5
    0x240A00F8,  # ADDIU T2, R0, 0x00F8
    0x3C0B8039,  # LUI   T3, 0x8039
    0x916B9C3D,  # LBU   T3, 0x9C3D (T3)
    0x15600005,  # BNEZ  T3,     [forward 0x05]
    0x00000000,  # NOP
    0xA02AD801,  # SB    T2, 0xD801 (AT)
    0xA02AD809,  # SB    T2, 0xD809 (AT)
    0x03E00008,  # JR    RA
    0xD430D800,  # LDC1  F16, 0xD800 (AT)
    0xA02ADDC1,  # SB    T2, 0xDDC1 (AT)
    0xA02ADDC9,  # SB    T2, 0xDDC9 (AT)
    0x03E00008,  # JR    RA
    0xD430DDC0   # LDC1  F16, 0xDDC0 (AT)
]

panther_jump_preventer = [
    # Optional hack to prevent jumping while moving at the increased panther dash speed as a way to prevent logic
    # sequence breaks that would otherwise be impossible without it. Such sequence breaks are never considered in logic
    # either way.

    # Decreases a "can running jump" value by 1 per frame unless it's at 0, or while in the sliding state. When the
    # player lets go of C-right, their running speed should have returned to a normal amount by the time it hits 0.
    0x9208007F,  # LBU   T0, 0x007F (S0)
    0x24090008,  # ADDIU T1, R0, 0x0008
    0x11090005,  # BEQ   T0, T1, [forward 0x05]
    0x3C088039,  # LUI   T0, 0x8039
    0x91099BC1,  # LBU   T1, 0x9BC1 (T0)
    0x11200002,  # BEQZ  T1,     [forward 0x02]
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1099BC1,  # SB    T1, 0x9BC1 (T0)
    0x080FF413,  # J     0x803FD04C
    0x00000000,  # NOP
    # Increases the "can running jump" value by 2 per frame while panther dashing unless it's at 8 or higher, at which
    # point the player should be at the max panther dash speed.
    0x00074402,  # SRL   T0, A3, 16
    0x29083F7F,  # SLTI  T0, T0, 0x3F7F
    0x11000006,  # BEQZ  T0,     [forward 0x06]
    0x3C098039,  # LUI   T1, 0x8039
    0x912A9BC1,  # LBU   T2, 0x9BC1 (T1)
    0x254A0002,  # ADDIU T2, T2, 0x0002
    0x294B0008,  # SLTI  T3, T2, 0x0008
    0x55600001,  # BNEZL T3,     [forward 0x01]
    0xA12A9BC1,  # SB    T2, 0x9BC1 (T1)
    0x03200008,  # JR    T9
    0x00000000,  # NOP
    # Makes running jumps only work while the "can running jump" value is at 0. Otherwise, their state won't change.
    0x3C010001,  # LUI   AT, 0x0001
    0x3C088039,  # LUI   T0, 0x8039
    0x91089BC1,  # LBU   T0, 0x9BC1 (T0)
    0x55000001,  # BNEZL T0,     [forward 0x01]
    0x3C010000,  # LUI   AT, 0x0000
    0x03E00008   # JR    RA
]

gondola_skipper = [
    # Upon stepping on one of the gondolas in Tunnel to activate it, this will instantly teleport you to the other end
    # of the gondola course depending on which one activated, skipping the entire 3-minute wait to get there.
    0x3C088039,  # LUI   T0, 0x8039
    0x240900FF,  # ADDIU T1, R0, 0x00FF
    0xA1099EE1,  # SB    T1, 0x9EE1 (T0)
    0x31EA0020,  # ANDI  T2, T7, 0x0020
    0x3C0C3080,  # LUI   T4, 0x3080
    0x358C9700,  # ORI   T4, T4, 0x9700
    0x154B0003,  # BNE   T2, T3, [forward 0x03]
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x24090003,  # ADDIU T1, R0, 0x0003
    0x3C0C7A00,  # LUI   T4, 0x7A00
    0xA1099EE3,  # SB    T1, 0x9EE3 (T0)
    0xAD0C9EE4,  # SW    T4, 0x9EE4 (T0)
    0x3C0D0010,  # LUI   T5, 0x0010
    0x25AD0010,  # ADDIU T5, T5, 0x0010
    0xAD0D9EE8,  # SW    T5, 0x9EE8 (T0)
    0x08063E68   # J     0x8018F9A0
]

mandragora_with_nitro_setter = [
    # When setting a Nitro, if Mandragora is in the inventory too and the wall's "Mandragora set" flag is not set, this
    # will automatically subtract a Mandragora from the inventory and set its flag so the wall can be blown up in just
    # one interaction instead of two.
    0x3C088039,  # LUI   T0, 0x8039
    0x81099EE1,  # LB    T1, 0x9EE1 (T0)
    0x240A000C,  # ADDIU T2, R0, 0x000C
    0x112A000E,  # BEQ   T1, T2, [forward 0x0E]
    0x81099C18,  # LB    T1, 0x9C18 (T0)
    0x31290002,  # ANDI  T1, T1, 0x0002
    0x11200009,  # BEQZ  T1,     [forward 0x09]
    0x91099C5D,  # LBU   T1, 0x9C5D (T0)
    0x11200007,  # BEQZ  T1,     [forward 0x07]
    0x910B9C1A,  # LBU   T3, 0x9C1A (T0)
    0x316A0001,  # ANDI  T2, T3, 0x0001
    0x15400004,  # BNEZ  T2,     [forward 0x04]
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1099C5D,  # SB    T1, 0x9C5D (T0)
    0x356B0001,  # ORI   T3, T3, 0x0001
    0xA10B9C1A,  # SB    T3, 0x9C1A (T0)
    0x08000512,  # J     0x80001448
    0x00000000,  # NOP
    0x810B9BF2,  # LB    T3, 0x9BF2 (T0)
    0x31690040,  # ANDI  T1, T3, 0x0040
    0x11200008,  # BEQZ  T1,     [forward 0x08]
    0x91099C5D,  # LBU   T1, 0x9C5D (T0)
    0x11200006,  # BEQZ  T1,     [forward 0x06]
    0x316A0080,  # ANDI  T2, T3, 0x0080
    0x15400004,  # BNEZ  T2, 0x803FE0E8
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1099C5D,  # SB    T1, 0x9C5D (T0)
    0x356B0080,  # ORI   T3, T3, 0x0080
    0xA10B9BF2,  # SB    T3, 0x9BF2 (T0)
    0x08000512   # J     0x80001448
]

ambience_silencer = [
    # Silences all map-specific ambience when loading into a different map, so we don't have to live with, say, Tower of
    # Science/Clock Tower machinery noises everywhere until either resetting, dying, or going into a map that is
    # normally set up to disable said noises.
    0x3C088039,  # LUI   T0, 0x8039
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x11090003,  # BEQ   T0, T1, [forward 0x03]
    0x00000000,  # NOP
    0x0C004FAB,  # JAL   0x80013EAC
    0x3404818C,  # ORI   A0, R0, 0x818C
    0x0C004FAB,  # JAL   0x80013EAC
    0x34048134,  # ORI   A0, R0, 0x8134
    0x0C004FAB,  # JAL   0x80013EAC
    0x34048135,  # ORI   A0, R0, 0x8135
    0x0C004FAB,  # JAL   0x80013EAC
    0x34048136,  # ORI   A0, R0, 0x8136
    0x08054987,  # J     0x8015261C
    0x00000000,  # NOP
    # Plays the fan ambience when loading into the fan meeting room if this detects the active character's cutscene flag
    # here already being set.
    0x3C088039,  # LUI   T0, 0x8039
    0x91099EE1,  # LBU   T1, 0x9EE1 (T0)
    0x240A0019,  # ADDIU T2, R0, 0x0019
    0x152A000A,  # BNE   T1, T2, [forward 0x0A]
    0x910B9BFE,  # LBU   T3, 0x9BFE (T0)
    0x910C9C3D,  # LBU   T4, 0x9C3D (T0)
    0x240D0001,  # ADDIU T5, R0, 0x0001
    0x55800001,  # BNEZL T4,     [forward 0x01]
    0x240D0002,  # ADDIU T5, R0, 0x0002
    0x016D7024,  # AND   T6, T3, T5
    0x11C00003,  # BEQZ  T6,     [forward 0x03]
    0x00000000,  # NOP
    0x0C0052B4,  # JAL   0x80014AD0
    0x34040169,  # ORI   A0, R0, 0x0169
    0x0805581C   # J     0x80156070
]

coffin_cutscene_skipper = [
    # Kills the normally-unskippable "Found a hidden path" cutscene at the end of Villa if this detects, in the current
    # module in the modules array, the cutscene's module number of 0x205C and the "skip" value 0f 0x01 normally set by
    # all cutscenes upon pressing Start.
    0x10A0000B,  # BEQZ  A1,     [forward 0x0B]
    0x00000000,  # NOP
    0x94A80000,  # LHU   T0, 0x0000 (A1)
    0x2409205C,  # ADDIU T1, R0, 0x205C
    0x15090007,  # BNE   T0, T1, [forward 0x07]
    0x90AA0070,  # LBU   T2, 0x0070 (A1)
    0x11400005,  # BEQZ  T2,     [forward 0x05]
    0x90AB0009,  # LBU   T3, 0x0009 (A1)
    0x240C0003,  # ADDIU T4, R0, 0x0003
    0x156C0002,  # BNE   T3, T4, [forward 0x02]
    0x240B0004,  # ADDIU T3, R0, 0x0004
    0xA0AB0009,  # SB    T3, 0x0009 (A1)
    0x03E00008   # JR    RA
]

multiworld_item_name_loader = [
    # When picking up an item from another world, this will load from ROM the custom message for that item explaining
    # in the item textbox what the item is and who it's for. The flag index it calculates determines from what part of
    # the ROM to load the item name from. If the item being picked up is a white jewel or a contract, it will always
    # load from a part of the ROM that has nothing in it to ensure their set "flag" values don't yield unintended names.
    0x3C088040,  # LUI   T0, 0x8040
    0xAD03E238,  # SW    V1, 0xE238 (T0)
    0x92080039,  # LBU   T0, 0x0039 (S0)
    0x11000003,  # BEQZ  T0,     [forward 0x03]
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x15090003,  # BNE   T0, T1, [forward 0x03]
    0x24080000,  # ADDIU T0, R0, 0x0000
    0x10000010,  # B             [forward 0x10]
    0x24080000,  # ADDIU T0, R0, 0x0000
    0x920C0055,  # LBU   T4, 0x0055 (S0)
    0x8E090058,  # LW    T1, 0x0058 (S0)
    0x1120000C,  # BEQZ  T1,     [forward 0x0C]
    0x298A0011,  # SLTI  T2, T4, 0x0011
    0x51400001,  # BEQZL T2,     [forward 0x01]
    0x258CFFED,  # ADDIU T4, T4, 0xFFED
    0x240A0000,  # ADDIU T2, R0, 0x0000
    0x00094840,  # SLL   T1, T1, 1
    0x5520FFFE,  # BNEZL T1,     [backward 0x02]
    0x254A0001,  # ADDIU T2, T2, 0x0001
    0x240B0020,  # ADDIU T3, R0, 0x0020
    0x018B0019,  # MULTU T4, T3
    0x00004812,  # MFLO  T1
    0x012A4021,  # ADDU  T0, T1, T2
    0x00084200,  # SLL   T0, T0, 8
    0x3C0400BB,  # LUI   A0, 0x00BB
    0x24847164,  # ADDIU A0, A0, 0x7164
    0x00882020,  # ADD   A0, A0, T0
    0x3C058018,  # LUI   A1, 0x8018
    0x34A5BF98,  # ORI   A1, A1, 0xBF98
    0x0C005DFB,  # JAL   0x800177EC
    0x24060100,  # ADDIU A2, R0, 0x0100
    0x3C088040,  # LUI   T0, 0x8040
    0x8D03E238,  # LW    V1, 0xE238 (T0)
    0x3C1F8012,  # LUI   RA, 0x8012
    0x27FF5BA4,  # ADDIU RA, RA, 0x5BA4
    0x0804EF54,  # J     0x8013BD50
    0x94640002,  # LHU   A0, 0x0002 (V1)
    # Changes the Y screen position of the textbox depending on how many line breaks there are.
    0x3C088019,  # LUI   T0, 0x8019
    0x9108C097,  # LBU   T0, 0xC097 (T0)
    0x11000005,  # BEQZ  T0,     [forward 0x05]
    0x2508FFFF,  # ADDIU T0, T0, 0xFFFF
    0x11000003,  # BEQZ  T0,     [forward 0x03]
    0x00000000,  # NOP
    0x1000FFFC,  # B             [backward 0x04]
    0x24C6FFF1,  # ADDIU A2, A2, 0xFFF1
    0x0804B33F,  # J     0x8012CCFC
    # Changes the length and number of lines on the textbox if there's a multiworld message in the buffer.
    0x3C088019,  # LUI   T0, 0x8019
    0x9108C097,  # LBU   T0, 0xC097 (T0)
    0x11000003,  # BEQZ  T0, [forward 0x03]
    0x00000000,  # NOP
    0x00082821,  # ADDU  A1, R0, T0
    0x240600B6,  # ADDIU A2, R0, 0x00B6
    0x0804B345,  # J     0x8012CD14
    0x00000000,  # NOP
    # Redirects the text to the multiworld message buffer if a message exists in it.
    0x3C088019,  # LUI   T0, 0x8019
    0x9108C097,  # LBU   T0, 0xC097 (T0)
    0x11000004,  # BEQZ  T0,     [forward 0x04]
    0x00000000,  # NOP
    0x3C048018,  # LUI   A0, 0x8018
    0x3484BF98,  # ORI   A0, A0, 0xBF98
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x0804B39F,  # J     0x8012CE7C
    # Copy the "item from player" text when being given an item through the multiworld via the game's copy function.
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x00000000,  # NOP
    0x3C088040,  # LUI   T0, 0x8040
    0xAD1FE33C,  # SW    RA, 0xE33C (T0)
    0xA104E338,  # SB    A0, 0xE338 (T0)
    0x3C048019,  # LUI   A0, 0x8019
    0x2484C0A8,  # ADDIU A0, A0, 0xC0A8
    0x3C058019,  # LUI   A1, 0x8019
    0x24A5BF98,  # ADDIU A1, A1, 0xBF98
    0x0C000234,  # JAL   0x800008D0
    0x24060100,  # ADDIU A2, R0, 0x0100
    0x3C088040,  # LUI   T0, 0x8040
    0x8D1FE33C,  # LW    RA, 0xE33C (T0)
    0x0804EDCE,  # J     0x8013B738
    0x9104E338,  # LBU   A0, 0xE338 (T0)
    0x00000000,  # NOP
    # Neuters the multiworld item text buffer if giving a non-multiworld item through the in-game remote item rewarder
    # byte before then jumping to item_prepareTextbox.
    0x24080011,  # ADDIU T0, R0, 0x0011
    0x10880004,  # BEQ   A0, T0, [forward 0x04]
    0x24080012,  # ADDIU T0, R0, 0x0012
    0x10880002,  # BEQ   A0, T0, [forward 0x02]
    0x3C088019,  # LUI   T0, 0x8019
    0xA100C097,  # SB    R0, 0xC097 (T0)
    0x0804EDCE   # J     0x8013B738
]

ice_trap_initializer = [
    # During a map load, creates the module that allows the ice block model to appear while in the frozen state if not
    # on the intro narration map (map 0x16).
    0x3C088039,  # LUI   T0, 0x8039
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    0x24090016,  # ADDIU T1, R0, 0x0016
    0x11090004,  # BEQ   T0, T1, [forward 0x04]
    0x3C048034,  # LUI   A0, 0x8034
    0x24842ACC,  # ADDIU A0, A0, 0x2ACC
    0x08000660,  # J     0x80001980
    0x24052125,  # ADDIU A1, R0, 0x2125
    0x03E00008   # JR    RA
]

the_deep_freezer = [
    # Writes 000C0000 into the player state to freeze the player on the spot if Ice Traps have been received, writes the
    # Ice Trap code into the pointer value (0x20B8, which is also Camilla's boss code),and decrements the Ice Traps
    # remaining counter. All after verifying the player is in a "safe" state to be frozen in.
    0x3C0B8039,  # LUI   T3, 0x8039
    0x91699BE2,  # LBU   T3, 0x9BE2 (T0)
    0x11200015,  # BEQZ  T1,     [forward 0x15]
    0x3C088034,  # LUI   T0, 0x8034
    0x910827A9,  # LBU   T0, 0x27A9 (T0)
    0x240A0005,  # ADDIU T2, R0, 0x0005
    0x110A0011,  # BEQ   T0, T2, [forward 0x11]
    0x240A000C,  # ADDIU T2, R0, 0x000C
    0x110A000F,  # BEQ   T0, T2, [forward 0x0F]
    0x240A0002,  # ADDIU T2, R0, 0x0002
    0x110A000D,  # BEQ   T0, T2, [forward 0x0D]
    0x240A0008,  # ADDIU T2, R0, 0x0008
    0x110A000B,  # BEQ   T0, T2, [forward 0x0B]
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA1699BE2,  # SB    T1, 0x9BE2 (T3)
    0x3C088034,  # LUI   T0, 0x8034
    0x3C09000C,  # LUI   T1, 0x000C
    0xAD0927A8,  # SW    T1, 0x27A8 (T0)
    0x240C20B8,  # ADDIU T4, R0, 0x20B8
    0xA56C9E6E,  # SH    T4, 0x9E6E (T3)
    0x8D0927C8,  # LW    T1, 0x27C8 (T0)
    0x912A0048,  # LBU   T2, 0x0068 (T1)
    0x314A007F,  # ANDI  T2, T2, 0x007F
    0xA12A0048,  # SB    T2, 0x0068 (T1)
    0x03E00008   # JR    RA
]

freeze_verifier = [
    # Verifies for the ice chunk module that a freeze should spawn the ice model. The player must be in the frozen state
    # (0x000C) and 0x20B8 must be in either the freeze pointer value or the current boss ID (Camilla's); otherwise, we
    # weill assume that the freeze happened due to a vampire grab or Actrise shard tornado and not spawn the ice chunk.
    0x8C4E000C,  # LW    T6, 0x000C (V0)
    0x00803025,  # OR    A2, A0, R0
    0x8DC30008,  # LW    V1, 0x0008 (T6)
    0x3C088039,  # LUI   T0, 0x8039
    0x240920B8,  # ADDIU T1, R0, 0x20B8
    0x950A9E72,  # LHU   T2, 0x9E72 (T0)
    0x3C0C8034,  # LUI   T4, 0x8034
    0x918C27A9,  # LBU   T4, 0x27A9 (T4)
    0x240D000C,  # ADDIU T5, R0, 0x000C
    0x158D0004,  # BNE   T4, T5, [forward 0x04]
    0x3C0B0F00,  # LUI   T3, 0x0F00
    0x112A0005,  # BEQ   T1, T2, [forward 0x05]
    0x950A9E78,  # LHU   T2, 0x9E78 (T0)
    0x112A0003,  # BEQ   T1, T2, [forward 0x03]
    0x357996A0,  # ORI   T9, T3, 0x96A0
    0x03200008,  # JR    T9
    0x00000000,  # NOP
    0x35799640,  # ORI   T9, T3, 0x9640
    0x03200008,  # JR    T9
]

countdown_extra_safety_check = [
    # Checks to see if the multiworld message is a red flashing trap before then truly deciding to decrement the
    # Countdown number. This was a VERY last minute thing I caught, since Ice Traps for other CV64 players can take the
    # appearance of majors with no other way of the game knowing.
    0x3C0B8019,  # LUI   T3, 0x8019
    0x956BBF98,  # LHU   T3, 0xBF98 (T3)
    0x240C0000,  # ADDIU T4, R0, 0x0000
    0x358CA20B,  # ORI   T4, T4, 0xA20B
    0x556C0001,  # BNEL  T3, T4, [forward 0x01]
    0xA1099CA4,  # SB    T1, 0x9CA4 (T0)
    0x03E00008   # JR    RA
]

countdown_demo_hider = [
    # Hides the Countdown number if we are not in the Gameplay state (state 2), which would happen if we were in the
    # Demo state (state 9). This is to ensure the demo maps' number is not peep-able before starting a run proper, for
    # the sake of preventing a marginal unfair advantage. Otherwise, updates the number once per frame.
    0x3C088039,  # LUI   T0, 0x8039
    0x91089EE1,  # LBU   T0, 0x9EE1 (T0)
    0x3C098040,  # LUI   T1, 0x8040
    0x01284821,  # ADDU  T1, T1, T0
    0x0C0FF507,  # JAL   0x803FD41C
    0x9124D6DC,  # LBU   A0, 0xD6DC (T1)
    0x3C088034,  # LUI   T0, 0x8034
    0x91092087,  # LBU   T0, 0x2087 (T0)
    0x240A0002,  # ADDIU T2, R0, 0x0002
    0x112A0003,  # BEQ   T1, T2, [forward 0x03]
    0x3C048040,  # LUI   A0, 0x8040
    0x8C84D6D4,  # LW    A0, 0xD6D4 (A0)
    0x0C0FF59F,  # JAL   0x803FD67C
    0x24050000,  # ADDIU A1, R0, 0x0000
    0x080FF411,  # J     0x803FD044
]

item_drop_spin_corrector = [
    # Corrects how far AP-placed items drop and how fast they spin based on what appearance they take.

    # Pickup actor ID table for the item appearance IDs to reference.
    0x01020304,
    0x05060708,
    0x090A0B0C,
    0x100D0E0F,
    0x11121314,
    0x15161718,
    0x191D1E1F,
    0x20212223,
    0x24252627,
    0x28291A1B,
    0x1C000000,
    0x00000000,
    # Makes AP-placed items in 1-hit breakables drop to their correct, dev-intended height depending on what appearance
    # we gave it. Primarily intended for the Axe and the Cross to ensure they don't land half buried in the ground.
    0x000C4202,  # SRL   T0, T4, 8
    0x318C00FF,  # ANDI  T4, T4, 0x00FF
    0x11000003,  # BEQZ  T0,     [forward 0x03]
    0x3C098040,  # LUI   T1, 0x8040
    0x01284821,  # ADDU  T1, T1, T0
    0x912CE7DB,  # LBU   T4, 0xE7D8
    0x03E00008,  # JR    RA
    0xAC600000,  # SW    R0, 0x0000 (V1)
    0x00000000,  # NOP
    # Makes items with changed appearances spin at their correct speed. Unless it's a local Ice Trap, wherein it will
    # instead spin at the speed it isn't supposed to.
    0x920B0040,  # LBU   T3, 0x0040 (S0)
    0x1160000D,  # BEQZ  T3,     [forward 0x0D]
    0x3C0C8040,  # LUI   T4, 0x8040
    0x016C6021,  # ADDU  T4, T3, T4
    0x918CE7DB,  # LBU   T4, 0xE7DB (T4)
    0x258CFFFF,  # ADDIU T4, T4, 0xFFFF
    0x240D0011,  # ADDIU T5, R0, 0x0011
    0x154D0006,  # BNE   T2, T5, [forward 0x06]
    0x29AE0006,  # SLTI  T6, T5, 0x0006
    0x240A0001,  # ADDIU T2, R0, 0x0001
    0x55C00001,  # BNEZL T6,     [forward 0x01]
    0x240A0007,  # ADDIU T2, R0, 0x0007
    0x10000002,  # B             [forward 0x02]
    0x00000000,  # NOP
    0x258A0000,  # ADDIU T2, T4, 0x0000
    0x08049648,  # J     0x80125920
    0x3C028017,  # LUI   V0, 0x8017
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    # Makes AP-placed items in 3-hit breakables drop to their correct, dev-intended height depending on what appearance
    # we gave it.
    0x00184202,  # SRL   T0, T8, 8
    0x331800FF,  # ANDI  T8, T8, 0x00FF
    0x11000003,  # BEQZ  T0,     [forward 0x03]
    0x3C098040,  # LUI   T1, 0x8040
    0x01284821,  # ADDU  T1, T1, T0
    0x9138E7DB,  # LBU   T8, 0xE7D8
    0x03E00008,  # JR    RA
    0xAC60FFD8,  # SW    R0, 0xFFD8 (V1)
    0x00000000,
    # Makes AP-placed items in the Villa chandelier drop to their correct, dev-intended height depending on what
    # appearance we gave it. (why must this singular breakable be such a problem child with its own code? :/)
    0x000D4202,  # SRL   T0, T5, 8
    0x31AD00FF,  # ANDI  T5, T5, 0x00FF
    0x11000003,  # BEQZ  T0,     [forward 0x03]
    0x3C098040,  # LUI   T1, 0x8040
    0x01284821,  # ADDU  T1, T1, T0
    0x912DE7DB,  # LBU   T5, 0xE7D8
    0x03E00008,  # JR    RA
    0xAC60FFD8,  # SW    R0, 0xFFD8 (V1)
]

big_tosser = [
    # Makes every hit the player takes that does not immobilize them send them flying backwards with the power of
    # Behemoth's charge.
    0x3C0A8038,  # LUI   T2, 0x8038
    0x914A7D7E,  # LBU   T2, 0x7D7E (T2)
    0x314A0020,  # ANDI  T2, T2, 0x0020
    0x1540000D,  # BEQZ  T2,     [forward 0x0D]
    0x3C0A800E,  # LUI   T2, 0x800E
    0x954B8290,  # LHU   T3, 0x8290 (T2)
    0x356B2000,  # ORI   T3, T3, 0x2000
    0xA54B8290,  # SH    T3, 0x8290 (T2)
    0x3C0C8035,  # LUI   T4, 0x8035
    0x958C09DE,  # LHU   T4, 0x09DE (T4)
    0x258C8000,  # ADDIU T4, T4, 0x8000
    0x3C0D8039,  # LUI   T5, 0x8039
    0xA5AC9CF0,  # SH    T4, 0x9CF0 (T5)
    0x3C0C4160,  # LUI   T4, 0x4160
    0xADAC9CF4,  # SW    T4, 0x9CF4 (T5)
    0x3C0C4040,  # LUI   T4, 0x4040
    0xADAC9CF8,  # SW    T4, 0x9CF8 (T5)
    0x03E00008,  # JR    RA
    0x8C680048,  # LW    T0, 0x0048 (V1)
    0x00000000,
    0x00000000,
    # Allows pressing A while getting launched to cancel all XZ momentum. Useful for saving oneself from getting
    # launched into an instant death trap.
    0x3C088038,  # LUI   T0, 0x8038
    0x91087D80,  # LBU   T0, 0x7D80 (T0)
    0x31090080,  # ANDI  T1, T0, 0x0080
    0x11200009,  # BEQZ  T1,     [forward 0x09]
    0x3C088035,  # LUI   T0, 0x8035
    0x8D0A079C,  # LW    T2, 0x079C (T0)
    0x3C0B000C,  # LUI   T3, 0x000C
    0x256B4000,  # ADDIU T3, T3, 0x4000
    0x014B5024,  # AND   T2, T2, T3
    0x154B0003,  # BNE   T2, T3, [forward 0x03]
    0x00000000,  # NOP
    0xAD00080C,  # SW    R0, 0x080C (T0)
    0xAD000814,  # SW    R0, 0x0814 (T0)
    0x03200008   # JR    T9
]

dog_bite_ice_trap_fix = [
    # Sets the freeze timer to 0 when a maze garden dog bites the player to ensure the ice chunk model will break if the
    # player gets bitten while frozen via Ice Trap.
    0x3C088039,  # LUI   T0, 0x8039
    0xA5009E76,  # SH    R0, 0x9E76 (T0)
    0x3C090F00,  # LUI   T1, 0x0F00
    0x25291CB8,  # ADDIU T1, T1, 0x1CB8
    0x01200008   # JR    T1
]

shimmy_speed_modifier = [
    # Increases the player's speed while shimmying as long as they are not holding down Z. If they are holding Z, it
    # will be the normal speed, allowing it to still be used to set up any tricks that might require the normal speed
    # (like Left Tower Skip).
    0x3C088038,  # LUI   T0, 0x8038
    0x91087D7E,  # LBU   T0, 0x7D7E (T0)
    0x31090020,  # ANDI  T1, T0, 0x0020
    0x3C0A800A,  # LUI   T2, 0x800A
    0x240B005A,  # ADDIU T3, R0, 0x005A
    0x55200001,  # BNEZL T1,     [forward 0x01]
    0x240B0032,  # ADDIU T3, R0, 0x0032
    0xA14B3641,  # SB    T3, 0x3641 (T2)
    0x0800B7C3   # J     0x8002DF0C
]
