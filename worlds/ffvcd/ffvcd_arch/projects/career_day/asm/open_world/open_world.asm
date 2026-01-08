hirom


; These are for permanent changes to open world


; TYCOON CASTLE
; Move the guard out of the way of the vault

org $CE685A
db $15

; ZOKK
; First Zokk cutscene flag off
org $F04B4E
db $FB, $FB
org $F0574B
db $FB, $FB
org $F05752
db $FB, $FB

; Disable all NPCs except 1 zokk
org $CE63F0
pad $CE640C

; RIFT
; Stop Omega from moving
org $CE992B
db $04

; ANCIENT LIBRARY
; Change flag for checking cid mid event
;org $D8EF42
org $F04EC2
db $EE


; SYLDRA
; Change Syldra's event to be tied to $A2, $11  ($7E0A16 bit 02), which is 
; Early game Pirate cave access. Could be a quasi-key item later 
; org $D8EC45
org $F04BC5
db $11


; MUA FOREST
; Change checked flag from event code $A2, $71 to $A2, $72 ($000A22 bit 04 instead of 02)
; The reason for this is that $A22 bit 02 is connected to both guido and mua forest
; BUt Bit 04 is specifically tied to the fast 'reentrance' of mua forest
; So we can isolate mua forest as its own area, and guido can remain $A22 bit 02
; This code specifically means when Mua forest is looking for the bit, it's now checking 04 instead of 02 at $A22
; org $D8F18E
org $F0510E
db $72

; always trigger cutscene for opening path to boss
org $F04D66
db $FC, $FB
; MOOGLE VILLAGE
; Event code [$A4, $3C] or setting bit 10 on $000A3B corresponds to both Tyrasaur being defeated and Moogle Village being open
; This fix allows for Tyrasaur to remain on $000A3B bit 10, while Moogle Village is swapped to another bit usually set upon 
; Finishing the Tyrasaur sequence, immediately set on new game ([$A4, $C1], or $000A4C bit 02)
;org $D8EF5C
org $F04EDC
db $C1                     ;Refer to event code [$A4, $C1]


; MOOGLE WATERWAY
; For some reason, $000A1F bit 40 (event [$A2, $5E]) is both tied to the pre-Tyrasaur cutscene (not the pre-battle cutscene, the cutscene before that) and the barrier for Exdeath's castle
; This will disable the waterway cutscene from checking that bit, so it's left only to be barrier related
; We set it to check a bit that we ALWAYS know will be set, which is event code $A2, $10 from starting_flags 
; this is address $000A16 bit $10

;org $D8F632
org $F055B2
db $10

; BAL CASTLE
org $f04d3d
db $ff, $00, $00

; disable hiryuu event
org $c9f3f7
db $FF

; ZEZA FLEET
; After Gilgamesh, change one of the flags for Hiryuu spawning to normal to be based off of:
; db $A2, $AA                     ;Turn on bit 04 at address 0x7e0a29
; instead of 
; db $A2, $6D                     ;Turn on bit 20 at address 0x7e0a21
; Which is tied to Zeza allowing access to Barrier Tower
; org $D8F254
org $F051D4
db $AA

; If used submarine to get here early, disallow access until hiryuu call is obtained
org $F051C1
db $FC, $B2


; BARRIER TOWER
; Similar to above, change barrier tower fight cutscene to deactivate from a different flag than the underwater barrier access warp tile
; org $D8F37D
org $F052FD
db $FD, $77




; FORK TOWER
; Galuf in party causes problems. Temporarily setting access after Mua forest boss → getting Cara
; Bit 80 at address 0x7e0a4b

; org $D8F85A
org $F057D9
db $FD, $C6


; ANTLION
; Moved antlion's area tile up 1 into the river.
; This makes it so the player can only access as Boco, which avoids the regular situation forcing the player
; to be on Boco by walking on the world map (instead of accessing with Boco like vanilla)
org $CE2869 ; this changes tile
db $57
org $C8B218 ; this changes leaving cutscene to place Boco one tile right of this 
db $7A


