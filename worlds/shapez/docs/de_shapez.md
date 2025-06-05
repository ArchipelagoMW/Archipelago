# shapez

## Was für ein Spiel ist das?

shapez ist ein Automatisierungsspiel, in dem du Formen aus zufällig generierten Vorkommen in einer endlosen Welt 
extrahierst, zerschneidest, rotierst, stapelst, anmalst und schließlich zum Zentrum beförderst, um Level abzuschließen
und Upgrades zu kaufen. Das Tutorial beinhaltet 26 Level, in denen du (fast) immer ein neues Gebäude oder eine neue
Spielmechanik freischaltest. Danach folgen endlos weitere Level mit zufällig generierten Vorgaben. Um das Spiel bzw.
deine Gebäude schneller zu machen, kannst du bis zu 1000 Upgrades (pro Kategorie) kaufen.

## Wo ist die Optionen-Seite?

Die [Spieler-Optionen-Seite für dieses Spiel](../player-options) enthält alle Optionen zum Erstellen und exportieren 
einer YAML-Datei.
Zusätzlich gibt es zu diesem Spiel "Datenpaket-Einstellungen", die du nach 
[dieser Anleitung](/tutorial/shapez/datapackage_settings/de) einstellen kannst.

## Inwiefern wird das Spiel randomisiert?

Alle Belohnungen aus den Tutorial-Level (das Freischalten von Gebäuden und Spielmechaniken) und Verbesserungen durch
Upgrades werden dem Itempool der Multiworld hinzugefügt. Außerdem werden, wenn so in den Spieler-Optionen festgelegt,
die Bedingungen zum Abschließen eines Levels und zum Kaufen der Upgrades randomisiert.

## Was ist das Ziel von shapez in Archipelago?

Da das Spiel eigentlich kein konkretes Ziel (nach dem Tutorial) hat, kann man sich zwischen (momentan) 4 verschiedenen
Zielen entscheiden:
1. Vanilla: Schließe Level 26 ab (eigentlich das Ende des Tutorials).
2. MAM: Schließe ein bestimmtes Level nach Level 26 ab, das zuvor in den Spieler-Optionen festgelegt wurde. Es ist
empfohlen, eine Maschine zu bauen, die alles automatisch herstellt ("Make-Anything-Machine", kurz MAM).
3. Even Fasterer: Kaufe alle Upgrades bis zu einer in den Spieler-Optionen festgelegten Stufe (nach Stufe 8).
4. Efficiency III: Liefere 256 Blaupausen-Formen pro Sekunde ins Zentrum.

## Welche Items können in den Welten anderer Spieler erscheinen?

- Freischalten verschiedener Gebäude
- Blaupausen freischalten
- Große Upgrades (addiert 1 zum Geschwindigkeitsmultiplikator)
- Kleine Upgrades (addiert 0.1 zum Geschwindigkeitsmultiplikator)
- Andere ungewöhnliche Upgrades (optional)
- Verschiedene Bündel, die bestimmte Formen enthalten
- Fallen, die bestimmte Formen aus dem Zentrum dränieren (ja, das Wort gibt es)
- Fallen, die zufällige Gebäude oder andere Spielmechaniken betreffen

## Was ist eine Location / ein Check?

- Level (minimum 1-25, bis zu 499 je nach Spieler-Optionen, mit zusätzlichen Checks für Level 1 und 20)
- Upgrades (minimum Stufen II-VIII (2-8), bis zu D (500) je nach Spieler-Optionen)
- Bestimmte Formen mindestens einmal ins Zentrum liefern ("Shapesanity", bis zu 1000 zufällig gewählte Definitionen)
- Errungenschaften (bis zu 45)

## Was passiert, wenn der Spieler ein Item erhält?

Ein Pop-Up erscheint, das das/die erhaltene(n) Item(s) und eventuell weitere Informationen auflistet.

## Was bedeuten die Namen dieser ganzen Shapesanity Dinger?

Hier ist ein Spicker für die Englischarbeit (bloß nicht dem Lehrer zeigen):

![image](/static/generated/docs/shapez/shapesanity_full.png)

## Kann ich auch weitere Mods neben dem AP Client installieren?

Zurzeit wird Kompatibilität mit anderen Mods nicht unterstützt, aber niemand kann dich davon abhalten, es trotzdem zu
versuchen. Mods, die das Gameplay verändern, werden wahrscheinlich nicht funktionieren, indem sie das Laden der 
jeweiligen Mods verhindern oder das Spiel zum Abstürzen bringen, während einfache QoL-Mods vielleicht problemlos
funktionieren könnten. Wenn du es versuchst, dann also auf eigene Gefahr.

## Hast du wirklich eine deutschsprachige Infoseite geschrieben, obwohl man sie aktuell nur über Umwege erreichen kann und du eigentlich an dem Praktikumsportfolio arbeiten solltest?

Ja
