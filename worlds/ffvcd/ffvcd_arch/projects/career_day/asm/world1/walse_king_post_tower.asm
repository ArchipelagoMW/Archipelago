hirom


; disable most of the conversation with the walse king after the tower sinks
org $C872DA

db $A2, $29			;Set Event Flag 029
db $A0, $01			;(Message) 01
db $FF

padbyte $00
pad $C8731A