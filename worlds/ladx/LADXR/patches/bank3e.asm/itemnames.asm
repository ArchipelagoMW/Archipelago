
BuildRemoteItemMessage:
    ld   de, wCustomMessage
    call CustomItemMessageThreeFour
    ld   a, $A0 ; low of wCustomMessage
    cp   e
    ret  nz

BuildItemMessage:    
    ld   hl, ItemNamePointers
    ldh  a, [$F1]
    ld   d, $00
    ld   e, a
    add  hl, de
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a
    ld   de, wCustomMessage
    jp   MessageCopyString
    
    ; And then see if the custom item message func wants to override

    ; add hl, de
    

CustomItemMessageThreeFour:
    ; the stack _should_ have the address to return to here, so we can just pop it when we're done
    ld   a,  $34   ; Set bank number
    ld   hl, $4000 ; Set next address
    push hl
    jp   $080C ; switch bank

FoundItemForOtherPlayerPostfix:
    db m" for player X", $ff
GotItemFromOtherPlayerPostfix:
    db m" from player X", $ff
SpaceFrom:
    db " from ", $ff, $ff
SpaceFor:
    db " for ", $ff, $ff
MessagePad:
    jr .start    ; goto start
.loop:
    ld   a, $20  ; a = ' '
    ld   [de], a ; *de = ' '
    inc  de      ; de++
    ld   a, $ff  ; a = 0xFF
    ld   [de], a ; *de = 0xff
.start:
    ld   a, e    ; a = de & 0xF
    and  $0F     ; a &= 0x0xF
    jr   nz, .loop ; if a != 0, goto loop
    ret

MessageAddTargetPlayer:
    call MessagePad
    ld   hl, FoundItemForOtherPlayerPostfix
    call MessageCopyString
    ret

MessageAddFromPlayerOld:
    call MessagePad
    ld   hl, GotItemFromOtherPlayerPostfix
    call MessageCopyString
    ret

; hahaha none of this follows calling conventions
MessageAddPlayerName:
    ; call MessagePad

    cp  101
    jr  C, .continue
    ld  a, 100
.continue:
    ld  h, 0 ; bc = a, hl = a
    ld  l, a
    ld  b, 0
    ld  c, a
    add hl, hl ; 2
    add hl, hl ; 4
    add hl, hl ; 8
    add hl, hl ; 16
    add hl, bc ; 17
    ld  bc, MultiNamePointers
    add hl, bc ; hl = MultiNamePointers + wLinkGiveItemFrom * 17
    
    call MessageCopyString
    ret

