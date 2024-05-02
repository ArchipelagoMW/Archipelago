# Pokémon Emerald Installations Guide

## Programvara som behövs

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Ett Engelsk Pokémon Emerald ROM, Archipelago kan inte hjälpa dig med detta
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 eller senare

### konfigurera BizHawk

När du har installerat Bizhawk, öppna `EmuHawk.exe` och ändra följande inställningar:

- Om du använder Bizhawk 2.7 eller 2.8, gå till `Config > Customize`. sen på "advanced tab" bytt Lua core från
`NLua+KopiLua` till `Lua+LuaInterface`, efteråt starta om EmuHawk. (Om du använder BizHawk 2.9, så kan du skippa detta steget.)
- Gå till `Config > Customize`, Tryck och markera "Run in background" inställningen för att förhindra att bli bortkopplad från klienten
 om du tabbar ur från EmuHawk.
 - Öppna en `.gba` fil i EmuHawk och gå till `Config > Controllers…` för att konfigurera dina tangentbords och handkontrolls inputs. 
 om du inte hittar `Controllers…`, I config menyn så starta bara något valfrit `.gba` ROM först.
- Överväg också att rensa keybind inställningar I `Config > Hotkeys…` som du inte tänkt använda, du kan trycka på en keybind
och använda ESC för att ta bort.

## Extra programvara

- [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest), används tillsamans med
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generera och patcha ett spel

1. Skapa din konfigurations fil (YAML). Du kan göra en via att använda
[Pokémon Emerald options page](../../../games/Pokemon%20Emerald/player-options).
2. Följ de allmänna Archipelago instruktionerna för hur man genererar ett spel [generating a game](../../Archipelago/setup/en#generating-a-game).
Detta kommer Generera en fil för dig. Din patch fil kommer ha `.apemerald` some sitt filnamnstillägg
3. Öppna `ArchipelagoLauncher.exe`
4. Välj "Open Patch" på vänster sidan, och välj sedan din patch fil
5. Om detta är första gången du patchar, så kommer du behöva välja ditt vanliga opatchade ROM.
6. En patchad `.gba` fil kommer skapas på samma plats där patch filen fanns.
7. Första gången du öppnar en patch med BizHawk klienten, kommer du också behöva bekräfta var `EmuHawk.exe` 
filen är installerad i din BizHawk map

Om du bara tänkt spela ett seed gjort för enspelarläge och du inte bryr dig om automatisk spårning eller tips, 
så behöver du inte göra något mer än det här. stäng klienten, och starta ditt patchade ROM med valfri emulator.
Vill du dock använda multvärlds funktionen eller andra Archipelago funktioner, så behöver du fortsätta med några steg till för BizHawk

## Anslut till en server

Som standard, När du öppnar du en patchad fil så görs steg 1-5 automatisk åt dig. Men det kan fortfarande va bra att veta hur allt funkar om
du till exempel behöver stänga och starta om något medans du spelar.

1. Pokemon Emerald använder Archipelago's BizHawk Klient. Om klienten fortfarande inte startat efter att du patchat ditt spel,
så kan du bara öppna den igen från launchern.
2. Dubbel kolla att EmuHawk faktiskt startat med den patchade ROM filen.
3. I EmuHawk, gå till `Tools > Lua Console`. Det är viktigt att du inte stänger denna Lua konsolen medans du spelar, dock är det ok att minimera för att dölja den
4. I Lua konsolen, Tryck på `Script > Open Script…`.
5. Leta reda på din Archipelago map och i den öppna `data/lua/connector_bizhawk_generic.lua`.
6. Emulatorn och klienten kommer så småningom koppla ihop med varanda. I klienten kommer du sedan kunna see om allt är
kopplat och att Pokemon Emerald startat ordentligt.
7. För att ansluta klienten till en server, skriv in din lobby adress och port i text fältet tex,`archipelago.gg:38281`
 längst upp i din klient och tryck sen på "connect"
 
Du borde nu kunna ta emot och skicka föremål. Du behöver göra dom hör stegen varje gång du vill ansluta.
du kan göra saker offline utan att behöva oroa dig; allt kommer synkronisera sig när du ansluter till servern igen

## Automatisk Spårning 

Pokémon Emerald har en fullt fungerande spårare med stöd för auto spårning

1. Laddaner [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest) och
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Plasera tracker pack filen i packs/ där du har PopTracker installerat.
3. Öppna PopTracker, och välj Pokemon Emerald.
4. För att automatisk spåra, tryck på "AP" symbolen längst upp
5. Skriv in Archipelago serverns uppgifter (Samma som du använda för att koppla Klienten), plats namn, och lösenord.