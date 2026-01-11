# Pokémon Kristall Setup Guide

## Benötigte Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Eine Englische (UE) Pokémon Kristall v1.0 oder v1.1 ROM. Die Archipelago-Community kann dies nicht bereitstellen.
    - Eine kompatible v1.1 ROM kann von der 3DS eShop Version des Spieles extrahiert werden.
- Eines der folgenden:
    - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 oder neuer. 2.10 wird empfohlen.
    - [mGBA](https://mgba.io) 0.10.3 oder neuer.
        - Du wirst auch das [mGBA to Bizhawk Client connector script](https://gist.github.com/gerbiljames/7b92dc62843794bd5902aad191b65efc) benötigen.
          Füge es zu `data/lua/` deiner Archipelago-Installation hinzu.
          
## Bizhawk konfigurieren

Sobald du Bizhawk installiert hast, öffne `EmuHawk.exe` und ändere die folgenden Einstellungen:

- Auf BizHawk 2.8 oder älter, navigiere zu `Config -> Customize` und drücke auf den `Advanced` Reiter. Ändere den Lua core von `NLua+KopiLua` zu `Lua+LuaInterface`, dann starte EmuHawk neu. Dieser Schritt ist bei Bizhawk 2.9 und neuer nicht nötig.
- Unter Config > Customize > Advanced, stelle sicher, dass der Kasten für AutoSaveRAM ausgefüllt ist und drücke auf den 5s-Knopf. Dies verrinert die Chance Speicherstände bei einem Emulator-Crash zu verlieren.
- Unter `Config -> Customize`, schalte `Run in background` ein. Dies verhindert, dass das Spiel die Verbindung zum Client verliert, wenn du heraustabbst.
- Um Controller-Einstellungen zu konfigurieren, öffne ein GameBoy oder ein GameBoy Color Spiel (`.gb` oder `.gbc`) und navigiere zu `Config -> Controllers...`. Dieses Menü ist eventuell nicht verfügbar, wenn noch kein Spiel geöffnet wurde.
- Stelle sicher, dass `Config -> Preferred Cores -> GB in SGB` ausgestellt ist.

### mGBA konfigurieren

Sobald du mGBA installiert hast, öffne `mGBA.exe` und navigiere zu `Settings -> Preferences` und ändere die folgenden Einstellungen:

- In `Game Boy`, under Models, select `Game Boy Color (CGB)` for all models.

## Optionale Software

[Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) zu Benutzen mit [PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Ein Spiel generieren und patchen

1. Füge `pokemon_crystal.apworld` zu deinem `custom_worlds`-Ordner in deiner Archipelago-Installation hinzu. Es sollte nicht in `lib\worlds` sein.
2. Erstelle deine Einstellungsdatei (YAML). Du kannst eine erstellen, indem du `Generate Templates` im Archipelago-Launcher auswählst. Von da aus, kannst du die `.yaml` in jeglichem Text-Editor bearbeiten.
3. Folge der allgemeinen Archipelago-Einleitung [wie man ein Spiel auf deiner lokalen Installation generiert](https://archipelago.gg/tutorial/Archipelago/setup/en#on-your-local-installation).
   Dies generiert eine output-Datei für dich. Deine Patch-Datei wird eine `.apcrystal`-Endung besitzen und befindet sich innerhalb dieser output-Datei. Alternativ kannst du diese Patch-Datei von der Seite deines Multiworlds-Room herunterladen, solltest du dein Spiel auf archipelago.gg hosten.
4. Öffne `ArchipelagoLauncher.exe`
5. Drücke "Open Patch" von der initialen Liste oder unter `Misc -> Open Patch` und wähle deine Patch-Datei aus.
6. Falls dies dein erstes Mal ist, wirst du aufgefordert deine Vanilla-ROM auszuwählen.
7. Eine gepatchte `.gbc`-Datei wird im gleichen Ort wie deine Patch-Datei erstellt.
8. Bei deinem ersten Mal wirst du auch aufgefordert `EmuHawk.exe` in deiner BizHawk-Installation auszuwählen. mGBA-Nutzer können `Cancel` auswählen und mGBA manuell öffnen.

Falls du eine Einzelspieler-Multiworld spielst und dir Autotracking und Hinweise egal sind, kannst du hier aufhören, den Client schließen und die gepatchte ROM in irgendeinem Emulator öffnen.
Falls du jedoch eine Multi-Slot-Multiworld spielst oder andere Archipelago-Features benutzen willst, fahre mit der Anleitung fort und benutze BizHawk oder mGBA als Emulator.

# Mit einem Server verbinden

Standardmäßig werden die gleich aufgeführten Schritte 1-5 automatisch ausgeführt, wenn du eine Patch-Datei doppelklickst.
Trotzdem solltest du diese im Hinterkopf behalten, nur für den Notfall, falls du während einer Sitzung irgendeines der Fenster schließt.

1. Pokémon Kristall nutzt Archipelago's Bizhawk Client. Falls der Client nicht noch vom Patchen deiner ROM offen ist, kannst du ihn vom Launcher aus starten.
2. Stelle sicher, dass EmuHawk oder mGBA die gepatchte ROM abspielt.
3. In EmuHawk:
    - Gehe zu `Tools > Lua Console`. Dieses Fenster muss während des Spielens offen bleiben.
    - Im Lua Console Fenster, gehe zu `Script > Open Script...`.
    - Navigiere zu deinem Archipelago-Installations-Ordner und öffne `data/lua/connector_bizhawk_generic.lua`.
4. In mGBA:
    - Gehe zu `Tools > Scripting...`. Dieses Fenster muss während des Spielens offen bleiben.
    - Gehe zu `File > Load Script...`.
    - Navigiere zu deinem Archipelago-Installations-Ordner und öffne `data/lua/connector_bizhawkclient_mgba.lua`.
5. Der Emulator und Client werden dann nach einer kurzen Weile sich automatisch miteinander verbinden. Das Bizhawk Client Fenster sollte zeigen, dass es verbunden ist und Pokémon Kristall erkennt.

Du solltest nun in der Lage sein, Items zu senden und zu bekommen. Du musst diese Schritte jedes Mal wiederholen, wenn du dich erneut verbinden willst.
Es ist vollkommen sicher Fortschritt offline zu machen; alles wird sich erfolgreich re-synchronisieren, sobald du dich wieder verbindest.

## Auto-Tracking

Pokémon Kristall hat einen voll-funktionalen Karten Tracker, der Auto-Tracking unterstützt.

1. Lade [Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) und
   [PopTracker](https://github.com/black-sliver/PopTracker/releases) herunter.
2. Schiebe das Tracker-Pack in den `packs/`-Ordner deiner Poptracker-Installation.
3. Öffne PopTracker und wähle das Pokémon Kristall Pack aus.
4. Um Autotracking zu aktivieren, drücke auf das "AP"-Symbol am oberen Ende des Programms.
5. Gebe die Archipelago Server Addresse (diejenige die in deinem Client auch steht), deinen Slotnamen, und ein Password ein, falls dein Raum ein Passwort hat. Falls dein Raum kein Passwort hat, lass das Passwort-Feld leer.