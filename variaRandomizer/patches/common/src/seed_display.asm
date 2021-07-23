arch snes.cpu
lorom

// Inject new menu graphic data after decompression
org $82ecbb
	jsr $f900

org $82f900
	pha
	phx
    php
    rep #$30

    lda $dfff00
    and #$001f
    asl
    asl
    asl
    tay
    ldx #$0000
-
    lda WordTable, y
    and #$00ff
    asl
    phx
    tax
    lda CharTable, x
    plx
    sta $7fc052, x
    inx
    inx
    iny
    cpx #$000E
    bne -

    lda $dfff01
    and #$001f
    asl
    asl
    asl
    tay
    ldx #$0000
-
    lda WordTable, y
    and #$00ff
    asl
    phx
    tax
    lda CharTable, x
    plx
    sta $7fc060, x
    inx
    inx
    iny
    cpx #$000E
    bne -

    lda $dfff02
    and #$001f
    asl
    asl
    asl
    tay
    ldx #$0000
-
    lda WordTable, y
    and #$00ff
    asl
    phx
    tax
    lda CharTable, x
    plx
    sta $7fc092, x
    inx
    inx
    iny
    cpx #$000E
    bne -

    lda $dfff03
    and #$001f
    asl
    asl
    asl
    tay
    ldx #$0000
-
    lda WordTable, y
    and #$00ff
    asl
    phx
    tax
    lda CharTable, x
    plx
    sta $7fc0a0, x
    inx
    inx
    iny
    cpx #$000E
    bne -
    
    plp
	plx
	pla
    ldx #$07fe
	rts

CharTable:
	// 0x00																				  	     0x0F
	dw $000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f
	// 0x10																				  	     0x0F
	dw $000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f,$000f
	// 0x20																				  	     0x0F
	dw $000f,$0084,$002d,$000f,$000f,$000f,$000f,$0022,$008a,$008b,$000f,$0086,$0089,$0087,$0088,$000f
NumTable:
	// 0x30																				  	     0x0F
	dw $0060,$0061,$0062,$0063,$0064,$0065,$0066,$0067,$0068,$0069,$000f,$000f,$000f,$000f,$000f,$0085
	// 0x40																				  	     0x0F
	dw $000f,$006a,$006b,$006c,$006d,$006e,$006f,$0070,$0071,$0072,$0073,$0074,$0075,$0076,$0077,$0078
	// 0x50																				  	     0x0F
	dw $0079,$007a,$007b,$007c,$007d,$007e,$007f,$0080,$0081,$0082,$0083,$000f,$000f,$000f,$000f,$000f

WordTable:
    db "GEEMER  "
    db "RIPPER  "
    db "ATOMIC  "
    db "POWAMP  "
    db "SCISER  "
    db "NAMIHE  "
    db "PUROMI  "
    db "ALCOON  "
    db "BEETOM  "
    db "OWTCH   "
    db "ZEBBO   "
    db "ZEELA   "
    db "HOLTZ   "
    db "VIOLA   "
    db "WAVER   "
    db "RINKA   "
    db "BOYON   "
    db "CHOOT   "
    db "KAGO    "
    db "SKREE   "
    db "COVERN  "
    db "EVIR    "
    db "TATORI  "
    db "OUM     "
    db "PUYO    "
    db "YARD    "
    db "ZOA     "
    db "FUNE    "
    db "GAMET   "
    db "GERUTA  "
    db "SOVA    "
    db "BULL    "

// place holder for VARIA seed type
InfoStr:
    db 0
// VARIA: placeholder for 'nothing' loc identifier (defaults to morph ball loc)
NothingId:
   db $1a
