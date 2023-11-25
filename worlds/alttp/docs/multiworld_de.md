# A Link to the Past Randomizer Setup Guide

## Benötigte Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [SNI](https://github.com/alttpo/sni/releases) (Integriert in Archipelago)
- Hardware oder Software zum Laden und Abspielen von SNES Rom-Dateien fähig zu einer Internetverbindung
    - Ein Emulator, der mit SNI verbinden kann
      ([snes9x rr](https://github.com/gocha/snes9x-rr/releases),
      [BizHawk](https://tasvideos.org/BizHawk))
    - Ein SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), oder andere kompatible Hardware
- Die Japanische Zelda 1.0 ROM-Datei, mit folgendem Namen: `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Installation Schritt für Schritt

### Windows

1. Lade die Multiworld Utilities herunter und führe die Installation aus. Sei sicher, dass du immer die aktuellste
   Version installiert hast.**Die Datei befindet sich im "assets"-Kasten unter der jeweiligen Versionsinfo!**. Für
   normale Multiworld-Spiele lädst du die `Setup.Archipelago.exe` herunter.
    - Für den Doorrandomizer muss die alternative doors-Variante geladen werden.
    - Während der Installation fragt dich das Programm nach der japanischen 1.0 ROM-Datei. Wenn du die Software bereits
      installiert hast und einfach nur updaten willst, wirst du nicht nochmal danach gefragt.
    - Es kann auch sein,dass der Installer Microsoft Visual C++ installieren möchte. Wenn du das bereits installiert
      hast (durch Steam oder andere Programme), wirst du nicht nochmal danach gefragt.

2. Wenn du einen Emulator benutzt, so ist es sinnvoll, ihn als Standard zum Abspielen für .sfc-dateien einzustellen.
    1. Entpacke oder Installiere deinen Emulator(-Ordner) an einen Ort, den du auch wiederfindest
    2. Rechtsklicke auf eine .sfc-Datei und wähle **Öffnen mit...**
    3. Mache einen Haken in die Box bei **Immer diese App zum Öffnen von .sfc Dateien benutzen **.
    4. Scrolle zum Ende und wähle **Weitere Apps** und nochmal am Ende **Andere App auf diesem PC suchen** auswählen.
    5. Suche nach der .exe-Datei des Emulators deiner Wahl und wähle **Öffnen**. Diese Datei befindet sich dort, wo den
       Emulator in Schritt 1 enpackt/installiert hast.

### Macintosh

- Es werden freiwillige Helfer gesucht! Meldet euch doch bei **Farrak Kilhn** auf Discord, wenn ihr helfen wollt!

## Erstellen deiner YAML-Datei

### Was ist eine YAML-Datei und wofür brauche ich die?

Deine persönliche YAML-Datei beinhaltet eine Reihe von Einstellungen, die der Zufallsgenerator zum Erstellen von deinem
Spiel benötigt. Jeder Spieler einer Multiworld stellt seine eigene YAML-Datei zur Verfügung. Dadurch kann jeder Spieler
sein Spiel nach seinem eigenen Geschmack gestalten, während andere Spieler unabhängig davon ihre eigenen Einstellungen
wählen können!

### Wo bekomme ich so eine YAML-Datei her?

Die [Player Settings](/games/A Link to the Past/player-settings) Seite auf der Website ermöglicht das einfache Erstellen
und Herunterladen deiner eigenen `yaml` Datei. Drei verschiedene Voreinstellungen können dort gespeichert werden.

### Deine YAML-Datei ist gewichtet!

Die **Player Settings** Seite hat eine Menge Optionen, die man per Schieber einstellen kann. Das ermöglicht es,
verschiedene Optionen mit unterschiedlichen Wahrscheinlichkeiten in einer Kategorie ausgewürfelt zu werden

Als Beispiel kann man sich die Option "Map Shuffle" als einen Eimer mit Zetteln zur Abstimmung Vorstellen. So kann man
beispielsweise für die Option "On" 20 Zettel mit dieser Option einwerfen und 40 Zettel mit "Off".

Entsprechend in diesem Beispiel liegen dann 60 Zettel im Eimer. 20 für "On" und 40 für "Off". Um die Option
festzulegen, "greift" der Generator in den Eimer und holt sich zufällig einen Zettel heraus. Entsprechend ist die
Wahrscheinlichkeit für "Off" bei einem Map Shuffle höher, als "On"

Wenn du eine Option nicht gewählt haben möchtest, setze ihren Wert einfach auf Null.
(Es muss aber mindestens eine Option pro Kategorie einen Wert größer Null besitzen, sonst funktioniert die yaml nicht!)

### Überprüfung deiner YAML-Datei

Wenn man sichergehen will, ob die YAML-Datei funktioniert, kann man dies bei der [YAML Validator](/check) Seite
tun.

## ein Einzelspielerspiel erstellen

1. Navigiere zur [Generator Seite](/generate) und lade dort deine YAML-Datei hoch.
2. Dir wird eine "Seed Info"-Seite angezeigt, wo du deine Patch-Datei herunterladen kannst.
3. Doppelklicke die Patchdatei und der Emulator sollte nach kurzer Verzögerung mit dem gepatchten Rom starten. Der
   Client ist soweit unnötig für Einzelspielerspiele, also kannst diesen und das WebUI einfach schließen.

## Einem MultiWorld-Spiel beitreten

### Erhalte deine Patch-Datei und erstelle dein ROM

Wenn du an einem MultiWorld-Spiel teilnehmen möchtest, wirst du in der Regel vom Host nach deiner YAML-Datei gefragt.
Sobald du diese weitergegeben hast, wird der Host einen Link bereitstellen, wo du deinen Patch oder eine .zip-Datei mit
allen Patches herunterladen kannst. Die Patch-Datei hat immer die Endung `.aplttp`.

### Mit dem Client verbinden

#### Via Emulator

Wenn der client den Emulator automatisch gestartet hat, wird SNI ebenfalls im Hintergrund gestartet. Wenn dies das erste
Mal ist, wird möglicherweise ein Fenster angezeigt, wo man bestätigen muss, dass das Programm durch die Windows Firewall
kommunizieren darf.

##### snes9x-rr

1. Lade die Entsprechende ROM-Datei, wenn sie nicht schon automatisch geladen wurde.
2. Klicke auf den Reiter "File" oben im Menü und wähle **Lua Scripting**
3. Klicke auf **New Lua Script Window...**
4. Im sich neu öffnenden Fenster, klicke auf **Browse...**
5. Navigiere zum Verzeichnis, wo du Archipelago installiert hast und dort in den Unterordner `SNI`.
6. Wähle dort die `Connector.lua` und klicke auf Öffnen.
7. Schaue im Lua-Fenster nach einem Namen, der dir zugeteilt wird und schaue im Client (WebUI im Browser), ob dort
   "Snes Device: Connected" mit demselben Namen dort steht (in der oberen linken Ecke).

##### BizHawk

1. Stelle sicher, dass der BSNES-Core in BizHawk geladen wird. Dazu musst du auf das Tools-Menü in BizHawk klicken und
   folgende Optionen wählen:
   `Config --> Cores --> SNES --> BSNES`
2. Lade die entsprechende ROM-Datei, wenn sie nicht schon automatisch geladen wurde.
3. Klicke auf das Tools-Menü und klicke auf **Lua Console**
4. Klicke auf den Button um ein neues Lua-Script zu öffnen.
5. Navigiere zum Verzeichnis, wo du Archipelago installiert hast und dort in den Unterordner `SNI`.
6. Wähle dort die `Connector.lua` und klicke auf Öffnen.
7. Schaue im Lua-Fenster nach einem Namen, der dir zugeteilt wird und schaue im Client (WebUI im Browser), ob dort
   "Snes Device: Connected" mit demselben Namen dort steht (in der oberen linken Ecke)

#### Mit (Original-)Hardware

Dieser Guide setzt voraus, dass du schon die entsprechende Firmware für dein Gerät heruntergeladen hast! Wenn du das
noch nicht getan hast, so tue dies am besten jetzt! SD2SNES und FXPak Pro Nutzer finden die passende Firmware
[hier](https://github.com/RedGuyyyy/sd2snes/releases). Nutzer ähnlicher Hardware finden Hilfestellung
[auf dieser Seite](http://usb2snes.com/#supported-platforms).

1. Schließe deinen Emulator, falls er automatisch gestartet haben sollte.
2. Start SNI
3. Starte deine (Original-)Konsole und lade die ROM-Datei.
4. Schaue auf dein Clientfenster, welches nun "Snes Device: Connected" und den namen deiner Konsole zeigen sollte.

### Mit dem MultiServer verbinden

Die Patch-Datei, welche auch den Client gestartet hat, sollte dich automatisch mit dem MultiServer verbunden haben.
Manchmal ist dies nicht der Fall, auch wenn das Spiel auf der Webseite gehostet wird, aber woanders erstellt wurde. Wenn
die WebUI vom Client "Server Status: Not Connected" zeigt, frag deinen Host nach der passenden Adresse und trage sie
einfach in das Textfeld neben "Server" ein und drücke Enter.

Der Client wird versuchen auf die neue Adresse zu verbinden und nach einer Weile "Server Status: Connected" zeigen.
Sollte nach einer Weile der Client sich nicht verbunden haben, lade die Seite neu.

### Spiele das Spiel!

Wenn der Client anzeigt, dass sowohl das SNES-Gerät (oder Emulator) und der Server verbunden sind, können du und deine
Freunde loslegen! Glückwunsch zum erfolgreichen Beitritt zu einem Multiworld-Spiel ;)

## Ein Multiworld-Spiel hosten

Die Empfohlene Art, ein Spiel zu hosten, ist, den Service auf
[der website](/generate) zu nutzen. Das Ganze ist recht einfach:

1. Lasse dir von deinen Mitspielern die YAML-Datei zuschicken.
2. Erstelle einen Zip-komprimierten Ordner´, in den du alle YAML-Dateien deiner Spieler einfügst.
3. Lade diesen Zip-Ordner auf der oben genannten Website hoch.
4. Warte einen Moment, wenn das Spiel erstellt wird.
5. Wenn das Spiel erstellt wurde, wirst du auf eine "Seed Info"-Seite weitergeleitet.
6. Klicke auf "Create New Room". Du wirst auf die Serverseite gebracht. Gib diesen Link deinen Mitspielern, sodass sie
   ihre Patch-Dateien von dort herunterladen können.
   **Anmerkung:** Die Patch-Dateien von dieser Seite ermöglichen es den Spielern, automatisch auf den Server zu
   verbinden. Die Patch-Dateien von der "Seed Info"-Seite tun dies nicht!
7. Oben auf der Serverseite ist ein Link zum MultiWorld-Tracker zum aktuellen Spiel zu finden. Gib diesen Link ebenfalls
   deinen Mitspielern, so dass ihr alle den Fortschritt eures Spiels verfolgen könnt! Ihr könnt ihn auch an Zuschauer
   weitergeben, so dass sie auf dem Laufenden bleiben.
8. Wenn alle Spieler verbunden sind, könnt ihr mit dem Spiel loslegen! Viel Spaß!
