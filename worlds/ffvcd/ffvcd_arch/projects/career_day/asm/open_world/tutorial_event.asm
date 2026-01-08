; this solely sits as event data within intro cutscene, within `starting_flags.asm`
; this should take place before the warp out happens


db $E3, $0D, $00, $8A, $07, $00 ;Inter-map cutscene? 0D 00 8A 07 00
db $0A                          ;Player Hide

; ; TESTING MUSIC ONLY
; db $D0, $F0, $00                ;(Music) F0 00

db $C3, $0C                     ;Fade in Speed 0C
db $73                          ;Long pause
db $D3, $80, $40, $07           ;Sprite 80 set map position 40, 07
db $80, $09                     ;Sprite 080 do event: Show
db $80, $13                     ;Sprite 080 do event face right, down hand backward
db $CE, $0A, $02                ;Play next 02 bytes 0A times
db $80, $02                     ;Sprite 080 do event: Move Right
db $70                          ;Very short pause
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $70                          ;Short pause
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $70                          ;Short pause
db $CA, $74, $00            ; set address 000A62 bit ON 10



db $80, $54                     ;Sprite 080 do event: 54
db $70                          ;Very short pause
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $70                          ;Long pause
db $C8, $AF, $00                ;Display Message/Text/Dialogue AF 00
db $70                          ;Short pause
db $C8, $B1, $00                ;Display Message/Text/Dialogue B0 00
db $70                          ;Very short pause
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $71                          ;Short pause
; db $C8, $A3, $01                ;Display Message/Text/Dialogue B1 00

; ; TESTING MUSIC ONLY
; db $B4, $30
; db $C8, $A3, $01                ;Display Message/Text/Dialogue B1 00


db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $80, $05                     ;Sprite 080 do event: Bounce
db $80, $00                     ;Sprite 080 do event: Hold
db $71
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $CE, $0A, $02                ;Play next 02 bytes 0A times
db $80, $02                     ;Sprite 080 do event: Move Right




db $D0, $80, $20                ;(Music) 80 20
db $80, $24                     ;Sprite 080 do event: face down, right hand raised in
db $71                          ;Short pause
db $D0, $F0, $00                ;(Music) F0 00
