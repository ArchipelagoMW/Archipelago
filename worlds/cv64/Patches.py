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
    0x11600003,  # BEQZ  T3, [forward 0x03]
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
    0x55600001,  # BNEZL T3, [forward 0x01]
    0x27FF0010,  # ADDIU RA, RA, 0x0010
    0x03E00008   # JR    RA
]

stage_select_overwrite = [
    # Replacement for the "wipe world state" function when using the warp menu. Now it's the "Special1 jewel checker"
    # to see how many destinations can be selected on it with the current count.
    0x8FA60018,  # LW	 A2, 0x0018 (SP)
    0xA0606437,  # SB	 R0, 0x6437 (V1)
    0x10000029,  # B	 [forward 0x29]
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
    0x15000007,  # BNEZ  T0, [forward 0x07]
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
    0x11200006,  # BEQZ	 T1, [forward 0x06]
    0x00000000,  # NOP
    0x11400002,  # BEQZ  T2, [forward 0x02]
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
    0x10000005,  # B	 [forward 0x05]
    0x256B0002,  # ADDIU T3, T3, 0x0002
    0x2409000F,  # ADDIU T1, R0, 0x000F
    0xA1690001,  # SB	 T1, 0x0001 (T3)
    0x0804EDCE,  # J	 0x8013B738
    0xA1600000,  # SB	 R0, 0x0000 (T3)
    0x91640000,  # LBU	 A0, 0x0000 (T3)
    0x14800002,  # BNEZ	 A0, [forward 0x02]
    0x00000000,  # NOP
    0x10000003,  # B     [forward 0x03]
    0x2409000F,  # ADDIU T1, R0, 0x000F
    0x080FF4D1,  # J	 0x803FD344
    0xA169FFFF,  # SB	 T1, 0xFFFF (T3)
    # DeathLink-specific checks
    0x3C0B8039,  # LUI   T3, 0x8039
    0x256B9BE1,  # ADDIU T3, T3, 0x9BE1
    0x95640001,  # LHU   A0, 0x0001 (T3)
    0x14800002,  # BNEZ  A0, [forward 0x02]
    0x916900A7,  # LBU   T1, 0x00A7 (T3)
    0x03E00008,  # JR    RA
    0x312A0080,  # ANDI  T2, T1, 0x0080
    0x11400002,  # BEQZ  T2, [forward 0x02]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x35290080,  # ORI   T1, T1, 0x0080
    0xA16900A7,  # SB    T1, 0x00A7 (T3)
    0x2484FFFF,  # ADDIU A0, A0, 0xFFFF
    0x03E00008,  # JR    RA
]

deathlink_counter_decrementer = [
    # Decrements the DeathLink counter if it's above zero upon loading a previous state. Checking this number will be
    # how the client will tell if a player's cause of death was something in-game or a DeathLink (and send a DeathLink
    # to the server if it was the former). Also resets the remote item values to 00 so the player's received items don't
    # get mucked up in-game.
    0x3C088039,  # LUI   T0, 0x8039
    0x95099BE2,  # LHU   T1, 0x9BE2 (T0)
    0x11200002,  # BEQZ  T1, 0x803FC154
    0x2529FFFF,  # ADDIU T1, T1, 0xFFFF
    0xA5099BE2,  # SH    T1, 0x9BE2
    0x240900FF,  # ADDIU T1, R0, 0x00FF
    0xA1099BE0,  # SB    T1, 0x9BE0 (T0)
    0xA1009BDF,  # SB	 R0, 0x9BDF (T0)
    0x03E00008,  # JR    RA
    0xA1009BE1   # SB	 R0, 0x9BE1 (T0)
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
    0x51400001,  # BEQZL T2, [forward 0x01]
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
    0x15090010,  # BNE   T0, T1, [forward 0x10]
    0x3C088035,  # LUI   T0, 0x8035
    0x9108F7D8,  # LBU   T0, 0xF7D8 (T0)
    0x24090020,  # ADDIU T1, R0, 0x0020
    0x1109000C,  # BEQ   T0, T1, [forward 0x0C]
    0x3C088039,  # LUI   T0, 0x8039
    0x91099BFA,  # LBU   T1, 0x9BFA (T0)
    0x31290001,  # ANDI  T1, T1, 0x0001
    0x15200008,  # BNEZ  T1, [forward 0x08]
    0x8D099EE0,  # LW    T1, 0x9EE0
    0x3C0A001B,  # LUI   T2, 0x001B
    0x254A0003,  # ADDIU T2, T2, 0x0003
    0x112A0004,  # BEQ   T1, T2, [forward 0x04]
    0x2408FFFC,  # ADDIU T0, R0, 0xFFFC
    0x3C098034,  # LUI   T1, 0x8034
    0x0804DA70,  # J     0x80136960
    0xAD282084,  # SW    T0, 0x2084 (T1)
    0x0804DA70,  # J     0x80136960
    0xA44E6436   # SH    T6, 0x6436 (V0)
]

