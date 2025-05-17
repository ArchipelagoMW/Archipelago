# Anleitung zum Ändern der maximalen Anzahl an Locations in shapez

## Wo finde ich die Einstellungen zum Erhöhen/Verringern der maximalen Anzahl an Locations?

Die Maximalwerte von `goal_amount` und `shapesanity_amount` sind fest eingebaute Einstellungen, die das Datenpaket des 
Spiels beeinflussen. Sie sind in einer Datei names `options.json` innerhalb der APWorld festgelegt. Durch das Ändern 
dieser Werte erschaffst du eine custom APWorld, die nur auf deinem PC existiert.

## Wie du die Datenpaket-Einstellungen änderst

Diese Anleitung ist für erfahrene Nutzer und kann in nicht richtig funktionierender Software resultieren, wenn sie nicht
ordnungsgemäß befolgt wird. Anwendung auf eigene Gefahr.

1. Navigiere zu `<AP-Installation>/lib/worlds`.
2. Benenne `shapez.apworld` zu `shapez.zip` um.
3. Öffne die Zip-Datei und navigiere zu `shapez/data/options.json`.
4. Ändere die Werte in dieser Datei nach Belieben und speichere die Datei.
   - `max_shapesanity` kann nicht weniger als `4` sein, da dies die benötigte Mindestanzahl zum Verhindern von 
      FillErrors ist.
   - `max_shapesanity` kann auch nicht mehr als `75800` sein, da dies die maximale Anzahl an möglichen Shapesanity-Namen
     ist. Ansonsten könnte die Generierung der Multiworld fehlschlagen.
   - `max_levels_and_upgrades` kann nicht weniger als `27` sein, da dies die Mindestanzahl für das `mam`-Ziel ist.
5. Schließe die Zip-Datei und benenne sie zurück zu `shapez.apworld`.

## Warum muss ich das ganze selbst machen?

Alle Spiele in Archipelago müssen eine Liste aller möglichen Locations **unabhängig der Spieler-Optionen** 
bereitstellen. Diese Listen aller in einer Multiworld inkludierten Spiele werden in den Daten der Multiworld gespeichert
und an alle verbundenen Clients gesendet. Je mehr mögliche Locations, desto größer das Datenpaket. Und mit ~80000 
möglichen Locations hatte shapez zu einem gewissen Zeitpunkt ein (von der Datenmenge her) größeres Datenpaket als alle 
supporteten Spiele zusammen. Um also diese Datenmenge zu reduzieren wurden die ausgeschriebenen 
Shapesanity-Locations-Namen (`Shapesanity Uncolored Circle`, `Shapesanity Blue Rectangle`, ...) durch standardisierte 
Namen (`Shapesanity 1`, `Shapesanity 2`, ...) ersetzt. Durch das Ändern dieser Maximalwerte, und damit das Erstellen 
einer custom APWorld, kannst du die Anzahl der möglichen Locations erhöhen, wirst aber auch gleichzeitig das Datenpaket 
vergrößern.
