;Changes how the end percentage in calculated. Made by Sadiztyk Fish   :P

;Allows tanks with multiple values (eg. missile tanks worth either 3 or 5)
;Allows an uneven or random number of items (up to 255 separate item pickups)
;Adds a single decimal point value, to give more accurate results to random item ammounts

!CollectedItems  = $7ED86E
!TotalItems      = #$64	;TOTAL number if items in the game. This includes ALL items: missiles, upgrades, etc

LOROM
arch snes.cpu
	
org $84889F
	JSL COLLECTTANK
org $84F830 			; FLO: changed original adress to avoid conflict with other patches
COLLECTTANK:
	PHA
	LDA !CollectedItems
	INC A
	STA !CollectedItems
	PLA
	JSL $80818E
	RTL
warnpc $84f840

org $8BE627
	PHP
	PHB
	PHK
	PLB
	REP #$30
	PHX
	PHY
	SEP #$20
	STZ $12
	LDA !CollectedItems				;Load number of collected items in the game
	STA $4202
	LDA #$64					;Load #100 decimal
	STA $4203
	PHA : PLA : XBA : XBA
	REP #$20
	LDA $4216					;Load number of (collected items * 100)
	STA $4204					;Store to devisor A
	SEP #$20
print "1st TotaItems (add 1) : ", pc
	LDA !TotalItems					;Load total number of game items ; FLO: this has to be changed at ROM patch phase
	STA $4206					;Store to devisor B
	PHA : PLA : XBA : XBA
	REP #$20
	LDA $4214					;Load ((collected items * 100)/Total items) ie Item percent
	STA $4204
	LDA $4216					;Load remainder
	PHA
	SEP #$20
	LDA #$0A
	STA $4206
	PHA : PLA : XBA : XBA				;Calculate percentage / 10
	REP #$20
	LDA $4214					;Load tenths of percentage / 10 (eg, if 78, load 7, if 53, load 5)
	STA $4204					;Store value to devisor A
	LDA $4216					;Load remainder of percentage / 10 (eg, if 78, load 8, if 53, load 3)
	STA $16						;Store to $16. oneths of percentage. if 78, = 8, if 100, = 0
	SEP #$20
	LDA #$0A
	STA $4206					
	PHA : PLA : XBA : XBA				;Divide percentage by 10 again
	REP #$20
	LDA $4214					;If 100%, this will be 1
	STA $12						;Store to $12. Contains 100th of percentage. WIll only be 1 if 100% achieved
	LDA $4216					;Load remainder, which will be 0 if 100% achieved
	STA $14						;Store to $14
	PLA						; gets initial division remainder to have decimal point
	SEP #$20
	STA $4202
	LDA #$0A					;Load #10 decimal
	STA $4203
	PHA : PLA : XBA : XBA
	REP #$20
	LDA $4216					;Load (remainder * 10) and use it to divide by number of items
	STA $4204
	SEP #$20
print "2nd TotaItems (add 1) : ", pc
	LDA !TotalItems	                                ; FLO : patch this value to have accurate decimal point
	STA $4206					
	PHA : PLA : XBA : XBA				;Divide remainder*10 by number of items
	REP #$20
	LDA $4214					;load value
	STA $18
HUNDREDTHS:
	LDA $12						;Load hundredths value
	BEQ TENTHS					;If 0, don't draw hundredths digit
	ASL A : ASL A
	TAY
	LDA $E741,y
	STA $7E339A
	LDA $E743,y
	STA $7E33DA
TENTHS:
	LDA $14						;Load tenths value
	BNE DRAWTENTHS					;If more than 0, draw tenths digit
	LDA $12						;If 0, load hundredths value
	BEQ ONETHS					;If hundredths is 0, don't draw tenths digit
	LDA $14
DRAWTENTHS:
	ASL A : ASL A
	TAY
	LDA $E741,y
	STA $7E339C
	LDA $E743,y
	STA $7E33DC
ONETHS:
	LDA $16						;load oneths value
	ASL A : ASL A
	TAY
	LDA $E741,y
	STA $7E339E
	LDA $E743,y
	STA $7E33DE
	LDA #$385A					;Load decimal point sign
	STA $7E33E0
	LDA $18						;load one/tenths value
	ASL A : ASL A
	TAY
	LDA $E741,y
	STA $7E33A2
	LDA $E743,y
	STA $7E33E2
	LDA #$386A					;draw percentage sign
	STA $7E33A4
	LDA #$387A
	STA $7E33E4
	PLY
	PLX
	PLB
	PLP
	RTS

warnpc $8be740
