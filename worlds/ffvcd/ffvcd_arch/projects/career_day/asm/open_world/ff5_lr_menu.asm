;
; ff5_lr_menu.asm
;    LR メニューの追加 revision 1.0
;
; 解説
;
;    SFC 版ファイナルファンタジー V に LR メニューの機能を追加します。また、
;    メニュー処理に関する不具合を修正します。対応している機能および修正され
;    た不具合は以下のとおりです:
;
;    * 追加機能:
;      - ジョブ・アビリティ・装備・ステータス・魔法メニューでキャラクタの切
;        り替えが可能
;      - 魔法メニューで魔法の種類の切り替え可能
;      - アビリティメニューでアビリティ欄のスクロールが可能
;      - アイテム・装備・店メニューでアイテム欄のスクロールが可能
;      - 主人公の名前設定でひらがな/カタカナの切り替えが可能
;      - 戦闘のアイテムコマンドでアイテム欄のスクロールが可能
;      - 戦闘の魔法コマンドで魔法欄のスクロールが可能
;      - LR 入力のリピートが可能
;
;    * 機能改善:
;      - リピートの処理を以下のように変更:
;        - リピート中にキーを同時押しした場合は最後の入力をリピートする
;        - リピート中にキーを放した場合は押されている入力をリピートする
;        - FF6 のように A 入力時の遅延時間の例外設定が可能 (デフォルト: 32)
;      - 装備メニューのカーソルの初期位置を、ジョブ/アビリティ変更後に最強装
;        備しても「そうび」を選択するように変更; FF5A と同じ
;      - 店の売却画面でアイテムメニューの選択したアイテムの位置をリセットし
;        ない; FF5A と同じ
;      - 戦闘の歌コマンドでスクロールバーを表示しないようにした
;
;    * バグ/不具合の修正:
;      - ステータス画面でキャラクタを切り替えても暗闇状態のパーツが残る不具
;        合を修正
;      - 青魔法の終了時に画面がちらつく不具合を修正
;      - 青魔法のカーソル位置が正しく設定されない不具合を修正
;      - 短縮コマンドの設定で 1 番目のコマンドを最初に選択するように修正
;      - 短縮コマンドの設定で同じコマンドを選択しても非選択にならない不具合
;        を修正
;      - 短縮コマンドの設定でキャラクタが状態異常にかかっているとジョブの名
;        前が表示されない不具合を修正
;      - 短縮コマンドの設定でカーソルが表示されたままになる不具合を修正
;      - 短縮コマンドの設定でキャラクタの選択が上下ループするように変更
;      - 短縮コマンドの設定でキャラクタが戦闘不能になっているとすっぴんのパ
;        レットが使用される不具合を修正
;      - カスタムの設定を B ボタンで終了できるように変更
;      - 道具屋でアイテムを購入できない場合にキャラクタが表示される不具合を
;        修正
;      - テント/コテージの使用時にカーソル位置が記憶されない不具合を修正
;      - 召喚獣アイテムの使用後にアイテムの説明が更新されない不具合を修正
;
;    注意: このパッチファイルは 効果タイプ 71h: レベルダウン [$C27964-$C2
;    7AD8] および レベルダウンの対象テーブル [$D0FFA0-$D0FFDF] の領域を削除
;    して使用します。このパッチファイルを適用する場合は、この領域を使用しな
;    いでください。
;
; NOTES
;
;    アビリティのキャラクタ切り替えの動作については以下で変更できます:
;
;      $C279BE: F0 00 - FF5 (SFC and PSX) 互換
;      $C279BE: 80 05 - FF5A (GBA) 互換
;      $C279BE: F0 05 - ff5_ability_menu.ips 互換 (デフォルト)
;
;    キー入力の遅延時間は以下で変更できます:
;
;      $C2FF3D: 20    - A ボタンの遅延時間
;      $C2FF8F: 16    - 遅延時間 (通常)
;      $C2FF5B: 10    - 遅延時間 (戦闘)
;
; 使用領域: 修正
;
;    $C0E63A-$C0E651:   24 bytes
;    $C0E652-$C0E6AE:   93 bytes
;    $C0E6AF-$C0E6E7:   57 bytes
;    $C0E6E8-$C0E720:   57 bytes
;    $C0E7C6-$C0E7D9:   20 bytes
;    $C0E9E2-$C0E9F1:   16 bytes
;    $C0E9F3-$C0EA01:   16 bytes
;    $C0EA08-$C0EA09:    2 bytes
;    $C14AF5-$C14AF8:    4 bytes
;    $C14BF8-$C14BBB:   45 bytes
;    $C15574-$C155AB:   56 bytes
;    $C155D0-$C15704:  309 bytes
;    $C157B1-$C157E6:   54 bytes
;    $C15BA3-$C15CC9:  183 bytes
;    $C15C88-$C15CD1:  314 bytes
;    $C15E04-$C15E1E:   27 bytes
;    $C2A06B-$C2A0C1:   87 bytes
;    $C2A1F0-$C2A21D:   46 bytes
;    $C2A2E9-$C2A339:   81 bytes
;    $C2A33A-$C2A357:   30 bytes
;    $C2A40F-$C2A42A:   28 bytes
;    $C2A6FC-$C2A77F:  132 bytes
;    $C2A96F-$C2A9D8:  106 bytes
;    $C2AA12-$C2AA34:   35 bytes
;    $C2AC1E-$C2AC20:    3 bytes
;    $C2AC90-$C2ACA7:   24 bytes
;    $C2ACC3-$C2ACCF:   13 bytes
;    $C2ACD0-$C2ACF8:   41 bytes
;    $C2ACF9-$C2ACFE:    6 bytes
;    $C2ACFF-$C2AD3D:   63 bytes
;    $C2ADB0-$C2ADCB:   28 bytes
;    $C2ADCC-$C2ADDE:   19 bytes
;    $C2AEE6-$C2AF06:   33 bytes
;    $C2B0A0-$C2B0AF:   16 bytes
;    $C2B7FC-$C2B80C:   21 bytes
;    $C2B8D0-$C2B8FC:   45 bytes
;    $C2B97E-$C2B992:   15 bytes
;    $C2BB66-$C2BB8F:   42 bytes
;    $C2BB90-$C2BBAB:   28 bytes
;    $C2BBFA-$C2BC1C:   35 bytes
;    $C2BC2D-$C2BC47:   27 bytes
;    $C2BC48-$C2BC56:   15 bytes
;    $C2C014-$C2C016:    3 bytes
;    $C2C0BD-$C2C0BF:    3 bytes
;    $C2C110-$C2C111:    2 bytes
;    $C2C34A-$C2C36E:   37 bytes
;    $C2C7C6-$C2C7C7:    2 bytes
;    $C2C803-$C2C880:  126 bytes
;    $C2C921-$C2C922:    2 bytes
;    $C2CA37-$C2CAA4:  110 bytes
;    $C2CAA5-$C2CAC7:   35 bytes
;    $C2CCCB-$C2CD07:   61 bytes
;    $C2CD57-$C2CD98:   66 bytes
;    $C2D388-$C2D3D0:   73 bytes
;    $C2D958-$C2D9AA:   83 bytes
;    $C2F4CB-$C2F4CD:    3 bytes
;    $C2FED0-$C2FF4C:  125 bytes
;    $C2FF7D-$C2FFC1:   69 bytes
;    $C3AB36:            1 byte
;    $C3AB2F:            1 byte
;
; 使用領域: 追加処理で使用
;
;    $C0E628-$C0E630:    9 bytes
;    $C14AF9-$C14B05:   13 bytes
;    $C14B06-$C14B1A:   21 bytes
;    $C155B9-$C155CF:   23 bytes
;    $C157E7-$C157F6:   16 bytes
;    $C157F7-$C15805:   15 bytes
;    $C15DC2-$C15DD3:   18 bytes
;    $C15E1F-$C15E35:   23 bytes
;    $C2A0D9-$C2A0F5:   29 bytes
;    $C2A21E-$C2A22F:   18 bytes
;    $C2B0B0-$C2B0D4:   37 bytes
;    $C2BC1D-$C2BC26:   10 bytes
;    $C2C881-$C2C89F:   31 bytes
;    $C2CD99-$C2CDAE:   22 bytes
;    $C2CDBA-$C2CDBF:    6 bytes
;    $C2CDC0-$C2CDC5:    6 bytes
;    $C2A42B-$C2A440:   22 bytes
;
; 使用領域: LR 入力で使用
;
;    $C15705-$C15729:   37 bytes
;    $C1572A-$C1574F:   38 bytes
;    $C15C5A-$C15C87:   46 bytes
;    $C15EE0-$C15F10:   49 bytes
;    $C2A230-$C2A23A:   11 bytes
;    $C2ACA8-$C2ACC2:   27 bytes
;    $C27964-$C27ABD:  346 bytes
;    $D0FFA0-$D0FFDD:   62 bytes
;
; 空き領域
;
;    $C0E631-$C0E639:    9 bytes (reserved)
;    $C0E7DA-$C0E7E6:   13 bytes
;    $C14B1B-$C14B21:    7 bytes
;    $C155AC-$C155B8:   13 bytes
;    $C15E36-$C15E3A:    5 bytes
;    $C2A0C2-$C2A0D8:   23 bytes
;    $C2AF07-$C2AF1A:   20 bytes (used by ff5_ngplus.ips)
;    $C2B80D-$C2B810:    4 bytes
;    $C2BC57-$C2BC5D:    7 bytes
;    $C2CDAF-$C2CDB9:   11 bytes
;    $C2D3D1-$C2D3DA:   10 bytes
;    $C2F4CE-$C2F4D3:    6 bytes
;    $C2FF4D-$C2FF55:    9 bytes
;
; 空き領域: LR 入力で使用
;
;    $C15F11-$C15F16:    6 bytes
;    $C27ABE-$C27AD8:   27 bytes (used by ff5_ngplus.ips)
;    $D0FFDE-$D0FFDF:    2 bytes
;
; 仕様
;
;    * キャラクタ切り替え処理はコンフィグの設定が「戻す」であればカーソルを
;      初期位置に戻します。
;    * リストのスクロール処理はカーソルの位置を常に変更しません。
;
; バグ
;
;    * 魔法メニューの種類選択画面でキャラクタの名前がすべて表示されません
;      (fixed in PSX version)。
;    * テレポの使用時にカーソル位置が記憶されません (not fixed in both PSX
;      and GBA version)。
;
; 技術資料
;
;    Table of $7600: メニュー動作制御テーブル
;    ----------------------------------------
;    $7600: メニュー番号 | スクロールタイプ (>= 0x80):
;                        |   80: アビリティ/変更
;                        |   82: ジョブ
;                        |   83: 装備/アイテム選択
;                        |   85: 店/個数選択
;                        |   86: アイテム/アイテム選択
;                        |   87: $2B66/$2B67 を使用する
;                        |   89: コンフィグ
;    $7601: カーソル位置 | スクロール引数
;    $7602: カーソルの表示位置(横)
;    $7603: カーソルの表示位置(縦)
;    $7604: Up:    カーソルインデックス
;    $7605: Down:  カーソルインデックス
;    $7606: Left:  カーソルインデックス
;    $7607: Right: カーソルインデックス
;
;    List of $0143: メニューコマンド番号
;    -----------------------------------
;    01: メインメニュー
;    02: アビリティ
;    03: ジョブ
;    04: 装備変更
;    05: ステータス
;    06: 店
;    07: アイテム
;    08: 魔法
;    09: コンフィグ
;    0A: お宝
;    0B: セーブ
;    0C: ロード
;    0D: 主人公の名前設定
;
;    List of $0154: メニュー番号
;    ---------------------------
;    01: メイン
;    02: メイン/隊列変更
;    03: メイン/キャラクタ選択
;    04: アビリティ
;    05: アビリティ/変更
;    06: ジョブ
;    07: 装備/装備選択
;    08: 装備
;    09: 装備/アイテム選択
;    0A: ステータス
;    0B: 店
;    0C: 店/購入
;    0D: 店/購入/個数選択
;    0E: 魔法屋/購入
;    0F: アイテム
;    10: アイテム/アイテム選択
;    11: (unused)
;    12: 魔法
;    13: 魔法/白魔法,黒魔法,時空,召喚,魔法剣
;    14: 魔法/青魔法
;    15: 魔法/歌
;    16: 店/売却
;    17: セーブ
;    18: 名前設定/モード
;    19: 名前設定/文字選択
;    1A: 店/売却/個数選択
;    1B: お宝
;    1C: セーブ/確認
;    1D: 魔法/使用/対象選択
;    1E: アイテム/使用/対象選択
;    1F: コンフィグ/短縮
;    20: コンフィグ
;    21: コンフィグ/マルチ
;    22: コンフィグ/カスタム
;    23: コンフィグ/短縮/選択
;    24: アイテム/アイテム選択/装備確認
;

; /* Start of definition */

;--------------------------------
; LR 入力で使用するアドレス
;--------------------------------
; $C27964:     LR 入力のプログラム
; $D0FFA0:    LR 入力で使用するアドレステーブル
; $C15EE0:   [戦闘] アイテムの LR 入力のプログラム
; $C15C5A:  [戦闘] アイテムのスクロール処理
; $C15705:  [戦闘] 魔法の LR 入力のプログラム
; $C15705+$25: [戦闘] 魔法のスクロール処理
;--------------------------------
; /* $C27964 is must be in $C2 bank */
!$C27964 = $C27964
!$D0FFA0 = $D0FFA0
; /* LR_LOC_BTL_* are must be in $C1 bank */
!$C15EE0 = $C15EE0
!$C15C5A = $C15C5A
!$C15705 = $C15705
!$C15705+$25 = $C15705+$25

;--------------------------------
; キー入力処理のアドレス
;--------------------------------
; $C2A358: キー入力タイプ No.007(07): デモメニューのウェイト
; $C2A36A:         キー入力タイプ No.001(01): A 入力
; $C2A378:         キー入力タイプ No.002(02): B 入力
; INPUT_DEMO_EXIT: キー入力タイプ No.008(08): デモメニューを終了する
; INPUT_UP:        キー入力タイプ No.003(03): UP
; INPUT_DOWN:      キー入力タイプ No.004(04): Down
; INPUT_LEFT:      キー入力タイプ No.005(05): Left
; INPUT_RIGHT:     キー入力タイプ No.006(06): Right
; INPUT_MOVE:      キー入力によって移動する (Aレジスタ: インデックス)
; INPUT_WAIT:      キー入力タイプ No.000(00): 入力待ち
; INPUT_LR:        キー入力タイプ No.009(09): LR 入力
;-------------------------------
$C2A358 equ $C2A358
$C2A36A         equ $C2A36A
$C2A378         equ $C2A378
INPUT_DEMO_EXIT equ $C2A441
INPUT_UP        equ $C2A45E
INPUT_DOWN      equ $C2A466
INPUT_LEFT      equ $C2A46E
INPUT_RIGHT     equ $C2A476
INPUT_MOVE      equ $C2A47C
INPUT_WAIT      equ $C2A4F0
INPUT_LR        equ $C2ACA8

;--------------------------------
; サウンドのアドレス
;--------------------------------
; SOUND_SELECT:     サウンドの設定: 選択音
; SOUND_OK:         サウンドの設定: 決定音
; SOUND_CANCEL:     サウンドの設定: 取消音
; SOUND_BEEP:       サウンドの設定: ビープ音
; SOUND_SAVE:       サウンドの設定: セーブ音
; SOUND_GET:        サウンドの設定: 購入/召喚獣習得
; LR_SOUND:         LR 入力時のサウンド
; BTL_SOUND_SELECT: [戦闘] サウンドの設定: 選択音
; BTL_SOUND_OK:     [戦闘] サウンドの設定: 決定音
; BTL_SOUND_CANCEL: [戦闘] サウンドの設定: 取消音
; BTL_SOUND_BEEP:   [戦闘] サウンドの設定: ビープ音
; BTL_LR_SOUND:     [戦闘] LR 入力時のサウンド
;--------------------------------
SOUND_SELECT     equ $C2E0A8
SOUND_OK         equ $C2E0B0
SOUND_CANCEL     equ $C2E0B8
SOUND_BEEP       equ $C2E0C0
SOUND_SAVE       equ $C2E0C8
SOUND_GET        equ $C2E0D9
LR_SOUND         equ SOUND_SELECT
BTL_SOUND_SELECT equ $C1FBAD
BTL_SOUND_OK     equ $C1FBB8
BTL_SOUND_CANCEL equ $C1FBC3
BTL_SOUND_BEEP   equ $C1FBCE
BTL_LR_SOUND     equ BTL_SOUND_SELECT

;--------------------------------
; メニュー処理ルーチンアドレス
;--------------------------------
org $C0E60E
FILEPOS_MENU_ADDR:
    dw $CFDC                ; 01: メインメニュー
    dw $CEEC                ; 02: アビリティ
    dw $CCCB                ; 03: ジョブ
    dw $CA37                ; 04: 装備変更
    dw $C8A0                ; 05: ステータス
    dw $C803                ; 06: 店
    dw $C6F7                ; 07: アイテム
    dw $C5C8                ; 08: 魔法
    dw $C34A                ; 09: コンフィグ
    dw $C36F                ; 0A: お宝
    dw $C5B9                ; 0B: セーブ
    dw $C56B                ; 0C: ロード
    dw $C442                ; 0D: 主人公の名前設定

;--------------------------------
; キー入力処理ルーチンアドレス [20 bytes]
;--------------------------------
org $C0E7C6                 ; moved from $C0E628
FILEPOS_$C2A36ADDR:
    dw INPUT_WAIT           ; 00: (none)
    dw $C2A36A              ; 01: A
    dw $C2A378              ; 02: B
    dw INPUT_UP             ; 03: Up
    dw INPUT_DOWN           ; 04: Down
    dw INPUT_LEFT           ; 05: Left
    dw INPUT_RIGHT          ; 06: Right
    dw $C2A358      ; 07: デモメニューで使用する
    dw INPUT_DEMO_EXIT      ; 08: デモメニューを終了する
    dw INPUT_LR             ; 09: LR