; PYRAMID W3
; Disable conditional event for pyramid cutscene. Reused for world warps 
; This disables X Y coords and replicates the previous xy checker to overwrite
org $CE288C
db $AD, $E9, $F0, $01

; Disable first mummy in Pyramid
org $F0599D
db $FB, $FB


; PYRAMID TOP
; change conditional flag to be a custom one 
org $F04B1D
db $FD, $78



; GARGOYLES
; Change each conditional event to have individual flags associated with their respective key items
; Only works for pyramid, the others had to be custom 
; Pyramid
; org $D8F3E7
org $F05367
db $BC

; Solitary Shrine
; org $D8FC64
; db $FC, $BB





;FINAL EXDEATH
;Always trigger the cutscene for the final fight
org $F05D3D
db $FF, $85, $07

org $F05D49
db $FF, $9F, $06

org $F053B7 ; this is the actual tile to trigger the fight 
db $FF, $84, $07, $00, $00

; edit LEAVING event to move player down 1 tile
org $C9C4CD
db $23
org $C9FE8A
db $31





; to be VERY Safe that Exdeath sprite doesnt show up, delete
org $CE9A7D
pad $CE9AC3


; spring nullify
org $F04BA4
db $33

;TULE
; change tutorial guy in Tule (duplicate text from 2nd floor guy)
org $CE5E6A
db $68

; AFTER TULE BOAT CUTSCENE
; world map trigger
org $F04F59
db $FB, $FB

; KUZAR 
; disable cutscene after placing first tablet
org $F051AD
db $FB, $FB

; BLACK CHOCOBO
; set to always have recatch cutscene play
; org $F04757
; db $85, $00

org $F04752
db $FD, $3A, $FF, $85, $00, $FF, $47, $03, $FF, $00, $00

org $CE17E0
db $fe, $3a, $fe, $3a, $ff, $7e, $00, $fe, $3a, $ff, $7e, $00, $f7, $00, $ff, $f6, $02


; set backup text to NOT crash the game
; org $CE7879
; db $F6, $00
; org $CE7880
; db $F6, $00



; GIL CAVE
; set to always trigger door opening
org $F05A8C
db $FB

; GUIDO CAVE
; Guido never appears 
org $F0509A
db $FB, $FB
org $F050A1
db $FB, $FB

; BLACK CHOCO W3
; make it so black choco always respawns at mirage
org $C99EBB
db $00, $00, $00

; MIRAGE VILLAGE
; make it so canal key's old item ($000A4C, bit 20) now required to enter
org $F057B4
db $FC, $C5

; disable chocobo access to Mirage Village
org $F057B2
db $00, $00

; NORTH MOUNTAIN
; conditional event for never interacting with hiryuu at top
org $F04835
db $FD, $79, $FF, $00, $00

; nuke npcs
org $ce670E
pad $CE673F


; EXDEATH WORLD 2 CASTLE
org $F05699
db $FC, $BF, $FF, $E1, $00, $00, $00, $00, $00
org $F056A2
db $FF, $00, $00, $00, $00, $00, $FF, $00, $00

; EARTH CRYSTAL
; if you wanna fix later, disable this flag getting set at c89b13 (for FD, B8, not FE)
org $F04AEC
db $FE, $B8



; CARWEN
; remove lady
org $CE65E1
pad $CE65EF



; Swapping GUIDO CAVE for BARRIER TOWER

org $c98874
; warp to barrier tower instead of guido (change event)
db $E0, $4B, $01, $11, $0d, $00 ;Unknown
db $FF                          ;End Event

; disable guido warp
org $F046AC
db $00

; disable guido bit flag $000A2C bit $01
org $C8CE86
db $00, $00