give_subweapon_stopper = [
    # Extension to "give subweapon" function to not change the player's weapon if the received item is a Stake or Rose.
    # Can also jump to prev_subweapon_dropper if applicable.
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x11240006,  # BEQ   T1, A0, [forward 0x06]
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x11240004,  # BEQ   T1, A0, [forward 0x04]
    0x9465618A,  # LHU   A1, 0x618A (V1)
    0xA46D618A,  # SH    T5, 0x618A (V1)
    0x0804F0BF,  # J     0x8013C2FC
    0x00000000,  # NOP
    0x0804F0BF,  # J     0x8013C2FC
]

give_powerup_stopper = [
    # Extension to "give PowerUp" function to not increase the player's PowerUp count beyond 2
    0x240D0002,  # ADDIU T5, R0, 0x0002
    0x556D0001,  # BNEL  T3, T5, [forward 1]
    0xA46C6234,  # SH    T4, 0x6234 (V1)
    0x0804F0BF   # J     0x8013C2FC
]

npc_item_hack = [
    # Hack to make NPC/shelf items show item textboxes when received.
    0x3C098039,  # LUI   T1, 0x8039
    0x240A0020,  # ADDIU T2, R0, 0x0020
    0xA12A9BE0,  # SB    T2, 0x9BE0 (T1)
    0x001F5602,  # SRL   T2, RA, 24
    0x240B0080,  # ADDIU T3, R0, 0x0080
    0x114B0019,  # BEQ   T2, T3, [forward 0x19]
    0xAFBF0014,  # SW    RA, 0x0014 (SP)
    0x240A0015,  # ADDIU T2, R0, 0x0015
    0x15440006,  # BNE   T2, A0, [forward 0x06]
    0x240B0015,  # ADDIU T3, R0, 0x0015
    0xA12B9BDF,  # SB    T3, 0x9BDF (T1)
    0x912C9BF0,  # LBU   T4, 0x9BF0 (T1)
    0x358C0080,  # ORI   T4, T4, 0x0080
    0xA12C9BF0,  # SB    T4, 0x9BF0 (T1)
    0x0804F0BF,  # J     0x8013C2FC
    0x240A0016,  # ADDIU T2, R0, 0x0016
    0x15440006,  # BNE   T2, A0, [forward 0x06]
    0x240B0016,  # ADDIU T3, R0, 0x0016
    0xA12B9BDF,  # SB    T3, 0x9BDF (T1)
    0x912C9C18,  # LBU   T4, 0x9C18 (T1)
    0x358C0080,  # ORI   T4, T4, 0x0080
    0xA12C9C18,  # SB    T4, 0x9C18 (T1)
    0x0804F0BF,  # J     0x8013C2FC
    0x240A001A,  # ADDIU T2, R0, 0x001A
    0x15440003,  # BNE   T2, A0, [forward 0x03]
    0x240B001A,  # ADDIU T3, R0, 0x001A
    0xA12B9BDF,  # SB    T3, 0x9BDF (T1)
    0x0804F0BF,  # J     0x8013C2FC
    0x240B001F,  # ADDIU T3, R0, 0x001F
    0x0804F0BF,  # J     0x8013C2FC
    0xA12B9BDF,  # SB    T3, 0x9BDF (T1)
    0x0804EFFD,  # J     0x8013C2FC
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
    # prevent placing them at the downstairs crack altogether until the seal is removed
    0x24090024,  # ADDIU T1, R0, 0x0024
    0x1509000F,  # BNE   T0, T1, [forward 0x0F]
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
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x3C0AA058,  # LUI   T2, 0xA058
    0x254A642B,  # ADDIU T2, T2, 0x642B
    0xAF2A0D88,  # SW    T2, 0x0D88 (T9)
    0xAF200D98,  # SW    R0, 0x0D98 (T9)
    0x03200008,  # JR    T9
]