;--------------------------------
; メニュースクロールの処理
;--------------------------------
org $C0E63A
FILEPOS_MENU_SCROLL_ADDR:
    db $80 : dw $A519       ; 80: アビリティ/変更
    db $82 : dw $A5B5       ; 82: ジョブ
    db $83 : dw $A5E6       ; 83: 装備/アイテム選択
    db $85 : dw $A618       ; 85: 店/個数選択
    db $86 : dw $A6B9       ; 86: アイテム/アイテム選択
    db $87 : dw $A6FC       ; 87: $2B66/$2B67 を使用する (魔法/青魔法,
                            ;     名前設定/文字選択)
    db $89 : dw $A79C       ; 89: コンフィグ
    db $00 : dw $0000       ; (eof)

;--------------------------------
; メニュー切り替え/開始時の処理
;--------------------------------
org $C0E652
FILEPOS_MENU_FOCUS_ADDR:
    db $01 : dw $A7FC                   ; 01: メイン
    db $02 : dw $A826                   ; 02: メイン/隊列変更
    db $03 : dw $A8FA                   ; 03: メイン/キャラクタ選択
    db $04 : dw $A925                   ; 04: アビリティ
    db $05 : dw $A958                   ; 05: アビリティ/変更
    db $06 : dw $A96C                   ; 06: ジョブ
    db $08 : dw $A9FD                   ; 08: 装備
    db $09 : dw $AA35                   ; 09: 装備/アイテム選択
    db $0B : dw $AABB                   ; 0B: 店
    db $0C : dw $AAE9                   ; 0C: 店/購入
    db $0D : dw $AB91                   ; 0D: 店/購入/個数選択
    db $0E : dw $ABC1                   ; 0E: 魔法屋/購入
    db $0F : dw $ABDF                   ; 0F: アイテム
    db $10 : dw $AC01                   ; 10: アイテム/アイテム選択
    db $12 : dw $ACC3                   ; 12: 魔法
    db $13 : dw MENU_FOCUS_MAGIC_LIST   ; 13: 魔法/白魔法,黒魔法,時空,召喚,
                                        ;     魔法剣
    db $14 : dw $ADB0                   ; 14: 魔法/青魔法
    db $15 : dw MENU_FOCUS_SONG_LIST    ; 15: 魔法/歌
    db $16 : dw $ADDF                   ; 16: 店/売却
    db $19 : dw $AE47                   ; 19: 名前設定/文字選択
    db $1A : dw $AE5C                   ; 1A: 店/売却/アイテム選択
    db $1C : dw $AE6F                   ; 1C: セーブ/確認
    db $1D : dw $AF1B                   ; 1D: 魔法/使用/対象選択
    db $1E : dw $B04F                   ; 1E: アイテム/使用/対象選択
    db $1F : dw $B079                   ; 1F: コンフィグ/短縮
    db $20 : dw $B0D6                   ; 20: コンフィグ
    db $21 : dw $B106                   ; 21: コンフィグ/マルチ
    db $22 : dw $B19A                   ; 22: コンフィグ/カスタム
    db $23 : dw $B1CA                   ; 23: コンフィグ/短縮/選択
    db $24 : dw $B1EC                   ; 24: アイテム/アイテム選択/装備確認
    db $00 : dw $0000                   ; (eof)

;--------------------------------
; メニュー切り替え/終了時の処理
;--------------------------------
org $C0E6AF
FILEPOS_MENU_UNFOCUS_ADDR:
    db $01 : dw $A81D                   ; 01: メイン
    db $02 : dw $A8D3                   ; 02: メイン/隊列変更
    db $03 : dw $A91C                   ; 03: メイン/キャラクタ選択
    db $04 : dw $A948                   ; 04: アビリティ
    db $08 : dw $AA12                   ; 08: 装備
    db $09 : dw $AA4E                   ; 09: 装備/アイテム選択
    db $0C : dw $AB19                   ; 0C: 店/購入
    db $0D : dw $ABB2                   ; 0D: 店/購入/個数選択
    db $0E : dw $ABD1                   ; 0E: 魔法屋/購入
    db $12 : dw MENU_UNFOCUS_MAGIC      ; 12: 魔法
    db $13 : dw $AD3E                   ; 13: 魔法/白魔法,黒魔法,時空,召喚,
                                        ;     魔法剣
    db $14 : dw $ADCC                   ; 14: 魔法/青魔法
    db $15 : dw $AD3E                   ; 15: 魔法/歌
    db $16 : dw $AE11                   ; 16: 店/売却
    db $1A : dw $AE6B                   ; 1A: 店/売却/個数選択
    db $1D : dw $AF87                   ; 1D: 魔法/使用/対象選択
    db $1E : dw $B063                   ; 1E: アイテム/使用/対象選択
    db $24 : dw $B257                   ; 24: アイテム/アイテム選択/装備確認
    db $00 : dw $0000                   ; (eof)

;--------------------------------
; メニュー移動時の処理
;--------------------------------
org $C0E6E8
FILEPOS_MENU_MOVE_ADDR:
    db $02 : dw $A8C1                   ; 02: メイン/隊列変更
    db $03 : dw $A918                   ; 03: メイン/キャラクタ選択
    db $04 : dw $A935                   ; 04: アビリティ
    db $05 : dw $A965                   ; 05: アビリティ/変更
    db $06 : dw $A96F                   ; 06: ジョブ
    db $09 : dw $AA6E                   ; 09: 装備/アイテム選択
    db $0B : dw $AAD1                   ; 0B: 店(魔法屋)
    db $0C : dw $AB20                   ; 0C: 店/購入
    db $0E : dw $ABDB                   ; 0E: 魔法屋/購入
    db $0F : dw $ABF2                   ; 0F: アイテム
    db $10 : dw $AC1E                   ; 10: アイテム/アイテム選択
    db $13 : dw $AD5B                   ; 13: 魔法/白魔法,黒魔法,時空,召喚,
                                        ;     魔法剣
    db $14 : dw $AD5B                   ; 14: 魔法/青魔法
; [$AC90: スタートで高速スクロール] を削除
;   db $16 : dw $AC90                   ; 16: 店/売却
    db $17 : dw $AE31                   ; 17: セーブ
    db $19 : dw $AE4B                   ; 19: 名前設定/文字選択
    db $1D : dw $AFB2                   ; 1D: 魔法/使用/対象選択
    db $1E : dw $AFB2                   ; 1E: アイテム/使用/対象選択
    db $21 : dw $B16E                   ; 21: コンフィグ/マルチ
    db $00 : dw $0000                   ; (eof)

;--------------------------------
; 決定/取消入力の処理ルーチンアドレス
;--------------------------------
org $C0E724
FILEPOS_MENU_INPUT_DETERMINE_ADDR:
    dw $B25B, $B25B         ; 00: (none)
    dw $B25E, $B2FB         ; 01: メイン
    dw $B302, $B40C         ; 02: メイン/隊列変更
    dw $B429, $B480         ; 03: メイン/キャラクタ選択
    dw $B48F, $B4A8         ; 04: アビリティ
    dw $B4D7, $B511         ; 05: アビリティ/変更
    dw $B521, $B5EA         ; 06: ジョブ
    dw $B6B9, $B74B         ; 07: 装備/装備選択
    dw $B752, $B796         ; 08: 装備
    dw $B7AD, $B7FC         ; 09: 装備/アイテム選択
    dw $B811, $B845         ; 0A: ステータス
    dw $B84D, $B879         ; 0B: 店
    dw $B8AE, $B91D         ; 0C: 店/購入
    dw $B955, $B993         ; 0D: 店/購入/個数選択
    dw $B998, $BA05         ; 0E: 魔法屋/購入
    dw $BA0A, $BA63         ; 0F: アイテム
    dw $BA7D, $BBFA         ; 10: アイテム/アイテム選択
    dw $BC27, $BC2A         ; 11: (unused)
    dw $BC2D, $BC48         ; 12: 魔法
    dw $BC5E, $BCD9         ; 13: 魔法/白魔法,黒魔法,時空,召喚,魔法剣
    dw $BCD9, $BCD9         ; 14: 魔法/青魔法
    dw $BCD9, $BCD9         ; 15: 魔法/歌
    dw $BCE0, $BD3D         ; 16: 店/売却
    dw $BD47, $BDB5         ; 17: セーブ
    dw $BDC6, $BDF3         ; 18: 名前設定/モード
    dw $BDF6, $BE2E         ; 19: 名前設定/文字選択
    dw $BE64, $BEC8         ; 1A: 店/売却/個数選択
    dw $BECD, $BEF4         ; 1B: お宝
    dw $BF2E, $BF89         ; 1C: セーブ/確認
    dw $BF9D, $BFCD         ; 1D: 魔法/使用/対象選択
    dw $BFD4, $BFF4         ; 1E: アイテム/使用/対象選択
    dw $C003, $C041         ; 1F: コンフィグ/短縮
    dw $C046, $C05E         ; 20: コンフィグ
    dw $C069, $C06C         ; 21: コンフィグ/マルチ
    dw $C071, $C0BD         ; 22: コンフィグ/カスタム
    dw $C0F7, $C146         ; 23: コンフィグ/短縮/選択
    dw $C162, $C162         ; 24: アイテム/アイテム選択/装備確認

;--------------------------------
; キー入力のコンフィグ設定テーブル
;--------------------------------
org $C0E7B8
FILEPOS_INPUT_CONFIG:
    dw $0080                ; 00: A
    dw $8000                ; 01: B
    dw $0040                ; 02: X
    dw $4000                ; 03: Y
    dw $0020                ; 04: L
    dw $0010                ; 05: R
    dw $2000                ; 06: Select

;--------------------------------
; メニューで使用できるキー入力処理テーブル [24 bytes]
;--------------------------------
org $C2AC90                 ; moved from $C0E7D2
FILEPOS_INPUT_INDEX:
    dw $0080 : db $01       ; 01: A
    dw $8000 : db $02       ; 02: B
    dw $0800 : db $03       ; 03: Up
    dw $0400 : db $04       ; 04: Down
    dw $0200 : db $05       ; 05: Left
    dw $0100 : db $06       ; 06: Right
    dw $0030 : db $09       ; 09: LR
    dw $0000 : db $00       ; 00: (none)

;--------------------------------
; コンフィグ/戻す: カーソルインデックスの初期値
;--------------------------------
org $C0E9E2
FILEPOS_CURSOR_RESET:
    db $00          ; 00: (none)
    db $02          ; 01: メイン
    db $08          ; 02: メイン/隊列変更
    db $0C          ; 03: メイン/キャラクタ選択
    db $00          ; 04: アビリティ
    db $04          ; 05: アビリティ/変更
    db $00          ; 06: ジョブ
    db $00          ; 07: 装備/装備選択
    db $05          ; 08: 装備
    db $00          ; 09: 装備/アイテム選択
    db $00          ; 0A: ステータス
    db $00          ; 0B: 店
    db $00          ; 0C: 店/購入
    db $00          ; 0D: 店/購入/個数選択
    db $00          ; 0E: 魔法屋/購入
    db $00          ; 0F: アイテム
    db $04          ; 10: アイテム/アイテム選択

;--------------------------------
; コンフィグ/記憶: 記憶したカーソルインデックスを格納するアドレス
;--------------------------------
org $C0E9F3
FILEPOS_CURSOR_REMEMBER:
    db $00          ; 00: (none)
    db $59          ; 01: メイン
    db $5A          ; 02: メイン/隊列変更
    db $5A          ; 03: メイン/キャラクタ選択
    db $00          ; 04: アビリティ
    db $00          ; 05: アビリティ/変更
    db $5F          ; 06: ジョブ
    db $5E          ; 07: 装備/装備選択
    db $5E          ; 08: 装備
    db $00          ; 09: 装備/アイテム選択
    db $00          ; 0A: ステータス
    db $00          ; 0B: 店
    db $00          ; 0C: 店/購入
    db $00          ; 0D: 店/購入/個数選択
    db $00          ; 0E: 魔法屋/購入
    db $00          ; 0F: アイテム
    db $00          ; 10: アイテム/アイテム選択

;--------------------------------
; デフォルトのカーソルインデックスの設定 [18 bytes] /* added */
;--------------------------------
org $C2A21E
FILEPOS_CURSOR_DEFAULT:
    db $00          ; $59: 最後に選択したメインメニューの位置
    db $08          ; $5A: 最後に選択したキャラクタの位置
    db $00          ; $5B: 最後に選択したアイテムの位置
    db $00          ; $5C: 最後に選択したアイテムのスクロール位置
    db $00          ; $5D: 最後に魔法を選択したキャラクタの番号
    db $05          ; $5E: 最後に選択した装備の位置
    db $00          ; $5F: 最後に選択したジョブの位置
    db $02          ; $60: 選択したアビリティコマンドの位置
    db $00          ; $61: (unused)
    db $00          ; $62: 最後に選択したセーブデータの位置
    db $00          ; $63: 選択した魔法の種類(1番目のキャラクタ)
    db $00          ; $64: 選択した魔法の種類(2番目のキャラクタ)
    db $00          ; $65: 選択した魔法の種類(3番目のキャラクタ)
    db $00          ; $66: 選択した魔法の種類(4番目のキャラクタ)
    db $07          ; $67: 選択した魔法の位置(1番目のキャラクタ)
    db $07          ; $68: 選択した魔法の位置(2番目のキャラクタ)
    db $07          ; $69: 選択した魔法の位置(3番目のキャラクタ)
    db $07          ; $6A: 選択した魔法の位置(4番目のキャラクタ)

;--------------------------------
; 拡張 DMA 転送設定 (src: $7EB000-$7EC17F, dest: $3000)
;--------------------------------
org $C0E628
    db $00,$30,$01,$18,$00,$B0,$7E,$80,$11

;--------------------------------
; 拡張 DMA 転送設定 (reserved)
;--------------------------------
org $C0E631
    db $00,$00,$00,$00,$00,$00,$00,$00,$00

;--------------------------------
; [戦闘] メニューコマンド処理ルーチンアドレス
;--------------------------------
org $C1119B
FILEPOS_BTL_$C2A36ADDR:
    dw $119A        ; 00: (none)
    dw $4986        ; 01: 設定
    dw $49C4        ; 02:
    dw $4A86        ; 03: 下スクロール
    dw $4B22        ; 04: 上スクロール
    dw $11E4        ; 05: メニューを開く
    dw $53CE        ; 06: コマンド選択
    dw $5C88        ; 07: アイテム
    dw $5BA3        ; 08: アイテム/武器
    dw $119A        ; 09: (none)
    dw $53CE        ; 0A: コマンド選択再開
    dw $55D0        ; 0B: 魔法
    dw $4759        ; 0C: マジックポイントを表示する
    dw $4735        ; 0D: 魔法からコマンドに戻る
    dw $11D3        ; 0E: 終了
    dw $51A5        ; 0F: コマンド/チェンジ
    dw $51E9        ; 10: コマンド/ぼうぎょ
    dw $11C5        ; 11: 装備の表示を更新する
    dw $4D80        ; 12: 対象選択
    dw $4CEF        ; 13: ルーレット処理
    dw $FD07        ; 14: メニューを変更する

;--------------------------------
; [戦闘] メニューコントロール処理ルーチンアドレス
;--------------------------------
org $C13A96
FILEPOS_BTL_CONTROL_ADDR:
    dw $3A95        ; 00: (none)
    dw $416B        ; 01: キャラクタの名前を表示する
    dw $422B        ; 02: コマンドメニューを更新する
    dw $455B        ; 03:
    dw $43CE        ; 04: 装備の表示を更新する
    dw $4176        ; 05: 操るメニューを表示する
    dw $3A95        ; 06: (none)
    dw $422B        ; 07: コマンドメニューを更新する
    dw $4552        ; 08: アイテムを表示する
    dw $3CD3        ; 09: 魔法剣を表示する
    dw $3CD7        ; 0A: 白魔法を表示する
    dw $3CDC        ; 0B: 黒魔法を表示する
    dw $3CE1        ; 0C: 時空魔法を表示する
    dw $3CE6        ; 0D: 召喚魔法を表示する
    dw $3CEB        ; 0E: 青魔法を表示する
    dw $3CF0        ; 0F: 歌うを表示する
    dw $3CF5        ; 10: 白黒魔を表示する
    dw $3CFA        ; 11: 連続魔を表示する
    dw $414B        ; 12: 魔法のマジックポイントを表示する
    dw $421D        ; 13: チェンジを表示する
    dw $4224        ; 14: ぼうぎょを表示する
    dw $609D        ; 15: 右手/左手の装備を入れ替える
    dw $60CC        ; 16: 武器欄からアイテム欄に移動する
    dw $605C        ; 17: アイテム欄を入れ替える
    dw $60BB        ; 18: アイテム欄から武器欄に移動する
    dw $3CCD        ; 19: アイテム欄の表示を更新する
    dw $3CD0        ; 1A: 装備の表示を更新する
    dw $3CC7        ; 1B: 魔法欄の表示を更新する
    dw $3CCA        ; 1C: 特殊魔法欄の表示を更新する
    dw $382E        ; 1D: パーティの状態を表示する

;--------------------------------
; コマンド処理ルーチンアドレス
;--------------------------------
org $C154F1
FILEPOS_BTL_COMMAND_ADDR:
    dw $4676        ; 00: 汎用メニュー
    dw $46B7        ; 01: 魔法剣
    dw $46BC        ; 02: 白魔法
    dw $46C1        ; 03: 黒魔法
    dw $46C6        ; 04: 時空魔法
    dw $46CB        ; 05: 召喚魔法
    dw $46D0        ; 06: 青魔法
    dw $46DA        ; 07: 白黒魔
    dw $46DF        ; 08: 連続魔
    dw $46D5        ; 09: 歌
    dw $4676        ; 0A: 汎用メニュー
    dw $468C        ; 0B: 選択不可
    dw $47B6        ; 0C: アイテム
    dw $468D        ; 0D: 調合
    dw $469F        ; 0E: 飲む
    dw $46AB        ; 0F: 投げる

; /* End of definition */

; /* Start of core implementation */

