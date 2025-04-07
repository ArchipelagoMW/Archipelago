# Minecraft Randomizer Uppsättningsguide

## Nödvändig Mjukvara

### Server Värd

- [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)

### Spelare

- [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)

## Installationsprocedurer

### Tillägnad

Bara en person behöver göra denna uppsättning och vara värd för en server för alla andra spelare att koppla till.

1. Ladda ner 1.16.5 **Minecraft Forge** installeraren från länken ovanför och se till att ladda ner den senaste
   rekommenderade versionen.

2. Kör `forge-1.16.5-xx.x.x-installer.jar` filen och välj **installera server**.
    - På denna sida kommer du också välja vart du ska installera servern för att komma ihåg denna katalog. Detta är
      viktigt för nästa steg.

3. Navigera till vart du har installerat servern och öppna `forge-1.16.5-xx.x.x-installer.jar`
    - Under första serverstart så kommer den att stängas ner och fråga dig att acceptera Minecrafts EULA. En ny fil
      kommer skapas vid namn `eula.txt` som har en länk till Minecrafts EULA, och en linje som du behöver byta
      till `eula=true` för att acceptera Minecrafts EULA.
    - Detta kommer skapa de lämpliga katalogerna för dig att placera filerna i de följande steget.

4. Placera `aprandomizer-x.x.x.jar` länken ovanför i `mods` mappen som ligger ovanför installationen av din forge
   server.
    - Kör servern igen. Den kommer ladda up och generera den nödvändiga katalogen `APData` för när du är redo att spela!

### Grundläggande Spelaruppsättning

- Köp och installera Minecraft från länken ovanför.

  **Du är klar**.

  Andra spelare behöver endast ha en 'Vanilla' omodifierad version av Minecraft för att kunna spela!

### Avancerad Spelaruppsättning

***Detta är inte nödvändigt för att spela ett slumpmässigt Minecraftspel.***
Dock så är det rekommenderat eftersom det hjälper att göra upplevelsen mer trevligt.

#### Rekommenderade Moddar

- [JourneyMap](https://www.curseforge.com/minecraft/mc-mods/journeymap) (Minimap)


1. Installera och Kör Minecraft från länken ovanför minst en gång.
2. Kör `forge-1.16.5-xx.x.x-installer.jar` filen och välj **installera klient**.
    - Starta Minecraft Forge minst en gång för att skapa katalogerna som behövs för de nästa stegen.
3. Navigera till din Minecraft installationskatalog och placera de önskade moddarna med `.jar`  i `mods` -katalogen.
    - Standardinstallationskatalogerna är som följande;
        - Windows `%APPDATA%\.minecraft\mods`
        - macOS `~/Library/Application Support/minecraft/mods`
        - Linux `~/.minecraft/mods`

## Konfigurera Din YAML-fil

### Vad är en YAML-fil och varför behöver jag en?

Din YAML-fil behåller en uppsättning av konfigurationsalternativ som ger generatorn med information om hur den borde
generera ditt spel. Varje spelare i en multivärld kommer behöva ge deras egen YAML-fil. Denna uppsättning tillåter varje
spelare att an njuta av en upplevelse anpassade för deras smaker, och olika spelare i samma multivärld kan ha helt olika
alternativ.

### Vart kan jag få tag i en YAML-fil?

En grundläggande Minecraft YAML kommer se ut så här.

```yaml
description: Template Name
# Ditt spelnamn. Mellanslag kommer bli omplacerad med understräck och det är en 16-karaktärsgräns.
name: YourName
game: Minecraft
accessibility: full
progression_balancing: 0
advancement_goal:
  few: 0
  normal: 1
  many: 0
combat_difficulty:
  easy: 0
  normal: 1
  hard: 0
include_hard_advancements:
  on: 0
  off: 1
include_insane_advancements:
  on: 0
  off: 1
include_postgame_advancements:
  on: 0
  off: 1
shuffle_structures:
  on: 1
  off: 0
```


## Gå med i ett Multivärld-spel

### Skaffa din Minecraft data-fil

**Endast en YAML-fil behöver användats per Minecraft-värld oavsett hur många spelare det är som spelar.**

När du går med it ett Multivärld spel så kommer du bli ombedd att lämna in din YAML-fil till personen som värdar. När
detta är klart så kommer värden att ge dig antingen en länk till att ladda ner din data-fil, eller mer en zip-fil som
innehåller allas data-filer. Din data-fil borde ha en `.apmc` -extension.

Lägg din data-fil i dina forge-servrar `APData` -mapp. Se till att ta bort alla tidigare data-filer som var i där förut.

### Koppla till Multiservern

Efter du har placerat din data-fil i `APData` -mappen, starta forge-servern och se till att you har OP-status genom att
skriva `/op DittAnvändarnamn` i forger-serverns konsol innan du kopplar dig till din Minecraft klient. När du är inne i
spelet, skriv `/connect <AP-Address> (<Lösenord>)` där `<AP-Address>` är addressen av
Archipelago-servern. `(<Lösenord>)` är endast nödvändigt om Archipelago-servern som du använder har ett tillsatt
lösenord.

### Spela spelet

När konsolen har informerat att du har gått med i rummet så är du redo att börja spela. Grattis att du har lykats med
att gått med i ett Multivärld-spel! Vid detta tillfälle, alla ytterligare Minecraft-spelare må koppla in till din
forge-server.