; NEW TEXT FOR DEBUG TO WARP AREA
org $e178fa
db $63, $64, $61, $74, $66, $9B, $96, $76, $7A, $8B, $89, $82, $87, $80, $96, $8D, $88, $96, $76, $7A, $8B, $89, $96, $60, $8B, $7E, $7A, $A3, $96, $01, $6D, $88, $8D, $96, $7A, $96, $7B, $8E, $80, $A1, $00

; STEAMSHIP / AIRSHIP
; never have the steamship (if it happens to spawn on world map??) or airship do anything except let you ride it (no cutscenes)
org $F04F57
db $FF, $00, $00


; METEOR WALSE
org $C984FC
db $FF

; Big Bridge
; Clear out encounters 
org $F0500E
db $00, $00
org $F05015
db $00, $00
org $F0501C
db $00, $00
org $F05023
db $00, $00
org $F0502A
db $00, $00
org $F05031
db $00, $00
org $F05038
db $00, $00
org $F0503D
db $00, $00
org $F05054
db $00, $00
org $F0505B
db $00, $00
org $F05007
db $00, $00
org $F0500E
db $00, $00
org $F05015
db $00, $00
org $F0501C
db $00, $00


; Chicken Knife always max power on equip menu
org $C2D9F1
lda #$7F
; Brave Blade always max power on equip menu
org $C2D9D3
lda #$00

; Chicken Knife max power in battle
org $C28626
lda #$FF
nop

; Brave Blade max power in battle
org $C2857E
nop
nop
nop

; delete guy blocking lone wolf item in carwen
org $CE65B7
db $00

; Delete King Walse
org $CE6A9C
pad $CE6AA3
; Change NPC dialogue bc King Walse not there
org $CE6AAA
db $D1

; gilgamesh music fix
org $D0495E
db $18
org $D04C9E
db $18
org $D04D0E
db $18
org $D04D4E
db $18
org $D04D8E
db $18


; disable surgate NPCs in bed
org $CE8A15
pad $CE8A38

; Moogle text adjust for shinryuu help text
org $c975a8
db $81, $04


; disable GILGA V
org $CE9A68
pad $CE9A6F

; open walse meteor tile (cut event short when entering)
org $C889CB
db $FF

; King Tycoon in ruined city area, spawn once
org $F04FC8
db $FF, $00, $00
org $F04FDD
db $FF, $90, $00, $00, $00
    ; entering the area
; org $F04FA3
; db $FF, $0C, $03

; Bal castle
; Disallow leaving from below into cave
; Fixes world1/2/3 issues
org $F05A39
db $FF, $00, $00, $00, $00

; Bard in Crescent
; fixed reward for all 8 pianos in certain conditionals
; org $CE179C
; db $29, $02

; Create crystal icon for text
org $D1FBB0
db $e7, $10, $d3, $38, $a9, $7c, $d5, $7c, $d5, $7c, $a9, $7c, $d3, $38, $e7, $10

; Fix GILGAMESH fights to have numbers
org $E00B85
db $54

org $E00BB7
db $55

org $E00C1B
db $56

org $E00C75
db $57

org $E00DFB
db $57

; Give GUARDIANS a name
org $E00C30
db $66, $8E, $7A, $8B, $7D, $82, $7A, $87
org $E00C3A
db $66, $8E, $7A, $8B, $7D, $82, $7A, $87
org $E00C44
db $66, $8E, $7A, $8B, $7D, $82, $7A, $87
org $E00C4E
db $66, $8E, $7A, $8B, $7D, $82, $7A, $87

; Disable Jacohl NPC from using Portal Boss event
org $ce7688
db $b3



; put underwater crags near zeza fleet
; dont ask me how I did this
; it involved 
; breakpoint write 7F22B1
; finding 7f763E reference
; copy and pasting data to find it in C7F0F7 area
; then changing 04 (underwater tile) -> 19 (crag)

org $C7F0F7
db $0B
org $C7F0D0
db $0B
org $C7F0AB
db $0B
org $C7F082
db $0B



