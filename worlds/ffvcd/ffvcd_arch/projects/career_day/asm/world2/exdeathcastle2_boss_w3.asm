hirom


; change Exdeath conditional event for new merugene originating flag
org $f05740
db $FB, $9B

; Exdeath pre-dialogue → Warp to World 3

org $C99619

db $D0, $80, $80                ;(Music) 80 80
db $01                          ;Player Move Up
db $B1, $02                     ;Set Player Sprite 02
db $94, $09                     ;Sprite 194 do event: Show
db $96, $09                     ;Sprite 196 do event: Show
db $95, $09                     ;Sprite 195 do event: Show
db $95, $20                     ;Sprite 195 do event: face down, left hand raised out
db $C7, $05                     ;Play next 05 bytes simultaneously
db $01                          ;Player Move Up
db $96, $02                     ;Sprite 196 do event: Move Right
db $94, $04                     ;Sprite 194 do event: Move Left
db $96, $20                     ;Sprite 196 do event: face down, left hand raised out
db $94, $20                     ;Sprite 194 do event: face down, left hand raised out
db $73                          ;Long pause
db $B4, $2D                     ;Play Background Music The Evil Lord Exdeath
db $71                          ;Short pause
db $93, $22                     ;Sprite 193 do event: face down, left hand on head
db $B2, $04                     ;Pause for 04 cycles
db $93, $24                     ;Sprite 193 do event: face down, right hand raised in
db $73                          ;Long pause
db $93, $0A                     ;Sprite 193 do event: Hide
db $BD, $24, $FF                ;Start Event Battle 24
db $B4, $24					;music
db $72

if !end_on_exdeath1 = 1

    db $B4, $11                     ;Play Background Music (Nothing)
    db $B7, $0C 					; add cara over galuf for non glitchy ending...?
    db $C4, $04                     ;Fade out Speed 06
    db $74
    db $74
    db $CD, $43, $01                ;Run event index 0143
    db $FF
else

    if !world_lock = 0
        db $C5, $80 ; Only do this if world lock is fully open (where Exdeath is optional)
        db $B5, $02
        db $70
        db $C5, $50
        db $B5, $02
        db $70
        db $C5, $20
        db $B5, $02
        db $70
        db $C5, $60
        db $B5, $02
        db $70
        db $C5, $F0
        db $B5, $02
        db $71
        db $C8, $A9, $05                ; Text: Phase 1 against final Exdeath weakened!
        db $CD, $9C, $03
    endif

        db $C4, $02                     ;Fade in Speed 06
        db $75


    ; CAREERDAY
    ; db $E1, $02, $00, $B7, $89, $00 ;Return from cutscene? 02 00 B7 89 00
    db $E1, $01, $00, $A0, $9D, $00 ;Return from cutscene? 



    ; db $A5, $7F                     ;Clear Event Flag 17F
    db $CB, $96, $01                ;Clear Flag 2/3/4/5/96 01
    ; db $A2, $79                     ;Set Event Flag 079
    db $A4, $9B            ; set address 000A47 bit ON 08. THIS WAS REPURPOSED FROM MERUGENE
    db $CB, $7C, $01                ;Clear Flag 2/3/4/5/7C 01
    db $CB, $7D, $01                ;Clear Flag 2/3/4/5/7D 01
    db $CB, $7E, $01                ;Clear Flag 2/3/4/5/7E 01
    db $CB, $7F, $01                ;Clear Flag 2/3/4/5/7F 01
    db $CB, $89, $01                ;Clear Flag 2/3/4/5/89 01
    db $CB, $8A, $01                ;Clear Flag 2/3/4/5/8A 01
    db $CB, $8B, $01                ;Clear Flag 2/3/4/5/8B 01
    db $CB, $8C, $01                ;Clear Flag 2/3/4/5/8C 01
    db $CA, $51, $00                ;Set Flag 2/3/4/5/51 00
    db $CA, $52, $00                ;Set Flag 2/3/4/5/52 00
    db $CA, $53, $00                ;Set Flag 2/3/4/5/53 00
    db $CA, $54, $00                ;Set Flag 2/3/4/5/54 00
    db $CA, $55, $00                ;Set Flag 2/3/4/5/55 00
    db $CA, $98, $03                ;Set Flag 2/3/4/5/98 03
    db $CA, $7D, $03                ;Set Flag 2/3/4/5/7D 03
    db $CA, $7E, $03                ;Set Flag 2/3/4/5/7E 03
    db $CA, $7F, $03                ;Set Flag 2/3/4/5/7F 03
    db $CA, $80, $03                ;Set Flag 2/3/4/5/80 03
    db $CA, $81, $03                ;Set Flag 2/3/4/5/81 03
    db $CA, $82, $03                ;Set Flag 2/3/4/5/82 03
    db $CB, $44, $00                ;Clear Flag 2/3/4/5/44 00
    db $CB, $45, $00                ;Clear Flag 2/3/4/5/45 00
    db $CB, $46, $00                ;Clear Flag 2/3/4/5/46 00
    db $CB, $47, $00                ;Clear Flag 2/3/4/5/47 00
    db $CB, $48, $00                ;Clear Flag 2/3/4/5/48 00
    db $CB, $49, $00                ;Clear Flag 2/3/4/5/49 00
    db $CB, $30, $00                ;Clear Flag 2/3/4/5/30 00
    db $A5, $9A                     ;Clear Event Flag 19A
    
    if !world_lock = 0
        if !remove_ned = 0
            
    
            ; new code - only do this IF remove_ned is NOT set
            ; i.e., do not set the custom flag for the 1HP exdfeath if another randomized boss was put there 
            db $A2, $CC						; CUSTOM FLAG for final exdeath death phase 1. Only do this if world lock is fully open (where Exdeath is optional)
        endif
    endif

    db $CA, $DA, $02            ; set address 000AAF bit ON 02. ENABLE world 3
    db $CA, $73, $02                ;Set Flag 2/3/4/5/73 02


    db $CB, $7F, $00            ; set address 000A63 bit OFF 80. remove exdeath & crystals


    ; tycoon chancellor & guard already set. by the time you get to w3, force this 
    db $CB, $01, $01                ;Turn off bit 02 at address  0x7e0a74
    db $CA, $0A, $01                ;Turn on bit 04 at address  0x7e0a75
    db $A2, $52                     ;Turn on bit 04 at address 0x7e0a1e

    ; db $A4, $FF                     ;Set Event Flag 1FF
    db $DB                          ;Restore Player status
    db $10                          ;Player pose: face up, left hand forward
    db $C3, $02                     ;Fade in Speed 06
    db $75                          ;Extremely long pause
    db $CC, $24                  	;Custom destination flag 24
    db $A4, $FB						;Turn on bit 08 at address 0x7e0a53 ;Enables the world map right before we transition to world 3 in case you haven't picked it up
    ; db $B4, $27                     ; music world map 2
    db $CD, $7F, $05				;Run event index 057F ; Party Heal
    db $FF                          ;End Event

endif

padbyte $00
pad $C9986C