;--------------------------------
; PPU RAM を初期化する
;--------------------------------
org $C2B0B0
MENU_INIT_PPU_RAM:
    PHP
    STZ $2121       ; CGRAM Address
    REP #$20
    STZ $2102       ; OAM Address low byte
    STZ $2116       ; VRAM Address low byte
    LDX #$F5B2      ; (DMA: $02, $04, $00, $02, $00, $20, $02)
    JSR $A0F6       ; OAM を設定する
    LDX #$F5B9      ; (DMA: $02, $22, $00, $73, $7E, $00, $02)
    JSR $A0F6       ; CG を設定する
    LDX #$F58B      ; (DMA: $01, $18, $00, $30, $7E, $00, $40)
    JSR $A0F6       ; VRAM を設定する
    LDX #$EFD9      ; (DMA: $01, $18, $00, $B0, $7E, $00, $20), ($2116:
                    ; $00, $30),
    JSR $D9FB       ; VRAM を設定する
    PLP
    RTS

;--------------------------------
; キー入力を取得する
;--------------------------------
; Returns:
;   $00:   Input Press (axlr----)
;   $01:   Input Press (byetUDLR)
;   $02:   Input Hold (axlr----)
;   $03:   Input Hold (byetUDLR)
;   $04:   Joypad Status (axlr----)
;   $05:   Joypad Status (byetUDLR)
;   $0106: Joypad Status (axlr----)
;   $0107: Joypad Status (byetUDLR)
;   $0108: Input Hold (axlr----)
;   $0109: Input Hold (byetUDLR)
;   $010A: Input Press (axlr----)
;   $010B: Input Press (byetUDLR)
;
; Variables:
;   $010C:       キー入力制御 (0: 標準, 80: AB リピート有効)
;   $010D:       キー入力中のキャラクタの番号
;   $010E:       前回のキー入力の結果
;   $010F:       前回のキー入力の結果
;   $0114: pad1  前回のキー入力の結果
;   $0115: pad1  前回のキー入力の結果
;   $0116: pad2  前回のキー入力の結果
;   $0117: pad2  前回のキー入力の結果
;   $0118:       キー入力遅延時間
;   $0119:       キー入力リピートレート
;   $011A: pad1  キー入力遅延時間(現在値)
;   $011B: pad1  0x00
;   $011C: pad2  キー入力遅延時間(現在値)
;   $011D: pad2  0x00
;   $011E: pad1  キー入力リピート対象 /* added */
;   $011F: pad1  キー入力リピート対象 /* added */
;   $0120: pad2  キー入力リピート対象 /* added */
;   $0121: pad2  キー入力リピート対象 /* added */
;   $0122: pad1  前回のリピート処理の結果 /* added */
;   $0123: pad1  前回のリピート処理の結果 /* added */
;   $0124: pad2  前回のリピート処理の結果 /* added */
;   $0125: pad2  前回のリピート処理の結果 /* added */
;   $014D:       キー入力設定 (0: 通常, 0以外: 戦闘)
;--------------------------------
org $C2FE5B
GET_JOYPAD:
    PHP
    REP #$20
    PHA
    PHP
    PHX
    PHY
    PHB
    PHD
    SEP #$20
    REP #$10
    LDA #$00
    PHA
    PLB             ; DBR = $00
    PEA $0100
    PLD             ; D = $0100
    LDA #$01

.joypad_wait
    BIT $4212       ; Auto-Joypad が準備できるまでウェイト
    BNE .joypad_wait

    LDY #$0000
    LDA $4D         ; キー入力設定 (0: 通常, 0以外: 戦闘)
    BEQ .multi_disabled

    LDA $0974       ; コンフィグ (40: カスタム, 80: マルチ)
    AND #$80        ; #$80 = "マルチ"
    BEQ .multi_disabled

    LDA $010D       ; キー入力中のキャラクタの番号
    REP #$20
    AND #$0003
    TAX
    LDA $097C,X     ; コンフィグ (マルチコントローラ設定)
    AND #$00FF
    BEQ .multi_disabled

    INY

.multi_disabled
    REP #$20
    STY $12         ; コントローラ設定 (0: pad1, 1: pad2)
    TYA
    ASL
    TAX
    LDA $4218,X     ; Joypad Registers
    STA $06         ; Joypad Status
    AND #$000F
    BEQ .joypad_true

    STZ $06         ; Joypad Status

.joypad_true
    LDA $14,X       ; 前回のキー入力の結果 ($0114: pad1, $0116: pad2)
    STA $0E         ; 前回のキー入力の結果
    JSR GET_CONFIGURED_JOYPAD
    LDA $12         ; コントローラ設定 (0: pad1, 1: pad2)
    ASL
    TAX
    LDA $0E         ; 前回のキー入力の結果
    STA $14,X       ; 前回のキー入力の結果 ($0114: pad1, $0116: pad2)
    PLD
    LDA $010A       ; Input Press (byetUDLR axlr----)
    STA $00
    LDA $0108       ; Input Hold (byetUDLR axlr----)
    STA $02
    LDA $0106       ; Joypad Status
    STA $04
    PLB
    PLY
    PLX
    PLP
    PLA
    PLP
    RTS

;--------------------------------
; キー入力設定に対応した値を取得 ($06: Joypad Status, $08: Hold, $0A: Press)
;--------------------------------
org $C2FED0
GET_CONFIGURED_JOYPAD:
    LDA $0974       ; コンフィグ (40: カスタム, 80: マルチ)
    AND #$0040      ; #$0040 = "カスタム"
    BNE .custom_init

    LDA $06         ; Joypad Status
    STA $08         ; Input Hold (byetUDLR axlr----)
    BRA .input_setup

.custom_init
    LDA $06         ; Joypad Status
    AND #$1F0F      ; #$1F0F = "Start, Up, Down, Left, Right"
    STA $08         ; Input Hold (byetUDLR axlr----)
    LDX #$0000

.custom_begin
    LDA $06         ; Joypad Status
    AND FILEPOS_INPUT_CONFIG,X
    BEQ .custom_continue

    LDA $26,X       ; コンフィグ (入力値)
    TSB $08         ; Input Hold (byetUDLR axlr----)

.custom_continue
    INX
    INX
    CPX #$000E
    BNE .custom_begin

.input_setup
    LDA $0E         ; 前回のキー入力の結果
    EOR #$FFFF
    AND $08         ; Input Hold (byetUDLR axlr----)
    STA $0A         ; Input Press (byetUDLR axlr----)
    LDA $12         ; コントローラ設定 (0: pad1, 1: pad2)
    ASL
    TAX
    LDA $08         ; Input Hold (byetUDLR axlr----)
    STA $0E         ; 前回のキー入力の結果
    BIT $0B         ; $0C: キー入力制御 (0: 標準, 80: AB リピート有効)
    BMI .enable_ab_repeat

    AND #$7F7F      ; リピート処理する入力: 戦闘中でなければ A, B はリピート
                    ; 不可

.enable_ab_repeat
    AND #$8FB0      ; リピート処理する入力: A, B, Up, Down, Left, Right,
                    ; L, R
    STA $10         ; リピートの対象
    BEQ .repeat_update
                    ; 入力がなければリピートを初期化する

    CMP $22,X       ; 前回のリピート処理の結果
    BNE .repeat_start

    LDA $1A,X       ; キー入力遅延時間(現在値)
    DEC
    BEQ .repeat_set_input

    BPL .repeat_set_delay

.repeat_set_input
    LDA $1E,X       ; キー入力リピート対象
    TSB $0A         ; Input Press (byetUDLR axlr----)
    LDA $19         ; キー入力リピートレート
    BRA .repeat_set_delay

.repeat_start
    EOR $1E,X       ; キー入力リピート対象
    AND $10         ; リピート処理中に別のキーを入力した場合...
    BNE .repeat_update

    LDA $10         ; リピート処理中に現在のキーを放した場合...

.repeat_update
    STA $1E,X       ; キー入力リピート対象
    BIT #$0080      ; #$0080 = "A"
    BEQ .repeat_init_delay

    LDA #$0020      ; キー入力遅延時間(A): 32
    BRA .repeat_set_delay

.repeat_init_delay
    LDA $18         ; キー入力遅延時間(他)

.repeat_set_delay
    AND #$00FF
    STA $1A,X       ; キー入力遅延時間(現在値)
    LDA $10         ; リピートの対象
    STA $22,X       ; 前回のリピート処理の結果
    RTS

    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; キー入力設定を更新する (戦闘)
;--------------------------------
org $C2FF56
SET_BATTLE_JOYPAD_CONFIG:

;--------------------------------
; キー入力設定を更新する (通常)
;--------------------------------
org $C2FF68
SET_NORMAL_JOYPAD_CONFIG:

;--------------------------------
; キー入力設定を読み込む
;--------------------------------
org $C2FF7D
LOAD_JOYPAD_CONFIG:
    PHB
    PHD
    PHA
    PHX
    PHY
    PHP
    PEA $0000
    PLB
    PLB             ; DBR = $00
    REP #$30
    PEA $0100
    PLD             ; D = $0100
    LDA #$0416      ; ($18 = 22), ($19 = 4)
    STA $18         ; ($18: キー入力遅延時間), ($19: キー入力リピートレート)
    STZ $4D         ; キー入力設定 (0: 通常, 0以外: 戦闘)
    LDY #$0000
    TYX

.transfer_config
    LDA $0975,Y     ; コンフィグ (ボタンの設定)
    JSR GET_INPUT_CONFIG
    STA $26,X       ; コンフィグ (入力値)
    INY
    INX
    INX
    CPY #$0007
    BNE .transfer_config

    STZ $0E         ; 前回のキー入力の結果
    STZ $14         ; 前回のキー入力の結果 ($0114: pad1)
    STZ $16         ; 前回のキー入力の結果 ($0116: pad2)
    LDA #$0000      ; <- LDA #$0101
    LDX #$000C

.init_input_delay
    DEX
    DEX
    STA $1A,X       ; キー入力遅延時間(現在値)
    BNE .init_input_delay

    PLP
    PLY
    PLX
    PLA
    PLD
    PLB
    RTS

;--------------------------------
; Aレジスタにコンフィグ入力設定の値をセットする (80: A, 40: B, 20: X, 10: Y,
; 8: R, 4: L)
;--------------------------------
org $C2FFC2
GET_INPUT_CONFIG:
    PHX
    AND #$00FC
    XBA
    LDX #$0000

.begin
    ASL
    BCS .break

    INX
    INX
    CPX #$000C
    BNE .begin

    LDX #$0000

.break
    LDA FILEPOS_INPUT_CONFIG,X
    PLX
    RTS

;--------------------------------
; メニュー処理を終了する
;--------------------------------
org $C2A02D
MENU_RETURN:
    JSR SCREEN_DISABLE

MENU_EXIT:
    SEP #$20
    RTL

;---------------------------------
; メニュー画面を表示する (Aレジスタ: 種類)
;---------------------------------
org $C2A06B
MENU_START:
    SEP #$20
    STA $43         ; メニューコマンド番号
    JSR MENU_LOAD_SCREEN
    REP #$20
    LDA $43         ; メニューコマンド番号
    AND #$00FF
    CMP #$000C      ; #$000C = "ロード"
    BNE .not_load_command

    LDA $39         ; ニューゲームを開始する (0: ON, 1: OFF)
    BEQ MENU_EXIT   ; セーブが存在しない場合はロード画面を表示せずにニューゲ
                    ; ームを開始する

.not_load_command
    SEP #$20
    LDA #$00
    PHA
    PLB             ; DBR = $00
    JSR MENU_INIT_PPU_RAM
    LDA #$04        ; #$04 = "Screen Settings"
    STA $CA         ; DMA を実行するチャンネル
    LDA #$00
    STA $7E7511     ; BG を更新する
    JSR $A106       ; Wait for V-Blank
    LDA $7E750E     ; HDMA を実行するチャンネル
    STA $420C       ; HDMA Enable
    JSR SCREEN_ENABLE
    JMP MENU_INPUT

;---------------------------------
; メニューの種類によって分岐する
;---------------------------------
MENU_LOAD_SCREEN:
    LDA #$7E
    PHA
    PLB             ; DBR = $7E
    REP #$20
    JSR $C16A       ; メニュー画面を設定する
    JSR $A16E       ; OAM を初期化する
    LDA $43         ; メニューコマンド番号
    AND #$00FF
    DEC
    ASL
    TAX
    LDA FILEPOS_MENU_ADDR,X
    STA $C7
    JMP ($01C7)

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP

;--------------------------------
; 画面表示を有効にする
;--------------------------------
org $C2A0D9
SCREEN_ENABLE:
    SEP #$20
    LDA $004210     ; NMI Flag and 5A22 Version
    LDA #$81        ; #$81 = NMI Enable | Joypad Enable
    STA $004200     ; Interrupt Enable Flags
    LDA #$00
    STA $7E7522
    STA $7E7525
    LDA #$03        ; #$03 = "フェードイン"
    STA $7E7513
    RTS

;--------------------------------
; 画面表示を無効にする
;--------------------------------
org $C2B2BD
SCREEN_DISABLE:
    SEP #$20
    LDA #$00
    STA $7E7510     ; カーソルのアニメーション処理: 対象 (1: ON, 5: ALL)
    STA $7E750F     ; ジョブのアニメーション処理: 対象
    STA $7E751D     ; ジョブのアニメーション処理: タイマー
    STA $7E751E     ; ジョブのアニメーション処理: 状態
    STZ $CA         ; DMA を実行するチャンネル
    LDA #$04        ; #$04 = "フェードアウト"
    STA $7E7513

.screen_wait
    JSR $E66F       ; NMI が完了するまでウェイト
    JSR $FC2F       ; Wait for Menu
    LDA $7E7513     ; フェードアウトが完了するまで繰り返す
    BNE .screen_wait

    LDA #$01        ; #$01 = Joypad Enable
    STA $004200     ; Interrupt Enable Flags
    JSR $A106       ; Wait for V-Blank
    LDA #$00        ; #$00 = HDMA Disable
    STA $00420C     ; HDMA Enable
    LDA #$80        ; #$80 = Force Blank
    STA $002100     ; Screen Display
    RTS

;--------------------------------
; キー入力によって分岐する
;--------------------------------
org $C2A2E9
MENU_INPUT:
    SEP #$20
    REP #$10
    JSR $E66F       ; NMI が完了するまでウェイト
    JSR $FC2F       ; Wait for Menu
    PEA $7E7E
    PLB
    PLB             ; DBR = $7E
    BIT $45         ; 制御フラグ (80: デモメニュー実行中)
    BMI .demo_parse

    JSR GET_INPUT_INDEX
    BRA .input_set

.demo_parse
    LDX $49         ; (デモメニューで使用: ウェイト)
    BMI .demo_next

    DEX
    STX $49         ; (デモメニューで使用: ウェイト)
    LDA $8E         ; $8E = 0
    BRA .input_set  ; ウェイトが完了するまで何もしない

.demo_next
    LDA $48         ; (デモメニューで使用: 入力が格納されたバンク)
    BNE .demo_input ; $48 がゼロなら中断する

    LDA #$08        ; #$08 = "デモメニューを終了する"
    BRA .input_set

.demo_input
    LDA [$46]       ; (デモメニューで使用: 入力が格納されたアドレス)
    LDX $46
    INX             ; 次のアドレスへ
    STX $46
    LDX #$000F      ; キー入力遅延時間 = 15
    STX $49         ; (デモメニューで使用: ウェイト)

.input_set
    STA $4B         ; (デモメニューで使用: 入力)
    BIT #$10        ; 0x10～0x1F はウェイト
    BEQ .input_parse

    LDA #$07        ; #$07 = "デモメニューのウェイト"

.input_parse
    REP #$20
    AND #$000F
    ASL
    TAX
    LDA FILEPOS_$C2A36ADDR,X
    STA $C7
    SEP #$20
    JMP ($01C7)

;--------------------------------
; キー入力に対応した値に変換する
;--------------------------------
org $C2A33A
GET_INPUT_INDEX:
    PHP
    REP #$20
    LDX $8E         ; $8E = 0

.begin
    LDA $0A         ; Input Press (byetUDLR axlr----)
    AND FILEPOS_INPUT_INDEX,X
    BNE .break

    INX
    INX
    INX
    CPX #$0015
    BNE .begin

.break
    LDA FILEPOS_INPUT_INDEX+2,X
    AND #$00FF      ; 入力されたキーによって結果を分岐 (01: A, 02: B,
                    ; 03: Up, 04: Down, 05: Left, 06: Right, 00: (none))
    PLP
    RTS

;--------------------------------
; 記憶したカーソルインデックスを復元する
;--------------------------------
org $C2E67C
RESTORE_CURSOR_POSITION:
    PHP
    REP #$20
    LDA $54         ; メニュー番号
    AND #$00FF
    TAX
    SEP #$20
    LDA $000973     ; コンフィグ (01: すべて外す, 02: モノラル, 04: 記憶,
                    ; 80: ゲージOFF)
    AND #$04        ; #$04 = "記憶"
    BNE .remember

.reset
    LDA FILEPOS_CURSOR_RESET,X
    STA $53         ; カーソルインデックス
    BRA .ret

.remember
    LDA FILEPOS_CURSOR_REMEMBER,X
    BEQ .reset      ; $00 が指定された場合は無効

    REP #$20
    AND #$00FF
    TAX
    SEP #$20
    LDA $00,X
    STA $53         ; カーソルインデックス

.ret
    PLP
    RTS

;--------------------------------
; デフォルトのコンフィグデータを読み込む
;--------------------------------
org $C2A1F0
LOAD_DEFAULT_CONFIG:
    PHB
    PHP
    REP #$20
    LDX #$F342      ; ブロック転送命令用(X) = $C0:F342
    LDY #$0970      ; ブロック転送命令用(Y) = $00:0970: コンフィグ
    LDA #$001F      ; ブロック転送命令用(A) = 31
    MVN $00,$C0
    LDA #$0100
    STA $042D       ; 選択したコマンドの位置(1番目のキャラクタ)
    LDA #$0302
    STA $042F       ; 選択したコマンドの位置(3番目のキャラクタ)
    LDX #FILEPOS_CURSOR_DEFAULT
    LDY #$0159      ; ブロック転送命令用(Y) = $00:0159
    LDA #$0011      ; ブロック転送命令用(A) = 17
    MVN $00,FILEPOS_CURSOR_DEFAULT>>16
    PLP
    PLB
    RTS

    NOP
    NOP
    NOP