ItemNamePointers:
    dw ItemNamePowerBracelet
    dw ItemNameShield
    dw ItemNameBow
    dw ItemNameHookshot
    dw ItemNameMagicRod
    dw ItemNamePegasusBoots
    dw ItemNameOcarina
    dw ItemNameFeather
    dw ItemNameShovel
    dw ItemNameMagicPowder
    dw ItemNameBomb
    dw ItemNameSword
    dw ItemNameFlippers
    dw ItemNameNone
    dw ItemNameBoomerang
    dw ItemNameSlimeKey
    dw ItemNameMedicine
    dw ItemNameTailKey
    dw ItemNameAnglerKey
    dw ItemNameFaceKey
    dw ItemNameBirdKey
    dw ItemNameGoldLeaf
    dw ItemNameMap
    dw ItemNameCompass
    dw ItemNameStoneBeak
    dw ItemNameNightmareKey
    dw ItemNameSmallKey
    dw ItemNameRupees50
    dw ItemNameRupees20
    dw ItemNameRupees100
    dw ItemNameRupees200
    dw ItemNameRupees500
    dw ItemNameSeashell
    dw ItemNameMessage
    dw ItemNameGel
    dw ItemNameKey1
    dw ItemNameKey2
    dw ItemNameKey3
    dw ItemNameKey4
    dw ItemNameKey5
    dw ItemNameKey6
    dw ItemNameKey7
    dw ItemNameKey8
    dw ItemNameKey9
    dw ItemNameMap1
    dw ItemNameMap2
    dw ItemNameMap3
    dw ItemNameMap4
    dw ItemNameMap5
    dw ItemNameMap6
    dw ItemNameMap7
    dw ItemNameMap8
    dw ItemNameMap9
    dw ItemNameCompass1
    dw ItemNameCompass2
    dw ItemNameCompass3
    dw ItemNameCompass4
    dw ItemNameCompass5
    dw ItemNameCompass6
    dw ItemNameCompass7
    dw ItemNameCompass8
    dw ItemNameCompass9
    dw ItemNameStoneBeak1
    dw ItemNameStoneBeak2
    dw ItemNameStoneBeak3
    dw ItemNameStoneBeak4
    dw ItemNameStoneBeak5
    dw ItemNameStoneBeak6
    dw ItemNameStoneBeak7
    dw ItemNameStoneBeak8
    dw ItemNameStoneBeak9
    dw ItemNameNightmareKey1
    dw ItemNameNightmareKey2
    dw ItemNameNightmareKey3
    dw ItemNameNightmareKey4
    dw ItemNameNightmareKey5
    dw ItemNameNightmareKey6
    dw ItemNameNightmareKey7
    dw ItemNameNightmareKey8
    dw ItemNameNightmareKey9
    dw ItemNameToadstool
    dw ItemNameGuardianAcorn
    dw ItemNameNone ; 0x52
    dw ItemNameNone ; 0x53
    dw ItemNameNone ; 0x54
    dw ItemNameNone ; 0x55
    dw ItemNameNone ; 0x56
    dw ItemNameNone ; 0x57
    dw ItemNameNone ; 0x58
    dw ItemNameNone ; 0x59
    dw ItemNameNone ; 0x5a
    dw ItemNameNone ; 0x5b
    dw ItemNameNone ; 0x5c
    dw ItemNameNone ; 0x5d
    dw ItemNameNone ; 0x5e
    dw ItemNameNone ; 0x5f
    dw ItemNameNone ; 0x60
    dw ItemNameNone ; 0x61
    dw ItemNameNone ; 0x62
    dw ItemNameNone ; 0x63
    dw ItemNameNone ; 0x64
    dw ItemNameNone ; 0x65
    dw ItemNameNone ; 0x66
    dw ItemNameNone ; 0x67
    dw ItemNameNone ; 0x68
    dw ItemNameNone ; 0x69
    dw ItemNameNone ; 0x6a
    dw ItemNameNone ; 0x6b
    dw ItemNameNone ; 0x6c
    dw ItemNameNone ; 0x6d
    dw ItemNameNone ; 0x6e
    dw ItemNameNone ; 0x6f
    dw ItemNameNone ; 0x70
    dw ItemNameNone ; 0x71
    dw ItemNameNone ; 0x72
    dw ItemNameNone ; 0x73
    dw ItemNameNone ; 0x74
    dw ItemNameNone ; 0x75
    dw ItemNameNone ; 0x76
    dw ItemNameNone ; 0x77
    dw ItemNameNone ; 0x78
    dw ItemNameNone ; 0x79
    dw ItemNameNone ; 0x7a
    dw ItemNameNone ; 0x7b
    dw ItemNameNone ; 0x7c
    dw ItemNameNone ; 0x7d
    dw ItemNameNone ; 0x7e
    dw ItemNameNone ; 0x7f
    dw ItemNameHeartPiece ; 0x80
    dw ItemNameBowwow
    dw ItemName10Arrows
    dw ItemNameSingleArrow
    dw ItemNamePowderUpgrade
    dw ItemNameBombUpgrade
    dw ItemNameArrowUpgrade
    dw ItemNameRedTunic
    dw ItemNameBlueTunic
    dw ItemNameHeartContainer
    dw ItemNameBadHeartContainer
    dw ItemNameSong1
    dw ItemNameSong2
    dw ItemNameSong3
    dw ItemInstrument1
    dw ItemInstrument2
    dw ItemInstrument3
    dw ItemInstrument4
    dw ItemInstrument5
    dw ItemInstrument6
    dw ItemInstrument7
    dw ItemInstrument8
    dw ItemRooster
    dw ItemTradeQuest1
    dw ItemTradeQuest2
    dw ItemTradeQuest3
    dw ItemTradeQuest4
    dw ItemTradeQuest5
    dw ItemTradeQuest6
    dw ItemTradeQuest7
    dw ItemTradeQuest8
    dw ItemTradeQuest9
    dw ItemTradeQuest10
    dw ItemTradeQuest11
    dw ItemTradeQuest12
    dw ItemTradeQuest13
    dw ItemTradeQuest14
    dw ItemPieceOfPower

ItemNameNone:
    db m"NONE", $ff

ItemNamePowerBracelet:
    db m"Got the {POWER_BRACELET}", $ff
ItemNameShield:
    db m"Got a {SHIELD}", $ff
ItemNameBow:
    db m"Got the {BOW}", $ff
ItemNameHookshot:
    db m"Got the {HOOKSHOT}", $ff
ItemNameMagicRod:
    db m"Got the {MAGIC_ROD}", $ff
ItemNamePegasusBoots:
    db m"Got the {PEGASUS_BOOTS}", $ff
