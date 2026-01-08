hirom


; $C9AD5E → $C9AD8C
; This was another anomaly. It's not like others with a clear cut start/finish. In this case there were problems padding, so I left in $00's along the way 

org $C9AD5E

db $88, $0A                     ;Sprite 088 do event: Hide
db $89, $0A                     ;Sprite 089 do event: Hide
db $8A, $0A                     ;Sprite 08A do event: Hide
db $8B, $0A                     ;Sprite 08B do event: Hide
;db $70
db $00
db $CD, $8B, $00                ;Run event index 008B
;db $C8, $82, $86                ;Display Message/Text/Dialogue 82 86
db $00, $00, $00
db $CD, $8C, $00                ;Run event index 008C
;db $C8, $83, $86                ;Display Message/Text/Dialogue 83 86
db $00, $00, $00
db $CD, $BA, $00                ;Run event index 00BA
db $CD, $B1, $05                ;Run event index 05B1
db $CD, $3F, $03                ;Run event index 033F
db $CB, $2C, $00                ;Clear Flag 2/3/4/5/2C 00
db $A2, $82                     ;Set Event Flag 082
db $FF                          ;End Event