;--------------------------------
; スクロールタイプ No.007(07): $2B66/$2B67 を使用する (魔法/青魔法,
; 名前設定/文字選択)
;--------------------------------
org $C2A6FC
MENU_SCROLL_BLUE_MAGIC:
    LDA $58         ; スクロール引数
    DEC
    AND #$0003
    ASL
    TAX
    LDA $C0F3AB,X   ; $FF00(-1,0), $0100(+1,0), $00FF(0,-1), $0001(0,+1)
    STZ $2B6E       ; 画面左に切り替えたかどうか (0: OFF, 1, ON)
    SEP #$20
    LDX $8E         ; $8E = 0

.set_position
    CLC
    ADC $2B66,X     ; 文字の選択位置(横)
    JSR $A780       ; 画面外への切り替えを制御する
    STA $2B66,X     ; 文字の選択位置(横)
    XBA
    INX
    CPX #$0002
    BNE .set_position

    LDA $2B67       ; 文字の選択位置(縦)
    STA $004202     ; 乗算器(8bit×8bit) 被乗数
    LDA $2B68       ; 文字領域のサイズ(縦)
    STA $004203     ; 乗算器(8bit×8bit) 乗数
    NOP             ; (2 cycles)
    NOP             ; (2 cycles)
    NOP             ; (2 cycles)
    CLC             ; (2 cycles)
    LDA $004216     ; 乗算結果(下位) or 除算余剰結果
    ADC $2B66       ; 文字の選択位置(横)
    REP #$20
    AND #$00FF
    TAX
    LDA $7A00,X     ; Menu buffer
    AND #$00FF
    CMP #$00FF      ; 0xFF は選択できない
    BEQ MENU_SCROLL_BLUE_MAGIC

    TXA
    INC
    SEP #$20
    JSR SET_BLUE_MAGIC_CURSOR_POSITION
    JMP $E6AB       ; カーソルの表示を更新する

INIT_BLUE_MAGIC_CURSOR_POSITION:
    STZ $2B66       ; 文字の選択位置(横)
    STZ $2B67       ; 文字の選択位置(縦)
    LDA #$01
    STA $55         ; カーソル位置

SET_BLUE_MAGIC_CURSOR_POSITION:
    LDX $2B6A       ; 文字選択用のカーソル制御アドレスへのオフセット
    STA $7601,X
    LDA #$00
    XBA
    LDA $2B66       ; 文字の選択位置(横)
    AND #$0F
    TAY
    LDA $2B70,Y     ; 文字の選択カーソル位置(横)
    STA $7602,X
    LDA $2B67       ; 文字の選択位置(縦)
    AND #$0F
    TAY
    LDA $2B80,Y     ; 文字の選択カーソル位置(縦)
    STA $7603,X
    RTS

;--------------------------------
; メニューコマンド No.003(03): ジョブ(移動)
;--------------------------------
org $C2A96F
MENU_MOVE_JOB:
    LDA $55         ; カーソル位置
    AND #$00FF
    DEC
    TAX
    SEP #$20
    LDA $6F         ; 選択したジョブ
    BNE .cannot_change
                    ; ジョブを選択中は移動できない

    LDA $7A00,X     ; Menu buffer
    BPL .end_change ; 以下は対象のジョブを取得していない場合

    LDA $53         ; カーソルインデックス
    SEC
    SBC $50         ; 変更前のカーソルインデックス
    CMP #$01
    BNE .cannot_change

    STZ $53         ; すっぴんから右方向へ移動した場合は初期位置へ
    BRA .end_change ; それ以外は移動できない

.cannot_change
    LDA $50         ; 変更前のカーソルインデックス
    STA $53         ; カーソルインデックス

.end_change
    JSR $E6AB       ; カーソルの表示を更新する
    LDA $52         ; 変更前のカーソル位置
    LDX #$0C0C
    JSR UPDATE_JOBS_HIGHLIGHT
    JSR $CD57       ; 選択したジョブの表示を設定する
    JSR $FAD4       ; OAM を更新する
    JSR $FAF0       ; CG を更新する
    JSR REDRAW_JOBS_HIGHLIGHT
    JSR $A9D9       ; ジョブの説明を表示する
    JSR $CD08       ; ジョブの(名前 | レベル | アビリティポイント | 装備でき
                    ; る武器)を表示する
    JMP $A69D       ; BG4 を更新する

;--------------------------------
; ジョブのハイライトの設定を更新する (Aレジスタ: 位置, XL: キャラクタ,
; XH: 星)
;--------------------------------
UPDATE_JOBS_HIGHLIGHT:
    STX $EA
    REP #$20
    AND #$00FF
    DEC
    ASL
    ASL
    TAY
    ASL
    TAX
    SEP #$20
    LDA $0293,X     ; (character)
    AND #$F1
    ORA $EA
    STA $0293,X     ; (character)
    STA $0297,X     ; (character)
    LDA $0363,Y     ; (stars)
    AND #$F1
    ORA $EB
    STA $0363,Y     ; (stars)
    RTS

;--------------------------------
; メニューコマンド No.003(03): ジョブ
;--------------------------------
org $C2CCCB
MENU_JOB:
    PHB
    SEP #$20
    LDA #$06        ; #$06 = "ジョブ"
    JSR $CFBD       ; メニュー番号をAレジスタの値に設定する | 記録したカーソ
                    ; ルインデックスを復元する | カーソルの表示の初期設定を
                    ; 行う | 自分の番号/アドレスを設定する
                    ; /* LONGA ON */
    NOP
    NOP
    NOP
    NOP
    NOP
    STZ $6F         ; 選択したジョブ
    JSR $D503       ; ($D8～$DF) = (ジョブ番号 | ジョブレベル | アビリティポ
                    ; イント | 次のジョブレベルに必要なアビリティポイント)
    JSR $E464       ; 現在のジョブのレベルとアビリティポイントを格納する
    JSR $CDC6       ; キャラクタの名前を表示する | ジョブの名前を表示する |
                    ; キャラクタのレベルを表示する | ジョブのレベル/記号を表
                    ; 示する | ジョブの ABP を表示する
    JSR $D388       ; 全ジョブのスプライトを取得する
    JSR $CECC       ; $7A00 に選択できるジョブをセットする
    JSR $CDE3       ; 各ジョブのスプライトの表示を設定する | 各ジョブをマス
                    ; ターしているかどうか判定する
    JSR $CD57       ; 選択したジョブの表示を設定する
    PHP
    SEP #$20
    LDA #$00        ; #$00 = "ナイト"
    STA $5F         ; 最後に選択したジョブの位置
    STZ $2D11       ; ジョブを変更したかどうかのフラグ (1: 変更した)
    PLP
    LDX #$E95A      ; $6644, $001C, $0038
    JSR $C6E9       ; メッセージの転送先・長さ・最大サイズを設定する (src:
                    ; $C00000 + X)
    JSR $A9D9       ; ジョブの説明を表示する
    JSR $CD08       ; ジョブの(名前 | レベル | アビリティポイント | 装備でき
                    ; る武器)を表示する
    PLB
    RTS

;--------------------------------
; 選択したジョブの表示を設定する
;--------------------------------
org $C2CD57
    PHP
    REP #$20
    LDA $55         ; カーソル位置
    AND #$00FF
    DEC
    TAY
    LDX $80         ; 自分アドレスへのインデックス
    SEP #$20
    LDA $7A00,Y     ; Menu buffer
    STA $EB
    LDA $0500,X     ; キャラクタ番号(bit0-3: 番号 | 20: 女性, 40: 離脱,
                    ; 80: 後列)
    AND #$07
    STA $EA
    REP #$20
    LDA #$C180      ; (dest: $7EC180)
    STA $E4
    JSR $D2DB       ; ジョブのスプライトが格納されているアドレスを取得する
    LDA #$000C
    LDX #$ED31      ; $0000, $0000, $0020, $0020, $0040, $0200, $0060,
                    ; $0220, $0080, $0400, $00A0, $0420,
                    ; $03C0, $0040, $03E0, $0060, $0400, $0240, $0420,
                    ; $0260, $0440, $0440, $0460, $0460
    JSR $D304       ; スプライトを取得する (bank: $E2 | src:
                    ; ($C00000,X) + ($E0) | dest: ($C00002,X) + ($E4)) |
                    ; count: Aレジスタ)
    LDA $EA
    AND #$1F07
    LDY #$0005
    JSR $D492       ; ジョブの CG を取得する (AL: キャラクタ番号, AH: ジョブ
                    ; 番号)
    LDA $55         ; カーソル位置
    LDX #$080A
    JSR UPDATE_JOBS_HIGHLIGHT
    PLP
    RTS

;--------------------------------
; ($7E: 自分の番号) のキャラクタのジョブレベルとアビリティポイントを格納する
;--------------------------------
SETPARAM_JOB_LVABP:
    PHP
    REP #$20
    JSR $D503       ; ($D8～$DF) = (ジョブ番号 | ジョブレベル | アビリティポ
                    ; イント | 次のジョブレベルに必要なアビリティポイント)
    JSR $E464       ; 現在のジョブのレベルとアビリティポイントを格納する
    PLP
    RTS

;--------------------------------
; 選択した魔法の種類をセットする
;--------------------------------
SETCONF_USED_MAGIC:
    PHP
    SEP #$20
    LDX $7E         ; 自分の番号
    LDA $53         ; カーソルインデックス
    STA $63,X       ; 選択した魔法の種類(1番目のキャラクタ)
    PLP
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP

;--------------------------------
; 全ジョブの表示を更新する
;--------------------------------
; /* org $C2CDBA */
REDRAW_JOBS:
    LDX #$E628      ; ブロック転送命令用(X) = $C0:E628
    JMP $A6A0       ; NMI の発生中に DMA 転送を行う ($2116: $00, $30),
                    ; ($4300: $01, $18, $00, $B0, $7E, $80, $11)

;--------------------------------
; 全ジョブのハイライトの表示を更新する
;--------------------------------
; /* org $C2CDC0 */
REDRAW_JOBS_HIGHLIGHT:
    LDX #$EE53      ; ブロック転送命令用(X) = $C0:EE53
    JMP $A6A0       ; NMI の発生中に DMA 転送を行う ($2116: $C0, $38),
                    ; ($4300: $01, $18, $80, $C1, $7E, $80, $06)

;--------------------------------
; 全ジョブのスプライトを取得する
;--------------------------------
org $C2D388
TRANSFER_JOBS_SPRITES:
    PHB
    PHP
    REP #$20
    LDX #$1800

.init_dest
    STZ $AFFE,X     ; ($B000～$C7FE) = 0x00
    DEX
    DEX
    BNE .init_dest

    LDX $80         ; 自分アドレスへのインデックス
    LDA $0500,X     ; キャラクタ番号(bit0-3: 番号 | 20: 女性, 40: 離脱,
                    ; 80: 後列)
    AND #$0007
    STA $EA         ; (キャラクタの番号)

.begin
    LDA $EB         ; (カウンタ)
    AND #$0018      ; #$0018 = %00011000
    ASL
    ASL
    ORA $EB         ; (カウンタ)
    AND #$0067      ; #$0067 = %01100111
    ASL
    XBA
    LSR
    LSR
    LSR
    ADC #$B000      ; (dest: $7EB000)
    STA $E4
    JSR $D2DB       ; ジョブのスプライトが格納されているアドレスを取得する
    LDA #$0006
    LDX #$ED31
    JSR $D304       ; スプライトを取得する (bank: $E2 | src:
                    ; ($C00000,X) + ($E0) | dest: ($C00002,X) + ($E4)) |
                    ; count: Aレジスタ)
    SEP #$20
    INC $EB         ; (カウンタ)
    LDA $EB         ; (カウンタ)
    CMP #$16        ; #$16 = "ジョブの数 (22 種類)"
    REP #$20
    BNE .begin

    PLP
    PLB
    RTS

    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; メニューコマンド No.004(04): 装備変更(終了)
;--------------------------------
org $C2AA12
MENU_UNFOCUS_EQUIP:
    STZ $6F         ; 選択したカーソル位置
    SEP #$20
    LDA #$02        ; #$02 = "BG2 enable"
    TSB $7500       ; Main Screen Designation
    LDA #$04        ; #$04 = "Screen Settings"
    TSB $CA         ; DMA を実行するチャンネル
    JSR GET_MENU_PROPERTY_EQUIP_SUBMENU
    JSR $A8F0       ; Run Menu Script (src: Aレジスタ) | BG2 を更新する
    RTS

    NOP

GET_MENU_PROPERTY_EQUIP_SUBMENU:
    LDA $74         ; 装備変更の種類
    CMP #$03        ; #$03 = "はずす"
    BEQ .unequip_selected

.equip_selected
    LDX #$B065      ; ("[そうび]")
    RTS

.unequip_selected
    LDX #$B07D      ; ("[はずす]")
    RTS

;--------------------------------
; メニューコマンド No.004(04): 装備変更
;--------------------------------
org $C2CA37
MENU_EQUIP:
    SEP #$20
    LDA #$08        ; #$08 = "装備変更"
    JSR $CFBD       ; メニュー番号をAレジスタの値に設定する | 記録したカーソ
                    ; ルインデックスを復元する | カーソルの表示の初期設定を
                    ; 行う | 自分の番号/アドレスを設定する
                    ; /* LONGA ON */
    STZ $6F         ; 選択したカーソル位置
    STZ $72
    SEP #$20
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    JSR $E6AB       ; カーソルの表示を更新する
    LDX #$B036      ; ("[そうび さいきょう すべてはずす はずす おわる]")
    LDA #$05        ; #$05 = "そうび"
    STA $5E         ; 最後に選択した装備の位置
    DEC
    CMP $53         ; カーソルインデックス
    BMI .main_menu  ; 値が 0x05 以上ならメインメニューを表示
                    ; 値が 0x00～0x04 ならサブメニューを表示

.sub_menu
    JSR GET_MENU_PROPERTY_EQUIP_SUBMENU

.main_menu
    REP #$20
    TXA
    JSR $C1B8       ; Run Menu Script
    LDA #$1E98      ; (X = $98, Y = $1E)
    JSR $C8DE       ; キャラクタのスプライトを表示する (AL: X座標,
                    ; AH: Y座標)
    LDY #$51AC      ; (dest: $7E51AC)
    JSR $D533       ; キャラクタの名前を表示する (Yレジスタ: dest)
    LDY #$522C      ; (dest: $7E522C)
    JSR $D554       ; ジョブの名前を表示する (Yレジスタ: dest)
    JSR $E76C       ; キャラクタの能力値をアイテムによって設定する
    JSR $CAC8       ; キャラクタの装備欄の表示を設定する
    JSR $CC9E       ; キャラクタの能力値/武器のパラメータを表示する
    LDY #$52AE      ; (dest: $7E52AE)
    JSR $D7CA       ; 現在装備できる武器のアイコンを表示する (Yレジスタ:
                    ; dest)
    REP #$20
    STZ $6B         ; スクロール位置
    LDA #$00F6
    STA $6D         ; スクロールの上限
    REP #$20
    LDX #$F2D4      ; ブロック転送命令用(X) = $C0:F2D4
    LDY #$298A      ; ブロック転送命令用(Y) = $7E:298A
    LDA #$0015      ; ブロック転送命令用(A) = 21
    MVN $7E,$C0
    LDA #$0001
    STA $29B6       ; スクロールバー位置 (0: $52FC/$55FC, 1: $545C/$585C,
                    ; 2: $537C/$573C, 3: $52FC/$57FC)
    RTS

;--------------------------------
; メニューコマンド No.004(04): 装備変更: アイテム選択: 取消
;--------------------------------
org $C2B7FC
MENU_EQUIP_SELECT_B:
    JSR $AAAF       ; (装備後の能力値の表示を消去する)
    STZ $70
    JMP $B7EE       ; メニューコマンド No.004(04): 装備変更: アイテム選択:
                    ; 決定

;--------------------------------
; 装備できるアイテムを表示するアドレスを設定する
;--------------------------------
SET_EQUIP_LIST_POSITION:
    REP #$20
    STY $99
    LDY $8E         ; $8E = 0
    LDX $6B         ; スクロール位置
    RTS

    NOP
    NOP
    NOP
    NOP

;--------------------------------
; 装備できるアイテムの表示を更新する
;--------------------------------
org $C2CAA5
UPDATE_EQUIP_LIST:
    PHB
    PHP
    PEA $7E7E
    PLB
    PLB             ; DBR = $7E
    LDY #$63C4      ; (dest: $7E63C4)
    JSR SET_EQUIP_LIST_POSITION

.begin
    PHX
    PHY
    LDY $99
    JSR $CB8C       ; $99 += 0x80 (改行)
    JSR $E3E3       ; アイテムの名前/個数を表示する
    PLY
    PLX
    INX
    INY
    CPY #$000A
    BNE .begin

    PLP
    PLB
    RTS

;--------------------------------
; メニューコマンド No.006(06): 店: 購入: 決定
;--------------------------------
org $C2B8AE
MENU_SHOP_BUY_A:
    JSR $B87C       ; ($2809: アイテムの番号), ($280A: 値段/フラグ), ($2810:
                    ; アイテムの説明) をセットする
    JSR $F070       ; ($2811: 所持数), ($2812: 装備数), ($2813: 購入/売却可
                    ; 能な上限値) をセットする
    SEP #$20
    LDA $2813       ; 購入/売却可能な上限値 (0: 購入できない)
    BEQ CANNOT_HAVE_ANY_MORE

    LDX #$2815      ; 店: 所持金
    LDY #$2819      ; 店: 値段
    JSR $EEC8       ; (Xレジスタ)の値 - (Yレジスタ)の値 = ($281D: 32bit)
    BCC HAVE_NOT_ENOUGH_MONEY

    BIT $2805       ; 店: カルナックの店イベント (80: ON)
    BMI KARNAK_EVENT

    LDA #$0B        ; #$0B = "購入/個数選択"
    JMP INPUT_MOVE