ItemNameOcarina:
    db m"Got the {OCARINA}", $ff
ItemNameFeather:
    db m"Got the {FEATHER}", $ff
ItemNameShovel:
    db m"Got the {SHOVEL}", $ff
ItemNameMagicPowder:
    db m"Got {MAGIC_POWDER}", $ff
ItemNameBomb:
    db m"Got {BOMB}", $ff
ItemNameSword:
    db m"Got a {SWORD}", $ff
ItemNameFlippers:
    db m"Got the {FLIPPERS}", $ff
ItemNameBoomerang:
    db m"Got the {BOOMERANG}", $ff
ItemNameSlimeKey:
    db m"Got the {SLIME_KEY}", $ff
ItemNameMedicine:
    db m"Got some {MEDICINE}", $ff
ItemNameTailKey:
    db m"Got the {TAIL_KEY}", $ff
ItemNameAnglerKey:
    db m"Got the {ANGLER_KEY}", $ff
ItemNameFaceKey:
    db m"Got the {FACE_KEY}", $ff
ItemNameBirdKey:
    db m"Got the {BIRD_KEY}", $ff
ItemNameGoldLeaf:
    db m"Got the {GOLD_LEAF}", $ff
ItemNameMap:
    db m"Got the {MAP}", $ff
ItemNameCompass:
    db m"Got the {COMPASS}", $ff
ItemNameStoneBeak:
    db m"Got the {STONE_BEAK}", $ff
ItemNameNightmareKey:
    db m"Got the {NIGHTMARE_KEY}", $ff
ItemNameSmallKey:
    db m"Got a {KEY}", $ff
ItemNameRupees50:
    db m"Got 50 {RUPEES}", $ff
ItemNameRupees20:
    db m"Got 20 {RUPEES}", $ff
ItemNameRupees100:
    db m"Got 100 {RUPEES}", $ff
ItemNameRupees200:
    db m"Got 200 {RUPEES}", $ff
ItemNameRupees500:
    db m"Got 500 {RUPEES}", $ff
ItemNameSeashell:
    db m"Got a {SEASHELL}", $ff
ItemNameGel:
    db m"Got a Zol Attack", $ff
ItemNameMessage:
    db m"Got ... nothing?", $ff
ItemNameKey1:
    db m"Got a {KEY1}", $ff
ItemNameKey2:
    db m"Got a {KEY2}", $ff
ItemNameKey3:
    db m"Got a {KEY3}", $ff
ItemNameKey4:
    db m"Got a {KEY4}", $ff
ItemNameKey5:
    db m"Got a {KEY5}", $ff
ItemNameKey6:
    db m"Got a {KEY6}", $ff
ItemNameKey7:
    db m"Got a {KEY7}", $ff
ItemNameKey8:
    db m"Got a {KEY8}", $ff
ItemNameKey9:
    db m"Got a {KEY9}", $ff
ItemNameMap1:
    db m"Got the {MAP1}", $ff
ItemNameMap2:
    db m"Got the {MAP2}", $ff
ItemNameMap3:
    db m"Got the {MAP3}", $ff
ItemNameMap4:
    db m"Got the {MAP4}", $ff
ItemNameMap5:
    db m"Got the {MAP5}", $ff
ItemNameMap6:
    db m"Got the {MAP6}", $ff
ItemNameMap7:
    db m"Got the {MAP7}", $ff
ItemNameMap8:
    db m"Got the {MAP8}", $ff
ItemNameMap9:
    db m"Got the {MAP9}", $ff
ItemNameCompass1:
    db m"Got the {COMPASS1}", $ff
ItemNameCompass2:
    db m"Got the {COMPASS2}", $ff
ItemNameCompass3:
    db m"Got the {COMPASS3}", $ff
ItemNameCompass4:
    db m"Got the {COMPASS4}", $ff
ItemNameCompass5:
    db m"Got the {COMPASS5}", $ff
ItemNameCompass6:
    db m"Got the {COMPASS6}", $ff
ItemNameCompass7:
    db m"Got the {COMPASS7}", $ff
ItemNameCompass8:
    db m"Got the {COMPASS8}", $ff
ItemNameCompass9:
    db m"Got the {COMPASS9}", $ff
ItemNameStoneBeak1:
    db m"Got the {STONE_BEAK1}", $ff
ItemNameStoneBeak2:
    db m"Got the {STONE_BEAK2}", $ff
ItemNameStoneBeak3:
    db m"Got the {STONE_BEAK3}", $ff
ItemNameStoneBeak4:
    db m"Got the {STONE_BEAK4}", $ff
ItemNameStoneBeak5:
    db m"Got the {STONE_BEAK5}", $ff
