# Setup Anleitung für Ocarina of Time: Archipelago Edition

## WICHTIG

Da wir BizHawk benutzen, gilt diese Anleitung nur für Windows und Linux.

## Benötigte Software

- BizHawk: [BizHawk Veröffentlichungen von TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 und später werden unterstützt. Version 2.10 ist empfohlen.
  - Detailierte Installtionsanweisungen für BizHawk können über den obrigen Link gefunden werden.
  - Windows-Benutzer müssen die Prerequisiten installiert haben. Diese können ebenfalls über
    den obrigen Link gefunden werden.
- Der integrierte Archipelago-Client, welcher [hier](https://github.com/ArchipelagoMW/Archipelago/releases) installiert
  werden kann.
- Eine `Ocarina of Time v1.0 US ROM`. (Nicht aus Europa und keine Master-Quest oder Debug-Rom!)

## Konfigurieren von BizHawk

Sobald Bizhawk einmal installiert wurde, öffne **EmuHawk** und ändere die folgenen Einsteluungen:

- (≤ 2.8) Gehe zu `Config > Customize`. Wechlse zu dem `Advanced`-Reiter, wechsle dann den `Lua Core` von "NLua+KopiLua" zu
  `"Lua+LuaInterface"`. Starte danach EmuHawk neu. Dies ist zwingend notwendig, damit die Lua-Scripts, mit denen man sich mit dem Client verbindet, ordnungsgemäß funktionieren.
  **ANMERKUNG: Selbst wenn "Lua+LuaInterface" bereits ausgewählt ist, wechsle zwischen den beiden Optionen umher und**
  **wähle es erneut aus. Neue Installationen oder Versionen von EmuHawk neigen dazu "Lua+LuaInterface" als die**
  **Standard-Option anzuzeigen, aber laden dennoch "NLua+KopiLua", bis dieser Schritt getan ist.**
- Unter `Config > Customize > Advanced`, gehe sicher dass der Haken bei `AutoSaveRAM` ausgeählt ist, und klicke dann
  den 5s-Knopf. Dies verringert die Wahrscheinlichkeit den Speicherfrotschritt zu verlieren, sollte der Emulator mal
  abstürzen.
- **(Optional)** Unter `Config > Customize` kannst du die Haken in den "Run in background"
  (Laufe weiter im Hintergrund) und "Accept background input" (akzeptiere Tastendruck im Hintergrund) Kästchen setzen.
  Dies erlaubt dir das Spiel im Hintergrund weiter zu spielen, selbst wenn ein anderes Fenster aktiv ist. (Nützlich bei
  mehreren oder eher großen Bildschrimen/Monitoren.)
- Unter `Config > Hotkeys` sind viele Hotkeys, die mit oft genuten Tasten belegt worden sind. Es wird empfohlen die
  meisten (oder alle) Hotkeys zu deaktivieren. Dies kann schnell mit `Esc` erledigt werden.
- Wird mit einem Kontroller gespielt, bei der Tastenbelegung (bei einem Laufendem Spiel, unter
  `Config > Controllers...`), deaktiviere "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right" und gehe stattdessen in
  den Reiter `Analog Controls` um den Stick zu belegen, da sonst Probleme beim Zielen auftreten (mit dem Bogen oder
  ähnliches). Y-Axis ist für Oben und Unten, und die X-Axis ist für Links und Rechts.
- Unter `N64` setze einen Haken bei "Use Expansion Slot" (Benutze Erweiterungs-Slot). Dies wird benötigt damit
  savestates/schnellspeichern funktioniert. (Das N64-Menü taucht nur **nach** dem laden einer N64-ROM auf.)

Es wird sehr empfohlen N64 Rom-Erweiterungen (\*.n64, \*.z64) mit dem Emuhawk - welcher zuvor installiert wurde - zu
verknüpfen.
Um dies zu tun, muss eine beliebige N64 Rom aufgefunden werden, welche in deinem Besitz ist, diese Rechtsklicken und
dann auf "Öffnen mit..." gehen. Gehe dann auf "Andere App auswählen" und suche nach deinen BizHawk-Ordner, in der
sich der Emulator befindet, und wähle dann `EmuHawk.exe` **(NICHT "DiscoHawk.exe"!)** aus.

Eine Alternative BizHawk Setup Anleitung (auf Englisch), sowie weitere Hilfe bei Problemen kann
[hier](https://wiki.ootrandomizer.com/index.php?title=Bizhawk) gefunden werden.

## Erstelle eine YAML-Datei

### Was ist eine YAML-Datei und Warum brauch ich eine?

Eine YAML-Datie enthält einen Satz an einstellbaren Optionen, die dem Generator mitteilen, wie
dein Spiel generiert werden soll. In einer Multiworld stellt jeder Spieler eine eigene YAML-Datei zur Verfügung. Dies
erlaubt jeden Spieler eine personalisierte Erfahrung nach derem Geschmack. Damit kann auch jeder Spieler in einer
Multiworld (des gleichen Spiels) völlig unterschiedliche Einstellungen haben.

Für weitere Informationen, besuche die allgemeine Anleitung zum Erstellen einer
YAML-Datei: [Archipelago Setup Anleitung](/tutorial/Archipelago/setup/en)

### Woher bekomme ich eine YAML-Datei?

Die Seite für die Spielereinstellungen auf dieser Website erlaubt es dir deine persönlichen Einstellungen nach
vorlieben zu konfigurieren und eine YAML-Datei zu exportieren.
Seite für die Spielereinstellungen:
[Seite für die Spielereinstellungen von Ocarina of Time](/games/Ocarina%20of%20Time/player-options)

### Überprüfen deiner YAML-Datei

Wenn du deine YAML-Datei überprüfen möchtest, um sicher zu gehen, dass sie funktioniert, kannst du dies auf der
YAML-Überprüfungsseite tun.
YAML-Überprüfungsseite: [YAML-Überprüfungsseite](/check)

## Beitreten einer Multiworld

### Erhalte deinen OoT-Patch

(Der folgende Prozess ist bei den meisten ROM-basierenden Spielen sehr ähnlich.)

Wenn du einer Multiworld beitrittst, wirst du gefordert eine YAML-Datei bei dem Host abzugeben. Ist dies getan,
erhälst du (in der Regel) einen Link vom Host der Multiworld. Dieser führt dich zu einem Raum, in dem alle
teilnehmenden Spieler (bzw. Welten) aufgelistet sind. Du solltest dich dann auf **deine** Welt konzentrieren
und klicke dann auf `Download APZ5 File...`.
![Screenshot of a Multiworld Room with an Ocarina of Time Player](/static/generated/docs/Ocarina%20of%20Time/MultiWorld-room_oot.png)

Führe die `.apz5`-Datei mit einem Doppelklick aus, um deinen Ocarina Of Time-Client zu starten, sowie das patchen
deiner ROM. Ist dieser Prozess fertig (kann etwas dauern), startet sich der Client und der Emulator automatisch
(sofern das "Öffnen mit..." ausgewählt wurde).

### Verbinde zum Multiserver

Sind einmal der Client und der Emulator gestartet, müssen sie nur noch miteinander verbunden werden. Gehe dazu in
deinen Archipelago-Ordner, dann zu `data/lua`, und füge das `connector_oot.lua` Script per Drag&Drop (ziehen und
fallen lassen) auf das EmuHawk-Fenster. (Alternativ kannst du die Lua-Konsole manuell öffnen, gehe dazu auf
`Script > Open Script` und durchsuche die Ordner nach `data/lua/connector_oot.lua`.)

Um den Client mit dem Multiserver zu verbinden, füge einfach `<Adresse>:<Port>` in das Textfeld ganz oben im
Client ein und drücke Enter oder "Connect" (verbinden). Wird ein Passwort benötigt, musst du es danach unten in das
Textfeld (für den Chat und Befehle) eingeben.
Alternativ kannst du auch in dem unterem Textfeld den folgenden Befehl schreiben:
`/connect <Adresse>:<Port> [Passwort]` (wie die Adresse und der Port lautet steht in dem Raum, oder wird von deinem
Host an dich weitergegeben.)
Beispiel: `/connect archipelago.gg:12345 Passw123`

Du bist nun bereit für dein Zeitreise-Abenteuer in Hyrule.