CANNOT_HAVE_ANY_MORE:
    JSR SOUND_BEEP
    LDA #$03        ; ("そんなに よくばっちゃダメだよ……")
    JSR $EEE7       ; 店のメッセージを表示する
    LDA #$01        ; #$01 = "しゃがむ"
    BRA CANNOT_BUY

HAVE_NOT_ENOUGH_MONEY:
    JSR SOUND_BEEP
    LDA #$02        ; ("……おかねが たりないようだね?")
    JSR $EEE7       ; 店のメッセージを表示する
    LDA #$00        ; #$00 = "衝撃"
    BRA CANNOT_BUY

ALREADY_HAVE:       ; /* added */
    JSR SOUND_BEEP
    LDA #$06        ; ("もう もってるんでしょ?")
    JSR $EEE7       ; 店のメッセージを表示する
    LDA #$01        ; #$01 = "しゃがむ"

CANNOT_BUY:
    JSR SHOP_CANNOT_BUY_ANIMATION
    LDA #$00        ; (店のメッセージを消去する)
    JSR $EEE7       ; 店のメッセージを表示する
    JMP INPUT_WAIT

;--------------------------------
; カルナックの店イベント
;--------------------------------
org $C2B8FD
KARNAK_EVENT:
    LDA #$01
    STA $39         ; ?
    JSR $B922       ; 選択したアイテムを購入する
    JSR SOUND_BEEP
    REP #$20
    LDA #$B349      ; ("「おまえら!」/「そのまま うごくなっ!!」")
    JSR $C1B8       ; Run Menu Script
    JSR $A698       ; BG3 を更新する
    LDA #$00        ; #$00 = "衝撃"
    JSR $EEFD       ; 購入できない状態の演出を行う (0: 衝撃, 1: しゃがむ)
    JSR $E658       ; 40/60 秒のウェイト
    JMP $A02D       ; メニュー処理を終了する

;--------------------------------
; メニューコマンド No.006(06): 店: 購入: 個数選択: 決定
;--------------------------------
org $C2B955
MENU_SHOP_BUY_SELECT_A:
;--------------------------------
; 購入する個数を選択後、所持金が足りない /* not used */
;--------------------------------
org $C2B97E
    JMP HAVE_NOT_ENOUGH_MONEY
;--------------------------------
; 道具屋でアイテムを購入できない場合にキャラクタが表示される不具合を修正
;--------------------------------
SHOP_CANNOT_BUY_ANIMATION:
    XBA
    LDA $2801       ; 店タイプ (0: 魔法屋, 1: 武器屋, 2: 防具屋, 3: 道具屋,
                    ; 4: アクセサリ, 5: ギルド, 6: 薬屋: 7: えちごや)
    AND #$03
    CMP #$03        ; #$03 = "道具屋/えちごや"
    BNE .equipment_shop

.item_shop
    XBA
    JMP $E658       ; 40/60 秒のウェイト

.equipment_shop
    XBA
    JMP $EEFD       ; 購入できない状態の演出を行う (0: 衝撃, 1: しゃがむ)

;--------------------------------
; メニューコマンド No.006(06): 店
;--------------------------------
org $C2C803
MENU_SHOP:
    SEP #$20
    LDA #$7E
    PHA
    PLB             ; DBR = $7E
    LDA $35         ; メニューコマンド引数: 店の番号
    STA $2800       ; 店の番号
    STZ $39         ; ?
    STZ $2805       ; 店: カルナックの店イベント (80: ON)
    LDA $2800       ; 店の番号
    CMP #$3E
    BEQ .do_karnak_event

    CMP #$3F
    BNE .no_karnak_event

.do_karnak_event
    LDA #$80        ; #$80 = "ON"
    STA $2805       ; 店: カルナックの店イベント (80: ON)

.no_karnak_event
    STZ $2804       ; 店: 制御フラグ (0: 購入, 80: 売却)
    JSR $F18F       ; 店データを初期化する
    REP #$20
    LDX $8E         ; $8E = 0

.init_shop_params
    STZ $2807,X     ; 店で選択したアイテムの位置
    INX
    INX
    CPX #$001E
    BNE .init_shop_params

    LDA $0947       ; 所持金(下位)
    STA $2815       ; 店: 所持金(下位)
    LDA $0949       ; 所持金(上位)
    AND #$00FF
    STA $2817       ; 店: 所持金(上位)
    LDA #$967F
    STA $2821       ; (9999999)
    LDA #$0098
    STA $2823       ; (9999999)
    LDX #$51E8      ; (dest: $7E51E8)
    LDY #$2815      ; 店: 所持金
    LDA #$7E73      ; バンク: $7E, サイズ: 3, 桁: 7
    JSR $E4ED       ; 数値から文字列を取得する (X: dest, Y: src, AH: bank,
                    ; AL: (bit0-3: size | bit4-6: 桁数 | bit7: ゼロパディン
                    ; グON))
    JSR $F15B       ; 店の名前を取得する (店タイプが通常なら「うる」の文字列
                    ; も取得する)
    SEP #$20
    LDA #$18
    STA $2806       ; 売却で最後に選択したアイテムの位置
    LDA #$0B        ; #$0B = "店"
    JSR $CFBD       ; メニュー番号をAレジスタの値に設定する | 記録したカーソ
                    ; ルインデックスを復元する | カーソルの表示の初期設定を
                    ; 行う | 自分の番号/アドレスを設定する
                    ; /* LONGA ON */
    STZ $6B         ; スクロール位置
    STZ $6F         ; 選択したカーソル位置
    LDA #$0003      ; #$0003 = 3
    STA $29B6       ; スクロールバー位置 (0: $52FC/$55FC, 1: $545C/$585C,
                    ; 2: $537C/$573C, 3: $52FC/$57FC)
    LDX #$E954      ; $44C4, $0017, $0045
    JSR $C6E9       ; メッセージの転送先・長さ・最大サイズを設定する (src:
                    ; $C00000 + X)
    JSR UPDATE_CHARACTER_CG
    RTS

;--------------------------------
; 全キャラクタのジョブの CG を取得する
;--------------------------------
org $C2C881
UPDATE_CHARACTER_CG:
    PHP
    REP #$20
    LDY $8E         ; $8E = 0

.begin
    STY $7E         ; 自分の番号
    JSR $D4C5       ; ($80: 自分アドレスへのインデックス) =
                    ; ($7E: 自分の番号)×80
    LDX $80         ; 自分アドレスへのインデックス
    LDA $0500,X     ; キャラクタ番号(bit0-3: 番号 | 20: 女性, 40: 離脱,
                    ; 80: 後列)
    AND #$1F07
    PHY
    JSR $D492       ; ジョブの CG を取得する (AL: キャラクタ番号, AH: ジョブ
                    ; 番号)
    PLY
    INY
    CPY #$0004
    BNE .begin

    PLP
    RTS

;--------------------------------
; メニューコマンド No.007(07): アイテム: 選択(移動)
;--------------------------------
org $C2AC1E
MENU_MOVE_ITEM_SELECT:
    NOP             ; [$AC90: スタートで高速スクロール] を削除
    NOP
    NOP

;--------------------------------
; メニューコマンド No.007(07): アイテム: アイテム選択: 取消
;--------------------------------
org $C2BBFA
MENU_ITEM_SELECT_B:
    STZ $6F         ; 選択したカーソル位置
    STZ $70
    LDA $2889       ; アイテムを選択中かどうか (0: 0FF, 1: ON)
    BNE .item_selected

    STZ $2889       ; アイテムを選択中かどうか (0: 0FF, 1: ON)
    JSR SETCONF_USED_ITEM
    LDA #$00        ; #$00 = "つかう"
    JMP INPUT_MOVE

.item_selected
    STZ $2889       ; アイテムを選択中かどうか (0: 0FF, 1: ON)
    STZ $7510       ; カーソルのアニメーション処理: 対象 (1: ON, 5: ALL)
    JSR $C0E2       ; 選択済みカーソルを消去する
    JSR $FAD4       ; OAM を更新する
    JMP INPUT_WAIT

;--------------------------------
; 選択したアイテムの位置をセットする
;--------------------------------
SETCONF_USED_ITEM:
    LDA $55         ; カーソル位置
    DEC
    STA $5B         ; 最後に選択したアイテムの位置
    LDA $6B         ; スクロール位置
    STA $5C         ; 最後に選択したアイテムのスクロール位置
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法(開始)
;--------------------------------
org $C2ACC3
MENU_FOCUS_MAGIC:
    LDA #$B434      ; ("[しろまほう/くろまほう/じくう][しょうかん/まほうけん
                    ; /あおまほう/うた]")
    JSR $C1B8       ; Run Menu Script
    JSR $A693       ; BG2 を更新する
    JSR $A69D       ; BG4 を更新する
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法(終了)
;--------------------------------
org $C2ACD0         ; moved from $C2ACD6
MENU_UNFOCUS_MAGIC:
    LDA #$B429      ; (魔法リストのウィンドウ領域を消去する)
    JSR $C1B8       ; Run Menu Script
    LDA #$B499      ; ("[しろまほう/くろまほう/じくう][しょうかん/まほうけん
                    ; /あおまほう/うた]" を消去する)
    JSR $C1B8       ; Run Menu Script
    LDA #$B4A4      ; (魔法の種類の枠を表示する)
    JSR $C1B8       ; Run Menu Script
    LDA $7E29E2     ; 選択中の魔法の種類 (0: 魔法剣, 1: 白魔法, 2: 黒魔法,
                    ; 3: 時空, 4: 召喚, 5: 青魔法, 6: 歌)
    AND #$0007
    ASL
    TAX
    LDA $C0F3B3,X   ; (魔法の種類の名称: $B4FD, $B4AF, $B4BF, $B4CF, $B4D9,
                    ; $B4E3, $B4F3)
    JSR $C1B8       ; Run Menu Script
    JSR $A693       ; BG2 を更新する
    JSR $A698       ; BG3 を更新する
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法: 歌(開始)
;--------------------------------
; /* org $C2ACF9 */
MENU_FOCUS_SONG_LIST:
    LDA #$B48E      ; (魔法の説明を消去する)
    JSR $C1B8       ; Run Menu Script
;--------------------------------
; メニューコマンド No.008(08): 魔法: 白魔法,黒魔法,時空,召喚,魔法剣(開始)
;--------------------------------
; /* org $C2ACFF */
MENU_FOCUS_MAGIC_LIST:
    LDA #$B3FE      ; (魔法ウィンドウの枠を表示する)
    JSR $C1B8       ; Run Menu Script
    JSR $DE3E       ; メニューに表示する魔法の設定を初期化する
    JSR $DF4D       ; メニューに表示する魔法の名前を取得する
    JSR $ADD2       ; メニューコマンド No.008(08): 魔法: 青魔法(終了)
    LDA $54         ; メニュー番号
    CMP #$13        ; #$13 = "白魔法,黒魔法,時空,召喚,魔法剣"
    BNE .ret

    LDA $29E2       ; 選択中の魔法の種類 (0: 魔法剣, 1: 白魔法, 2: 黒魔法,
                    ; 3: 時空, 4: 召喚, 5: 青魔法, 6: 歌)
    CMP #$04        ; #$04 = "召喚"
    BEQ .ret

    LDX $7E         ; 自分の番号
    LDA $0973       ; コンフィグ (01: すべて外す, 02: モノラル, 04: 記憶,
                    ; 80: ゲージOFF)
    AND #$04        ; #$04 = "記憶"
    BNE .remember

.reset
    LDA #$07        ; #$07 = "1 番目の魔法"
    STA $67,X       ; 選択した魔法の位置(1番目のキャラクタ)

.remember
    LDA $67,X       ; 選択した魔法の位置(1番目のキャラクタ)
    CMP #$07
    BMI .reset

    CMP #$19
    BPL .reset

    STA $53         ; カーソルインデックス
    JSR $E6AB       ; カーソルの表示を更新する

.ret
    JSR $C6BA       ; キャラクタの名前を表示する | ジョブの名前を表示する |
                    ; キャラクタのレベルを表示する | ジョブのレベル/記号を表
                    ; 示する | ジョブの ABP を表示する | キャラクタの HP を
                    ; 表示する | キャラクタの MP を表示する | 状態アイコンを
                    ; 表示する
    JSR $A698       ; BG3 を更新する
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法: 青魔法(開始)
;--------------------------------
org $C2ADB0
MENU_FOCUS_MAGIC_BLUE_MAGIC:
    LDA #$B41E      ; (青魔法ウィンドウの枠を表示する)
    JSR $C1B8       ; Run Menu Script
    JSR $DE3E       ; メニューに表示する魔法の設定を初期化する
    JSR $DF4D       ; メニューに表示する魔法の名前を取得する
    LDX #$B8EC      ; $07, $04, $0C, $0C, $2C, $04, $0C, $0C, $0C, $0C, $0C,
                    ; $0C, $0C, $0C, $0C, 14, $00
    LDY #$7180      ; #$7180 = "BG4"
    JSR $C1FD       ; Configure the Line Position
    JSR $A69D       ; BG4 を更新する
    STZ $2B66       ; 文字の選択位置(横)
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法: 青魔法(終了)
;--------------------------------
org $C2ADCC
MENU_UNFOCUS_MAGIC_BLUE_MAGIC:
    LDA #$B429      ; (青魔法ウィンドウを消去する)
    JSR $C1B8       ; Run Menu Script
    LDX #$B8E6      ; $07, $04, $0C, $0C, $04, $00
    LDY #$7180      ; #$7180 = "BG4"
    JSR $C1FD       ; Configure the Line Position
    JSR $A69D       ; BG4 を更新する
    RTS

;--------------------------------
; メニューコマンド No.008(08): 魔法: 決定
;--------------------------------
org $C2BC2D
MENU_MAGIC_A:
    LDX $7E         ; 自分の番号
    LDA $53         ; カーソルインデックス
    STA $63,X       ; 選択した魔法の種類(1番目のキャラクタ)
    LDA $55         ; カーソル位置

UPDATE_MAGIC_LIST:
    DEC
    STA $29E2       ; 選択中の魔法の種類 (0: 魔法剣, 1: 白魔法, 2: 黒魔法,
                    ; 3: 時空, 4: 召喚, 5: 青魔法, 6: 歌)
    REP #$20
    AND #$0007
    TAX
    SEP #$20
    LDA $C0F3A4,X   ; $07, $07, $07, $07, $07, $19, $1A
    JMP INPUT_MOVE

;--------------------------------
; メニューコマンド No.008(08): 魔法: 取消
;--------------------------------
org $C2BC48
MENU_MAGIC_B:
    JSR SCREEN_DISABLE
    JSR SETCONF_USED_MAGIC
    LDA $71         ; 選択したキャラクタの番号
    STA $5D         ; 最後に魔法を選択したキャラクタの番号
    LDA #$01        ; #$01 = "メインメニュー"
    JMP MENU_START

    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; メニューコマンド No.009(09): コンフィグ: 短縮(開始)
;--------------------------------
org $C2B079
MENU_FOCUS_CONFIG_SHORTUCT:
;--------------------------------
; $EF9F を使用; 拡張用の空き領域を作成する
; /* XXX: これ以上の容量を使用しないこと ($C2B0B0 is used) */
;--------------------------------
org $C2B0A0
    JSR $EF9F       ; パーティにいないキャラクタを表示しない
    STZ $6F         ; 選択したカーソル位置
    NOP             ; (used for fix)
    NOP
    NOP
    STZ $71         ; 選択したキャラクタの番号
    LDA #$0020      ; #$0020 = "HDMA channel 5: BG2 Vertical Scroll"
    JMP $B154       ; BG2 を前面に表示する | Aレジスタの値の HDMA を使用する

;--------------------------------
; メニューコマンド No.009(09): コンフィグ
;--------------------------------
org $C2C34A
MENU_CONFIG:
    JSR $F63D       ; コンフィグデータを読み込む
    STZ $2C94

.init_config
    JSR $F7A6       ; コンフィグの表示を設定する
    INC $2C94
    LDA $2C94
    CMP #$000A
    BNE .init_config

    NOP
    NOP
    NOP
    NOP             ; (used for fix)
    NOP
    NOP
    JSR $F810       ; ウィンドウカラーバーの表示を設定する
    SEP #$20
    STZ $53         ; カーソルインデックス
    JSR $D210       ; カーソルの表示の初期設定を行う
    RTS

;--------------------------------
; メニューコマンド No.011(0B): セーブ: 確認(開始)
; メニューコマンド No.012(0C): ロード: 確認(開始)
;--------------------------------
org $C2AE6F
MENU_FOCUS_SAVELOAD:
;--------------------------------
; SCREEN_ENABLE を使用; 拡張用の空き領域を作成する
;--------------------------------
org $C2AEE6
    JSR SCREEN_ENABLE
    JSR $A698       ; BG3 を更新する
    JSR $FAD4       ; OAM を更新する
    JSR $FAF0       ; CG を更新する
    LDA #$0C        ; #$0C = "BG3 and BG4 enable"
    TSB $7500       ; Main Screen Designation
    TSB $7502       ; Window Mask Designation for the Main Screen
    LDA #$02        ; #$02 = "BG2 enable"
    TRB $7500       ; Main Screen Designation
    LDA #$04        ; #$04 = "Screen Settings"
    TSB $CA         ; DMA を実行するチャンネル
    JSR $A69D       ; BG4 を更新する
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP

;--------------------------------
; セーブデータの全ジョブのスプライトを取得する
;--------------------------------
org $C2F463
SAVELOAD_TRANSFER_JOBS_SPRITES:
;--------------------------------
; MENU_INIT_PPU_RAM で処理されるため、ここでは転送しない
;--------------------------------
org $C2F4CB
    PLP
    PLB
    RTS

    NOP
    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; クルルのパラメータを初期化する
;--------------------------------
org $C2D958
INIT_PARAMETERS_FOR_KRILE:
    PHP
    PHB
    STZ $7E         ; 自分の番号

