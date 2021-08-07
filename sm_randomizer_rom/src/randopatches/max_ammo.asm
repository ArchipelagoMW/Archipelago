lorom

; change the icons for the missiles, super missiles, and power bombs so we can display maximum amounts
org $9AB540  ; location in vanilla SM
DB $FF,$80,$9F,$7F,$B2,$7F,$AE,$73,$AE,$73,$B2,$7F,$9F,$7F,$FF,$80  ; left half of super missile tile
DB $FF,$01,$F1,$FE,$FD,$2E,$2B,$F6,$FB,$26,$2D,$FE,$F1,$FE,$FF,$01  ; right half of super missile tile
DB $FF,$80,$83,$7F,$86,$7F,$8F,$7A,$8E,$7B,$87,$7E,$83,$7F,$FF,$80  ; left half of power bomb tile
DB $FF,$01,$C1,$FE,$61,$FE,$F1,$5E,$71,$DE,$E1,$7E,$C1,$FE,$FF,$01  ; right half of power bomb tile

org $9AB5C0  ; location in vanilla SM
; now we need to update the number tiles so they look right on the max ammo display
DB $3C,$C3,$7C,$9B,$7C,$BB,$7C,$9B,$3C,$DB,$3C,$DB,$3C,$C3,$00,$FF  ; 1
DB $FE,$01,$FF,$7C,$7F,$86,$FF,$3C,$FF,$60,$FF,$7E,$FF,$00,$00,$FF  ; 2
DB $FE,$01,$FF,$7C,$FF,$06,$7F,$BC,$FF,$06,$FF,$7C,$FE,$01,$00,$FF  ; 3
DB $3E,$C1,$7E,$9D,$FE,$2D,$FF,$4C,$FF,$7E,$FF,$0C,$1E,$E1,$00,$FF  ; 4
DB $FF,$00,$FF,$7C,$FE,$61,$FF,$7C,$FF,$06,$FF,$7C,$FE,$01,$00,$FF  ; 5
DB $7E,$81,$FE,$3D,$FE,$61,$FF,$7C,$FF,$66,$FF,$3C,$7E,$81,$00,$FF  ; 6
DB $FF,$00,$FF,$7E,$FF,$06,$3F,$CC,$3E,$D9,$3C,$DB,$3C,$C3,$00,$FF  ; 7
DB $7E,$81,$FF,$3C,$FF,$66,$FF,$3C,$FF,$66,$FF,$3C,$7E,$81,$00,$FF  ; 8
DB $7E,$81,$FF,$3C,$FF,$66,$FF,$3E,$7F,$86,$7F,$BC,$7E,$81,$00,$FF  ; 9
DB $7E,$81,$FF,$3C,$FF,$66,$FF,$66,$FF,$66,$FF,$3C,$7E,$81,$00,$FF  ; 0

org $9AB690  ; location in crossover
DB $FF,$80,$80,$7F,$87,$7F,$89,$7E,$89,$7E,$87,$7F,$80,$7F,$FF,$80  ; left third of missile tile
DB $FF,$00,$E3,$FF,$1F,$FE,$FF,$21,$E1,$3F,$1E,$FF,$E3,$FF,$FF,$00  ; middle third of missile tile
DB $FF,$01,$F9,$FE,$F1,$1E,$21,$FE,$E1,$3E,$11,$FE,$F9,$FE,$FF,$01  ; right third of missile tile

; now it's time to do all of the code changes necessary for HUD display
; skip drawing part of the original missile icon in the HUD
org $8099E1  ; location in vanilla SM
rep 21 : nop

org $809ACE
NOP : NOP : NOP : NOP  ; wipe out a JSL call

org $809AD7
NOP : NOP : NOP : NOP  ; wipe out a JSL call

org $809AE0
NOP : NOP : NOP : NOP  ; wipe out a JSL call

org $809B0C
JSR Missile_Counter  ; person's code has this going to $80CDA0, but that may change so it's looking at a label instead

org $809B1A
JSR Super_Counter  ; person's code has this going to $80CDAD, but that may change so it's looking at a label instead

org $809B28
JSR Power_Counter  ; person's code has this going to $80CDBA, but that may change so it's looking at a label instead

org $809C00
JSR Running_Counter  ; originally LDA $09C8