; hardcode write rewards for free tablets
org $C0FBD0
db $30, $1A
db $30, $1B
db $30, $1C
db $30, $1D

; odin borrowed from bal_castle_timerguard
org $CE22A0
db $FD, $D5, $FF, $A6, $00, $FF, $C9, $00, $F0




; steamship world map
org $C71569
db $05, $52, $73, $43, $43 
org $C715D5
db $05, $73, $43, $43, $43, $87, $87, $50, $51, $99

; change steamship exit to always be outside karnak
org $F04E19
db $6E, $00

; change old steamship -> catapult warp event 
org $c93fb5
db $c8, $ad, $84, $04, $ff
pad $c93FC3

; event text for above
org $E25116
db $63, $88, $88, $8B, $96, $85, $88, $7C, $84, $7E, $7D, $A3, $01, $75, $82, $8C, $82, $8D, $96, $88, $8E, $8D, $8C, $82, $7D, $7E, $96, $6A, $7A, $8B, $87, $7A, $84, $96, $7F, $88, $8B, $96, $72, $8D, $7E, $7A, $86, $8C, $81, $82, $89, $A3, $00

; disable steamship spawning via event
org $c878c0
db $00, $00, $00, $00, $00


; disable all conditional events at steamship
org $F04BD0
db $FF, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00






; force karnak npc to always give hint
org $CE12AB
db $01


; THIS was once used for Merugene, but now that the fight has moved entirely, no longer necessary
; ; fix merugune spot's event flag for clearing the fight
; org $f0562D
; db $FB, $9B

; org $f05634
; db $FB, $9B

; INSTEAD, deleting entirely from world map checks
; simply overwrite the entry in the table with another duplicate 
org $CE2890
db $CE, $C8, $FC, $01, $CE, $C8, $FC, $01


; change excalibur fake to excalipoor
org $E76100
db $64, $91, $7C, $7A, $94, $89, $88, $8B
org $D116BD
db $64, $91, $7C, $7A, $94, $89, $88, $8B



;;; seed hash system
; change byte for when to start hash string on new game
org $C3B577
db $09

; set new text string to E73400
org $C0FA3D
db $00, $34

; initialize text for non buggy title screen if hash isnt made
org $E73400
db $00

; put hash on butz creation 
org $C0FA23
db $00, $34, $10, $34



; change mirage village guy's dialogue
org $e364d6
db $72, $88, $8B, $8B, $92, $A3, $A3, $A3, $96, $7A, $85, $85, $96, $88, $8E, $8D, $96, $88, $7F, $96, $80, $82, $7F, $8D, $8C, $A1, $00
pad $E36564



; change Mediator text to Trainer
org $E1B752
db $73, $8B, $7A, $82, $87, $7E, $8B, $FF
; e1b752 - 76d (fill with FFs)

; D15678 -> 80
org $D15678
db $73, $8B, $7A, $82, $87, $7E, $8B, $FF


; rename Capture to Mug
org $e011a4
db $6C, $8E, $80, $FF, $FF, $FF, $FF

; rename Combine to Mix
org $e01229
db  $6C, $82, $91, $FF, $FF, $FF, $FF



;Time
org $e730f2
db $73, $82, $86, $7E, $FF



org $e01302
db $73, $82, $86, $7E, $FF
org $e01309
db $73, $82, $86, $7E, $FF
org $e01310
db $73, $82, $86, $7E, $FF
org $e01317
db $73, $82, $86, $7E, $FF
org $e0131e
db $73, $82, $86, $7E, $FF
org $e01325
db $73, $82, $86, $7E, $FF

; Worus -> Walse

org $e70257
db $76, $7A, $85, $8C, $7E
org $e70263
db $76, $7A, $85, $8C, $7E
org $e70274
db $76, $7A, $85, $8C, $7E
org $e70285
db $76, $7A, $85, $8C, $7E
org $e70298
db $76, $7A, $85, $8C, $7E
org $e7029d
db $76, $7A, $85, $8C, $7E
org $e702b2
db $76, $7A, $85, $8C, $7E