.next_character
    JSR $D4C5       ; ($80: 自分アドレスへのインデックス) =
                    ; ($7E: 自分の番号)×80
    LDX $80         ; 自分アドレスへのインデックス
    LDA $0500,X     ; キャラクタ番号(bit0-3: 番号 | 20: 女性, 40: 離脱,
                    ; 80: 後列)
    AND #$07
    CMP #$04        ; #$04 = "クルル"
    BEQ .init_params

    INC $7E         ; 自分の番号
    LDA $7E         ; 自分の番号
    CMP #$04
    BNE .next_character

    BRA .ret

.init_params
    JSR SETPARAM_JOB_LVABP
    JSR $DAA4       ; 装備をすべて外す
    LDX $7E         ; 自分の番号
    INC $0420,X     ; 選択したコマンドの位置(チェックサム)
    LDA #$15        ; #$15 = "すっぴん"
    JSR JOB_CHANGE

.ret
    PLB
    PLP
    RTS

;--------------------------------
; 現在のキャラクタのジョブを変更する (Aレジスタ: ジョブ番号)
;--------------------------------
JOB_CHANGE:
    PHP
    SEP #$20
    STA $D8         ; 現在のジョブ番号
    JSR $E47D       ; 現在のジョブの(レベル | アビリティポイント | 次に必要
                    ; なアビリティポイント)をセットする
    LDX $80         ; 自分アドレスへのインデックス
    LDA $DA         ; 現在のジョブレベル
    STA $053A,X     ; ジョブレベル
    LDA $D8         ; 現在のジョブ番号
    STA $0501,X     ; ジョブ番号
    REP #$20
    LDA $DC         ; 現在のジョブのアビリティポイント
    STA $053B,X     ; アビリティポイント
    JSR $EB82       ; 現在のジョブの(ジョブ特性 | アビリティコマンド | 装備
                    ; できるアイテム)をセットする
    JSR $E6D6       ; キャラクタの(HP | MP | 能力値 | フラグ)を初期化する
    PLP
    RTS

    NOP

;--------------------------------
; デモメニューを開始/再開する
;--------------------------------
org $C2A394 : DEMO_CONFIGURE:
org $C2A394 : .backup_parameters
org $C2A3A3 : .init_demo
org $C2A3CA : .init_abilities
org $C2A3D8 : .init_config
org $C2A3FB : .init_items
org $C2A40F : .init_jobs
    STZ $7E         ; 自分の番号
    JSR $D4C5       ; ($80: 自分アドレスへのインデックス) =
                    ; ($7E: 自分の番号)×80
    JSR $DAA4       ; 装備をすべて外す
    REP #$20
    LDA $35         ; メニューコマンド引数: デモの種類
    AND #$0007
    TAX
    SEP #$20
    LDA $C0E8F0,X   ; $15, $0A, $0A, $0A, $09, $15, $15, $15
    JSR JOB_CHANGE
    PLP
    RTS

    NOP

;--------------------------------
; すべてのキャラクタの装備をすべて外す
;--------------------------------
; /* org $C2A42B */
UNEQUIP_ALL_MEMBER:
    PHP
    SEP #$20
    LDA #$03
    STA $7E         ; 自分の番号

.next_character
    JSR $D4C5       ; ($80: 自分アドレスへのインデックス) =
                    ; ($7E: 自分の番号)×80
    JSR $DAA4       ; 装備をすべて外す
    JSR $E6D6       ; キャラクタの(HP | MP | 能力値 | フラグ)を初期化する
    DEC $7E         ; 自分の番号
    BPL .next_character

    PLP
    RTS

; /* End of core implementation */

; /* Start of BTL_core implementation */

;--------------------------------
; 実行中のメニューコマンドタイプによって処理を分岐する
;--------------------------------
org $C11186
BTL_MENU_INPUT:
    LDA $CD3A       ; メニューコマンドタイプ
    ASL
    TAX
    LDA FILEPOS_BTL_$C2A36ADDR,X
    STA $88
    LDA FILEPOS_BTL_$C2A36ADDR+1,X
    STA $89
    JMP ($0088)

;--------------------------------
; メニューコントロールを実行する
;--------------------------------
org $C13A6E
BTL_MENU_CONTROL:
    LDA $BC65       ; グラフィックを更新する
    BNE .ret

    LDA $CD38       ; 実行中のメニューコントロール
    BNE .do_control

    LDA $CD39       ; メニューコントロール
    STA $CD38       ; 実行中のメニューコントロール
    STZ $CD39       ; メニューコントロール

.do_control
    LDA $CD38       ; 実行中のメニューコントロール
    ASL
    TAX
    LDA FILEPOS_BTL_CONTROL_ADDR,X
    STA $70
    LDA FILEPOS_BTL_CONTROL_ADDR+1,X
    STA $71
    JMP ($0070)

.ret
    RTS

;--------------------------------
; メニューコマンドタイプ No.003(03): 下スクロール処理
;--------------------------------
org $C14A86
BTL_SCROLL_COMMAND_DOWN:

org $C14AF5
    SEC             ; C=1 to subtract
    JMP BTL_SCROLL_COMMAND_PROCEED

;--------------------------------
; スクロールバッファのアドレスをセットする
;--------------------------------
; /* org $C14AF9 */
BTL_SCROLL_GETADDR:
    LDY #$CD7B      ; (dest: $7ECD7B)
    STY $BF
    LDY #$CDBB      ; (dest: $7ECDBB)
    STY $C1
    TDC
    TAY             ; Y = 0
    RTS

;--------------------------------
; スクロールバッファを更新する
;--------------------------------
; /* org $C14B06 */
BTL_SCROLL_UPDATE:
    LDA $CDFA
    ASL
    TAX
    REP #$20
    LDA $CEFFF5,X   ; $4C20, $4C60, $4CA0, $4CE0, $4D20
    STA $CD75
    TDC
    SEP #$20
    INC $CD74       ; アイテム/魔法リストを更新する
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP

;--------------------------------
; メニューコマンドタイプ No.004(04): 上スクロール処理
;--------------------------------
org $C14B22
BTL_SCROLL_COMMAND_UP:

org $C14B8F
    CLC             ; C=0 to add
    JMP BTL_SCROLL_COMMAND_PROCEED

    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; メニューコマンドタイプ No.003(03): スクロール続行/終了
;--------------------------------
BTL_SCROLL_COMMAND_PROCEED:
    LDX #$00BC

.begin
    LDA $BA37,X
    STA $B2D5,X
    DEX
    DEX
    DEX
    DEX
    BPL .begin

    TDC
    SEP #$20
    JSR BTL_SCROLL_MOVECURSOR_SINGLE
    JSR $4BBC       ; 選択したカーソルの表示を更新する
    DEC $CD37       ; メニュー処理を行う回数
    BNE .ret

    JSR $FD07       ; メニューを変更する
    JSR $1186       ; 実行中のメニューコマンドタイプによって処理を分岐する

.ret
    RTS

;--------------------------------
; アイテムリストのスクロール処理
;--------------------------------
org $C15E04
BTL_SCROLL_ITEM:
    PHX
    JSR $5B86       ; $92 = 行動選択中のキャラクタの有効フラグビット
    JSR BTL_SCROLL_GETADDR
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    CLC
    ADC $88
    ASL
    TAX
    JSR $5E3B       ; アイテムの名前/所持数を表示する
    INX
    JSR $5E3B       ; アイテムの名前/所持数を表示する
    JSR BTL_SCROLL_UPDATE
    PLX
    RTS

;--------------------------------
; 選択済みカーソルをスクロールする
;--------------------------------
; /* org $C15E1F */
BTL_SCROLL_MOVECURSOR_TRIPLE:
    LDA #$0C
    BRA BTL_SCROLL_MOVECURSOR

BTL_SCROLL_MOVECURSOR_SINGLE:
    LDA #$04

BTL_SCROLL_MOVECURSOR:
    REP #$20
    BCC .positive

.negative
    EOR #$FFFF      ; carry がセットされていれば負の数とする

.positive
    ADC $CF3E       ; 選択済みカーソルの表示位置(縦)
    STA $CF3E       ; 選択済みカーソルの表示位置(縦)
    TDC
    SEP #$20
    RTS

    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; 魔法のスクロール処理
;--------------------------------
org $C157B1
BTL_SCROLL_MAGIC:
    PHY
    TYA
    ASL
    TAX
    JSR $5784       ; Xレジスタと($88) = スクロールで表示する魔法のアドレス
    JSR BTL_SCROLL_GETADDR
    LDA $CF         ; 魔法の種類 (0: 通常, 1: 歌/青魔法)
    BEQ .normal_magic

.blue_magic
    JSR $584B       ; 魔法の名前を表示する (歌・青魔法)
    INX
    JSR $584B       ; 魔法の名前を表示する (歌・青魔法)
    LDX #$0008
    BRA .fill_submenu

.normal_magic
    JSR $5806       ; 魔法の名前を表示する (魔法剣・白魔法・黒魔法・時魔法・
                    ; 召喚)
    INX
    JSR $5806       ; 魔法の名前を表示する (魔法剣・白魔法・黒魔法・時魔法・
                    ; 召喚)
    INX
    JSR $5806       ; 魔法の名前を表示する (魔法剣・白魔法・黒魔法・時魔法・
                    ; 召喚)
    LDX #$0007

.fill_submenu
    LDA #$FF        ; #$FF = " "
    JSR $5F6B       ; 数値の文字コードを処理する (dest: ($BF),Y | ($C1),Y)
    DEX
    BNE .fill_submenu

    JSR BTL_SCROLL_UPDATE
    PLY
    RTS

    NOP

;--------------------------------
; Xレジスタ = 選択した魔法へのインデックス
;--------------------------------
BTL_MAGIC_GETADDR:
    LDA ($D3),Y     ; 選択した魔法の位置
    CLC
    ADC $DB         ; 魔法リスト: 開始番号
    REP #$21
    ADC $CEFF8D,X   ; ($2E38, $2F3C: 使用できる魔法) へのインデックス:
                    ; 0, 650, 1300, 1950
    TAX
    TDC
    SEP #$20
    RTS

;--------------------------------
; 実行する行動の種類をセットする | Aレジスタの値の魔法を選択する
;--------------------------------
BTL_MAGIC_SETNUM:
    CLC
    ADC $DB         ; 魔法リスト: 開始番号
    STA $41B6,X     ; 選択したアイテム/魔法の番号
    LDA #$20        ; #$20 = "魔法"
    ORA $F891       ; アイテム/魔法の選択回数 (0: 1回, 8: 2回)
    STA $41B1,X     ; 実行する行動の種類 (1)
    RTS

;--------------------------------
; 魔法の消費マジックポイントを更新する
;--------------------------------
org $C15574
BTL_MAGIC_UPDATE_MP_COST:
    JSR BTL_MAGIC_GETADDR
    LDA $2E38,X     ; 1人目の魔法の消費MP
    TAX
    CMP #$64        ; C=1 if MP_cost >= 100
    TDC
    ADC #$68        ; (MP_cost >= 100) ? 0x69("0") : 0x68(" ")
    STA $C363       ; 消費マジックポイントの表示[0]
    CPX #$000A      ; C=1 if MP_cost >= 10
    TDC
    ADC #$68        ; (MP_cost >= 10) ? 0x69("0") : 0x68(" ")
    STA $C365       ; 消費マジックポイントの表示[1]
    TXA

.digit_hundreds
    CMP #$64
    BCC .digit_tens

    SBC #$64
    INC $C363       ; 消費マジックポイントの表示[0]
    BRA .digit_hundreds

.digit_tens
    CMP #$0A
    BCC .digit_one

    SBC #$0A
    INC $C365       ; 消費マジックポイントの表示[1]
    BRA .digit_tens

.digit_one
    ADC #$69        ; #$69 = "0"
    STA $C367       ; 消費マジックポイントの表示[2]
    INC $CD44       ; 消費マジックポイントを更新する
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP

;--------------------------------
; メニューコマンド処理: 上スクロール
;--------------------------------
; /* org $C155B9 */
BTL_SCROLL_UP:
    LDA #$04        ; #$04 = "上スクロール"
    BRA BTL_SCROLL

;--------------------------------
; メニューコマンド処理: 下スクロール
;--------------------------------
; /* org $C155BD */
BTL_SCROLL_DOWN:
    LDA #$03        ; #$03 = "下スクロール"

BTL_SCROLL:
    PHA
    LDA $CD3A       ; メニューコマンドタイプ
    STA $CD3B       ; 次に実行するメニューコマンドタイプ[0]
    PLA
    STA $CD3A       ; メニューコマンドタイプ
    LDA #$03
    STA $CD37       ; メニュー処理を行う回数
    RTS

;--------------------------------
; メニューコマンドタイプ No.011(0B): 魔法
;--------------------------------
org $C155D0
BTL_MAGIC_INPUT:
    LDA $CD42       ; 行動選択中のキャラクタの番号 (FF: none)
    TAY
    ASL
    TAX
    STZ $CD6C       ; 上スクロールバーを表示する (1: ON, 0: OFF)
    STZ $CD70       ; 下スクロールバーを表示する (1: ON, 0: OFF)
    LDA $CDF8       ; (メニューを閉じる)
    BNE .reset_selected_menu

    LDA #$33        ; vhoopppN = 00110011
    STA $CD6F       ; 上スクロールバーの設定
    LDA #$B3        ; vhoopppN = 10110011
    STA $CD73       ; 下スクロールバーの設定
    LDA ($D9),Y     ; 選択した魔法のスクロール位置
    BEQ .hide_scroll_up

    INC $CD6C       ; 上スクロールバーを表示する (1: ON, 0: OFF)

.hide_scroll_up
    CMP $DD         ; 魔法リスト: スクロールの上限
    BEQ .hide_scroll_down

    INC $CD70       ; 下スクロールバーを表示する (1: ON, 0: OFF)

.hide_scroll_down
.begin
    LDA $00         ; Input Press (axlr----)
    BPL .read_$C2A378

.$C2A36A
    JSR BTL_SOUND_OK
    JSR BTL_MAGIC_GETADDR
    LDA $2F3C,X     ; 1人目の魔法欄の魔法が使用かどうか (80: 使用不可)
    BPL .magic_select

    JMP BTL_SOUND_BEEP

.magic_select
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    PHX
    LDA $F890       ; 行動指定オフセット (0: 1回目, 7: 2回目)
    TAX
    LDA ($D3),Y     ; 選択した魔法の位置
    JSR BTL_MAGIC_SETNUM
    PLX
    LDA #$0B        ; #$0B = "魔法"
    STA $88         ; 取消時に表示するメニューコマンドタイプ
    LDA $2EBA,X     ; 魔法の対象
    JMP $510E       ; Aレジスタの対象フラグに従って、対象を選択する

.read_$C2A378
    LDA $01         ; Input Press (byetUDLR)
    BPL .read_input_move

.$C2A378
    JSR BTL_SOUND_CANCEL

.reset_selected_menu
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    JMP $4773       ; メニューコマンド処理: 魔法: キャンセル

.read_input_move
    JSR $5574       ; 魔法の消費マジックポイントを更新する
    JSR $5536       ; カーソルの表示: 魔法
    LDA $01         ; Input Press (byetUDLR)
    BIT #$02
    BNE BTL_MAGIC_INPUT_LEFT

    BIT #$01
    BNE BTL_MAGIC_INPUT_RIGHT

    BIT #$04
    BNE BTL_MAGIC_INPUT_DOWN

    BIT #$08
    BEQ .not_input_up

    JMP BTL_MAGIC_INPUT_UP

.not_input_up
    LDA $00         ; Input Press (axlr----)
    AND #$30
    BEQ .ret

    JMP BTL_MAGIC_INPUT_LR

.ret
    RTS

;--------------------------------
; メニューコマンドタイプ No.012(0C): 魔法: 右
;--------------------------------
BTL_MAGIC_INPUT_RIGHT:
    LDA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    CMP $D1         ; 魔法リスト: カーソル位置の上限(横)
    BEQ .next

    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    INC
    STA ($D3),Y     ; 選択した魔法の位置
    LDA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    INC
    STA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    BRA .ret

.next
    LDA $DC         ; 魔法リスト: 終了番号
    SEC
    SBC $DB         ; 魔法リスト: 開始番号
    CMP ($D3),Y     ; 選択した魔法の位置
    BEQ .ret

.move_to_down
    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    SEC
    SBC $D1         ; 魔法リスト: カーソル位置の上限(横)
    STA ($D3),Y     ; 選択した魔法の位置
    TDC
    STA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    JSR BTL_MAGIC_INPUT_DOWN

.ret
    JMP $5536       ; カーソルの表示: 魔法

;--------------------------------
; メニューコマンドタイプ No.012(0C): 魔法: 左
;--------------------------------
BTL_MAGIC_INPUT_LEFT:
    LDA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    BEQ .next

    JSR BTL_SOUND_SELECT
    LDA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    DEC
    STA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    LDA ($D3),Y     ; 選択した魔法の位置
    DEC
    STA ($D3),Y     ; 選択した魔法の位置
    BRA .ret

.next
    LDA ($D3),Y     ; 選択した魔法の位置
    BEQ .ret

.move_to_up
    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    CLC
    ADC $D1         ; 魔法リスト: カーソル位置の上限(横)
    STA ($D3),Y     ; 選択した魔法の位置
    LDA $D1         ; 魔法リスト: カーソル位置の上限(横)
    STA ($D5),Y     ; 選択した魔法のカーソル位置(横)
    JSR BTL_MAGIC_INPUT_UP

.ret
    JMP $5536       ; カーソルの表示: 魔法

;--------------------------------
; メニューコマンドタイプ No.012(0C): 魔法: 下
;--------------------------------
BTL_MAGIC_INPUT_DOWN:
    LDA ($D7),Y     ; 選択した魔法のカーソル位置(縦)
    CMP #$03
    BEQ .next

    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    CLC
    ADC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    LDA ($D7),Y     ; 選択した魔法のカーソル位置(縦)
    INC
    STA ($D7),Y     ; 選択した魔法のカーソル位置(縦)