double_component_checker = [
    # When checking to see if a bomb component can be placed at a cracked wall, this will run if the code lands at the
    # "no need to set 2" outcome to see if the other can be set.

    # Mandragora checker
    0x10400007,  # BEQZ  V0, [forward 0x07]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x31098000,  # ANDI  T1, T0, 0x8000
    0x15200008,  # BNEZ  T1, [forward 0x08]
    0x91499C5D,  # LBU   T1, 0x9C5D (T2)
    0x11200006,  # BEQZ  T1, 0x80183938
    0x00000000,  # NOP
    0x10000007,  # B     [forward 0x07]
    0x31E90100,  # ANDI  T1, T7, 0x0100
    0x15200002,  # BNEZ  T1, [forward 0x02]
    0x91499C5D,  # LBU   T1, 0x9C5D (T2)
    0x15200003,  # BNEZ  T1, [forward 0x03]
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
    0x10400007,  # BEQZ  V0, [forward 0x07]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x31694000,  # ANDI  T1, T3, 0x4000
    0x15200008,  # BNEZ  T1, [forward 0x08]
    0x91499C5C,  # LBU   T1, 0x9C5C
    0x11200006,  # BEQZ  T1, [forward 0x06]
    0x00000000,  # NOP
    0x1000FFF4,  # B     [backward 0x0B]
    0x914F9C18,  # LBU   T7, 0x9C18 (T2)
    0x31E90002,  # ANDI  T1, T7, 0x0002
    0x1520FFEC,  # BNEZ  T1, [backward 0x13]
    0x91499C5C,  # LBU   T1, 0x9C5C (T2)
    0x1520FFEF,  # BNEZ  T1, [backward 0x15]
    0x00000000,  # NOP
    0x1000FFE8,  # B     [backward 0x17]
    0x00000000,  # NOP
]