org $80CDA0
; luckily this chunk of free space is in the same relative location in the crossover, so no JSRs need to change to JSLs!
; copypasta person's code, but removed all of the definitions he created in case of conflicts with additional files being used
	Missile_Counter:
		JSR $9D78	;game's original number calculation routine for current ammo
		LDA $09C8	;max missiles
		LDX #$0014
		JMP $9D78	;this time to display the max ammo
		; RTS
	
	Super_Counter:
		JSR $9D98
		LDA $09CC	;max supers
		LDX #$001C
		JMP $9D98
		; RTS
	
	Power_Counter:
		JSR $9D98
		LDA $09D0	;max powers
		LDX #$0022
		JMP $9D98
		; RTS

	Running_Counter:
		PHA : PHX : PHY
		LDA $09C8
		BEQ + : JSR MissileMax
		+ : LDA $09CC
		BEQ + : JSR SuperMax
		+ : LDA $09D0
		BEQ + : JSR PowerMax
		+ : PLY : PLX : PLA
		LDA $09C8
		RTS
	
	MissileMax:
		JSR Triple_Counter
		LDA $09D2
		CMP #$0001
		BEQ +
		LDA #$1400 : STA $18 : BRA ++							;Load gray color for icons, put in $18
		+ : LDA #$1000 : STA $18 : ++							;Load green color for icons, put in $18
		LDX $12 : LDA SM_Numbers,x : ORA $18 : STA $7EC61C	;Draw SM_Numbers
		LDX $14 : LDA SM_Numbers,x : ORA $18 : STA $7EC61E
		LDX $16 : LDA SM_Numbers,x : ORA $18 : STA $7EC620
		LDA #$0049 : ORA $18 : STA $7EC65C		;Load new missile icon, pieced together from graphics starting at D3200, and store them to the HUD
		LDA #$004A : ORA $18 : STA $7EC65E
		LDA #$004B : ORA $18 : STA $7EC660
		RTS
		
	SuperMax:
		JSR Double_Counter
		LDA $09D2
		CMP #$0002
		BEQ +
		LDA #$1400 : STA $18 : BRA ++
		+ : LDA #$1000 : STA $18 : ++
		LDX $14 : LDA SM_Numbers,x : ORA $18 : STA $7EC624
		LDX $16 : LDA SM_Numbers,x : ORA $18 : STA $7EC626
		LDA #$0034 : ORA $18 : STA $7EC664
		LDA #$0035 : ORA $18 : STA $7EC666
		RTS
		
	PowerMax:
		JSR Double_Counter
		LDA $09D2
		CMP #$0003
		BEQ +
		LDA #$1400 : STA $18 : BRA ++
		+ : LDA #$1000 : STA $18 : ++
		LDX $14 : LDA SM_Numbers,x : ORA $18 : STA $7EC62A
		LDX $16 : LDA SM_Numbers,x : ORA $18 : STA $7EC62C
		LDA #$0036 : ORA $18 : STA $7EC66A
		LDA #$0037 : ORA $18 : STA $7EC66C
		RTS
		
	Triple_Counter:								;Current Missile counter: brain melting simple math
		STA $4204							;ex 125. 125/?
		SEP #$20
		LDA #$64 : STA $4206					;xxx/100
		PHA : PLA : PHA : PLA					;...125/100...
		REP #$20
		LDA $4214 : ASL A : STA $12	;qoutient = 1. 1*2 then store
		LDA $4216 : STA $4204			;remainder = 25
		SEP #$20
		LDA #$0A : STA $4206					;xx/10
		PHA : PLA : PHA : PLA					;...25/10...
		REP #$20
		LDA $4214 : ASL A : STA $14		;qoutient = 2. 2*2 then store
		LDA $4216 : ASL A : STA $16		;remainder = 5. 5*2 then store
		RTS
		
	Double_Counter:
		STA $4204
		SEP #$20
		LDA #$0A : STA $4206
		PHA : PLA : PHA : PLA
		REP #$20
		LDA $4214 : ASL A : STA $14
		LDA $4216 : ASL A : STA $16
		RTS
		
	SM_Numbers:
		DW #$0045, #$003C, #$003D, #$003E, #$003F, #$0040, #$0041, #$0042, #$0043, #$0044

org $858851
; data, message boxes specifically
DB $0F,$28,$0F,$28,$0F,$28

org $858891
DB $49,$30,$4A,$30,$4B,$30

org $858951
DB $0F,$28,$0F,$28,$0F,$28

org $858993
DB $34,$30,$35,$30

org $858A4F
DB $0F,$28,$0F,$28

org $858A8F
DB $36,$30,$37,$30
