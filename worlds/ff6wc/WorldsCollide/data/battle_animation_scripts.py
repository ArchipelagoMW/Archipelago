# List of addresses within the Battle Animation Scripts for the following commands which cause screen flashes:
#  B0 - Set background palette color addition (absolute)
#  B5 - Add color to background palette (relative)
#  AF - Set background palette color subtraction (absolute)
#  B6 - Subtract color from background palette (relative)
# By changing address + 1 to E0 (for absolute) or F0 (for relative), it causes no change to the background color (that is, no flash)
BATTLE_ANIMATION_FLASHES = {
    "Goner": [
        0x100088, # AF E0 - set background color subtraction to 0 (black)
        0x10008C, # B6 61 - increase background color subtraction by 1 (red)
        0x100092, # B6 31 - decrease background color subtraction by 1 (yellow)
        0x100098, # B6 81 - increase background color subtraction by 1 (cyan)
        0x1000A1, # B6 91 - decrease background color subtraction by 1 (cyan)
        0x1000A3, # B6 21 - increase background color subtraction by 1 (yellow)
        0x1000D3, # B6 8F - increase background color subtraction by 15 (cyan)
        0x1000DF, # B0 FF - set background color addition to 31 (white)
        0x100172, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Final KEFKA Death": [
        0x10023A, # B0 FF - set background color addition to 31 (white)
        0x100240, # B5 F4 - decrease background color addition by 4 (white)
        0x100248, # B0 FF - set background color addition to 31 (white)
        0x10024E, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "Atom Edge": [ # Also True Edge
        0x1003D0, # AF E0 - set background color subtraction to 0 (black)
        0x1003DD, # B6 E1 - increase background color subtraction by 1 (black)
        0x1003E6, # B6 E1 - increase background color subtraction by 1 (black)
        0x10044B, # B6 F1 - decrease background color subtraction by 1 (black)
        0x100457, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "Boss Death": [
        0x100476, # B0 FF - set background color addition to 31 (white)
        0x10047C, # B5 F4 - decrease background color addition by 4 (white)
        0x100484, # B0 FF - set background color addition to 31 (white)
        0x100497, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "Transform into Magicite": [
        0x100F30, # B0 FF - set background color addition to 31 (white)
        0x100F3F, # B5 F2 - decrease background color addition by 2 (white)
        0x100F4E, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Purifier": [
        0x101340, # AF E0 - set background color subtraction to 0 (black)
        0x101348, # B6 62 - increase background color subtraction by 2 (red)
        0x101380, # B6 81 - increase background color subtraction by 1 (cyan)
        0x10138A, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "Wall": [
        0x10177B, # AF E0 - set background color subtraction to 0 (black)
        0x10177F, # B6 61 - increase background color subtraction by 1 (red)
        0x101788, # B6 51 - decrease background color subtraction by 1 (magenta)
        0x101791, # B6 81 - increase background color subtraction by 1 (cyan)
        0x10179A, # B6 31 - decrease background color subtraction by 1 (yellow)
        0x1017A3, # B6 41 - increase background color subtraction by 1 (magenta)
        0x1017AC, # B6 91 - decrease background color subtraction by 1 (cyan)
        0x1017B5, # B6 51 - decrease background color subtraction by 1 (magenta)
        ],
    "Pearl": [
        0x10190E, # B0 E0 - set background color addition to 0 (white)
        0x101913, # B5 E2 - increase background color addition by 2 (white)
        0x10191E, # B5 F1 - decrease background color addition by 1 (white)
        0x10193E, # B6 C2 - increase background color subtraction by 2 (blue)
        ],
    "Ice 3": [
        0x101978, # B0 FF - set background color addition to 31 (white)
        0x10197B, # B5 F4 - decrease background color addition by 4 (white)
        0x10197E, # B5 F4 - decrease background color addition by 4 (white)
        0x101981, # B5 F4 - decrease background color addition by 4 (white)
        0x101984, # B5 F4 - decrease background color addition by 4 (white)
        0x101987, # B5 F4 - decrease background color addition by 4 (white)
        0x10198A, # B5 F4 - decrease background color addition by 4 (white)
        0x10198D, # B5 F4 - decrease background color addition by 4 (white)
        0x101990, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "Fire 3": [
        0x1019FA, # B0 9F - set background color addition to 31 (red)
        0x101A1C, # B5 94 - decrease background color addition by 4 (red)
        ],
    "Sleep": [
        0x101A23, # AF E0 - set background color subtraction to 0 (black)
        0x101A29, # B6 E1 - increase background color subtraction by 1 (black)
        0x101A33, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "7-Flush": [
        0x101B43, # AF E0 - set background color subtraction to 0 (black)
        0x101B47, # B6 61 - increase background color subtraction by 1 (red)
        0x101B4D, # B6 51 - decrease background color subtraction by 1 (magenta)
        0x101B53, # B6 81 - increase background color subtraction by 1 (cyan)
        0x101B59, # B6 31 - decrease background color subtraction by 1 (yellow)
        0x101B5F, # B6 41 - increase background color subtraction by 1 (magenta)
        0x101B65, # B6 91 - decrease background color subtraction by 1 (cyan)
        0x101B6B, # B6 51 - decrease background color subtraction by 1 (magenta)
        ],
    "H-Bomb": [
        0x101BC5, # B0 E0 - set background color addition to 0 (white)
        0x101BC9, # B5 E1 - increase background color addition by 1 (white)
        0x101C13, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Revenger": [
        0x101C62, # AF E0 - set background color subtraction to 0 (black)
        0x101C66, # B6 81 - increase background color subtraction by 1 (cyan)
        0x101C6C, # B6 41 - increase background color subtraction by 1 (magenta)
        0x101C72, # B6 91 - decrease background color subtraction by 1 (cyan)
        0x101C78, # B6 21 - increase background color subtraction by 1 (yellow)
        0x101C7E, # B6 51 - decrease background color subtraction by 1 (magenta)
        0x101C84, # B6 81 - increase background color subtraction by 1 (cyan)
        0x101C86, # B6 31 - decrease background color subtraction by 1 (yellow)
        0x101C8C, # B6 91 - decrease background color subtraction by 1 (cyan)
        ],
    "Phantasm": [
        0x101DFD, # AF E0 - set background color subtraction to 0 (black)
        0x101E03, # B6 E1 - increase background color subtraction by 1 (black)
        0x101E07, # B0 FF - set background color addition to 31 (white)
        0x101E0D, # B5 F4 - decrease background color addition by 4 (white)
        0x101E15, # B6 E2 - increase background color subtraction by 2 (black)
        0x101E1F, # B0 FF - set background color addition to 31 (white)
        0x101E27, # B5 F4 - decrease background color addition by 4 (white)
        0x101E2F, # B6 E2 - increase background color subtraction by 2 (black)
        0x101E3B, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "TigerBreak": [
        0x10240D, # B0 FF - set background color addition to 31 (white)
        0x102411, # B5 F2 - decrease background color addition by 2 (white)
        0x102416, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Metamorph": [
        0x102595, # AF E0 - set background color subtraction to 0 (black)
        0x102599, # B6 61 - increase background color subtraction by 1 (red)
        0x1025AF, # B6 71 - decrease background color subtraction by 1 (red)
        ],
    "Cat Rain": [
        0x102677, # B0 FF - set background color addition to 31 (white)
        0x10267B, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Charm": [
        0x1026EE, # B0 FF - set background color addition to 31 (white)
        0x1026FB, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Mirager": [
        0x102791, # B0 FF - set background color addition to 31 (white)
        0x102795, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "SabreSoul": [
        0x1027D3, # B0 FF - set background color addition to 31 (white)
        0x1027DA, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Back Blade": [
        0x1028D3, # AF FF - set background color subtraction to 31 (black)
        0x1028DF, # B6 F4 - decrease background color subtraction by 4 (black)
        ],
    "RoyalShock": [
        0x102967, # B0 FF - set background color addition to 31 (white)
        0x10296B, # B5 F2 - decrease background color addition by 2 (white)
        0x102973, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Overcast": [
        0x102C3A, # AF E0 - set background color subtraction to 0 (black)
        0x102C55, # B6 E1 - increase background color subtraction by 1 (black)
        0x102C8D, # B6 F1 - decrease background color subtraction by 1 (black)
        0x102C91, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "Disaster": [
        0x102CEE, # AF E0 - set background color subtraction to 0 (black)
        0x102CF2, # B6 E1 - increase background color subtraction by 1 (black)
        0x102D19, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "ForceField": [
        0x102D3A, # B0 E0 - set background color addition to 0 (white)
        0x102D48, # B5 E1 - increase background color addition by 1 (white)
        0x102D64, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Terra/Tritoch Lightning": [
        0x102E05, # B0 E0 - set background color addition to 0 (white)
        0x102E09, # B5 81 - increase background color addition by 1 (red)
        0x102E24, # B5 61 - increase background color addition by 1 (cyan)
        ],
    "S. Cross": [
        0x102EDA, # AF E0 - set background color subtraction to 0 (black)
        0x102EDE, # B6 E2 - increase background color subtraction by 2 (black)
        0x102FA8, # B6 F2 - decrease background color subtraction by 2 (black)
        0x102FB1, # B0 E0 - set background color addition to 0 (white)
        0x102FBE, # B5 E2 - increase background color addition by 2 (white)
        0x102FD9, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Mind Blast": [
        0x102FED, # B0 E0 - set background color addition to 0 (white)
        0x102FF1, # B5 81 - increase background color addition by 1 (red)
        0x102FF7, # B5 91 - decrease background color addition by 1 (red)
        0x102FF9, # B5 21 - increase background color addition by 1 (blue)
        0x102FFF, # B5 31 - decrease background color addition by 1 (blue)
        0x103001, # B5 C1 - increase background color addition by 1 (yellow)
        0x103007, # B5 91 - decrease background color addition by 1 (red)
        0x10300D, # B5 51 - decrease background color addition by 1 (green)
        0x103015, # B5 E2 - increase background color addition by 2 (white)
        0x10301F, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Flare Star": [
        0x1030F5, # B0 E0 - set background color addition to 0 (white)
        0x103106, # B5 81 - increase background color addition by 1 (red)
        0x10310D, # B5 E2 - increase background color addition by 2 (white)
        0x103123, # B5 71 - decrease background color addition by 1 (cyan)
        0x10312E, # B5 91 - decrease background color addition by 1 (red)
        ],
    "Quasar": [
        0x1031D2, # AF E0 - set background color subtraction to 0 (black)
        0x1031D6, # B6 E1 - increase background color subtraction by 1 (black)
        0x1031FA, # B6 F1 - decrease background color subtraction by 1 (black)
        ],
    "R.Polarity": [
        0x10328B, # B0 FF - set background color addition to 31 (white)
        0x103292, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Rippler": [
        0x1033C6, # B0 FF - set background color addition to 31 (white)
        0x1033CA, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Step Mine": [
        0x1034D9, # B0 FF - set background color addition to 31 (white)
        0x1034E0, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "L.5 Doom": [
        0x1035E6, # B0 FF - set background color addition to 31 (white)
        0x1035F6, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "Megazerk": [
        0x103757, # B0 80 - set background color addition to 0 (red)
        0x103761, # B5 82 - increase background color addition by 2 (red)
        0x10378F, # B5 92 - decrease background color addition by 2 (red)
        0x103795, # B5 92 - decrease background color addition by 2 (red)
        0x10379B, # B5 92 - decrease background color addition by 2 (red)
        0x1037A1, # B5 92 - decrease background color addition by 2 (red)
        0x1037A7, # B5 92 - decrease background color addition by 2 (red)
        0x1037AD, # B5 92 - decrease background color addition by 2 (red)
        0x1037B3, # B5 92 - decrease background color addition by 2 (red)
        0x1037B9, # B5 92 - decrease background color addition by 2 (red)
        0x1037C0, # B5 92 - decrease background color addition by 2 (red)
        ],
    "Schiller": [
        0x103819, # B0 FF - set background color addition to 31 (white)
        0x10381D, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "WallChange": [
        0x10399E, # B0 FF - set background color addition to 31 (white)
        0x1039A3, # B5 F2 - decrease background color addition by 2 (white)
        0x1039A9, # B5 F2 - decrease background color addition by 2 (white)
        0x1039AF, # B5 F2 - decrease background color addition by 2 (white)
        0x1039B5, # B5 F2 - decrease background color addition by 2 (white)
        0x1039BB, # B5 F2 - decrease background color addition by 2 (white)
        0x1039C1, # B5 F2 - decrease background color addition by 2 (white)
        0x1039C7, # B5 F2 - decrease background color addition by 2 (white)
        0x1039CD, # B5 F2 - decrease background color addition by 2 (white)
        0x1039D4, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Ultima": [
        0x1056CB, # AF 60 - set background color subtraction to 0 (red)
        0x1056CF, # B6 C2 - increase background color subtraction by 2 (blue)
        0x1056ED, # B0 FF - set background color addition to 31 (white)
        0x1056F5, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Bolt 3": [ # Also Giga Volt
        0x10588E, # B0 FF - set background color addition to 31 (white)
        0x105893, # B5 F4 - decrease background color addition by 4 (white)
        0x105896, # B5 F4 - decrease background color addition by 4 (white)
        0x105899, # B5 F4 - decrease background color addition by 4 (white)
        0x10589C, # B5 F4 - decrease background color addition by 4 (white)
        0x1058A1, # B5 F4 - decrease background color addition by 4 (white)
        0x1058A6, # B5 F4 - decrease background color addition by 4 (white)
        0x1058AB, # B5 F4 - decrease background color addition by 4 (white)
        0x1058B0, # B5 F4 - decrease background color addition by 4 (white)
        ],
    "X-Zone": [
        0x105A5D, # B0 FF - set background color addition to 31 (white)
        0x105A6A, # B5 F2 - decrease background color addition by 2 (white)
        0x105A79, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Dispel": [
        0x105DC2, # B0 FF - set background color addition to 31 (white)
        0x105DC9, # B5 F1 - decrease background color addition by 1 (white)
        0x105DD2, # B5 F1 - decrease background color addition by 1 (white)
        0x105DDB, # B5 F1 - decrease background color addition by 1 (white)
        0x105DE4, # B5 F1 - decrease background color addition by 1 (white)
        0x105DED, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Muddle": [ # Also L.3 Muddle, Confusion
        0x1060EA, # B0 FF - set background color addition to 31 (white)
        0x1060EE, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Shock": [
        0x1068BE, # B0 FF - set background color addition to 31 (white)
        0x1068D0, # B5 F1 - decrease background color addition by 1 (white)
        ],
    "Bum Rush": [
        0x106C3E, # B0 E0 - set background color addition to 0 (white)
        0x106C47, # B0 E0 - set background color addition to 0 (white)
        0x106C53, # B0 E0 - set background color addition to 0 (white)
        0x106C7E, # B0 FF - set background color addition to 31 (white)
        0x106C87, # B0 E0 - set background color addition to 0 (white)
        0x106C95, # B0 FF - set background color addition to 31 (white)
        0x106C9E, # B0 E0 - set background color addition to 0 (white)
        ],
    "Stunner": [
        0x1071BA, # B0 20 - set background color addition to 0 (blue)
        0x1071C1, # B5 24 - increase background color addition by 4 (blue)
        0x1071CA, # B5 24 - increase background color addition by 4 (blue)
        0x1071D5, # B5 24 - increase background color addition by 4 (blue)
        0x1071DE, # B5 24 - increase background color addition by 4 (blue)
        0x1071E9, # B5 24 - increase background color addition by 4 (blue)
        0x1071F2, # B5 24 - increase background color addition by 4 (blue)
        0x1071FD, # B5 24 - increase background color addition by 4 (blue)
        0x107206, # B5 24 - increase background color addition by 4 (blue)
        0x107211, # B5 24 - increase background color addition by 4 (blue)
        0x10721A, # B5 24 - increase background color addition by 4 (blue)
        0x10725A, # B5 32 - decrease background color addition by 2 (blue)
        ],
    "Quadra Slam": [ # Also Quadra Slice
        0x1073DC, # B0 FF - set background color addition to 31 (white)
        0x1073EE, # B5 F2 - decrease background color addition by 2 (white)
        0x1073F3, # B5 F2 - decrease background color addition by 2 (white)
        0x107402, # B0 5F - set background color addition to 31 (green)
        0x107424, # B5 54 - decrease background color addition by 4 (green)
        0x107429, # B5 54 - decrease background color addition by 4 (green)
        0x107436, # B0 3F - set background color addition to 31 (blue)
        0x107458, # B5 34 - decrease background color addition by 4 (blue)
        0x10745D, # B5 34 - decrease background color addition by 4 (blue)
        0x107490, # B0 9F - set background color addition to 31 (red)
        0x1074B2, # B5 94 - decrease background color addition by 4 (red)
        0x1074B7, # B5 94 - decrease background color addition by 4 (red)
        ],
    "Slash": [
        0x1074F4, # B0 FF - set background color addition to 31 (white)
        0x1074FD, # B5 F2 - decrease background color addition by 2 (white)
        0x107507, # B5 F2 - decrease background color addition by 2 (white)
        ],
    "Flash": [
        0x107850, # B0 FF - set background color addition to 31 (white)
        0x10785C, # B5 F1 - decrease background color addition by 1 (white)
        ]
}

