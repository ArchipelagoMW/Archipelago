hirom



; This entire event was scrapped and relocated for Rift tablet handling

; org $C8d048

; db $E3, $46, $01, $8D, $25, $00 ;Inter-map cutscene? 46 01 8D 25 00
; db $CD, $FE, $01                ;Run event index 01FE
; db $D3, $81, $8C, $2C           ;Sprite 81 set map position 8C, 2C
; db $88, $10                     ;Sprite 088 do event: face up, left hand forward
; db $89, $10                     ;Sprite 089 do event: face up, left hand forward
; db $8A, $10                     ;Sprite 08A do event: face up, left hand forward
; db $86, $10                     ;Sprite 086 do event: face up, left hand forward
; db $81, $13                     ;Sprite 081 do event: face right, down hand backward
; db $77                          ;<Unknown>
; db $72                          ;Medium pause
; db $CE, $0A, $02                ;Play next 02 bytes 0A times
; db $81, $01                     ;Sprite 081 do event: Move Up
; db $86, $26                     ;Sprite 086 do event: face up, right hand raised out
; db $CF, $06, $03                ;Play next 03 bytes simultaneously 06 times
; db $81, $01                     ;Sprite 081 do event: Move Up
; db $01                          ;Player Move Up
; db $81, $10                     ;Sprite 081 do event: face up, left hand forward
; db $76                          ;<Unknown>
; db $CF, $02, $03                ;Play next 03 bytes simultaneously 02 times
; db $81, $01                     ;Sprite 081 do event: Move Up
; db $01                          ;Player Move Up
; db $01                          ;Player Move Up
; db $86, $20                     ;Sprite 086 do event: face down, left hand raised out
; db $81, $02                     ;Sprite 081 do event: Move Right
; db $CF, $04, $04                ;Play next 04 bytes simultaneously 04 times
; db $88, $03                     ;Sprite 088 do event: Move Down
; db $89, $03                     ;Sprite 089 do event: Move Down
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $88, $02                     ;Sprite 088 do event: Move Right
; db $89, $04                     ;Sprite 089 do event: Move Left
; db $8A, $02                     ;Sprite 08A do event: Move Right
; db $88, $20                     ;Sprite 088 do event: face down, left hand raised out
; db $89, $20                     ;Sprite 089 do event: face down, left hand raised out
; db $8A, $01                     ;Sprite 08A do event: Move Up
; db $8A, $01                     ;Sprite 08A do event: Move Up
; db $CD, $FF, $01                ;Run event index 01FF
; db $82, $10                     ;Sprite 082 do event: face up, left hand forward
; db $82, $02                     ;Sprite 082 do event: Move Right
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $82, $04                     ;Sprite 082 do event: Move Left
; db $D8, $C4, $0F, $D8           ;Unknown
; db $85, $0F                     ;Sprite 085 do event: 0F
; db $D8, $C3, $0F, $B1           ;Unknown
; db $02                          ;Player Move Right
; db $82, $24                     ;Sprite 082 do event: face down, right hand raised in
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $85, $04                     ;Sprite 085 do event: Move Left
; db $84, $03                     ;Sprite 084 do event: Move Down
; db $83, $02                     ;Sprite 083 do event: Move Right
; db $83, $24                     ;Sprite 083 do event: face down, right hand raised in
; db $85, $24                     ;Sprite 085 do event: face down, right hand raised in
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $88, $04                     ;Sprite 088 do event: Move Left
; db $89, $02                     ;Sprite 089 do event: Move Right
; db $8A, $03                     ;Sprite 08A do event: Move Down
; db $CF, $02, $04                ;Play next 04 bytes simultaneously 02 times
; db $8A, $04                     ;Sprite 08A do event: Move Left
; db $86, $01                     ;Sprite 086 do event: Move Up
; db $88, $22                     ;Sprite 088 do event: face down, left hand on head
; db $89, $26                     ;Sprite 089 do event: face up, right hand raised out
; db $8A, $22                     ;Sprite 08A do event: face down, left hand on head
; db $84, $03                     ;Sprite 084 do event: Move Down
; db $84, $04                     ;Sprite 084 do event: Move Left
; db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
; db $84, $50                     ;Sprite 084 do event: 50
; db $82, $03                     ;Sprite 082 do event: Move Down
; db $14                          ;Player pose: face down, left hand forward
; db $09                          ;Player Show
; db $D3, $82, $00, $00           ;Sprite 82 set map position 00, 00
; db $84, $20                     ;Sprite 084 do event: face down, left hand raised out
; db $C7, $04                     ;Play next 04 bytes simultaneously
; db $83, $03                     ;Sprite 083 do event: Move Down
; db $85, $03                     ;Sprite 085 do event: Move Down
; db $86, $52                     ;Sprite 086 do event: 52
; db $86, $20                     ;Sprite 086 do event: face down, left hand raised out
; db $84, $02                     ;Sprite 084 do event: Move Right
; db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
; db $CE, $04, $0A                ;Play next 0A bytes 04 times
; db $84, $46                     ;Sprite 084 do event: garbage
; db $86, $52                     ;Sprite 086 do event: 52
; db $70                          ;Very short pause
; db $84, $47                     ;Sprite 084 do event: face down, left hand up in
; db $86, $20                     ;Sprite 086 do event: face down, left hand raised out
; db $70                          ;Very short pause
; db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
; db $84, $3E                     ;Sprite 084 do event: face up, both arms raised in
; db $70                          ;Very short pause
; db $84, $24                     ;Sprite 084 do event: face down, right hand raised in
; db $84, $20                     ;Sprite 084 do event: face down, left hand raised out
; db $2E                          ;Player pose: face down, head lowered
; db $14                          ;Player pose: face down, left hand forward
; db $C7, $06                     ;Play next 06 bytes simultaneously
; db $84, $01                     ;Sprite 084 do event: Move Up
; db $85, $02                     ;Sprite 085 do event: Move Right
; db $83, $04                     ;Sprite 083 do event: Move Left
; db $84, $0A                     ;Sprite 084 do event: Hide
; db $83, $0A                     ;Sprite 083 do event: Hide
; db $85, $0A                     ;Sprite 085 do event: Hide
; db $DB                          ;Restore Player status
; db $86, $03                     ;Sprite 086 do event: Move Down
; db $86, $03                     ;Sprite 086 do event: Move Down
; db $88, $12                     ;Sprite 088 do event: face right, standing
; db $89, $12                     ;Sprite 089 do event: face right, standing
; db $8A, $12                     ;Sprite 08A do event: face right, standing
; db $86, $12                     ;Sprite 086 do event: face right, standing
; db $A2, $6B                     ;Set Event Flag 06B
; db $FF                          ;End Event

; padbyte $00
; pad $C8D14B