.ret
    RTS

.next
    LDA ($D9),Y     ; 選択した魔法のスクロール位置
    CMP $DD         ; 魔法リスト: スクロールの上限
    BEQ .ret

.scroll_down
    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    CLC
    ADC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    JSR $5750       ; メニューコマンドタイプ No.012(0C): 魔法: 下スクロール
    JMP BTL_SCROLL_DOWN

;--------------------------------
; メニューコマンドタイプ No.012(0C): 魔法: 上
;--------------------------------
BTL_MAGIC_INPUT_UP:
    LDA ($D7),Y     ; 選択した魔法のカーソル位置(縦)
    BEQ .next

    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    SEC
    SBC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    LDA ($D7),Y     ; 選択した魔法のカーソル位置(縦)
    DEC
    STA ($D7),Y     ; 選択した魔法のカーソル位置(縦)

.ret
    RTS

.next
    LDA ($D9),Y     ; 選択した魔法のスクロール位置
    BEQ .ret

.scroll_up
    JSR BTL_SOUND_SELECT
    LDA ($D3),Y     ; 選択した魔法の位置
    SEC
    SBC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    JSR $576C       ; メニューコマンドタイプ No.012(0C): 魔法: 上スクロール
    JMP BTL_SCROLL_UP

;--------------------------------
; メニューコマンドタイプ No.008(08): アイテム/武器
;--------------------------------
org $C15BA3
BTL_WEAPON_INPUT:
    LDA #$03        ; vhoopppN = 00000011
    STA $CD4B       ; カーソルの設定
    LDA $CD42       ; 行動選択中のキャラクタの番号 (FF: none)
    TAX
    LDA $CDF8       ; (メニューを閉じる)
    BNE .reset_selected_menu

.begin
    LDA #$01
    STA $043D,X     ; 現在のアイテム欄の種類 (0: アイテム, 1: 武器)
    LDA $00         ; Input Press (axlr----)
    BPL .read_$C2A378

.$C2A36A
    JSR BTL_SOUND_OK
    LDA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)
    JSR $588D       ; 装備アイテムを選択/使用する (C=1: 対象選択)
    BCC .break

    LDA #$10        ; #$10 = "武器使用"
    JMP BTL_USE_ITEM_WEAPON

.read_$C2A378
    LDA $01         ; Input Press (byetUDLR)
    BPL .read_input_down

.$C2A378
    JSR BTL_SOUND_CANCEL
    LDA $F88C       ; アイテムを選択したかどうか (80: ON)
    BPL .weapon_cancel

.weapon_unselect
    JSR $5B93       ; 項目を非選択にする
    BRA .break

.weapon_cancel
    INC $0439,X     ; 武器選択をキャンセルした (1: ON)
    BRA .reset_selected_menu

.read_input_down
    BIT #$04        ; #$04 = "Down"
    BEQ .read_input_left

.input_down
    LDA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)

.weapon_back
    JSR BTL_SOUND_SELECT
    STA $0445,X     ; 選択したアイテムのカーソル位置(横)
    STA $0441,X     ; 選択したアイテムの位置
    STZ $043D,X     ; 現在のアイテム欄の種類 (0: アイテム, 1: 武器)

.reset_selected_menu
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    JMP $47A3       ; メニューコマンド処理: アイテム/武器: キャンセル

.read_input_left
    BIT #$02        ; #$02 = "Left"
    BEQ .read_input_right

    LDA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)
    BEQ .break

    DEC
    BRA .weapon_swap

.read_input_right
    BIT #$01        ; #$01 = "Right"
    BEQ .break

    LDA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)
    DEC             ; (左手から移動したかどうか?)
    BEQ .weapon_back

    INC
    INC

.weapon_swap
    JSR BTL_SOUND_SELECT
    STA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)

.break
    LDA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)
    ASL
    TAX
    LDA $C1525B,X   ; $10, $80
    STA $CD49       ; カーソルの表示位置(横)
    LDA $C1525C,X   ; $BA, $BA
    STA $CD4A       ; カーソルの表示位置(縦)
    LDA #$01
    STA $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    LDA #$33        ; vhoopppN = 00110011
    STA $CD4B       ; カーソルの設定
    STA $CD53       ; 武器カーソルの設定
    STZ $CD50       ; 武器カーソルを表示する (1: ON, 0: OFF)
    LDA $F88C       ; アイテムを選択したかどうか (80: ON)
    AND #$40
    BEQ .ret

    LDA $F88D       ; 選択中の装備/アイテムの位置
    ASL
    TAX
    LDA $C1525B,X   ; $10, $80
    ADC #$04        ; $14, $84
    STA $CD51       ; 武器カーソルの表示位置(横)
    LDA $C1525C,X   ; $BA, $BA
    STA $CD52       ; 武器カーソルの表示位置(縦)
    INC $CD50       ; 武器カーソルを表示する (1: ON, 0: OFF)

.ret
    RTS

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム
;--------------------------------
org $C15C88
BTL_ITEM_INPUT:
    LDA $CD42       ; 行動選択中のキャラクタの番号 (FF: none)
    TAX
    STZ $CD6C       ; 上スクロールバーを表示する (1: ON, 0: OFF)
    STZ $CD70       ; 下スクロールバーを表示する (1: ON, 0: OFF)
    LDA $CDF8       ; (メニューを閉じる)
    BNE .reset_selected_menu

    LDA $0439,X     ; 武器選択をキャンセルした (1: ON)
    BNE .reset_selected_menu

    INC $CD6C       ; 上スクロールバーを表示する (1: ON, 0: OFF)
    LDA #$03        ; vhoopppN = 00000011
    STA $CD6F       ; 上スクロールバーの設定
    LDA #$83        ; vhoopppN = 10000011
    STA $CD73       ; 下スクロールバーの設定
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    CMP #$7C
    BEQ .hide_scroll_down

    INC $CD70       ; 下スクロールバーを表示する (1: ON, 0: OFF)

.hide_scroll_down
    LDA $CFC3       ; (「アイテム」以外では武器欄は無効)
    BEQ .allow_select_weapon

    STZ $043D,X     ; 現在のアイテム欄の種類 (0: アイテム, 1: 武器)

.allow_select_weapon
    LDA $043D,X     ; 現在のアイテム欄の種類 (0: アイテム, 1: 武器)
    BNE BTL_DISPLAY_WEAPON_CURRENT

.begin
    JSR $5511       ; カーソルの表示: アイテム
    LDA $00         ; Input Press (axlr----)
    BPL .read_$C2A378

.$C2A36A
    JSR BTL_SOUND_OK
    LDA $0441,X     ; 選択したアイテムの位置
    JSR $594E       ; アイテムを選択/使用する (C=1: 対象選択)
    BCC .ret

    LDA #$40        ; #$40 = "アイテム"
    JMP BTL_USE_ITEM_WEAPON

.read_$C2A378
    LDA $01         ; Input Press (byetUDLR)
    BPL .read_input_move

.$C2A378
    JSR BTL_SOUND_CANCEL
    LDA $F88C       ; アイテムを選択したかどうか (80: ON)
    BPL .reset_selected_menu

.item_unselect
    JMP $5B93       ; 項目を非選択にする

.reset_selected_menu
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    STZ $0439,X     ; 武器選択をキャンセルした (1: ON)
    JMP $47FE

.read_input_move
    BIT #$02
    BNE BTL_ITEM_INPUT_LEFT

    BIT #$01
    BNE BTL_ITEM_INPUT_RIGHT

    BIT #$04
    BEQ .not_input_down

    JMP BTL_ITEM_INPUT_DOWN

.not_input_down
    BIT #$08
    BNE BTL_ITEM_INPUT_UP

    LDA $00         ; Input Press (axlr----)
    AND #$30
    BEQ .ret

    JMP BTL_ITEM_INPUT_LR

.ret
    RTS

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: 武器に移動
;--------------------------------
BTL_DISPLAY_WEAPON:
    JSR BTL_SOUND_SELECT
    STA $0435,X     ; 選択した武器の種類 (0: 右手, 1: 左手)

BTL_DISPLAY_WEAPON_CURRENT:
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    JMP $4789       ; メニューコマンド処理: アイテム: 武器

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: 左
;--------------------------------
BTL_ITEM_INPUT_LEFT:
    LDA $0445,X     ; 選択したアイテムのカーソル位置(横)
    BEQ .next

    JSR BTL_SOUND_SELECT
    DEC $0441,X     ; 選択したアイテムの位置
    DEC $0445,X     ; 選択したアイテムのカーソル位置(横)
    BRA .ret

.next
    LDA $0441,X     ; 選択したアイテムの位置
    BNE .move_to_up

    LDA $CFC3       ; (「アイテム」以外では武器欄は無効)
    BNE .ret

.move_to_weapon
    LDA #$01        ; #$01 = "左手"
    BRA BTL_DISPLAY_WEAPON

.move_to_up
    INC $0441,X     ; 選択したアイテムの位置
    INC $0445,X     ; 選択したアイテムのカーソル位置(横)
    JSR BTL_ITEM_INPUT_UP

.ret
    JMP $5511       ; カーソルの表示: アイテム

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: 右
;--------------------------------
BTL_ITEM_INPUT_RIGHT:
    LDA $0445,X     ; 選択したアイテムのカーソル位置(横)
    BNE .next

    JSR BTL_SOUND_SELECT
    INC $0441,X     ; 選択したアイテムの位置
    INC $0445,X     ; 選択したアイテムのカーソル位置(横)
    BRA .ret

.next
    LDA $0441,X     ; 選択したアイテムの位置
    CMP #$FF
    BEQ .ret

.move_to_down
    JSR BTL_SOUND_SELECT
    DEC $0441,X     ; 選択したアイテムの位置
    STZ $0445,X     ; 選択したアイテムのカーソル位置(横)
    JSR BTL_ITEM_INPUT_DOWN

.ret
    JMP $5511       ; カーソルの表示: アイテム

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: 上
;--------------------------------
BTL_ITEM_INPUT_UP:
    LDA $0449,X     ; 選択したアイテムのカーソル位置(縦)
    BEQ .next

    JSR BTL_SOUND_SELECT
    DEC $0449,X     ; 選択したアイテムのカーソル位置(縦)
    DEC $0441,X     ; 選択したアイテムの位置
    DEC $0441,X     ; 選択したアイテムの位置

.ret
    RTS

.next
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    BNE .scroll_up

    LDA $CFC3       ; (「アイテム」以外では武器欄は無効)
    BNE .ret

.move_to_weapon
    LDA $0445,X     ; 選択したアイテムのカーソル位置(横)
    BRA BTL_DISPLAY_WEAPON

.scroll_up
    JSR BTL_SOUND_SELECT
    DEC $0441,X     ; 選択したアイテムの位置
    DEC $0441,X     ; 選択したアイテムの位置
    JSR $5DD4       ; メニューコマンドタイプ No.007(07): アイテム: 上スクロ
                    ; ール
    JMP BTL_SCROLL_UP

;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: 下
;--------------------------------
BTL_ITEM_INPUT_DOWN:
    LDA $0449,X     ; 選択したアイテムのカーソル位置(縦)
    CMP #$03
    BEQ .next

    JSR BTL_SOUND_SELECT
    INC $0441,X     ; 選択したアイテムの位置
    INC $0441,X     ; 選択したアイテムの位置
    INC $0449,X     ; 選択したアイテムのカーソル位置(縦)

.ret
    RTS

.next
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    CMP #$7C
    BEQ .ret

.scroll_down
    JSR BTL_SOUND_SELECT
    INC $0441,X     ; 選択したアイテムの位置
    INC $0441,X     ; 選択したアイテムの位置
    JSR $5DEA       ; メニューコマンドタイプ No.007(07): アイテム: 下スクロ
                    ; ール
    JMP BTL_SCROLL_DOWN

;--------------------------------
; 実行する行動の種類をセットする | 項目を非選択にする | カーソルを非表示にす
; る
;--------------------------------
; /* org $C15DC2 */
BTL_USE_ITEM_WEAPON:
    PHA
    LDA $F890       ; 行動指定オフセット (0: 1回目, 7: 2回目)
    TAX
    PLA
    ORA $F891       ; アイテム/魔法の選択回数 (0: 1回, 8: 2回)
    STA $41B1,X     ; 実行する行動の種類
    STZ $CD48       ; カーソルを表示する (1: ON, 0: OFF)
    JMP $5B93       ; 項目を非選択にする

; /* End of BTL_core implementation */

; /* Start of LR implementation */

;--------------------------------
; LR 入力で使用するカーソル移動処理
;--------------------------------
org $C2A230
;--------------------------------
; LR 入力は失敗である
;--------------------------------
LR_DISABLE equ INPUT_WAIT   ; is used for $D0FFA0
LR_FAILURE equ INPUT_WAIT
;--------------------------------
; LR 入力後、サウンドを再生してキー入力を待つ
;--------------------------------
LR_RETURN:
    JSR LR_SOUND
    JMP INPUT_WAIT
;--------------------------------
; LR 入力後、カーソルを更新してキー入力を待つ
;--------------------------------
LR_RELOAD:
    LDA $53         ; カーソルインデックス
    JMP INPUT_MOVE

;--------------------------------
; キー入力タイプ No.009(09): LR 入力 [27 bytes]
;--------------------------------
org INPUT_LR
    LDA $54         ; メニュー番号
    REP #$20
    AND #$00FF
    CMP #$001F      ; #$001F = "コンフィグ/短縮"
    BCC .lr_enable

    LDA $8E         ; メニュー番号 0x1F 以上は LR 無効

.lr_enable
    ASL
    TAX
    LDA $D0FFA0,X
    STA $C7
    SEP #$20
    JMP ($01C7)

;--------------------------------
; LR 入力で使用するアドレステーブル [62 bytes]
;--------------------------------
org $D0FFA0
    dw LR_DISABLE       ; 00: (none)
    dw LR_DISABLE       ; 01: メイン
    dw LR_DISABLE       ; 02: メイン/隊列変更
    dw LR_DISABLE       ; 03: メイン/キャラクタ選択
    dw LR_ABT_MAIN      ; 04: アビリティ
    dw LR_ABT_SELECT    ; 05: アビリティ/変更
    dw LR_JOB_MAIN      ; 06: ジョブ
    dw LR_EQUIP_MAIN    ; 07: 装備/装備選択
    dw LR_EQUIP_MAIN    ; 08: 装備
    dw LR_EQUIP_SELECT  ; 09: 装備/アイテム選択
    dw LR_STATUS        ; 0A: ステータス
    dw LR_DISABLE       ; 0B: 店
    dw LR_DISABLE       ; 0C: 店/購入
    dw LR_DISABLE       ; 0D: 店/購入/個数選択
    dw LR_DISABLE       ; 0E: 魔法屋/購入
    dw LR_DISABLE       ; 0F: アイテム
    dw LR_ITEM_SELECT   ; 10: アイテム/アイテム選択
    dw LR_DISABLE       ; 11: (unused)
    dw LR_MAGIC_MAIN    ; 12: 魔法
    dw LR_MAGIC_SELECT  ; 13: 魔法/白魔法,黒魔法,時空,召喚,魔法剣
    dw LR_MAGIC_SELECT  ; 14: 魔法/青魔法
    dw LR_MAGIC_SELECT  ; 15: 魔法/歌
    dw LR_SHOP_SELL     ; 16: 店/売却
    dw LR_DISABLE       ; 17: セーブ
    dw LR_NAME_MODE     ; 18: 名前設定/モード
    dw LR_NAME_MODE     ; 19: 名前設定/文字選択
    dw LR_DISABLE       ; 1A: 店/売却/個数選択
    dw LR_DISABLE       ; 1B: お宝
    dw LR_DISABLE       ; 1C: セーブ/確認
    dw LR_DISABLE       ; 1D: 魔法/使用/対象選択
    dw LR_DISABLE       ; 1E: アイテム/使用/対象選択
                        ; 1F: コンフィグ/短縮
                        ; 20: コンフィグ
                        ; 21: コンフィグ/マルチ
                        ; 22: コンフィグ/カスタム
                        ; 23: コンフィグ/短縮/選択
                        ; 24: アイテム/アイテム選択/装備確認

org $C27964
;--------------------------------
; LR 入力: ページの切り替え
;--------------------------------
; Returns:
;   $016B: スクロール位置
;
; Params:
;   X register: 移動する回数
;
; Flags Affected:
;   16-bit accum
;--------------------------------
LR_SUBR_NEXTPAGE:
    SEP #$20
    LDA $0A         ; Input Press (axlr----)
    ASL
    ASL
    ASL             ; C=1 if L button is pressed
    REP #$20
    TXA
    BCC .input_r

    EOR #$FFFF      ; L が入力されていれば $6B -= X

.input_r
    ADC $6B         ; R が入力されていれば $6B += X
    BPL .skip_low

    LDA $8E         ; $8E = 0

.skip_low
    CMP $6D         ; スクロールの上限
    BMI .skip_high

    LDA $6D         ; スクロールの上限

.skip_high
    STA $6B         ; スクロール位置
    RTS

;--------------------------------
; LR 入力: キャラクタの切り替え
;--------------------------------
; Returns:
;   $0171: 選択したキャラクタの番号
;   $017E: 自分の番号
;   $0180: 自分アドレスへのインデックス
;   X register: [$017E: 自分の番号]
;   Y register: [$0180: 自分アドレスへのインデックス]
;
; Flags Affected:
;   16-bit accum
;--------------------------------
LR_SUBR_NEXTCHR:
    SEP #$20

.next_character
    LDA $0A         ; Input Press (axlr----)
    ASL
    ASL
    ASL             ; C=1 if L button is pressed
    LDA $71         ; 選択したキャラクタの番号
    BCC .input_r

    DEC
    DEC             ; L が入力されていれば $71 -= 1

