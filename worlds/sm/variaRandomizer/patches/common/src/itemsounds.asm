;Removes all item sound clips, and replaces them with sound FX that don't interupt the BG music (you can still play the usual sound clip if you wish) 

;Uses free space from $26FD3 to $27023 ($51/81 bytes)
;Made by Sadiztyk Fish

lorom

;--------------------------------SOUNDFX VALUES----------------------------------

!None = $02			;Stops current sounds (use for no sound)
!Missile = $03			;Sound when firing a missile
!Super = $04			;Sound when firing a super missile
!Power = $01			;Sound when a powerbomb explodes
!Click = $37			;Sound when selecting a HUD item
!SpazerShield = $26		;Spazer Shield sound
!PlasmaShield = $27		;Plasma Shield sound
!WaveShield = $28		;Wave Shield sound (doesn't stop)
!IceShield = $24		;Ice Shield sound
!Grapple = $05			;Grapple fire sound
!Crumble = $3D			;Crumble block sound
!Toggle = $38			;Sound when you toggle on/off items on status screen
!Helmet = $2A			;Sound when you select a save
!Flip = $2F			;Sound when you spin underwater
!Save = $2E			;Clip when you save the game
!Hurt = $35			;Samus hurt sound

;--------------------------------SPECIALFX VALUES--------------------------------

!Energy = $01			;Sound when picking up dropped energy
!Refill = $05			;Sound when picking up dropped missiles/bombs
!Bomb = $07			;Regular Bomb explosion
!Enemy = $09			;Enemy vaporising sound (when they die)
!Screw = $0B			;Enemy explode sound (from Screw Attack)
!Splash = $0D			;Water splash, or possibly an enemy sound?
!Bubble = $0F			;A bubble sound (from lava or being underwater)
!Beep = $16			;A weird beep. I don't recognise it
!Hum = $18			;Humming of the ship
!Statue = $19			;Releasing the Statue Spirits
!Quake = $1B			;Earthquake rumble
!Chozo = $1C			;I *think* it's when the Chozo grabs you, but not sure
!Dachora = $1D			;The bird is the word =P
!Skree = $21			;Skreeeee
!Explode = $25			;Some kind of explosion, but I can't think what. Sounds cool anyway
!Laser = $26			;A fucking awesome laser sound =D Possibly from MB
!Suit = $56			;Sound when you 'don a suit' =P

;Many more values for enemy sounds. Some are song-dependent

;--------------------------------MISCFX VALUES--------------------------------

!Land = $04			;Landing sound
!DoorO = $07			;A door opening
!DoorC = $08			;A door closing
!ShipO = $14			;Ship hatch opening
!ShipC = $15			;Ship hatch closing
!CeresO = $2C			;Ceres hatch opening
!Buzz = $09			;A cool buzz. Might be related to Grapple?
!Freeze = $0A			;enemy is frozen
!Text = $0D			;Text sound from the intro
!Gate = $0E			;A gate moving
!Spark = $0F			;Shinespark sound
!ExplodeA = $10			;Another explosion sound
!Lava = $11			;Sound of rising lava
!WTF = $16			;Sounds like a gunshot?
!Pirate = $17			;Pirate laser?
!LaserA = $1C			;A short laser
!Fire = $1D			;Sounds like a Norfair fire explosion thing
!Spin = $21			;Single spin jump sound
!BubbleA = $22			;3 bubbles
!Acid = $2D			;Hurt by acid/lava

;30+ Nothing or crash from what I checked. There were also some that sounded song-dependent

;--------------------------------ITEM SOUNDS-----------------------------------

;For each item, you just need to specify which type of sound, followed by which effect. Some are done as an example, so it should be easy to figure out.
;If you want to play the normal sound clip for an item, put "DW NORMAL *newline* DB $02" (or leave it black if you haven't already changed it)

org $84E0B3			;Energy Tank
	DW SPECIALFX
	DB !Energy
org $84E0D8			;Missile
	DW SOUNDFX
	DB !Click	
org $84E0FD			;Super Missile
	DW SOUNDFX
	DB !Click
org $84E122			;Powerbomb
	DW SOUNDFX
	DB !Click
org $84E14F			;Bombs
	DW SPECIALFX
	DB !Bomb
org $84E17D			;Charge Beam
	DW SPECIALFX
	DB !Laser
org $84E1AB			;Ice Beam
	DW MISCFX
	DB !Freeze
org $84E1D9			;High Jump
	DW SOUNDFX
	DB !Helmet
org $84E207			;Speed Booster
	DW MISCFX
	DB !Spark
org $84E235			;Wave Beam
	DW SPECIALFX
	DB !Laser
org $84E263			;Spazer Beam
	DW SPECIALFX
	DB !Laser
org $84E291			;Spring Ball
	DW MISCFX
	DB !Land
org $84E2C3			;Varia Suit
	DW SOUNDFX
	DB !None
org $84E2F8			;Gravity Suit
	DW SPECIALFX
	DB !Bubble
org $84E32D			;X-ray
	DW SOUNDFX
	DB !Click
org $84E35A			;Plasma Beam
	DW SPECIALFX
	DB !Laser
org $84E388			;Grapple Beam
	DW SOUNDFX
	DB !Click
org $84E3B5			;Space Jump
	DW SOUNDFX
	DB !Helmet	
org $84E3E3			;Screw Attack
	DW SPECIALFX
	DB !Screw	
org $84E411			;Morph Ball
	DW SOUNDFX
	DB !None
org $84E43F			;Reserve Tank
	DW SPECIALFX
	DB !Energy
org $84E46F			;Chozo Energy Tank
	DW SPECIALFX
	DB !Energy
org $84E4A1			;Chozo Missile
	DW SOUNDFX
	DB !Click
org $84E4D3			;Chozo Super Missile
	DW SOUNDFX
	DB !Click
org $84E505			;Chozo Powerbomb
	DW SOUNDFX
	DB !Click
org $84E53F			;Chozo Bombs
	DW SPECIALFX
	DB !Bomb
org $84E57A			;Chozo Charge Beam
	DW SPECIALFX
	DB !Laser
org $84E5B5			;Chozo Ice Beam
	DW MISCFX
	DB !Freeze
org $84E5F0			;Chozo High Jump
	DW SOUNDFX
	DB !Helmet
org $84E62B			;Chozo Speed Booster
	DW MISCFX
	DB !Spark
org $84E66F			;Chozo Wave Beam
	DW SPECIALFX
	DB !Laser
org $84E6AA			;Chozo Spazer Beam
	DW SPECIALFX
	DB !Laser
org $84E6E5			;Chozo Spring Ball
	DW MISCFX
	DB !Land
org $84E720			;Chozo Varia Suit
	DW SOUNDFX
	DB !None
org $84E762			;Chozo Gravity Suit
	DW SPECIALFX
	DB !Bubble
org $84E7A4			;Chozo X-ray
	DW SOUNDFX
	DB !Click	
org $84E7DE			;Chozo Plasma Beam
	DW SPECIALFX
	DB !Laser
org $84E819			;Chozo Grapple Beam
	DW SOUNDFX
	DB !Click
org $84E853			;Chozo Space Jump
	DW SOUNDFX
	DB !Helmet
org $84E88E			;Chozo Screw Attack
	DW SPECIALFX
	DB !Screw
org $84E8C9			;Chozo Morph Ball
	DW SOUNDFX
	DB !None
org $84E904			;Chozo Reserve Tank
	DW SPECIALFX
	DB !Energy
org $84E93A			;Scenery Energy Tank
	DW SPECIALFX
	DB !Energy
org $84E972			;Scenery Missile
	DW SOUNDFX
	DB !Click
org $84E9AA			;Scenery Super Missile
	DW SOUNDFX
	DB !Click
org $84E9E2			;Scenery Powerbomb
	DW SOUNDFX
	DB !Click
org $84EA22			;Scenery Bombs
	DW SPECIALFX
	DB !Bomb
org $84EA63			;Scenery Charge Beam
	DW SPECIALFX
	DB !Laser
org $84EAA4			;Scenery Ice Beam
	DW MISCFX
	DB !Freeze
org $84EAE5			;Scenery High Jump
	DW SOUNDFX
	DB !Helmet
org $84EB26			;Scenery Speed Booster
	DW MISCFX
	DB !Spark
org $84EB67			;Scenery Wave Beam
	DW SPECIALFX
	DB !Laser
org $84EBA8			;Scenery Spazer Beam
	DW SPECIALFX
	DB !Laser
org $84EBE9			;Scenery Spring Ball
	DW MISCFX
	DB !Land
org $84EC2A			;Scenery Varia Suit
	DW SOUNDFX
	DB !None
org $84EC72			;Scenery Gravity Suit
	DW SPECIALFX
	DB !Bubble
org $84ECBA			;Scenery X-ray
	DW SOUNDFX
	DB !Click	
org $84ECFA			;Scenery Plasma Beam
	DW SPECIALFX
	DB !Laser
org $84ED3B			;Scenery Grapple Beam
	DW SOUNDFX
	DB !Click
org $84ED7B			;Scenery Space Jump
	DW SOUNDFX
	DB !Helmet
org $84EDBC			;Scenery Screw Attack
	DW SPECIALFX
	DB !Screw
org $84EDFD			;Scenery Morph Ball
	DW SOUNDFX
	DB !None	
org $84EE3E			;Scenery Reserve Tank
	DW SPECIALFX
	DB !Energy

;-------------------------DON'T EDIT THIS STUFF--------------------------

org $858491
	DW #$0020
org $82E126
	JSL CLIPCHECK
	BRA $08
org $858089
	BRA $02
org $848BF2
NORMAL:
	JSR CLIPSET

org $84EFD3			;You can safely change this address to free space in bank $84 ($20000-$27FFF)
CLIPCHECK:
	LDA $05D7
	CMP #$0002
	BEQ $0E
	LDA #$0000
	JSL $808FF7
	LDA $07F5
	JSL $808FC1
	LDA #$0000
	STA $05D7
	RTL
CLIPSET:
	LDA #$0001
	STA $05D7
	JSL $82BE17
	LDA #$0000
	RTS
SOUNDFX:
	JSR SETFX
	AND #$00FF
	JSL $809049
	RTS
SPECIALFX:
	JSR SETFX
	JSL $8090CB
	RTS
MISCFX:
	JSR SETFX
	JSL $80914D
	RTS
SETFX:
	LDA #$0002
	STA $05D7
	LDA $0000,y
	INY
	RTS