ItemNameStoneBeak6:
    db m"Got the {STONE_BEAK6}", $ff
ItemNameStoneBeak7:
    db m"Got the {STONE_BEAK7}", $ff
ItemNameStoneBeak8:
    db m"Got the {STONE_BEAK8}", $ff
ItemNameStoneBeak9:
    db m"Got the {STONE_BEAK9}", $ff
ItemNameNightmareKey1:
    db m"Got the {NIGHTMARE_KEY1}", $ff
ItemNameNightmareKey2:
    db m"Got the {NIGHTMARE_KEY2}", $ff
ItemNameNightmareKey3:
    db m"Got the {NIGHTMARE_KEY3}", $ff
ItemNameNightmareKey4:
    db m"Got the {NIGHTMARE_KEY4}", $ff
ItemNameNightmareKey5:
    db m"Got the {NIGHTMARE_KEY5}", $ff
ItemNameNightmareKey6:
    db m"Got the {NIGHTMARE_KEY6}", $ff
ItemNameNightmareKey7:
    db m"Got the {NIGHTMARE_KEY7}", $ff
ItemNameNightmareKey8:
    db m"Got the {NIGHTMARE_KEY8}", $ff
ItemNameNightmareKey9:
    db m"Got the {NIGHTMARE_KEY9}", $ff
ItemNameToadstool:
    db m"Got the {TOADSTOOL}", $ff
ItemNameGuardianAcorn:
    db m"Got a Guardian Acorn", $ff

ItemNameHeartPiece:
    db m"Got the {HEART_PIECE}", $ff
ItemNameBowwow:
    db m"Got the {BOWWOW}", $ff
ItemName10Arrows:
    db m"Got {ARROWS_10}", $ff
ItemNameSingleArrow:
    db m"Got the {SINGLE_ARROW}", $ff
ItemNamePowderUpgrade:
    db m"Got the {MAX_POWDER_UPGRADE}", $ff
ItemNameBombUpgrade:
    db m"Got the {MAX_BOMBS_UPGRADE}", $ff
ItemNameArrowUpgrade:
    db m"Got the {MAX_ARROWS_UPGRADE}", $ff
ItemNameRedTunic:
    db m"Got the {RED_TUNIC}", $ff
ItemNameBlueTunic:
    db m"Got the {BLUE_TUNIC}", $ff
ItemNameHeartContainer:
    db m"Got a {HEART_CONTAINER}", $ff
ItemNameBadHeartContainer:
    db m"Got the {BAD_HEART_CONTAINER}", $ff
ItemNameSong1:
    db m"Got the {SONG1}", $ff
ItemNameSong2:
    db m"Got {SONG2}", $ff
ItemNameSong3:
    db m"Got {SONG3}", $ff

ItemInstrument1:
    db m"You've got the {INSTRUMENT1}", $ff
ItemInstrument2:
    db m"You've got the {INSTRUMENT2}", $ff
ItemInstrument3:
    db m"You've got the {INSTRUMENT3}", $ff
ItemInstrument4:
    db m"You've got the {INSTRUMENT4}", $ff
ItemInstrument5:
    db m"You've got the {INSTRUMENT5}", $ff
ItemInstrument6:
    db m"You've got the {INSTRUMENT6}", $ff
ItemInstrument7:
    db m"You've got the {INSTRUMENT7}", $ff
ItemInstrument8:
    db m"You've got the {INSTRUMENT8}", $ff

ItemRooster:
    db m"You've got the {ROOSTER}", $ff

ItemTradeQuest1:
    db m"You've got the Yoshi Doll", $ff
ItemTradeQuest2:
    db m"You've got the Ribbon", $ff
ItemTradeQuest3:
    db m"You've got the Dog Food", $ff
ItemTradeQuest4:
    db m"You've got the Bananas", $ff
ItemTradeQuest5:
    db m"You've got the Stick", $ff
ItemTradeQuest6:
    db m"You've got the Honeycomb", $ff
ItemTradeQuest7:
    db m"You've got the Pineapple", $ff
ItemTradeQuest8:
    db m"You've got the Hibiscus", $ff
ItemTradeQuest9:
    db m"You've got the Letter", $ff
ItemTradeQuest10:
    db m"You've got the Broom", $ff
ItemTradeQuest11:
    db m"You've got the Fishing Hook", $ff
ItemTradeQuest12:
    db m"You've got the Necklace", $ff
ItemTradeQuest13:
    db m"You've got the Scale", $ff
ItemTradeQuest14:
    db m"You've got the Magnifying Lens", $ff
 
ItemPieceOfPower:
    db m"You've got a Piece of Power", $ff

MultiNamePointers: