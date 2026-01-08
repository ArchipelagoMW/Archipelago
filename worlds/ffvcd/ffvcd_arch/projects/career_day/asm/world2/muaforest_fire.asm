hirom


; Overall, going to have to preserve cutscene and not warp to post-fire state because of the Flame/Aegis shield 
; Will speed up first fire cutscene
; Then as soon as enter Moogle pit, immediately go to post-fire state

; First fire cutscene

org $C8DB99

; db $D0, $81, $20                ;(Music) 81 20
db $C4, $03
db $73
db $C3, $03
db $E1, $67, $01, $EF, $30, $00 ;Unknown
db $CA, $4D, $03                ;Set Flag 2/3/4/5/4D 03
db $A4, $EC                     ;Set Event Flag 1EC
db $A2, $74                     ;Set Event Flag 074     Event flags for showing branch to enter final area
db $73
db $FF

padbyte $00
pad $C8DCD2






; $C8DCFA → $C8DD47
; Moogle appears. This is called by timer $D1 $00 $10 $01

org $C8DCFA

db $7C                          ;<Unknown>
db $F3, $20, $09, $01           ;Set Map Tiles 20 09 01
db $15                          ;Player pose: face down, right hand forward
db $16                          ;Player pose: face left, standing
db $D3, $83, $A1, $09           ;Sprite 83 set map position A1, 09
db $83, $5A                     ;Sprite 083 do event: 5A
db $83, $0B                     ;Sprite 083 do event: 0B
db $83, $06                     ;Sprite 083 do event: Bounce
db $83, $04                     ;Sprite 083 do event: Move Left
db $83, $0B                     ;Sprite 083 do event: 0B
db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
db $83, $26                     ;Sprite 083 do event: face up, right hand raised out
db $83, $22                     ;Sprite 083 do event: face down, left hand on head
db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
db $CE, $03, $06                ;Play next 06 bytes 03 times
db $83, $56                     ;Sprite 083 do event: 56
db $83, $57                     ;Sprite 083 do event: 57
db $83, $54                     ;Sprite 083 do event: 54
db $CE, $0A, $10                ;Play next 10 bytes 0A times
db $83, $20                     ;Sprite 083 do event: face down, left hand raised out
db $B2, $03                     ;Pause for 03 cycles
db $83, $22                     ;Sprite 083 do event: face down, left hand on head
db $B2, $03                     ;Pause for 03 cycles
db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
db $B2, $03                     ;Pause for 03 cycles
db $83, $26                     ;Sprite 083 do event: face up, right hand raised out
db $B2, $03                     ;Pause for 03 cycles
db $83, $06                     ;Sprite 083 do event: Bounce
db $83, $02                     ;Sprite 083 do event: Move Right
db $83, $0A                     ;Sprite 083 do event: Hide
db $A4, $EC                     ;Set Event Flag 1EC
db $FF                          ;End Event

padbyte $00
pad $C8DCD2


; Underground moogle cave
; Immediately set flag to enter

org $C8DD49

db $A4, $FE                     ;Set Event Flag 1FE
db $D0, $81, $A0                ;(Music) 81 A0
db $CD, $13, $01                ;Run event index 0113
db $A5, $FE                     ;Clear Event Flag 1FE
db $82, $04                     ;Sprite 082 do event: Move Left
db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
db $B4, $19                     ;Play Background Music As I Feel, You Feel
db $D1, $00, $0E, $01           ;(Timer?) 00 0E 01
db $A5, $FF                     ;Clear Event Flag 1FF

db $A2, $74                     ;Set Event Flag 074     Event flags for showing branch to enter final area

padbyte $00
pad $C8DD61