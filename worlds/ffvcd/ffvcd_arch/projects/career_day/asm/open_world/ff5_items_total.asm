;
; ff5_items_total.asm
;    メニューに所持アイテム数を表示する revision 1.0
;
; 解説
;
;    FF6 のように、アイテムメニューに所持しているアイテムの数を表示します。
;
; 使用領域
;
;    $C2AC5E-$C2AC8F:   50 bytes
;    $C2C780-$C2C7BC:   61 bytes
;



;--------------------------------
; アイテムの説明を表示する
;--------------------------------
org $C2AC5E
DISPLAY_ITEM_MESSAGE:
    REP #$20
    LDA #$B3A9      ; (アイテムの説明を消去する)
    JSR $C1B8       ; Run Menu Script
    LDA $55         ; カーソル位置
    AND #$00FF
    DEC
    CLC
    ADC $6B         ; スクロール位置
    TAX
    LDA $288A,X     ; アイテムの説明[0]
    AND #$007F
    BEQ DISPLAY_ITEMS_TOTAL

    ASL
    TAX
    LDA FILEPOS_ITEMMES_ADDR,X
    STA $2CEB
    JSR $DA16       ; メッセージを取得する (src: $D10000 + ($2CEB))
;--------------------------------
; アイテムの所持数を表示する
;--------------------------------
DISPLAY_ITEMS_TOTAL:
    LDX #$5276      ; (dest: $7E5276)
    LDY #$2D1B      ; アイテムの所持数 (装備確認では「アイテムの番号」で上書
                    ; きされる)
    LDA #$7E31      ; バンク: $7E, サイズ: 1, 桁: 3
    JMP $E4ED       ; 数値から文字列を取得する (X: dest, Y: src, AH: bank,
                    ; AL: (bit0-3: size | bit4-6: 桁数 | bit7: ゼロパディン
                    ; グON))

;--------------------------------
; アイテムの説明を設定する
;--------------------------------
org $C2C780
SET_ITEM_MESSAGES:
    PHP
    LDX $8E         ; $8E = 0
    STX $2D1B       ; アイテムの所持数 (装備確認では「アイテムの番号」で上書
                    ; きされる)
    SEP #$20

.begin
    LDA $7A00,X     ; アイテムの番号[0]
    BNE .not_empty

    STZ $7B00,X     ; アイテムの個数[0]
    STZ $288A,X     ; アイテムの説明[0]
    BRA .next_item

.not_empty
    INC $2D1B       ; アイテムの所持数 (装備確認では「アイテムの番号」で上書
                    ; きされる)
    PHX
    PHA
    JSR $D9AB       ; アイテムデータを読み込む (Aレジスタ: アイテムの番号)
                    ; (-> $019B～$01A6)
    PLA
    CMP #$E0        ; #$E0 = "ポーション"
    NOP
    NOP
    BCC .is_equip

.is_item
    LDA $9E         ; アイテムデータ[3]: メッセージの番号
    AND #$3F
    BRA .set_item_msg

.is_equip
    LDA $9F         ; 武器/防具データ[4]: メッセージの番号
    AND #$3F
    CLC
    ADC #$00

.set_item_msg
    PLX
    STA $288A,X     ; アイテムの説明[0]

.next_item
    INX
    CPX #$0100
    BNE .begin

    PLP
    RTS
