
;code made by lioran
!speed = $0003 ;changeing this will force you to change !timer aswell dont go higher than 8
!timer = $0018 ;$0C is good for speed 5
			   ;$10 is good for speed 4
			   ;$18 good for speed 3,
			   ;$20 good for 2
			   ;$if you see samus stick out the bottom, increase the value, if stick out the top, lower the value
!freespace = $A3F320 ;get some free space from your hack  need 43 bytes
!freeram = $0741 ;just some free ram that's used for the timer from bank 7E if you need to change it somehow.

lorom

org $A39581
JSL !freespace ;hijack the elevator transition code for down elevator cause just setting the speed of that one cause unwanted visual effect.
NOP #$15

org !freespace ;write your code at the free space

STZ $0799
LDA #$0008 : CMP $0998 : BNE ++  ;check game state is 08, if it is go on
STZ !freeram ;set free ram to 0
JMP +++
++
LDA #!timer : CMP !freeram : BEQ + ;if timer is not equal to !timer then increase by 1.
LDA !freeram : INC A : STA !freeram ;increase timer by 1
+++
LDA $0F7E, x ;samus y position ram position
CLC : ADC #!speed ;move samus !speed amount vertically down
STA $0F7E, x
+
RTL

;set other elevator speed to !speed aswell those dont need to have a fix to it
org $A395D2
DB !speed

org $A395EC
DB !speed

org $A395B0
DB !speed
