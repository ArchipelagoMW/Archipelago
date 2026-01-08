hirom


; $C8E33D → $C8EA0C
; Guide cutscene at his dwelling

; $C9EFA6 → $C9F346
; Guide cutscene at Library. This is branched to during the above 


org $C8E33D
db $01
db $01
db $01
db $01
db $01
db $C4, $01
db $A4, $F5                     ;Set Event Flag 1F5
db $CB, $30, $03                ;Clear Flag 2/3/4/5/30 03
db $CB, $17, $01                ;Clear Flag 2/3/4/5/17 01
db $A2, $80                     ;Set Event Flag 080
db $C4, $02                     ;Fade out Speed 03
db $75
db $E1, $A9, $00, $17, $2E, $00 ;Return from cutscene? A9 00 17 2E 00
db $D3, $93, $17, $2D           ;Sprite 93 set map position 17, 2D
db $93, $10                     ;Sprite 193 do event: face up, left hand forward
db $8D, $0A                     ;Sprite 08D do event: Hide
db $94, $0A                     ;Sprite 194 do event: Hide
db $84, $0A                     ;Sprite 084 do event: Hide
db $85, $0A                     ;Sprite 085 do event: Hide
db $86, $0A                     ;Sprite 086 do event: Hide
db $87, $0A                     ;Sprite 087 do event: Hide
db $8C, $0A                     ;Sprite 08C do event: Hide
db $D3, $80, $54, $27           ;Sprite 80 set map position 54, 27
db $D3, $81, $54, $28           ;Sprite 81 set map position 54, 28
db $D3, $82, $54, $29           ;Sprite 82 set map position 54, 29
db $D3, $83, $54, $2A           ;Sprite 83 set map position 54, 2A
db $D3, $88, $DA, $26           ;Sprite 88 set map position DA, 26
db $D3, $89, $DA, $28           ;Sprite 89 set map position DA, 28
db $D3, $8A, $DA, $29           ;Sprite 8A set map position DA, 29
db $D3, $8B, $DA, $2B           ;Sprite 8B set map position DA, 2B
db $93, $09                     ;Sprite 193 do event: Show
db $80, $10                     ;Sprite 080 do event: face up, left hand forward
db $81, $10                     ;Sprite 081 do event: face up, left hand forward
db $82, $10                     ;Sprite 082 do event: face up, left hand forward
db $83, $10                     ;Sprite 083 do event: face up, left hand forward
db $88, $10                     ;Sprite 088 do event: face up, left hand forward
db $89, $10                     ;Sprite 089 do event: face up, left hand forward
db $8A, $10                     ;Sprite 08A do event: face up, left hand forward
db $8B, $10                     ;Sprite 08B do event: face up, left hand forward
db $93, $10                     ;Sprite 193 do event: face up, left hand forward
db $73                          ;Long pause
db $C3, $03                     ;Fade in Speed 03
db $C7, $03                     ;Play next 03 bytes simultaneously
db $93, $01                     ;Sprite 193 do event: Move Up
db $01                          ;Player Move Up
db $C7, $03                     ;Play next 03 bytes simultaneously
db $93, $02                     ;Sprite 193 do event: Move Right
db $01                          ;Player Move Up
db $93, $20                     ;Sprite 193 do event: face down, left hand raised out
;db $71                          ;Short pause
db $93, $26                     ;Sprite 193 do event: face up, right hand raised out
db $12                          ;Player pose: face right, standing
db $72                          ;Medium pause
db $93, $20                     ;Sprite 193 do event: face down, left hand raised out
db $73                          ;Long pause
db $B5, $3A                     ;Play Sound Effect Quick
;db $71                          ;Short pause
db $B5, $84                     ;Play Sound Effect Exdeath destroyed 2
db $BE, $05                     ;Rumble effect of 05 magnitude
;db $71                          ;Short pause
db $10                          ;Player pose: face up, left hand forward
db $80, $5B                     ;Sprite 080 do event: 5B
db $81, $5B                     ;Sprite 081 do event: 5B
db $82, $5B                     ;Sprite 082 do event: 5B
db $83, $5B                     ;Sprite 083 do event: 5B
db $88, $5B                     ;Sprite 088 do event: 5B
db $89, $5B                     ;Sprite 089 do event: 5B
db $8A, $5B                     ;Sprite 08A do event: 5B
db $8B, $5B                     ;Sprite 08B do event: 5B
db $F3, $16, $26, $53           ;Set Map Tiles 16 26 53
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $9C, $BA                     ;Sprite 19C do event: BA
db $9D, $20                     ;Sprite 19D do event: face down, left hand raised out
db $DE, $9A, $EC, $95           ;Noop
db $CF, $85, $CF                ;Play next CF bytes simultaneously 85 times
db $95, $67                     ;Sprite 195 do event: 67
db $85, $67                     ;Sprite 085 do event: 67
db $95, $77                     ;Sprite 195 do event: 77
db $65                  ;Player or Sprite Pose
db $77                          ;<Unknown>
db $22                          ;Player pose: face down, left hand on head
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $27, $43           ;Set Map Tiles 16 27 43
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $9C, $BA                     ;Sprite 19C do event: BA
db $9D, $20                     ;Sprite 19D do event: face down, left hand raised out
db $DE, $9A, $EC, $95           ;Noop
db $CF, $85, $CF                ;Play next CF bytes simultaneously 85 times
db $95, $67                     ;Sprite 195 do event: 67
db $65                  ;Player or Sprite Pose
db $67                  ;Player or Sprite Pose
db $22                          ;Player pose: face down, left hand on head
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $28, $33           ;Set Map Tiles 16 28 33
db $1F                          ;Player pose: face right, walking, right hand forward
db $1F                          ;Player pose: face right, walking, right hand forward
db $1F                          ;Player pose: face right, walking, right hand forward
db $20                          ;Player pose: face down, left hand raised out
db $9C, $BA                     ;Sprite 19C do event: BA
db $9D, $20                     ;Sprite 19D do event: face down, left hand raised out
db $DE, $9A, $EC, $20           ;Noop
db $CF, $65, $CF                ;Play next CF bytes simultaneously 65 times
db $20                          ;Player pose: face down, left hand raised out
db $F3, $56, $28, $02           ;Set Map Tiles 56 28 02
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $29, $22           ;Set Map Tiles 16 29 22
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $9C, $BA                     ;Sprite 19C do event: BA
db $9D, $DE                     ;Sprite 19D do event: DE
db $9A, $EC                     ;Sprite 19A do event: EC
db $F3, $56, $29, $22           ;Set Map Tiles 56 29 22
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $2A, $12           ;Set Map Tiles 16 2A 12
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $9C, $BA                     ;Sprite 19C do event: BA
db $9D, $F3                     ;Sprite 19D do event: F3
db $56                  ;Player or Sprite Pose
db $2A                          ;Player pose: face left, left hand raised
db $02                          ;Player Move Right
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $2B, $02           ;Set Map Tiles 16 2B 02
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $F3, $56, $2B, $02           ;Set Map Tiles 56 2B 02
db $01                          ;Player Move Up
db $01                          ;Player Move Up
db $01                          ;Player Move Up
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $2B, $02           ;Set Map Tiles 16 2B 02
db $F3, $E0, $F4, $F3           ;Set Map Tiles E0 F4 F3
db $56                  ;Player or Sprite Pose
db $2B                          ;Player pose: face left, left hand out
db $02                          ;Player Move Right
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $2A, $12           ;Set Map Tiles 16 2A 12
db $F3, $E0, $F4, $D2           ;Set Map Tiles E0 F4 D2
db $E1, $D3, $F3, $56, $2A, $02 ;Return from cutscene? D3 F3 56 2A 02
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $29, $12           ;Set Map Tiles 16 29 12
db $F3, $E0, $F4, $D2           ;Set Map Tiles E0 F4 D2
db $E1, $D3, $F3, $56, $29, $02 ;Return from cutscene? D3 F3 56 29 02
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $28, $32           ;Set Map Tiles 16 28 32
db $F3, $E0, $F4, $D2           ;Set Map Tiles E0 F4 D2
db $E1, $D3, $D2, $E1, $D3, $F0 ;Return from cutscene? D3 D2 E1 D3 F0
db $F1, $F2                     ;Unknown
db $F3, $56, $28, $02           ;Set Map Tiles 56 28 02
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
db $20                          ;Player pose: face down, left hand raised out
;db $B2, $04                     ;Pause for 04 cycles
db $F3, $16, $27, $42           ;Set Map Tiles 16 27 42
db $F3, $E0, $F4, $D2           ;Set Map Tiles E0 F4 D2
db $E1, $D3, $D2, $E1, $D3, $F0 ;Return from cutscene? D3 D2 E1 D3 F0
db $F1, $F2                     ;Unknown
db $C6, $C7                     ;Add job C7
db $C8, $71, $BE                ;Display Message/Text/Dialogue 71 BE
db $00                          ;Player Hold
db $D0, $80, $60                ;(Music) 80 60
db $80, $22                     ;Sprite 080 do event: face down, left hand on head
db $81, $22                     ;Sprite 081 do event: face down, left hand on head
db $82, $22                     ;Sprite 082 do event: face down, left hand on head
db $83, $22                     ;Sprite 083 do event: face down, left hand on head
db $88, $26                     ;Sprite 088 do event: face up, right hand raised out
db $89, $26                     ;Sprite 089 do event: face up, right hand raised out
db $8A, $26                     ;Sprite 08A do event: face up, right hand raised out
db $8B, $26                     ;Sprite 08B do event: face up, right hand raised out
db $93, $02                     ;Sprite 193 do event: Move Right
db $CE, $06, $02                ;Play next 02 bytes 06 times
db $93, $01                     ;Sprite 193 do event: Move Up
db $93, $04                     ;Sprite 193 do event: Move Left
db $93, $04                     ;Sprite 193 do event: Move Left
;db $70                          ;Very short pause
db $93, $24                     ;Sprite 193 do event: face down, right hand raised in
db $01                          ;Player Move Up
;db $71                          ;Short pause
db $B4, $16                     ;Play Background Music The Four Warriors of Dawn
db $B9, $63                     ;Toggle Subtracitve Tint by 63
db $8D, $11                     ;Sprite 08D do event: face up, right hand forward
db $B4, $24                     ;Play Background Music The Book of Sealings
db $B3, $02                     ;Pause for 100 cycles
db $73                          ;Long pause
db $B8, $7B                     ;Toggle Additive Tint by 7B
;db $74                          ;Very long pause
;db $73                          ;Long pause
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8D, $03                     ;Sprite 08D do event: Move Down
db $8D, $0A                     ;Sprite 08D do event: Hide
db $C5                          ;<unknown>
db $E0, $73                     ;Unknown
db $C8, $1D, $88                ;Display Message/Text/Dialogue 1D 88
;db $71                          ;Short pause
db $D0, $80, $40                ;(Music) 80 40
;db $73                         ;Extremely long pause
db $B4, $16                     ;Play Background Music The Four Warriors of Dawn
db $A5, $FE                     ;Clear Event Flag 1FE
db $A4, $7F                     ;Set Event Flag 17F
db $A5, $FF                     ;Clear Event Flag 1FF
db $CA, $98, $03                ;Set Flag 2/3/4/5/98 03
db $D0, $80, $60                ;(Music) 80 60
db $C4, $02                     ;Fade out Speed 03
db $75
db $E1, $A9, $00, $97, $2C, $00 ;Return from cutscene? A9 00 97 2C 00
db $14                          ;Player pose: face down, left hand forward
db $75                          ;Extremely long pause
db $C3, $02                     ;Fade in Speed 04
db $A4, $50                     ;Set Event Flag 150


; First Tree visit flag
db $A4, $7C                     ;Set Event Flag 17C

; Pyramid flags
db $A5, $FE                     ;Clear Event Flag 1FE
db $A2, $BD                     ;Set Event Flag 0BD

db $CC, $26                  ;Custom destination flag 26


db $FF                          ;End Event

padbyte $00
pad $C8EA0C
