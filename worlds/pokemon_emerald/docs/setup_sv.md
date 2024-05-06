# Pokémon Emerald Installations Guide

## Programvara som behövs

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Ett Engelsk Pokémon Emerald ROM, Archipelago kan inte hjälpa dig med detta.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 eller senare

### konfigurera BizHawk

När du har installerat BizHawk, öppna `EmuHawk.exe` och ändra följande inställningar:

- Om du använder BizHawk 2.7 eller 2.8, gå till `Config > Customize`. Sen på "Advanced Tab" bytt Lua core från
`NLua+KopiLua` till `Lua+LuaInterface`, efteråt starta om EmuHawk. (Använder du BizHawk 2.9, kan du skippa detta.)
- Gå till `Config > Customize`, Markera "Run in background" inställningen för att förhindra bortkoppling från
klienten om du tabbar ur från EmuHawk.
- Öppna en `.gba` fil i EmuHawk och gå till `Config > Controllers…` för att konfigurera dina inputs.
om du inte hittar `Controllers…`, starta valfrit `.gba` ROM först.
- Överväg att rensa keybinds i `Config > Hotkeys…` som du inte tänkt använda, Välj en keybind och tryck på ESC
för att rensa bort den.

## Extra programvara

- [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest),
används tillsammans med
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generera och patcha ett spel

1. Skapa din konfigurations fil (YAML). Du kan göra en via att använda
[Pokémon Emerald options hemsida](../../../games/Pokemon%20Emerald/player-options).
2. Följ de allmänna Archipelago instruktionerna för att
[Generera ett spel](../../Archipelago/setup/en#generating-a-game).
Detta kommer Generera en fil för dig. Din patch fil kommer ha `.apemerald` some sitt filnamnstillägg
3. Öppna `ArchipelagoLauncher.exe`
4. Välj "Open Patch" på vänster sidan, och välj din patch fil.
5. Om detta är första gången du patchar, så kommer du behöva välja var ditt vanliga ROM är.
6. En patchad `.gba` fil kommer skapas på samma plats som patch filen.
7. Första gången du öppnar en patch med BizHawk klienten, kommer du också behöva bekräfta var `EmuHawk.exe`
filen är installerad i din BizHawk map.

Om du bara tänkt spela själv och du inte bryr dig om automatisk spårning eller tips, så kan du stoppa här, stäng
klienten, och starta ditt patchade ROM med valfri emulator. Dock, för multvärlds funktionen eller andra Archipelago
funktioner, fortsätt nedanför med BizHawk.

## Anslut till en server

Som standard, Öppnar du en patchad fil så görs steg 1-5 automatisk åt dig. Även om det är så, kom ihåg dom om ifall
du till exempel behöver stänga och starta om något medans du spelar.

1. Pokemon Emerald använder Archipelago's BizHawk Klient. Om klienten inte startat efter att du patchat ditt spel,
så kan du bara öppna den igen från launchern.
2. Dubbel kolla att EmuHawk faktiskt startat med den patchade ROM filen.
3. I EmuHawk, gå till `Tools > Lua Console`. Denna Lua konsolen måste va igång medans du spelar.
4. I Lua konsolen, Tryck på `Script > Open Script…`.
5. Leta reda på din Archipelago map och i den öppna `data/lua/connector_bizhawk_generic.lua`.
6. Emulatorn och klienten kommer så småningom koppla ihop. I BizHawk klienten kommer du kunna see om allt är
kopplat och att Pokemon Emerald är igenkänt.
7. För att ansluta klienten till en server, skriv in din lobby adress och port i text fältet tex,
`archipelago.gg:38281`
längst upp i din klient och tryck sen på "Connect".

Du borde nu kunna ta emot och skicka föremål. Du behöver göra dom hör stegen varje gång du vill ansluta igen. Det är
helt okej att göra saker offline utan att behöva oroa sig; allt kommer synkronisera sig när du ansluter till servern
igen.

## Automatisk Spårning

Pokémon Emerald har en fullt fungerande spårare med stöd för auto spårning.

1. Ladda ner [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest)
och
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Placera tracker pack filen i packs/ där du har PopTracker installerat.
3. Öppna PopTracker, och välj Pokemon Emerald.
4. För att automatisk spåra, tryck på "AP" symbolen längst upp.
5. Skriv in Archipelago serverns uppgifter (Samma som du använda för att koppla Klienten), plats namn, och lösenord.