org $e174c5
db $76, $7A, $85, $8C, $7E
org $e16f60
db $76, $7A, $85, $8C, $7E
org $e170fc
db $76, $7A, $85, $8C, $7E
org $e17009
db $76, $7A, $85, $8C, $7E
org $e17209
db $76, $7A, $85, $8C, $7E


; Mua -> Moore
org $e33993
db $6C, $88, $88, $8B, $7E, $96, $82, $8C, $96, $96
org $e33851
db $6C, $88, $88, $8B, $7E, $96
org $e33589
db $6C, $88, $88, $8B, $7E, $A3, $A3, $A3

org $D070FE
db $8A
org $e70485
db $6C, $88, $88, $8B, $7E, $FF, $FF, $FF



; Coronet -> Hypno
org $d11aa4
db $67, $92, $89, $87, $88, $FF, $FF
org $e76b68
db $67, $92, $89, $87, $88, $96, $67, $7E, $85, $86


; Air Lance -> Air Knife
org $d113de
db $6A, $87, $82, $7F, $7E

org $E75954
db $6A, $87, $82, $7F, $7E, $FF

; Gungnir -> Heavy Spear
org $d11486
db $67, $7E, $7A, $8F, $92, $FF, $FF
org $e75b18
db $67, $7E, $7A, $8F, $92, $96, $72, $89, $7E, $7A, $8B
; org $e719c0
; db $67, $7E, $7A, $8F, $92, $96, $72, $89, $7E, $7A, $8B


; Protect Drink -> Protect Potion (MIX)
org $e70c80
db $6F, $8B, $88, $8D, $7E, $7C, $8D, $96, $6F, $88, $8D, $82, $88, $87

; Sampson -> Samson
org $e70c40
db $72, $7A, $86, $8C, $88, $87, $96, $6F, $88, $90, $7E, $8B, $FF

;  MgthyGrd -> BigGuard
org $d120e5
db $61, $82, $80, $66, $8E, $7A, $8B, $7D





; cause Odin to not self terminate (for giving EXP)
org $D0BBBE
db $FF




; change 2-Handed to 2-Wield
org $D16290
db $55, $C5, $76, $82, $7E, $85, $7D, $FF



; fix zokk to work in w3
org $E029D4
db $DD, $49, $E1
; fix mua to work in w3
org $E02B72
db $31
; fix kelgar to work in w3
org $E0227B
db $28, $63, $E2
; allow guy outside kelgar to give hint (I could not get kelgar to spawn after certain flags are set)
org $E02BC6
db $28, $63, $e2



; hook to reset the MIB free address on all screen transitions

org $c05852
jml !ADDRESS_reset_unusedram3

org !ADDRESS_reset_unusedram3
lda $c05ba8,x
sta $109a 
lda $06
sep #$20
stz !unusedram3
jml $C0585D


; fix wind shrine potion guy to always give reward before/after wind shrine cleared 
org $CE096A
db $FB, $FB

; fix walse tower guard's text
org $e16e82
;You cannot enter this tower without the Walse Tower Key.
db $78, $88, $8E, $96, $7C, $7A, $87, $87, $88, $8D, $96, $7E, $87, $8D, $7E, $8B, $96, $8D, $81, $82, $8C, $96, $8D, $88, $90, $7E, $8B, $01, $96, $90, $82, $8D, $81, $88, $8E, $8D, $96, $8D, $81, $7E, $96, $76, $7A, $85, $8C, $7E, $96, $73, $88, $90, $7E, $8B, $96, $6A, $7E, $92, $A3, $00


; fix karnak guards position
org $CE6ED5
db $FE, $FE
org $CE6EDC
db $FE, $FE

; abbreviate credits

org $C8ECEF


; disable lone wolf from being interacted with
org $F047A2
db $00, $00