downstairs_seal_checker = [
    # This will run specifically for the downstairs crack to see if the seal has been removed before then deciding to
    # let the player set the bomb components or not. An anti-dick measure, since there is a limited number of each
    # component per world.
    0x14400004,  # BNEZ  V0, [forward 0x04]
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914A9C18,  # LBU   T2, 0x9C18 (T2)
    0x314A0001,  # ANDI  T2, T2, 0x0001
    0x11400003,  # BEQZ  T2, [forward 0x03]
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
    0x15090019,  # BNE   T0, T1, [forward 0x19]
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
    0x340A0000,  # ORI   T2, R0, 0x0000         <- Sub-weapons lower flag
    0xA44A009C,  # SH    T2, 0x009C (V0)
    0xA44A00AC,  # SH    T2, 0x00AC (V0)
    0xA44A00BC,  # SH    T2, 0x00BC (V0)
    0xA44A00CC,  # SH    T2, 0x00CC (V0)
    0x340A0000,  # ORI   T2, R0, 0x0000         <- Sub-weapons upper flags
    0x240B0000,  # ADDIU T3, R0, 0x0000
    0x240C0000,  # ADDIU T4, R0, 0x0000
    0x240D0000,  # ADDIU T5, R0, 0x0000
    0xA44A00CA,  # SH    T2, 0x00CA (V0)
    0xA44B00BA,  # SH    T3, 0x00BA (V0)
    0xA44C009A,  # SH    T4, 0x009A (V0)
    0xA44D00AA,  # SH    T5, 0x00AA (V0)
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    # Tunnel (replaces 1 invisible Cure Ampoule)
    0x24090007,  # ADDIU T1, R0, 0x0007
    0x15090006,  # BNE   T0, T1, [forward 0x06]
    0x340A0001,  # ORI   T2, R0, 0x0001         <- Bucket
    0xA44A0268,  # SH    T2, 0x0268 (V0)
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x1139FFC0,  # BEQ   T1, T9, [backward 0x3F]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Center factory floor (replaces 1 moneybag, 1 jewel, and gives every lizard man coffin item a unique flag)
    0x2409000B,  # ADDIU T1, R0, 0x000B
    0x15090012,  # BNE   T0, T1, [forward 0x12]
    0x340A001A,  # ORI   T2, R0, 0x0001         <- Lizard coffin nearside mid-right
    0x340B0003,  # ORI   T3, R0, 0x0001         <- Lizard coffin nearside mid-left
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
    0x1139FF9B,  # BEQ   T1, T9, [backward 0x63]
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
    0x1139FF8F,  # BEQ   T0, T1, [backward 0x70]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Castle Wall main area (sets a flag for the freestanding Holy Water if applicable and the "beginning of stage"
    # state if entered from the rear)
    0x24090002,  # ADDIU T1, R0, 0x0002
    0x15090006,  # BNE   T0, T1, [forward 0x06]
    0x24090004,  # ADDIU T1, R0, 0x0004
    0xA049009B,  # SB    T1, 0x009B (V0)
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x1139FF87,  # BEQ   T1, T9, [backward 0x79]
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
    0x1139FF7D,  # BEQ   T1, T9, [backward 0x84]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Underground Waterway (sets the "beginning of stage" state if entered from the rear)
    0x24090008,  # ADDIU T1, R0, 0x0008
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090001,  # ADDIU T1, R0, 0x0001
    0x1139FF77,  # BEQ   T1, T9, [backward 0x8B]
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
    0x1139FF6D,  # BEQ   T1, T9, [backward 0x96]
    0x24090003,  # ADDIU T1, R0, 0x0003
    0x1139FF6B,  # BEQ   T1, T9, [backward 0x98]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Execution (sets the "beginning of stage" state if entered from the rear)
    0x24090010,  # ADDIU T1, R0, 0x0010
    0x15090004,  # BNE   T0, T1, [forward 0x10]
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x1139FF65,  # BEQ   T1, T9, [backward 0x9B]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Sorcery (sets the "beginning of stage" state if entered from the rear)
    0x24090011,  # ADDIU T1, R0, 0x0011
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090013,  # ADDIU T1, R0, 0x0013
    0x1139FF5F,  # BEQ   T1, T9, [backward 0xA6]
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    # Tower of Science (sets the "beginning of stage" state if entered from the rear)
    0x24090012,  # ADDIU T1, R0, 0x0012
    0x15090004,  # BNE   T0, T1, [forward 0x04]
    0x24090004,  # ADDIU T1, R0, 0x0004
    0x1139FF59,  # BEQ   T1, T9, [backward 0xAD]
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
    0x1139FF4F,  # BEQ   T1, T9, [backward 0xB8]
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
    0x15090013,  # BNE   T0, T1, [forward 0x13]
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
    0x03E00008,  # JR    RA
    # Fan meeting room (sets "beginning of stage" flag)
    0x24090019,  # ADDIU T1, R0, 0x0019
    0x1109FF23,  # BEQ   T1, T9, [backward 0xE5]
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
    0x2442CC3C,  # ADDIU V0, V0, 0xCC3C
    0x03E00008   # JR    RA
]