.input_r
    INC             ; R が入力されていれば $71 += 1
    AND #$03
    STA $71         ; 選択したキャラクタの番号
    STA $7E         ; 自分の番号
    STZ $7F
    JSR $D4C5       ; ($80: 自分アドレスへのインデックス) =
                    ; ($7E: 自分の番号)×80
    LDX $7E         ; 自分の番号
    LDY $80         ; 自分アドレスへのインデックス
    LDA $0500,Y     ; キャラクタ番号(bit0-3: 番号 | 20: 女性, 40: 離脱,
                    ; 80: 後列)
    AND #$40        ; #$40 = "参加していない"
    BNE .next_character

    LDA $54         ; メニュー番号
    CMP #$0A        ; #$0A = "ステータス"
    BEQ .ret        ; ステータス画面では状態異常は関係なし

    LDA $051A,Y     ; 状態変化1(永続的状態) (01: 暗闇, 02: ゾンビー,
                    ; 04: 猛毒, 08: レビテト, 10: ミニマム, 20: 蛙,
                    ; 40: 石化, 80: 戦闘不能)
    AND #$C2        ; #$C2 = "戦闘不能" | "石化" | "ゾンビー"
    BNE .next_character

    LDA $54         ; メニュー番号
    CMP #$04        ; #$04 = "アビリティ"
    BNE .ret        ; アビリティ画面では選択できるアビリティが必要

                    ; /* Sync with ff5_ability_menu.ips */
    LDA $0501,Y     ; ジョブ番号
    CMP #$14        ; #$14 = "ものまねし"
    BEQ .ret

    LDA $08F3,X     ; 覚えたアビリティの数[0]
    BEQ .next_character

.ret
    REP #$20
    RTS

;--------------------------------
; LR 入力: No.004(04): アビリティ/キャラクタの切り替え
;--------------------------------
LR_ABT_MAIN:
    LDA $2D12       ; アビリティを変更したかどうかのフラグ (1: 変更した)
    ORA $2D11       ; ジョブを変更したかどうかのフラグ (1: 変更した)
    BNE .cannot_change

    JSR LR_SUBR_NEXTCHR
    LDA #$ADF4      ; (アビリティウィンドウを消去する)
    JSR $C1B8       ; Run Menu Script
    JSR $CEEC       ; メニューコマンド No.002(02): アビリティ
    JSR $FAD4       ; OAM を更新する
    JSR $A693       ; BG2 を更新する
    JSR $A698       ; BG3 を更新する
    JSR $A69D       ; BG4 を更新する
    JMP LR_RETURN

.cannot_change
    JMP LR_FAILURE  ; ジョブ/アビリティを変更した場合は切り替えできない

;--------------------------------
; LR 入力: No.005(05): アビリティ/アビリティ欄をスクロール
;--------------------------------
LR_ABT_SELECT:
    LDX #$000E
    JSR LR_SUBR_NEXTPAGE
    JSR $D837       ; 選択できるアビリティの表示を更新する
    JSR $E367       ; スクロールバーの表示を更新する
    JSR $A69D       ; BG4 を更新する
    JMP LR_RELOAD

;--------------------------------
; LR 入力: No.006(06): ジョブ/キャラクタの切り替え
;--------------------------------
LR_JOB_MAIN:
    LDA $6F         ; 選択したジョブ
    BNE .cannot_change

    LDA $53         ; カーソルインデックス
    STA $5F         ; 最後に選択したジョブの位置
    JSR LR_SUBR_NEXTCHR
    JSR $A16E       ; OAM を初期化する (-> ジョブマスターの星を消去する)
    JSR $CCCB       ; メニューコマンド No.003(03): ジョブ選択
    JSR REDRAW_JOBS
    JSR REDRAW_JOBS_HIGHLIGHT
    JSR $FAD4       ; OAM を更新する
    JSR $FAF0       ; CG を更新する
    JSR $A698       ; BG3 を更新する
    JMP LR_RELOAD

.cannot_change
    JMP LR_FAILURE  ; ジョブを選択中は切り替えできない

;--------------------------------
; LR 入力: No.007(07): 装備/キャラクタの切り替え
;--------------------------------
LR_EQUIP_MAIN:
    LDA $53         ; カーソルインデックス
    STA $5E         ; 最後に選択した装備の位置
    JSR LR_SUBR_NEXTCHR
    LDA #$5000      ; #$5000 = "BG3"
    STA $E6         ; Menu Script Destination
    LDA #$AF4D      ; ("[みぎて/ひだりて][りょうてもち/にとうりゅう]" および
                    ; 装備、装備できるアイテム、能力値を消去する)
    JSR $C1B8       ; Run Menu Script
    JSR $CA37       ; メニューコマンド No.004(04): 装備変更
    JSR $A693       ; BG2 を更新する
    JSR $A698       ; BG3 を更新する
    JMP LR_RETURN

;--------------------------------
; LR 入力: No.009(09): 装備/アイテム欄をスクロール
;--------------------------------
LR_EQUIP_SELECT:
    LDX #$0009
    JSR LR_SUBR_NEXTPAGE
    JSR UPDATE_EQUIP_LIST
    JSR $E367       ; スクロールバーの表示を更新する
    JSR $A69D       ; BG4 を更新する
    JMP LR_RELOAD

;--------------------------------
; LR 入力: No.010(0A): ステータス/キャラクタの切り替え
;--------------------------------
LR_STATUS:
    JSR LR_SUBR_NEXTCHR
    JSR LR_SOUND
    JMP $B828       ; メニューコマンド No.005(05): ステータス: 決定

;--------------------------------
; LR 入力: No.016(10): アイテム/アイテム欄をスクロール
;--------------------------------
LR_ITEM_SELECT:
    JSR $C0E2       ; 選択済みカーソルを消去する

;--------------------------------
; LR 入力: No.022(16): 店/売却/アイテム欄をスクロール
;--------------------------------
LR_SHOP_SELL:
    LDX #$0016
    JSR LR_SUBR_NEXTPAGE
    JSR $AC0E       ; アイテム欄の表示を更新する
    JMP LR_RELOAD

;--------------------------------
; LR 入力: No.018(12): 魔法/キャラクタの切り替え
;--------------------------------
LR_MAGIC_MAIN:
    JSR LR_SUBR_NEXTCHR
    JSR SETCONF_USED_MAGIC
    JSR $C5C8       ; メニューコマンド No.008(08): 魔法
    JSR $FAD4       ; OAM を更新する
    JSR $A698       ; BG3 を更新する
    JMP LR_RETURN

;--------------------------------
; LR 入力: No.019(13): 魔法/白魔法,黒魔法,時空,召喚,魔法剣/種類の切り替え
; LR 入力: No.020(14): 魔法/青魔法/種類の切り替え
; LR 入力: No.021(15): 魔法/歌/種類の切り替え
;--------------------------------
LR_MAGIC_SELECT:
    LDA $0A         ; Input Press (axlr----)
    ASL
    ASL
    ASL
    LDX $7E         ; 自分のキャラクタ
    LDA $63,X       ; 選択した魔法の種類(1番目のキャラクタ)
    BCC .input_r

    DEC
    DEC             ; L が入力されていれば $63,X -= 1

.input_r
    INC             ; R が入力されていれば $63,X -= 1
    BPL .skip_low

    LDA #$06        ; #$06 = "うた"

.skip_low
    CMP #$07
    BCC .skip_high

    LDA #$00        ; #$00 = "しろまほう"

.skip_high
    STA $53         ; カーソルインデックス
    STA $63,X       ; 選択した魔法の種類(1番目のキャラクタ)
    LDA #$07        ; #$07 = "1 番目の魔法"
    STA $67,X       ; 選択した魔法の位置(1番目のキャラクタ)
    LDA #$12        ; #$12 = "魔法"
    STA $54         ; メニュー番号を変更することで強制的に [12: 魔法] から切
                    ; り替えたものとして扱う
    JSR $E4DF       ; Xレジスタ = ($53: 8bit)×8
    LDA $7601,X
    JMP UPDATE_MAGIC_LIST

;--------------------------------
; LR 入力: No.025(19): 名前設定/ひらがな/カタカナの切り替え
;--------------------------------
LR_NAME_MODE:
    LDA $2B65       ; ひらがな/カタカナの切り替え (0: カタカナ, 1: ひらがな)
    EOR #$01
    STA $2B65       ; ひらがな/カタカナの切り替え (0: カタカナ, 1: ひらがな)
    JSR $C4DA       ; 文字一覧の表示を更新する
    JSR $A69D       ; BG4 を更新する
    JMP LR_RETURN

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP

; /* End of LR implementation */

; /* Start of BTL_LR implementation */

org $C15EE0
;--------------------------------
; メニューコマンドタイプ No.007(07): アイテム: LR 入力
;--------------------------------
BTL_ITEM_INPUT_LR:
    LDY #$0004
    AND #$20        ; #$20 = "L"
    BEQ .input_r

.input_l
    JSR BTL_LR_ITEM_SCROLL_UP
    CPY #$0004
    BNE .lr_success

    LDA $CFC3       ; (「アイテム」以外では武器欄は無効)
    BNE .lr_failure

.select_weapon
    STZ $0449,X     ; 選択したアイテムのカーソル位置(縦)
    LDA $0445,X     ; 選択したアイテムのカーソル位置(横)
    STA $0441,X     ; 選択したアイテムの位置
    JMP BTL_DISPLAY_WEAPON

.input_r
    JSR BTL_LR_ITEM_SCROLL_DOWN
    CPY #$0004
    BEQ .lr_failure

.lr_success
    LDA #$19        ; #$19 = "アイテム欄の表示を更新する"
    STA $CD39       ; メニューコントロール
    JMP BTL_LR_SOUND

.lr_failure
    RTS

org $C15705
;--------------------------------
; メニューコマンドタイプ No.011(0B): 魔法: LR 入力
;--------------------------------
BTL_MAGIC_INPUT_LR:
    LDX #$0004
    AND #$20        ; #$20 = "L"
    BEQ .input_r

.input_l
    JSR BTL_LR_MAGIC_SCROLL_UP
    CPX #$0004
    BNE .lr_success

    BRA .lr_failure

.input_r
    JSR BTL_LR_MAGIC_SCROLL_DOWN
    CPX #$0004
    BEQ .lr_failure

.lr_success
    CLC
    LDA #$1B        ; #$1B = "魔法欄の表示を更新する"
    ADC $CF         ; 魔法の種類 (0: 通常, 1: 歌/青魔法)
    STA $CD39       ; メニューコントロール
    JMP BTL_LR_SOUND

.lr_failure
    RTS

org $C15C5A
;--------------------------------
; LR 入力: アイテム欄をスクロール: UP
;--------------------------------
; Returns:
;   $0441,X: 選択したアイテムの位置
;   $044D,X: 選択したアイテムのスクロール位置
;   Y register: 移動不可回数
;
; Params:
;   Y register: 移動する回数
;--------------------------------
BTL_LR_ITEM_SCROLL_UP:
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    BEQ .break

    DEC $0441,X     ; 選択したアイテムの位置
    DEC $0441,X     ; 選択したアイテムの位置
    DEC $044D,X     ; 選択したアイテムのスクロール位置
    CLC
    JSR BTL_SCROLL_MOVECURSOR_TRIPLE
    DEY
    BNE BTL_LR_ITEM_SCROLL_UP

.break
    RTS

;--------------------------------
; LR 入力: アイテム欄をスクロール: DOWN
;--------------------------------
; Returns:
;   $0441,X: 選択したアイテムの位置
;   $044D,X: 選択したアイテムのスクロール位置
;   Y register: 移動不可回数
;
; Params:
;   Y register: 移動する回数
;--------------------------------
BTL_LR_ITEM_SCROLL_DOWN:
    LDA $044D,X     ; 選択したアイテムのスクロール位置
    CMP #$7C
    BEQ .break

    INC $0441,X     ; 選択したアイテムの位置
    INC $0441,X     ; 選択したアイテムの位置
    INC $044D,X     ; 選択したアイテムのスクロール位置
    SEC
    JSR BTL_SCROLL_MOVECURSOR_TRIPLE
    DEY
    BNE BTL_LR_ITEM_SCROLL_DOWN

.break
    RTS

org $C15705+$25
;--------------------------------
; LR 入力: 魔法欄をスクロール: UP
;--------------------------------
; Returns:
;   ($D3),Y: 選択した魔法の位置
;   ($D9),Y: 選択した魔法のスクロール位置
;   X register: 移動不可回数
;
; Params:
;   X register: 移動する回数
;--------------------------------
BTL_LR_MAGIC_SCROLL_UP:
    LDA ($D9),Y     ; 選択した魔法のスクロール位置
    BEQ .break

    DEC
    STA ($D9),Y     ; 選択した魔法のスクロール位置
    LDA ($D3),Y     ; 選択した魔法の位置
    SEC
    SBC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    DEX
    BNE BTL_LR_MAGIC_SCROLL_UP

.break
    RTS

;--------------------------------
; LR 入力: 魔法欄をスクロール: DOWN
;--------------------------------
; Returns:
;   ($D3),Y: 選択した魔法の位置
;   ($D9),Y: 選択した魔法のスクロール位置
;   X register: 移動不可回数
;
; Params:
;   X register: 移動する回数
;--------------------------------
BTL_LR_MAGIC_SCROLL_DOWN:
    LDA ($D9),Y     ; 選択した魔法のスクロール位置
    CMP $DD         ; 魔法リスト: スクロールの上限
    BEQ .break

    INC
    STA ($D9),Y     ; 選択した魔法のスクロール位置
    LDA ($D3),Y     ; 選択した魔法の位置
    CLC
    ADC $D2         ; 魔法リスト: オフセット
    STA ($D3),Y     ; 選択した魔法の位置
    DEX
    BNE BTL_LR_MAGIC_SCROLL_DOWN

.break
    RTS

; /* End of BTL_LR implementation */

; /* Start of bug fix */

;--------------------------------
; 青魔法のカーソル位置が正しく設定されない不具合を修正
;--------------------------------
org $C2ADC8
    JSR INIT_BLUE_MAGIC_CURSOR_POSITION

;--------------------------------
; 青魔法の LR 切り替え時に画面がちらつく不具合を修正
;--------------------------------
org $C2ADBC
    JSR $A69D       ; BG4 を更新する
    LDX #$B8EC      ; $07, $04, $0C, $0C, $2C, $04, $0C, $0C, $0C, $0C, $0C,
                    ; $0C, $0C, $0C, $0C, 14, $00
    LDY #$7180      ; #$7180 = "BG4"
    JSR $C1FD       ; Configure the Line Position

;--------------------------------
; 青魔法の終了時に画面がちらつく不具合を修正
;--------------------------------
org $C2ADD2
    JSR $A69D       ; BG4 を更新する
    LDX #$B8E6      ; $07, $04, $0C, $0C, $04, $00
    LDY #$7180      ; #$7180 = "BG4"
    JSR $C1FD       ; Configure the Line Position

;--------------------------------
; アイテム欄の表示を更新しても選択したアイテムの位置を初期化しないように修正
;--------------------------------
org $C2C7C6
    NOP             ; <- STZ $6F
    NOP

;--------------------------------
; キャラクタの切り替えで暗闇状態のパーツが残る不具合を修正
;--------------------------------
org $C2C921
    BEQ $C923       ; <- BEQ $C93D

;--------------------------------
; カスタムの設定を B ボタンで終了できるように変更
;--------------------------------
org $C2C0BD
    JMP $C07A       ; メニューコマンド No.009(09): コンフィグ: カスタム:
                    ; 決定(おわり)

;--------------------------------
; 短縮コマンドの設定で 1 番目のコマンドを最初に選択するように修正
;--------------------------------
org $C2C014
    ADC #$0020      ; <- ADC #$0021

;--------------------------------
; 短縮コマンドの設定で同じコマンドを選択しても非選択にならない不具合を修正
;--------------------------------
org $C2C110
    BEQ $C155       ; <- BEQ $C109

;--------------------------------
; 短縮コマンドの設定でキャラクタが状態異常にかかっているとジョブの名前が表示
; されない不具合を修正
;--------------------------------
org $C0EA08
    dw %00000000101 ; <- dw %00000000011

;--------------------------------
; 短縮コマンドの設定でキャラクタの選択が上下ループするように変更
;--------------------------------
org $C3AB2F
    db $1F          ; <- db $1E
org $C3AB36
    db $1E          ; <- db $1F

;--------------------------------
; 短縮コマンドの設定でカーソルが表示されたままになる不具合を修正
;--------------------------------
org $C2B0A5
    JSR $C0E2       ; 選択済みカーソルを消去する

;--------------------------------
; テント/コテージの使用時にカーソル位置が記憶されない不具合を修正
;--------------------------------
org $C2BB90
    BIT $44         ; フラグ (02: テレポできる, 80: セーブできる)
    BPL $BBEB       ; セーブできなければテント/コテージは使用不可

    STA $39         ; テント/コテージ/テレポを使用した (3E: テレポ,
                    ; F0: テント, F1: コテージ)
    STZ $3A
    LDA #$01
    XBA
    LDA $29E7
    JSR $E328       ; アイテムを減らす (AL: 種類, AH: 個数)
    JSR SETCONF_USED_ITEM
    JMP $A02D       ; メニュー処理を終了する

    NOP
    NOP
    NOP
    NOP
    NOP

;--------------------------------
; 短縮コマンドの設定でキャラクタが戦闘不能になっているとすっぴんのパレットが
; 使用される不具合を修正
;--------------------------------
org $C2C361
    JSR UPDATE_CHARACTER_CG

;--------------------------------
; 召喚獣アイテムの使用後にアイテムの説明が更新されない不具合を修正
;--------------------------------
org $C2BB66
    PHA
    ORA #$0100
    JSR $E328       ; アイテムを減らす (AL: 種類, AH: 個数)
    PLX
    LDA $C0EEAE-$00F8,X ; $4D, $4C, $50, $4F
    JSR $F00B       ; Aレジスタの魔法を覚えた魔法に追加する
    LDA $C0EEB2-$00F8,X ; $76, $44, $47, $4B
    JSR SOUND_GET
    JSR $C7BD       ; アイテム欄を再読込する
    JSR $AC5E       ; アイテムの説明を表示する
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    JSR $A698       ; BG3 を更新する
    JSR $A69D       ; BG4 を更新する
    BRA $BBEB

; /* End of bug fix */
