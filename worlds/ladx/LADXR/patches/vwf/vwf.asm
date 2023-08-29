
variableWidthFontThunk:
	call variableWidthFont
	pop hl
	jp $2663 ; jp .noDiacritic
	

variableWidthFont:
	; If it's a linebreak
	cp $FD
	call z, newLinebreak

	; If it's blank
	cp $00
	ret z
	
	; If it's the first character
	ld a, [wDialogCharacterIndex]
	cp $00
	call z, initVWF

	call initTile

 	ld a, [PIXELS_TO_ADD]
	cp   $00
	jr   z, .NoRight
	call MoveRight
	jr   .NextR
 .NoRight:
	ld   d, $01
	ld   bc, CURR_CHAR_BUFFER
	ld   hl, TILE_BUFFER
	call CopyLine
 .NextR:

	ld   a, [CURR_CHAR_SIZE]
	ld   e, a
	ld   a, [PIXELS_TO_ADD]
	add  a, e
	ld   [CURR_CHAR_SIZE], a
	cp   8						; Current size compared to a tile (8px)
	jr   z, .EqualTo
	jr   c, .LessThan

 .MoreThan:
	sub  a, 8
	ld   [CURR_CHAR_SIZE], a
	ld   [PIXELS_TO_ADD], a
	ld   d, a
	ld   a, e
	sub  a, d
	ld   [PIXELS_TO_SUBTRACT], a
	ld   a, $01
	ld   [IS_TILE_READY], a
	ld   [IS_CHAR_READY], a
	jr   .WidthSet

 .EqualTo:
	xor a
	ld   [CURR_CHAR_SIZE], a
	ld   [PIXELS_TO_ADD], a
	ld   [PIXELS_TO_SUBTRACT], a
	ld   a, $01
	ld   [IS_TILE_READY], a
	ld   [IS_CHAR_READY], a
	jr   .WidthSet

 .LessThan:
	ld   [PIXELS_TO_ADD], a

	xor a
	ld   [PIXELS_TO_SUBTRACT], a
	ld   [IS_TILE_READY], a

 .WidthSet:
	ld   a, [IS_TILE_READY]
	cp   $00
	ret z

	call IncrementTile
 .PushCharacter:
	ld   d, $01
	ld   bc, TILE_BUFFER
	ld   hl, CURR_CHAR_GFX
	call CopyLine

	call clearTileBuffer

MoveLeft:
	ld   a, [PIXELS_TO_SUBTRACT]
	cp   a, $00
	ret  z

	ld   b, $10
	ld   hl, TILE_BUFFER
	ld   de, CURR_CHAR_BUFFER

 .Next:
	ld   a, [PIXELS_TO_SUBTRACT]
	ld   c, a
	ld   a, [de]
	cpl
 .Loop:
	sla   a
	dec   c
	jr   nz, .Loop
	or   a, [hl]
	ldi  [hl], a
	inc  de
	dec  b
	jr nz, .Next
	ret

MoveRight:
	ld   b, $10
	ld   hl, TILE_BUFFER
	ld   de, CURR_CHAR_BUFFER

 .Next:
	ld   a, [PIXELS_TO_ADD]
	ld   c, a
	ld   a, [de]
	cpl
 .Loop:
	srl   a
	dec   c
	jr   nz, .Loop
	or   a, [hl]
	ldi  [hl], a
	inc  de
	dec  b
	jr nz, .Next

	ret

CopyLine:
	ld   e, 16
 .Loop:
	ld   a, d
	cp   a, $00
	ld   a, [bc]
	jr   z, .NoFlip
	cpl
 .NoFlip:
	ldi  [hl], a
	inc  bc
	dec  e
	jr   nz, .Loop
	ret

initVWF:
	xor a
	ld hl, $D668
	ldi [hl],a	; $D668
	ldi [hl],a	; $D668Hi
	ldi [hl],a	; PIXELS_TO_SUBTRACT
	ldi [hl],a	; PIXELS_TO_ADD
	
	; If wDialogState = $8x, the textbox is in the bottom
	ld a, [wDialogState]
	and $F0
	cp $80
	ld a, $62
	jr z, .bottomTextbox
	ld a, $42
 .bottomTextbox:
	ld [wDrawCommand.destinationLow], a	; Forces the BG copy to the first letter's position

	ld   d, $00
	ld   bc, CURR_CHAR_GFX
	ld   hl, CURR_CHAR_BUFFER
	call CopyLine
	
clearTileBuffer:
	xor a
	ld b, $10
	ld hl, TILE_BUFFER
 .Loop:
	ldi [hl], a
	dec b
	jr nz, .Loop
	ret

initTile:
	ld   d, $00
	ld   bc, CURR_CHAR_GFX
	ld   hl, CURR_CHAR_BUFFER
	call CopyLine
	ret

IncrementTile:
	ld   a, [$D668]
	cp $2F
	jr nz, .noWrap
	xor a
	jr .wrap
   .noWrap:
    add  a, $01
   .wrap:
    ld   [$D668], a
	ret

newLinebreak:
	ld a, [$D668]
	and $F0
	cp $00
	jr z, .firstLine
	cp $20
	jr z, .lineCR
	ld a, $1F
	ld [wDialogNextCharPosition], a
	inc a
	jr .setLine

  .lineCR:
  	ld a, $1F
	ld [wDialogNextCharPosition], a
  .firstLine:
	ld a, $10
  .setLine:
	ld [$D668], a
	call variableWidthFont.PushCharacter
	xor a
	ld [CURR_CHAR_SIZE], a
	ld [PIXELS_TO_ADD], a
	ret