coffin_time_checker = [
    # When entering the Villa coffin, this will check to see whether it's day or night and send you to either the Tunnel
    # or Underground Waterway level slot accordingly regardless of which character you are
    0x28490006,  # SLTI  T1, V0, 0x0006
    0x15200005,  # BNEZ  T1, [forward 0x05]
    0x28490012,  # SLTI  T1, V0, 0x0012
    0x11200003,  # BEQZ  T1, [forward 0x03]
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
    0x15C00003,  # BNEZ  T6, [forward 0x03]
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
    0x15C00005,  # BNEZ  T6, [forward 0x05]
    0x3C0E0020,  # LUI   T6, 0x0020
    0x014EC024,  # AND   T8, T2, T6
    0x014E5025,  # OR    T2, T2, T6
    0xAC4A613C,  # SW    T2, 0x613C (V0)
    0x17000003,  # BNEZ  T8, [forward 0x03]
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
    0x11200002,  # BEQZ  T1, [forward 0x02]
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

crystal_goal_checker = [
    # Checks the Castle Center basement crystal's flag to see if it has been activated and puts 0x0004 in V0 to disallow
    # opening Dracula's door if it hasn't been.
    0x3C0A8039,  # LUI   T2, 0x8039
    0x914B9C1B,  # LBU   T3, 0x9C1B (T2)
    0x316A0001,  # ANDI  T2, T3, 0x0001
    0x51400001,  # BEQZL T2, [forward 0x01]
    0x24020004,  # ADDIU V0, R0, 0x0004
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
    0x11800010,  # BEQZ  T4, [forward 0x10]
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
    0x11800005,  # BEQZ  T4, [forward 0x05]
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
    0x1000001F,  # B     [forward 0x1F]
    0x3C0F8000,  # LUI   T7, 0x8000
    # Warp 1
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x1000001B,  # B     [forward 0x1B]
    0x3C0F8040,  # LUI   T7, 0x8040
    # Warp 2
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x10000017,  # B     [forward 0x17]
    0x3C0F8080,  # LUI   T7, 0x8080
    # Warp 3
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x10000013,  # B     [forward 0x13]
    0x3C0F0080,  # LUI   T7, 0x0080
    # Warp 4
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x3C0F0080,  # LUI   T7, 0x0080
    0x1000000E,  # B     [forward 0x0E]
    0x25EF8000,  # ADDIU T7, T7, 0x8000
    # Warp 5
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x1000000A,  # B     [forward 0x0A]
    0x340F8000,  # ORI   T7, R0, 0x8000
    # Warp 6
    0x3C0E0000,  # LUI   T6, 0x0000
    0x25CE0000,  # ADDIU T6, T6, 0x0000
    0x3C0F8000,  # LUI   T7, 0x8000
    0x10000005,  # B     [forward 0x05]
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
    0x11400003,  # BEQZ  T2, [forward 0x03]
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
    # cursor on "Previously saved". Then jump to deathlink_counter_decrementer in the event we're loading a save from
    # the Game Over screen.
    0x3C088039,  # LUI    T0, 0x8039
    0xA1009BC0,  # SB     R0, 0x9BC0 (T0)
    0x080FF052   # J   0x803FC148
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
    0x10400003,  # BEQZ  V0, [forward 0x03]
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
    0x51800001,  # BEQZL T4, [forward 0x01]
    0x000B5C00,  # SLL   T3, T3, 16
    0x00006012,  # MFLO  T4
    0xA0CC0055,  # SB    T4, 0x0055 (A2)
    0xACCB0058,  # SW    T3, 0x0058 (A2)
    0x080494E5,  # J     0x80125394
    0x032A0019   # MULTU T9, T2
]

item_appearance_switcher = [
    # Determines an item's model appearance by checking to see if a different item appearance ID was written in a
    # specific spot in the actor's data; if one wasn't (or it is C0 since that is for invisibility), then the appearance
    # value will be grabbed from the item's entry in the item property table like normal instead.
    0x92080040,  # LBU   T0, 0x0040 (S0)
    0x240900C0,  # ADDIU T1, R0, 0x00C0
    0x11090003,  # BEQ   T0, T1, [forward 0x03]
    0x00000000,  # NOP
    0x55000001,  # BNEZL T0, T1, [forward 0x01]
    0x01002025,  # OR    A0, T0, R0
    0x03E00008,  # JR    RA
    0xAFA70024   # SW    A3, 0x0024 (SP)
]

item_model_visibility_switcher = [
    # If C0 is written in the appearance switch value in the item's actor data, parse 0C00 to the function that checks
    # if an item should be invisible or not. Otherwise, grab that setting from the item property table like normal.
    0x920B0040,  # LBU   T3, 0x0040 (S0)
    0x240E00C0,  # ADDIU T6, R0, 0x00C0
    0x156E0003,  # BNE   T3, T6, [forward 0x03]
    0x240D0C00,  # ADDIU T5, R0, 0x0C00
    0x03E00008,  # JR    RA
    0x00000000,  # NOP
    0x03E00008,  # JR    RA
    0x958D0004   # LHU   T5, 0x0004 (T4)
]

item_shine_visibility_switcher = [
    # Same as the above, but for item shines instead of the model.
    0x920B0040,  # LBU   T3, 0x0040 (S0)
    0x240900C0,  # ADDIU T1, R0, 0x00C0
    0x15690003,  # BNE   T3, T1, [forward 0x03]
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
    0x15200003,  # BNEZ  T1, [forward 0x03]
    0x00000000,  # NOP
    0x34098000,  # ORI   T1, R0, 0x8000
    0x25080001,  # ADDIU T0, T0, 0x0001
    0x0154582A,  # SLT   T3, T2, S4
    0x1560FFF9,  # BNEZ  T3, [backward 0x07]
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
    0x15200003,  # BNEZ  T1, [forward 0x03]
    0x00000000,  # NOP
    0x34098000,  # ORI   T1, R0, 0x8000
    0x25080001,  # ADDIU T0, T0, 0x0001
    0x0155582A,  # SLT   T3, T2, S5
    0x1560FFF9,  # BNEZ  T3, [backward 0x07]
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
    0x10AD0007,  # BEQ   A1, T5, [forward 0x07
    0x3C088040,  # LUI   T0, 0x8040
    0x01054021,  # ADDU  T0, T0, A1
    0x0C0FF416,  # JAL   0x803FD058
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
    0x0801AEB5   # J     0x8006BAD4
]

prev_subweapon_dropper = [
    # Spawns a pickup actor of the sub-weapon the player had before picking up a new one behind them at their current
    # position like in other CVs. This will enable them to pick it back up again if they still want it.
    # Courtesy of B_squo; see derp.c in the src folder for the C source code.
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
    0xC428D330,
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
    0xC424D334,
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
    0x3C038040,
    0x2463D328,
    0x906E0000,
    0x3C058040,
    0x3C018035,
    0x15C0001D,
    0x24A5D324,
    0xC42409D4,
    0x3C01800D,
    0xC4267B98,
    0x3C013F80,
    0x44815000,
    0x46062200,
    0x3C058040,
    0x24A5D324,
    0x2401000F,
    0x460A4400,
    0x240F0001,
    0xE4B00000,
    0x94820038,
    0x10410006,
    0x24010010,
    0x10410004,
    0x2401002F,
    0x10410002,
    0x24010030,
    0x14410005,
    0x3C014040,
    0x44812000,
    0xC4B20000,
    0x46049180,
    0xE4A60000,
    0xA06F0000,
    0x03E00008,
    0x24020001,
    0xC4800068,
    0xC4A80000,
    0x3C058039,
    0x24A59BD0,
    0x4608003E,
    0x00001025,
    0x45000005,
    0x00000000,
    0x44805000,
    0xA0600000,
    0x03E00008,
    0xE4AA0000,
    0x3C058039,
    0x24A59BD0,
    0x3C018019,
    0xC430C870,
    0xC4A20000,
    0x4610103C,
    0x00000000,
    0x45000006,
    0x3C018019,
    0xC432C878,
    0x46121100,
    0xE4A40000,
    0xC4A20000,
    0xC4800068,
    0x46020181,
    0x24020001,
    0xE4860068,
    0xC4880068,
    0xE4880034,
    0x03E00008,
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
    0x0804EDCE,  # J     0x8013B738
    0xA56C00DD,  # SH    T4, 0x00DD (T3)
    0x00000000,  # NOP
    0x03E00008   # JR    RA
]
