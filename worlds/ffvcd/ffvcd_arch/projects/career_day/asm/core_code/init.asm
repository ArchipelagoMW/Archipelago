hirom


; this code standardizes the romfile to be 4MB 
org !ADDRESS_STARTROM
padbyte $00
pad !ADDRESS_ENDROM
org !ADDRESS_ENDROM
db $00

; in the event vanilla rewards is set to 0 (randomization) but values arent written to E79F00 for starting job/weapon/magic
; without this, default 'job' would be highly messed up 
org $E79F00
db $15, $38, $FF, $20