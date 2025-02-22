# Subnautica Randomizer Einrichtungsanleitung

## Erforderliche Software

- Subnautica von dem: [Steam Store](https://store.steampowered.com/app/264710/Subnautica/) | [Epic Games Store](https://store.epicgames.com/p/subnautica)
- Archipelago-Mod für Subnautica  
  von der: [Subnautica Archipelago Mod Releases Seite](https://github.com/Berserker66/ArchipelagoSubnauticaModSrc/releases)

## Installationsanleitung

1. Entpacke die Archipelago-Mod in deinen Subnautica-Ordner, sodass `Subnautica/BepInEx` ein gültiger Pfad ist.

2. Starte Subnautica. Du solltest im Hauptmenü oben links ein Verbindungsformular mit drei Eingabefeldern sehen.

**Falls du Linux verwendest**, füge ``WINEDLLOVERRIDES="winhttp=n,b" %command%`` zu den Startargumenten von Subnautica in Steam hinzu. Falls du Subnautica über eine andere Plattform erworben hast, kannst du es entweder in Steam als ein Steam-fremdes-Spiel hinzufügen und die eben genannten Startoptionen nutzen oder über `winecfg` die DLL-Überschreibung setzen.

## Verbindung einrichten

Verwende das Verbindungsformular im Hauptmenü von Subnautica, um deine Verbindungsinformationen einzugeben und dich mit einer Archipelago-Multiwelt zu verbinden.  
Die Verbindungsinformationen bestehen aus:
- Host: Die vollständige URL, zu der du dich verbinden willst, z. B. `archipelago.gg:38281`.
- Spielername: Dein Name in der Multiwelt. Wird auch als „Slot-Name“ bezeichnet und ist der Name, den du bei der Erstellung deiner Optionen eingegeben hast.
- Passwort: Optionales Passwort – leer lassen, falls kein Passwort festgelegt wurde.

Nachdem die Verbindung erfolgreich hergestellt wurde, starte ein neues Spiel. Du solltest nun Chatnachrichten von Archipelago sehen können, wie z.B. eine Meldung, dass du einer Multiwelt beigetreten bist.

## Fortsetzen eines Archipelago Spielstandes

Archipelago Spielstände speichern die Verbindungsinformationen, die du eingegeben hast und versuchen sich automatisch, beim Laden des Spielstands mit der Multiwelt zu verbinden. 
Falls die Verbindungsinformationen nicht mehr gültig sind (z. B. wenn sich die IP-Adresse oder der Port des Servers geändert hat), musst du die neuen/korrekten Verbindungsinformationen vor dem Laden des Spielstandes im Hauptmenü erneut eingeben.

**Warnung:** Es wird derzeit nicht überprüft, ob dein gespeicherter Spielstand zur Multiwelt gehört, mit der du dich versuchst zu verbinden. Bitte stell selbst sicher, das der Spielstand zur Multiwelt gehört, bevor du dich versuchst zu verbinden.

## Konsolenbefehle

Die Mod fügt folgende Konsolenbefehle hinzu:
- `say` sendet den nachfolgenden Text als Chatnachricht an Archipelago.
    - Beispiel: Um den [`!hint`-Befehl](/tutorial/Archipelago/commands/en#remote-commands) zu nutzen, tippe `say !hint`.
- `silent` schaltet Archipelago-Nachrichten ein oder aus.
- `tracker` wechselt zwischen den Einstellungen des In-Game-Trackers, der den nächsten Bereich anzeigt, wo noch nichts eingesammelt wurde.
- `deathlink` schaltet Death-Link ein oder aus.

Um die Konsole in Subnautica zu aktivieren, drücke `Shift+Enter`.

## Bekannte Probleme

- Beim Spielen eines normalen (Vanilla) Spielstandes, während die Mod installiert ist, werden alle Scan-Einträge des Spielstandes überschrieben.
- Beim Zurückkehren ins Hauptmenü wird der Mod-Status nicht korrekt zurückgesetzt, wenn du von diesem Punkt aus versuchst ein Spielstand zu laden treten mehrere Fehler auf.
  Falls du einen Spielstand neu laden möchtest, ist es empfohlen, das gesamte Spiel neu zu starten.
- Beim Laden eines Spielstandes mit ungültigen Verbindungsinformationen, ohne vorher gültige Daten im Hauptmenü eingegeben zu haben, hängt sich das Spiel im Ladebildschirm auf.

## Fehlerbehebung

Falls du das Verbindungsformular im Hauptmenü nicht siehst, überprüfe, ob eine Datei mit dem Namen `LogOutput.txt` im Verzeichnis `Subnautica/BepInEx` vorhanden ist.
Wenn dies nicht der Fall ist, ist BepInEx nicht korrekt installiert.
Andernfalls öffne die Datei und suche nach der Zeile `Plugin Archipelago is loaded!`, wenn diese Zeile nicht existiert, konnte BepIx die Archipelago-Mod nicht finden. Überprüfe sicherheitshalber die Richtigkeit deiner Installationspfade der beiden Mods.
