;;; disable demos to avoid crash in area rando
;;; compile with asar

lorom
arch snes.cpu
	
;;; original code, timer in $1F53:
;;; $8B:9F29 CE 53 1F    DEC $1F53  [$7E:1F53]
;;; $8B:9F2C F0 02       BEQ $02    [$9F30]
;;; $8B:9F2E 10 08       BPL $08    [$9F38]
org $8B9f2C
    bra loop                    ; no longer branch when timer is zero
org $8B9F38
loop:
